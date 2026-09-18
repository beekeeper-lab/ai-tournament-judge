---
event_id: sample-mock-2026
match_id: mu:sample-mock-2026:semifinal:01
round_id: semifinal
team_a: team-quill
team_b: team-harbor
commit_a: 1ff35a656b351b0529a7bc2d6b169aec650e1e71
commit_b: 213a8d470271071a81322e41614345b87f67dd0c
evidence_package_a: ev:sample-mock-2026:team-quill:1ff35a656b35:f815c851
evidence_package_b: ev:sample-mock-2026:team-harbor:213a8d470271:85a7e2cb
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
    presented_first: team-quill
    comparisons:
      functional: 1
      product: -1
      agentic: 0
      engineering: 0
      reliability: 0
      security: 0
      innovation: 0
  b_first:
    presented_first: team-harbor
    comparisons:
      functional: -1
      product: 1
      agentic: 0
      engineering: 0
      reliability: 0
      security: 0
      innovation: 0
combined_margin: 5.0
order_disagreement: false
outcome: adjudication-required
winner: null
adjudication_id: adj:sample-mock-2026:semifinal-2-close-call:01
visibility: private
approval_state: approved
validation_state: valid
---

# Matchup Report — Quill vs Harbor

## Eligibility and common evidence

Both teams carry a valid consolidated report at rubric `submission-evaluation@1.1.0`
and a pinned evidence package. Neither presentation order, bracket position,
affiliation nor previous placement was treated as evidence.

## Order-balanced results

<!-- atj:matchup:begin -->
| Criterion | Weight | A-first value | B-first normalized | Combined margin | Order |
|---|---:|---:|---:|---:|---|
| functional | 25 | +1 | +1 | +12.50 | consistent |
| product | 15 | -1 | -1 | -7.50 | consistent |
| agentic | 15 | +0 | +0 | +0.00 | consistent |
| engineering | 15 | +0 | +0 | +0.00 | consistent |
| reliability | 10 | +0 | +0 | +0.00 | consistent |
| security | 10 | +0 | +0 | +0.00 | consistent |
| innovation | 10 | +0 | +0 | +0.00 | consistent |

- A-first pass margin: **+5.00** (picked team-quill)
- B-first pass margin, normalized: **+5.00** (picked team-quill)
- Combined margin: **+5.00** on a −100…+100 scale (positive favours team-quill)
- Close-call band: ±5
- Outcome: **adjudication-required**

**Why this needs adjudication:**
- combined margin 5.0 is inside the close-call band of 5.0
<!-- atj:matchup:end -->

## Margin and outcome

A close call. Both orders favour the same team, but the combined margin of 5.0 sits exactly on the close-call band, so no winner is returned and a human official decides.

## Decisive evidence

- Quill: Keyboard-first interface with visible loading, empty and failure states. (ev-quill-01)
- Harbor: Novel log-correlation approach that groups events by causal proximity. (ev-harbor-01)

## Conflicting evidence

None: both presentation orders reached the same comparative finding on every criterion.

## Tie-break or adjudication

Required. The combined margin of +5.00 sits inside the ±5 band, so the framework returned no winner. See `adjudications/adj-sample-mock-2026-semifinal-2-close-call-01.md`, decided by a human official.

## Audit

- [x] Both passes were independent
- [x] Presentation order was reversed
- [x] Every nonzero comparison cites evidence
- [x] No prohibited team metadata influenced judgment
