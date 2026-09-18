---
event_id: sample-mock-2026
team_id: team-verdant
commit: 57435ce0f24aacf5d49e41d78225d67882eccf91
evidence_package_id: ev:sample-mock-2026:team-verdant:57435ce0f24a:e015944d
rubric: submission-evaluation@1.0.0
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

# Evidence Manifest — Verdant

## Scope and provenance

Pinned to synthetic commit `57435ce0f24aacf5d49e41d78225d67882eccf91`. Prepared by the `prepare-submission`
skill against the frozen rubric. All content below is invented for this fixture.

## Requirements and team claims

| ID | Claim or requirement | Source | Evidence status |
|---|---|---|---|
| req-01 | A campus energy dashboard with anomaly alerts over meter data. | team statement | partially demonstrated |
| req-02 | Honest uncertainty handling: alerts show confidence and can be dismissed. | team statement | demonstrated |
| req-03 | No known blocking defect | team statement | contradicted |

## Direct observations

| Evidence ID | Class | Observation |
|---|---|---|
| ev-verdant-01 | direct-observation | Alert confidence is shown and dismissals persist. |
| ev-verdant-02 | artifact | src/ingest.py:14 hard-codes the meter endpoint. |
| ev-verdant-03 | direct-observation | A failed ingest leaves the dashboard silently stale. |
| ev-verdant-04 | artifact | Nine integration tests cover the alerting path. |

## Tests and execution

| Command or scenario | Result | Output artifact | Safety controls |
|---|---|---|---|
| (none) | not run | none | `atj sandbox preflight` reported no verified isolation |

## Relevant implementation evidence

| Evidence ID | Path/symbol | Relevance |
|---|---|---|
| ev-verdant-02 | see the observation table | primary implementation evidence |

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
