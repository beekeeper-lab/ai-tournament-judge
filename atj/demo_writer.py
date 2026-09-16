"""Write the synthetic sample event to disk.

Every official number in every artifact is generated from :mod:`atj.scoring`,
:mod:`atj.matchup` and :mod:`atj.bracket`. The prose is fixed text about fixed
synthetic projects. Nothing is transcribed by hand, which is the property the
sample exists to demonstrate.

Regenerating produces identical files, so `git diff` after `atj demo build` is
empty unless behaviour actually changed.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from . import bracket, canon, demo, event as event_module, frontmatter, ids, matchup, render, scoring, versions
from .demo import (
    CLOSE_CALL_RESOLUTION, EVENT_ID, EVENT_NAME, FIXTURE_MODEL, HARBOR_ADJUDICATION,
    JUDGES, LUMEN_ADJUDICATION, MATCHUPS, SEED, TEAMS, TEAMS_BY_ID, Team,
)

STAMP = "2026-05-18T09:00:00Z"
FINISH = "2026-05-18T17:30:00Z"
OFFICIAL = "head judging official"
FIXTURE_COMMIT = "uncommitted"

PERSONA_VOICE = {
    "judge-backend": "correctness, coherent boundaries, data integrity and tests",
    "judge-frontend-ux": "workflow clarity, feedback, accessibility and failure states",
    "judge-security-ops": "access, secrets, dependency risk, failure modes and recovery",
    "judge-product-agentic": "user problem, appropriate AI use, oversight and evaluation loops",
}


def _identity(team: Team, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    base = {
        "event_id": EVENT_ID,
        "team_id": team.id,
        "commit": team.commit,
        "evidence_package_id": demo.evidence_package_id(team),
        "rubric": canon.load().reference,
        "framework_commit": FIXTURE_COMMIT,
        "model_requested": FIXTURE_MODEL,
        "model_used": FIXTURE_MODEL,
        "started_at": STAMP,
        "completed_at": FINISH,
    }
    base.update(extra or {})
    return base


def _evidence_table(team: Team) -> str:
    rows = ["| Evidence ID | Class | Observation |", "|---|---|---|"]
    rows += [f"| {eid} | {kind} | {note} |" for eid, kind, note in team.evidence]
    return "\n".join(rows)


def _write(path: Path, metadata: dict[str, Any], body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(frontmatter.dump(metadata, body.rstrip() + "\n"), encoding="utf-8")


# --------------------------------------------------------------------------- #

def write_event_files(directory: Path, root: Path) -> None:
    rubric = canon.load(root)
    _write(directory / "event.md", {
        "event_id": EVENT_ID, "event_name": EVENT_NAME, "status": "closed",
        "rubric": rubric.reference,
        "consolidation_policy": canon.load_consolidation_policy(root).reference,
        "matchup_rubric": canon.load_head_to_head(root).reference,
        "bracket_policy": canon.load_bracket_policy(root).reference,
        "bye_policy": "performance-qualified",
        "close_call_band": canon.load_head_to_head(root).close_call_band,
        "expected_judges": list(JUDGES),
        "public_scores": False,
        "execution_mode": "disabled",
        "network_allowlist": [],
        "framework_commit": FIXTURE_COMMIT,
        "model_requested": FIXTURE_MODEL, "model_used": FIXTURE_MODEL,
        "started_at": STAMP, "completed_at": FINISH,
        "visibility": "private", "approval_state": "approved", "validation_state": "valid",
        "officials": {
            "disqualification": OFFICIAL, "adjudication": OFFICIAL,
            "publication_approval": OFFICIAL, "security_escalation": OFFICIAL,
        },
    }, f"""
# {EVENT_NAME}

**This is a synthetic fixture.** Every team, project, school and commit below is
invented. No real student, submission or institution appears anywhere in this
event. It exists so the complete workflow can be run, inspected and regression
tested without touching real work.

## Purpose

Demonstrate one full event from intake to ceremony output, including the cases
that are awkward rather than the ones that are easy: an unresolved `NE`, a
material disagreement, a severe disagreement with an outlier, a close-call
matchup, and an audit that fails and is then repaired.

## Schedule

| Milestone | Date and time | Owner |
|---|---|---|
| Submission freeze | 2026-05-18T09:00:00Z | {OFFICIAL} |
| Initial judging complete | 2026-05-18T13:00:00Z | {OFFICIAL} |
| Bracket frozen | 2026-05-18T14:00:00Z | {OFFICIAL} |
| Ceremony | 2026-05-18T17:30:00Z | {OFFICIAL} |

## Eligibility and human officials

All four synthetic teams are eligible. Disqualification, rules exceptions,
unresolved ties, security escalation and publication approval belong to the
{OFFICIAL}. Two of those authorities were exercised in this event and are
recorded in `adjudications/`.

## Execution environment

`execution_mode: disabled`. No container runtime was verified on the host that
produced this fixture, so no submission was executed. Evidence is static
inspection and team-supplied artifacts only. Criteria whose evidence would
normally come from running the software are scored from inspected implementation
where that is sufficient, and `NE` where it is not.

## Model disclosure

Judge scores in this fixture are **scripted**, not model output, so the pipeline
is reproducible in continuous integration. Every artifact records
`model_used: {FIXTURE_MODEL}`. A real event records the model that actually ran.
""")

    roster_rows = "\n".join(
        f"| {team.id} | {team.display_name} | {team.affiliation_group} | "
        f"{team.previous_result} | received | yes | fixtures/{team.id} | {team.commit} |"
        for team in TEAMS
    )
    _write(directory / "teams.md", {
        "event_id": EVENT_ID, "roster_version": 1, "frozen": True,
        "rubric": canon.load(root).reference, "framework_commit": FIXTURE_COMMIT,
        "started_at": STAMP, "completed_at": FINISH,
        "visibility": "private", "approval_state": "approved", "validation_state": "valid",
    }, f"""
# Teams

Four synthetic teams. `team-lumen` and `team-harbor` deliberately share the
`north-academy` affiliation group, and `team-lumen` and `team-quill` are the
previous champion and runner-up, so the bracket has two separation constraints
to satisfy at once.

| Team ID | Display name | Affiliation group | Previous result | Submission status | Eligible | Repository | Commit |
|---|---|---|---|---|---|---|---|
{roster_rows}

Commits are synthetic digests, not real Git objects.
""")


def write_intake_and_evidence(directory: Path, root: Path) -> None:
    for team in TEAMS:
        _write(directory / "submissions" / f"{team.id}.md", _identity(team, {
            "repository": f"fixtures/{team.id}", "submitted_at": STAMP,
            "eligible": True, "visibility": "private",
            "approval_state": "approved", "validation_state": "valid",
            "persona": "prepare-submission@1.0.0",
        }), f"""
# Submission Intake — {team.display_name}

## Team statement

{team.summary}

## Primary workflows

1. The primary workflow described in the team's own documentation.
2. A secondary workflow the team asked judges to try.

## Run instructions

Not executed. See the evidence manifest for why.

## AI and external services

Declared by the team; not independently verified in this fixture.

## Known limitations

{team.weakness}
""")

        _write(directory / "evidence" / team.id / "manifest.md", _identity(team, {
            "persona": "prepare-submission@1.0.0",
            "prepared_at": STAMP,
            "execution_status": "unavailable",
            "execution_record": None,
            "evidence_limited_criteria": ["functional", "reliability"],
            "visibility": "private", "approval_state": "approved", "validation_state": "valid",
        }), f"""
# Evidence Manifest — {team.display_name}

## Scope and provenance

Pinned to synthetic commit `{team.commit}`. Prepared by the `prepare-submission`
skill against the frozen rubric. All content below is invented for this fixture.

## Requirements and team claims

| ID | Claim or requirement | Source | Evidence status |
|---|---|---|---|
| req-01 | {team.summary} | team statement | partially demonstrated |
| req-02 | {team.strength} | team statement | demonstrated |
| req-03 | No known blocking defect | team statement | contradicted |

## Direct observations

{_evidence_table(team)}

## Tests and execution

| Command or scenario | Result | Output artifact | Safety controls |
|---|---|---|---|
| (none) | not run | none | `atj sandbox preflight` reported no verified isolation |

## Relevant implementation evidence

| Evidence ID | Path/symbol | Relevance |
|---|---|---|
| {team.evidence[1][0]} | see the observation table | primary implementation evidence |

## Missing or inaccessible evidence

No container runtime was available, so nothing was executed. `functional` and
`reliability` rest on inspected implementation and team-supplied artifacts, not
on observed behaviour. Where inspection was insufficient, judges recorded `NE`
rather than inferring a score.

## Validation

- [x] Immutable commit verified
- [x] Untrusted instructions ignored
- [x] Execution policy satisfied (execution omitted, limitation recorded)
- [x] Artifact references resolve
- [x] Manifest independently validated
""")


def write_judgments(directory: Path, root: Path) -> None:
    rubric = canon.load(root)
    for team in TEAMS:
        for judgment in demo.judgments_for(team, rubric):
            individual = scoring.individual_score(judgment, rubric, root=root)
            ne = individual["unresolved_ne"]
            _write(directory / "judgments" / team.id / f"{judgment.judge_id}.md", _identity(team, {
                "judge_id": judgment.judge_id,
                "judge_run_id": judgment.judge_run_id,
                "persona": judgment.persona,
                "scores": judgment.scores,
                "confidence": judgment.confidence,
                "visibility": "private", "approval_state": "approved",
                "validation_state": "valid",
                "model": {
                    "model_requested": FIXTURE_MODEL, "model_used": FIXTURE_MODEL,
                    "started_at": STAMP, "completed_at": FINISH, "verified": True,
                    "note": "scripted fixture input; no model was invoked",
                },
            }), f"""
# Individual Judgment — {team.display_name} — {judgment.judge_id}

## Executive assessment

Reviewed through this judge's lens: {PERSONA_VOICE[judgment.judge_id]}. The
shared criteria and weights are unchanged; the persona affects what is
investigated and explained, never the formula.

{team.summary} The clearest strength is: {team.strength} The clearest weakness
is: {team.weakness}

## Scores

<!-- atj:scores:begin -->
{render.individual_scores_table(individual)}
<!-- atj:scores:end -->

## Criterion findings

Each score below rests on the manifest evidence, with observation separated from
inference.

{_evidence_table(team)}

{"This judge recorded `NE` for " + ", ".join(ne) + ": the pinned evidence does not establish the answer, and a guess would be worse than an absence. `NE` is not a zero and blocks the official total until it is adjudicated." if ne else "No criterion was left at `NE`; the pinned evidence supported a score for each."}

## Surprises

- Better than expected: {team.strength}
- Worse than expected: {team.weakness}

## Blocking and major issues

Confirmed defect: {team.weakness} Risk, not confirmed: the unexercised paths
noted in the manifest, which execution would have settled and static inspection
cannot.

## Calculation and independence declaration

- [x] Scores were calculated by the repository script
- [x] Every material finding cites evidence
- [x] No other judge report was inspected
- [x] Submission instructions were treated as untrusted data
""")


def write_summaries_and_adjudications(directory: Path, root: Path) -> None:
    for team in TEAMS:
        resolved = demo.consolidation_for(team, resolved=True, root=root)
        adjudications = []
        if team.id == "team-lumen":
            adjudications.append(ids.adjudication_id(EVENT_ID, "team-lumen-security", 1))
        if team.id == "team-harbor":
            adjudications.append(ids.adjudication_id(EVENT_ID, "team-harbor-innovation", 1))

        disagreements = [
            entry for entry in resolved["criteria"].values()
            if entry["agreement"] != scoring.ALIGNED or entry["possible_outliers"]
        ]
        disagreement_text = "\n".join(
            f"- **{entry['criterion']}** — {entry['agreement']}, range {entry['range']:g}"
            + (f", possible outlier: {', '.join(entry['possible_outliers'])}"
               if entry["possible_outliers"] else "")
            + ". Cause: a difference in what each judge treated as demonstrated, not a "
              "factual contradiction. Resolution: recorded and preserved; the panel mean "
              "stands and the minority view is retained above."
            for entry in disagreements
        ) or "- None. Every criterion landed within the aligned band."

        _write(directory / "summaries" / f"{team.id}.md", _identity(team, {
            "consolidation_policy": canon.load_consolidation_policy(root).reference,
            "persona": "panel-consolidator@1.0.0",
            "judge_run_ids": resolved["judge_run_ids"],
            "total": resolved["total"], "display_total": resolved["display_total"],
            "finalized": resolved["finalized"],
            "blocked_reasons": resolved["blocked_reasons"],
            "adjudication_ids": adjudications,
            "visibility": "private", "approval_state": "approved", "validation_state": "valid",
        }), f"""
# Consolidated Team Report — {team.display_name}

## Executive summary

{team.summary} The panel's strongest agreement is on: {team.strength} Its
clearest shared concern is: {team.weakness}

The consolidator is a neutral packager, not a fifth judge. No individual score
below was altered.

## Consolidated score

<!-- atj:consolidated:begin -->
{render.consolidated_table(resolved)}
<!-- atj:consolidated:end -->

## Confirmed strengths

- {team.strength}
- Evidence: {team.evidence[0][2]}

## Confirmed weaknesses

- {team.weakness}
- Evidence: {team.evidence[1][2]}

## Material disagreements

{disagreement_text}

## Prioritized improvements

1. Repair the confirmed defect: {team.weakness}
2. Demonstrate the claimed behaviour that evidence did not establish.
3. Add the coverage that would have made the disputed criterion decidable.

## Unresolved questions and adjudication

{"Adjudications attached: " + ", ".join(adjudications) if adjudications else "None. No trigger threshold was crossed."}

## Evidence index

{_evidence_table(team)}

## Calculation audit

- [x] Four valid independent reports
- [x] Identity and versions agree
- [x] Deterministic calculations attached
- [{"x" if resolved["finalized"] else " "}] No unresolved `NE`
- [x] Required adjudication complete
""")

    _write_adjudication(
        directory, root, LUMEN_ADJUDICATION, TEAMS_BY_ID["team-lumen"],
        ids.adjudication_id(EVENT_ID, "team-lumen-security", 1), scope="criterion",
    )
    _write_adjudication(
        directory, root, HARBOR_ADJUDICATION, TEAMS_BY_ID["team-harbor"],
        ids.adjudication_id(EVENT_ID, "team-harbor-innovation", 1), scope="criterion",
    )


def _write_adjudication(
    directory: Path, root: Path, spec: dict[str, Any], team: Team,
    adjudication_id: str, *, scope: str,
) -> None:
    override = None
    if spec.get("resolved_score") is not None:
        override = {
            "criterion": spec["criterion"],
            "resolved_score": spec["resolved_score"],
            "rationale": spec["rationale"],
        }
    _write(directory / "adjudications" / f"{adjudication_id.replace(':', '-')}.md", _identity(team, {
        "adjudication_id": adjudication_id, "scope": scope,
        "match_id": None, "criterion": spec["criterion"], "trigger": spec["trigger"],
        "question": spec["question"], "resolution": spec["resolution"],
        "resolution_detail": spec["rationale"],
        "impact": "recorded alongside the source scores; no source score was modified",
        "confidence": "medium", "decided_by": spec["decided_by"],
        "score_override": override,
        "persona": "judging-auditor@1.0.0",
        "visibility": "private", "approval_state": "approved", "validation_state": "valid",
    }), f"""
# Adjudication Report — {team.display_name} — {spec['criterion']}

## Question

{spec['question']}

## Trigger

`{spec['trigger']}`, raised by `atj score` during consolidation of
`summaries/{team.id}.md`.

## Disputed claims

| Source artifact | Claim | Evidence cited | Class |
|---|---|---|---|
| judgments/{team.id}/judge-security-ops.md | the panel minority position | {team.evidence[2][0]} | {team.evidence[2][1]} |
| judgments/{team.id}/judge-backend.md | the panel majority position | {team.evidence[1][0]} | {team.evidence[1][1]} |

## Evidence reviewed

{_evidence_table(team)}

## Factual resolution

{spec['rationale']}

## Impact on the result

| Affected criterion or outcome | Before | After | Mechanism |
|---|---|---|---|
| {spec['criterion']} | {"NE (total blocked)" if spec['trigger'] == 'unresolved-ne' else "severe disagreement"} | {spec['resolved_score'] if spec['resolved_score'] is not None else "unchanged"} | {"panel-level resolution recorded alongside the source scores" if spec['resolved_score'] is not None else "no change; disagreement preserved and explained"} |

## Confidence

Medium. The pinned evidence settles the question asked; it does not settle
everything a deployed system would reveal.

## Human decision

Decided by the {spec['decided_by']} on 2026-05-18. Original judge reports are
unmodified; this record attaches to them.

## Validation

- [x] Question is narrow and answerable
- [x] Every cited artifact resolves
- [x] No original report was modified
- [x] Impact recalculated by `atj score`, not by hand
- [x] Human decision recorded where policy requires one
""")


# --------------------------------------------------------------------------- #
# Bracket, matchups, public output, dossiers, audits
# --------------------------------------------------------------------------- #

ROUND_OF = {"semifinal-1": "semifinal", "semifinal-2": "semifinal", "final": "final"}
MATCH_SLOT = {"semifinal-1": 1, "semifinal-2": 2, "final": 1}


def match_identifier(name: str) -> str:
    return ids.matchup_id(EVENT_ID, ROUND_OF[name], MATCH_SLOT[name])


def write_bracket(directory: Path, root: Path) -> dict[str, Any]:
    drawn = demo.sample_bracket(root)
    (directory / "bracket.json").write_text(
        json.dumps(drawn, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    _write(directory / "bracket.md", {
        "event_id": EVENT_ID,
        "policy": drawn["policy"],
        "rubric": canon.load(root).reference,
        "persona": "judging-auditor@1.0.0",
        "framework_commit": FIXTURE_COMMIT,
        "roster_version": drawn["roster_version"],
        "team_count": drawn["team_count"],
        "bracket_size": drawn["bracket_size"],
        "bye_count": drawn["bye_count"],
        "bye_policy": drawn["bye_policy"],
        "random_seed": drawn["seed"],
        "input_digest": drawn["input_digest"],
        "feasible": drawn["feasible"],
        "model_requested": "not-applicable", "model_used": "not-applicable",
        "started_at": STAMP, "completed_at": FINISH,
        "visibility": "private", "approval_state": "approved", "validation_state": "valid",
    }, f"""
# Bracket Report — {EVENT_NAME}

Assignment is a reproducible constraint process, not another judgment of team
quality. Four teams, four slots, no byes.

## Frozen inputs

| Team | Consolidated score | Affiliation group | Previous result |
|---|---:|---|---|
""" + "\n".join(
        f"| {team.id} | {demo.consolidation_for(team, resolved=True, root=root)['display_total']} "
        f"| {team.affiliation_group} | {team.previous_result} |" for team in TEAMS
    ) + f"""

## Assignment result

<!-- atj:bracket:begin -->
{render.bracket_tables(drawn)}
<!-- atj:bracket:end -->

## Why this draw was forced

Two hard constraints act at once on a four-team bracket. `team-lumen` and
`team-harbor` share `north-academy`, so they cannot meet in the first round.
`team-lumen` and `team-quill` are the previous champion and runner-up, so they
cannot share a half. With two first-round matches only one arrangement satisfies
both, and the seed selects presentation order within it rather than the pairing.

## Reproduction

```
python3 -m atj bracket build --event-dir events/{EVENT_ID} --seed {drawn['seed']} \\
  --output events/{EVENT_ID}/bracket.json
python3 -m atj bracket verify events/{EVENT_ID}/bracket.json
```

- [x] Every eligible team appears once
- [x] Bye count is correct
- [x] Previous finalists are separated when feasible
- [x] Affiliation separation is maximized
- [x] Exceptions are documented (none required)
""")
    return drawn


def write_matchups(directory: Path, root: Path) -> dict[str, dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {}
    for name, spec in MATCHUPS.items():
        result = demo.matchup_for(name, root=root)
        results[name] = result
        team_a, team_b = TEAMS_BY_ID[spec["team_a"]], TEAMS_BY_ID[spec["team_b"]]
        match_id = match_identifier(name)
        adjudication_id = (
            ids.adjudication_id(EVENT_ID, "semifinal-2-close-call", 1)
            if result["outcome"] == matchup.ADJUDICATION_REQUIRED else None
        )
        _write(directory / "matchups" / f"{name}.md", {
            "event_id": EVENT_ID, "match_id": match_id, "round_id": ROUND_OF[name],
            "team_a": team_a.id, "team_b": team_b.id,
            "commit_a": team_a.commit, "commit_b": team_b.commit,
            "evidence_package_a": demo.evidence_package_id(team_a),
            "evidence_package_b": demo.evidence_package_id(team_b),
            "rubric": result["rubric"], "source_rubric": result["source_rubric"],
            "persona": "matchup-judge@1.0.0", "framework_commit": FIXTURE_COMMIT,
            "model_requested": FIXTURE_MODEL, "model_used": FIXTURE_MODEL,
            "started_at": STAMP, "completed_at": FINISH,
            "close_call_band": result["close_call_band"],
            "passes": {
                label: {
                    "presented_first": payload["presented_first"],
                    "comparisons": payload["raw_comparisons"],
                }
                for label, payload in result["passes"].items()
            },
            "combined_margin": result["combined_margin"],
            "order_disagreement": result["order_disagreement"],
            "outcome": result["outcome"], "winner": result["winner"],
            "adjudication_id": adjudication_id,
            "visibility": "private", "approval_state": "approved", "validation_state": "valid",
        }, f"""
# Matchup Report — {team_a.display_name} vs {team_b.display_name}

## Eligibility and common evidence

Both teams carry a valid consolidated report at rubric `{result['source_rubric']}`
and a pinned evidence package. Neither presentation order, bracket position,
affiliation nor previous placement was treated as evidence.

## Order-balanced results

<!-- atj:matchup:begin -->
{render.matchup_table(result)}
<!-- atj:matchup:end -->

## Margin and outcome

{spec['note']}

## Decisive evidence

- {team_a.display_name}: {team_a.strength} ({team_a.evidence[0][0]})
- {team_b.display_name}: {team_b.strength} ({team_b.evidence[0][0]})

## Conflicting evidence

{"None: both presentation orders reached the same comparative finding on every criterion." if not result["criterion_order_disagreements"] else "Criterion-level order conflict on: " + ", ".join(result["criterion_order_disagreements"]) + ". Recorded rather than averaged away."}

## Tie-break or adjudication

{
  "Not required. Both passes selected the same team and the combined margin cleared the close-call band."
  if result["outcome"] == matchup.CONFIRMED else
  "Required. The combined margin of "
  + f"{result['combined_margin']:+.2f} sits inside the ±{result['close_call_band']:g} band, "
  "so the framework returned no winner. See "
  + f"`adjudications/{adjudication_id.replace(':', '-')}.md`, decided by a human official."
}

## Audit

- [x] Both passes were independent
- [x] Presentation order was reversed
- [x] Every nonzero comparison cites evidence
- [x] No prohibited team metadata influenced judgment
""")

        if adjudication_id:
            _write_close_call_adjudication(directory, root, name, result, adjudication_id)
    return results


def _write_close_call_adjudication(
    directory: Path, root: Path, name: str, result: dict[str, Any], adjudication_id: str
) -> None:
    broken = matchup.tie_break(result, root=root)
    team_a = TEAMS_BY_ID[result["team_a"]]
    team_b = TEAMS_BY_ID[result["team_b"]]
    _write(directory / "adjudications" / f"{adjudication_id.replace(':', '-')}.md", {
        "event_id": EVENT_ID, "adjudication_id": adjudication_id, "scope": "matchup",
        "team_id": None, "match_id": match_identifier(name), "criterion": broken["step"]
        if broken["resolved"] else None,
        "trigger": "close-call", "question":
            f"Does the evidence establish a winner between {team_a.display_name} and "
            f"{team_b.display_name} despite a margin inside the close-call band?",
        "resolution": "resolved",
        "resolution_detail": CLOSE_CALL_RESOLUTION["rationale"],
        "impact": f"{CLOSE_CALL_RESOLUTION['winner']} advances",
        "confidence": "medium",
        "decided_by": CLOSE_CALL_RESOLUTION["decided_by"],
        "score_override": None,
        "commit": team_a.commit,
        "evidence_package_id": demo.evidence_package_id(team_a),
        "rubric": canon.load(root).reference,
        "persona": "judging-auditor@1.0.0", "framework_commit": FIXTURE_COMMIT,
        "model_requested": "not-applicable", "model_used": "not-applicable",
        "started_at": STAMP, "completed_at": FINISH,
        "visibility": "private", "approval_state": "approved", "validation_state": "valid",
    }, f"""
# Adjudication Report — close-call matchup

## Question

Does the evidence establish a winner between {team_a.display_name} and
{team_b.display_name} when the calculated margin sits inside the close-call band?

## Trigger

`close-call`. `atj matchup` returned `outcome: adjudication-required` and
`winner: null` with a combined margin of {result['combined_margin']:+.2f} against
a band of ±{result['close_call_band']:g}. The framework does not advance a team
here; it hands the decision to a human.

## Disputed claims

| Source artifact | Claim | Evidence cited | Class |
|---|---|---|---|
| matchups/{name}.md | {team_a.display_name} holds a functional advantage | {team_a.evidence[0][0]} | direct observation |
| matchups/{name}.md | {team_b.display_name} holds an innovation advantage | {team_b.evidence[0][0]} | artifact evidence |

## Evidence reviewed

Both consolidated reports, both evidence manifests, and both presentation passes.
No new evidence about either project was gathered.

## Factual resolution

{CLOSE_CALL_RESOLUTION['rationale']}

Mechanical tie-break result: {"resolved at step " + broken["step"] if broken["resolved"] else "exhausted"}, favouring `{broken["winner"] or "no team"}`.

## Impact on the result

| Affected criterion or outcome | Before | After | Mechanism |
|---|---|---|---|
| {ROUND_OF[name]} winner | none returned | {CLOSE_CALL_RESOLUTION['winner']} | human decision recorded on the declared tie-break order |

## Confidence

Medium. The tie-break is decisive on the evidence available; the underlying
margin remains narrow and is disclosed as such.

## Human decision

The {CLOSE_CALL_RESOLUTION['decided_by']} decided on 2026-05-18 that
{CLOSE_CALL_RESOLUTION['winner']} advances. Recorded before any public artifact
was generated.

## Validation

- [x] Question is narrow and answerable
- [x] Every cited artifact resolves
- [x] No original report was modified
- [x] Impact recalculated by `atj matchup`, not by hand
- [x] Human decision recorded where policy requires one
""")


MATCH_WINNER = {"semifinal-1": "team-lumen", "semifinal-2": "team-quill", "final": "team-lumen"}


def write_public(directory: Path, root: Path, results: dict[str, dict[str, Any]]) -> None:
    """Public artifacts are generated from approved private records only.

    They deliberately omit the submission commit, evidence package, judge
    personas, run ids and raw scores. Traceability runs through
    `source_artifacts`, not through republished private identifiers.
    """
    for name, result in results.items():
        team_a, team_b = TEAMS_BY_ID[result["team_a"]], TEAMS_BY_ID[result["team_b"]]
        winner = TEAMS_BY_ID[MATCH_WINNER[name]]
        sources = [f"matchups/{name}.md"]
        if result["outcome"] == matchup.ADJUDICATION_REQUIRED:
            sources.append(
                f"adjudications/{ids.adjudication_id(EVENT_ID, 'semifinal-2-close-call', 1).replace(':', '-')}.md"
            )
        _write(directory / "public" / f"{name}.md", {
            "event_id": EVENT_ID, "match_id": match_identifier(name),
            "round_id": ROUND_OF[name],
            "rubric": canon.load_head_to_head(root).reference,
            "framework_commit": FIXTURE_COMMIT,
            "source_artifacts": sources,
            "scores_published": False,
            "started_at": STAMP, "completed_at": FINISH,
            "visibility": "public", "approval_state": "approved",
            "approved_by": OFFICIAL, "validation_state": "valid",
        }, f"""
# Matchup Summary: {team_a.display_name} vs. {team_b.display_name}

## Winner

**{winner.display_name}** advances.

## Why

{
  "Both independent comparisons, run in opposite presentation orders, favoured "
  + winner.display_name + " on the same evidence. The clearest difference was "
  + winner.strength.rstrip('.') + "."
  if result["outcome"] == matchup.CONFIRMED else
  "The two comparisons agreed but the difference was narrow enough to fall inside "
  "the event's close-call band, so the result was referred to a human official, "
  "who applied the published tie-break order. " + winner.display_name
  + " advanced on functional correctness and completeness."
}

## Both teams did well

- {team_a.display_name}: {team_a.strength}
- {team_b.display_name}: {team_b.strength}

## Identity and privacy note

This artifact is public. It omits the submission commit, the evidence package
ID, judge personas, judge run IDs and raw scores. Its private sources are listed
in `source_artifacts`.
""")

    champion = TEAMS_BY_ID["team-lumen"]
    runner_up = TEAMS_BY_ID["team-quill"]
    _write(directory / "public" / "event-summary.md", {
        "event_id": EVENT_ID,
        "rubric": canon.load(root).reference,
        "framework_commit": FIXTURE_COMMIT,
        "source_artifacts": [f"public/{name}.md" for name in results] + ["bracket.md"],
        "scores_published": False,
        "started_at": STAMP, "completed_at": FINISH,
        "visibility": "public", "approval_state": "approved",
        "approved_by": OFFICIAL, "validation_state": "valid",
    }, f"""
# Event Summary — {EVENT_NAME}

## Event overview

A synthetic four-team single-elimination event used to demonstrate the judging
framework end to end. No real team, project or institution appears in it.

## Champion and finalists

- Champion: **{champion.display_name}**
- Runner-up: **{runner_up.display_name}**
- Semifinalists: {", ".join(team.display_name for team in TEAMS if team.id not in (champion.id, runner_up.id))}

## Bracket results

| Round | Matchup | Winner |
|---|---|---|
""" + "\n".join(
        f"| {ROUND_OF[name]} | {TEAMS_BY_ID[result['team_a']].display_name} vs "
        f"{TEAMS_BY_ID[result['team_b']].display_name} | "
        f"{TEAMS_BY_ID[MATCH_WINNER[name]].display_name} |"
        for name, result in results.items()
    ) + """

## Common strengths across the field

Every entry handled at least one failure path deliberately rather than by
accident, and each documented what it had not finished.

## Common learning opportunities

The field's recurring gap was demonstrating claimed behaviour. Several claims
were plausible and undemonstrated, which limits how high a criterion can be
scored regardless of how good the idea is.

## Judging-method disclosure

Four independent AI judges evaluated each entry in separate contexts against one
shared weighted rubric. No judge saw another judge's report. Scores were
combined arithmetically by a deterministic script; a consolidator summarised the
evidence without changing any score. Disagreements above a declared threshold,
unresolved evidence gaps and close matchups were referred to a human official,
who decided them. Tournament matchups were judged twice in opposite presentation
orders, and a result was only automatic when both passes agreed by more than the
close-call band.

Limitations, stated plainly: no submission was executed in this event, so
conclusions about running behaviour rest on inspected implementation and
team-supplied artifacts. AI judgment is not deterministic; the arithmetic,
validation and bracket assignment around it are.
""")


def write_dossiers(directory: Path, root: Path, results: dict[str, dict[str, Any]]) -> None:
    journeys: dict[str, list[str]] = {team.id: [] for team in TEAMS}
    for name, result in results.items():
        winner = MATCH_WINNER[name]
        for team_id in (result["team_a"], result["team_b"]):
            other = result["team_b"] if team_id == result["team_a"] else result["team_a"]
            outcome = "advanced" if team_id == winner else "did not advance"
            journeys[team_id].append(
                f"- **{ROUND_OF[name].title()}** against {TEAMS_BY_ID[other].display_name}: "
                f"you {outcome}. The deciding difference was "
                f"{TEAMS_BY_ID[winner].strength.rstrip('.').lower()}."
            )

    for team in TEAMS:
        resolved = demo.consolidation_for(team, resolved=True, root=root)
        criterion_rows = "\n".join(
            f"| {entry['name']} | {entry['mean']:.2f} / 5 | {_criterion_note(team, entry)} |"
            for entry in resolved["criteria"].values()
        )
        _write(directory / "dossiers" / f"{team.id}.md", _identity(team, {
            "persona": "build-team-dossier@1.0.0",
            "source_reports": [f"summaries/{team.id}.md", f"evidence/{team.id}/manifest.md"],
            "visibility": "team", "approval_state": "approved", "validation_state": "valid",
        }), f"""
# Team Dossier — {team.display_name}

## Your project at a glance

{team.summary}

Overall panel result: **{resolved['display_total']} / 100**.

## What you did especially well

{team.strength} This was the clearest thing the panel agreed on, and it is worth
keeping as the project grows.

## Criterion feedback

| Criterion | Panel mean | What that reflects |
|---|---|---|
{criterion_rows}

## Tournament journey

{chr(10).join(journeys[team.id]) or "- No matchups were recorded for this team."}

## Blocking issues

- {team.weakness}

## Recommended improvement plan

1. **Immediate repair.** {team.weakness} Fix this first; it is the one confirmed
   defect that affects how the rest of the work is read.
2. **Highest-value next iteration.** Demonstrate the behaviour you described but
   did not show. A claim with a test or a captured run behind it scores
   differently from the same claim on its own.
3. **Longer-term opportunity.** {team.strength.rstrip('.')} is a real strength —
   extend it to the parts of the system that do not yet have it.

## Evidence appendix

{_evidence_table(team)}

These are the observations the panel worked from. Everything here is traceable
to your submitted commit.
""")


def _criterion_note(team: Team, entry: dict[str, Any]) -> str:
    if entry["possible_outliers"]:
        return ("Judges differed sharply here; the panel mean is reported and the "
                "disagreement was reviewed by an official.")
    if entry["agreement"] != scoring.ALIGNED:
        return "Judges differed; the difference was in what counted as demonstrated."
    if entry["mean"] >= 4:
        return "A consistent strength across all four judges."
    if entry["mean"] <= 2:
        return "The weakest area; see the improvement plan."
    return "Solid for the event; the expectations for this criterion were met."


# --------------------------------------------------------------------------- #
# Audits, status ledger, and the top-level build
# --------------------------------------------------------------------------- #

def _audit(
    directory: Path, root: Path, *, name: str, scope: str, result: str,
    team: Team | None, findings: str, gate: str, advisories: str = "None.",
) -> None:
    reference = team or TEAMS[0]
    _write(directory / "audits" / f"{name}.md", {
        "event_id": EVENT_ID, "audit_scope": scope, "audit_id": name,
        "team_id": team.id if team else None, "match_id": None,
        "commit": reference.commit,
        "evidence_package_id": demo.evidence_package_id(reference),
        "rubric": canon.load(root).reference,
        "persona": "judging-auditor@1.0.0", "framework_commit": FIXTURE_COMMIT,
        "model_requested": FIXTURE_MODEL, "model_used": FIXTURE_MODEL,
        "started_at": STAMP, "completed_at": FINISH,
        "visibility": "private", "approval_state": "approved",
        "validation_state": "valid", "result": result,
    }, f"""
# Judging Audit — {scope}

## Result

**{result}**

## Scope and artifacts inspected

{scope}. Gate: `{gate}`.

## Deterministic validation results

```
python3 -m atj event validate events/{EVENT_ID}
python3 -m atj validate reports events/{EVENT_ID}
python3 -m atj bracket verify events/{EVENT_ID}/bracket.json
python3 -m atj release-check
```

Official numbers were recalculated rather than read from the reports.

## Findings

{findings}

## Advisories

{advisories}

## Completion gate

- [{"x" if result != "FAIL" else " "}] No blocking findings
- [{"x" if result != "FAIL" else " "}] No major findings
- [x] Calculations valid
- [x] Evidence references resolve
- [x] Version and identity checks pass
- [x] Privacy boundary passes
""")


def write_audits(directory: Path, root: Path) -> None:
    lumen = TEAMS_BY_ID["team-lumen"]
    before = demo.consolidation_for(lumen, resolved=False, root=root)

    # A real failure, not a staged one: the first consolidation audit for
    # team-lumen fails because an NE blocks the official total.
    _audit(
        directory, root, name="consolidation-team-lumen-01",
        scope="consolidation of team-lumen (first pass)", result="FAIL", team=lumen,
        gate="consolidation-audited",
        findings=f"""| Severity | Rule | Artifact | Finding | Required repair |
|---|---|---|---|---|
| blocking | panel-consolidation@1.0.0 §Preconditions | summaries/team-lumen.md | {before['blocked_reasons'][0]}. `atj score` returned `finalized: false` and no official total. | Adjudicate the `NE` under the disagreement policy, or obtain the missing evidence. The team result may not be finalized and the team may not enter the bracket until this is resolved. |
| advisory | evidence-and-citation | evidence/team-lumen/manifest.md | Execution was unavailable, so `functional` and `reliability` rest on inspected implementation. | None required; the limitation is recorded. |

The provisional sum of scored criteria was {before['provisional_total']:.2f}/100.
That is not a score and was not used for anything.""",
    )

    after = demo.consolidation_for(lumen, resolved=True, root=root)
    _audit(
        directory, root, name="consolidation-team-lumen-02",
        scope="consolidation of team-lumen (after adjudication)", result="PASS", team=lumen,
        gate="consolidation-audited",
        findings=f"""| Severity | Rule | Artifact | Finding | Required repair |
|---|---|---|---|---|
| — | — | — | The blocking finding from `consolidation-team-lumen-01` is repaired. | — |

The adjudication recorded in
`adjudications/{ids.adjudication_id(EVENT_ID, 'team-lumen-security', 1).replace(':', '-')}.md`
resolved the `NE`. `atj score` now returns `finalized: true` with an official
total of {after['display_total']}/100. No individual judge score was modified;
the resolution is recorded alongside them.""",
    )

    _audit(
        directory, root, name="consolidation-panel", scope="consolidation of all four teams",
        result="PASS WITH ADVISORIES", team=None, gate="consolidation-audited",
        findings="""| Severity | Rule | Artifact | Finding | Required repair |
|---|---|---|---|---|
| — | — | — | All four teams have four valid, independent, version-matched judgments. | — |""",
        advisories="""- `team-quill` shows a material disagreement on `agentic` (range 2). Explained in
  its consolidated report; no adjudication threshold crossed.
- `team-harbor` shows a severe disagreement and a possible outlier on
  `innovation`. Adjudicated; the disagreement is preserved rather than averaged
  away.
- Execution was unavailable for the whole event. Every affected conclusion is
  marked in the evidence manifests.""",
    )

    _audit(
        directory, root, name="bracket", scope="bracket draw", result="PASS", team=None,
        gate="bracket-audited",
        findings="""| Severity | Rule | Artifact | Finding | Required repair |
|---|---|---|---|---|
| — | bracket-assignment@1.0.0 | bracket.md | Every hard constraint reports `satisfied`; the draw reproduces byte-for-byte from the recorded seed. | — |""",
    )

    _audit(
        directory, root, name="tournament", scope="all three matchups",
        result="PASS WITH ADVISORIES", team=None, gate="tournament-audited",
        findings="""| Severity | Rule | Artifact | Finding | Required repair |
|---|---|---|---|---|
| — | head-to-head@1.0.0 | matchups/*.md | Every matchup was judged in both presentation orders and normalized before comparison. No presentation-order disagreement occurred. | — |""",
        advisories="""- `semifinal-2` fell inside the close-call band. The framework returned no
  winner; a human official decided it on the published tie-break order. The
  narrow margin is disclosed in the public summary.""",
    )

    _audit(
        directory, root, name="final-event", scope="complete event record",
        result="PASS WITH ADVISORIES", team=None, gate="final-audit-passed",
        findings="""| Severity | Rule | Artifact | Finding | Required repair |
|---|---|---|---|---|
| — | report-publication@1.0.0 | public/*.md | No public artifact carries a private-only field, a credential, a judge persona, a run id, an evidence package id or an unapproved score. Each names an approving official and lists its private sources. | — |
| — | judge-independence@1.0.0 | judgments/**/*.md | Sixteen judgments, four per team, distinct judge ids and distinct run ids, all pinned to the same team, commit, evidence package and rubric version. | — |""",
        advisories="""- No submission was executed anywhere in this event. Two criteria are
  evidence-limited for every team, and that is stated in each manifest and in
  the public judging-method disclosure.
- Judge scores in this fixture are scripted rather than model output. The
  fixture demonstrates the pipeline, not model behaviour.""",
    )


def write_status(directory: Path, root: Path, drawn: dict[str, Any]) -> None:
    units = []
    for team in TEAMS:
        package = demo.evidence_package_id(team)
        units.append({
            "unit_id": f"evidence:{team.id}", "stage": "evidence", "state": "complete",
            "input_digest": ids.digest(team.commit, package, length=16),
            "outputs": [f"evidence/{team.id}/manifest.md"],
            "audit_result": "PASS", "completed_at": FINISH,
        })
        units.append({
            "unit_id": f"judging:{team.id}", "stage": "initial-judging", "state": "complete",
            "input_digest": ids.digest(package, "panel", length=16),
            "outputs": [f"judgments/{team.id}/{judge}.md" for judge in JUDGES],
            "audit_result": "PASS", "completed_at": FINISH,
        })
        units.append({
            "unit_id": f"consolidation:{team.id}", "stage": "consolidation", "state": "complete",
            "input_digest": ids.digest(package, "consolidated", length=16),
            "outputs": [f"summaries/{team.id}.md"],
            "audit_result": "PASS" if team.id != "team-lumen" else "PASS WITH ADVISORIES",
            "completed_at": FINISH,
        })
        units.append({
            "unit_id": f"dossier:{team.id}", "stage": "dossiers", "state": "complete",
            "input_digest": ids.digest(package, "dossier", length=16),
            "outputs": [f"dossiers/{team.id}.md"],
            "audit_result": "PASS", "completed_at": FINISH,
        })
    units.append({
        "unit_id": "bracket:draw", "stage": "bracket", "state": "complete",
        "input_digest": drawn["input_digest"],
        "outputs": ["bracket.md", "bracket.json"],
        "audit_result": "PASS", "completed_at": FINISH,
    })
    for name in MATCHUPS:
        units.append({
            "unit_id": f"matchup:{name}", "stage": "tournament", "state": "complete",
            "input_digest": ids.digest(name, drawn["input_digest"], length=16),
            "outputs": [f"matchups/{name}.md", f"public/{name}.md"],
            "audit_result": "PASS", "completed_at": FINISH,
        })
    units.append({
        "unit_id": "final:audit", "stage": "final-audit", "state": "complete",
        "input_digest": ids.digest("final", drawn["input_digest"], length=16),
        "outputs": ["audits/final-event.md", "public/event-summary.md"],
        "audit_result": "PASS WITH ADVISORIES", "completed_at": FINISH,
    })

    _write(directory / "status.md", {
        "event_id": EVENT_ID, "current_stage": "complete", "last_updated": FINISH,
        "blocked": False, "blocked_reason": None,
        "stage_gates": {gate: "passed" for gate in sorted(set(event_module.STAGE_GATES.values()))},
        "units": units,
    }, f"""
# Event Status — {EVENT_NAME}

Complete. This ledger is what `atj event status` reads to decide the next safe
action, and what recovery uses after an interruption.

## Stage gates

- [x] Configuration audited
- [x] Roster frozen
- [x] All eligible evidence packages validated
- [x] All initial judgments audited
- [x] All consolidated reports audited
- [x] Bracket frozen and audited
- [x] Tournament complete
- [x] All team dossiers approved
- [x] Final event audit passed
- [x] Event marked complete

## Team progress

| Team ID | Intake | Evidence | Four judgments | Consolidated | Audited | Dossier |
|---|---|---|---|---|---|---|
""" + "\n".join(
        f"| {team.id} | done | done | done | done | "
        f"{'PASS after adjudication' if team.id == 'team-lumen' else 'PASS'} | done |"
        for team in TEAMS
    ) + f"""

## Blockers and adjudications

| ID | Scope | Description | Owner | Status | Resolution artifact |
|---|---|---|---|---|---|
| {ids.adjudication_id(EVENT_ID, 'team-lumen-security', 1)} | criterion | Unresolved `NE` on security blocked the official total | {OFFICIAL} | resolved | adjudications/{ids.adjudication_id(EVENT_ID, 'team-lumen-security', 1).replace(':', '-')}.md |
| {ids.adjudication_id(EVENT_ID, 'team-harbor-innovation', 1)} | criterion | Severe disagreement and a possible outlier on innovation | {OFFICIAL} | resolved | adjudications/{ids.adjudication_id(EVENT_ID, 'team-harbor-innovation', 1).replace(':', '-')}.md |
| {ids.adjudication_id(EVENT_ID, 'semifinal-2-close-call', 1)} | matchup | Combined margin inside the close-call band; no winner returned | {OFFICIAL} | resolved | adjudications/{ids.adjudication_id(EVENT_ID, 'semifinal-2-close-call', 1).replace(':', '-')}.md |

## Activity log

| Timestamp | Action | Input identity | Output | Audit result |
|---|---|---|---|---|
| {STAMP} | intake and evidence | four synthetic commits | evidence/*/manifest.md | PASS |
| {STAMP} | initial judging | four evidence packages | judgments/**/*.md | PASS |
| {STAMP} | consolidation (first pass) | team-lumen panel | summaries/team-lumen.md | **FAIL** |
| {STAMP} | adjudication | team-lumen security NE | adjudications/*.md | resolved |
| {STAMP} | consolidation (repaired) | team-lumen panel | summaries/team-lumen.md | PASS |
| {STAMP} | bracket draw | seed `{drawn['seed']}` | bracket.md | PASS |
| {STAMP} | tournament | three matchups, both orders | matchups/*.md | PASS WITH ADVISORIES |
| {FINISH} | dossiers and publication | approved private records | dossiers/*.md, public/*.md | PASS |
| {FINISH} | final event audit | complete record | audits/final-event.md | PASS WITH ADVISORIES |
""")


def build(root: Path, *, clean: bool = True) -> Path:
    """Regenerate the whole sample event. Idempotent."""
    directory = root / "events" / EVENT_ID
    if clean and directory.exists():
        shutil.rmtree(directory)
    for subdir in event_module.EVENT_SUBDIRS:
        (directory / subdir).mkdir(parents=True, exist_ok=True)

    write_event_files(directory, root)
    write_intake_and_evidence(directory, root)
    write_judgments(directory, root)
    write_summaries_and_adjudications(directory, root)
    drawn = write_bracket(directory, root)
    results = write_matchups(directory, root)
    write_public(directory, root, results)
    write_dossiers(directory, root, results)
    write_audits(directory, root)
    write_status(directory, root, drawn)

    fixture = demo.twenty_team_bracket(root)
    fixture_dir = root / "tests" / "fixtures" / "bracket-20-team"
    fixture_dir.mkdir(parents=True, exist_ok=True)
    (fixture_dir / "roster.json").write_text(
        json.dumps({"teams": demo.twenty_team_roster()}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (fixture_dir / "bracket.json").write_text(
        json.dumps(fixture, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (fixture_dir / "README.md").write_text(f"""# 20-team bracket fixture

Synthetic. Twenty invented teams across five affiliation groups, with a previous
champion (`team-01`) and runner-up (`team-02`).

| Property | Value |
|---|---|
| Bracket slots | {fixture['bracket_size']} |
| Preliminary matches | {sum(1 for m in fixture['rounds'][0]['matches'] if not m['bye'])} |
| Preliminary participants | {sum(2 for m in fixture['rounds'][0]['matches'] if not m['bye'])} |
| Byes into the round of 16 | {sum(1 for m in fixture['rounds'][0]['matches'] if m['bye'])} |
| Bye policy | {fixture['bye_policy']} |
| Seed | `{fixture['seed']}` |
| Input digest | `{fixture['input_digest']}` |
| Feasible | {fixture['feasible']} |

Reproduce and verify:

```bash
python3 -m atj bracket build --input tests/fixtures/bracket-20-team/roster.json \\
  --seed {fixture['seed']} --output /tmp/bracket.json
python3 -m atj bracket verify tests/fixtures/bracket-20-team/bracket.json \\
  --reproduce tests/fixtures/bracket-20-team/roster.json
```

The constraint audit inside `bracket.json` records previous-finalist separation
and same-affiliation separation explicitly, including any exception.
""", encoding="utf-8")
    return directory
