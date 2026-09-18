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
persona: build-team-dossier@1.0.0
source_reports:
- summaries/team-verdant.md
- evidence/team-verdant/manifest.md
visibility: team
approval_state: approved
validation_state: valid
approved_by: head judging official
approved_at: "2026-05-18T17:30:00Z"
---

# Team Dossier — Verdant

## Your project at a glance

A campus energy dashboard with anomaly alerts over meter data.

Overall panel result: **59.8 / 100**.

## What you did especially well

Honest uncertainty handling: alerts show confidence and can be dismissed. This was the clearest thing the panel agreed on, and it is worth
keeping as the project grows.

## Criterion feedback

| Criterion | Panel mean | What that reflects |
|---|---|---|
| Functional correctness and completeness | 3.00 / 5 | Solid for the event; the expectations for this criterion were met. |
| Product value and usability | 3.00 / 5 | Solid for the event; the expectations for this criterion were met. |
| Agentic and AI system design | 3.25 / 5 | Solid for the event; the expectations for this criterion were met. |
| Engineering and maintainability | 3.00 / 5 | Solid for the event; the expectations for this criterion were met. |
| Reliability, testing, and observability | 2.50 / 5 | Solid for the event; the expectations for this criterion were met. |
| Security, privacy, and responsible AI | 3.00 / 5 | Solid for the event; the expectations for this criterion were met. |
| Innovation and technical ambition | 3.00 / 5 | Solid for the event; the expectations for this criterion were met. |

## Tournament journey

- **Semifinal** against Lumen: you did not advance. The comparison turned on **engineering**. Your evidence there did not carry the comparison; your own criterion feedback above says what would have.

## Blocking issues

- Single hard-coded data source; ingestion fails closed with no operator signal.

## Recommended improvement plan

1. **Immediate repair.** Single hard-coded data source; ingestion fails closed with no operator signal. Fix this first; it is the one confirmed
   defect that affects how the rest of the work is read.
2. **Highest-value next iteration.** Demonstrate the behaviour you described but
   did not show. A claim with a test or a captured run behind it scores
   differently from the same claim on its own.
3. **Longer-term opportunity.** Honest uncertainty handling: alerts show confidence and can be dismissed is a real strength —
   extend it to the parts of the system that do not yet have it.

## Evidence appendix

| Evidence ID | Class | Observation |
|---|---|---|
| ev-verdant-01 | direct-observation | Alert confidence is shown and dismissals persist. |
| ev-verdant-02 | artifact | src/ingest.py:14 hard-codes the meter endpoint. |
| ev-verdant-03 | direct-observation | A failed ingest leaves the dashboard silently stale. |
| ev-verdant-04 | artifact | Nine integration tests cover the alerting path. |

These are the observations the panel worked from. Everything here is traceable
to your submitted commit.
