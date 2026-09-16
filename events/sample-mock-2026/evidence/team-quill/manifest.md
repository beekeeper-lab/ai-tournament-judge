---
event_id: sample-mock-2026
team_id: team-quill
commit: 1ff35a656b351b0529a7bc2d6b169aec650e1e71
evidence_package_id: ev:sample-mock-2026:team-quill:1ff35a656b35:f815c851
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
# Evidence Manifest — Quill

## Scope and provenance

Pinned to synthetic commit `1ff35a656b351b0529a7bc2d6b169aec650e1e71`. Prepared by the `prepare-submission`
skill against the frozen rubric. All content below is invented for this fixture.

## Requirements and team claims

| ID | Claim or requirement | Source | Evidence status |
|---|---|---|---|
| req-01 | A reading-list assistant that summarizes and tags saved articles. | team statement | partially demonstrated |
| req-02 | Keyboard-first interface with visible loading, empty and failure states. | team statement | demonstrated |
| req-03 | No known blocking defect | team statement | contradicted |

## Direct observations

| Evidence ID | Class | Observation |
|---|---|---|
| ev-quill-01 | direct-observation | Empty, loading and error states captured for the save flow. |
| ev-quill-02 | artifact | src/summarize.ts calls the model once with no retry or fallback. |
| ev-quill-03 | direct-observation | Keyboard traversal reaches every interactive control. |
| ev-quill-04 | inference | No evaluation harness is present in the repository. |

## Tests and execution

| Command or scenario | Result | Output artifact | Safety controls |
|---|---|---|---|
| (none) | not run | none | `atj sandbox preflight` reported no verified isolation |

## Relevant implementation evidence

| Evidence ID | Path/symbol | Relevance |
|---|---|---|
| ev-quill-02 | see the observation table | primary implementation evidence |

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
