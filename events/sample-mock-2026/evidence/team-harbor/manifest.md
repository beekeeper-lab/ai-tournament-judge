---
event_id: sample-mock-2026
team_id: team-harbor
commit: 213a8d470271071a81322e41614345b87f67dd0c
evidence_package_id: ev:sample-mock-2026:team-harbor:213a8d470271:85a7e2cb
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
approved_by: head judging official
approved_at: "2026-05-18T17:30:00Z"
---

# Evidence Manifest — Harbor

## Scope and provenance

Pinned to synthetic commit `213a8d470271071a81322e41614345b87f67dd0c`. Prepared by the `prepare-submission`
skill against the frozen rubric. All content below is invented for this fixture.

## Requirements and team claims

| ID | Claim or requirement | Source | Evidence status |
|---|---|---|---|
| req-01 | An incident-timeline builder that assembles a narrative from logs. | team statement | partially demonstrated — [[evidence:ev-harbor-01]] |
| req-02 | Novel log-correlation approach that groups events by causal proximity. | team statement | demonstrated — [[evidence:ev-harbor-02]] |
| req-03 | No known blocking defect | team statement | contradicted — [[evidence:ev-harbor-03]] |

## Direct observations

| Evidence ID | Observation | Supports | Class |
|---|---|---|---|
| ev-harbor-01 | src/correlate.py groups by timestamp proximity only. | req-01 | artifact |
| ev-harbor-02 | The demo timeline file is committed, not generated. | req-02 | direct-observation |
| ev-harbor-03 | Two of nine documented workflows complete. | req-03 | direct-observation |
| ev-harbor-04 | No tests cover the correlation heuristic. | - | artifact |

## Tests and execution

| Command or scenario | Result | Output artifact | Safety controls |
|---|---|---|---|
| (none) | not run | none | `atj sandbox preflight` reported no verified isolation |

## Relevant implementation evidence

| Evidence ID | Path/symbol | Relevance |
|---|---|---|
| ev-harbor-02 | see the observation table | primary implementation evidence |

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
