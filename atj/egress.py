"""The egress proxy a network allowlist needs to mean anything.

Container flags cannot filter by destination. `--network none` is total and
`--network <bridge>` is unrestricted, so honouring an event's
`network_allowlist` with runtime flags alone would grant exactly the access it
was written to withhold. `atj/sandbox.py` refuses that combination rather than
pretending, and advisory 5 of `docs/final-audit.md` recorded the consequence: a
configured allowlist could not be used at all, so that path was never exercised.

This module is the missing half. Two networks and one proxy:

    submission container      atj-egress (internal: no route off the host)
      HTTPS_PROXY ----------> atj-egress-proxy
                                |  tinyproxy, FilterDefaultDeny Yes
                                |  one anchored regex per allowed host
                                v
                              podman (default bridge: has a route out)

The submission cannot reach anything directly -- an internal network has no
outbound route and no external DNS -- so everything it can reach, the proxy
decides. The proxy is the only thing on the sandbox network with a way out.

This is a destination filter for code that is being observed, not a boundary
against a determined escape. `atj sandbox preflight` still judges the isolation,
and a rootful runtime is still a rootful runtime.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from .errors import SafetyError

SANDBOX_NETWORK = "atj-egress"
OUTBOUND_NETWORK = "podman"
PROXY_NAME = "atj-egress-proxy"
PROXY_IMAGE = "localhost/atj/egress-proxy:1"
PROXY_PORT = 8888
PROBE_TIMEOUT = 20
BUILD_TIMEOUT = 300

# A host an event may reach. Deliberately strict: no scheme, no port, no path,
# no bare address, and no wildcard beyond a leading `*.`. Every character of
# laxity here is a destination nobody authorized.
# The final label must be alphabetic, which is what refuses a bare address:
# `10.0.0.1` is a valid hostname shape and not a name this filter can match,
# because a proxy filters the name in a request and a submission reaching an
# address directly never sends one.
_HOST = re.compile(
    r"^(?:\*\.)?(?:(?!-)[a-z0-9-]{1,63}\.)+(?!-)[a-z]{2,63}$", re.IGNORECASE
)

CONTAINERFILE = """FROM docker.io/library/alpine:3.20
RUN apk add --no-cache tinyproxy
COPY tinyproxy.conf /etc/tinyproxy/tinyproxy.conf
COPY filter /etc/tinyproxy/filter
EXPOSE {port}
ENTRYPOINT ["tinyproxy", "-d", "-c", "/etc/tinyproxy/tinyproxy.conf"]
"""


@dataclass(frozen=True)
class ProxyState:
    """What is running right now, read from the runtime rather than remembered."""

    runtime: str
    running: bool
    allowlist: tuple[str, ...]
    url: str

    def to_dict(self) -> dict:
        return {
            "runtime": self.runtime, "running": self.running,
            "allowlist": list(self.allowlist), "url": self.url,
        }


def proxy_url(address: str | None = None) -> str:
    """The proxy's URL, by address.

    An address rather than a name: the sandbox network has no resolver, on
    purpose, so a submission cannot look up anything at all -- including the
    proxy. The address is read back from the runtime after the proxy starts.
    """
    return f"http://{address or PROXY_NAME}:{PROXY_PORT}"


def proxy_address(runtime: str) -> str:
    """The proxy's IP on the sandbox network, read from the runtime."""
    inspected = _run([
        runtime, "inspect", PROXY_NAME,
        "--format", f'{{{{(index .NetworkSettings.Networks "{SANDBOX_NETWORK}").IPAddress}}}}',
    ])
    if inspected is None or inspected.returncode != 0:
        return ""
    return (inspected.stdout or "").strip()


def normalize_allowlist(entries: Iterable[str]) -> tuple[str, ...]:
    """Validate and canonicalize an event's allowlist.

    An entry that is not a bare hostname is refused rather than coerced. An
    official who writes `https://pypi.org/simple/` means one host, not a path,
    and a filter that had to widen the entry to accept it would grant more than
    was approved.
    """
    seen: list[str] = []
    for raw in entries:
        entry = str(raw).strip().lower()
        if not entry:
            continue
        if not _HOST.match(entry):
            raise SafetyError(
                f"network_allowlist entry {raw!r} is not a bare hostname. Write "
                f"`pypi.org` or `*.pythonhosted.org`: no scheme, port, path or bare "
                f"address. An entry this filter cannot express exactly would have to be "
                f"widened, and widening an allowlist grants access nobody approved."
            )
        if entry not in seen:
            seen.append(entry)
    if not seen:
        raise SafetyError(
            "an egress proxy with an empty allowlist reaches nothing; run with no "
            "network instead and record the limitation"
        )
    return tuple(seen)


def filter_rules(allowlist: Sequence[str]) -> str:
    """tinyproxy's destination filter: one anchored regex per allowed host.

    Anchored at both ends, so `pypi.org` does not also permit
    `pypi.org.attacker.example`. A leading `*.` becomes a subdomain match whose
    suffix must still be the whole tail of the name.
    """
    lines = []
    for entry in allowlist:
        if entry.startswith("*."):
            lines.append(rf"^([a-z0-9-]+\.)+{re.escape(entry[2:])}$")
        else:
            lines.append(rf"^{re.escape(entry)}$")
    return "\n".join(lines) + "\n"


def proxy_config() -> str:
    return "\n".join([
        f"Port {PROXY_PORT}",
        "Listen 0.0.0.0",
        "Timeout 120",
        # Who may use the proxy. The only reachable clients are containers on the
        # internal sandbox network, which has no route in from anywhere else.
        "Allow 0.0.0.0/0",
        "FilterDefaultDeny Yes",
        'Filter "/etc/tinyproxy/filter"',
        "FilterExtended On",
        "FilterCaseSensitive Off",
        # CONNECT is how TLS gets through a proxy, and these are the only ports it
        # may be asked for. Without this, CONNECT to any port would be permitted.
        "ConnectPort 443",
        "ConnectPort 80",
        "DisableViaHeader Yes",
        "LogLevel Notice",
        "",
    ])


def _run(command: Sequence[str], timeout: int = PROBE_TIMEOUT) -> subprocess.CompletedProcess | None:
    try:
        return subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None


def _require_runtime(runtime: str | None) -> str:
    chosen = runtime or "podman"
    if not shutil.which(chosen):
        raise SafetyError(
            f"{chosen} is not on PATH, so no proxy can be started and a configured "
            f"network allowlist cannot be honoured. Run with no network instead."
        )
    return chosen


def _network_facts(runtime: str, name: str) -> dict:
    inspected = _run([runtime, "network", "inspect", name])
    if inspected is None or inspected.returncode != 0:
        return {}
    try:
        return json.loads(inspected.stdout)[0]
    except (json.JSONDecodeError, IndexError, TypeError):
        return {}


def ensure_networks(runtime: str) -> None:
    """The internal sandbox network, and the outbound one the proxy uses.

    The sandbox network is created `--internal --disable-dns`, and both halves
    matter.

    `--internal` gives it no route off the host, which is what makes the proxy
    the only way out. `--disable-dns` removes the runtime's own resolver from it,
    for two reasons. A submission with no resolver cannot look anything up, so
    the proxy is the only thing that can turn a name into an address -- and a
    proxy attached to an internal network *with* DNS inherits that resolver
    first in its own `/etc/resolv.conf`, where it answers NXDOMAIN for every
    external name and the real upstreams below it are never tried. That produced
    a proxy which refused allowed hosts with a 500 and looked, from the outside,
    exactly like a working filter.

    Both properties are asserted on an existing network, and a network of this
    name that has either one wrong is recreated rather than trusted.
    """
    listed = _run([runtime, "network", "ls", "--format", "{{.Name}}"])
    names = set((listed.stdout or "").split()) if listed else set()

    if SANDBOX_NETWORK in names:
        facts = _network_facts(runtime, SANDBOX_NETWORK)
        if not facts.get("internal", False) or facts.get("dns_enabled", False):
            removed = _run([runtime, "network", "rm", "--force", SANDBOX_NETWORK])
            if removed is None or removed.returncode != 0:
                raise SafetyError(
                    f"network {SANDBOX_NETWORK!r} is not internal, or has DNS enabled, and "
                    f"could not be removed: "
                    + ((removed.stderr or "").strip() if removed else "no response")
                    + ". A submission attached to it would reach the network directly, so "
                      "this refuses rather than running against it."
                )
            names.discard(SANDBOX_NETWORK)

    if SANDBOX_NETWORK not in names:
        created = _run([
            runtime, "network", "create", "--internal", "--disable-dns", SANDBOX_NETWORK
        ])
        if created is None or created.returncode != 0:
            raise SafetyError(
                f"could not create the internal network {SANDBOX_NETWORK!r}: "
                + ((created.stderr or "").strip() if created else "runtime did not respond")
            )
    if OUTBOUND_NETWORK not in names:
        _run([runtime, "network", "create", OUTBOUND_NETWORK])


def build_image(runtime: str, allowlist: Sequence[str]) -> str:
    """Build the proxy image with this allowlist baked into it.

    In the image rather than a mount, so the filter a running proxy enforces
    cannot be edited underneath a run in progress.
    """
    with tempfile.TemporaryDirectory() as directory:
        context = Path(directory)
        (context / "Containerfile").write_text(
            CONTAINERFILE.format(port=PROXY_PORT), encoding="utf-8"
        )
        (context / "tinyproxy.conf").write_text(proxy_config(), encoding="utf-8")
        (context / "filter").write_text(filter_rules(allowlist), encoding="utf-8")
        built = _run(
            [runtime, "build", "--quiet", "--tag", PROXY_IMAGE, str(context)],
            timeout=BUILD_TIMEOUT,
        )
    if built is None or built.returncode != 0:
        raise SafetyError(
            "could not build the egress proxy image: "
            + ((built.stderr or built.stdout).strip() if built else "runtime did not respond")
        )
    return PROXY_IMAGE


def outbound_resolvers(runtime: str, image: str = PROXY_IMAGE) -> tuple[str, ...]:
    """The nameservers a container on the outbound network is given.

    Attached to an internal network *and* an outbound one, a container's
    `/etc/resolv.conf` holds only the internal network's DNS -- aardvark, which
    resolves container names and has nothing upstream to forward to, because the
    internal network has no route out. The proxy then failed on every request
    with `Could not retrieve address info for pypi.org:443: Name does not
    resolve`, which looks exactly like a blocked destination and is not one.

    So the resolvers are read from the runtime rather than guessed: a throwaway
    container on the outbound network reports what it was given, and the proxy is
    started with those. No public resolver is ever substituted -- a framework
    that quietly sent an event's DNS somewhere the operator did not choose would
    be making a policy decision it has no standing to make.
    """
    probe = _run([
        runtime, "run", "--rm", "--network", OUTBOUND_NETWORK,
        "--entrypoint", "cat", image, "/etc/resolv.conf",
    ], timeout=60)
    if probe is None or probe.returncode != 0:
        raise SafetyError(
            "could not read the outbound network's resolvers: "
            + ((probe.stderr or probe.stdout).strip() if probe else "runtime did not respond")
        )
    found = tuple(
        line.split()[1]
        for line in (probe.stdout or "").splitlines()
        if line.strip().startswith("nameserver") and len(line.split()) > 1
    )
    if not found:
        raise SafetyError(
            "the outbound network offers no nameserver, so the proxy could not resolve "
            "any allowed host. Every request would fail as if the destination were "
            "blocked, which is worse than refusing to start."
        )
    return found


def stop(runtime: str | None = None) -> bool:
    """Remove the proxy container. Returns whether one was there."""
    chosen = _require_runtime(runtime)
    removed = _run([chosen, "rm", "--force", PROXY_NAME])
    return bool(removed and removed.returncode == 0 and removed.stdout.strip())


def start(allowlist: Iterable[str], runtime: str | None = None) -> ProxyState:
    """Bring up a proxy enforcing exactly this allowlist.

    Always replaces a running proxy rather than reusing one: a proxy left from
    another event would enforce that event's allowlist, and nothing outside the
    container could tell the difference.
    """
    chosen = _require_runtime(runtime)
    entries = normalize_allowlist(allowlist)
    ensure_networks(chosen)
    stop(chosen)
    build_image(chosen, entries)
    resolvers: list[str] = []
    for nameserver in outbound_resolvers(chosen):
        resolvers += ["--dns", nameserver]
    started = _run([
        chosen, "run", "--detach", "--name", PROXY_NAME,
        "--network", SANDBOX_NETWORK,
        "--network", OUTBOUND_NETWORK,
        *resolvers,
        "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges",
        "--memory", "256m", "--pids-limit", "64",
        "--label", "atj-allowlist=" + ",".join(entries),
        PROXY_IMAGE,
    ], timeout=60)
    if started is None or started.returncode != 0:
        raise SafetyError(
            "could not start the egress proxy: "
            + ((started.stderr or started.stdout).strip() if started else "no response")
        )
    address = proxy_address(chosen)
    if not address:
        raise SafetyError(
            f"the egress proxy started but reports no address on {SANDBOX_NETWORK!r}, so "
            f"nothing on that network could reach it"
        )
    return ProxyState(
        runtime=chosen, running=True, allowlist=entries, url=proxy_url(address)
    )



def state(runtime: str | None = None) -> ProxyState:
    """What the runtime says is running, including the allowlist in force."""
    chosen = _require_runtime(runtime)
    inspected = _run([
        chosen, "inspect", PROXY_NAME,
        "--format", '{{.State.Running}} {{index .Config.Labels "atj-allowlist"}}',
    ])
    if inspected is None or inspected.returncode != 0:
        return ProxyState(runtime=chosen, running=False, allowlist=(), url="")
    parts = (inspected.stdout or "").strip().split(None, 1)
    running = bool(parts) and parts[0].lower() == "true"
    entries = tuple(parts[1].split(",")) if len(parts) > 1 and parts[1] else ()
    address = proxy_address(chosen) if running else ""
    return ProxyState(
        runtime=chosen, running=running, allowlist=entries,
        url=proxy_url(address) if address else "",
    )


def require_for(allowlist: Iterable[str], runtime: str | None = None) -> str:
    """The proxy URL to use for a run, or a refusal naming the mismatch.

    An event's allowlist is a decision by an official. A proxy enforcing a
    different one -- left from another event, or started by hand -- would make
    that decision quietly false, so the two must match exactly.
    """
    wanted = normalize_allowlist(allowlist)
    current = state(runtime)
    if not current.running:
        raise SafetyError(
            "this event configures a network_allowlist and no egress proxy is running. "
            "Start one with `atj sandbox proxy up --event-dir <event>`, or run with no "
            "network and record the limitation."
        )
    if tuple(sorted(current.allowlist)) != tuple(sorted(wanted)):
        raise SafetyError(
            f"the running egress proxy enforces {sorted(current.allowlist)} and this event "
            f"authorizes {sorted(wanted)}. Restart it with "
            f"`atj sandbox proxy up --event-dir <event>` rather than running against an "
            f"allowlist nobody approved for this event."
        )
    return current.url
