"""`atj` — the deterministic command line for the framework.

One entry point replaces the five disconnected scripts of v0.1.0-alpha, which
had incompatible input conventions, duplicated the official weights, and could
not see each other's output.

Exit codes: 0 success, 1 validation or audit failure, 2 usage or environment
error. Errors print as ``code: message [artifact]`` rather than a traceback,
because operators run these commands, not developers.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from . import (
    VERSION, bracket, canon, event as event_module, frontmatter, ids, matchup,
    publication, render, reports, sandbox, schema, scoring, versions,
)
from .errors import AtjError

OK, FAILURE, USAGE = 0, 1, 2


def _root(args) -> Path:
    return Path(args.root).resolve() if getattr(args, "root", None) else canon.repository_root()


def _emit(payload: Any, args) -> None:
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2, sort_keys=True, default=str))


def _print_findings(findings) -> None:
    for finding in findings:
        print(f"  {finding.render()}")


# --------------------------------------------------------------------------- #
# rubric / schemas / personas
# --------------------------------------------------------------------------- #

def cmd_rubric(args) -> int:
    root = _root(args)
    rubric = canon.load(root)
    payload = {
        "reference": rubric.reference,
        "scale": [rubric.scale_min, rubric.scale_max],
        "total_weight": rubric.total_weight,
        "criteria": [
            {"id": c.id, "name": c.name, "weight": c.weight, "question": c.question}
            for c in rubric.criteria
        ],
        "source": rubric.source,
    }
    if args.json:
        _emit(payload, args)
        return OK
    print(f"{rubric.reference}  scale {rubric.scale_min}-{rubric.scale_max}  "
          f"total {rubric.total_weight}")
    for criterion in rubric.criteria:
        print(f"  {criterion.id:12s} {criterion.weight:3d}  {criterion.name}")
    print(f"source: {rubric.source}")
    return OK


def cmd_schemas(args) -> int:
    root = _root(args)
    problems = schema.check_schemas(root)
    _emit({"problems": problems}, args)
    if problems:
        print("Schema check: FAIL")
        for problem in problems:
            print(f"  {problem}")
        return FAILURE
    print(f"Schema check: PASS ({len(schema.ARTIFACT_SCHEMAS)} artifact schemas)")
    return OK


def cmd_personas(args) -> int:
    root = _root(args)
    if args.refresh:
        changed = versions.refresh_personas(root)
        for line in changed:
            print(f"  updated {line}")
        print(f"Persona digests refreshed ({len(changed)} changed)")
        return OK
    problems = versions.check_personas(root)
    _emit({"problems": problems}, args)
    if problems:
        print("Persona registry: FAIL")
        for problem in problems:
            print(f"  {problem}")
        return FAILURE
    registry = versions.load_personas(root)
    print(f"Persona registry: PASS ({len(registry)} agents)")
    for persona in sorted(registry.values(), key=lambda p: p.agent_id):
        print(f"  {persona.reference:34s} {persona.role}")
    return OK


# --------------------------------------------------------------------------- #
# event
# --------------------------------------------------------------------------- #

def cmd_event_init(args) -> int:
    root = _root(args)
    target = event_module.initialize(args.event_id, root=root, event_name=args.name)
    loaded = event_module.load(target, root=root)
    problems = event_module.validate_configuration(loaded)
    print(f"Created {target}")
    if problems:
        print("Configuration is not yet complete:")
        for problem in problems:
            print(f"  {problem}")
        print("Fill in event.md and teams.md, then run: atj event validate " + str(target))
        return OK
    print("Configuration validates. Next: complete teams.md, then `atj event validate`.")
    return OK


def cmd_event_validate(args) -> int:
    root = _root(args)
    loaded = event_module.load(Path(args.event_dir), root=root)
    problems: list[str] = []
    problems += [f"config: {p}" for p in event_module.validate_configuration(loaded, strict=args.strict)]
    problems += [f"status: {p}" for p in event_module.validate_status(loaded)]
    problems += [f"roster: {p}" for p in event_module.validate_roster(loaded)]
    try:
        versions.require_personas(root)
    except AtjError as exc:
        problems.append(f"personas: {exc.message}")
    _emit({"problems": problems}, args)
    for problem in problems:
        print(f"  ERROR {problem}")
    print(f"Event validation: {'FAIL' if problems else 'PASS'} "
          f"({len(problems)} problems, stage {loaded.stage})")
    return FAILURE if problems else OK


def cmd_event_status(args) -> int:
    root = _root(args)
    loaded = event_module.load(Path(args.event_dir), root=root)
    action = event_module.next_action(loaded)
    allowed, reasons = event_module.can_advance(loaded)
    gates = loaded.status.get("stage_gates") or {}
    units = loaded.status.get("units") or []
    payload = {
        "event_id": loaded.event_id,
        "stage": loaded.stage,
        "blocked": bool(loaded.status.get("blocked")),
        "next_action": action,
        "can_advance": allowed,
        "reasons": reasons,
        "gates": gates,
        "units": units,
    }
    _emit(payload, args)
    if args.json:
        return OK
    print(f"Event {loaded.event_id}  stage: {loaded.stage}")
    print(f"  teams: {len(loaded.teams)} on roster, {len(loaded.eligible_teams)} eligible")
    print(f"  gate: {event_module.STAGE_GATES.get(loaded.stage, '-')} = "
          f"{gates.get(event_module.STAGE_GATES.get(loaded.stage, ''), 'pending')}")
    states: dict[str, int] = {}
    for unit in units:
        states[unit.get("state", "?")] = states.get(unit.get("state", "?"), 0) + 1
    print(f"  units: {states or 'none recorded'}")
    print(f"  next: {action['action']} — {action['detail']}")
    for problem in action["problems"][:10]:
        print(f"    - {problem}")
    if allowed:
        print(f"  ready to advance to: {event_module.legal_transitions(loaded.stage)[0]}")
    else:
        for reason in reasons:
            print(f"  blocked: {reason}")
    return OK


def cmd_event_advance(args) -> int:
    root = _root(args)
    loaded = event_module.load(Path(args.event_dir), root=root)
    try:
        target = event_module.advance(loaded, force_reason=args.force_reason)
    except AtjError as exc:
        print(exc.render())
        return FAILURE
    event_module.save_status(loaded)
    print(f"Stage advanced to {target}"
          + (f" (override recorded: {args.force_reason})" if args.force_reason else ""))
    return OK


def cmd_event_gate(args) -> int:
    root = _root(args)
    loaded = event_module.load(Path(args.event_dir), root=root)
    gates = loaded.status.setdefault("stage_gates", {})
    if args.gate not in event_module.STAGE_GATES.values():
        print(f"usage: unknown gate {args.gate!r}; expected one of "
              f"{', '.join(sorted(set(event_module.STAGE_GATES.values())))}")
        return USAGE
    gates[args.gate] = args.state
    loaded.status["last_updated"] = versions.now()
    event_module.save_status(loaded)
    print(f"Gate {args.gate} = {args.state}")
    return OK


# --------------------------------------------------------------------------- #
# scoring
# --------------------------------------------------------------------------- #

def _judgments_from(args, root: Path) -> list[scoring.Judgment]:
    source = Path(args.source)
    if source.is_dir():
        return scoring.load_panel(source, root=root)
    payload = json.loads(source.read_text(encoding="utf-8"))
    if "weights" in payload:
        # Alpha defect B1: caller-supplied weights silently replaced the rubric.
        raise AtjError(
            "input supplies 'weights'; official weights come only from "
            f"{canon.SUBMISSION_RUBRIC} and may not be overridden"
        )
    return [
        scoring.Judgment(
            judge_id=entry["judge_id"],
            judge_run_id=entry.get("judge_run_id", f"jr:x:x:{entry['judge_id']}:00000000:01"),
            team_id=entry.get("team_id", payload.get("team_id", "unknown")),
            commit=entry.get("commit", payload.get("commit", "0" * 40)),
            evidence_package_id=entry.get(
                "evidence_package_id", payload.get("evidence_package_id", "ev:x:x:" + "0" * 12 + ":00000000")
            ),
            rubric=entry.get("rubric", payload.get("rubric", canon.load(root).reference)),
            persona=entry.get("persona", f"{entry['judge_id']}@1.0.0"),
            scores=entry["scores"],
            confidence=entry.get("confidence") or {},
            source=str(source),
        )
        for entry in payload["judges"]
    ]


def cmd_score(args) -> int:
    root = _root(args)
    judgments = _judgments_from(args, root)
    expected = args.expect.split(",") if args.expect else None
    result = scoring.consolidate(judgments, expected_judges=expected, root=root)
    if args.json:
        _emit(result, args)
        return OK if result["finalized"] else FAILURE
    print(render.consolidated_table(result))
    if args.output:
        Path(args.output).write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"\nwrote {args.output}")
    return OK if result["finalized"] else FAILURE


def cmd_matchup(args) -> int:
    root = _root(args)
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if "close_call_band" in payload:
        raise AtjError(
            "the close-call band may not be set from a matchup input file. It comes from "
            f"{canon.HEAD_TO_HEAD_RUBRIC}, and an event may only widen it through validated "
            "event configuration (--event-dir)."
        )
    band = None
    if args.event_dir:
        loaded = event_module.load(Path(args.event_dir), root=root)
        versions.require_versions(
            dict(loaded.config), root=root, artifact=str(Path(args.event_dir) / "event.md")
        )
        band = loaded.config.get("close_call_band")
    result = matchup.calculate(
        team_a=payload["team_a"],
        team_b=payload["team_b"],
        a_first=payload["a_first"],
        b_first=payload["b_first"],
        close_call_band=band,
        root=root,
    )
    if args.json:
        _emit(result, args)
    else:
        print(render.matchup_table(result))
    if args.output:
        Path(args.output).write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    return OK


# --------------------------------------------------------------------------- #
# bracket
# --------------------------------------------------------------------------- #

def cmd_bracket_build(args) -> int:
    root = _root(args)
    if args.event_dir:
        loaded = event_module.load(Path(args.event_dir), root=root)
        teams = loaded.eligible_teams
        event_id = loaded.event_id
        policy = args.bye_policy or loaded.config.get("bye_policy", bracket.DEFAULT_BYE_POLICY)
        roster_version = int(loaded.roster.get("roster_version", 1))
    else:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        teams = payload["teams"]
        event_id = payload.get("event_id", "adhoc")
        policy = args.bye_policy or payload.get("bye_policy", bracket.DEFAULT_BYE_POLICY)
        roster_version = int(payload.get("roster_version", 1))

    result = bracket.build(
        event_id=event_id, teams=teams, seed=args.seed, bye_policy=policy,
        roster_version=roster_version, framework_commit=versions.framework_commit(root), root=root,
    )
    problems = bracket.verify(result) + schema.validate("bracket", result, root=root)
    if args.json:
        _emit(result, args)
    else:
        print(render.bracket_tables(result))
    if args.output:
        Path(args.output).write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"\nwrote {args.output}")
    if problems:
        print("\nBracket verification FAILED:")
        for problem in problems:
            print(f"  {problem}")
        return FAILURE
    if not result["feasible"]:
        print("\nBracket built but hard constraints could not all be satisfied:")
        for constraint in result["unsatisfied_hard_constraints"]:
            print(f"  {constraint}")
        print("  An event official must accept these exceptions before the draw is used.")
        return FAILURE
    return OK


def cmd_bracket_verify(args) -> int:
    root = _root(args)
    result = json.loads(Path(args.bracket).read_text(encoding="utf-8"))
    teams = None
    if args.reproduce:
        teams = json.loads(Path(args.reproduce).read_text(encoding="utf-8"))["teams"]
    elif args.event_dir:
        teams = event_module.load(Path(args.event_dir), root=root).eligible_teams
    problems = bracket.verify(result, teams) + schema.validate("bracket", result, root=root)
    rebuilt = None
    if args.reproduce:
        rebuilt = bracket.build(
            event_id=result["event_id"], teams=teams, seed=result["seed"],
            bye_policy=result["bye_policy"], roster_version=result["roster_version"],
            framework_commit=result["framework_commit"], root=root,
        )
        if rebuilt["rounds"] != result["rounds"]:
            problems.append("bracket does not reproduce from its recorded seed and roster")
    _emit({"problems": problems}, args)
    for problem in problems:
        print(f"  ERROR {problem}")
    print(f"Bracket verification: {'FAIL' if problems else 'PASS'}"
          + (" (reproduced from seed)" if rebuilt and not problems else ""))
    return FAILURE if problems else OK


# --------------------------------------------------------------------------- #
# report validation
# --------------------------------------------------------------------------- #

def cmd_validate_reports(args) -> int:
    root = _root(args)
    event_dir = Path(args.event_dir)
    try:
        loaded = event_module.load(event_dir, root=root)
        public_scores = bool(loaded.config.get("public_scores"))
        team_ids = [team["id"] for team in loaded.teams]
    except AtjError:
        public_scores, team_ids = False, []
    found = reports.validate_event_reports(
        event_dir, root=root, public_scores=public_scores, all_teams=team_ids
    )
    summary = reports.summarize(found)
    if args.json:
        _emit({
            "artifacts": summary["artifacts"], "counts": summary["counts"],
            "result": summary["result"],
            "findings": [vars(f) for f in summary["findings"]],
        }, args)
        return FAILURE if summary["result"] == "FAIL" else OK
    for report in found:
        if report.findings:
            print(f"{report.path}")
            _print_findings(report.findings)
    counts = summary["counts"]
    print(f"Report validation: {summary['result']} — {summary['artifacts']} artifacts, "
          f"{counts['blocking']} blocking, {counts['major']} major, "
          f"{counts['minor']} minor, {counts['advisory']} advisory")
    return FAILURE if summary["result"] == "FAIL" else OK


def cmd_check_publication(args) -> int:
    """Gate a single artifact before it is shown to anyone outside the panel."""
    root = _root(args)
    path = Path(args.artifact)
    event_dir = Path(args.event_dir) if args.event_dir else path.parent.parent
    metadata, body = frontmatter.read(path)
    try:
        loaded = event_module.load(event_dir, root=root)
        public_scores = bool(loaded.config.get("public_scores"))
        team_ids = [team["id"] for team in loaded.teams]
    except AtjError:
        public_scores, team_ids = False, []
    findings = publication.check_artifact(
        path, event_dir, metadata, body, public_scores=public_scores, all_teams=team_ids
    )
    _emit({"findings": [vars(f) for f in findings]}, args)
    blocking = [f for f in findings if f.severity == "blocking"]
    _print_findings(findings)
    print(f"Publication check: {'BLOCKED' if blocking else 'CLEAR'} "
          f"({len(blocking)} blocking, {len(findings) - len(blocking)} other)")
    return FAILURE if blocking else OK


# --------------------------------------------------------------------------- #
# release check
# --------------------------------------------------------------------------- #

def cmd_release_check(args) -> int:
    root = _root(args)
    failures: list[str] = []

    rubric = canon.load(root)
    if rubric.total_weight != 100:
        failures.append(f"rubric weights total {rubric.total_weight}, expected 100")
    print(f"rubric            {rubric.reference}, {len(rubric.criteria)} criteria, "
          f"total {rubric.total_weight}")

    problems = schema.check_schemas(root)
    failures += [f"schema: {p}" for p in problems]
    print(f"schemas           {'PASS' if not problems else 'FAIL'} "
          f"({len(schema.ARTIFACT_SCHEMAS)} artifact schemas)")

    problems = versions.check_personas(root)
    failures += [f"persona: {p}" for p in problems]
    print(f"personas          {'PASS' if not problems else 'FAIL'}")

    problems = check_templates(root)
    failures += [f"template: {p}" for p in problems]
    print(f"templates         {'PASS' if not problems else 'FAIL'}")

    problems = check_claude_components(root)
    failures += [f"claude: {p}" for p in problems]
    print(f"claude components {'PASS' if not problems else 'FAIL'}")

    problems = check_no_duplicate_weights(root)
    failures += [f"duplicate-number: {p}" for p in problems]
    print(f"single-source     {'PASS' if not problems else 'FAIL'}")

    problems = check_declared_versions(root)
    failures += [f"version-skew: {p}" for p in problems]
    print(f"version-skew      {'PASS' if not problems else 'FAIL'}")

    problems = check_sample_event(root)
    failures += [f"sample-event: {p}" for p in problems]
    print(f"sample event      {'PASS' if not problems else 'FAIL'}")

    _emit({"failures": failures}, args)
    if failures:
        print("\nRelease check: FAIL")
        for failure in failures:
            print(f"  {failure}")
        return FAILURE
    print("\nRelease check: PASS")
    return OK


def check_templates(root: Path) -> list[str]:
    """Every template must carry the identity fields an official artifact needs."""
    required = (
        "event_id", "rubric", "framework_commit", "visibility",
        "approval_state", "validation_state", "started_at", "completed_at",
    )
    problems: list[str] = []
    directory = root / reports.TEMPLATE_DIR
    for path in sorted(directory.glob("*.md")):
        try:
            metadata, _ = frontmatter.read(path)
        except AtjError as exc:
            problems.append(f"{path.name}: {exc.message}")
            continue
        for field in required:
            if field not in metadata:
                problems.append(f"{path.name}: missing {field}")
        if metadata.get("visibility") == "public":
            for field in publication.PRIVATE_ONLY_FIELDS:
                if field in metadata:
                    problems.append(f"{path.name}: public template carries private field {field!r}")
    return problems


VERSIONED_FIELDS = ("rubric", "source_rubric", "consolidation_policy",
                    "matchup_rubric", "bracket_policy")


def check_declared_versions(root: Path) -> list[str]:
    """Every version literal in the framework must resolve against the canon.

    Templates, the event template and the rubrics themselves all spell out
    references like ``submission-evaluation@1.0.0``. Bumping a rubric used to
    leave those silently pointing at a version that no longer exists.
    """
    problems: list[str] = []
    targets = sorted((root / "framework" / "templates").glob("*.md"))
    targets += sorted((root / "framework" / "rubrics").glob("*.md"))
    targets += sorted((root / "events" / "_template").glob("*.md"))
    placeholder = re.compile(r"[A-Z]{3,}")
    for path in targets:
        try:
            metadata, _ = frontmatter.read(path)
        except AtjError:
            # A document with no front matter declares no version. Prose files
            # such as framework/rubrics/README.md are not version carriers.
            continue
        checkable = {
            field: str(metadata[field])
            for field in VERSIONED_FIELDS
            if metadata.get(field) and not placeholder.search(str(metadata[field]))
        }
        if not checkable:
            continue
        # Persona is checked separately by `atj personas`; a template legitimately
        # carries `PERSONA@VERSION` until it is instantiated.
        payload = dict(checkable)
        payload.setdefault("rubric", canon.load(root).reference)
        if metadata.get("close_call_band") is not None:
            payload["close_call_band"] = metadata["close_call_band"]
        try:
            versions.require_versions(payload, root=root, artifact=str(path))
        except AtjError as exc:
            problems.append(f"{path.relative_to(root)}: {exc.message}")
    return problems


def check_sample_event(root: Path) -> list[str]:
    """The committed sample event must still demonstrate every required case."""
    from . import demo

    if not (root / "events" / demo.EVENT_ID).is_dir():
        return [f"the sample event is missing from events/{demo.EVENT_ID}"]
    return demo.check_conditions(root)


def check_claude_components(root: Path) -> list[str]:
    """Structural check of project-local agents, skills, and commands."""
    problems: list[str] = []
    for kind, pattern, required in (
        ("agent", ".claude/agents/*.md", ("name", "description")),
        ("skill", ".claude/skills/*/SKILL.md", ("name", "description")),
        ("command", ".claude/commands/*.md", ("description",)),
    ):
        paths = sorted(root.glob(pattern))
        if not paths:
            problems.append(f"no {kind} definitions found at {pattern}")
        for path in paths:
            try:
                metadata, body = frontmatter.read(path)
            except AtjError as exc:
                problems.append(f"{kind} {path.name}: {exc.message}")
                continue
            for field in required:
                if not metadata.get(field):
                    problems.append(f"{kind} {path.name}: missing {field}")
            if not body.strip():
                problems.append(f"{kind} {path.name}: empty body")
            if kind == "skill" and metadata.get("name") != path.parent.name:
                problems.append(
                    f"skill {path.parent.name}: front-matter name {metadata.get('name')!r} "
                    f"does not match its directory"
                )
            if kind == "agent" and metadata.get("name") != path.stem:
                problems.append(
                    f"agent {path.name}: front-matter name {metadata.get('name')!r} "
                    f"does not match its filename"
                )
    return problems


def check_no_duplicate_weights(root: Path) -> list[str]:
    """No second editable copy of the official weights outside the rubric.

    Scans the whole tree, not just the Python. Alpha defect X1 was a Python dict;
    a Markdown table or a JSON enum would be exactly as damaging.
    """
    import re as _re

    rubric = canon.load(root)
    rubric_path = (root / canon.SUBMISSION_RUBRIC).resolve()
    pattern = _re.compile(
        r"""["']?(""" + "|".join(rubric.criterion_ids) + r""")["']?\s*[:=]\s*(\d+)"""
    )
    skip_parts = {".git", "__pycache__", "node_modules", "dist", ".pytest_cache"}
    # Narrow exemptions only. `tests/` asserts against the real weights on
    # purpose, and the baseline audit quotes the alpha's duplicate as evidence.
    # Everything else, including the rest of `docs/`, is scanned.
    allowed = {
        rubric_path,
        (root / "tests").resolve(),
        (root / "docs" / "release-readiness-audit.md").resolve(),
    }
    problems: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in (".py", ".json", ".md", ".yaml", ".yml"):
            continue
        if skip_parts & set(path.parts):
            continue
        resolved = path.resolve()
        if resolved in allowed or any(
            base.is_dir() and str(resolved).startswith(str(base) + "/") for base in allowed
        ):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for criterion, value in pattern.findall(text):
            if int(value) == rubric.weights[criterion]:
                problems.append(
                    f"{path.relative_to(root)}: holds an editable copy of the official weight "
                    f"for {criterion!r} ({value})"
                )
                break
    return problems


# --------------------------------------------------------------------------- #
# sandbox
# --------------------------------------------------------------------------- #

def cmd_sandbox_preflight(args) -> int:
    capability = sandbox.preflight(args.runtime)
    payload = {
        "available": capability.available, "runtime": capability.runtime,
        "version": capability.version, "rootless": capability.rootless,
        "reasons": capability.reasons, "execution_status": capability.execution_status,
        "evidence_limitation": sandbox.evidence_limitation(capability),
    }
    _emit(payload, args)
    if args.json:
        return OK if capability.available else FAILURE
    print(f"Sandbox preflight: {'AVAILABLE' if capability.available else 'UNAVAILABLE'}")
    print(f"  {capability.summary()}")
    if not capability.available:
        limitation = sandbox.evidence_limitation(capability)
        print(f"  record execution_status: {limitation['execution_status']}")
        print(f"  criteria needing NE unless other direct evidence exists: "
              f"{', '.join(limitation['evidence_limited_criteria'])}")
        print("  There is no host fallback. Static inspection may continue.")
    return OK if capability.available else FAILURE


def cmd_sandbox_run(args) -> int:
    capability = sandbox.preflight(args.runtime)
    record = sandbox.run_in_sandbox(
        source=Path(args.source), command=args.command, image=args.image,
        limits={"timeout_seconds": args.timeout} if args.timeout else None,
        capability=capability,
    )
    _emit(record.to_dict(), args)
    if not args.json:
        print(f"exit status: {record.exit_status}"
              + ("  (timed out)" if record.timed_out else ""))
        print(f"duration: {record.duration_seconds:.2f}s  runtime: {record.runtime} "
              f"{record.runtime_version}")
        if record.stdout:
            print("--- stdout ---")
            print(record.stdout)
        if record.stderr:
            print("--- stderr ---")
            print(record.stderr)
    if args.output:
        Path(args.output).write_text(
            json.dumps(record.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    return OK if record.exit_status == 0 else FAILURE


# --------------------------------------------------------------------------- #
# demo
# --------------------------------------------------------------------------- #

def cmd_demo(args) -> int:
    from . import demo, demo_writer

    root = _root(args)
    if args.action == "build":
        directory = demo_writer.build(root)
        print(f"Rebuilt {directory.relative_to(root)} and the 20-team bracket fixture.")
    directory = root / "events" / demo.EVENT_ID
    if not directory.is_dir():
        print(f"sample event not found at {directory}; run `atj demo build`", file=sys.stderr)
        return FAILURE

    problems: list[str] = []
    problems += [f"condition: {p}" for p in demo.check_conditions(root)]

    loaded = event_module.load(directory, root=root)
    problems += [f"config: {p}" for p in event_module.validate_configuration(loaded)]
    problems += [f"roster: {p}" for p in event_module.validate_roster(loaded)]
    problems += [f"status: {p}" for p in event_module.validate_status(loaded)]

    found = reports.validate_event_reports(
        directory, root=root, public_scores=bool(loaded.config.get("public_scores")),
        all_teams=[team["id"] for team in loaded.teams],
    )
    summary = reports.summarize(found)
    problems += [
        f"report: {finding.render()}" for finding in summary["findings"]
        if finding.severity in ("blocking", "major")
    ]

    drawn = json.loads((directory / "bracket.json").read_text(encoding="utf-8"))
    problems += [f"bracket: {p}" for p in bracket.verify(drawn, loaded.eligible_teams)]
    if drawn["rounds"] != demo.sample_bracket(root)["rounds"]:
        problems.append("bracket: committed draw does not reproduce from its recorded seed")

    fixture_dir = root / "tests" / "fixtures" / "bracket-20-team"
    fixture = json.loads((fixture_dir / "bracket.json").read_text(encoding="utf-8"))
    fixture_roster = json.loads((fixture_dir / "roster.json").read_text(encoding="utf-8"))["teams"]
    problems += [f"fixture: {p}" for p in bracket.verify(fixture, fixture_roster)]
    if fixture["rounds"] != demo.twenty_team_bracket(root)["rounds"]:
        problems.append("fixture: 20-team bracket does not reproduce from its recorded seed")

    _emit({"problems": problems}, args)
    if not args.json:
        print(f"Sample event: {len(found)} artifacts validated")
        for problem in problems:
            print(f"  ERROR {problem}")
        print(f"Demo check: {'FAIL' if problems else 'PASS'}")
    return FAILURE if problems else OK


# --------------------------------------------------------------------------- #
# argument parsing
# --------------------------------------------------------------------------- #

def _shared() -> argparse.ArgumentParser:
    """Options accepted both before and after the subcommand."""
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--root", help="framework root (default: auto-detected)")
    shared.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return shared


def build_parser() -> argparse.ArgumentParser:
    shared = _shared()
    parser = argparse.ArgumentParser(
        parents=[shared],
        prog="atj",
        description="Deterministic tooling for the AI Tournament Judge framework. "
                    "Calculation, validation, rendering, state transitions and seeded "
                    "bracket assignment are deterministic; LLM judgment is not.",
    )
    parser.add_argument("--version", action="version", version=f"atj {VERSION}")
    sub = parser.add_subparsers(dest="command", required=True, parser_class=lambda **kw: argparse.ArgumentParser(parents=[shared], **kw))

    sub.add_parser("rubric", help="print the canonical rubric").set_defaults(func=cmd_rubric)
    sub.add_parser("schemas", help="self-check the shipped schemas").set_defaults(func=cmd_schemas)

    personas = sub.add_parser("personas", help="check or refresh persona versions")
    personas.add_argument("--refresh", action="store_true", help="recompute content digests")
    personas.set_defaults(func=cmd_personas)

    event_parser = sub.add_parser("event", help="event lifecycle operations")
    event_sub = event_parser.add_subparsers(dest="event_command", required=True)

    init = event_sub.add_parser("init", help="create an event from the template")
    init.add_argument("event_id")
    init.add_argument("--name", help="human-readable event name")
    init.set_defaults(func=cmd_event_init)

    validate = event_sub.add_parser("validate", help="validate configuration, roster and status")
    validate.add_argument("event_dir")
    validate.add_argument("--strict", action="store_true", help="treat placeholders as errors")
    validate.set_defaults(func=cmd_event_validate)

    status = event_sub.add_parser("status", help="report stage, gates and the next safe action")
    status.add_argument("event_dir")
    status.set_defaults(func=cmd_event_status)

    advance = event_sub.add_parser("advance", help="advance to the next stage")
    advance.add_argument("event_dir")
    advance.add_argument("--force-reason", help="human override; recorded in the ledger")
    advance.set_defaults(func=cmd_event_advance)

    gate = event_sub.add_parser("gate", help="record a stage gate result")
    gate.add_argument("event_dir")
    gate.add_argument("gate")
    gate.add_argument("state", choices=("pending", "passed", "failed"))
    gate.set_defaults(func=cmd_event_gate)

    score = sub.add_parser("score", help="consolidate a judge panel")
    score.add_argument("source", help="judgments directory, or a JSON file of judge scores")
    score.add_argument("--expect", help="comma-separated configured judge ids")
    score.add_argument("--output", help="write the structured result to this path")
    score.set_defaults(func=cmd_score)

    match = sub.add_parser("matchup", help="resolve an order-balanced head-to-head")
    match.add_argument("input", help="JSON with team_a, team_b, a_first, b_first")
    match.add_argument("--event-dir", help="read the event's close-call band from its config")
    match.add_argument("--output")
    match.set_defaults(func=cmd_matchup)

    bracket_parser = sub.add_parser("bracket", help="bracket assignment")
    bracket_sub = bracket_parser.add_subparsers(dest="bracket_command", required=True)

    build = bracket_sub.add_parser("build", help="draw a reproducible bracket")
    source = build.add_mutually_exclusive_group(required=True)
    source.add_argument("--event-dir")
    source.add_argument("--input", help="JSON with a teams array")
    build.add_argument("--seed", required=True, help="recorded and required for reproduction")
    build.add_argument("--bye-policy", choices=bracket.BYE_POLICIES)
    build.add_argument("--output")
    build.set_defaults(func=cmd_bracket_build)

    verify = bracket_sub.add_parser("verify", help="re-check a built bracket")
    verify.add_argument("bracket")
    verify.add_argument("--reproduce", help="team JSON to redraw and compare against")
    verify.add_argument(
        "--event-dir",
        help="re-derive the constraints from this event's roster instead of trusting "
             "the audit block inside the bracket file",
    )
    verify.set_defaults(func=cmd_bracket_verify)

    validate_parser = sub.add_parser("validate", help="artifact validation")
    validate_sub = validate_parser.add_subparsers(dest="validate_command", required=True)

    report_validate = validate_sub.add_parser("reports", help="validate every report in an event")
    report_validate.add_argument("event_dir")
    report_validate.set_defaults(func=cmd_validate_reports)

    publish = validate_sub.add_parser("publication", help="gate one artifact before disclosure")
    publish.add_argument("artifact")
    publish.add_argument("--event-dir")
    publish.set_defaults(func=cmd_check_publication)

    sandbox_parser = sub.add_parser("sandbox", help="isolated execution of untrusted code")
    sandbox_sub = sandbox_parser.add_subparsers(dest="sandbox_command", required=True)

    preflight = sandbox_sub.add_parser(
        "preflight", help="report whether verified isolation is available"
    )
    preflight.add_argument("--runtime", choices=(sandbox.PODMAN, sandbox.DOCKER))
    preflight.set_defaults(func=cmd_sandbox_preflight)

    run = sandbox_sub.add_parser("run", help="run one command against a submission, isolated")
    run.add_argument("source", help="submission checkout; mounted read-only")
    run.add_argument("command", nargs="+")
    run.add_argument("--image", default="docker.io/library/python:3.12-alpine")
    run.add_argument("--runtime", choices=(sandbox.PODMAN, sandbox.DOCKER))
    run.add_argument("--timeout", type=int, help="seconds")
    run.add_argument("--output", help="write the execution record here")
    run.set_defaults(func=cmd_sandbox_run)

    demo_parser = sub.add_parser("demo", help="the committed synthetic sample event")
    demo_parser.add_argument(
        "action", nargs="?", default="check", choices=("build", "check"),
        help="'build' regenerates it; 'check' verifies the committed one",
    )
    demo_parser.set_defaults(func=cmd_demo)

    sub.add_parser(
        "release-check", help="framework-level checks required before a release"
    ).set_defaults(func=cmd_release_check)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except AtjError as exc:
        print(exc.render(), file=sys.stderr)
        return FAILURE
    except FileNotFoundError as exc:
        print(f"usage: file not found: {exc.filename}", file=sys.stderr)
        return USAGE
    except json.JSONDecodeError as exc:
        print(f"usage: invalid JSON input: {exc}", file=sys.stderr)
        return USAGE
    except BrokenPipeError:
        return OK


if __name__ == "__main__":
    raise SystemExit(main())
