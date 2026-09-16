"""Synthetic sample event.

Generates a complete, committed, obviously-fake event that exercises every stage
and every awkward case the framework claims to handle: a material disagreement,
a severe disagreement with an outlier, an initial `NE`, an adjudication, a
close-call matchup, an order-balanced matchup with a consistent result, a failed
audit that is then repaired, and the full private / team-facing / public split.

**The judge scores here are scripted, not model output.** They are fixed inputs
chosen to produce the exact conditions above, so the pipeline is reproducible in
CI without an LLM call and without claiming an LLM is deterministic. Every
artifact records `model_used: not-applicable (scripted fixture)`; nothing here
should be mistaken for a judgment. The agent layer is exercised separately
against a real panel run, recorded in docs/implementation-detail.md.

No real team, person, school, or repository appears anywhere in this module.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import bracket, canon, frontmatter, ids, matchup, scoring, versions
from .errors import ValidationError

EVENT_ID = "sample-mock-2026"
EVENT_NAME = "Sample Mock Event 2026"
SEED = "sample-mock-2026-draw"
FIXTURE_MODEL = "not-applicable (scripted fixture)"
JUDGES = ("judge-backend", "judge-frontend-ux", "judge-security-ops", "judge-product-agentic")

BRACKET_FIXTURE_SEED = "twenty-team-fixture-2026"
BRACKET_FIXTURE_TEAMS = 20


@dataclass(frozen=True)
class Team:
    id: str
    display_name: str
    affiliation_group: str
    previous_result: str
    summary: str
    strength: str
    weakness: str
    scores: dict[str, dict[str, Any]]
    evidence: list[tuple[str, str, str]] = field(default_factory=list)

    @property
    def commit(self) -> str:
        """A deterministic, obviously synthetic commit hash."""
        return ids.digest("sample-commit", self.id, length=40)


# Scores are chosen to produce, respectively: an aligned panel, a material
# disagreement, a severe disagreement with an outlier, and an initial NE.
TEAMS = (
    Team(
        id="team-lumen",
        display_name="Lumen",
        affiliation_group="north-academy",
        previous_result="champion",
        summary="A shift-handover tool for small clinics. Server-rendered, no framework.",
        strength="Explicit state machine for handover status with exhaustive transition tests.",
        weakness="Session handling stores a bare user id in a cookie with no signature.",
        scores={
            "functional":  {j: 4 for j in JUDGES},
            "product":     {j: 4 for j in JUDGES},
            "agentic":     {j: 3 for j in JUDGES},
            "engineering": {"judge-backend": 5, "judge-frontend-ux": 4,
                            "judge-security-ops": 4, "judge-product-agentic": 4},
            "reliability": {j: 4 for j in JUDGES},
            # The security judge cannot see the deployed cookie configuration and
            # says so rather than guessing. This blocks finalization until it is
            # adjudicated.
            "security":    {"judge-backend": 3, "judge-frontend-ux": 3,
                            "judge-security-ops": "NE", "judge-product-agentic": 3},
            "innovation":  {j: 3 for j in JUDGES},
        },
        evidence=[
            ("ev-lumen-01", "direct-observation", "Handover transition tests pass: 41 of 41."),
            ("ev-lumen-02", "artifact", "src/handover/state.py defines the transition table."),
            ("ev-lumen-03", "artifact", "src/web/session.py:22 sets an unsigned `uid` cookie."),
            ("ev-lumen-04", "team-claim", "README claims audit logging; no log sink is configured."),
        ],
    ),
    Team(
        id="team-quill",
        display_name="Quill",
        affiliation_group="south-institute",
        previous_result="runner-up",
        summary="A reading-list assistant that summarizes and tags saved articles.",
        strength="Keyboard-first interface with visible loading, empty and failure states.",
        weakness="The summarizer has no evaluation loop and no fallback when the model errors.",
        scores={
            "functional":  {j: 4 for j in JUDGES},
            "product":     {"judge-backend": 4, "judge-frontend-ux": 5,
                            "judge-security-ops": 4, "judge-product-agentic": 5},
            # Range of 2: a material disagreement that must be explained.
            "agentic":     {"judge-backend": 2, "judge-frontend-ux": 4,
                            "judge-security-ops": 3, "judge-product-agentic": 4},
            "engineering": {j: 3 for j in JUDGES},
            "reliability": {j: 3 for j in JUDGES},
            "security":    {j: 3 for j in JUDGES},
            "innovation":  {j: 4 for j in JUDGES},
        },
        evidence=[
            ("ev-quill-01", "direct-observation", "Empty, loading and error states captured for the save flow."),
            ("ev-quill-02", "artifact", "src/summarize.ts calls the model once with no retry or fallback."),
            ("ev-quill-03", "direct-observation", "Keyboard traversal reaches every interactive control."),
            ("ev-quill-04", "inference", "No evaluation harness is present in the repository."),
        ],
    ),
    Team(
        id="team-harbor",
        display_name="Harbor",
        affiliation_group="north-academy",
        previous_result="none",
        summary="An incident-timeline builder that assembles a narrative from logs.",
        strength="Novel log-correlation approach that groups events by causal proximity.",
        weakness="Correlation is unvalidated; the demo timeline is hand-curated.",
        scores={
            "functional":  {"judge-backend": 2, "judge-frontend-ux": 3,
                            "judge-security-ops": 3, "judge-product-agentic": 3},
            "product":     {j: 3 for j in JUDGES},
            "agentic":     {j: 3 for j in JUDGES},
            "engineering": {j: 2 for j in JUDGES},
            "reliability": {j: 2 for j in JUDGES},
            "security":    {j: 3 for j in JUDGES},
            # Range of 3 and a judge two points from the median: severe
            # disagreement plus a possible outlier.
            "innovation":  {"judge-backend": 2, "judge-frontend-ux": 2,
                            "judge-security-ops": 2, "judge-product-agentic": 5},
        },
        evidence=[
            ("ev-harbor-01", "artifact", "src/correlate.py groups by timestamp proximity only."),
            ("ev-harbor-02", "direct-observation", "The demo timeline file is committed, not generated."),
            ("ev-harbor-03", "direct-observation", "Two of nine documented workflows complete."),
            ("ev-harbor-04", "artifact", "No tests cover the correlation heuristic."),
        ],
    ),
    Team(
        id="team-verdant",
        display_name="Verdant",
        affiliation_group="east-college",
        previous_result="none",
        summary="A campus energy dashboard with anomaly alerts over meter data.",
        strength="Honest uncertainty handling: alerts show confidence and can be dismissed.",
        weakness="Single hard-coded data source; ingestion fails closed with no operator signal.",
        scores={
            "functional":  {j: 3 for j in JUDGES},
            "product":     {j: 3 for j in JUDGES},
            "agentic":     {"judge-backend": 3, "judge-frontend-ux": 3,
                            "judge-security-ops": 3, "judge-product-agentic": 4},
            "engineering": {j: 3 for j in JUDGES},
            "reliability": {"judge-backend": 2, "judge-frontend-ux": 3,
                            "judge-security-ops": 2, "judge-product-agentic": 3},
            "security":    {j: 3 for j in JUDGES},
            "innovation":  {j: 3 for j in JUDGES},
        },
        evidence=[
            ("ev-verdant-01", "direct-observation", "Alert confidence is shown and dismissals persist."),
            ("ev-verdant-02", "artifact", "src/ingest.py:14 hard-codes the meter endpoint."),
            ("ev-verdant-03", "direct-observation", "A failed ingest leaves the dashboard silently stale."),
            ("ev-verdant-04", "artifact", "Nine integration tests cover the alerting path."),
        ],
    ),
)

TEAMS_BY_ID = {team.id: team for team in TEAMS}

# The adjudication that clears team-lumen's NE. A human official decides; the
# framework records the decision, it does not make it.
LUMEN_ADJUDICATION = {
    "criterion": "security",
    "trigger": "unresolved-ne",
    "question": "Can the session cookie's protection be established from the pinned evidence?",
    "resolution": "resolved",
    "resolved_score": 2,
    "rationale": (
        "src/web/session.py:22 sets the cookie without a signature, and no middleware "
        "adds one. The absence of deployment configuration limits confidence about "
        "transport flags, but the unsigned value is directly observable in the pinned "
        "source and is sufficient to score the criterion."
    ),
    "decided_by": "head judging official",
}

HARBOR_ADJUDICATION = {
    "criterion": "innovation",
    "trigger": "severe-disagreement",
    "question": "Is the log-correlation approach demonstrated, or only described?",
    "resolution": "resolved",
    "resolved_score": None,
    "rationale": (
        "The approach is genuinely unusual, which explains the high score, but "
        "ev-harbor-02 shows the demonstrating timeline is committed rather than "
        "produced by the code. The panel mean stands; the disagreement is recorded "
        "as a difference in what each judge treated as demonstration, not as a "
        "factual contradiction."
    ),
    "decided_by": "head judging official",
}

# Comparison values are scripted to produce one decisive matchup, one close call,
# and a final whose two presentation orders agree.
MATCHUPS = {
    "semifinal-1": {
        "team_a": "team-lumen", "team_b": "team-verdant",
        "a_first": {"functional": 1, "product": 1, "agentic": 0,
                    "engineering": 2, "reliability": 1, "security": 0, "innovation": 0},
        "b_first": {"functional": -1, "product": -1, "agentic": 0,
                    "engineering": -2, "reliability": -1, "security": 0, "innovation": 0},
        "note": "Consistent across both presentation orders and decisively outside the band.",
    },
    "semifinal-2": {
        "team_a": "team-quill", "team_b": "team-harbor",
        "a_first": {"functional": 1, "product": -1, "agentic": 0,
                    "engineering": 0, "reliability": 0, "security": 0, "innovation": 0},
        "b_first": {"functional": -1, "product": 1, "agentic": 0,
                    "engineering": 0, "reliability": 0, "security": 0, "innovation": 0},
        "note": ("A close call. Both orders favour the same team, but the combined margin "
                 "of 5.0 sits exactly on the close-call band, so no winner is returned and "
                 "a human official decides."),
    },
    "final": {
        "team_a": "team-lumen", "team_b": "team-quill",
        "a_first": {"functional": 0, "product": -1, "agentic": 0,
                    "engineering": 1, "reliability": 2, "security": 0, "innovation": 0},
        "b_first": {"functional": 0, "product": 1, "agentic": 0,
                    "engineering": -1, "reliability": -2, "security": 0, "innovation": 0},
        "note": "Both orders select the same team; the margin clears the close-call band.",
    },
}

CLOSE_CALL_RESOLUTION = {
    "match": "semifinal-2",
    "winner": "team-quill",
    "decided_by": "head judging official",
    "rationale": (
        "Tie-break order applied. Functional correctness and completeness is the first "
        "step and favours team-quill in both presentation orders (ev-quill-01 against "
        "ev-harbor-03: seven of eight documented workflows complete versus two of nine). "
        "Recorded as a human decision because the calculated margin was inside the "
        "close-call band."
    ),
}


def evidence_package_id(team: Team) -> str:
    body = "\n".join(f"{eid}|{kind}|{note}" for eid, kind, note in team.evidence)
    return ids.evidence_package_id(EVENT_ID, team.id, team.commit, ids.content_digest(body))


def judgments_for(team: Team, rubric: canon.Rubric) -> list[scoring.Judgment]:
    package = evidence_package_id(team)
    return [
        scoring.Judgment(
            judge_id=judge,
            judge_run_id=ids.judge_run_id(EVENT_ID, team.id, judge, package),
            team_id=team.id,
            commit=team.commit,
            evidence_package_id=package,
            rubric=rubric.reference,
            persona=f"{judge}@1.0.0",
            scores={c: team.scores[c][judge] for c in rubric.criterion_ids},
            confidence={c: "high" if team.scores[c][judge] != "NE" else "low"
                        for c in rubric.criterion_ids},
            source=f"{team.id}/{judge}",
        )
        for judge in JUDGES
    ]


RESOLUTIONS = {
    "team-lumen": {
        "security": {
            "adjudication_id": "team-lumen-security",
            "resolved_score": LUMEN_ADJUDICATION["resolved_score"],
            "rationale": LUMEN_ADJUDICATION["rationale"],
        }
    },
    "team-harbor": {
        "innovation": {
            "adjudication_id": "team-harbor-innovation",
            "resolved_score": None,
            "rationale": HARBOR_ADJUDICATION["rationale"],
        }
    },
}


def consolidation_for(team: Team, *, resolved: bool, root: Path | None = None) -> dict[str, Any]:
    """Consolidate a team, optionally after its adjudication has been applied.

    ``resolved=False`` reproduces the pre-adjudication state, which is what makes
    the sample event's failed-then-repaired audit real rather than staged.
    """
    rubric = canon.load(root)
    judgments = judgments_for(team, rubric)
    resolutions = RESOLUTIONS.get(team.id, {}) if resolved else {}
    return scoring.consolidate(
        judgments, expected_judges=JUDGES, resolutions=resolutions, root=root
    )


def matchup_for(name: str, *, root: Path | None = None) -> dict[str, Any]:
    spec = MATCHUPS[name]
    return matchup.calculate(
        team_a=spec["team_a"], team_b=spec["team_b"],
        a_first={"presented_first": spec["team_a"], "comparisons": spec["a_first"]},
        b_first={"presented_first": spec["team_b"], "comparisons": spec["b_first"]},
        root=root,
    )


def sample_bracket(root: Path | None = None) -> dict[str, Any]:
    scores = {
        team.id: consolidation_for(team, resolved=True, root=root)["display_total"]
        for team in TEAMS
    }
    entries = [
        {
            "id": team.id,
            "affiliation_group": team.affiliation_group,
            "previous_result": team.previous_result,
            "score": scores[team.id],
        }
        for team in TEAMS
    ]
    return bracket.build(
        event_id=EVENT_ID, teams=entries, seed=SEED,
        bye_policy="performance-qualified", roster_version=1,
        framework_commit=versions.framework_commit(root), root=root,
    )


def twenty_team_roster() -> list[dict[str, Any]]:
    """A synthetic 20-team field: obviously fake names, five affiliation groups."""
    groups = ("north-academy", "south-institute", "east-college", "west-polytechnic", "central-lab")
    roster = []
    for index in range(BRACKET_FIXTURE_TEAMS):
        roster.append({
            "id": f"team-{index + 1:02d}",
            "display_name": f"Synthetic Team {index + 1:02d}",
            "affiliation_group": groups[index % len(groups)],
            "previous_result": "none",
            "score": round(92.5 - index * 2.1, 1),
        })
    roster[0]["previous_result"] = "champion"
    roster[1]["previous_result"] = "runner-up"
    return roster


def twenty_team_bracket(root: Path | None = None) -> dict[str, Any]:
    return bracket.build(
        event_id="bracket-fixture-2026", teams=twenty_team_roster(), seed=BRACKET_FIXTURE_SEED,
        bye_policy="performance-qualified", roster_version=1,
        framework_commit=ids.UNCOMMITTED, root=root,
    )


def expected_conditions(root: Path | None = None) -> dict[str, Any]:
    """Re-derive every condition the sample event is supposed to demonstrate.

    Used by the demo verifier and by CI. If a change to the tooling stops the
    fixture producing, say, a severe disagreement, this reports it rather than
    letting the sample quietly stop covering the case.
    """
    findings: dict[str, Any] = {}

    lumen_before = consolidation_for(TEAMS_BY_ID["team-lumen"], resolved=False, root=root)
    findings["initial_ne"] = {
        "team": "team-lumen",
        "blocked": not lumen_before["finalized"],
        "reasons": lumen_before["blocked_reasons"],
    }
    harbor_before = consolidation_for(TEAMS_BY_ID["team-harbor"], resolved=False, root=root)
    findings["severe_disagreement_blocks"] = {
        "team": "team-harbor",
        "blocked": not harbor_before["finalized"],
        "reasons": harbor_before["blocked_reasons"],
    }
    lumen_after = consolidation_for(TEAMS_BY_ID["team-lumen"], resolved=True, root=root)
    findings["adjudication_clears_ne"] = {
        "team": "team-lumen", "finalized": lumen_after["finalized"],
        "total": lumen_after["display_total"],
    }

    quill = consolidation_for(TEAMS_BY_ID["team-quill"], resolved=True, root=root)
    findings["material_disagreement"] = {
        "team": "team-quill", "criterion": "agentic",
        "agreement": quill["criteria"]["agentic"]["agreement"],
        "range": quill["criteria"]["agentic"]["range"],
    }

    harbor = consolidation_for(TEAMS_BY_ID["team-harbor"], resolved=True, root=root)
    findings["severe_disagreement"] = {
        "team": "team-harbor", "criterion": "innovation",
        "agreement": harbor["criteria"]["innovation"]["agreement"],
        "outliers": harbor["criteria"]["innovation"]["possible_outliers"],
    }

    for name in MATCHUPS:
        result = matchup_for(name, root=root)
        findings[f"matchup_{name.replace('-', '_')}"] = {
            "outcome": result["outcome"], "winner": result["winner"],
            "combined_margin": result["combined_margin"],
            "order_disagreement": result["order_disagreement"],
        }

    drawn = sample_bracket(root)
    findings["bracket"] = {
        "feasible": drawn["feasible"],
        "problems": bracket.verify(drawn),
        "constraints": {entry["constraint"]: entry["status"] for entry in drawn["constraint_audit"]},
    }

    fixture = twenty_team_bracket(root)
    first = fixture["rounds"][0]["matches"]
    findings["twenty_team_fixture"] = {
        "slots": fixture["bracket_size"],
        "preliminary_matches": sum(1 for m in first if not m["bye"]),
        "preliminary_participants": sum(2 for m in first if not m["bye"]),
        "byes": sum(1 for m in first if m["bye"]),
        "feasible": fixture["feasible"],
        "reproducible": (
            bracket.draw_only(twenty_team_bracket(root)) == bracket.draw_only(fixture)
        ),
    }
    return findings


REQUIRED_CONDITIONS = {
    "initial_ne": lambda f: f["initial_ne"]["blocked"],
    "adjudication_clears_ne": lambda f: f["adjudication_clears_ne"]["finalized"],
    "material_disagreement": lambda f: f["material_disagreement"]["agreement"] == scoring.MATERIAL,
    "severe_disagreement": lambda f: (
        f["severe_disagreement"]["agreement"] == scoring.SEVERE
        and bool(f["severe_disagreement"]["outliers"])
    ),
    "severe_disagreement_blocks_until_adjudicated": lambda f: (
        f["severe_disagreement_blocks"]["blocked"]
    ),
    "decisive_matchup": lambda f: (
        f["matchup_semifinal_1"]["outcome"] == matchup.CONFIRMED
        and f["matchup_semifinal_1"]["winner"] is not None
    ),
    "close_call_matchup": lambda f: (
        f["matchup_semifinal_2"]["outcome"] == matchup.ADJUDICATION_REQUIRED
        and f["matchup_semifinal_2"]["winner"] is None
    ),
    "order_balanced_consistent_matchup": lambda f: (
        f["matchup_final"]["outcome"] == matchup.CONFIRMED
        and not f["matchup_final"]["order_disagreement"]
    ),
    "bracket_feasible": lambda f: f["bracket"]["feasible"] and not f["bracket"]["problems"],
    "twenty_team_shape": lambda f: (
        f["twenty_team_fixture"]["slots"] == 32
        and f["twenty_team_fixture"]["preliminary_matches"] == 4
        and f["twenty_team_fixture"]["preliminary_participants"] == 8
        and f["twenty_team_fixture"]["byes"] == 12
    ),
    "twenty_team_reproducible": lambda f: f["twenty_team_fixture"]["reproducible"],
}


CONDITION_EVIDENCE = {
    "initial_ne": "initial_ne",
    "adjudication_clears_ne": "adjudication_clears_ne",
    "material_disagreement": "material_disagreement",
    "severe_disagreement": "severe_disagreement",
    "severe_disagreement_blocks_until_adjudicated": "severe_disagreement_blocks",
    "decisive_matchup": "matchup_semifinal_1",
    "close_call_matchup": "matchup_semifinal_2",
    "order_balanced_consistent_matchup": "matchup_final",
    "bracket_feasible": "bracket",
    "twenty_team_shape": "twenty_team_fixture",
    "twenty_team_reproducible": "twenty_team_fixture",
}


def check_conditions(root: Path | None = None) -> list[str]:
    """Report any required case the fixture has stopped demonstrating."""
    findings = expected_conditions(root)
    problems = []
    for name, predicate in REQUIRED_CONDITIONS.items():
        if predicate(findings):
            continue
        evidence = findings.get(CONDITION_EVIDENCE.get(name, name), {})
        problems.append(f"{name}: not demonstrated — {json.dumps(evidence, default=str)[:200]}")
    return problems
