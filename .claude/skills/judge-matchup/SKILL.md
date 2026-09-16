---
name: judge-matchup
description: Performs an order-balanced head-to-head comparison, resolves close outcomes, and produces private and public reports.
---

# Judge Matchup

Read the head-to-head rubric, evidence policy, both teams' valid consolidated and individual reports, and both original evidence manifests.

1. Verify both teams use the same rubric version and are eligible for this match.
2. Invoke `matchup-judge` with Team A first and Team B second.
3. Invoke a fresh `matchup-judge` context with Team B first and Team A second. Do not expose the first result.
4. Validate both reports and calculate margins deterministically.
5. Confirm a winner only when both passes agree and the confidence threshold is met.
6. Apply the documented tie-break or neutral human adjudication when passes conflict or the margin is inside the close-call band.
7. Write the private matchup report and a separately redacted public summary.
8. Audit before advancing the bracket.

Never use school, historical placement, bracket convenience, popularity, or presentation order as judging evidence.
