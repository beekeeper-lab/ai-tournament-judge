---
event_id: trial-2-2026
current_stage: consolidation
last_updated: "2026-09-22T20:05:00Z"
blocked: false
blocked_reason: null
stage_gates:
  configuration-audited: passed
  roster-frozen: passed
  evidence-validated: passed
  judgments-audited: passed
  consolidation-audited: pending
  bracket-audited: pending
  tournament-audited: pending
  dossiers-approved: pending
  final-audit-passed: pending
units: []
gate_evidence:
  configuration-audited: audits/configuration.md
  roster-frozen: audits/intake.md
  evidence-validated: audits/evidence.md
  judgments-audited: audits/judgments.md
---

# Event Status

## Stage gates

- [x] Configuration audited
- [x] Roster frozen
- [x] All eligible evidence packages validated
- [x] All initial judgments audited
- [ ] All consolidated reports audited
- [ ] Bracket frozen and audited
- [ ] Tournament complete
- [ ] All team dossiers approved
- [ ] Final event audit passed
- [ ] Event marked complete
## Team progress

| Team ID | Intake | Evidence | Four judgments | Consolidated | Audited | Dossier |
|---|---|---|---|---|---|---|
| team-scribe | pinned `67969dd9`, approved, roster frozen | `ev:…:018cf089`, sandboxed-partial, approved | 4 of 4, audited over three rounds | not finalized; `agentic` NE accepted by `adj:trial-2-2026:team-scribe:01`, provisional 32.5 | judgments audited, gate passed | — |
| team-demos | pinned `dc35f696`, approved, roster frozen | `ev:…:cb3847cb`, sandboxed-partial, approved | 4 of 4, audited over three rounds | not finalized; `functional` NE accepted by `adj:trial-2-2026:team-demos:01`, provisional 52.5 | judgments audited, gate passed | — |

## Blockers and adjudications

| ID | Scope | Description | Owner | Status | Resolution artifact |
|---|---|---|---|---|---|
| ADJ-1 | team-scribe, `agentic` | `atj score` records `adjudication_required: unresolved-ne`; judge-frontend-ux and judge-security-ops both recorded `NE`, which blocks an official total. Not due at this stage, since no total is wanted here | event-director | deferred to consolidation by decision | — |
| ADJ-2 | team-demos, `functional` | `atj score` records `adjudication_required: unresolved-ne`; judge-frontend-ux and judge-security-ops both recorded `NE`, which blocks an official total. Not due at this stage, since no total is wanted here | event-director | deferred to consolidation by decision | — |

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
| 2026-09-22T00:14:30Z | Evidence packages prepared for both teams: 11 isolated runs, two manifests, the F7 no-audio-device decision and the F11 whole-checkout wrapper recorded, and the demos dry-run invocation taken as the event's decision | both checkouts at their pins, images `034af8181f8d` and `ec7d6c95cd36` | evidence/team-scribe/manifest.md, evidence/team-demos/manifest.md, runs/*.json, evidence/Containerfile.demos | FAIL — see audits/evidence.md |
| 2026-09-22T00:40:30Z | Evidence stage audit | both manifests, 11 run records, both Containerfiles, status.md, both checkouts, framework policies and schemas | audits/evidence.md | FAIL (3 major and blocking, 10 minor, 6 advisory) |
| 2026-09-22T00:41:20Z | Evidence repaired, round one: F1 the fourth `OPENAI_API_KEY` read site, F2 the hardened variant's second change, F3 `agentic` added and `security` argued out, F4-F13 counts, line references, reproduction pointers and timestamps, F15 the stale backup deleted, F16 `execution_record`, F17 both manifests approved, F18 configuration F7 closed, F19 the image contents argued against `event.md`'s rule. F14 left open: `runs/*.json` is validated by nothing, and registering a schema is a framework change this stage will not make mid-event | audits/evidence.md F1-F19 | evidence/*/manifest.md, audits/configuration.md, status.md | pending re-audit |
| 2026-09-22T00:56:33Z | Evidence re-audited, round two; report superseded in place | audits/evidence.md, both manifests, the repair diff | audits/evidence.md | PASS WITH ADVISORIES — 28 findings, 16 repaired, 12 open, none blocking; gate may be set |
| 2026-09-22T00:59:00Z | Evidence repaired, round two: F10 and F13 residue, F20 hand-stamped approvals redone with `atj event approve`, F21 the thirteenth thread-safety test, F22 the apt count and comment range, F23 no payload in either capture, F26-F28 the `DEMO_DIR` path fix, the reporting-function read site and the hardened SYSTEM range. F14 stays open in framework scope | audits/evidence.md F10, F13, F20-F28 | evidence/*/manifest.md, status.md, audits/configuration.md | pending re-audit |
| 2026-09-22T01:05:25Z | Evidence audited, round three, scoped to the round-two repair; report superseded in place | audits/evidence.md, both manifests, the repair diff | audits/evidence.md | PASS WITH ADVISORIES — 34 findings over three rounds, 26 repaired, none blocking; gate may be set |
| 2026-09-22T01:10:39Z | Evidence repaired, round three: F22 the install line range, F28 the two citation cells the prose had outrun, F32 and F33 the twelve-of-thirteen wording and the `setUp` it names, F34 the observation R9's payload clause rests on, claimed from both ends. F29-F31 ledger stamps corrected to times that precede their commits. Not audited | audits/evidence.md F22, F28-F34 | evidence/*/manifest.md, status.md | not-audited |
| 2026-09-22T01:11:35Z | `atj event gate` evidence-validated passed and `atj event advance` evidence to initial-judging (`75d24b0`) | audits/evidence.md | status.md | gate evidence-validated passed on audits/evidence.md |
| 2026-09-22T10:37:08Z | Four independent judgments for team-scribe (`5752c04`) | evidence/team-scribe/manifest.md, runs/team-scribe-*.json, checkout at `67969dd9` | judgments/team-scribe/judge-{backend,frontend-ux,product-agentic,security-ops}.md | not-audited |
| 2026-09-22T10:45:25Z | Repair: three team-scribe judgment files carried a duplicate preamble appended after `## Calculation and independence declaration`, an orchestrator extraction defect. `atj validate reports` had returned PASS on them; recorded as W9 (`0047f03`) | judgments/team-scribe/*.md | judgments/team-scribe/*.md, docs/0.5.0-beta-plan.md | not-audited |
| 2026-09-22T10:46:19Z | Four independent judgments for team-demos (`2b91208`) | evidence/team-demos/manifest.md, runs/team-demos-*.json, checkout at `dc35f696` | judgments/team-demos/judge-{backend,frontend-ux,product-agentic,security-ops}.md | not-audited |
| 2026-09-22T13:06:00Z | Initial-judging stage audit; roughly 120 citations followed to the artifact | eight judgments, both manifests, 11 run records, both Containerfiles, status.md, event.md, both checkouts, framework rubrics and templates | audits/judgments.md | FAIL (1 blocking, 1 major, 5 minor, 5 advisory) |
| 2026-09-22T13:19:00Z | Judgments repaired, round one: F1 the claimed absence of `.env.example`, withdrawn by both judges that made it after each re-checked the git index rather than a filesystem glob; F2 the bean count; F3 the `rm` pre-approval citation; F4 the installer's reachable branch; F5 this ledger; F6 both unresolved-NE triggers recorded as ADJ-1 and ADJ-2; F10 the demo enumeration; F11 the stale backup. F7 recorded as W10 and F1's root cause as W11, both framework scope and not landed mid-event. No raw score changed anywhere | audits/judgments.md F1-F7, F10, F11 | judgments/team-demos/judge-{frontend-ux,security-ops,backend}.md, judgments/team-scribe/judge-{product-agentic,security-ops}.md, status.md, docs/0.5.0-beta-plan.md | pending re-audit |
| 2026-09-22T14:05:00Z | Judgments re-audited, round two, scoped to the round-one repair; report superseded in place | audits/judgments.md, the eight judgments, the repair diff `91ce6a6` | audits/judgments.md | PASS WITH ADVISORIES — 19 findings over two rounds, 8 repaired, 2 accepted, 2 deferred, 7 open, none blocking; gate may be set |
| 2026-09-22T14:13:00Z | Judgments repaired, round two: F13 the amendment record moved out of prose after the declaration and into a declaration checkbox in both files, which is where W9's defect had reappeared; F14 the antecedent the round-one repair broke; F15 `Bash(rm:*)` corrected to the seventeen command files that carry it, from a seven in one place and an eight in another, which widens D2 rather than softening it; F16 the root README ordering inside the D1 withdrawal; F17 an amendment record added to the three files the event director corrected rather than their authors. Four of the seven were introduced by the round-one repair. F18 and F19 accepted as advisory with no repair: naming the `settings.py:304` guard is optional and would strengthen rather than weaken S1, and F19 is a note carried to consolidation. W12 records that the judgment template defines no place for an amendment, which is why the round-one repair invented two | audits/judgments.md F13-F19 | judgments/team-demos/judge-frontend-ux.md, judgments/team-demos/judge-security-ops.md, judgments/team-demos/judge-backend.md, judgments/team-scribe/judge-product-agentic.md, judgments/team-scribe/judge-security-ops.md, status.md, docs/0.5.0-beta-plan.md | pending re-audit |
| 2026-09-22T14:20:00Z | Judgments audited, round three, scoped to the round-two repair; report superseded in place | audits/judgments.md, the eight judgments, the repair diff `7957530` | audits/judgments.md | PASS WITH ADVISORIES — 22 findings over three rounds, 13 repaired, 4 accepted, 2 deferred in framework scope, 3 open, none blocking or major; gate may be set |
| 2026-09-22T14:22:00Z | Judgments repaired, round three: F20 this ledger's round-two audit row, stamped before the artifact it records; F22 the half-repaired over-generalisation at `judge-security-ops.md:193`, where F16's correction had reached `:79` and not the D1 withdrawal below it. F21 accepted as advisory: three amendment checkboxes record the event director's action inside the judge's attestation block, each naming who acted, and W12 closes it. No raw score has moved in any of the three rounds | audits/judgments.md F20-F22 | status.md, judgments/team-demos/judge-security-ops.md | not-audited |
| 2026-09-22T14:19:58Z | `atj event approve` audits/judgments.md, then `atj event gate` judgments-audited passed and `atj event advance` initial-judging to consolidation | audits/judgments.md | status.md | gate judgments-audited passed on audits/judgments.md |
| 2026-09-22T18:07:45Z | Two adjudications written and approved: `adj:trial-2-2026:team-scribe:01` accepts the `agentic` NE and `adj:trial-2-2026:team-demos:01` accepts the `functional` NE. Event-director decision, `decision_authority: human-official`, no score supplied for either. `atj score` now records `adjudication_required: []` and both NEs as accepted; both panels stay unfinalized by decision. Writing them found W13: the adjudication template ships `substitution_reason: null`, which its own schema rejects, and `scope: team`, which `atj/scoring.py:497` silently skips | summaries/*.json, framework/templates/adjudication-report.md | adjudications/adj-trial-2-2026-team-scribe-agentic.md, adjudications/adj-trial-2-2026-team-demos-functional.md, docs/0.5.0-beta-plan.md | not-audited |
| 2026-09-22T18:40:00Z | Consolidated panel reports for both teams, written by `panel-consolidator` from the four judgments, the approved adjudication and the `atj score` result; score blocks generated by `atj render consolidated`, no cell transcribed by hand. Neither report carries an official total: `total: null`, `finalized: false`, provisional sums 32.5 and 52.5, not publishable and not usable for seeding | judgments/*/*.md, summaries/*.json, adjudications/*.md, audits/judgments.md | summaries/team-scribe.md, summaries/team-demos.md | not-audited |
| 2026-09-22T20:02:00Z | Consolidation stage audit, first pass. `atj score` reproduced both panels field for field, `atj render consolidated` rewrote both score blocks to byte-identical output, and the four repository validators pass. The stage fails on prose: F1, `summaries/team-scribe.md:218-221` credits a `.env` documentation contradiction to two judges where `judge-product-agentic` never mentions `.env`. Ten further major findings are the same family — corroboration inflated or a single-judge concern dropped | both summaries and their JSON, eight judgments, two adjudications, both manifests, 11 run records, audits/judgments.md, status.md, framework rubrics and `atj/scoring.py` | audits/consolidation.md | FAIL (1 blocking, 10 major, 14 minor, 7 advisory) |
