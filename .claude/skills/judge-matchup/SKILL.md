---
name: judge-matchup
description: Performs an order-balanced head-to-head comparison, resolves close outcomes, and produces private and public reports.
---

# Judge Matchup

Read the head-to-head rubric, evidence policy, both teams' valid consolidated and individual reports, and both original evidence manifests.

1. Verify both teams use the same rubric version and are eligible for this match.
2. Invoke `matchup-judge` with Team A first and Team B second.
3. Invoke a fresh `matchup-judge` context with Team B first and Team A second. Do not expose the first result.
4. Validate both reports, then calculate margins with `python3 -m atj matchup <input.json>`. It normalizes the B-first pass into A/B orientation; never do that by hand.
5. `atj matchup` returns `outcome: confirmed` with a winner, or `outcome: adjudication-required` with `winner: null`. There is no third result and no winner to advance in the second case.
6. Apply the documented tie-break or neutral human adjudication when passes conflict or the margin is inside the close-call band.
7. Write the private matchup report, then generate the public summary and gate it with `python3 -m atj validate publication <artifact> --event-dir <event>`. It must name an approving official and list its source artifacts.
8. Audit before advancing the bracket.

Never use school, historical placement, bracket convenience, popularity, or presentation order as judging evidence.
