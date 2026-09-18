---
event_id: sample-mock-2026
team_id: team-lumen
commit: 1d46525edc7a377a802930091df18ad921262657
evidence_package_id: ev:sample-mock-2026:team-lumen:1d46525edc7a:7c194426
rubric: submission-evaluation@1.1.0
framework_commit: uncommitted
model_requested: not-applicable (scripted fixture)
model_used: not-applicable (scripted fixture)
started_at: "2026-05-18T09:00:00Z"
completed_at: "2026-05-18T17:30:00Z"
persona: prepare-submission@1.1.0
prepared_at: "2026-05-18T09:00:00Z"
execution_status: unavailable
execution_record: null
evidence_limited_criteria:
- functional
- reliability
visibility: private
approval_state: approved
validation_state: valid
---

# Evidence Manifest — Lumen

## Scope and provenance

Pinned to synthetic commit `1d46525edc7a377a802930091df18ad921262657`. Prepared by the `prepare-submission`
skill against the frozen rubric. All content below is invented for this fixture.

## Requirements and team claims

| ID | Claim or requirement | Source | Evidence status |
|---|---|---|---|
| req-01 | A shift-handover tool for small clinics. Server-rendered, no framework. | team statement | partially demonstrated — [[evidence:ev-lumen-01]] |
| req-02 | Explicit state machine for handover status with exhaustive transition tests. | team statement | demonstrated — [[evidence:ev-lumen-02]] |
| req-03 | No known blocking defect | team statement | contradicted — [[evidence:ev-lumen-03]] |

## Direct observations

| Evidence ID | Observation | Supports | Class |
|---|---|---|---|
| ev-lumen-01 | Handover transition tests pass: 41 of 41. | req-01 | direct-observation |
| ev-lumen-02 | src/handover/state.py defines the transition table. | req-02 | artifact |
| ev-lumen-03 | src/web/session.py:22 sets an unsigned `uid` cookie. | req-03 | artifact |
| ev-lumen-04 | README claims audit logging; no log sink is configured. | - | team-claim |

## Tests and execution

| Command or scenario | Result | Output artifact | Safety controls |
|---|---|---|---|
| (none) | not run | none | `atj sandbox preflight` reported no verified isolation |

## Relevant implementation evidence

| Evidence ID | Path/symbol | Relevance |
|---|---|---|
| ev-lumen-02 | see the observation table | primary implementation evidence |

## Missing or inaccessible evidence

No container runtime was available, so nothing was executed. `functional` and
`reliability` rest on inspected implementation and team-supplied artifacts, not
on observed behaviour. Where inspection was insufficient, judges recorded `NE`
rather than inferring a score.

## Validation

- [x] Immutable commit verified
- [x] Untrusted instructions ignored
- [x] Execution policy satisfied (execution omitted, limitation recorded)
- [x] Artifact references resolve
- [x] Manifest independently validated
