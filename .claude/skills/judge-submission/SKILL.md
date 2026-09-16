---
name: judge-submission
description: Runs the four independent submission judges, consolidates valid reports, and audits one team's result.
---

# Judge Submission

Use only a validated evidence manifest pinned to the event rubric version and source commit.

## Workflow

1. Confirm the team is eligible and intake is complete.
2. Create four independent tasks using `judge-backend`, `judge-frontend-ux`, `judge-security-ops`, and `judge-product-agentic`.
3. Give each task the same evidence manifest, submission rubric, evidence policy, and individual report template. Do not give it other judge reports.
4. Save returned reports under `judgments/<team-id>/`.
5. Validate required sections, evidence references, rubric version, commit, and score range.
6. Repair malformed output through the originating judge; do not have the orchestrator invent missing judgment.
7. Invoke `consolidate-judgments` only after all four reports are valid.
8. Invoke `audit-judging-run` for the team result. Update event status only after PASS or PASS WITH ADVISORIES.

Never parallelize tasks in a way that shares one judge's conclusions with another. An `NE`, severe disagreement, or factual contradiction remains visible and follows adjudication policy.
