---
event_id: sample-mock-2026
event_name: Sample Mock Event 2026
status: closed
rubric: submission-evaluation@1.0.0
consolidation_policy: panel-consolidation@1.0.0
matchup_rubric: head-to-head@1.0.0
bracket_policy: bracket-assignment@1.0.0
bye_policy: performance-qualified
close_call_band: 5.0
expected_judges:
- judge-backend
- judge-frontend-ux
- judge-security-ops
- judge-product-agentic
public_scores: false
execution_mode: disabled
network_allowlist: []
framework_commit: uncommitted
model_requested: not-applicable (scripted fixture)
model_used: not-applicable (scripted fixture)
started_at: "2026-05-18T09:00:00Z"
completed_at: "2026-05-18T17:30:00Z"
visibility: private
approval_state: approved
validation_state: valid
officials:
  disqualification: head judging official
  adjudication: head judging official
  publication_approval: head judging official
  security_escalation: head judging official
---
# Sample Mock Event 2026

**This is a synthetic fixture.** Every team, project, school and commit below is
invented. No real student, submission or institution appears anywhere in this
event. It exists so the complete workflow can be run, inspected and regression
tested without touching real work.

## Purpose

Demonstrate one full event from intake to ceremony output, including the cases
that are awkward rather than the ones that are easy: an unresolved `NE`, a
material disagreement, a severe disagreement with an outlier, a close-call
matchup, and an audit that fails and is then repaired.

## Schedule

| Milestone | Date and time | Owner |
|---|---|---|
| Submission freeze | 2026-05-18T09:00:00Z | head judging official |
| Initial judging complete | 2026-05-18T13:00:00Z | head judging official |
| Bracket frozen | 2026-05-18T14:00:00Z | head judging official |
| Ceremony | 2026-05-18T17:30:00Z | head judging official |

## Eligibility and human officials

All four synthetic teams are eligible. Disqualification, rules exceptions,
unresolved ties, security escalation and publication approval belong to the
head judging official. Two of those authorities were exercised in this event and are
recorded in `adjudications/`.

## Execution environment

`execution_mode: disabled`. No container runtime was verified on the host that
produced this fixture, so no submission was executed. Evidence is static
inspection and team-supplied artifacts only. Criteria whose evidence would
normally come from running the software are scored from inspected implementation
where that is sufficient, and `NE` where it is not.

## Model disclosure

Judge scores in this fixture are **scripted**, not model output, so the pipeline
is reproducible in continuous integration. Every artifact records
`model_used: not-applicable (scripted fixture)`. A real event records the model that actually ran.
