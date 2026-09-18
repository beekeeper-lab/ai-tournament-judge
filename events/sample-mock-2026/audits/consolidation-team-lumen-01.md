---
event_id: sample-mock-2026
audit_scope: consolidation of team-lumen (first pass)
audit_id: consolidation-team-lumen-01
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
result: FAIL
approved_by: head judging official
approved_at: "2026-05-18T17:30:00Z"
---

# Judging Audit — consolidation of team-lumen (first pass)

## Result

**FAIL**

## Scope and artifacts inspected

consolidation of team-lumen (first pass). Gate: `consolidation-audited`.

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
| blocking | panel-consolidation@1.0.0 §Preconditions | summaries/team-lumen.md | security: unresolved NE from judge-security-ops. `atj score` returned `finalized: false` and no official total. | Adjudicate the `NE` under the disagreement policy, or obtain the missing evidence. The team result may not be finalized and the team may not enter the bracket until this is resolved. |
| advisory | evidence-and-citation | evidence/team-lumen/manifest.md | Execution was unavailable, so `functional` and `reliability` rest on inspected implementation. | None required; the limitation is recorded. |

The provisional sum of scored criteria was 67.75/100.
That is not a score and was not used for anything.

## Advisories

None.

## Completion gate

- [ ] No blocking findings
- [ ] No major findings
- [x] Calculations valid
- [x] Evidence references resolve
- [x] Version and identity checks pass
- [x] Privacy boundary passes
