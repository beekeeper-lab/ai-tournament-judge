---
event_id: sample-mock-2026
team_id: team-verdant
commit: 57435ce0f24aacf5d49e41d78225d67882eccf91
evidence_package_id: ev:sample-mock-2026:team-verdant:57435ce0f24a:e015944d
rubric: submission-evaluation@1.1.0
framework_commit: uncommitted
model_requested: not-applicable (scripted fixture)
model_used: not-applicable (scripted fixture)
started_at: "2026-05-18T09:00:00Z"
completed_at: "2026-05-18T17:30:00Z"
consolidation_policy: panel-consolidation@1.1.0
persona: panel-consolidator@1.1.0
judge_run_ids:
- jr:sample-mock-2026:team-verdant:judge-backend:e015944d:01
- jr:sample-mock-2026:team-verdant:judge-frontend-ux:e015944d:01
- jr:sample-mock-2026:team-verdant:judge-product-agentic:e015944d:01
- jr:sample-mock-2026:team-verdant:judge-security-ops:e015944d:01
total: 59.75
display_total: 59.8
finalized: true
blocked_reasons: []
adjudication_ids: []
visibility: private
approval_state: approved
validation_state: valid
---

# Consolidated Team Report — Verdant

## Executive summary

A campus energy dashboard with anomaly alerts over meter data. The panel's strongest agreement is on: Honest uncertainty handling: alerts show confidence and can be dismissed. Its
clearest shared concern is: Single hard-coded data source; ingestion fails closed with no operator signal.

The consolidator is a neutral packager, not a fifth judge. No individual score
below was altered.

## Consolidated score

<!-- atj:consolidated:begin -->
| Criterion | Judge scores | Mean | Weight | Points | Agreement |
|---|---|---:|---:|---:|---|
| functional | judge-backend=3.0, judge-frontend-ux=3.0, judge-product-agentic=3.0, judge-security-ops=3.0 | 3.00 | 25 | 15.00 | aligned |
| product | judge-backend=3.0, judge-frontend-ux=3.0, judge-product-agentic=3.0, judge-security-ops=3.0 | 3.00 | 15 | 9.00 | aligned |
| agentic | judge-backend=3.0, judge-frontend-ux=3.0, judge-product-agentic=4.0, judge-security-ops=3.0 | 3.25 | 15 | 9.75 | aligned |
| engineering | judge-backend=3.0, judge-frontend-ux=3.0, judge-product-agentic=3.0, judge-security-ops=3.0 | 3.00 | 15 | 9.00 | aligned |
| reliability | judge-backend=2.0, judge-frontend-ux=3.0, judge-product-agentic=3.0, judge-security-ops=2.0 | 2.50 | 10 | 5.00 | aligned |
| security | judge-backend=3.0, judge-frontend-ux=3.0, judge-product-agentic=3.0, judge-security-ops=3.0 | 3.00 | 10 | 6.00 | aligned |
| innovation | judge-backend=3.0, judge-frontend-ux=3.0, judge-product-agentic=3.0, judge-security-ops=3.0 | 3.00 | 10 | 6.00 | aligned |
| **Overall** |  |  | **100** | **59.8** |  |
<!-- atj:consolidated:end -->

## Confirmed strengths

- Honest uncertainty handling: alerts show confidence and can be dismissed.
- Evidence: Alert confidence is shown and dismissals persist.

## Confirmed weaknesses

- Single hard-coded data source; ingestion fails closed with no operator signal.
- Evidence: src/ingest.py:14 hard-codes the meter endpoint.

## Material disagreements

- None. Every criterion landed within the aligned band.

## Prioritized improvements

1. Repair the confirmed defect: Single hard-coded data source; ingestion fails closed with no operator signal.
2. Demonstrate the claimed behaviour that evidence did not establish.
3. Add the coverage that would have made the disputed criterion decidable.

## Unresolved questions and adjudication

None. No trigger threshold was crossed.

## Evidence index

| Evidence ID | Class | Observation |
|---|---|---|
| ev-verdant-01 | direct-observation | Alert confidence is shown and dismissals persist. |
| ev-verdant-02 | artifact | src/ingest.py:14 hard-codes the meter endpoint. |
| ev-verdant-03 | direct-observation | A failed ingest leaves the dashboard silently stale. |
| ev-verdant-04 | artifact | Nine integration tests cover the alerting path. |

## Calculation audit

- [x] Four valid independent reports
- [x] Identity and versions agree
- [x] Deterministic calculations attached
- [x] No unresolved `NE`
- [x] Required adjudication complete
