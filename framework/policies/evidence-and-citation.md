# Evidence and Citation Policy

Every material conclusion must be traceable to the pinned evidence package.

## Evidence classes

1. **Direct observation:** witnessed behavior, captured output, test result, or inspected implementation.
2. **Artifact evidence:** source file, configuration, requirement, screenshot, recording, or log tied to the submission.
3. **Team claim:** statement in documentation or presentation that has not been independently demonstrated.
4. **Inference:** evaluator conclusion derived from identified evidence.

Reports must distinguish these classes. Team claims alone may explain intent but do not prove behavior. Cite repository-relative paths and line or symbol when practical; cite artifact IDs for non-code evidence. Never cite mutable branch state in place of the recorded commit.

## Model identity

`model.verified` is a claim about provenance, and the same evidence classes apply
to it. Record `true` only when the model identity came from outside the model's
own statement: the orchestrator's run record, the harness-reported model
identifier, or a recorded API response. That is direct observation.

Record `false` when the only available source is the model asserting its own
identity. A model's self-report is a team claim, one level removed — it may be
accurate and it is not independently established. Say which source was available
in `note` either way.

There is no `NE` for this field, because the question is never unanswerable:
either an external source exists or it does not.

Four judges in `live-trial-2026` recorded `model.verified` on identical grounds
and split three to one, because nothing defined the threshold.

Use `NE` when required evidence is unavailable. Do not manufacture certainty or treat absence of evidence as proof of failure unless the submission was explicitly required to provide that evidence.
