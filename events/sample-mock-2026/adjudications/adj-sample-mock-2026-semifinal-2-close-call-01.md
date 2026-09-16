---
event_id: sample-mock-2026
adjudication_id: adj:sample-mock-2026:semifinal-2-close-call:01
scope: matchup
team_id: null
match_id: mu:sample-mock-2026:semifinal:01
criterion: functional
trigger: close-call
question: Does the evidence establish a winner between Quill and Harbor despite a
  margin inside the close-call band?
resolution: resolved
resolution_detail: 'Tie-break order applied. Functional correctness and completeness
  is the first step and favours team-quill in both presentation orders (ev-quill-01
  against ev-harbor-03: seven of eight documented workflows complete versus two of
  nine). Recorded as a human decision because the calculated margin was inside the
  close-call band.'
impact: team-quill advances
confidence: medium
decided_by: head judging official
score_override: null
commit: 1ff35a656b351b0529a7bc2d6b169aec650e1e71
evidence_package_id: ev:sample-mock-2026:team-quill:1ff35a656b35:f815c851
rubric: submission-evaluation@1.0.0
persona: judging-auditor@1.0.0
framework_commit: uncommitted
model_requested: not-applicable
model_used: not-applicable
started_at: "2026-05-18T09:00:00Z"
completed_at: "2026-05-18T17:30:00Z"
visibility: private
approval_state: approved
validation_state: valid
---
# Adjudication Report — close-call matchup

## Question

Does the evidence establish a winner between Quill and
Harbor when the calculated margin sits inside the close-call band?

## Trigger

`close-call`. `atj matchup` returned `outcome: adjudication-required` and
`winner: null` with a combined margin of +5.00 against
a band of ±5. The framework does not advance a team
here; it hands the decision to a human.

## Disputed claims

| Source artifact | Claim | Evidence cited | Class |
|---|---|---|---|
| matchups/semifinal-2.md | Quill holds a functional advantage | ev-quill-01 | direct observation |
| matchups/semifinal-2.md | Harbor holds an innovation advantage | ev-harbor-01 | artifact evidence |

## Evidence reviewed

Both consolidated reports, both evidence manifests, and both presentation passes.
No new evidence about either project was gathered.

## Factual resolution

Tie-break order applied. Functional correctness and completeness is the first step and favours team-quill in both presentation orders (ev-quill-01 against ev-harbor-03: seven of eight documented workflows complete versus two of nine). Recorded as a human decision because the calculated margin was inside the close-call band.

Mechanical tie-break result: resolved at step functional, favouring `team-quill`.

## Impact on the result

| Affected criterion or outcome | Before | After | Mechanism |
|---|---|---|---|
| semifinal winner | none returned | team-quill | human decision recorded on the declared tie-break order |

## Confidence

Medium. The tie-break is decisive on the evidence available; the underlying
margin remains narrow and is disclosed as such.

## Human decision

The head judging official decided on 2026-05-18 that
team-quill advances. Recorded before any public artifact
was generated.

## Validation

- [x] Question is narrow and answerable
- [x] Every cited artifact resolves
- [x] No original report was modified
- [x] Impact recalculated by `atj matchup`, not by hand
- [x] Human decision recorded where policy requires one
