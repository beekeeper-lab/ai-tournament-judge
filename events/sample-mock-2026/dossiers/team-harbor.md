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
persona: build-team-dossier@1.0.0
source_reports:
- summaries/team-harbor.md
- evidence/team-harbor/manifest.md
visibility: team
approval_state: approved
validation_state: valid
---
# Team Dossier — Harbor

## Your project at a glance

An incident-timeline builder that assembles a narrative from logs.

Overall panel result: **53.3 / 100**.

## What you did especially well

Novel log-correlation approach that groups events by causal proximity. This was the clearest thing the panel agreed on, and it is worth
keeping as the project grows.

## Criterion feedback

| Criterion | Panel mean | What that reflects |
|---|---|---|
| Functional correctness and completeness | 2.75 / 5 | Solid for the event; the expectations for this criterion were met. |
| Product value and usability | 3.00 / 5 | Solid for the event; the expectations for this criterion were met. |
| Agentic and AI system design | 3.00 / 5 | Solid for the event; the expectations for this criterion were met. |
| Engineering and maintainability | 2.00 / 5 | The weakest area; see the improvement plan. |
| Reliability, testing, and observability | 2.00 / 5 | The weakest area; see the improvement plan. |
| Security, privacy, and responsible AI | 3.00 / 5 | Solid for the event; the expectations for this criterion were met. |
| Innovation and technical ambition | 2.75 / 5 | Judges differed sharply here; the panel mean is reported and the disagreement was reviewed by an official. |

## Tournament journey

- **Semifinal** against Quill: you did not advance. The comparison turned on **functional**. Your evidence there did not carry the comparison; your own criterion feedback above says what would have.

## Blocking issues

- Correlation is unvalidated; the demo timeline is hand-curated.

## Recommended improvement plan

1. **Immediate repair.** Correlation is unvalidated; the demo timeline is hand-curated. Fix this first; it is the one confirmed
   defect that affects how the rest of the work is read.
2. **Highest-value next iteration.** Demonstrate the behaviour you described but
   did not show. A claim with a test or a captured run behind it scores
   differently from the same claim on its own.
3. **Longer-term opportunity.** Novel log-correlation approach that groups events by causal proximity is a real strength —
   extend it to the parts of the system that do not yet have it.

## Evidence appendix

| Evidence ID | Class | Observation |
|---|---|---|
| ev-harbor-01 | artifact | src/correlate.py groups by timestamp proximity only. |
| ev-harbor-02 | direct-observation | The demo timeline file is committed, not generated. |
| ev-harbor-03 | direct-observation | Two of nine documented workflows complete. |
| ev-harbor-04 | artifact | No tests cover the correlation heuristic. |

These are the observations the panel worked from. Everything here is traceable
to your submitted commit.
