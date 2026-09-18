---
event_id: sample-mock-2026
audit_scope: complete event record
audit_id: final-event
team_id: null
match_id: null
commit: 1d46525edc7a377a802930091df18ad921262657
evidence_package_id: ev:sample-mock-2026:team-lumen:1d46525edc7a:7c194426
rubric: submission-evaluation@1.0.0
persona: judging-auditor@1.0.0
framework_commit: uncommitted
model_requested: not-applicable (scripted fixture)
model_used: not-applicable (scripted fixture)
started_at: "2026-05-18T09:00:00Z"
completed_at: "2026-05-18T17:30:00Z"
visibility: private
approval_state: approved
validation_state: valid
result: PASS WITH ADVISORIES
---

# Judging Audit — complete event record

## Result

**PASS WITH ADVISORIES**

## Scope and artifacts inspected

complete event record. Gate: `final-audit-passed`.

## Deterministic validation results

```
python3 -m atj event validate events/sample-mock-2026
python3 -m atj validate reports events/sample-mock-2026
python3 -m atj bracket verify events/sample-mock-2026/bracket.json
python3 -m atj release-check
```

Official numbers were recalculated rather than read from the reports.

## Findings

| Severity | Rule | Artifact | Finding | Required repair |
|---|---|---|---|---|
| — | report-publication@1.0.0 | public/*.md | No public artifact carries a private-only field, a credential, a judge persona, a run id, an evidence package id or an unapproved score. Each names an approving official and lists its private sources. | — |
| — | judge-independence@1.0.0 | judgments/**/*.md | Sixteen judgments, four per team, distinct judge ids and distinct run ids, all pinned to the same team, commit, evidence package and rubric version. | — |

## Advisories

- No submission was executed anywhere in this event. Two criteria are
  evidence-limited for every team, and that is stated in each manifest and in
  the public judging-method disclosure.
- Judge scores in this fixture are scripted rather than model output. The
  fixture demonstrates the pipeline, not model behaviour.

## Completion gate

- [x] No blocking findings
- [x] No major findings
- [x] Calculations valid
- [x] Evidence references resolve
- [x] Version and identity checks pass
- [x] Privacy boundary passes
