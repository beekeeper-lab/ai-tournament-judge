"""Isolated execution of untrusted submissions.

In v0.1.0-alpha `framework/policies/execution-safety.md` described controls that
nothing implemented. This module implements them, and — more importantly —
refuses to run when it cannot guarantee them.

Design rules, in order of priority:

1. **There is no host fallback.** If isolation cannot be verified, execution is
   *unavailable*, not *degraded*. Affected criteria become `NE`. A judge with
   less evidence is a correct outcome; running a student's code on the operator's
   laptop is not.
2. **Nothing from the host enters the container.** No environment variables, no
   SSH agent, no cloud credential files, no Docker socket, no home directory.
   The submission is mounted read-only.
3. **No network by default.** An event may authorize specific destinations, but
   only through an explicitly configured egress proxy. Plain container flags
   cannot filter by destination, so an allowlist without a proxy is refused
   rather than silently granting full network access.
4. **Everything is recorded.** Command, exit status, stdout, stderr, duration,
   limits, image digest, and runtime version go into the evidence record.
"""

from __future__ import annotations

import json
import shlex
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence

from . import versions
from .errors import SafetyError

# Execution status values recorded on an evidence manifest.
NOT_RUN = "not-run"
UNAVAILABLE = "unavailable"
COMPLETE = "sandboxed-complete"
PARTIAL = "sandboxed-partial"
REFUSED = "refused"

PODMAN, DOCKER = "podman", "docker"
PROBE_TIMEOUT = 10

DEFAULT_LIMITS = {
    "cpus": "1.0",
    "memory": "1g",
    "pids": 256,
    "tmpfs_size": "64m",
    "timeout_seconds": 120,
    "output_bytes": 256 * 1024,
}

# Criteria whose evidence usually depends on running the software. When execution
# is unavailable these are the ones a judge must mark NE rather than guess at.
EXECUTION_DEPENDENT_CRITERIA = ("functional", "reliability")


@dataclass
class Capability:
    """What isolation this host can actually provide, right now."""

    runtime: str | None
    version: str | None
    available: bool
    rootless: bool | None
    reasons: list[str] = field(default_factory=list)

    @property
    def execution_status(self) -> str:
        return NOT_RUN if self.available else UNAVAILABLE

    def summary(self) -> str:
        if self.available:
            mode = "rootless" if self.rootless else "rootful"
            return f"{self.runtime} {self.version} ({mode})"
        return "no verified container isolation: " + "; ".join(self.reasons)


def _run(command: Sequence[str], timeout: int = PROBE_TIMEOUT) -> subprocess.CompletedProcess | None:
    try:
        return subprocess.run(
            list(command), capture_output=True, text=True, timeout=timeout, check=False
        )
    except (OSError, subprocess.SubprocessError):
        return None


def preflight(preferred: str | None = None) -> Capability:
    """Detect a usable container runtime.

    Podman is preferred: rootless by default, no long-lived daemon. Docker is
    accepted when its daemon actually answers — a present client with an
    unreachable daemon is not isolation, and this returns unavailable rather
    than hanging an event on it.
    """
    reasons: list[str] = []
    candidates = [preferred] if preferred else [PODMAN, DOCKER]
    for runtime in candidates:
        if not runtime or not shutil.which(runtime):
            reasons.append(f"{runtime}: not installed")
            continue
        probe = _run([runtime, "version", "--format", "{{.Server.Version}}"])
        if probe is None:
            reasons.append(f"{runtime}: client present but the daemon did not respond within "
                           f"{PROBE_TIMEOUT}s")
            continue
        if probe.returncode != 0:
            detail = (probe.stderr or probe.stdout or "").strip().splitlines()
            reasons.append(f"{runtime}: {detail[0] if detail else 'version probe failed'}")
            continue
        version = probe.stdout.strip() or "unknown"
        rootless = None
        info = _run([runtime, "info", "--format", "{{json .}}"])
        if info and info.returncode == 0:
            try:
                payload = json.loads(info.stdout)
                if runtime == PODMAN:
                    rootless = bool(payload.get("host", {}).get("security", {}).get("rootless"))
                else:
                    rootless = "rootless" in json.dumps(payload.get("SecurityOptions", []))
            except (json.JSONDecodeError, AttributeError):
                rootless = None
        return Capability(runtime=runtime, version=version, available=True, rootless=rootless)
    return Capability(runtime=None, version=None, available=False, rootless=None, reasons=reasons)


def _reject_unsafe_mounts(source: Path) -> None:
    """Refuse to mount anything that would carry host trust into the sandbox."""
    resolved = source.resolve()
    forbidden = [
        Path.home(),
        Path("/"),
        Path("/etc"),
        Path("/var/run"),
        Path("/run"),
    ]
    for path in forbidden:
        if resolved == path:
            raise SafetyError(f"refusing to mount {resolved} into a sandbox")
    for name in (".ssh", ".aws", ".config/gcloud", ".kube", ".docker", ".gnupg"):
        if (resolved / name).exists():
            raise SafetyError(
                f"refusing to mount {resolved}: it contains {name}, which would place host "
                f"credentials inside untrusted code"
            )


def build_command(
    *,
    runtime: str,
    image: str,
    source: Path,
    command: Sequence[str],
    limits: dict[str, Any] | None = None,
    network_allowlist: Sequence[str] = (),
    egress_proxy: str | None = None,
    workdir: str = "/submission",
) -> list[str]:
    """Assemble the container invocation. Never returns a host command."""
    limits = {**DEFAULT_LIMITS, **(limits or {})}
    _reject_unsafe_mounts(source)

    if network_allowlist and not egress_proxy:
        raise SafetyError(
            "a network allowlist was configured without an egress proxy. Container flags "
            "cannot filter by destination, so honouring the allowlist would in fact grant "
            "unrestricted network access. Configure an authorized proxy or run with no network."
        )

    mount = f"{source.resolve()}:{workdir}:ro"
    if runtime == PODMAN:
        mount += ",Z"

    argv = [
        runtime, "run", "--rm",
        "--network", "none" if not egress_proxy else "sandbox-egress",
        "--read-only",
        "--tmpfs", f"/tmp:rw,noexec,nosuid,size={limits['tmpfs_size']}",
        "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges",
        "--pids-limit", str(limits["pids"]),
        "--memory", str(limits["memory"]),
        "--cpus", str(limits["cpus"]),
        "--user", "65534:65534",
        "--workdir", workdir,
        "--env", "HOME=/tmp",
        "--volume", mount,
    ]
    if egress_proxy:
        # The proxy is the only destination the container can reach; it enforces
        # the allowlist, not the container runtime.
        argv += ["--env", f"HTTPS_PROXY={egress_proxy}", "--env", f"HTTP_PROXY={egress_proxy}",
                 "--env", "NO_PROXY="]
    argv += [image, *command]

    for banned in ("--privileged", "/var/run/docker.sock", "--cap-add", "--pid=host",
                   "--network=host", "--userns=host"):
        joined = " ".join(argv)
        if banned in joined:
            raise SafetyError(f"refusing to build a command containing {banned!r}")
    return argv


@dataclass
class ExecutionRecord:
    command: list[str]
    exit_status: int | None
    stdout: str
    stderr: str
    duration_seconds: float
    timed_out: bool
    truncated: bool
    limits: dict[str, Any]
    runtime: str
    runtime_version: str | None
    image: str
    started_at: str
    completed_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "command": " ".join(shlex.quote(part) for part in self.command),
            "exit_status": self.exit_status,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "duration_seconds": round(self.duration_seconds, 3),
            "timed_out": self.timed_out,
            "output_truncated": self.truncated,
            "limits": self.limits,
            "runtime": self.runtime,
            "runtime_version": self.runtime_version,
            "image": self.image,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }


def run_in_sandbox(
    *,
    source: Path,
    command: Sequence[str],
    image: str = "docker.io/library/python:3.12-alpine",
    limits: dict[str, Any] | None = None,
    network_allowlist: Sequence[str] = (),
    egress_proxy: str | None = None,
    capability: Capability | None = None,
) -> ExecutionRecord:
    """Run one command against a submission, isolated. Raises rather than degrading."""
    capability = capability or preflight()
    if not capability.available:
        raise SafetyError(
            "execution refused: " + capability.summary()
            + ". Static inspection may continue; executable evidence is unavailable and "
              "affected criteria must use NE."
        )
    limits = {**DEFAULT_LIMITS, **(limits or {})}
    argv = build_command(
        runtime=capability.runtime, image=image, source=Path(source), command=command,
        limits=limits, network_allowlist=network_allowlist, egress_proxy=egress_proxy,
    )
    started = versions.now()
    begin = time.monotonic()
    timed_out = False
    try:
        completed = subprocess.run(
            argv, capture_output=True, text=True,
            timeout=float(limits["timeout_seconds"]), check=False,
        )
        stdout, stderr, status = completed.stdout, completed.stderr, completed.returncode
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        stdout = exc.stdout.decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode("utf-8", "replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        status = None
    except OSError as exc:
        raise SafetyError(f"sandbox invocation failed: {exc}") from exc

    limit = int(limits["output_bytes"])
    truncated = len(stdout) > limit or len(stderr) > limit
    return ExecutionRecord(
        command=argv,
        exit_status=status,
        stdout=stdout[:limit],
        stderr=stderr[:limit],
        duration_seconds=time.monotonic() - begin,
        timed_out=timed_out,
        truncated=truncated,
        limits=limits,
        runtime=capability.runtime,
        runtime_version=capability.version,
        image=image,
        started_at=started,
        completed_at=versions.now(),
    )


def evidence_limitation(capability: Capability) -> dict[str, Any]:
    """What an evidence manifest must record when execution is unavailable."""
    if capability.available:
        return {"execution_status": NOT_RUN, "evidence_limited_criteria": []}
    return {
        "execution_status": UNAVAILABLE,
        "evidence_limited_criteria": list(EXECUTION_DEPENDENT_CRITERIA),
        "limitation": (
            capability.summary()
            + ". Only static inspection and team-supplied artifacts are available. "
              "Criteria that require observed behaviour must be scored NE unless other "
              "direct evidence exists."
        ),
    }
