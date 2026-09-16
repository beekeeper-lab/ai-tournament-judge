---
name: audit-judging-run
description: Audits one team, stage, round, or event for completeness, evidence support, calculation integrity, safety, and privacy.
---

# Audit Judging Run

Select the narrowest requested scope and invoke the `judging-auditor` agent with the relevant configuration, rubric, policies, templates, and artifacts.

Run `python3 -m atj event validate <event>`, `python3 -m atj validate reports <event>`, and `python3 -m atj release-check`. Recalculate official scores with `atj score` rather than trusting a displayed total, and re-verify the bracket with `atj bracket verify --reproduce`. Check source commit and version consistency, required judge independence, evidence citations, disagreement handling, bracket constraints, status transitions, and publication boundaries.

Write an audit report using the audit template. A blocking or major unresolved finding produces FAIL. Do not advance status until a subsequent audit verifies repairs.
