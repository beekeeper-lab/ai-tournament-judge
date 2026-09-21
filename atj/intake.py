"""Submission intake: getting a team's code onto disk, pinned, and recorded.

Everything downstream of this module assumed three things that nothing produced:
a checkout that exists, a commit that cannot move, and a roster row naming both.
`atj sandbox run` took a source path some other step had to create, and
`schemas/submission-intake.schema.json` required a commit that a zipped
submission does not have. The gap was filled by hand, which is the one place an
evidence chain cannot afford improvisation.

A submission is untrusted input. Nothing here executes it. `git` is the only
subprocess, it runs with hooks disabled, and archives are inspected entry by
entry before a single byte is written.

An archive has no commit, so one is made for it. The snapshot commit uses a
fixed identity and a fixed timestamp, which makes the hash a pure function of
the delivered tree: the same archive pins to the same commit on any machine, and
a changed archive cannot pin to the same one.
"""

from __future__ import annotations

import os
import re
import shutil
import stat
import subprocess
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import event as event_module, frontmatter, ids, versions
from .errors import AtjError, SafetyError, StateError, ValidationError

# --------------------------------------------------------------------------- #
# Source classification
# --------------------------------------------------------------------------- #

GIT_URL = re.compile(r"^(?:https?|git|ssh|git\+ssh)://|^[^/\s:]+@[^/\s:]+:")
ARCHIVE_SUFFIXES = (".zip",)

#: Stages at which the roster may still gain a team. Intake after the roster is
#: frozen is a different act with a different authorization, not a later call of
#: the same one.
OPEN_STAGES = ("configuration", "intake")

# Archive guards. A submission is allowed to be large; it is not allowed to
# decide how much of the operator's disk it uses.
MAX_ENTRIES = 20_000
MAX_TOTAL_BYTES = 2 * 1024 ** 3
MAX_RATIO = 200

SNAPSHOT_NAME = "atj intake"
SNAPSHOT_EMAIL = "intake@atj.invalid"
SNAPSHOT_DATE = "1970-01-01T00:00:00 +0000"

# Hooks are the reason this list exists: `git clone` does not copy a remote's
# hooks, but it does honour the ones already sitting in a local source repo.
_GIT_HARDENING = (
    "-c", "core.hooksPath=/dev/null",
    "-c", "protocol.ext.allow=never",
    "-c", "advice.detachedHead=false",
)


def classify(source: str) -> str:
    """Name the kind of thing `source` is: the intake path branches on it."""
    if GIT_URL.search(source):
        return "git-url"
    path = Path(source).expanduser()
    if not path.exists():
        raise ValidationError(
            f"submission source not found: {source}. A local source must exist; "
            f"a remote one must look like a git URL.",
            artifact=source,
        )
    if path.is_file():
        if path.suffix.lower() in ARCHIVE_SUFFIXES:
            return "archive"
        raise ValidationError(
            f"{path.name} is not a supported submission archive "
            f"({', '.join(ARCHIVE_SUFFIXES)}) or a directory.",
            artifact=str(path),
        )
    if (path / ".git").exists():
        return "git-repo"
    return "directory"


# --------------------------------------------------------------------------- #
# git
# --------------------------------------------------------------------------- #

def _git(*args: str, cwd: Path | None = None, env: dict[str, str] | None = None) -> str:
    command = ["git", *_GIT_HARDENING, *args]
    environment = dict(os.environ)
    # A clone that stops for a password is a clone that hangs a judging run.
    environment.setdefault("GIT_TERMINAL_PROMPT", "0")
    environment.update(env or {})
    try:
        completed = subprocess.run(
            command, cwd=str(cwd) if cwd else None, env=environment,
            capture_output=True, text=True, check=False,
        )
    except FileNotFoundError as exc:  # pragma: no cover - environment failure
        raise AtjError("git is not installed; intake cannot pin a commit") from exc
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "").strip().splitlines()
        raise AtjError(
            f"git {args[0]} failed: {detail[-1] if detail else 'no output'}",
            artifact=str(cwd) if cwd else None,
        )
    return completed.stdout.strip()


def _clone(source: str, destination: Path, ref: str | None) -> str:
    """Copy committed history to `destination` and report the pinned commit."""
    _git("clone", "--quiet", source, str(destination))
    if ref:
        _git("checkout", "--quiet", "--detach", ref, cwd=destination)
    return _git("rev-parse", "HEAD", cwd=destination)


def _source_is_dirty(path: Path) -> bool:
    try:
        return bool(_git("status", "--porcelain", cwd=path))
    except AtjError:
        return False


def _snapshot(destination: Path, team_id: str) -> str:
    """Create the immutable commit an archive or loose directory does not have.

    Fixed identity and fixed dates make the resulting hash depend on the tree and
    nothing else, so the pin is reproducible and a changed tree cannot hide
    behind the same commit.
    """
    _git("init", "--quiet", "--initial-branch=main", cwd=destination)
    # `-f` on purpose: a submission's own .gitignore describes what its authors
    # did not want in *their* history. The pin has to describe what was actually
    # delivered, or the commit stops matching the checkout judges are reading.
    _git("add", "--all", "--force", cwd=destination)
    identity = {
        "GIT_AUTHOR_NAME": SNAPSHOT_NAME, "GIT_AUTHOR_EMAIL": SNAPSHOT_EMAIL,
        "GIT_COMMITTER_NAME": SNAPSHOT_NAME, "GIT_COMMITTER_EMAIL": SNAPSHOT_EMAIL,
        "GIT_AUTHOR_DATE": SNAPSHOT_DATE, "GIT_COMMITTER_DATE": SNAPSHOT_DATE,
    }
    _git(
        "commit", "--quiet", "--allow-empty", "--no-verify",
        "-m", f"Submission snapshot: {team_id}",
        cwd=destination, env=identity,
    )
    return _git("rev-parse", "HEAD", cwd=destination)


# --------------------------------------------------------------------------- #
# Archives
# --------------------------------------------------------------------------- #

def _reject_member(name: str, info: zipfile.ZipInfo) -> str | None:
    """Why this archive entry must not be written, or None if it may be."""
    if info.is_dir():
        return None
    pure = Path(name)
    if pure.is_absolute() or name.startswith("/") or (len(name) > 1 and name[1] == ":"):
        return "absolute path"
    if ".." in pure.parts:
        return "parent-directory traversal"
    mode = info.external_attr >> 16
    # Not every writer records a file type. An absent one is not a claim to be
    # anything unusual; only a type that is present and is not a plain file or
    # directory is grounds for refusing the archive.
    kind = stat.S_IFMT(mode)
    if kind == stat.S_IFLNK:
        return "symbolic link"
    if kind not in (0, stat.S_IFREG, stat.S_IFDIR):
        return "not a regular file"
    return None


def _extract_archive(archive: Path, destination: Path) -> list[str]:
    notes: list[str] = []
    with zipfile.ZipFile(archive) as bundle:
        infos = bundle.infolist()
        if len(infos) > MAX_ENTRIES:
            raise SafetyError(
                f"{archive.name} holds {len(infos)} entries, over the {MAX_ENTRIES} "
                f"intake limit. Unpack and review it by hand before ingesting.",
                artifact=str(archive),
            )
        total = 0
        for info in infos:
            reason = _reject_member(info.filename, info)
            if reason is not None:
                raise SafetyError(
                    f"{archive.name} contains {info.filename!r} ({reason}). "
                    f"Nothing was extracted.",
                    artifact=str(archive),
                )
            total += info.file_size
            if info.compress_size and info.file_size / max(info.compress_size, 1) > MAX_RATIO:
                raise SafetyError(
                    f"{archive.name}: {info.filename!r} expands more than "
                    f"{MAX_RATIO}x. Nothing was extracted.",
                    artifact=str(archive),
                )
        if total > MAX_TOTAL_BYTES:
            raise SafetyError(
                f"{archive.name} expands to {total / 1024 ** 3:.1f} GiB, over the "
                f"intake limit. Nothing was extracted.",
                artifact=str(archive),
            )
        destination.mkdir(parents=True, exist_ok=True)
        bundle.extractall(destination)
        notes.append(f"extracted {len(infos)} entries from {archive.name}")
    return notes


def _strip_single_root(directory: Path) -> str | None:
    """Unwrap the one wrapper directory an exported archive is packed inside."""
    entries = [path for path in directory.iterdir()]
    if len(entries) != 1 or not entries[0].is_dir():
        return None
    inner = entries[0]
    staging = directory.parent / f".{directory.name}.unwrap"
    inner.rename(staging)
    inner_name = inner.name
    for child in staging.iterdir():
        child.rename(directory / child.name)
    staging.rmdir()
    return inner_name


def _copy_tree(source: Path, destination: Path) -> None:
    shutil.copytree(source, destination, symlinks=True, dirs_exist_ok=False)


# --------------------------------------------------------------------------- #
# Materialization
# --------------------------------------------------------------------------- #

@dataclass
class Materialized:
    kind: str
    checkout: Path
    commit: str
    pin: str
    notes: list[str] = field(default_factory=list)


def _submodule_notes(destination: Path) -> list[str]:
    """Report gitlinks the checkout did not materialize.

    `git clone` without `--recurse-submodules` leaves a pinned but empty gitlink,
    and `git submodule status` marks it with a leading `-`. The checkout then does
    not fully realize the commit it claims, which an auditor has to be told rather
    than left to discover: a judgment about a submission's configuration made from
    part of that configuration is a judgment on partial evidence.
    """
    if not (destination / ".gitmodules").is_file():
        return []
    try:
        status = _git("submodule", "status", cwd=destination)
    except ValidationError:
        return ["`.gitmodules` is present but `git submodule status` failed; "
                "whether every gitlink is materialized is unverified"]
    notes: list[str] = []
    for line in status.splitlines():
        marker, rest = line[:1], line[1:]
        if marker not in ("-", "+"):
            continue
        parts = rest.split()
        if not parts:
            continue
        commit = parts[0]
        path = parts[1] if len(parts) > 1 else "(unnamed)"
        if marker == "-":
            notes.append(
                f"submodule `{path}` is pinned at `{commit}` and was not "
                f"materialized; its content is absent from this checkout and "
                f"outside the eligible scope"
            )
        else:
            notes.append(
                f"submodule `{path}` is checked out at `{commit}`, which is not the "
                f"commit the superproject pins; the checkout looks complete and does "
                f"not match its own pin"
            )
    return notes


def materialize(
    source: str, destination: Path, *, team_id: str, ref: str | None = None
) -> Materialized:
    """Put the submission at `destination` and return the commit it is pinned to.

    `pin` records how the commit was obtained. `cloned` means the team's own
    history supplied it. `snapshot` means the delivery had none and this tool
    created one, which an auditor reading the record needs to be able to tell
    apart.
    """
    kind = classify(source)
    notes: list[str] = []
    destination.parent.mkdir(parents=True, exist_ok=True)

    if kind in ("git-url", "git-repo"):
        if kind == "git-repo" and _source_is_dirty(Path(source).expanduser()):
            notes.append(
                "the source working tree has uncommitted changes; they are not part "
                "of the pinned commit and were not ingested"
            )
        commit = _clone(source, destination, ref)
        notes += _submodule_notes(destination)
        return Materialized(kind, destination, commit, "cloned", notes)

    if ref:
        raise ValidationError(
            f"--ref names a commit in a git source; {kind} submissions have no "
            f"history to select from.",
            artifact=source,
        )

    if kind == "archive":
        notes += _extract_archive(Path(source).expanduser(), destination)
        unwrapped = _strip_single_root(destination)
        if unwrapped:
            notes.append(f"unwrapped the single top-level directory {unwrapped!r}")
    else:
        _copy_tree(Path(source).expanduser(), destination)
        notes.append(f"copied the directory {source}")

    # An export can carry a whole repository inside it. Its history is better
    # evidence than a snapshot of its working tree, so use it.
    if (destination / ".git").exists():
        notes.append("the delivery contains a git repository; pinned its own HEAD")
        commit = _git("rev-parse", "HEAD", cwd=destination)
        notes += _submodule_notes(destination)
        return Materialized(kind, destination, commit, "cloned", notes)

    commit = _snapshot(destination, team_id)
    notes.append("no history was delivered; pinned a reproducible snapshot commit")
    return Materialized(kind, destination, commit, "snapshot", notes)


# --------------------------------------------------------------------------- #
# The intake record
# --------------------------------------------------------------------------- #

UNSUPPLIED = "Not supplied at intake. Complete this from the team's submission before judging."

PROVENANCE = "Intake provenance"


def _template_sections(root: Path) -> list[str]:
    from . import reports

    return reports.template_sections("submission-intake.md", root)


def build_record(
    event: event_module.Event,
    team_id: str,
    materialized: Materialized,
    *,
    source: str,
    display_name: str,
    now: datetime,
) -> str:
    """Render the intake record: mechanical facts filled, narrative left open.

    The tool knows where the code came from and what it is pinned to. It does not
    know what the team built or how to run it, and writing a guess into an
    evidence artifact is worse than leaving the section visibly open.
    """
    root = event.root
    stamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    metadata: dict[str, Any] = {
        "event_id": event.event_id,
        "team_id": team_id,
        "repository": source,
        "commit": materialized.commit,
        "rubric": str(event.config["rubric"]),
        "persona": versions.load_personas(root)["prepare-submission"].reference,
        "framework_commit": str(
            event.config.get("framework_commit") or versions.framework_commit(root)
        ),
        "submitted_at": stamp,
        "started_at": stamp,
        "completed_at": stamp,
        "model_requested": "not-applicable",
        "model_used": "not-applicable",
        "eligible": True,
        "visibility": "private",
        "approval_state": "draft",
        "validation_state": "unvalidated",
    }

    lines = [
        f"# Submission Intake — {display_name}",
        "",
        "`atj intake` materialized this submission and pinned it. It does not supply "
        "the sections below. Complete them from the team's own account of what they "
        "built. Where no participant supplies one, compile them from the submission's "
        "own documentation, attribute every claim to the file it came from, and record "
        "in the provenance table who or what compiled them.",
        "",
    ]
    for heading in _template_sections(root):
        if heading == PROVENANCE:
            continue
        lines += [f"## {heading}", "", UNSUPPLIED, ""]

    lines += [
        f"## {PROVENANCE}",
        "",
        "| Fact | Value |",
        "|---|---|",
        f"| Source | `{source}` |",
        f"| Source kind | {materialized.kind} |",
        f"| Pinned commit | `{materialized.commit}` |",
        f"| How the commit was obtained | {materialized.pin} |",
        f"| Checkout | `{materialized.checkout}` |",
        f"| Materialized at | {stamp} |",
        "| Narrative sections compiled by | unsupplied at intake |",
        "",
    ]
    if materialized.pin == "snapshot":
        lines += [
            "The delivery carried no history, so the commit above is a snapshot this "
            "tool created with a fixed identity and timestamp. It is reproducible from "
            "the same tree and is not the team's own commit.",
            "",
        ]
    for note in materialized.notes:
        lines.append(f"- {note}")
    if materialized.notes:
        lines.append("")
    lines += [
        "Nothing in this submission has been executed. Execution requires "
        "`atj sandbox preflight` to report isolation available.",
        "",
    ]
    return frontmatter.dump(metadata, "\n".join(lines))


# --------------------------------------------------------------------------- #
# The roster
# --------------------------------------------------------------------------- #

_SEPARATOR = re.compile(r"^\|[\s:|-]+\|$")


def _cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _table_width(lines: list[str]) -> int:
    for index, line in enumerate(lines):
        if _SEPARATOR.match(line.strip()) and index:
            return len(_cells(lines[index - 1]))
    raise ValidationError("teams.md has no roster table header")


def update_roster(
    path: Path,
    team_id: str,
    *,
    repository: str,
    commit: str,
    display_name: str,
    affiliation_group: str | None,
) -> str:
    """Insert or update one roster row, leaving every other line untouched.

    The table is the editable source of the roster, so this edits the table
    rather than keeping a parallel record beside it.
    """
    metadata, body = frontmatter.read(path)
    lines = body.splitlines()
    # The table's own header defines its width. Assuming a column count here
    # would be a second copy of a shape that already exists in the file.
    columns = _table_width(lines)
    row = [
        team_id, display_name, affiliation_group or "none", "none",
        "received", "yes", repository, commit,
    ][:columns]
    row += [""] * (columns - len(row))
    rendered = "| " + " | ".join(row) + " |"

    for index, line in enumerate(lines):
        if not line.strip().startswith("|") or _SEPARATOR.match(line.strip()):
            continue
        cells = _cells(line)
        if cells and cells[0] == team_id:
            # An existing row carries decisions the operator made: eligibility,
            # previous result, display name. Intake supplies the source, not
            # those.
            merged = list(cells) + [""] * (columns - len(cells))
            merged[6], merged[7] = repository, commit
            if affiliation_group:
                merged[2] = affiliation_group
            lines[index] = "| " + " | ".join(merged[:columns]) + " |"
            return frontmatter.dump(metadata, "\n".join(lines) + "\n")

    for index, line in enumerate(lines):
        if _SEPARATOR.match(line.strip()):
            insert = index + 1
            while insert < len(lines) and lines[insert].strip().startswith("|"):
                insert += 1
            lines.insert(insert, rendered)
            return frontmatter.dump(metadata, "\n".join(lines) + "\n")

    raise ValidationError(
        f"{path.name} has no roster table to add {team_id!r} to", artifact=str(path)
    )


# --------------------------------------------------------------------------- #
# The operation
# --------------------------------------------------------------------------- #

@dataclass
class Result:
    event_id: str
    team_id: str
    source: str
    source_kind: str
    checkout: Path
    commit: str
    pin: str
    record: Path
    notes: list[str]


def default_workspace(root: Path) -> Path:
    return root / "workspaces"


def run(
    event: event_module.Event,
    team_id: str,
    source: str,
    *,
    workspace: Path | None = None,
    ref: str | None = None,
    display_name: str | None = None,
    affiliation_group: str | None = None,
    force: bool = False,
    now: datetime | None = None,
) -> Result:
    """Materialize, pin, record and enroll one submission."""
    ids.require_slug(team_id, kind="team_id")
    stamp = now or datetime.now(timezone.utc)

    if event.stage not in OPEN_STAGES and not force:
        raise StateError(
            f"{event.event_id} is at stage {event.stage!r}; intake belongs to "
            f"{' or '.join(OPEN_STAGES)}. Adding a submission now changes the inputs "
            f"every later stage was audited against.",
            artifact=str(event.directory),
        )
    if event.roster.get("frozen") and not force:
        raise StateError(
            f"the roster of {event.event_id} is frozen. A frozen roster is what the "
            f"bracket was drawn from; re-open it deliberately or run a versioned redraw.",
            artifact=str(event.directory / "teams.md"),
        )

    base = workspace or default_workspace(event.root)
    checkout = (base / event.event_id / team_id).resolve()
    if checkout.exists() and not force:
        raise StateError(
            f"a checkout already exists at {checkout}. Re-ingesting replaces the "
            f"code every downstream artifact cites; pass --force to do it anyway.",
            artifact=str(checkout),
        )

    # Build beside the real location and swap. A half-extracted archive that
    # failed a safety check must never be left sitting where a judge would read
    # it, and a failed re-ingest must not destroy the checkout already there.
    staging = checkout.parent / f".{checkout.name}.incoming"
    staging.parent.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(staging, ignore_errors=True)
    try:
        materialized = materialize(source, staging, team_id=team_id, ref=ref)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    shutil.rmtree(checkout, ignore_errors=True)
    staging.rename(checkout)
    materialized.checkout = checkout

    enrolled = next((team for team in event.teams if team["id"] == team_id), None)
    resolved_name = display_name or (enrolled or {}).get("display_name") or team_id

    record = event.directory / "submissions" / f"{team_id}.md"
    record.parent.mkdir(parents=True, exist_ok=True)
    record.write_text(
        build_record(
            event, team_id, materialized,
            source=source, display_name=resolved_name, now=stamp,
        ),
        encoding="utf-8",
    )

    roster_path = event.directory / "teams.md"
    roster_path.write_text(
        update_roster(
            roster_path, team_id,
            repository=source, commit=materialized.commit,
            display_name=resolved_name, affiliation_group=affiliation_group,
        ),
        encoding="utf-8",
    )

    return Result(
        event_id=event.event_id,
        team_id=team_id,
        source=source,
        source_kind=materialized.kind,
        checkout=materialized.checkout,
        commit=materialized.commit,
        pin=materialized.pin,
        record=record,
        notes=materialized.notes,
    )
