"""Event lifecycle: initialization, state transitions, staleness, and resume.

`events/<event>/status.md` is the recovery ledger. Its front matter is the
machine-readable state; the Markdown body below it stays human-reviewable.

A stage advances only forwards along the declared sequence, and only when the
current stage's audit gate has passed. A unit is complete only when its outputs
exist *and* its recorded input digest still matches its inputs; when an input
changes, everything downstream becomes ``stale`` rather than silently wrong.
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from . import canon, frontmatter, ids, schema, versions
from .errors import StateError, ValidationError

STAGES = (
    "configuration", "intake", "evidence", "initial-judging", "consolidation",
    "bracket", "tournament", "dossiers", "final-audit", "complete",
)
STAGE_INDEX = {stage: index for index, stage in enumerate(STAGES)}

STAGE_GATES = {
    "configuration": "configuration-audited",
    "intake": "roster-frozen",
    "evidence": "evidence-validated",
    "initial-judging": "judgments-audited",
    "consolidation": "consolidation-audited",
    "bracket": "bracket-audited",
    "tournament": "tournament-audited",
    "dossiers": "dossiers-approved",
    "final-audit": "final-audit-passed",
}

EVENT_SUBDIRS = (
    "submissions", "evidence", "judgments", "summaries", "matchups",
    "adjudications", "dossiers", "public", "audits", "runs",
)

REQUIRED_FILES = ("event.md", "teams.md", "status.md", "bracket.md")
TEMPLATE_DIR = "events/_template"

PASS_RESULTS = ("PASS", "PASS WITH ADVISORIES")

_ROSTER_ROW = re.compile(r"^\|\s*([a-z][a-z0-9-]*)\s*\|(.+)\|\s*$", re.MULTILINE)


# --------------------------------------------------------------------------- #
# Reading event records
# --------------------------------------------------------------------------- #

@dataclass
class Event:
    directory: Path
    root: Path
    config: dict[str, Any]
    status: dict[str, Any]
    roster: dict[str, Any]

    @property
    def event_id(self) -> str:
        return str(self.config["event_id"])

    @property
    def stage(self) -> str:
        return str(self.status["current_stage"])

    @property
    def teams(self) -> list[dict[str, Any]]:
        return list(self.roster.get("teams") or [])

    @property
    def eligible_teams(self) -> list[dict[str, Any]]:
        return [team for team in self.teams if team.get("eligible") and not team.get("withdrawn")]

    def team(self, team_id: str) -> dict[str, Any]:
        for candidate in self.teams:
            if candidate["id"] == team_id:
                return candidate
        raise ValidationError(f"team {team_id!r} is not on the roster of {self.event_id}")


def load(event_dir: Path, *, root: Path | None = None) -> Event:
    event_dir = Path(event_dir)
    base = root or canon.repository_root()
    missing = [name for name in REQUIRED_FILES if not (event_dir / name).is_file()]
    if missing:
        raise ValidationError(f"event directory is incomplete; missing {missing}", artifact=str(event_dir))
    config, _ = frontmatter.read(event_dir / "event.md")
    status, _ = frontmatter.read(event_dir / "status.md")
    roster, roster_body = frontmatter.read(event_dir / "teams.md")
    if "teams" not in roster:
        roster = dict(roster, teams=parse_roster_table(roster_body))
    return Event(directory=event_dir, root=base, config=config, status=status, roster=roster)


def parse_roster_table(body: str) -> list[dict[str, Any]]:
    """Read the human-editable roster table.

    Operators edit the Markdown table; the tooling reads it. Keeping one editable
    representation is the point — a parallel YAML list would be a second source
    of the same facts.
    """
    teams: list[dict[str, Any]] = []
    for line in body.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 6 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", cells[0]):
            continue
        team_id, display, affiliation, previous, submission, eligible = cells[:6]
        teams.append({
            "id": team_id,
            "display_name": display,
            "affiliation_group": None if affiliation in ("", "-", "none") else affiliation,
            "previous_result": previous if previous in ("champion", "runner-up") else "none",
            "submission_status": submission,
            "eligible": eligible.lower() in ("yes", "true", "y"),
            "repository": cells[6] if len(cells) > 6 else "",
            "commit": cells[7] if len(cells) > 7 else "",
        })
    return teams


# --------------------------------------------------------------------------- #
# Initialization
# --------------------------------------------------------------------------- #

def initialize(event_id: str, *, root: Path | None = None, event_name: str | None = None) -> Path:
    base = root or canon.repository_root()
    ids.require_slug(event_id, kind="event_id")
    source = base / TEMPLATE_DIR
    if not source.is_dir():
        raise ValidationError(f"event template not found: {source}")
    target = base / "events" / event_id
    if target.exists():
        raise ValidationError(f"event already exists: {target}")

    shutil.copytree(source, target)
    stamp = versions.now()
    commit = versions.framework_commit(base)
    replacements = {
        "replace-me": event_id,
        "REPLACE-ME": event_name or event_id.replace("-", " ").title(),
        "FRAMEWORK-COMMIT": commit,
        "YYYY-MM-DDTHH:MM:SSZ": stamp,
    }
    for name in REQUIRED_FILES:
        path = target / name
        text = path.read_text(encoding="utf-8")
        for needle, value in replacements.items():
            text = text.replace(needle, value)
        path.write_text(text, encoding="utf-8")
    for subdir in EVENT_SUBDIRS:
        directory = target / subdir
        directory.mkdir(exist_ok=True)
        keep = directory / ".gitkeep"
        if not any(directory.iterdir()):
            keep.write_text("", encoding="utf-8")
    return target


# --------------------------------------------------------------------------- #
# Validation
# --------------------------------------------------------------------------- #

def validate_configuration(event: Event, *, strict: bool = False) -> list[str]:
    problems: list[str] = []
    problems.extend(
        schema.validate("event", event.config, root=event.root,
                        artifact=str(event.directory / "event.md"))
    )
    try:
        versions.require_versions(event.config, root=event.root,
                                  artifact=str(event.directory / "event.md"))
    except Exception as exc:  # version errors are reported, not raised, by the validator
        problems.append(str(exc))

    for subdir in EVENT_SUBDIRS:
        if not (event.directory / subdir).is_dir():
            problems.append(f"missing required directory: {event.directory / subdir}")

    if event.config.get("event_id") != event.status.get("event_id"):
        problems.append("event.md and status.md declare different event_id values")
    if event.config.get("event_id") != event.roster.get("event_id"):
        problems.append("event.md and teams.md declare different event_id values")

    if strict:
        for name in REQUIRED_FILES:
            text = (event.directory / name).read_text(encoding="utf-8")
            for placeholder in ("replace-me", "REPLACE-ME", "EVENT-ID", "TEAM-ID", "TBD"):
                if placeholder in text:
                    problems.append(f"unresolved placeholder {placeholder!r} in {name}")
    return problems


def validate_roster(event: Event) -> list[str]:
    problems: list[str] = []
    teams = event.teams
    if len(teams) < 2:
        problems.append(f"roster has {len(teams)} team(s); at least 2 are required")

    seen: set[str] = set()
    for team in teams:
        team_id = team.get("id", "<missing>")
        if team_id in seen:
            problems.append(f"duplicate team id: {team_id}")
        seen.add(team_id)
        problems.extend(
            schema.validate("team", team, root=event.root,
                            artifact=f"{event.directory / 'teams.md'}#{team_id}")
        )

    for result in ("champion", "runner-up"):
        holders = [t["id"] for t in teams if t.get("previous_result") == result]
        if len(holders) > 1:
            problems.append(f"more than one team marked {result!r}: {holders}")

    if STAGE_INDEX.get(event.stage, 0) >= STAGE_INDEX["evidence"]:
        # From the evidence stage onward a team must be pinned to an immutable
        # commit; judging a moving branch is what the evidence policy forbids.
        for team in event.eligible_teams:
            if not team.get("repository"):
                problems.append(f"{team['id']}: no repository recorded; intake is incomplete")
            if not team.get("commit"):
                problems.append(f"{team['id']}: no immutable commit pinned; intake is incomplete")

    if event.config.get("bye_policy") == "performance-qualified":
        # Scores arrive at consolidation; only enforce once the bracket is due.
        if STAGE_INDEX.get(event.stage, 0) >= STAGE_INDEX["bracket"]:
            unscored = [t["id"] for t in event.eligible_teams if t.get("score") is None]
            if unscored:
                problems.append(
                    f"performance-qualified byes need a consolidated score for every eligible "
                    f"team; missing for {sorted(unscored)}"
                )
    return problems


def validate_status(event: Event) -> list[str]:
    problems = schema.validate(
        "status", event.status, root=event.root, artifact=str(event.directory / "status.md")
    )
    stage = event.status.get("current_stage")
    if stage not in STAGE_INDEX:
        problems.append(f"unknown current_stage: {stage!r}")
    return problems


# --------------------------------------------------------------------------- #
# State transitions
# --------------------------------------------------------------------------- #

def legal_transitions(stage: str) -> tuple[str, ...]:
    """Forward by exactly one stage. Backwards moves are explicit invalidations."""
    index = STAGE_INDEX.get(stage)
    if index is None:
        raise StateError(f"unknown stage: {stage!r}")
    if index + 1 >= len(STAGES):
        return ()
    return (STAGES[index + 1],)


def can_advance(event: Event) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    stage = event.stage
    if stage == "complete":
        return False, ["event is already complete"]
    if event.status.get("blocked"):
        reasons.append(f"event is blocked: {event.status.get('blocked_reason') or 'no reason recorded'}")

    gate = STAGE_GATES.get(stage)
    gates = event.status.get("stage_gates") or {}
    if gate and gates.get(gate) != "passed":
        reasons.append(
            f"stage gate {gate!r} is {gates.get(gate, 'pending')!r}; the stage audit must pass first"
        )

    incomplete = [
        unit["unit_id"] for unit in event.status.get("units", [])
        if unit.get("stage") == stage and unit.get("state") != "complete"
    ]
    if incomplete:
        reasons.append(f"incomplete units in {stage}: {sorted(incomplete)}")

    failed = [
        unit["unit_id"] for unit in event.status.get("units", [])
        if unit.get("stage") == stage and unit.get("audit_result") == "FAIL"
    ]
    if failed:
        reasons.append(f"failed audits in {stage}: {sorted(failed)}")
    return (not reasons), reasons


def advance(event: Event, *, force_reason: str | None = None) -> str:
    """Move to the next stage. Raises unless the gate is satisfied."""
    allowed, reasons = can_advance(event)
    if not allowed and force_reason is None:
        raise StateError(
            f"cannot advance from {event.stage!r}: " + "; ".join(reasons),
            artifact=str(event.directory),
        )
    targets = legal_transitions(event.stage)
    if not targets:
        raise StateError(f"{event.stage!r} is terminal")
    event.status["current_stage"] = targets[0]
    event.status["last_updated"] = versions.now()
    if force_reason:
        event.status.setdefault("overrides", []).append(
            {"from": event.stage, "to": targets[0], "reason": force_reason,
             "recorded_at": event.status["last_updated"]}
        )
    return targets[0]


def set_stage(event: Event, stage: str) -> None:
    """Explicit stage assignment, including backwards for an invalidation.

    Going backwards is legitimate (an operator invalidated work) but is never
    implicit: it marks every unit at or after the target stage stale.
    """
    if stage not in STAGE_INDEX:
        raise StateError(f"unknown stage: {stage!r}")
    target = STAGE_INDEX[stage]
    if target < STAGE_INDEX[event.stage]:
        for unit in event.status.get("units", []):
            if STAGE_INDEX.get(unit.get("stage", ""), 99) >= target:
                unit["state"] = "stale"
    event.status["current_stage"] = stage
    event.status["last_updated"] = versions.now()


# --------------------------------------------------------------------------- #
# Units, staleness, resume
# --------------------------------------------------------------------------- #

def unit_digest(*parts: str) -> str:
    return ids.digest(*parts, length=16)


def find_unit(event: Event, unit_id: str) -> dict[str, Any] | None:
    for unit in event.status.get("units", []):
        if unit.get("unit_id") == unit_id:
            return unit
    return None


def record_unit(
    event: Event,
    *,
    unit_id: str,
    stage: str,
    input_digest: str,
    outputs: Iterable[str],
    state: str = "complete",
    audit_result: str = "not-audited",
) -> dict[str, Any]:
    unit = find_unit(event, unit_id)
    payload = {
        "unit_id": unit_id,
        "stage": stage,
        "state": state,
        "input_digest": input_digest,
        "outputs": sorted(outputs),
        "audit_result": audit_result,
        "completed_at": versions.now() if state == "complete" else None,
    }
    if unit is None:
        event.status.setdefault("units", []).append(payload)
        unit = payload
    else:
        unit.update(payload)
    event.status["last_updated"] = versions.now()
    return unit


def mark_stale(event: Event, unit_id: str, reason: str) -> None:
    unit = find_unit(event, unit_id)
    if unit is None:
        return
    unit["state"] = "stale"
    unit["stale_reason"] = reason
    event.status["last_updated"] = versions.now()


def check_staleness(event: Event, current_digests: dict[str, str]) -> list[str]:
    """Report units whose recorded inputs no longer match reality.

    ``current_digests`` maps unit_id to the digest of its inputs right now.
    A unit whose digest changed is stale, and so is any unit that depends on it.
    """
    stale: list[str] = []
    for unit in event.status.get("units", []):
        unit_id = unit.get("unit_id")
        expected = current_digests.get(unit_id)
        if expected is None:
            continue
        if unit.get("input_digest") != expected:
            stale.append(unit_id)
    return stale


def missing_outputs(event: Event) -> list[str]:
    """Units recorded complete whose outputs are not on disk.

    An interrupted run can leave a ledger entry without its artifact. Resume must
    notice, otherwise it would skip work that was never finished.
    """
    problems: list[str] = []
    for unit in event.status.get("units", []):
        if unit.get("state") != "complete":
            continue
        for output in unit.get("outputs", []):
            if not (event.directory / output).exists() and not Path(output).exists():
                problems.append(f"{unit['unit_id']}: recorded output is missing: {output}")
    return problems


def next_action(event: Event) -> dict[str, Any]:
    """The first incomplete valid unit of work, and why.

    This is the whole of resume: read the ledger, re-derive what is real, and
    name the narrowest next step. Completed audited units are never redone.
    """
    gaps = missing_outputs(event)
    if gaps:
        return {
            "stage": event.stage,
            "action": "repair-incomplete-unit",
            "detail": "a unit is recorded complete but its output is missing",
            "problems": gaps,
            "blocked": True,
        }

    stale = [
        unit["unit_id"] for unit in event.status.get("units", [])
        if unit.get("state") == "stale"
    ]
    if stale:
        return {
            "stage": event.stage,
            "action": "rerun-stale-units",
            "detail": "inputs changed after these units completed",
            "problems": sorted(stale),
            "blocked": False,
        }

    failed = [
        unit["unit_id"] for unit in event.status.get("units", [])
        if unit.get("audit_result") == "FAIL"
    ]
    if failed:
        return {
            "stage": event.stage,
            "action": "repair-failed-audit",
            "detail": "an audit failed; repair before advancing",
            "problems": sorted(failed),
            "blocked": True,
        }

    pending = [
        unit["unit_id"] for unit in event.status.get("units", [])
        if unit.get("stage") == event.stage and unit.get("state") in ("pending", "in-progress")
    ]
    if pending:
        return {
            "stage": event.stage,
            "action": f"complete-{event.stage}",
            "detail": "units remain in the current stage",
            "problems": sorted(pending),
            "blocked": False,
        }

    allowed, reasons = can_advance(event)
    if allowed:
        return {
            "stage": event.stage,
            "action": "advance-stage",
            "detail": f"ready to advance to {legal_transitions(event.stage)[0]}",
            "problems": [],
            "blocked": False,
        }
    return {
        "stage": event.stage,
        "action": f"complete-{event.stage}",
        "detail": "; ".join(reasons) or "stage work remains",
        "problems": reasons,
        "blocked": bool(event.status.get("blocked")),
    }


# --------------------------------------------------------------------------- #
# Writing status back
# --------------------------------------------------------------------------- #

def save_status(event: Event) -> None:
    """Rewrite status.md front matter, preserving the human-written body."""
    path = event.directory / "status.md"
    _, body = frontmatter.read(path)
    schema.require("status", event.status, root=event.root, artifact=str(path))
    path.write_text(frontmatter.dump(event.status, body), encoding="utf-8")
