---
event_id: sample-mock-2026
match_id: mu:sample-mock-2026:semifinal:02
round_id: semifinal
team_a: team-lumen
team_b: team-verdant
commit_a: 1d46525edc7a377a802930091df18ad921262657
commit_b: 57435ce0f24aacf5d49e41d78225d67882eccf91
evidence_package_a: ev:sample-mock-2026:team-lumen:1d46525edc7a:7c194426
evidence_package_b: ev:sample-mock-2026:team-verdant:57435ce0f24a:e015944d
rubric: head-to-head@1.1.0
source_rubric: submission-evaluation@1.1.0
persona: matchup-judge@1.1.0
framework_commit: uncommitted
model_requested: not-applicable (scripted fixture)
model_used: not-applicable (scripted fixture)
started_at: "2026-05-18T09:00:00Z"
completed_at: "2026-05-18T17:30:00Z"
close_call_band: 5.0
passes:
  a_first:
    presented_first: team-lumen
    comparisons:
      functional: 1
      product: 1
      agentic: 0
      engineering: 2
      reliability: 1
      security: 0
      innovation: 0
  b_first:
    presented_first: team-verdant
    comparisons:
      functional: -1
      product: -1
      agentic: 0
      engineering: -2
      reliability: -1
      security: 0
      innovation: 0
combined_margin: 40.0
order_disagreement: false
outcome: confirmed
winner: team-lumen
adjudication_id: null
visibility: private
approval_state: approved
validation_state: valid
approved_by: head judging official
approved_at: "2026-05-18T17:30:00Z"
---

# Matchup Report — Lumen vs Verdant

## Eligibility and common evidence

Both teams carry a valid consolidated report at rubric `submission-evaluation@1.1.0`
and a pinned evidence package. Neither presentation order, bracket position,
affiliation nor previous placement was treated as evidence.

## Order-balanced results

<!-- atj:matchup:begin -->
| Criterion | Weight | A-first value | B-first normalized | Combined margin | Order |
|---|---:|---:|---:|---:|---|
| functional | 25 | +1 | +1 | +12.50 | consistent |
| product | 15 | +1 | +1 | +7.50 | consistent |
| agentic | 15 | +0 | +0 | +0.00 | consistent |
| engineering | 15 | +2 | +2 | +15.00 | consistent |
| reliability | 10 | +1 | +1 | +5.00 | consistent |
| security | 10 | +0 | +0 | +0.00 | consistent |
| innovation | 10 | +0 | +0 | +0.00 | consistent |

- A-first pass margin: **+40.00** (picked team-lumen)
- B-first pass margin, normalized: **+40.00** (picked team-lumen)
- Combined margin: **+40.00** on a −100…+100 scale (positive favours team-lumen)
- Close-call band: ±5
- Outcome: **confirmed**, winner **team-lumen**
<!-- atj:matchup:end -->

## Margin and outcome

Consistent across both presentation orders and decisively outside the band.

## Decisive evidence

- Lumen: Explicit state machine for handover status with exhaustive transition tests. (ev-lumen-01)
- Verdant: Honest uncertainty handling: alerts show confidence and can be dismissed. (ev-verdant-01)

## Conflicting evidence

None: both presentation orders reached the same comparative finding on every criterion.

## Tie-break or adjudication

Not required. Both passes selected the same team and the combined margin cleared the close-call band.

## Audit

- [x] Both passes were independent
- [x] Presentation order was reversed
- [x] Every nonzero comparison cites evidence
- [x] No prohibited team metadata influenced judgment
