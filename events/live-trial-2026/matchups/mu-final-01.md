---
event_id: live-trial-2026
match_id: mu:live-trial-2026:final:01
round_id: final
team_a: team-ledger
team_b: team-podcast
commit_a: 9d21b7707f204ef60f5a1cee612f1d4db0a4a575
commit_b: f3fdd342465fa6bc2a52d226a8613b082ad329e0
evidence_package_a: ev:live-trial-2026:team-ledger:9d21b7707f20:b859a240
evidence_package_b: ev:live-trial-2026:team-podcast:f3fdd342465f:d06f90cc
rubric: head-to-head@1.0.0
source_rubric: submission-evaluation@1.0.0
persona: matchup-judge@1.0.0
framework_commit: 1e761e639141d099f975cd6b4e3efaa296e6602f
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-17T23:20:00Z"
completed_at: "2026-09-17T23:35:00Z"
close_call_band: 5.0
presentation_order: both
passes:
  a_first:
    presented_first: team-ledger
    comparisons: {agentic: 1, engineering: 1, functional: 1, innovation: 0, product: 0, reliability: 0, security: 1}
  b_first:
    presented_first: team-podcast
    comparisons: {agentic: -1, engineering: -1, functional: -1, innovation: -1, product: 0, reliability: 0, security: -1}
combined_margin: 35.0
order_disagreement: false
outcome: confirmed
winner: team-ledger
adjudication_id: null
visibility: private
approval_state: draft
validation_state: unvalidated
---

# Matchup Report

Resolved by `atj matchup` from the two order-balanced passes. Every number here is
read from `matchups/mu-final-01.json`; none was computed by hand. The judges' own
reports are in `events/live-trial-2026/matchup-passes/`; each judge worked without
sight of the other and neither computed a margin.

## Eligibility and common evidence

Both teams eligible, both packages `approved` and `valid`, both
`execution_status: sandboxed-partial`, both prepared by `prepare-submission@1.1.0`
under `submission-evaluation@1.0.0`. Initial totals were not used and are not
comparable: team-ledger is finalized at 76.3, team-podcast has no official total
because `reliability` is an accepted `NE` (`adj:live-trial-2026:team-podcast:01`).
`head-to-head.md` forbids selecting on initial totals and both passes recorded that
they did not.

The evidence asymmetry between the packages was created by the event, not the teams:
team-ledger's suite ran to completion, team-podcast's never did, for framework-imposed
reasons — a 64 MB tmpfs, a 64 MB `/dev/shm`, no `--shm-size`. Both passes named that
asymmetry and declined to convert it into a quality difference between the teams.

## Order-balanced results

| Criterion | Weight | A-first value | B-first normalized | Combined margin | Order |
|---|---:|---:|---:|---:|---|
| functional | 25 | +1 | +1 | +12.50 | consistent |
| product | 15 | +0 | +0 | +0.00 | consistent |
| agentic | 15 | +1 | +1 | +7.50 | consistent |
| engineering | 15 | +1 | +1 | +7.50 | consistent |
| reliability | 10 | +0 | +0 | +0.00 | consistent |
| security | 10 | +1 | +1 | +5.00 | consistent |
| innovation | 10 | +0 | +1 | +2.50 | consistent |

Positive favours **team-ledger**. The B-first pass was negated by `atj matchup` from
its `presented_first` field (`atj/matchup.py:42-70`), not by either judge.

## Margin and outcome

- A-first pass margin: **+32.50**, picked **team-ledger**
- B-first pass margin, normalized: **+37.50**, picked **team-ledger**
- Combined margin: **+35.00** on a -100..+100 scale
- Close-call band: +/-5.0
- Order disagreement: false
- Outcome: **confirmed**, winner **team-ledger**

The combined margin is seven times the close-call band, so the result confirms
automatically and no adjudication is required. `adjudication_reasons` is empty.

Both passes selected team-ledger independently and all seven criteria are
order-consistent. Both judges predicted qualitatively that the combined margin would
land near the close-call band. It did not. Neither judge computed a margin, which is
what the rubric requires of them, and the deterministic calculation matched neither
intuition — which is the case for keeping arithmetic in the tool.

## Decisive evidence

No criterion reached a decisive value of +/-2 in either pass. The result rests on four
meaningful advantages both passes agreed on — `functional`, `agentic`, `engineering`,
`security` — plus `innovation`, where the passes differed in magnitude (0 in A-first,
+1 normalized in B-first) without disagreeing in direction. The full evidence is in the
two pass reports and is not restated here.

`product` is 0 in both passes: each submission has one strong surface and one rough one,
and neither advantage is material.

## Conflicting evidence

Both passes recorded the same contested items and neither let one reading carry a
criterion: team-ledger's unconstrained `fin sql` surface, rated the top risk by two of
its judges and low impact by two others on the same code read; team-podcast's three
unclassified suite outcomes, where the environmental explanations and the missing
`worker.onerror` pull in opposite directions; and the classification split on
team-podcast's prune/cascade defect. Nothing was penetration-tested on either side.

## Tie-break or adjudication

Not reached. `tie_break_order` is `[functional, reliability, product]` and the combined
margin of +35.00 is far outside the close-call band, so resolution did not
require it. Both passes independently noted that `reliability` at 0 contributes no
tie-break signal for this pairing, as the adjudication anticipated; that observation did
not need to be applied.

## Audit

- [x] Both passes independent — neither judge read the other's work or anything under `matchups/`
- [x] Presentation order reversed — `a-first` presented team-ledger first, `b-first` presented team-podcast first
- [x] Normalization performed by the tool, not by a judge
- [x] Every nonzero comparison cites evidence — see the pass reports
- [x] No arithmetic performed by hand — every figure read from `mu-final-01.json`
- [x] Comparison values verified against each judge's own output before resolution — both matched exactly
- [x] Initial totals not used; team-podcast's accepted `NE` never treated as a deficiency
