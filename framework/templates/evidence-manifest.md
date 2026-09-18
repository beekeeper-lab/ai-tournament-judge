---
event_id: EVENT-ID
team_id: TEAM-ID
commit: IMMUTABLE-COMMIT
evidence_package_id: EVIDENCE-ID
rubric: submission-evaluation@1.1.0
persona: prepare-submission@VERSION
framework_commit: FRAMEWORK-COMMIT
model_requested: MODEL-REQUESTED
model_used: MODEL-USED
started_at: YYYY-MM-DDTHH:MM:SSZ
completed_at: YYYY-MM-DDTHH:MM:SSZ
prepared_at: YYYY-MM-DDTHH:MM:SSZ
execution_status: not-run
execution_record: null
evidence_limited_criteria: []
visibility: private
approval_state: draft
validation_state: unvalidated
---

# Evidence Manifest

## Scope and provenance

Record source location, commit verification, preparer, rubric version, and environment.

## Requirements and team claims

Give every row an ID (`R1`, `R2`, …) and cite the observations it rests on as
`[[evidence:ID]]`. A citation is checked from both ends: each observation below
must independently claim to support the requirement that cites it.

| ID | Claim or requirement | Source | Evidence status |
|---|---|---|---|

## Direct observations

`Supports` lists the requirement IDs this observation establishes, or `-` when it
deliberately supports none. It is not a restatement of the requirements table: the
two are written independently and `atj validate reports` asserts they agree.
Evidence audit round 1 of live-trial-2026 found nine requirement rows citing an
observation that said nothing about them, and validation reported no findings at
all, because every id resolved. Resolving is all a schema can see.

| Evidence ID | Observation | Supports | Artifact or source reference | Reproduction | Confidence |
|---|---|---|---|---|---|

## Tests and execution

| Command or scenario | Result | Output artifact | Safety controls |
|---|---|---|---|

## Relevant implementation evidence

| Evidence ID | Path/symbol | Relevance |
|---|---|---|

## Missing or inaccessible evidence

List evidence gaps and the conclusions they limit.

## Validation

- [ ] Immutable commit verified
- [ ] Untrusted instructions ignored
- [ ] Execution policy satisfied or execution omitted
- [ ] Artifact references resolve
- [ ] Manifest independently validated
