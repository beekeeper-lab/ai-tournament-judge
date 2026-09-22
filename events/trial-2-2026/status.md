---
event_id: trial-2-2026
current_stage: evidence
last_updated: "2026-09-22T00:55:00Z"
blocked: false
blocked_reason: null
stage_gates:
  configuration-audited: passed
  roster-frozen: passed
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
  roster-frozen: audits/intake.md
---

# Event Status

## Stage gates

- [x] Configuration audited
- [x] Roster frozen
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
| team-scribe | pinned `67969dd9`, approved, roster frozen | `ev:…:ba263edf`, sandboxed-partial, approved | — | — | — | — |
| team-demos | pinned `dc35f696`, approved, roster frozen | `ev:…:a19ab6dc`, sandboxed-partial, approved | — | — | — | — |

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
| 2026-09-21T23:16:00Z | Hand repair: the body checkbox 'Configuration audited' ticked to match the ledger, which `atj event validate` was failing on | status.md | status.md | audited — intake F3 confirms it correct and minimal |
| 2026-09-21T23:16:37Z | Intake stage audit | event.md, teams.md, submissions/*.md, status.md, audits/configuration.md, both checkouts | audits/intake.md | FAIL (1 major and blocking, 4 minor, 5 advisory) |
| 2026-09-21T23:35:29Z | Intake repaired, round one: F1 gitlink scope restated as an event-director decision, F2 `completed_at`, F3 this ledger, F5 wrapper scope, F6 both records approved, F8 repository-relative checkout paths, F9 the visibility check cited, F10 both checkouts detached at their pins. F4 and F8 also repaired in the framework; F7 left open | audits/intake.md F1-F10 | submissions/*.md, status.md, docs/0.5.0-beta-plan.md, atj/event.py, atj/intake.py, tests/ | pending re-audit |
| 2026-09-21T23:37:00Z | Intake re-audited, round two; report superseded in place | audits/intake.md | audits/intake.md | PASS WITH ADVISORIES (F1 repaired; F11-F15 new, three of them introduced by the round-one repair) |
| 2026-09-21T23:49:03Z | Intake repaired, round two: F11 bean directory count 56 to 54, F12 python scan count and the tree enumeration, F13 the antecedent the round-one insert broke, F15 why the two records scope the wrapper differently. F14 repaired in the framework; both records re-approved after the edits | audits/intake.md F11-F15 | submissions/*.md, status.md, atj/event.py, atj/cli.py, tests/ | pending re-audit |
| 2026-09-21T23:53:00Z | Intake re-audited, round three; report superseded in place | audits/intake.md | audits/intake.md | PASS WITH ADVISORIES — 18 findings over three rounds, 14 repaired, freeze cleared |
| 2026-09-21T23:55:13Z | Intake repaired, round three: F16 the bean count sentence, F17 the checkbox notice reached only `atj event gate`, F18 the closing paragraph left under the wrong heading. Records and the audit approved, `teams.md` frozen, `roster-frozen` recorded | audits/intake.md F16-F18 | submissions/*.md, teams.md, status.md, audits/intake.md, atj/cli.py | not-audited |
| 2026-09-21T23:56:18Z | `atj event advance` intake to evidence | status.md | status.md | gate roster-frozen passed on audits/intake.md |
| 2026-09-22T00:35:00Z | Evidence packages prepared for both teams: 11 isolated runs, two manifests, the F7 no-audio-device decision and the F11 whole-checkout wrapper recorded, and the demos dry-run invocation taken as the event's decision | both checkouts at their pins, images `034af8181f8d` and `ec7d6c95cd36` | evidence/team-scribe/manifest.md, evidence/team-demos/manifest.md, runs/*.json, evidence/Containerfile.demos | FAIL — see audits/evidence.md |
| 2026-09-22T00:41:00Z | Evidence stage audit | both manifests, 11 run records, both Containerfiles, status.md, both checkouts, framework policies and schemas | audits/evidence.md | FAIL (3 major and blocking, 10 minor, 6 advisory) |
| 2026-09-22T00:55:00Z | Evidence repaired, round one: F1 the fourth `OPENAI_API_KEY` read site, F2 the hardened variant's second change, F3 `agentic` added and `security` argued out, F4-F13 counts, line references, reproduction pointers and timestamps, F15 the stale backup deleted, F16 `execution_record`, F17 both manifests approved, F18 configuration F7 closed, F19 the image contents argued against `event.md`'s rule. F14 left open: `runs/*.json` is validated by nothing, and registering a schema is a framework change this stage will not make mid-event | audits/evidence.md F1-F19 | evidence/*/manifest.md, audits/configuration.md, status.md | pending re-audit |
