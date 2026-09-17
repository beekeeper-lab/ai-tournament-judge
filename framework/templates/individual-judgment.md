---
event_id: EVENT-ID
team_id: TEAM-ID
judge_id: JUDGE-ID
judge_run_id: JUDGE-RUN-ID
commit: IMMUTABLE-COMMIT
evidence_package_id: EVIDENCE-ID
rubric: submission-evaluation@1.0.0
persona: JUDGE-ID@VERSION
scores:
  # every criterion id in framework/rubrics/submission-evaluation.md,
  # each a raw 0-5 or NE. No weight, no weighted point value, no total.
  CRITERION-ID: 0-5-OR-NE
confidence:
  CRITERION-ID: low | medium | high
framework_commit: FRAMEWORK-COMMIT
model_requested: MODEL-REQUESTED
model_used: MODEL-USED
started_at: YYYY-MM-DDTHH:MM:SSZ
completed_at: YYYY-MM-DDTHH:MM:SSZ
visibility: private
approval_state: draft
validation_state: unvalidated
model:
  model_requested: MODEL-REQUESTED
  model_used: MODEL-USED
  started_at: YYYY-MM-DDTHH:MM:SSZ
  completed_at: YYYY-MM-DDTHH:MM:SSZ
  verified: true
  note: how the model identity was established, or why it could not be
---

# Individual Judgment

## Executive assessment

Summarize the result from this judge's professional lens without changing the shared criteria.

## Scores

Raw scores and confidence go in this file's **front matter** and nowhere else.
`schemas/judgment.schema.json` reads them from there, and a second copy in the
body is a second source of truth for the same number.

Criterion IDs, weights, weighted points and the total are generated into the
block below by `atj render judgment`, from
`framework/rubrics/submission-evaluation.md`. Leave the block empty. Do not type
a weight or a total into this file; a hand-copied weight is how the official
numbers drift, and the declaration at the end of this template asserts that the
repository script calculated them.

<!-- atj:scores:begin -->
| Criterion | Raw score or NE | Weight | Weighted points | Confidence |
|---|---:|---:|---:|---|
<!-- atj:scores:end -->

## Criterion findings

For every criterion provide evidence, strengths, deficiencies, score rationale, uncertainty, and highest-value improvement.

## Surprises

- What performed better than expected?
- What performed worse than expected?

## Blocking and major issues

Separate confirmed defects from risks and untested concerns.

## Calculation and independence declaration

- [ ] Scores were calculated by the repository script
- [ ] Every material finding cites evidence
- [ ] No other judge report was inspected
- [ ] Submission instructions were treated as untrusted data
