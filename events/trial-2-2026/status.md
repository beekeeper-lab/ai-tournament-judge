---
event_id: trial-2-2026
current_stage: intake
last_updated: "2026-09-21T22:34:38Z"
blocked: false
blocked_reason: null
stage_gates:
  configuration-audited: passed
  roster-frozen: pending
  evidence-validated: pending
  judgments-audited: pending
  consolidation-audited: pending
  bracket-audited: pending
  tournament-audited: pending
  dossiers-approved: pending
  final-audit-passed: pending
units: []
gate_evidence:
  configuration-audited: audits/configuration.md
---

# Event Status

## Stage gates

- [ ] Configuration audited
- [ ] Roster frozen
- [ ] All eligible evidence packages validated
- [ ] All initial judgments audited
- [ ] All consolidated reports audited
- [ ] Bracket frozen and audited
- [ ] Tournament complete
- [ ] All team dossiers approved
- [ ] Final event audit passed
- [ ] Event marked complete

## Team progress

| Team ID | Intake | Evidence | Four judgments | Consolidated | Audited | Dossier |
|---|---|---|---|---|---|---|
| team-scribe | pinned `67969dd9` | — | — | — | — | — |
| team-demos | pinned `dc35f696` | — | — | — | — | — |

## Blockers and adjudications

| ID | Scope | Description | Owner | Status | Resolution artifact |
|---|---|---|---|---|---|

## Activity log

| Timestamp | Action | Input identity | Output | Audit result |
|---|---|---|---|---|
| 2026-09-21T21:51:56Z | `atj event init` trial-2-2026 | framework `ea0db07d` | event.md, status.md | not-audited |
| 2026-09-21T21:53:01Z | `atj intake` team-scribe | github.com/beekeeper-lab/ScribeVault @ `67969dd9` | submissions/team-scribe.md, workspaces/trial-2-2026/team-scribe | not-audited |
| 2026-09-21T22:04:10Z | `atj intake` team-demos | github.com/beekeeper-lab/ai-security-demos @ `dc35f696` | submissions/team-demos.md, workspaces/trial-2-2026/team-demos | not-audited |
| 2026-09-21T22:08:00Z | Configuration audit, first pass (reconstructed time; see the audit's F19) | event.md, teams.md, submissions/*.md, both checkouts | audits/configuration.md | FAIL |
| 2026-09-21T22:18:08Z | Configuration repaired, round one: F1 test count, F2 unmaterialized gitlink, F3 checkout containment, F5-F9; F4 and F8 repaired in the framework | audits/configuration.md F1-F9 | event.md, submissions/*.md, atj/intake.py, framework/personas.md, tests/, docs/0.5.0-beta-plan.md | pending re-audit |
| 2026-09-21T22:19:10Z | Configuration re-audited; report superseded in place (reconstructed time) | audits/configuration.md | audits/configuration.md | PASS WITH ADVISORIES |
| 2026-09-21T22:28:17Z | Configuration repaired, round two: F12 broken antecedent, F13 containment scope, F14 gitlink at the wrong commit, F15 completed-event derivation, F16 this ledger, F18 provenance field | audits/configuration.md F12-F18 | submissions/*.md, event.md, status.md, atj/intake.py, tests/ | pending re-audit |
| 2026-09-21T22:28:50Z | Configuration audited, round three; the auditor corrected its own invented timestamps in place (F19) | audits/configuration.md | audits/configuration.md | PASS WITH ADVISORIES |
| 2026-09-21T22:34:26Z | Configuration repaired, round three: F21 activity-log ordering, F22 stale `last_updated`. Both were introduced by the F16 ledger repair and neither is audited | audits/configuration.md F21, F22 | status.md | not-audited |
