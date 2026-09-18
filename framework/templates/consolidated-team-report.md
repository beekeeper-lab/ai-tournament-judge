---
event_id: EVENT-ID
team_id: TEAM-ID
commit: IMMUTABLE-COMMIT
evidence_package_id: EVIDENCE-ID
rubric: submission-evaluation@1.1.0
consolidation_policy: panel-consolidation@1.1.0
persona: panel-consolidator@VERSION
framework_commit: FRAMEWORK-COMMIT
judge_run_ids: []
model_requested: MODEL-REQUESTED
model_used: MODEL-USED
started_at: YYYY-MM-DDTHH:MM:SSZ
completed_at: YYYY-MM-DDTHH:MM:SSZ
total: null
display_total: null
finalized: false
blocked_reasons: []
adjudication_ids: []
visibility: private
approval_state: draft
validation_state: unvalidated
---

# Consolidated Team Report

## Executive summary

## Consolidated score

Generate this block with `atj render consolidated <this file>`. It consolidates
the team's individual judgments through the canonical rubric and writes the table
below, together with `total`, `display_total`, `finalized` and `blocked_reasons`
in the front matter. Everything between the markers is the tool's output: do not
edit it, and do not transcribe it from `atj score`.

If you find yourself copying numbers into the table by hand, stop and say so in
`## Material disagreements`. A hand-built score block is not a generated one, and
a report that claims otherwise is making a false statement about its own
provenance.

<!-- atj:consolidated:begin -->
| Criterion | Judge scores | Mean | Weight | Points | Agreement |
|---|---|---:|---:|---:|---|
<!-- atj:consolidated:end -->

**Overall:** generated  
**Overall confidence:** generated

## Confirmed strengths

## Confirmed weaknesses

## Material disagreements

Explain cause, evidence on each side, and resolution status.

## Prioritized improvements

1. Highest-impact improvement
2. Second improvement
3. Third improvement

## Unresolved questions and adjudication

## Evidence index

## Calculation audit

- [ ] Four valid independent reports
- [ ] Identity and versions agree
- [ ] Deterministic calculations attached
- [ ] No unresolved `NE`
- [ ] Required adjudication complete
