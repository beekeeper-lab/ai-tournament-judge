---
event_id: live-trial-2026
current_stage: intake
last_updated: "2026-09-16T23:41:29Z"
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
| team-podcast | done, pinned f3fdd342465fa6bc2a52d226a8613b082ad329e0 | pending | pending | pending | pending | pending |
| team-ledger | done, pinned 9d21b7707f204ef60f5a1cee612f1d4db0a4a575 | pending | pending | pending | pending | pending |

Intake is not a unit in the ledger: `atj event unit` derives digests only for
`evidence:`, `judging:` and `consolidation:`. Intake state is tracked here and in
the roster.

## Blockers and adjudications

| ID | Scope | Description | Owner | Status | Resolution artifact |
|---|---|---|---|---|---|

## Activity log

| Timestamp | Action | Input identity | Output | Audit result |
|---|---|---|---|---|
| 2026-09-16T23:27:41Z | `atj intake` team-podcast | github.com/beekeeper-lab/podcast-listener @ f3fdd342 | submissions/team-podcast.md, workspaces/live-trial-2026/team-podcast | not-audited |
| 2026-09-16T23:29:24Z | `atj intake` team-ledger | github.com/beekeeper-lab/hive-ledger @ 9d21b770 | submissions/team-ledger.md, workspaces/live-trial-2026/team-ledger | not-audited |
| 2026-09-16T23:36:00Z | Configuration audit, first pass | event.md, teams.md, submissions/*.md | audits/configuration.md | FAIL |
| 2026-09-16T23:37:00Z | Configuration repaired: body sections written, validation_state corrected, status brought current | audits/configuration.md F1-F3 | event.md, status.md | pending re-audit |
| 2026-09-16T23:41:20Z | Configuration re-audited after repair; approved images recorded (F4), ledger timestamps corrected (F5) | audits/configuration.md | event.md, status.md | PASS WITH ADVISORIES |
