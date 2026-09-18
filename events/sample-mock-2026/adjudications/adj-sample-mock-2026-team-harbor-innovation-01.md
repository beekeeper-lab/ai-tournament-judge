---
event_id: sample-mock-2026
team_id: team-harbor
commit: 213a8d470271071a81322e41614345b87f67dd0c
evidence_package_id: ev:sample-mock-2026:team-harbor:213a8d470271:85a7e2cb
rubric: submission-evaluation@1.1.0
framework_commit: uncommitted
model_requested: not-applicable (scripted fixture)
model_used: not-applicable (scripted fixture)
started_at: "2026-05-18T09:00:00Z"
completed_at: "2026-05-18T17:30:00Z"
adjudication_id: adj:sample-mock-2026:team-harbor-innovation:01
scope: criterion
match_id: null
criterion: innovation
trigger: severe-disagreement
question: Is the log-correlation approach demonstrated, or only described?
resolution: resolved
resolution_detail: The approach is genuinely unusual, which explains the high score, but ev-harbor-02 shows the demonstrating timeline is committed rather than produced by the code. The panel mean stands; the disagreement is recorded as a difference in what each judge treated as demonstration, not as a factual contradiction.
impact: recorded alongside the source scores; no source score was modified
confidence: medium
decided_by: head judging official
decision_authority: human-official
score_override: null
persona: judging-auditor@1.1.0
visibility: private
approval_state: approved
validation_state: valid
---

# Adjudication Report — Harbor — innovation

## Question

Is the log-correlation approach demonstrated, or only described?

## Trigger

`severe-disagreement`, raised by `atj score` during consolidation of
`summaries/team-harbor.md`.

## Disputed claims

| Source artifact | Claim | Evidence cited | Class |
|---|---|---|---|
| judgments/team-harbor/judge-security-ops.md | the panel minority position | ev-harbor-03 | direct-observation |
| judgments/team-harbor/judge-backend.md | the panel majority position | ev-harbor-02 | direct-observation |

## Evidence reviewed

| Evidence ID | Class | Observation |
|---|---|---|
| ev-harbor-01 | artifact | src/correlate.py groups by timestamp proximity only. |
| ev-harbor-02 | direct-observation | The demo timeline file is committed, not generated. |
| ev-harbor-03 | direct-observation | Two of nine documented workflows complete. |
| ev-harbor-04 | artifact | No tests cover the correlation heuristic. |

## Factual resolution

The approach is genuinely unusual, which explains the high score, but ev-harbor-02 shows the demonstrating timeline is committed rather than produced by the code. The panel mean stands; the disagreement is recorded as a difference in what each judge treated as demonstration, not as a factual contradiction.

## Impact on the result

| Affected criterion or outcome | Before | After | Mechanism |
|---|---|---|---|
| innovation | severe disagreement | unchanged | no change; disagreement preserved and explained |

## Confidence

Medium. The pinned evidence settles the question asked; it does not settle
everything a deployed system would reveal.

## Human decision

Decided by the head judging official on 2026-05-18. Original judge reports are
unmodified; this record attaches to them.

## Validation

- [x] Question is narrow and answerable
- [x] Every cited artifact resolves
- [x] No original report was modified
- [x] Impact recalculated by `atj score`, not by hand
- [x] Human decision recorded where policy requires one
