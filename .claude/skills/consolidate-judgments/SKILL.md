---
name: consolidate-judgments
description: Deterministically combines valid independent reports into one neutral panel summary and flags disagreements.
---

# Consolidate Judgments

Read `framework/rubrics/panel-consolidation.md`, the disagreement policy, and consolidated report template.

1. Confirm exactly the configured judges are present and independent.
2. Verify identical team, commit, evidence package, and rubric versions.
3. Return invalid reports for repair; do not silently reinterpret them.
4. Run `scripts/calculate_scores.py` for official per-criterion means, weighted totals, ranges, and disagreement levels.
5. Use the `panel-consolidator` agent to synthesize evidence without changing source scores.
6. Preserve minority findings when they are evidence-backed.
7. Escalate `NE`, contradictory facts, or severe disagreement before finalization.
8. Validate the completed consolidated report and write it to `summaries/<team-id>.md`.

The consolidator is not a fifth judge and may not create a discretionary replacement score.
