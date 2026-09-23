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
    egress, VERSION, bracket, canon, event as event_module, frontmatter, ids, intake,
    matchup, publication, render, reports, sandbox, schema, scoring, versions,
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
    if not versions.components_available(root):
        print(
            "Component registry: SKIPPED — no .claude/ components here. This looks like "
            "an installed package rather than a working copy; run from a checkout to "
            "check agent and skill versions."
        )
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
    # Events belong to the operator's working directory, not to wherever the
    # package happens to be installed. `--root` still overrides for tests.
    destination = Path(args.dir).resolve() if args.dir else (
        root if getattr(args, "root", None) else Path.cwd()
    )
    if "site-packages" in destination.parts or (destination / "atj" / "data").is_dir():
        raise AtjError(
            f"refusing to create an event inside an installed package at {destination}. "
            f"Run from the directory that should hold events/, or pass --dir."
        )
    target = event_module.initialize(
        args.event_id, root=root, event_name=args.name, destination=destination
    )
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


def _save_status(loaded) -> None:
    """Write the ledger and say so when it rewrote the body.

    Intake audit F14 and F17. `save_status` rewrites the status body's gate
    checkboxes from the ledger, and a rewrite nobody is told about silently
    discards a deliberate hand edit. F14 wired the notice into `atj event gate`
    only, which left the advance -- the one write that can flip
    `Event marked complete` -- still silent. Every command that writes the
    ledger goes through here.
    """
    for label in event_module.save_status(loaded):
        print(f"  status.md body: {label!r} rewritten to match the ledger")


def cmd_event_advance(args) -> int:
    root = _root(args)
    loaded = event_module.load(Path(args.event_dir), root=root)
    try:
        target = event_module.advance(
            loaded, force_reason=args.force_reason, force_approver=args.force_approver
        )
    except AtjError as exc:
        print(exc.render())
        return FAILURE
    _save_status(loaded)
    print(f"Stage advanced to {target}"
          + (f" (override recorded: {args.force_reason})" if args.force_reason else ""))
    return OK


def cmd_event_overrides(args) -> int:
    """List the gate bypasses, and let a human record that they read one.

    The release's final audit closed with six controls that "end in a human and
    cannot be verified further", and noted that no command summarised
    `status.overrides` for review. This is that command. It reports what was
    bypassed; it never judges whether the bypass was justified, because that is
    the judgment it exists to put in front of a person.
    """
    root = _root(args)
    loaded = event_module.load(Path(args.event_dir), root=root)
    recorded = event_module.overrides(loaded)

    if args.review is not None:
        if not args.official:
            print("usage: --review requires --official", file=sys.stderr)
            return USAGE
        entry = event_module.review_override(
            loaded, args.review, official=args.official, note=args.note
        )
        _save_status(loaded)
        _emit({"reviewed": entry}, args)
        if not args.json:
            print(f"override {args.review} marked reviewed by {args.official} "
                  f"at {entry['reviewed_at']}")
            print("  Recording that it was read. Not that it was justified.")
        return OK

    unreviewed = [entry for entry in recorded if not entry.get("reviewed_by")]
    _emit({
        "overrides": recorded,
        "count": len(recorded),
        "unreviewed": len(unreviewed),
    }, args)
    if not args.json:
        if not recorded:
            print(f"{args.event_dir}: no stage gate was ever bypassed")
            return OK
        print(f"{args.event_dir}: {len(recorded)} override(s), {len(unreviewed)} unreviewed")
        for index, entry in enumerate(recorded):
            print(f"\n  [{index}] {entry.get('from')} -> {entry.get('to')}  "
                  f"{entry.get('recorded_at')}")
            print(f"      authorized by: {entry.get('authorized_by')}")
            print(f"      reason:        {entry.get('reason')}")
            for bypassed in entry.get("bypassed") or []:
                print(f"      bypassed:      {bypassed}")
            if entry.get("reviewed_by"):
                print(f"      reviewed by:   {entry['reviewed_by']} at {entry.get('reviewed_at')}")
                if entry.get("review_note"):
                    print(f"      review note:   {entry['review_note']}")
            else:
                print(f"      reviewed:      NO — "
                      f"`atj event overrides {args.event_dir} --review {index} "
                      f"--official <role>`")
        if unreviewed:
            print("\nAn unreviewed override is an open question, not a failure. The "
                  "framework cannot tell whether a bypass was justified; it can only "
                  "refuse to let one go unread.")
    return FAILURE if unreviewed else OK


def cmd_event_unit(args) -> int:
    """Write the ledger `atj event status` reads to decide what to resume."""
    root = _root(args)
    loaded = event_module.load(Path(args.event_dir), root=root)
    derived = event_module.derive_digests(loaded)

    if args.action == "list":
        drifted = {entry["unit_id"] for entry in event_module.stale_units(loaded)}
        rows = []
        for unit in loaded.status.get("units", []):
            rows.append({
                "unit_id": unit["unit_id"], "stage": unit.get("stage"),
                "state": "stale" if unit["unit_id"] in drifted else unit.get("state"),
                "audit_result": unit.get("audit_result"),
                "input_digest": unit.get("input_digest"),
                "current_digest": derived.get(unit["unit_id"]),
            })
        _emit({"units": rows}, args)
        if not args.json:
            for row in rows:
                flag = " STALE" if row["state"] == "stale" else ""
                print(f"  {row['unit_id']:32s} {row['stage']:16s} {row['state']:12s} "
                      f"{row['audit_result']}{flag}")
            print(f"{len(rows)} unit(s), {len(drifted)} stale")
        return FAILURE if drifted else OK

    if not args.id:
        print("usage: --id is required for record and stale", file=sys.stderr)
        return USAGE

    if args.action == "stale":
        event_module.mark_stale(loaded, args.id, args.reason or "invalidated by an operator")
        _save_status(loaded)
        print(f"{args.id} marked stale")
        return OK

    digest = derived.get(args.id)
    if digest is None:
        print(
            f"usage: cannot derive an input digest for {args.id!r}. Known units: "
            f"{', '.join(sorted(derived)) or 'none — the artifacts do not exist yet'}",
            file=sys.stderr,
        )
        return USAGE
    stage = args.stage or args.id.split(":", 1)[0]
    existing = event_module.find_unit(loaded, args.id)
    if args.completed_at and args.completed_at != "now":
        if not frontmatter.TIMESTAMP.match(args.completed_at):
            print(f"usage: --completed-at {args.completed_at!r} is not a UTC timestamp "
                  f"(YYYY-MM-DDTHH:MM:SSZ) or 'now'", file=sys.stderr)
            return USAGE
    unit = event_module.record_unit(
        loaded, unit_id=args.id, stage=stage, input_digest=digest,
        outputs=args.output, audit_result=args.audit_result,
        completed_at=args.completed_at,
    )
    _save_status(loaded)
    print(f"{args.id} recorded complete (digest {digest}, audit {args.audit_result})")
    if (
        existing is not None
        and existing.get("completed_at")
        and unit.get("completed_at") == existing.get("completed_at")
    ):
        print(f"  completed_at kept at {unit['completed_at']} — the inputs did not change. "
              f"Pass --completed-at now to restamp it.")
    return OK


APPROVAL_STATES = ("draft", "pending-approval", "approved", "rejected", "withdrawn")


def cmd_event_approve(args) -> int:
    """Set `approval_state` on event artifacts, with the validation behind it.

    D25: six sites in `atj` read `approval_state` and no code path wrote it, so
    every artifact stayed `draft` through every gate. The consequences were real
    in live-trial-2026 and verified in code: `atj/ceremony.py:372` refuses to
    render a dossier that is not approved, so neither deliverable could be
    released under a gate literally named `dossiers-approved`; and
    `atj/cli.py`'s guard against silently rewriting an approved judgment's
    scores table never armed for the entire event. `demo_writer.py` writes
    `approved` directly, so the one fixture that would have caught the gap
    bypassed it.

    Approving runs the artifact's own validation first and writes
    `validation_state` from the result. An approval is a claim that a human
    official reviewed a valid artifact; approving something the validator
    rejects is the failure the whole gate chain exists to prevent, so it is
    refused rather than warned about.

    `approved_by` and `approved_at` are recorded alongside. Every artifact
    schema allows additional properties, so this adds a fact rather than
    changing a shape, and an approval with no name on it is not an approval.
    """
    root = _root(args)
    event_dir = Path(args.event_dir) if args.event_dir else None
    paths: list[Path] = []
    for target in args.paths:
        path = Path(target)
        if event_dir is None:
            event_dir = _event_root_of(path if path.is_dir() else path.parent)
        paths.extend(sorted(path.rglob("*.md")) if path.is_dir() else [path])
    if event_dir is None:
        raise AtjError(
            "cannot locate the event these artifacts belong to; pass --event-dir. "
            "Approval is an event official's act and is recorded against an event."
        )
    if not paths:
        raise AtjError(f"no artifacts found under {', '.join(args.paths)}")

    loaded = event_module.load(event_dir, root=root)
    official = args.official or (loaded.config.get("officials") or {}).get(
        "publication_approval"
    )
    if not official:
        raise AtjError(
            f"no approving official. Pass --official <role>, or record one as "
            f"`officials.publication_approval` in {event_dir / 'event.md'}. An "
            f"approval with no official behind it is a flag, not an approval."
        )

    public_scores = bool(loaded.config.get("public_scores"))
    team_ids = [team["id"] for team in loaded.teams]
    display_names = {
        str(team.get("id")): str(team.get("display_name") or team.get("id"))
        for team in loaded.teams
    }
    totals = publication.official_totals(event_dir)

    stamp = versions.now()
    planned: list[tuple[Path, dict, str, str]] = []
    refused: list[tuple[Path, list]] = []
    for path in paths:
        metadata, body = frontmatter.read(path)
        report = reports.validate_artifact(
            path, event_dir, root=root, public_scores=public_scores,
            all_teams=team_ids, display_names=display_names, totals=totals,
        )
        disqualifying = [
            f for f in report.findings if f.severity in ("blocking", "major")
        ]
        state = "valid" if not disqualifying else "invalid"
        if args.state == "approved" and disqualifying:
            refused.append((path, disqualifying))
            continue
        metadata["validation_state"] = state
        metadata["approval_state"] = args.state
        if args.state == "approved":
            metadata["approved_by"] = official
            metadata["approved_at"] = stamp
            if args.note:
                metadata["approval_note"] = args.note
        else:
            for field in ("approved_by", "approved_at", "approval_note"):
                metadata.pop(field, None)
        planned.append((path, metadata, body, state))

    if refused:
        _emit({"refused": [
            {"artifact": str(path),
             "findings": [vars(f) for f in findings]} for path, findings in refused
        ]}, args)
        if not args.json:
            print(f"Refused to approve {len(refused)} artifact(s); nothing was written.")
            for path, findings in refused:
                print(f"  {path}")
                for finding in findings:
                    print(f"    {finding.render()}")
            print("\nAn approval says a human official reviewed a valid artifact. "
                  "Repair the findings, or approve the artifacts individually.")
        return FAILURE

    for path, metadata, body, _ in planned:
        path.write_text(frontmatter.dump(metadata, body), encoding="utf-8")

    _emit({"state": args.state, "official": official, "at": stamp,
           "artifacts": [{"artifact": str(p), "validation_state": v}
                         for p, _, _, v in planned]}, args)
    if not args.json:
        for path, _, _, state in planned:
            print(f"{args.state:16s} {path} (validation {state})")
        print(f"{len(planned)} artifact(s) {args.state} by {official} at {stamp}")
    return OK


def cmd_event_gate(args) -> int:
    """Record a stage audit result.

    Passing a gate requires the audit artifact that justifies it. Without that,
    a gate was a boolean an operator could set with no audit behind it, and an
    event could reach `complete` in eighteen commands with zero artifacts.
    """
    root = _root(args)
    loaded = event_module.load(Path(args.event_dir), root=root)
    gates = loaded.status.setdefault("stage_gates", {})
    if args.gate not in event_module.STAGE_GATES.values():
        print(f"usage: unknown gate {args.gate!r}; expected one of "
              f"{', '.join(sorted(set(event_module.STAGE_GATES.values())))}")
        return USAGE

    stage = next(
        (name for name, gate in event_module.STAGE_GATES.items() if gate == args.gate), None
    )
    if args.state == "passed":
        if not args.audit:
            print(
                f"usage: passing a gate requires the audit that justifies it:\n"
                f"  atj event gate {args.event_dir} {args.gate} passed --audit "
                f"<audits/...md>",
                file=sys.stderr,
            )
            return USAGE
        audit_path = Path(args.audit)
        if not audit_path.is_absolute():
            candidate = loaded.directory / args.audit
            audit_path = candidate if candidate.exists() else audit_path
        problems = event_module.audit_supports_gate(
            audit_path, stage=stage or "", root=root, event_id=loaded.event_id
        )
        problems += [
            f"stage work missing: {item}"
            for item in event_module.stage_work_present(loaded, stage or "")
        ]
        if problems:
            print(f"Gate {args.gate} NOT passed:")
            for problem in problems:
                print(f"  {problem}")
            return FAILURE
        gates[args.gate] = "passed"
        loaded.status.setdefault("gate_evidence", {})[args.gate] = str(
            audit_path.relative_to(loaded.directory)
            if str(audit_path).startswith(str(loaded.directory)) else audit_path
        )
        # A gate that opened over a failing verdict is recorded in the ledger,
        # not just printed. Nobody should later find a passed gate behind a
        # failed audit and have to reconstruct why (D16).
        note = event_module.gate_opens_over_a_failing_verdict(
            frontmatter.read(audit_path)[0]
        )
        if note:
            loaded.status.setdefault("gate_notes", {})[args.gate] = note
            print(f"Gate {args.gate}: {note}")
        else:
            loaded.status.get("gate_notes", {}).pop(args.gate, None)
    else:
        gates[args.gate] = args.state
        loaded.status.get("gate_evidence", {}).pop(args.gate, None)
        loaded.status.get("gate_notes", {}).pop(args.gate, None)

    loaded.status["last_updated"] = versions.now()
    _save_status(loaded)
    print(f"Gate {args.gate} = {args.state}"
          + (f" (audit: {args.audit})" if args.state == "passed" else ""))
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


def _event_context(source: Path, root: Path) -> tuple[Path | None, list[str] | None]:
    """Locate the event a judgments directory belongs to.

    Finding it automatically is what stops `atj score` quietly finalizing a
    two-judge panel when the event configured four.
    """
    for candidate in [source, *source.parents]:
        if (candidate / "event.md").is_file() and (candidate / "status.md").is_file():
            try:
                loaded = event_module.load(candidate, root=root)
            except AtjError:
                return candidate, None
            return candidate, [str(j) for j in loaded.config.get("expected_judges") or []]
    return None, None


def cmd_score(args) -> int:
    root = _root(args)
    judgments = _judgments_from(args, root)
    source = Path(args.source)

    expected = args.expect.split(",") if args.expect else None
    adjudications = Path(args.adjudications) if args.adjudications else None
    event_dir, configured = _event_context(source if source.is_dir() else source.parent, root)
    if expected is None:
        expected = configured
    if adjudications is None and event_dir is not None:
        adjudications = event_dir / "adjudications"

    if expected is None:
        raise AtjError(
            "no configured judge list. Run this against a judgments directory inside an "
            "event, or pass --expect with the event's configured judges. Consolidating "
            "without knowing who was configured cannot detect a missing judge."
        )

    team_id = judgments[0].team_id if judgments else None
    resolutions = (
        scoring.load_resolutions(adjudications, team_id=team_id, root=root)
        if adjudications else {}
    )
    result = scoring.consolidate(
        judgments, expected_judges=expected, resolutions=resolutions, root=root
    )
    if resolutions and not args.json:
        for criterion, resolution in sorted(resolutions.items()):
            print(f"applied adjudication {resolution['adjudication_id']} to {criterion} "
                  f"(decided by {resolution['decided_by']})")
    if args.json:
        _emit(result, args)
        return OK if result["finalized"] else FAILURE
    print(render.consolidated_table(result))
    notice = render.adjudication_notice(result)
    if notice:
        print()
        print(notice)
    if args.output:
        Path(args.output).write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"\nwrote {args.output}")
    return OK if result["finalized"] else FAILURE


def cmd_render_judgment(args) -> int:
    """Generate the official scores table into an individual judgment.

    The judge writes raw scores and confidence in front matter and nothing else
    numeric. Weights, weighted points and the total come from the canonical
    rubric through :mod:`atj.scoring`, so a hand-copied weight cannot drift into
    an official artifact.

    Every file is scored and checked before any file is written. A run that is
    going to refuse refuses having changed nothing, rather than leaving the
    first half of a panel rendered and the second half not.
    """
    root = _root(args)
    planned: list[tuple[Path, dict, str]] = []
    unchanged: list[Path] = []
    forced: list[Path] = []
    for target in args.paths:
        path = Path(target)
        paths = sorted(path.glob("*.md")) if path.is_dir() else [path]
        if not paths:
            raise AtjError(f"no judgment files under {path}")
        for source in paths:
            metadata, body = frontmatter.read(source)
            judgment = scoring.Judgment.from_metadata(metadata, source=str(source))
            result = scoring.individual_score(judgment, root=root)
            table = render.individual_scores_table(result, root)
            rendered = render.replace_block(body, "scores", table)
            if rendered == body:
                unchanged.append(source)
                continue
            if metadata.get("approval_state") == "approved":
                if not args.force:
                    raise AtjError(
                        f"{source} is approved and rendering would change its scores "
                        f"table. An approved judgment is a reviewed artifact; silently "
                        f"rewriting its official numbers is how a panel comes to cite a "
                        f"total no one approved. Re-render before approval, or pass "
                        f"--force and record why in the event ledger. Nothing was "
                        f"written."
                    )
                forced.append(source)
            planned.append((source, metadata, rendered))

    for source, metadata, rendered in planned:
        source.write_text(frontmatter.dump(metadata, rendered), encoding="utf-8")

    written = [source for source, _, _ in planned]
    if args.json:
        _emit({"rendered": [str(s) for s in written],
               "unchanged": [str(s) for s in unchanged],
               "forced_over_approval": [str(s) for s in forced]}, args)
        return OK
    for source in written:
        print(f"rendered {source}" + (" (FORCED over approval)" if source in forced else ""))
    for source in unchanged:
        print(f"unchanged {source}")
    if forced:
        print(f"\n{len(forced)} approved judgment(s) re-rendered with --force. "
              f"Record why in the event ledger.")
    return OK


def cmd_render_consolidated(args) -> int:
    """Generate the official consolidated score block into a panel report.

    D18: `framework/templates/consolidated-team-report.md` names `atj consolidate`
    and carries an `atj:consolidated` marker region, and no command existed to
    fill it. Both of live-trial-2026's panel reports were therefore transcribed
    by hand, both consolidators disclosed it unprompted, and each table had to be
    verified cell by cell against `summaries/<team>.json` by a throwaway script.
    This is that check, built as the generator it should have been.

    The table comes from `atj.scoring.consolidate` over the team's judgments, the
    same call `atj score` makes, so the report cannot hold a number the tool did
    not produce. Front-matter `total`, `display_total`, `finalized` and
    `blocked_reasons` are written from the same result for the same reason.

    Every report is consolidated and checked before any is written, and an
    approved report is refused without --force, as for judgments.
    """
    root = _root(args)
    planned: list[tuple[Path, dict, str]] = []
    unchanged: list[Path] = []
    forced: list[Path] = []
    for target in args.paths:
        path = Path(target)
        paths = sorted(path.glob("*.md")) if path.is_dir() else [path]
        if not paths:
            raise AtjError(f"no consolidated reports under {path}")
        for source in paths:
            metadata, body = frontmatter.read(source)
            result = _consolidate_for_report(source, metadata, root=root)
            table = render.consolidated_table(result, root)
            rendered = render.replace_block(body, "consolidated", table)
            updates = {
                "total": result["total"],
                "display_total": result["display_total"],
                "finalized": result["finalized"],
                "blocked_reasons": list(result["blocked_reasons"]),
            }
            drift = {k: v for k, v in updates.items() if metadata.get(k) != v}
            if rendered == body and not drift:
                unchanged.append(source)
                continue
            if metadata.get("approval_state") == "approved":
                if not args.force:
                    raise AtjError(
                        f"{source} is approved and rendering would change its official "
                        f"numbers ({', '.join(sorted(drift)) or 'score table'}). An "
                        f"approved panel report is a reviewed artifact. Re-render before "
                        f"approval, or pass --force and record why in the event ledger. "
                        f"Nothing was written."
                    )
                forced.append(source)
            metadata.update(updates)
            planned.append((source, metadata, rendered))

    for source, metadata, rendered in planned:
        source.write_text(frontmatter.dump(metadata, rendered), encoding="utf-8")

    written = [source for source, _, _ in planned]
    if args.json:
        _emit({"rendered": [str(s) for s in written],
               "unchanged": [str(s) for s in unchanged],
               "forced_over_approval": [str(s) for s in forced]}, args)
        return OK
    for source in written:
        print(f"rendered {source}" + (" (FORCED over approval)" if source in forced else ""))
    for source in unchanged:
        print(f"unchanged {source}")
    if forced:
        print(f"\n{len(forced)} approved report(s) re-rendered with --force. "
              f"Record why in the event ledger.")
    return OK


def _consolidate_for_report(source: Path, metadata: dict, *, root: Path) -> dict:
    """Consolidate the judgments behind one panel report.

    The report names its own team and lives inside its own event, so the inputs
    are derivable: `judgments/<team>/` for the panel, the event's configured
    judge list for who was expected, and `adjudications/` for any resolution
    that moves an official number. Deriving them rather than accepting them as
    arguments is what stops a report being rendered from the wrong panel.
    """
    event_dir = _event_root_of(source.parent)
    if event_dir is None:
        raise AtjError(
            f"{source} is not inside an event directory. A consolidated report is "
            f"rendered from the event's judgments, its configured judge list and its "
            f"adjudications; none of those can be located from a loose file."
        )
    team_id = str(metadata.get("team_id") or source.stem)
    judgments_dir = event_dir / "judgments" / team_id
    if not judgments_dir.is_dir():
        raise AtjError(f"no judgments directory for {team_id!r} at {judgments_dir}")
    judgments = scoring.load_panel(judgments_dir, root=root)
    loaded = event_module.load(event_dir, root=root)
    expected = [str(j) for j in loaded.config.get("expected_judges") or []]
    if not expected:
        raise AtjError(
            f"{event_dir / 'event.md'} configures no expected_judges. Consolidating "
            f"without knowing who was configured cannot detect a missing judge."
        )
    resolutions = scoring.load_resolutions(
        event_dir / "adjudications", team_id=team_id, root=root
    )
    return scoring.consolidate(
        judgments, expected_judges=expected, resolutions=resolutions, root=root
    )


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


def cmd_bracket_advance(args) -> int:
    """Advance a winner, and only a winner the framework or a human actually named.

    A matchup whose outcome is `adjudication-required` returns no winner. This
    refuses to advance anyone unless an approved adjudication for that match names
    the advancing team.
    """
    root = _root(args)
    path = Path(args.bracket)
    result = json.loads(path.read_text(encoding="utf-8"))
    metadata, _ = frontmatter.read(Path(args.matchup))

    match_id = args.match
    if metadata.get("match_id") != match_id:
        raise AtjError(
            f"{args.matchup} records match_id {metadata.get('match_id')!r}, not {match_id!r}"
        )

    winner = metadata.get("winner")
    outcome = metadata.get("outcome")
    if outcome != matchup.CONFIRMED or not winner:
        event_dir = Path(args.event_dir) if args.event_dir else Path(args.matchup).parent.parent
        winner = _adjudicated_winner(event_dir, match_id, root)
        if not winner:
            raise AtjError(
                f"{match_id} has outcome {outcome!r} and no approved adjudication naming a "
                f"winner. The framework does not advance a team here; a human official must "
                f"decide and record it in adjudications/."
            )
        print(f"advancing on a recorded human adjudication, not an automatic result")

    located = bracket.match_by_id(result, match_id)
    if located is None:
        raise AtjError(f"no match {match_id!r} in this bracket")
    _, match = located
    entrants = {entrant for entrant in (match.get("entrants") or []) if entrant}
    reported = {str(metadata.get("team_a")), str(metadata.get("team_b"))}
    if reported != entrants:
        raise AtjError(
            f"{args.matchup} compares {sorted(reported)} but the bracket records "
            f"{sorted(entrants)} for {match_id}. One of the two is wrong and an "
            f"operator cannot tell which from either alone."
        )
    undecided = [
        source for source in (match.get("source_matches") or [])
        if (bracket.match_by_id(result, source) or (0, {}))[1].get("winner") is None
    ]
    if undecided:
        raise AtjError(
            f"{match_id} draws from {undecided}, which have no recorded winner. "
            f"Deciding a later round first would advance a team that has not earned "
            f"its place."
        )
    bracket.advance(result, match_id, str(winner))
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _emit({"match_id": match_id, "winner": winner}, args)
    if not args.json:
        print(f"{match_id}: {winner} advances")
        remaining = bracket.pending_matches(result)
        print(f"ready to judge next: {', '.join(remaining) if remaining else 'none'}")
    return OK


def _adjudicated_winner(event_dir: Path, match_id: str, root: Path) -> str | None:
    """The team an approved adjudication named for this match.

    Read from a structured `advances_team` field, never from prose. Scanning the
    free-text impact line for the first `team-` token advanced the loser whenever
    an official wrote "team-harbor does not advance; team-quill advances".
    """
    directory = event_dir / "adjudications"
    if not directory.is_dir():
        return None
    for path in sorted(directory.glob("*.md")):
        metadata, _ = frontmatter.read(path)
        if metadata.get("match_id") != match_id:
            continue
        if metadata.get("scope") != "matchup":
            continue
        if metadata.get("resolution") != "resolved":
            continue
        if metadata.get("approval_state") != "approved" or not metadata.get("decided_by"):
            continue
        advances = metadata.get("advances_team")
        if not advances:
            raise AtjError(
                f"{path.name} resolves {match_id} but records no `advances_team`. The "
                f"advancing team is read from that field, never from prose."
            )
        return str(advances)
    return None


def cmd_bracket_verify(args) -> int:
    root = _root(args)
    # Advisory 2 of the release audit: the bare form checks structure only, said
    # so in its label, and exited 0. An operator reading the label was not
    # misled; one reading the exit code could be, and an exit code is what a
    # script reads. The weaker check now has to be asked for by name.
    if not args.reproduce and not args.event_dir and not args.structure_only:
        print(
            "usage: this would check the bracket's structure only, trusting the "
            "constraint audit block inside the file rather than re-deriving it.\n"
            "  --event-dir events/<id>        re-derive the constraints from the roster\n"
            "  --reproduce <roster.json>      redraw from the recorded seed and compare\n"
            "  --structure-only               you meant the weaker check; exit 0 on pass",
            file=sys.stderr,
        )
        return USAGE
    result = json.loads(Path(args.bracket).read_text(encoding="utf-8"))
    teams = None
    if args.reproduce:
        teams = json.loads(Path(args.reproduce).read_text(encoding="utf-8"))["teams"]
    elif args.event_dir:
        teams = event_module.load(Path(args.event_dir), root=root).eligible_teams
    problems = bracket.verify(result, teams) + schema.validate("bracket", result, root=root)
    if args.event_dir:
        problems += bracket.check_matchup_records(
            result, _matchup_records(Path(args.event_dir))
        )
    elif not args.reproduce:
        print("  NOTE structure only, as requested: the constraint audit block inside "
              "this file is trusted, not re-derived. A tampered bracket that keeps its "
              "own audit block consistent passes this check.")
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
    if problems:
        label = "FAIL"
    elif rebuilt:
        label = "PASS (reproduced from seed)"
    elif args.event_dir:
        label = "PASS (constraints re-derived from the roster)"
    else:
        label = "PASS (structure only; constraints not re-derived)"
    print(f"Bracket verification: {label}")
    return FAILURE if problems else OK


# --------------------------------------------------------------------------- #
# report validation
# --------------------------------------------------------------------------- #

def _matchup_records(event_dir: Path):
    for path in sorted((event_dir / "matchups").glob("*.md")):
        metadata, _ = frontmatter.read(path)
        if not metadata.get("match_id"):
            continue
        yield (
            str(metadata["match_id"]), str(metadata.get("team_a")),
            str(metadata.get("team_b")), metadata.get("winner"),
        )


def cmd_validate_reports(args) -> int:
    root = _root(args)
    event_dir = Path(args.event_dir)
    try:
        loaded = event_module.load(event_dir, root=root)
        public_scores = bool(loaded.config.get("public_scores"))
        team_ids = [team["id"] for team in loaded.teams]
    except AtjError:
        public_scores, team_ids = False, []
    expected_judges = None
    try:
        expected_judges = [
            str(judge) for judge in
            event_module.load(event_dir, root=root).config.get("expected_judges") or []
        ] or None
    except AtjError:
        pass
    found = reports.validate_event_reports(
        event_dir, root=root, public_scores=public_scores, all_teams=team_ids,
        expected_judges=expected_judges,
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


def _event_root_of(path: Path) -> Path | None:
    """The event directory *path* sits in, found by walking up."""
    for candidate in [path, *path.parents]:
        if (candidate / "event.md").is_file() and (candidate / "status.md").is_file():
            return candidate
    return None


def _publication_targets(path: Path, event_dir: Path) -> list[Path]:
    """Every artifact under *path* the disclosure gate applies to.

    A single file is itself. A directory is every Markdown and rendered artifact
    in a *subdirectory* beneath it.

    Subdirectories the gate has no rules for are included on purpose. They are
    where `publication.check_artifact` returns a blocking `location-unknown`,
    and that failing-closed is the property the tournament audit relied on to
    call live-trial-2026's undeclared `matchup-passes/` survivable (D22). A
    directory scan that quietly skipped an unrecognised directory would remove
    the one control standing over it.

    The event's own top-level files — `event.md`, `teams.md`, `status.md`,
    `bracket.md` — are excluded. They are the event's configuration and state,
    not artifacts that leave the panel, and they have no visibility routing.
    """
    if path.is_file():
        return [path]
    targets: list[Path] = []
    for child in sorted(path.iterdir()):
        if child.is_dir():
            targets.extend(sorted(child.rglob("*.md")))
            targets.extend(sorted(child.rglob("*.html")))
    if path != event_dir:
        # The request names a subdirectory; its own files are in scope too.
        targets.extend(sorted(path.glob("*.md")))
        targets.extend(sorted(path.glob("*.html")))
    return sorted(set(targets))


def cmd_check_publication(args) -> int:
    """Gate artifacts before they are shown to anyone outside the panel.

    Takes a file or a directory. D24: this accepted only a single artifact and
    raised `Is a directory` on anything else, so the event-wide disclosure check
    CLAUDE.md mandates before anything leaves the panel could not actually be
    run — every artifact had to be named individually, which is how a check gets
    skipped.
    """
    root = _root(args)
    path = Path(args.artifact)
    if args.event_dir:
        event_dir = Path(args.event_dir)
    else:
        event_dir = _event_root_of(path if path.is_dir() else path.parent) or path.parent.parent
    try:
        loaded = event_module.load(event_dir, root=root)
        public_scores = bool(loaded.config.get("public_scores"))
        team_ids = [team["id"] for team in loaded.teams]
    except AtjError:
        public_scores, team_ids = False, []

    targets = _publication_targets(path, event_dir)
    if not targets:
        raise AtjError(
            f"no artifacts to gate under {path}. A directory is scanned for the "
            f"artifact kinds the gate has rules for; {path} holds none."
        )

    totals = publication.official_totals(event_dir)
    display_names = {
        str(team.get("id")): str(team.get("display_name") or team.get("id"))
        for team in loaded.teams
    } if team_ids else {}

    findings: list[publication.Finding] = []
    per_artifact: list[dict] = []
    for target in targets:
        if target.suffix == ".html":
            found = reports.rendered_publication_findings(
                target, event_dir, public_scores=public_scores,
                all_teams=team_ids, display_names=display_names, totals=totals,
            )
        else:
            try:
                metadata, body = frontmatter.read(target)
            except AtjError as exc:
                found = [publication.Finding(
                    "blocking", "front-matter", exc.message, str(target)
                )]
            else:
                found = publication.check_artifact(
                    target, event_dir, metadata, body,
                    public_scores=public_scores, all_teams=team_ids,
                    display_names=display_names, totals=totals,
                )
        findings.extend(found)
        per_artifact.append({
            "artifact": str(target),
            "blocking": len([f for f in found if f.severity == "blocking"]),
            "findings": [vars(f) for f in found],
        })

    blocking = [f for f in findings if f.severity == "blocking"]
    _emit({"artifacts": per_artifact, "findings": [vars(f) for f in findings]}, args)
    if not args.json:
        _print_findings(findings)
        print(f"Publication check: {'BLOCKED' if blocking else 'CLEAR'} "
              f"({len(targets)} artifact(s), {len(blocking)} blocking, "
              f"{len(findings) - len(blocking)} other)")
    return FAILURE if blocking else OK


# --------------------------------------------------------------------------- #
# ceremony
# --------------------------------------------------------------------------- #

def cmd_ceremony(args) -> int:
    """Render the static ceremony view and printable dossiers.

    Reads approved public artifacts and the bracket's structural facts. It never
    opens the private record, and it refuses rather than skipping an artifact
    that does not pass the publication gate.
    """
    from . import ceremony

    root = _root(args)
    event_dir = Path(args.event_dir)
    output = Path(args.output) if args.output else event_dir / "public" / "ceremony"
    output.mkdir(parents=True, exist_ok=True)

    try:
        public_scores = bool(
            event_module.load(event_dir, root=root).config.get("public_scores")
        )
    except AtjError:
        public_scores = False
    page = output / "index.html"
    page.write_text(
        ceremony.render_ceremony(event_dir, public_scores=public_scores), encoding="utf-8"
    )
    written = [page]

    if not args.no_dossiers:
        # Dossiers are team-facing, so they render into the team-facing directory.
        # Writing them under public/ put a team's own score into the public tree,
        # where the publication gate then had to allow it.
        for dossier in sorted((event_dir / "dossiers").glob("*.md")):
            target = event_dir / "dossiers" / f"{dossier.stem}.html"
            target.write_text(ceremony.render_dossier(dossier), encoding="utf-8")
            written.append(target)

    _emit({"written": [str(path) for path in written]}, args)
    if not args.json:
        for path in written:
            print(f"  wrote {path}")
        print(f"Ceremony output: {len(written)} file(s)")
    return OK


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

    if versions.components_available(root):
        problems = versions.check_personas(root)
        failures += [f"persona: {p}" for p in problems]
        print(f"personas          {'PASS' if not problems else 'FAIL'}")
    else:
        problems = []
        print("personas          SKIPPED (no .claude/ components; not a working copy)")

    problems = check_templates(root)
    failures += [f"template: {p}" for p in problems]
    print(f"templates         {'PASS' if not problems else 'FAIL'}")

    if versions.components_available(root):
        problems = check_claude_components(root)
        failures += [f"claude: {p}" for p in problems]
        print(f"claude components {'PASS' if not problems else 'FAIL'}")
    else:
        print("claude components SKIPPED (no .claude/ components; not a working copy)")

    problems = check_no_duplicate_weights(root)
    failures += [f"duplicate-number: {p}" for p in problems]
    print(f"single-source     {'PASS' if not problems else 'FAIL'}")

    problems = check_template_schemas(root)
    failures += [f"template-schema: {p}" for p in problems]
    print(f"template schemas  {'PASS' if not problems else 'FAIL'}")

    problems = check_declared_versions(root)
    failures += [f"version-skew: {p}" for p in problems]
    print(f"version-skew      {'PASS' if not problems else 'FAIL'}")

    problems = check_packaging(root)
    failures += [f"packaging: {p}" for p in problems]
    if (root / "pyproject.toml").is_file():
        print(f"packaging         {'PASS' if not problems else 'FAIL'}")
    else:
        print(f"packaging         {'PASS' if not problems else 'FAIL'} "
              f"(version only; an installed wheel carries no build wiring)")

    problems = check_version_archive(root)
    failures += [f"archive: {p}" for p in problems]
    print(f"version archive   {'PASS' if not problems else 'FAIL'} "
          f"({len(canon.superseded_references(root))} superseded)")

    if versions.components_available(root):
        problems = check_write_contracts(root)
        failures += [f"write-contract: {p}" for p in problems]
        print(f"write contracts   {'PASS' if not problems else 'FAIL'}")
    else:
        print("write contracts   SKIPPED (no .claude/ components; not a working copy)")

    if (root / "events").is_dir():
        problems, historical = _unsigned_approvals(root)
        failures += [f"approval: {p}" for p in problems]
        note = (
            f" ({len(historical)} in completed events, frozen)" if historical else ""
        )
        print(f"signed approvals  {'PASS' if not problems else 'FAIL'}{note}")
    else:
        print("signed approvals  SKIPPED (not a working copy)")

    if (root / "events" / "sample-mock-2026").is_dir():
        problems = check_sample_event(root)
        failures += [f"sample-event: {p}" for p in problems]
        print(f"sample event      {'PASS' if not problems else 'FAIL'}")
    else:
        print("sample event      SKIPPED (not a working copy)")

    _emit({"failures": failures}, args)
    if failures:
        print("\nRelease check: FAIL")
        for failure in failures:
            print(f"  {failure}")
        return FAILURE
    print("\nRelease check: PASS")
    return OK


def check_packaging(root: Path) -> list[str]:
    """`VERSION`, `pyproject.toml` and the build backend must agree.

    D31: `pip install dist/*.whl` into a clean environment produced
    `atj unknown` and a `release-check` that could not find its own rubric,
    because the wheel shipped no `atj/data/`. `tools/stage_package_data.py`
    existed to stage it and its docstring said to run it in the build step; there
    was no build step that did, only a line in the release checklist telling a
    person to remember. The build backend is now that step, and this asserts the
    wiring so a later edit cannot quietly unhook it.
    """
    problems: list[str] = []
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if VERSION != version:
        problems.append(f"atj.VERSION is {VERSION!r} and VERSION reads {version!r}")
    if not (root / "pyproject.toml").is_file():
        # An installed wheel is the *result* of this check, not a subject of it:
        # it ships the framework data and none of the build wiring. Reading
        # pyproject.toml here made `atj release-check` fail inside the very
        # environment the check exists to protect.
        return problems
    pyproject = (root / "pyproject.toml").read_text(encoding="utf-8")

    # PEP 440 form of the same version: 0.3.0-beta -> 0.3.0b0.
    expected = version
    for suffix, replacement in (("-beta", "b0"), ("-alpha", "a0"), ("-rc", "rc0")):
        if version.endswith(suffix):
            expected = version[: -len(suffix)] + replacement
            break
    if f'version = "{expected}"' not in pyproject:
        problems.append(
            f"pyproject.toml does not declare version {expected!r}, the PEP 440 form of "
            f"VERSION ({version!r})"
        )
    if 'build-backend = "build_backend"' not in pyproject:
        problems.append(
            "pyproject.toml does not use the in-tree build backend, so a wheel can be "
            "built without staging atj/data/ and will install a command that cannot start"
        )
    if not (root / "build_backend.py").is_file():
        problems.append("build_backend.py is missing, and pyproject.toml names it")
    manifest = root / "MANIFEST.in"
    if not manifest.is_file():
        problems.append("MANIFEST.in is missing; an sdist could not build its own wheel")
    else:
        listed = manifest.read_text(encoding="utf-8")
        for needed in ("build_backend.py", "tools/stage_package_data.py", "framework"):
            if needed not in listed:
                problems.append(f"MANIFEST.in does not ship {needed}, which the wheel build needs")
    return problems


def check_version_archive(root: Path) -> list[str]:
    """The archive of superseded contract versions must stay honest.

    An archive file is the sole source for one retired version. It may not
    restate the current version -- that would be the second editable copy the
    single-source rule forbids -- and it must parse as the contract it claims to
    be, because a completed event's totals are recomputed from it.
    """
    problems: list[str] = []
    try:
        archived = canon.superseded_references(root)
    except AtjError as exc:
        return [exc.message]
    current = {
        canon.load(root).reference,
        canon.load_head_to_head(root).reference,
        canon.load_bracket_policy(root).reference,
        canon.load_consolidation_policy(root).reference,
    }
    submission_id = canon.load(root).rubric_id
    for reference, path in sorted(archived.items()):
        if reference in current:
            problems.append(
                f"{path.relative_to(root)}: archives {reference!r}, which is the current "
                f"version; an archive holds retired versions only"
            )
            continue
        if reference.startswith(f"{submission_id}@"):
            try:
                canon.load_reference(reference, root)
            except AtjError as exc:
                problems.append(f"{path.relative_to(root)}: {exc.message}")
    for (agent_id, version), retired in sorted(versions.load_superseded(root).items()):
        personas = versions.load_personas(root)
        if agent_id not in personas:
            problems.append(
                f"personas.md: superseded row {retired.reference} names a component that "
                f"is no longer registered"
            )
        elif personas[agent_id].version == version:
            problems.append(
                f"personas.md: {retired.reference} is listed as superseded and is also the "
                f"current version"
            )
    return problems


def check_write_contracts(root: Path) -> list[str]:
    """A component must hold the tool the artifact it owes requires.

    live-trial-2026 ran four judges whose skill requires each to produce a
    judgment document and whose definitions granted `Read, Grep, Glob`. Nothing
    compared the two, so the contract violation surfaced as four agents returning
    prose the orchestrator had to write out for them. The registry's `writes`
    column is the declaration; this is the check.
    """
    problems: list[str] = []
    for agent_id, persona in sorted(versions.load_personas(root).items()):
        path = versions.component_path(agent_id, root)
        if path is None:
            continue  # reported by check_personas
        try:
            metadata, _ = frontmatter.read(path)
        except AtjError as exc:
            problems.append(f"{agent_id}: {exc.message}")
            continue
        declared = metadata.get("tools")
        if declared is None:
            # Skills run in the orchestrator's own session and declare no tool
            # surface; there is nothing to compare a contract against.
            if persona.must_write and path.name != "SKILL.md":
                problems.append(
                    f"{agent_id}: owes an artifact in {persona.writes} but declares no tools"
                )
            continue
        tools = {tool.strip() for tool in str(declared).split(",")}
        if persona.must_write and "Write" not in tools:
            problems.append(
                f"{agent_id}: framework/personas.md says it writes {persona.writes} but "
                f"{path.relative_to(root)} declares tools {sorted(tools)} with no Write"
            )
        if not persona.must_write and "Write" in tools:
            problems.append(
                f"{agent_id}: holds the Write tool while the registry declares it writes "
                f"nothing; either give it a path in personas.md or take the tool away"
            )
    return problems


def check_template_schemas(root: Path) -> list[str]:
    """Every template must show every field its own schema requires.

    A template is the instruction an author follows. When it omits a field the
    schema demands, the author writes a conforming-looking artifact that fails
    validation only after the work is done. That is not hypothetical: the
    judgment template omitted the ``model`` block for the whole of
    live-trial-2026 and four finished judgments failed blocking on it.

    This compares keys, never values, because a template's values are
    placeholders by design.
    """
    problems: list[str] = []
    directory = root / reports.TEMPLATE_DIR
    for kind, (schema_name, template_name) in sorted(reports.ARTIFACT_KINDS.items()):
        if not schema_name or not template_name:
            continue
        path = directory / template_name
        if not path.is_file():
            problems.append(f"{template_name}: declared by kind {kind!r} but missing")
            continue
        try:
            metadata, _ = frontmatter.read(path)
        except AtjError as exc:
            problems.append(f"{template_name}: {exc.message}")
            continue
        document = schema.get_schema(schema_name, root)
        for field in document.get("required", []):
            if field not in metadata:
                problems.append(
                    f"{template_name}: missing {field!r}, which "
                    f"{schema_name}.schema.json requires"
                )
    return problems


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
    targets = [path for path in targets if "data" not in path.parts]
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
        # An artifact may pin a retired version; a template may not. A template is
        # the instruction for work that has not happened yet, so a superseded pin
        # there starts every new artifact out of date.
        for retired in versions.superseded_pins(payload, root=root):
            problems.append(
                f"{path.relative_to(root)}: pins a superseded contract ({retired}); a "
                f"template must instruct the current version"
            )
    return problems


def check_approvals_are_signed(root: Path) -> list[str]:
    """No committed artifact may be `approved` with nobody's name on it.

    The last of D25. `atj event approve` writes `approved_by` and `approved_at`,
    and the sample generator used to write `approval_state: approved` directly --
    so 47 committed artifacts asserted an approval no person was recorded as
    making, in the one fixture whose job is to demonstrate the gate chain.
    """
    problems, historical = _unsigned_approvals(root)
    return problems


def _unsigned_approvals(root: Path) -> tuple[list[str], list[str]]:
    """Unsigned approvals, split into the ones that can still be fixed and the rest.

    A completed event's artifacts are frozen. Five of live-trial-2026's were
    approved by hand before `atj event approve` existed, so they record the state
    without the name, and the only repair inside a completed event is to rewrite
    a frozen record -- which is D28's trap, and the third time this framework has
    walked into it. Those are reported as history; anything in an event still
    running has to be fixed.
    """
    from . import demo as demo_module

    problems: list[str] = []
    historical: list[str] = []
    for event_dir in sorted((root / "events").glob("*")):
        if not event_dir.is_dir() or event_dir.name == "_template":
            continue
        stage = ""
        status = event_dir / "status.md"
        if status.is_file():
            try:
                metadata, _ = frontmatter.read(status)
                stage = str(metadata.get("current_stage") or "")
            except AtjError:
                stage = ""
        for path in sorted(event_dir.rglob("*.md")):
            try:
                metadata, _ = frontmatter.read(path)
            except AtjError:
                continue  # reported by report validation
            if metadata.get("approval_state") != "approved":
                continue
            if metadata.get("approved_by"):
                continue
            detail = (
                f"{path.relative_to(root)}: approval_state is 'approved' and "
                f"approved_by is empty; an approval is a human act and has a name"
            )
            # The sample event is generated, not frozen: `atj demo build` rewrites
            # it wholesale, so an unsigned approval there is a live defect in the
            # generator whatever stage the fixture claims to be at.
            frozen = stage == "complete" and event_dir.name != demo_module.EVENT_ID
            (historical if frozen else problems).append(detail)
    return problems, historical


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


def tracked_files(root: Path) -> list[Path] | None:
    """Every file git tracks under *root*, or ``None`` if this is not a checkout.

    A whole-tree scan must ask git what belongs to this repository, not the
    filesystem what happens to sit inside it. D17: an agent worktree created
    under the repository is a second full checkout, so a filesystem walk found a
    second copy of every file — including `tests/test_canonical_model.py`, which
    holds the official weights on purpose — and `release-check` failed on a
    duplicate that was the same file seen twice. Gitignoring the worktree does
    not help, because a worktree's own files are tracked in *its* index.

    Returns ``None`` rather than an empty list when git is unavailable or this is
    an export, so the caller can fall back to walking the tree. An sdist and a CI
    export have no `.git`, and the scan must still run there.
    """
    import subprocess

    if not (root / ".git").exists():
        return None
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others",
             "--exclude-standard"],
            capture_output=True, timeout=30, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if completed.returncode != 0:
        return None
    names = completed.stdout.decode("utf-8", errors="replace").split("\0")
    return sorted(root / name for name in names if name)


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
    # `atj/data/` is a build-time copy staged by tools/stage_package_data.py. It is
    # generated, git-ignored, and not an editable source.
    skip_parts = {".git", "__pycache__", "node_modules", "dist", ".pytest_cache", "data"}
    # Narrow exemptions only. `tests/` asserts against the real weights on
    # purpose, and the baseline audit quotes the alpha's duplicate as evidence.
    # Everything else, including the rest of `docs/`, is scanned.
    allowed = {
        rubric_path,
        (root / "tests").resolve(),
        (root / "docs" / "release-readiness-audit.md").resolve(),
        # The archive holds retired rubric versions. Each is the sole source for
        # its own version and is never edited, so it is not a second copy of the
        # current weights even when the numbers happen to match.
        canon.archive_dir(root).resolve(),
    }
    problems: list[str] = []
    candidates = tracked_files(root)
    if candidates is None:
        candidates = sorted(root.rglob("*"))
    for path in candidates:
        if not path.is_file() or path.suffix not in (".py", ".json", ".md", ".yaml", ".yml"):
            continue
        if skip_parts & set(path.parts):
            continue
        resolved = path.resolve()
        # An `atj matchup` result keys its criterion margins by criterion id, and a
        # decisive value makes the margin equal the weight. The file is tool output,
        # reproduced by the tournament audit, so it is exempt by what it is and not
        # by how its numbers are written: a float copy elsewhere is still a copy.
        rel = path.relative_to(root).parts
        if len(rel) == 4 and rel[0] == "events" and rel[2] == "matchups" and path.suffix == ".json":
            continue
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
        "privilege_warning": capability.privilege_warning,
        "evidence_limitation": sandbox.evidence_limitation(capability),
    }
    _emit(payload, args)
    if args.json:
        return OK if capability.available else FAILURE
    print(f"Sandbox preflight: {'AVAILABLE' if capability.available else 'UNAVAILABLE'}")
    print(f"  {capability.summary()}")
    if capability.privilege_warning:
        print(f"  WARNING: {capability.privilege_warning}")
    if not capability.available:
        limitation = sandbox.evidence_limitation(capability)
        print(f"  record execution_status: {limitation['execution_status']}")
        print(f"  criteria needing NE unless other direct evidence exists: "
              f"{', '.join(limitation['evidence_limited_criteria'])}")
        print("  There is no host fallback. Static inspection may continue.")
    return OK if capability.available else FAILURE


def cmd_sandbox_proxy(args) -> int:
    """Bring up, tear down or report the egress proxy an allowlist needs.

    Advisory 5 of the release audit: a network allowlist needs an egress proxy
    the repository did not provide, so `atj sandbox run` refused every event that
    configured one and the path was never exercised. `atj/egress.py` provides it;
    this is the operator surface.
    """
    root = _root(args)
    allowlist: list[str] = list(args.allow or [])
    if args.event_dir:
        config = event_module.load(Path(args.event_dir), root=root).config
        allowlist += [str(entry) for entry in config.get("network_allowlist") or []]

    if args.action == "status":
        current = egress.state(args.runtime)
        _emit(current.to_dict(), args)
        if not args.json:
            if not current.running:
                print("Egress proxy: not running")
                print("  Start one with `atj sandbox proxy up --event-dir <event>`.")
            else:
                print(f"Egress proxy: RUNNING at {current.url}")
                print(f"  allowlist: {', '.join(current.allowlist) or '(none)'}")
                print("  Everything not on that list is refused by the proxy, and the "
                      "submission network has no other way out.")
        return OK if current.running else FAILURE

    if args.action == "down":
        removed = egress.stop(args.runtime)
        _emit({"removed": removed}, args)
        if not args.json:
            print("Egress proxy removed" if removed else "No egress proxy was running")
        return OK

    if not allowlist:
        print("usage: `up` needs an allowlist: pass --event-dir <event> whose "
              "network_allowlist names the hosts, or --allow <host> per host",
              file=sys.stderr)
        return USAGE
    current = egress.start(allowlist, args.runtime)
    _emit(current.to_dict(), args)
    if not args.json:
        print(f"Egress proxy: RUNNING at {current.url}")
        print(f"  allowlist: {', '.join(current.allowlist)}")
        print(f"  submissions join {egress.SANDBOX_NETWORK}, which has no route off the "
              f"host; the proxy is the only way out and it refuses everything else.")
        print("  Run with `atj sandbox run ... --event-dir <event> --egress-proxy auto`.")
    return OK


def cmd_sandbox_run(args) -> int:
    root = _root(args)
    capability = sandbox.preflight(args.runtime)
    allowlist: list[str] = []
    if args.event_dir:
        config = event_module.load(Path(args.event_dir), root=root).config
        allowlist = [str(entry) for entry in config.get("network_allowlist") or []]
        if config.get("execution_mode") != "sandboxed":
            raise AtjError(
                f"{args.event_dir} declares execution_mode "
                f"{config.get('execution_mode')!r}. An event official must set it to "
                f"'sandboxed' before any submission is executed."
            )
    proxy = args.egress_proxy
    if proxy == "auto" and not allowlist:
        print(
            "usage: --egress-proxy auto takes the allowlist from the event, so it needs "
            "--event-dir <event> whose network_allowlist names the hosts. The allowlist "
            "is an official's decision recorded in event.md; a command-line flag that "
            "could widen it would not be that decision.",
            file=sys.stderr,
        )
        return USAGE
    if proxy == "auto":
        # `auto` means "the proxy this event's allowlist authorizes". Resolving it
        # here rather than trusting a URL on the command line is the point: a
        # proxy enforcing another event's allowlist is refused by name.
        proxy = egress.require_for(allowlist, args.runtime)
    record = sandbox.run_in_sandbox(
        source=Path(args.source), command=args.command, image=args.image,
        limits={"timeout_seconds": args.timeout} if args.timeout else None,
        network_allowlist=allowlist, egress_proxy=proxy,
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
# intake
# --------------------------------------------------------------------------- #

def cmd_intake(args) -> int:
    root = _root(args)
    loaded = event_module.load(Path(args.event_dir), root=root)
    result = intake.run(
        loaded, args.team_id, args.source,
        workspace=Path(args.workspace).resolve() if args.workspace else None,
        ref=args.ref,
        display_name=args.display_name,
        affiliation_group=args.affiliation_group,
        force=args.force,
    )
    payload = {
        "event_id": result.event_id, "team_id": result.team_id,
        "source": result.source, "source_kind": result.source_kind,
        "checkout": str(result.checkout), "commit": result.commit,
        "pin": result.pin, "record": str(result.record), "notes": result.notes,
    }
    _emit(payload, args)
    if not args.json:
        print(f"Ingested {result.team_id} into {result.event_id}")
        print(f"  source:   {result.source} ({result.source_kind})")
        print(f"  checkout: {result.checkout}")
        print(f"  commit:   {result.commit} ({result.pin})")
        print(f"  record:   {result.record}")
        for note in result.notes:
            print(f"  note:     {note}")
        print("  Nothing was executed. Complete the intake record's narrative "
              "sections, then run `atj event validate`.")
    return OK


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
    if bracket.draw_only(drawn) != bracket.draw_only(demo.sample_bracket(root)):
        problems.append("bracket: committed draw does not reproduce from its recorded seed")
    problems += [
        f"bracket: {p}" for p in
        bracket.check_matchup_records(drawn, _matchup_records(directory))
    ]

    fixture_dir = root / "tests" / "fixtures" / "bracket-20-team"
    fixture = json.loads((fixture_dir / "bracket.json").read_text(encoding="utf-8"))
    fixture_roster = json.loads((fixture_dir / "roster.json").read_text(encoding="utf-8"))["teams"]
    problems += [f"fixture: {p}" for p in bracket.verify(fixture, fixture_roster)]
    if bracket.draw_only(fixture) != bracket.draw_only(demo.twenty_team_bracket(root)):
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
    init.add_argument("--dir", help="directory to create events/ in (default: cwd)")
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
    advance.add_argument(
        "--force-approver", help="the official authorizing the override; required with it"
    )
    advance.set_defaults(func=cmd_event_advance)

    gate = event_sub.add_parser("gate", help="record a stage gate result")
    gate.add_argument("event_dir")
    gate.add_argument("gate")
    gate.add_argument("state", choices=("pending", "passed", "failed"))
    gate.add_argument(
        "--audit", help="the audit artifact justifying a pass; required to pass a gate"
    )
    gate.set_defaults(func=cmd_event_gate)

    approve = event_sub.add_parser(
        "approve", help="set approval_state on event artifacts, with validation behind it"
    )
    approve.add_argument("paths", nargs="+", help="artifact files, or directories of them")
    approve.add_argument(
        "--state", choices=APPROVAL_STATES, default="approved",
        help="the state to set (default: approved)",
    )
    approve.add_argument(
        "--official",
        help="the role approving, e.g. event-director. Defaults to the event's "
             "officials.publication_approval",
    )
    approve.add_argument("--note", help="recorded as approval_note")
    approve.add_argument("--event-dir", help="the event these artifacts belong to")
    approve.set_defaults(func=cmd_event_approve)

    overrides_parser = event_sub.add_parser(
        "overrides", help="list the stage gates a human bypassed, for review"
    )
    overrides_parser.add_argument("event_dir")
    overrides_parser.add_argument(
        "--review", type=int, metavar="INDEX",
        help="mark the override at this index as read by a human official",
    )
    overrides_parser.add_argument("--official", help="the role recording the review")
    overrides_parser.add_argument("--note", help="what the reviewer concluded")
    overrides_parser.set_defaults(func=cmd_event_overrides)

    unit = event_sub.add_parser("unit", help="record or invalidate a unit of work")
    unit.add_argument("event_dir")
    unit.add_argument("action", choices=("record", "stale", "list"))
    unit.add_argument("--id", help="unit id, e.g. judging:team-lumen")
    unit.add_argument("--stage", help="the stage this unit belongs to")
    unit.add_argument("--output", action="append", default=[], help="artifact path")
    unit.add_argument(
        "--audit-result", default="not-audited",
        choices=("PASS", "PASS WITH ADVISORIES", "FAIL", "not-audited"),
    )
    unit.add_argument("--reason", help="why the unit is being invalidated")
    unit.add_argument(
        "--completed-at",
        help="when the work finished, as YYYY-MM-DDTHH:MM:SSZ, or 'now' to restamp. "
             "Omit it and a re-record over unchanged inputs keeps the original time",
    )
    unit.set_defaults(func=cmd_event_unit)

    score = sub.add_parser("score", help="consolidate a judge panel")
    score.add_argument("source", help="judgments directory, or a JSON file of judge scores")
    score.add_argument(
        "--expect",
        help="comma-separated configured judge ids; read from event.md automatically "
             "when the judgments directory sits inside an event",
    )
    score.add_argument(
        "--adjudications",
        help="directory of adjudication records to apply; defaults to the event's",
    )
    score.add_argument("--output", help="write the structured result to this path")
    score.set_defaults(func=cmd_score)

    render_parser = sub.add_parser(
        "render", help="generate official numbers into a reviewed artifact"
    )
    render_sub = render_parser.add_subparsers(
        dest="render_command", required=True,
        parser_class=lambda **kw: argparse.ArgumentParser(parents=[shared], **kw),
    )
    render_judgment = render_sub.add_parser(
        "judgment", help="generate the scores table into an individual judgment"
    )
    render_judgment.add_argument(
        "paths", nargs="+", help="judgment files, or directories of them"
    )
    render_judgment.add_argument(
        "--force", action="store_true",
        help="re-render a judgment already marked approved; record why in the ledger",
    )
    render_judgment.set_defaults(func=cmd_render_judgment)

    render_consolidated = render_sub.add_parser(
        "consolidated", help="generate the panel score block into a consolidated report"
    )
    render_consolidated.add_argument(
        "paths", nargs="+", help="consolidated report files, or directories of them"
    )
    render_consolidated.add_argument(
        "--force", action="store_true",
        help="re-render a report already marked approved; record why in the ledger",
    )
    render_consolidated.set_defaults(func=cmd_render_consolidated)

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

    advance = bracket_sub.add_parser(
        "advance", help="record a match winner and carry it into the next round"
    )
    advance.add_argument("bracket")
    advance.add_argument("--match", required=True, help="match id")
    advance.add_argument(
        "--from", dest="matchup", required=True, help="the private matchup report"
    )
    advance.add_argument("--event-dir", help="event directory, for adjudication records")
    advance.set_defaults(func=cmd_bracket_advance)

    verify = bracket_sub.add_parser("verify", help="re-check a built bracket")
    verify.add_argument("bracket")
    verify.add_argument("--reproduce", help="team JSON to redraw and compare against")
    verify.add_argument(
        "--event-dir",
        help="re-derive the constraints from this event's roster instead of trusting "
             "the audit block inside the bracket file",
    )
    verify.add_argument(
        "--structure-only", action="store_true",
        help="check shape alone and trust the file's own constraint audit. Required "
             "to make that the check, so a bare invocation cannot be mistaken for a "
             "full verification by anything reading only the exit code",
    )
    verify.set_defaults(func=cmd_bracket_verify)

    validate_parser = sub.add_parser("validate", help="artifact validation")
    validate_sub = validate_parser.add_subparsers(dest="validate_command", required=True)

    report_validate = validate_sub.add_parser("reports", help="validate every report in an event")
    report_validate.add_argument("event_dir")
    report_validate.set_defaults(func=cmd_validate_reports)

    publish = validate_sub.add_parser(
        "publication", help="gate an artifact, or a whole event, before disclosure"
    )
    publish.add_argument("artifact", help="an artifact file, or a directory to scan")
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
    run.add_argument(
        "--event-dir",
        help="read execution_mode and network_allowlist from this event's configuration",
    )
    run.add_argument(
        "--egress-proxy",
        help="authorized proxy enforcing the allowlist; 'auto' uses the one "
             "`atj sandbox proxy up` started, and refuses if it enforces a different "
             "allowlist than this event's. Without a proxy, a configured allowlist is "
             "refused rather than silently granting full network access",
    )
    run.add_argument("--output", help="write the execution record here")
    run.set_defaults(func=cmd_sandbox_run)

    proxy_parser = sandbox_sub.add_parser(
        "proxy", help="the egress proxy that makes a network allowlist enforceable"
    )
    proxy_parser.add_argument("action", choices=("up", "down", "status"))
    proxy_parser.add_argument(
        "--event-dir", help="read network_allowlist from this event's configuration"
    )
    proxy_parser.add_argument(
        "--allow", action="append", default=[],
        help="a hostname to allow, repeatable; `*.example.org` matches subdomains",
    )
    proxy_parser.add_argument("--runtime", choices=(sandbox.PODMAN, sandbox.DOCKER))
    proxy_parser.set_defaults(func=cmd_sandbox_proxy)

    ceremony_parser = sub.add_parser(
        "ceremony", help="render the static ceremony view from approved public artifacts"
    )
    ceremony_parser.add_argument("event_dir")
    ceremony_parser.add_argument("--output", help="output directory")
    ceremony_parser.add_argument(
        "--no-dossiers", action="store_true", help="skip the printable team dossiers"
    )
    ceremony_parser.set_defaults(func=cmd_ceremony)

    intake_parser = sub.add_parser(
        "intake", help="materialize, pin and enroll one submission"
    )
    intake_parser.add_argument("event_dir")
    intake_parser.add_argument("team_id")
    intake_parser.add_argument(
        "source", help="git URL, local git repository, directory, or .zip archive"
    )
    intake_parser.add_argument(
        "--ref", help="commit, tag or branch to pin; git sources only (default: HEAD)"
    )
    intake_parser.add_argument("--display-name", help="roster display name for a new team")
    intake_parser.add_argument("--affiliation-group", help="school or group, for bracket separation")
    intake_parser.add_argument(
        "--workspace", help="where checkouts live (default: <root>/workspaces)"
    )
    intake_parser.add_argument(
        "--force", action="store_true",
        help="replace an existing checkout, or ingest past a frozen roster",
    )
    intake_parser.set_defaults(func=cmd_intake)

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
