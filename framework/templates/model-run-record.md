---
event_id: EVENT-ID
run_id: RUN-ID
component: COMPONENT-ID
component_version: COMPONENT-ID@VERSION
team_id: TEAM-ID
match_id: null
commit: IMMUTABLE-COMMIT
evidence_package_id: EVIDENCE-ID
rubric: submission-evaluation@1.1.0
persona: PERSONA@VERSION
framework_commit: FRAMEWORK-COMMIT
model_requested: MODEL-REQUESTED
model_used: MODEL-USED
verified: false
started_at: YYYY-MM-DDTHH:MM:SSZ
completed_at: YYYY-MM-DDTHH:MM:SSZ
visibility: private
approval_state: draft
validation_state: unvalidated
---

# Model Execution Record

Evidence trail for which model produced which artifact. Without it an award
cannot be defended if it is disputed.

## What ran

| Field | Value |
|---|---|
| Component | agent, skill, or command |
| Component version | from `framework/personas.md` |
| Model requested | the model the operator asked for |
| Model actually used | the model that actually ran |
| Verified | `true` only when the model in use was directly confirmed |
| Started / completed | UTC |

## Model substitution

If the model used differs from the model requested, record it here and mark
every dependent conclusion **unverified**. Do not silently downgrade a model.
A substitution is an event-official decision, not an operator convenience.

| Requested | Used | Reason | Who approved | Dependent artifacts |
|---|---|---|---|---|

## Cost and usage

| Metric | Value |
|---|---|
| Elapsed wall time | |
| Approximate token usage | |
| Retries | |

Record these as observed. An unmeasured value is blank, never estimated.

## Determinism statement

LLM judgment is **not** deterministic and this record does not claim it is. The
same model, prompt, and evidence may produce different wording and different
scores on different runs. Only calculation, validation, rendering, state
transitions, and seeded bracket assignment are deterministic in this framework.

## Validation

- [ ] Requested and used models both recorded
- [ ] `verified` is honest
- [ ] Substitutions approved and disclosed
- [ ] Timestamps present and ordered
- [ ] Linked artifacts resolve
