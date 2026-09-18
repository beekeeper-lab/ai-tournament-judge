---
rubric_id: head-to-head
version: 1.0.0
source_rubric: submission-evaluation@1.0.0
close_call_band: 5
order_balancing: required
tie_break_order: [functional, reliability, product]
---

# Head-to-Head Comparison Rubric

Compare the two teams directly using the seven source-rubric criteria and weights. Do not merely select the team with the higher initial total.

| Comparative finding | Value |
|---|---:|
| Team A decisive advantage | 2 |
| Team A meaningful advantage | 1 |
| Substantially equal or insufficient comparative evidence | 0 |
| Team B meaningful advantage | -1 |
| Team B decisive advantage | -2 |

`criterion_margin = comparison_value / 2 * criterion_weight`

The matchup margin ranges from -100 to 100. A decisive advantage requires material, outcome-relevant evidence; preference alone is insufficient.

## Procedure

Run two fresh comparisons: A then B, and B then A. Do not expose one pass to the other. Normalize the second result to the original A/B orientation. Both passes must select the same winner and the combined absolute margin must exceed the configured close-call band to confirm automatically.

When passes disagree, evidence is contradictory, or the result is inside the close-call band, use neutral human adjudication or the event's declared tie-break procedure.

## Tie-break order

Steps 1-3 are declared in this file's `tie_break_order` front matter and read
from there by `atj matchup`. Steps 4 and 5 need evidence or a decision the
tooling does not hold, and are referred to a human official.

1. Functional correctness and completeness
2. Reliability, testing, and observability
3. Product value and usability
4. Fewest confirmed critical security or data risks
5. Neutral live challenge or human decision

Do not consider school, previous placement, bracket path, popularity, team identity, presentation order, or ceremony convenience. Provide evidence for every nonzero comparison and create separate private and public reports.
