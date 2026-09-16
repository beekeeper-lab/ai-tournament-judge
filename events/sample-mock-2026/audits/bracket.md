---
event_id: sample-mock-2026
audit_scope: bracket draw
audit_id: bracket
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
result: PASS
---
# Judging Audit — bracket draw

## Result

**PASS**

## Scope and artifacts inspected

bracket draw. Gate: `bracket-audited`.

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
| — | bracket-assignment@1.0.0 | bracket.md | Every hard constraint reports `satisfied`; the draw reproduces byte-for-byte from the recorded seed. | — |

## Advisories

None.

## Completion gate

- [x] No blocking findings
- [x] No major findings
- [x] Calculations valid
- [x] Evidence references resolve
- [x] Version and identity checks pass
- [x] Privacy boundary passes
