---
event_id: trial-2-2026
adjudication_id: adj:trial-2-2026:team-demos:01
question: does the `functional` NE for team-demos stand, or is it cleared by a score the event director supplies?
scope: criterion
team_id: team-demos
match_id: null
criterion: functional
trigger: unresolved-ne
advances_team: null
commit: dc35f6962130af5e5be3fe16672e3d4964850eb9
evidence_package_id: ev:trial-2-2026:team-demos:dc35f6962130:cb3847cb
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
  criterion: functional
  resolved_score: NE
  rationale: >-
    The event director reviewed the criterion and accepted the NE rather than
    supplying a score. The evidence package records functional as evidence-limited for team-demos: no model call was possible in this event, and acts 2
    and 3 require a write into a read-only pinned checkout. Supplying a number
    would be a discretionary value standing in for an observation the event
    could not make, and the rubric's own rule is that a missing observation is
    NE and not a low score. No official total follows, by decision.
amendments:
- amended_at: "2026-09-22T20:40:00Z"
  amended_by: event-director
  reason: >-
    Consolidation audit F26: score_override.rationale was absent, so the
    machine-readable resolution carried no reason for accepting the NE; the
    reasoning now matches the Factual resolution section. Consolidation audit F28: the head-to-head citation paraphrased rule 12 as a
    prohibition; it now quotes the rubric.
  supersedes: >-
    Before this amendment: score_override carried no rationale; the head-to-head
    sentence read "forbids deciding a matchup by the higher initial total".
approved_by: event-director
approved_at: "2026-09-22T18:07:45Z"
approval_note: Both NEs reviewed and accepted; no score supplied.
---

# Adjudication Report

## Question

Does the `functional` `NE` for team-demos stand as the panel recorded it, or does the
event director supply a score that clears it and finalizes an official total?

## Trigger

`unresolved-ne`. `atj score events/trial-2-2026/judgments/team-demos` records
`adjudication_required: [{criterion: functional, trigger: unresolved-ne}]` and
returns `finalized: false` with no total. `judge-frontend-ux` and `judge-security-ops` each recorded `functional` as
`NE`; the other two judges scored it. `framework/rubrics/submission-evaluation.md:36`
permits no official total while a criterion is `NE`.

## Disputed claims

| Source artifact | Claim | Evidence cited | Class |
|---|---|---|---|
| `judgments/team-demos/judge-frontend-ux.md` | the demonstration behaviour the READMEs promise was not observable, so `functional` is `NE` | `ev-demos-01`, `runs/team-demos-envcheck-01.json`, `ev-demos-06` | artifact evidence |
| `judgments/team-demos/judge-security-ops.md` | same | manifest Missing evidence #1 and #2 | artifact evidence |
| `judgments/team-demos/judge-backend.md` | the dry runs are a complete execution of act 1 as documented and `functional` is scorable at 3 | `runs/team-demos-01-dryrun-*.json` | direct observation |
| `judgments/team-demos/judge-product-agentic.md` | `functional` is scorable at 3 on the same captures | `runs/team-demos-01-dryrun-*.json` | direct observation |

## Evidence reviewed

`evidence/team-demos/manifest.md`, whose Missing evidence entries record that no model call was possible in this event — no route off the host and no provider SDK — and that acts 2 and 3 need a write into a read-only pinned checkout; the eleven run records under `runs/`; the four judgments at `judgments/team-demos/`; and `audits/judgments.md`.

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
| `functional` | `NE`, unresolved | `NE`, accepted by adjudication | Panel-level resolution recording `resolved_score: NE`; no judge's score was replaced or adjusted |
| team-demos official total | not finalized, adjudication outstanding | not finalized by decision | The rubric permits no official total while a criterion is `NE`; `atj score` now reports the `NE` as accepted and stops requiring an adjudication |
| Provisional sum | 52.50 of 100, not official | unchanged | No number moved |

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
