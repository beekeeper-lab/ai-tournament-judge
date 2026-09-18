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
4. Hold each returned report in the orchestrator's own context, or under
   `workspaces/<event>/staging/<team-id>/`, until **all four** have completed.
   Move them into `judgments/<team-id>/` only then. A judge's tool surface is
   read-only but not path-restricted, so a report written into the event
   directory while another judge is still running is a report that judge could
   read. Staging is what makes independence structural rather than instructed.
5. Run `python3 -m atj validate reports <event>` to check required sections, evidence references, rubric and persona versions, commit, evidence package, score range, and visibility.
6. Repair malformed output through the originating judge; do not have the orchestrator invent missing judgment.
7. Invoke `consolidate-judgments` only after all four reports are valid.
8. Invoke `audit-judging-run` for the team result. Update event status only after PASS or PASS WITH ADVISORIES.

Never parallelize tasks in a way that shares one judge's conclusions with another.
`atj validate reports` flags near-duplicate wording between two judgments on the
same team, which is the observable consequence of contamination; it is a detector,
not a guarantee. An `NE`, severe disagreement, or factual contradiction remains visible and follows adjudication policy.
