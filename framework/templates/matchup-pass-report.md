---
event_id: EVENT-ID
match_id: MATCH-ID
round_id: ROUND-ID
team_a: TEAM-A
team_b: TEAM-B
commit_a: IMMUTABLE-COMMIT-A
commit_b: IMMUTABLE-COMMIT-B
evidence_package_a: EVIDENCE-ID-A
evidence_package_b: EVIDENCE-ID-B
rubric: head-to-head@1.0.0
source_rubric: submission-evaluation@1.0.0
persona: matchup-judge@VERSION
framework_commit: FRAMEWORK-COMMIT
model_requested: MODEL-REQUESTED
model_used: MODEL-USED
started_at: YYYY-MM-DDTHH:MM:SSZ
completed_at: YYYY-MM-DDTHH:MM:SSZ
close_call_band: 5
presentation_order: a-first
passes:
  a_first:
    presented_first: TEAM-A
    comparisons: {}
  b_first:
    presented_first: TEAM-B
    comparisons: {}
combined_margin: null
order_disagreement: false
outcome: null
winner: null
adjudication_id: null
visibility: private
approval_state: draft
validation_state: unvalidated
---

# Matchup Pass Report

One pass of an order-balanced comparison, in one presentation order, written
without sight of the other pass. Fill the `comparisons` block that matches
`presentation_order` and leave the other one empty: the schema requires exactly
one populated block, because an entry in both would mean a single judge produced
both passes and order balancing bought nothing.

`combined_margin`, `winner` and `outcome` stay null here. They belong to
`atj matchup`, which reads both passes and resolves them. Nothing in this
artifact is an official result, and `atj validate publication` refuses it: a pass
report is panel-private and never a disclosure source.

## Eligibility and common evidence

Confirm both teams are eligible, both submissions are pinned, and both evidence
packages are approved and valid. Name the common evidence you compared on. Do
not compare initial totals; the head-to-head rubric forbids selecting on them.

## Order-balanced results

| Criterion | Weight | Value in this pass | Evidence |
|---|---:|---:|---|

## Margin and outcome

- Presentation order judged:
- Populated pass block:
- Margin: resolved by `atj matchup`, not stated here
- Close-call threshold:

## Decisive evidence

## Conflicting evidence

## Tie-break or adjudication

State what a tie-break would turn on if this pass were decisive. Do not apply
one: the tie-break order lives in `framework/rubrics/head-to-head.md` and is
applied once, over both passes.

## Audit

- [ ] This pass was judged without sight of the other pass
- [ ] Only the block matching `presentation_order` carries comparisons
- [ ] Every nonzero comparison cites evidence
- [ ] No prohibited team metadata influenced judgment
- [ ] No official number was computed in this artifact
