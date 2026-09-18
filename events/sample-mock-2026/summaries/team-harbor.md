---
event_id: sample-mock-2026
team_id: team-harbor
commit: 213a8d470271071a81322e41614345b87f67dd0c
evidence_package_id: ev:sample-mock-2026:team-harbor:213a8d470271:85a7e2cb
rubric: submission-evaluation@1.0.0
framework_commit: uncommitted
model_requested: not-applicable (scripted fixture)
model_used: not-applicable (scripted fixture)
started_at: "2026-05-18T09:00:00Z"
completed_at: "2026-05-18T17:30:00Z"
consolidation_policy: panel-consolidation@1.0.0
persona: panel-consolidator@1.0.0
judge_run_ids:
- jr:sample-mock-2026:team-harbor:judge-backend:85a7e2cb:01
- jr:sample-mock-2026:team-harbor:judge-frontend-ux:85a7e2cb:01
- jr:sample-mock-2026:team-harbor:judge-product-agentic:85a7e2cb:01
- jr:sample-mock-2026:team-harbor:judge-security-ops:85a7e2cb:01
total: 53.25
display_total: 53.3
finalized: true
blocked_reasons: []
adjudication_ids:
- adj:sample-mock-2026:team-harbor-innovation:01
visibility: private
approval_state: approved
validation_state: valid
---

# Consolidated Team Report — Harbor

## Executive summary

An incident-timeline builder that assembles a narrative from logs. The panel's strongest agreement is on: Novel log-correlation approach that groups events by causal proximity. Its
clearest shared concern is: Correlation is unvalidated; the demo timeline is hand-curated.

The consolidator is a neutral packager, not a fifth judge. No individual score
below was altered.

## Consolidated score

<!-- atj:consolidated:begin -->
| Criterion | Judge scores | Mean | Weight | Points | Agreement |
|---|---|---:|---:|---:|---|
| functional | judge-backend=2.0, judge-frontend-ux=3.0, judge-product-agentic=3.0, judge-security-ops=3.0 | 2.75 | 25 | 13.75 | aligned |
| product | judge-backend=3.0, judge-frontend-ux=3.0, judge-product-agentic=3.0, judge-security-ops=3.0 | 3.00 | 15 | 9.00 | aligned |
| agentic | judge-backend=3.0, judge-frontend-ux=3.0, judge-product-agentic=3.0, judge-security-ops=3.0 | 3.00 | 15 | 9.00 | aligned |
| engineering | judge-backend=2.0, judge-frontend-ux=2.0, judge-product-agentic=2.0, judge-security-ops=2.0 | 2.00 | 15 | 6.00 | aligned |
| reliability | judge-backend=2.0, judge-frontend-ux=2.0, judge-product-agentic=2.0, judge-security-ops=2.0 | 2.00 | 10 | 4.00 | aligned |
| security | judge-backend=3.0, judge-frontend-ux=3.0, judge-product-agentic=3.0, judge-security-ops=3.0 | 3.00 | 10 | 6.00 | aligned |
| innovation | judge-backend=2.0, judge-frontend-ux=2.0, judge-product-agentic=5.0, judge-security-ops=2.0 | 2.75 | 10 | 5.50 | severe-disagreement ⚑outlier |
| **Overall** |  |  | **100** | **53.3** |  |
<!-- atj:consolidated:end -->

## Confirmed strengths

- Novel log-correlation approach that groups events by causal proximity.
- Evidence: src/correlate.py groups by timestamp proximity only.

## Confirmed weaknesses

- Correlation is unvalidated; the demo timeline is hand-curated.
- Evidence: The demo timeline file is committed, not generated.

## Material disagreements

- **innovation** — severe-disagreement, range 3, possible outlier: judge-product-agentic. Cause: a difference in what each judge treated as demonstrated, not a factual contradiction. Resolution: recorded and preserved; the panel mean stands and the minority view is retained above.

## Prioritized improvements

1. Repair the confirmed defect: Correlation is unvalidated; the demo timeline is hand-curated.
2. Demonstrate the claimed behaviour that evidence did not establish.
3. Add the coverage that would have made the disputed criterion decidable.

## Unresolved questions and adjudication

Adjudications attached: adj:sample-mock-2026:team-harbor-innovation:01

## Evidence index

| Evidence ID | Class | Observation |
|---|---|---|
| ev-harbor-01 | artifact | src/correlate.py groups by timestamp proximity only. |
| ev-harbor-02 | direct-observation | The demo timeline file is committed, not generated. |
| ev-harbor-03 | direct-observation | Two of nine documented workflows complete. |
| ev-harbor-04 | artifact | No tests cover the correlation heuristic. |

## Calculation audit

- [x] Four valid independent reports
- [x] Identity and versions agree
- [x] Deterministic calculations attached
- [x] No unresolved `NE`
- [x] Required adjudication complete
