# Evidence and Citation Policy

Every material conclusion must be traceable to the pinned evidence package.

## Evidence classes

1. **Direct observation:** witnessed behavior, captured output, test result, or inspected implementation.
2. **Artifact evidence:** source file, configuration, requirement, screenshot, recording, or log tied to the submission.
3. **Team claim:** statement in documentation or presentation that has not been independently demonstrated.
4. **Inference:** evaluator conclusion derived from identified evidence.

Reports must distinguish these classes. Team claims alone may explain intent but do not prove behavior. Cite repository-relative paths and line or symbol when practical; cite artifact IDs for non-code evidence. Never cite mutable branch state in place of the recorded commit.

Use `NE` when required evidence is unavailable. Do not manufacture certainty or treat absence of evidence as proof of failure unless the submission was explicitly required to provide that evidence.
