---
event_id: trial-2-2026
adjudication_id: adj:trial-2-2026:team-scribe:01
question: does the `agentic` NE for team-scribe stand, or is it cleared by a score the event director supplies?
scope: criterion
team_id: team-scribe
match_id: null
criterion: agentic
trigger: unresolved-ne
advances_team: null
commit: 67969dd9479c096f05d998d8c50e5ea1968e3245
evidence_package_id: ev:trial-2-2026:team-scribe:67969dd9479c:018cf089
rubric: submission-evaluation@1.1.0
persona: consolidate-judgments@1.0.0
framework_commit: af9f6fba9e0d6f54a69156193fc57be16d7a4357
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-22T14:40:00Z"
completed_at: "2026-09-22T14:45:00Z"
visibility: private
approval_state: approved
validation_state: valid
resolution: resolved
decided_by: event-director
decision_authority: human-official
score_override:
  criterion: agentic
  resolved_score: NE
  rationale: >-
    The event director reviewed the criterion and accepted the NE rather than
    supplying a score. The evidence package records agentic as evidence-limited
    for team-scribe: no model call, no cost figure, no categorization output and
    no rendered estimate were obtainable. Supplying a number would be a
    discretionary value standing in for an observation the event could not make,
    and the rubric's own rule is that a missing observation is NE and not a low
    score. No official total follows, by decision.
amendments:
- amended_at: "2026-09-22T20:40:00Z"
  amended_by: event-director
  reason: >-
    Consolidation audit F26: score_override.rationale was absent, so the
    machine-readable resolution carried no reason for accepting the NE; the
    reasoning now matches the Factual resolution section. Consolidation audit F28: the head-to-head citation paraphrased rule 12 as a
    prohibition; it now quotes the rubric.
- amended_at: "2026-09-22T20:40:00Z"
  amended_by: event-director
  reason: >-
    Consolidation audit F29: the disputed-claims row misstated the basis of
    judge-backend's agentic score as the development-time agent configuration;
    that judgment rests on the runtime AI path and ev-scribe-11. The question,
    the resolution and the human decision are unchanged.
  supersedes: >-
    Before this amendment: score_override carried no rationale; the head-to-head
    sentence read "forbids deciding a matchup by the higher initial total"; the
    disputed-claims row read "`agentic` is scorable at 2 from the development-
    time agent configuration in the tree".
approved_by: event-director
approved_at: "2026-09-22T18:07:45Z"
approval_note: Both NEs reviewed and accepted; no score supplied.
---

# Adjudication Report

## Question

Does the `agentic` `NE` for team-scribe stand as the panel recorded it, or does the
event director supply a score that clears it and finalizes an official total?

## Trigger

`unresolved-ne`. `atj score events/trial-2-2026/judgments/team-scribe` records
`adjudication_required: [{criterion: agentic, trigger: unresolved-ne}]` and
returns `finalized: false` with no total. `judge-frontend-ux` and `judge-security-ops` each recorded `agentic` as
`NE`; the other two judges scored it. `framework/rubrics/submission-evaluation.md:36`
permits no official total while a criterion is `NE`.

## Disputed claims

| Source artifact | Claim | Evidence cited | Class |
|---|---|---|---|
| `judgments/team-scribe/judge-frontend-ux.md` | `agentic` is not observable from the evidence available | manifest `evidence_limited_criteria` | artifact evidence |
| `judgments/team-scribe/judge-security-ops.md` | same | manifest `evidence_limited_criteria` | artifact evidence |
| `judgments/team-scribe/judge-backend.md` | `agentic` is scorable at 2 from the runtime AI path read at the pin, plus `ev-scribe-11` | static read at the pin | direct observation |
| `judgments/team-scribe/judge-product-agentic.md` | `agentic` is scorable at 3 on the same surface | static read at the pin | direct observation |

## Evidence reviewed

`evidence/team-scribe/manifest.md`, which lists the criteria it declares evidence-limited and states which absences are the event's and which are the submission's; the four judgments at `judgments/team-scribe/`; and `audits/judgments.md`, which verified each `NE` against the manifest sentence that authorizes it.

No evidence outside the pinned package was gathered for this adjudication, and
none was needed: the question is whether the recorded `NE` stands, not what the
criterion's value is.

## Factual resolution

The `NE`s are correct and they are not resolvable from the available evidence.
Each was argued from the exact sentence of the evidence manifest that declares the
criterion evidence-limited, and the judgments stage audit verified every one of the
four against its manifest over three rounds (`audits/judgments.md`, F1 through F22,
none of which disturbed an `NE`).

The event director reviewed the criterion and accepts the `NE`. It stands. No score
is supplied, because supplying one would be a discretionary number standing in for
an observation the event could not make, and the rubric's own rule is that a
missing observation is `NE` and not a low score.

## Impact on the result

| Affected criterion or outcome | Before | After | Mechanism |
|---|---|---|---|
| `agentic` | `NE`, unresolved | `NE`, accepted by adjudication | Panel-level resolution recording `resolved_score: NE`; no judge's score was replaced or adjusted |
| team-scribe official total | not finalized, adjudication outstanding | not finalized by decision | The rubric permits no official total while a criterion is `NE`; `atj score` now reports the `NE` as accepted and stops requiring an adjudication |
| Provisional sum | 32.50 of 100, not official | unchanged | No number moved |

## Confidence

`high`. The disposition rests on what the evidence package does not contain, which
is recorded in the manifest, approved, and frozen. Nothing about it is a judgment
call on the submission.

## Human decision

The event director decided on 2026-09-22 to accept the `NE` rather than supply a
score. Recorded as `decision_authority: human-official` because the official made
the decision; the record was drafted by the agent running the consolidation stage
and carries no authority of its own.

The decision costs the event nothing downstream. Two teams grant no byes, so the
`performance-qualified` bye policy never reads a total
(`events/trial-2-2026/event.md:88-90`), and `framework/rubrics/head-to-head.md:12`
says "Do not merely select the team with the higher initial total". The dossier carries
per-criterion scores and no team total.

## Validation

- [x] Question is narrow and answerable
- [x] Every cited artifact resolves
- [x] No original report was modified
