---
event_id: sample-mock-2026
team_id: team-lumen
commit: 1d46525edc7a377a802930091df18ad921262657
evidence_package_id: ev:sample-mock-2026:team-lumen:1d46525edc7a:7c194426
rubric: submission-evaluation@1.0.0
framework_commit: uncommitted
model_requested: not-applicable (scripted fixture)
model_used: not-applicable (scripted fixture)
started_at: "2026-05-18T09:00:00Z"
completed_at: "2026-05-18T17:30:00Z"
persona: build-team-dossier@1.0.0
source_reports:
- summaries/team-lumen.md
- evidence/team-lumen/manifest.md
visibility: team
approval_state: approved
validation_state: valid
---

# Team Dossier — Lumen

## Your project at a glance

A shift-handover tool for small clinics. Server-rendered, no framework.

Overall panel result: **73.3 / 100**.

## What you did especially well

Explicit state machine for handover status with exhaustive transition tests. This was the clearest thing the panel agreed on, and it is worth
keeping as the project grows.

## Criterion feedback

| Criterion | Panel mean | What that reflects |
|---|---|---|
| Functional correctness and completeness | 4.00 / 5 | A consistent strength across all four judges. |
| Product value and usability | 4.00 / 5 | A consistent strength across all four judges. |
| Agentic and AI system design | 3.00 / 5 | Solid for the event; the expectations for this criterion were met. |
| Engineering and maintainability | 4.25 / 5 | A consistent strength across all four judges. |
| Reliability, testing, and observability | 4.00 / 5 | A consistent strength across all four judges. |
| Security, privacy, and responsible AI | 2.75 / 5 | Solid for the event; the expectations for this criterion were met. |
| Innovation and technical ambition | 3.00 / 5 | Solid for the event; the expectations for this criterion were met. |

## Tournament journey

- **Semifinal** against Verdant: you advanced. The comparison turned on **engineering**, where your evidence was the stronger of the two.
- **Final** against Quill: you advanced. The comparison turned on **reliability**, where your evidence was the stronger of the two.

## Blocking issues

- Session handling stores a bare user id in a cookie with no signature.

## Recommended improvement plan

1. **Immediate repair.** Session handling stores a bare user id in a cookie with no signature. Fix this first; it is the one confirmed
   defect that affects how the rest of the work is read.
2. **Highest-value next iteration.** Demonstrate the behaviour you described but
   did not show. A claim with a test or a captured run behind it scores
   differently from the same claim on its own.
3. **Longer-term opportunity.** Explicit state machine for handover status with exhaustive transition tests is a real strength —
   extend it to the parts of the system that do not yet have it.

## Evidence appendix

| Evidence ID | Class | Observation |
|---|---|---|
| ev-lumen-01 | direct-observation | Handover transition tests pass: 41 of 41. |
| ev-lumen-02 | artifact | src/handover/state.py defines the transition table. |
| ev-lumen-03 | artifact | src/web/session.py:22 sets an unsigned `uid` cookie. |
| ev-lumen-04 | team-claim | README claims audit logging; no log sink is configured. |

These are the observations the panel worked from. Everything here is traceable
to your submitted commit.
