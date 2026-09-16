---
name: audit-judging-run
description: Audits one team, stage, round, or event for completeness, evidence support, calculation integrity, safety, and privacy.
---

# Audit Judging Run

Select the narrowest requested scope and invoke the `judging-auditor` agent with the relevant configuration, rubric, policies, templates, and artifacts.

Run `scripts/validate_configuration.py` and `scripts/validate_reports.py` where applicable. Recalculate official scores rather than trusting displayed totals. Check source commit and version consistency, required judge independence, evidence citations, disagreement handling, bracket constraints, status transitions, and publication boundaries.

Write an audit report using the audit template. A blocking or major unresolved finding produces FAIL. Do not advance status until a subsequent audit verifies repairs.
