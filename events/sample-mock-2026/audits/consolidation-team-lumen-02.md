---
event_id: sample-mock-2026
audit_scope: consolidation of team-lumen (after adjudication)
audit_id: consolidation-team-lumen-02
team_id: team-lumen
match_id: null
commit: 1d46525edc7a377a802930091df18ad921262657
evidence_package_id: ev:sample-mock-2026:team-lumen:1d46525edc7a:7c194426
rubric: submission-evaluation@1.1.0
persona: judging-auditor@1.1.0
framework_commit: uncommitted
model_requested: not-applicable (scripted fixture)
model_used: not-applicable (scripted fixture)
started_at: "2026-05-18T09:00:00Z"
completed_at: "2026-05-18T17:30:00Z"
visibility: private
approval_state: approved
validation_state: valid
result: PASS
approved_by: head judging official
approved_at: "2026-05-18T17:30:00Z"
---

# Judging Audit — consolidation of team-lumen (after adjudication)

## Result

**PASS**

## Scope and artifacts inspected

consolidation of team-lumen (after adjudication). Gate: `consolidation-audited`.

## Deterministic validation results

```
python3 -m atj event validate events/sample-mock-2026
python3 -m atj validate reports events/sample-mock-2026
python3 -m atj bracket verify events/sample-mock-2026/bracket.json --event-dir events/sample-mock-2026
python3 -m atj release-check
```

Official numbers were recalculated rather than read from the reports.

## Findings

| Severity | Rule | Artifact | Finding | Required repair |
|---|---|---|---|---|
| — | — | — | The blocking finding from `consolidation-team-lumen-01` is repaired. | — |

The adjudication recorded in
`adjudications/adj-sample-mock-2026-team-lumen-security-01.md`
resolved the `NE`. `atj score` now returns `finalized: true` with an official
total of 73.3/100. No individual judge score was modified;
the resolution is recorded alongside them.

## Advisories

None.

## Completion gate

- [x] No blocking findings
- [x] No major findings
- [x] Calculations valid
- [x] Evidence references resolve
- [x] Version and identity checks pass
- [x] Privacy boundary passes
