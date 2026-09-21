"""Event lifecycle: initialization, state transitions, staleness, and resume.

`events/<event>/status.md` is the recovery ledger. Its front matter is the
machine-readable state; the Markdown body below it stays human-reviewable.

A stage advances only forwards along the declared sequence, and only when the
current stage's audit gate has passed. A unit is complete only when its outputs
exist *and* its recorded input digest still matches its inputs; when an input
changes, everything downstream becomes ``stale`` rather than silently wrong.
"""

from __future__ import annotations

import json
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

# Directories a new event gets and a validator routes, but that an event is not
# required to have. D27: `calibration-report.md` and `manual-override-record.md`
# described artifacts with no kind, no schema and nowhere to live, so anything
# written from them was unvalidated — and a manual override is the last artifact
# that should be unchecked. Making them *required* would instead have made both
# completed events retroactively invalid for lacking an empty directory, which is
# the trade D10 and D26 both refused.
# D22 adds `matchup-passes` on the same terms: an event with no tournament round
# never produces one, and requiring the directory would invalidate a completed
# event for lacking something it had no occasion to write.
OPTIONAL_EVENT_SUBDIRS = ("calibrations", "overrides", "matchup-passes")

ALL_EVENT_SUBDIRS = EVENT_SUBDIRS + OPTIONAL_EVENT_SUBDIRS

REQUIRED_FILES = ("event.md", "teams.md", "status.md", "bracket.md")
TEMPLATE_DIR = "events/_template"

PASS_RESULTS = ("PASS", "PASS WITH ADVISORIES")

# What must exist before a stage may be considered complete. A gate flag with no
# work behind it let an event reach `complete` with zero artifacts.
STAGE_REQUIREMENTS = {
    "evidence": ("evidence/{team}/manifest.md",),
    "initial-judging": ("judgments/{team}/",),
    "consolidation": ("summaries/{team}.md",),
    "bracket": ("bracket.json",),
    "dossiers": ("dossiers/{team}.md",),
}


def stage_work_present(event: "Event", stage: str) -> list[str]:
    """Report the artifacts a stage requires but does not have."""
    missing: list[str] = []
    for pattern in STAGE_REQUIREMENTS.get(stage, ()):
        if "{team}" in pattern:
            for team in event.eligible_teams:
                target = event.directory / pattern.format(team=team["id"])
                if pattern.endswith("/"):
                    if not target.is_dir() or not any(target.glob("*.md")):
                        missing.append(f"{pattern.format(team=team['id'])} is empty or absent")
                elif not target.is_file():
                    missing.append(f"{pattern.format(team=team['id'])} is missing")
        elif not (event.directory / pattern).exists():
            missing.append(f"{pattern} is missing")

    if stage == "initial-judging":
        configured = [str(j) for j in event.config.get("expected_judges") or []]
        for team in event.eligible_teams:
            directory = event.directory / "judgments" / team["id"]
            present = {path.stem for path in directory.glob("*.md")} if directory.is_dir() else set()
            for judge in configured:
                if judge not in present:
                    missing.append(f"judgments/{team['id']}/{judge}.md is missing")
    if stage == "tournament":
        matchups = event.directory / "matchups"
        if not matchups.is_dir() or not any(matchups.glob("*.md")):
            missing.append("matchups/ contains no matchup report")
    return missing


def gate_blocking_findings(metadata: dict[str, Any]) -> list[dict[str, Any]]:
    """The findings in an audit that must hold a stage gate.

    D16: `can_advance` branched on an audit's verdict alone, and an auditor had
    no way to mark a finding as outside the thing being gated. In
    live-trial-2026 the `judgments-audited` gate took three passes and five
    repair rounds, and those repair rounds produced five new defects. At the
    second pass the two findings holding the gate were that a framework document
    said "three" where it meant "four", and a numbering collision between two
    branches. Neither is inside `events/`, inside the audited stage, or attached
    to any score. Repairing them introduced three more findings, two of which
    held the gate again.

    A finding holds the gate when it is `scope: event` and the auditor marked it
    `blocking: true`. Both are the auditor's judgment, deliberately: severity
    alone does not decide it, and an auditor who cannot say "real, recorded, and
    not about this stage" will keep having their verdict overruled by prose.
    """
    findings = metadata.get("findings")
    if not isinstance(findings, list):
        return []
    return [
        entry for entry in findings
        if isinstance(entry, dict)
        and entry.get("scope") == "event"
        and entry.get("blocking") is True
    ]


def gate_findings_problems(metadata: dict[str, Any], name: str) -> list[str]:
    """Why this audit does or does not authorize its gate.

    With structured `findings`, the scope filter decides and a verdict of FAIL
    can stand in the record while the gate still opens — which is the state
    live-trial-2026 was actually in for two of its three judging passes. Without
    them, behaviour is unchanged: the verdict alone decides.
    """
    result = str(metadata.get("result", ""))
    findings = metadata.get("findings")
    if not isinstance(findings, list):
        if result not in PASS_RESULTS:
            return [f"{name}: result is {result!r}; a gate needs {' or '.join(PASS_RESULTS)}"]
        return []

    holding = gate_blocking_findings(metadata)
    if holding:
        named = ", ".join(str(entry.get("id") or "?") for entry in holding)
        return [
            f"{name}: {len(holding)} blocking event-scope finding(s) hold this gate: {named}"
        ]
    if result not in PASS_RESULTS and not findings:
        return [
            f"{name}: result is {result!r} and no findings are recorded. A failing "
            f"audit must say what failed, with a scope and a blocking flag on each "
            f"finding, before the gate can read past the verdict."
        ]
    return []


def gate_opens_over_a_failing_verdict(metadata: dict[str, Any]) -> str | None:
    """A one-line record of a gate that opened while the verdict was not a pass.

    This must never be silent. The point of D16 is that a FAIL can be true and
    still not be about the stage being gated; the point of recording it is that
    nobody should later find a passed gate behind a failed audit and have to
    reconstruct why.
    """
    result = str(metadata.get("result", ""))
    findings = metadata.get("findings")
    if result in PASS_RESULTS or not isinstance(findings, list) or not findings:
        return None
    if gate_blocking_findings(metadata):
        return None
    outside = sum(1 for f in findings if isinstance(f, dict) and f.get("scope") != "event")
    non_blocking = len(findings) - outside
    return (
        f"result is {result!r} and the gate opened: {len(findings)} finding(s), "
        f"{outside} outside this event and {non_blocking} not marked blocking. "
        f"No finding is both event-scope and blocking."
    )


def audit_supports_gate(
    path: Path, *, stage: str, root: Path, event_id: str | None = None
) -> list[str]:
    """Whether an audit artifact actually authorizes passing *this* stage gate.

    An audit from another event, or about another stage, is not authorization.
    Both were previously accepted because only the file's existence was checked.
    """
    problems: list[str] = []
    if not path.is_file():
        return [f"audit artifact not found: {path}"]
    try:
        metadata, body = frontmatter.read(path)
    except Exception as exc:  # noqa: BLE001 - reported, not raised
        return [f"{path.name}: {exc}"]
    if event_id and metadata.get("event_id") != event_id:
        problems.append(
            f"{path.name}: audits event {metadata.get('event_id')!r}, not {event_id!r}"
        )
    scope = str(metadata.get("audit_scope") or "")
    if stage and stage not in scope.lower().replace("_", "-"):
        problems.append(
            f"{path.name}: audit_scope {scope!r} does not name the {stage!r} stage"
        )
    problems.extend(gate_findings_problems(metadata, path.name))
    if metadata.get("approval_state") != "approved":
        problems.append(f"{path.name}: approval_state is {metadata.get('approval_state')!r}")
    if metadata.get("visibility") != "private":
        problems.append(f"{path.name}: an audit record is private")
    if not str(metadata.get("audit_scope") or "").strip():
        problems.append(f"{path.name}: no audit_scope recorded")
    if not body.strip():
        problems.append(f"{path.name}: the audit has no content")
    return problems

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
    table = parse_roster_table(roster_body)
    if "teams" in roster and table:
        # Two rosters in one file is exactly the duplicate-source problem the
        # canonical model exists to remove, and the front-matter copy used to win
        # silently.
        raise ValidationError(
            "teams.md declares a `teams:` list in its front matter and a roster table in "
            "its body. Keep one. The reviewed Markdown table is the intended source.",
            artifact=str(event_dir / "teams.md"),
        )
    if "teams" not in roster:
        roster = dict(roster, teams=table)
    roster = dict(roster, teams=_with_consolidated_scores(event_dir, roster.get("teams") or []))
    return Event(directory=event_dir, root=base, config=config, status=status, roster=roster)


def _with_consolidated_scores(
    event_dir: Path, teams: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Attach each team's finalized consolidated total, read from its summary.

    The score is not copied onto the roster. `summaries/<team>.md` is where
    consolidation wrote it, and that is where the bracket reads it from, so there
    is only ever one editable copy of a team's official total.
    """
    enriched: list[dict[str, Any]] = []
    for team in teams:
        summary = event_dir / "summaries" / f"{team['id']}.md"
        if summary.is_file():
            try:
                metadata, _ = frontmatter.read(summary)
            except Exception:  # noqa: BLE001 - a malformed summary is reported elsewhere
                metadata = {}
            if metadata.get("finalized") and metadata.get("display_total") is not None:
                team = dict(team, score=float(metadata["display_total"]))
        enriched.append(team)
    return enriched


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

def initialize(
    event_id: str, *, root: Path | None = None, event_name: str | None = None,
    destination: Path | None = None,
) -> Path:
    """Create an event directory.

    ``root`` locates the framework (the template and the canonical rubrics);
    ``destination`` is where the event is written. They are the same in a
    checkout and deliberately different for an installed package, which must not
    write event data into site-packages.
    """
    base = root or canon.repository_root()
    ids.require_slug(event_id, kind="event_id")
    source = base / TEMPLATE_DIR
    if not source.is_dir():
        raise ValidationError(f"event template not found: {source}")
    target = (destination or base) / "events" / event_id
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
    for subdir in ALL_EVENT_SUBDIRS:
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
        # Scores arrive at consolidation; only enforce once the bracket is due,
        # and only when the policy actually has byes to allocate. D20: this used
        # to fire on the policy name alone. An event whose team count is an exact
        # power of two grants zero byes, so the policy consumes no score, and a
        # single unscored team made the event permanently invalid with no
        # permitted repair — the only two moves available were to fabricate a
        # total or to change the bye policy of an active event.
        if STAGE_INDEX.get(event.stage, 0) >= STAGE_INDEX["bracket"] and bye_count(event):
            unscored = [t["id"] for t in event.eligible_teams if t.get("score") is None]
            if unscored:
                problems.append(
                    f"performance-qualified byes need a consolidated score for every eligible "
                    f"team; missing for {sorted(unscored)}"
                )
    return problems


def bye_count(event: Event) -> int:
    """How many byes this event's bracket grants.

    The committed bracket is authoritative once it exists, because a bracket may
    be built from a subset of the roster. Before that, derive it the way
    `atj.bracket` will: the gap between the eligible team count and the next
    power of two.
    """
    from . import bracket as bracket_module

    path = event.directory / "bracket.json"
    if path.is_file():
        try:
            recorded = json.loads(path.read_text(encoding="utf-8")).get("bye_count")
        except (OSError, ValueError):
            recorded = None
        if isinstance(recorded, int):
            return recorded
    count = len(event.eligible_teams)
    if count < 2:
        return 0
    return bracket_module.bracket_size(count) - count


_CHECKBOX = re.compile(r"^-\s+\[([ xX])\]\s+(.+?)\s*$", re.MULTILINE)


def status_checkbox_labels(root: Path) -> tuple[list[str], str | None]:
    """The stage-gate checkbox labels, read from the event template.

    The labels have one home, `events/_template/status.md`, and they are paired
    with `STAGE_GATES` by position: the template writes them in stage order, and
    a count that disagrees is a defect in the template rather than something to
    guess around.
    """
    template = root / TEMPLATE_DIR / "status.md"
    if not template.is_file():
        return [], None
    _, body = frontmatter.read(template)
    labels = [label for _, label in _CHECKBOX.findall(body)]
    gate_count = len(STAGE_GATES)
    if len(labels) < gate_count:
        return [], None
    return labels[:gate_count], labels[gate_count] if len(labels) > gate_count else None


def sync_status_checkboxes(event: Event, body: str) -> str:
    """Rewrite the body's stage-gate checkboxes to match the ledger.

    Intake audit F4. `atj event gate` and `atj event advance` wrote the front
    matter and left the body alone, so every passing gate put `status.md` into
    the exact state `validate_status_narrative` rejects, and the operator had to
    tick the box by hand before the next validate would pass. live-trial-2026
    finished in that state; that is D30.

    The body is prose about the ledger, so the ledger writes it. Anything in the
    body that is not one of the known gate labels is left untouched.
    """
    gate_labels, complete_label = status_checkbox_labels(event.root)
    if not gate_labels:
        return body
    gates = event.status.get("stage_gates") or {}
    wanted = {
        label: str(gates.get(gate, "pending")) == "passed"
        for gate, label in zip(STAGE_GATES.values(), gate_labels)
    }
    if complete_label:
        wanted[complete_label] = event.stage == "complete"

    def replace(match: re.Match[str]) -> str:
        label = match.group(2)
        if label not in wanted:
            return match.group(0)
        return f"- [{'x' if wanted[label] else ' '}] {label}"

    return _CHECKBOX.sub(replace, body)


def validate_status_narrative(event: Event) -> list[str]:
    """The prose in status.md must agree with the ledger above it.

    D30. `status.md` carries the ledger in its front matter and a human-readable
    summary in its body, and nothing compared the two. live-trial-2026 finished
    with `final-audit-passed: passed`, `current_stage: complete` and two approved
    dossiers in its front matter, while its own body still showed the final audit
    unchecked, the event not marked complete, and both dossiers "pending".

    This is D19's shape one file over: an artifact asserting something false in
    its own voice. The state file is the one place an operator looks to answer
    "where is this event", so a body that disagrees with the ledger is worse than
    no body at all.
    """
    problems: list[str] = []
    status_path = event.directory / "status.md"
    if not status_path.is_file():
        return problems
    try:
        _, body = frontmatter.read(status_path)
    except ValidationError:
        return problems  # reported by validate_status
    boxes = {label: mark.lower() == "x" for mark, label in _CHECKBOX.findall(body)}
    if not boxes:
        return problems

    gate_labels, complete_label = status_checkbox_labels(event.root)
    gates = event.status.get("stage_gates") or {}
    for gate, label in zip(STAGE_GATES.values(), gate_labels):
        if label not in boxes:
            problems.append(
                f"status.md body no longer lists the {gate!r} checkbox ({label!r}); "
                f"a reader cannot see the gate state from the body"
            )
            continue
        recorded = str(gates.get(gate, "pending"))
        if boxes[label] != (recorded == "passed"):
            problems.append(
                f"status.md body says {label!r} is "
                f"{'checked' if boxes[label] else 'unchecked'} while the ledger records "
                f"{gate}: {recorded}. The body is prose about the ledger and may not "
                f"contradict it"
            )
    if complete_label and complete_label in boxes:
        complete = event.stage == "complete"
        if boxes[complete_label] != complete:
            problems.append(
                f"status.md body says {complete_label!r} is "
                f"{'checked' if boxes[complete_label] else 'unchecked'} while "
                f"current_stage is {event.stage!r}"
            )
    return problems


def validate_status(event: Event) -> list[str]:
    problems = schema.validate(
        "status", event.status, root=event.root, artifact=str(event.directory / "status.md")
    )
    stage = event.status.get("current_stage")
    if stage not in STAGE_INDEX:
        problems.append(f"unknown current_stage: {stage!r}")
    problems += validate_status_narrative(event)
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

    missing = stage_work_present(event, stage)
    if missing:
        reasons.append(
            f"{stage} has no completed work for: " + "; ".join(sorted(missing)[:6])
            + (" …" if len(missing) > 6 else "")
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

    # Advancing over stale work builds the next stage on inputs that changed.
    drifted = [entry["unit_id"] for entry in stale_units(event)]
    if drifted:
        reasons.append(
            f"inputs changed after these units completed: {sorted(drifted)}; "
            f"re-run them before advancing"
        )

    # An event may be *run* past a bypassed gate -- that is what `--force-reason`
    # is for, and stopping the event dead would only teach an operator to edit
    # the ledger by hand. It may not be *called complete* while nobody has read
    # the bypass. This is the one place the framework can insist on the review
    # it cannot perform, and it is the last transition, so it costs no in-flight
    # work.
    if stage == "final-audit":
        unread = [
            entry for entry in overrides(event) if not entry.get("reviewed_by")
        ]
        if unread:
            described = ", ".join(
                f"{entry.get('from')}->{entry.get('to')} ({entry.get('authorized_by')})"
                for entry in unread
            )
            reasons.append(
                f"{len(unread)} stage gate bypass(es) have not been reviewed: {described}. "
                f"Read them with `atj event overrides <event>` and record the review; the "
                f"framework cannot tell whether a bypass was justified, only that nobody "
                f"has looked"
            )
    return (not reasons), reasons


def advance(
    event: Event, *, force_reason: str | None = None, force_approver: str | None = None
) -> str:
    """Move to the next stage. Raises unless the gate is satisfied.

    An override is a human act that must leave a trace. An empty or whitespace
    reason is not a reason: it previously slipped past the gate check *and* the
    recording, so an event could reach `complete` with nothing written down.
    """
    reason = (force_reason or "").strip()
    approver = (force_approver or "").strip()
    forcing = bool(reason)
    if force_reason is not None and not reason:
        raise StateError(
            "--force-reason must give an actual reason. An override is a human decision "
            "and is recorded as one.",
            artifact=str(event.directory),
        )
    if forcing and not approver:
        raise StateError(
            "an override must name the official who authorized it: pass --force-approver.",
            artifact=str(event.directory),
        )

    allowed, reasons = can_advance(event)
    if not allowed and not forcing:
        raise StateError(
            f"cannot advance from {event.stage!r}: " + "; ".join(reasons),
            artifact=str(event.directory),
        )
    source = event.stage
    targets = legal_transitions(source)
    if not targets:
        raise StateError(f"{source!r} is terminal")
    event.status["current_stage"] = targets[0]
    event.status["last_updated"] = versions.now()
    if forcing:
        event.status.setdefault("overrides", []).append({
            "from": source, "to": targets[0], "reason": reason,
            "authorized_by": approver, "bypassed": reasons,
            "recorded_at": event.status["last_updated"],
        })
    return targets[0]


def overrides(event: Event) -> list[dict[str, Any]]:
    """Every stage advance that bypassed a gate, oldest first.

    The framework refuses to pass a gate without a matching audit, to advance a
    winner without a confirmed result, and to publish without a named approver.
    `--force-reason` is the one door through all of that, and the final audit of
    the release recorded that no command summarised what had gone through it
    (advisory 6). A control whose exercise nobody can list is a control nobody
    can review.
    """
    return list(event.status.get("overrides") or [])


def review_override(
    event: Event, index: int, *, official: str, note: str | None = None
) -> dict[str, Any]:
    """Record that a human read one override. Never that it was justified."""
    recorded = overrides(event)
    if not 0 <= index < len(recorded):
        raise StateError(
            f"no override at index {index}; the event has {len(recorded)}",
            artifact=str(event.directory),
        )
    entry = event.status["overrides"][index]
    entry["reviewed_by"] = official
    entry["reviewed_at"] = versions.now()
    if note:
        entry["review_note"] = note
    event.status["last_updated"] = entry["reviewed_at"]
    return entry


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
    completed_at: str | None = None,
) -> dict[str, Any]:
    """Write or update one ledger unit.

    ``completed_at`` records when the *work* finished, not when the ledger row
    was last touched. D15: this used to be ``versions.now()`` unconditionally, so
    re-recording a unit to carry an audit result forward overwrote the real
    completion time with the clock at repair time — and the ledger is what
    `stale_units` and the audit trail read.

    The rule now: if the unit already completed and its input digest is
    unchanged, the same work is being re-recorded and the original time stands.
    A changed digest means different inputs produced this unit, so it is stamped
    anew. ``completed_at`` overrides both, and the caller may pass ``"now"``.
    """
    unit = find_unit(event, unit_id)
    if state != "complete":
        stamp = None
    elif completed_at and completed_at != "now":
        stamp = completed_at
    elif completed_at == "now":
        stamp = versions.now()
    elif (
        unit is not None
        and unit.get("state") == "complete"
        and unit.get("completed_at")
        and unit.get("input_digest") == input_digest
    ):
        stamp = str(unit["completed_at"])
    else:
        stamp = versions.now()
    payload = {
        "unit_id": unit_id,
        "stage": stage,
        "state": state,
        "input_digest": input_digest,
        "outputs": sorted(outputs),
        "audit_result": audit_result,
        "completed_at": stamp,
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


def derive_digests(event: Event) -> dict[str, str]:
    """Recompute each standard unit's input digest from what is on disk now.

    This is what makes staleness real rather than a data structure nobody fills
    in: an edited judgment or evidence manifest changes the digest, and the unit
    that depended on it no longer matches its recorded one.
    """
    digests: dict[str, str] = {}
    for team in event.eligible_teams:
        team_id = team["id"]
        manifest = event.directory / "evidence" / team_id / "manifest.md"
        package = ""
        if manifest.is_file():
            try:
                metadata, _ = frontmatter.read(manifest)
                package = str(metadata.get("evidence_package_id") or "")
            except Exception:  # noqa: BLE001 - reported by report validation
                package = "unreadable"
            digests[f"evidence:{team_id}"] = unit_digest(
                str(team.get("commit") or ""), ids.file_digest(manifest, length=16)
            )

        judgments = event.directory / "judgments" / team_id
        if judgments.is_dir():
            parts = [package]
            for path in sorted(judgments.glob("*.md")):
                parts.append(f"{path.name}:{ids.file_digest(path, length=16)}")
            digests[f"judging:{team_id}"] = unit_digest(*parts)

        summary = event.directory / "summaries" / f"{team_id}.md"
        if summary.is_file():
            digests[f"consolidation:{team_id}"] = unit_digest(
                package, ids.file_digest(summary, length=16)
            )

        dossier = event.directory / "dossiers" / f"{team_id}.md"
        if dossier.is_file():
            # A dossier is derived from the team's own consolidated report and
            # from the matchups it took part in; both are in its digest, so
            # re-consolidating or re-judging a matchup makes the dossier stale.
            parts = [package, ids.file_digest(dossier, length=16)]
            if summary.is_file():
                parts.append(ids.file_digest(summary, length=16))
            for matchup in sorted((event.directory / "matchups").glob("*.md")):
                if team_id in matchup.read_text(encoding="utf-8", errors="replace"):
                    parts.append(f"{matchup.name}:{ids.file_digest(matchup, length=16)}")
            digests[f"dossier:{team_id}"] = unit_digest(*parts)

    # D21: the bracket, tournament and dossier stages could not be recorded as
    # ledger units at all, because no digest was derived for them. They were
    # invisible to `stale_units` and to the drift check in `can_advance`, so an
    # edited bracket or matchup report left every later stage looking current.
    drawn = event.directory / "bracket.json"
    if drawn.is_file():
        roster = event.directory / "teams.md"
        parts = [ids.file_digest(drawn, length=16)]
        if roster.is_file():
            parts.append(ids.file_digest(roster, length=16))
        # The draw is a function of the eligible roster and of the consolidated
        # scores that seed it, so a summary that moves after the draw is drift.
        # The summaries are digested from disk rather than read off the enriched
        # roster: `Event.load` fills scores in from those same files, and a digest
        # that depended on how the Event was constructed would differ between the
        # process that recorded the unit and the one that re-derives it.
        for team in event.eligible_teams:
            summary_path = event.directory / "summaries" / f"{team['id']}.md"
            if summary_path.is_file():
                parts.append(f"{team['id']}:{ids.file_digest(summary_path, length=16)}")
        digests["bracket:draw"] = unit_digest(*parts)

    matchups = event.directory / "matchups"
    if matchups.is_dir():
        for report in sorted(matchups.glob("*.md")):
            match_id = report.stem
            parts = [f"{report.name}:{ids.file_digest(report, length=16)}"]
            resolved = matchups / f"{match_id}.json"
            if resolved.is_file():
                parts.append(f"{resolved.name}:{ids.file_digest(resolved, length=16)}")
            for pass_report in sorted(
                (event.directory / "matchup-passes").glob(f"{match_id}-pass-*.md")
            ):
                parts.append(f"{pass_report.name}:{ids.file_digest(pass_report, length=16)}")
            digests[f"matchup:{match_id}"] = unit_digest(*parts)

    # The final-audit stage is a unit too, and its inputs are the audit it rests
    # on plus the public summary it authorizes. Recorded with an invented digest,
    # it was the last unit in the sample ledger that drift detection skipped.
    final_audit = event.directory / "audits" / "final-event.md"
    if not final_audit.is_file():
        final_audit = event.directory / "audits" / "final.md"
    if final_audit.is_file():
        parts = [ids.file_digest(final_audit, length=16)]
        summary = event.directory / "public" / "event-summary.md"
        if summary.is_file():
            parts.append(ids.file_digest(summary, length=16))
        digests["final:audit"] = unit_digest(*parts)
    return digests


def stale_units(event: Event) -> list[dict[str, str]]:
    """Units whose recorded inputs no longer match what is on disk."""
    current = derive_digests(event)
    drifted: list[dict[str, str]] = []
    for unit in event.status.get("units", []):
        unit_id = unit.get("unit_id")
        expected = current.get(unit_id)
        if expected is None:
            continue
        if unit.get("input_digest") != expected:
            drifted.append({
                "unit_id": unit_id,
                "recorded": str(unit.get("input_digest")),
                "actual": expected,
            })
    return drifted


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

    drifted = stale_units(event)
    if drifted:
        return {
            "stage": event.stage,
            "action": "rerun-stale-units",
            "detail": "inputs changed after these units completed",
            "problems": [
                f"{entry['unit_id']}: recorded {entry['recorded']}, now {entry['actual']}"
                for entry in drifted
            ],
            "blocked": False,
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
    """Rewrite status.md atomically, preserving the human-written body.

    An interrupt part-way through a direct write truncated the recovery ledger,
    which is the one file recovery depends on. Write to a temporary file, keep a
    backup of the previous ledger, then replace in one step.
    """
    import os

    path = event.directory / "status.md"
    _, body = frontmatter.read(path)
    body = sync_status_checkboxes(event, body)
    schema.require("status", event.status, root=event.root, artifact=str(path))
    rendered = frontmatter.dump(event.status, body)

    backup = path.with_suffix(".md.bak")
    try:
        backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    except OSError:
        pass
    temporary = path.with_suffix(".md.tmp")
    temporary.write_text(rendered, encoding="utf-8")
    os.replace(temporary, path)
