---
event_id: live-trial-2026
current_stage: consolidation
last_updated: "2026-09-17T22:14:54Z"
blocked: false
blocked_reason: null
stage_gates:
  configuration-audited: passed
  roster-frozen: passed
  evidence-validated: passed
  judgments-audited: passed
  consolidation-audited: passed
  bracket-audited: pending
  tournament-audited: pending
  dossiers-approved: pending
  final-audit-passed: pending
units:
- unit_id: evidence:team-podcast
  stage: evidence
  state: complete
  input_digest: 29ed1aec8ef5bb24
  outputs:
  - evidence/team-podcast/manifest.md
  audit_result: PASS WITH ADVISORIES
  completed_at: "2026-09-17T19:12:26Z"
- unit_id: evidence:team-ledger
  stage: evidence
  state: complete
  input_digest: 814294074475db23
  outputs:
  - evidence/team-ledger/manifest.md
  audit_result: PASS WITH ADVISORIES
  completed_at: "2026-09-17T19:12:26Z"
- unit_id: judging:team-ledger
  stage: initial-judging
  state: complete
  input_digest: 22215ab0e39dee06
  outputs:
  - judgments/team-ledger
  audit_result: PASS WITH ADVISORIES
  completed_at: "2026-09-17T21:38:23Z"
- unit_id: judging:team-podcast
  stage: initial-judging
  state: complete
  input_digest: 9ed387f6a70da5dd
  outputs:
  - judgments/team-podcast
  audit_result: PASS WITH ADVISORIES
  completed_at: "2026-09-17T21:38:23Z"
- unit_id: consolidation:team-ledger
  stage: consolidation
  state: complete
  input_digest: be70393f10f80e05
  outputs:
  - summaries/team-ledger.md
  audit_result: PASS WITH ADVISORIES
  completed_at: "2026-09-17T22:14:54Z"
- unit_id: consolidation:team-podcast
  stage: consolidation
  state: complete
  input_digest: c68ba1d4e6cafbf7
  outputs:
  - summaries/team-podcast.md
  audit_result: PASS WITH ADVISORIES
  completed_at: "2026-09-17T22:14:54Z"
gate_evidence:
  configuration-audited: audits/configuration.md
  roster-frozen: audits/intake.md
  evidence-validated: audits/evidence.md
  judgments-audited: audits/judgments.md
  consolidation-audited: audits/consolidation.md
---
# Event Status

## Stage gates

- [x] Configuration audited
- [x] Roster frozen
- [x] All eligible evidence packages validated
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
| team-podcast | done, pinned f3fdd342465fa6bc2a52d226a8613b082ad329e0 | done, audited PASS WITH ADVISORIES on the third pass (ev:live-trial-2026:team-podcast:f3fdd342465f:d06f90cc) — `reliability` evidence-limited | done, 4 of 4, six criteria aligned, `reliability` NE from all four | done, **no official total** — NE adjudicated and accepted; provisional 58.25 unofficial and kept out of the score block | consolidation audit PASS WITH ADVISORIES | pending |
| team-ledger | done, pinned 9d21b7707f204ef60f5a1cee612f1d4db0a4a575 | done, audited PASS WITH ADVISORIES (ev:live-trial-2026:team-ledger:9d21b7707f20:b859a240) | done, 4 of 4, all criteria aligned | done, 76.3 finalized, all seven aligned | consolidation audit PASS WITH ADVISORIES | pending |

Intake is not a unit in the ledger: `atj event unit` derives digests only for
`evidence:`, `judging:` and `consolidation:`. Intake state is tracked here and in
the roster.

## Blockers and adjudications

| ID | Scope | Description | Owner | Status | Resolution artifact |
|---|---|---|---|---|---|
| adj:live-trial-2026:team-podcast:01 | criterion | Unresolved `NE` on `reliability` from all four judges blocks the official total; evidence cannot resolve it and the stage is frozen | event-director | resolved | adjudications/team-podcast-reliability-ne.md |

## Activity log

| Timestamp | Action | Input identity | Output | Audit result |
|---|---|---|---|---|
| 2026-09-16T23:27:41Z | `atj intake` team-podcast | github.com/beekeeper-lab/podcast-listener @ f3fdd342 | submissions/team-podcast.md, workspaces/live-trial-2026/team-podcast | not-audited |
| 2026-09-16T23:29:24Z | `atj intake` team-ledger | github.com/beekeeper-lab/hive-ledger @ 9d21b770 | submissions/team-ledger.md, workspaces/live-trial-2026/team-ledger | not-audited |
| 2026-09-16T23:36:00Z | Configuration audit, first pass | event.md, teams.md, submissions/*.md | audits/configuration.md | FAIL |
| 2026-09-16T23:37:00Z | Configuration repaired: body sections written, validation_state corrected, status brought current | audits/configuration.md F1-F3 | event.md, status.md | pending re-audit |
| 2026-09-16T23:41:20Z | Configuration re-audited after repair; approved images recorded (F4), ledger timestamps corrected (F5) | audits/configuration.md | event.md, status.md | PASS WITH ADVISORIES |
| 2026-09-16T23:49:05Z | Roster frozen at version 1 | teams.md | teams.md | not-audited |
| 2026-09-16T23:49:05Z | Sandbox verified live: podman 6.1.0, rootless, exit 0 against both checkouts | workspaces/live-trial-2026/* | — | not-audited |
| 2026-09-16T23:49:05Z | Approved images amended (authorized by the event-director, the official named in `event.md` for configuration changes): default image cannot run either test suite offline | event.md | event.md, evidence images | pending intake audit |
| 2026-09-16T23:49:05Z | team-ledger test suite executed in sandbox: 35 passed, exit 0, no network | 9d21b770 @ localhost/atj-live-trial/ledger:1 | run record | not-audited |
| 2026-09-16T23:56:58Z | Intake records completed by two independent agents | checkouts @ f3fdd342, 9d21b770 | submissions/team-podcast.md, submissions/team-ledger.md | PASS WITH ADVISORIES |
| 2026-09-16T23:56:58Z | Intake stage audited | teams.md, submissions/*.md, event.md amendment | audits/intake.md | PASS WITH ADVISORIES |
| 2026-09-16T23:56:58Z | Images rebuilt to close intake F1: uvicorn[standard], httpx and pytest removed from podcast; poppler-utils added to ledger (A9) | Containerfile.ledger, Containerfile.podcast | ledger:2 7780b2b9e6e1, podcast:2 5ff34ae63320 | not-audited |
| 2026-09-16T23:56:58Z | Image IDs recorded in event.md to close intake F4 | podman images | event.md | not-audited |
| 2026-09-16T23:56:58Z | team-ledger suite re-run WITH a run record, closing intake F2 | 9d21b770 @ localhost/atj-live-trial/ledger:2 | runs/team-ledger-pytest-01.json — 35 passed, exit 0, no network | not-audited |
| 2026-09-16T23:56:58Z | Intake records moved to approved/valid (A2); team-ledger execution footer corrected | audits/intake.md | submissions/*.md | not-audited |
| 2026-09-17T00:06:11Z | Evidence prepared for team-podcast: 5 sandboxed executions (env probe confirming no ffmpeg/ffprobe in the approved image; server boot on an empty library; direct route-level byte-range + progress/resume tests via a synthetic media file; a full `tests/e2e.py` attempt that reached Chromium and static-asset serving but stopped at check 1 for lack of transcoded media; a `run.sh` attempt showing its venv step cannot run against the read-only mount) | f3fdd342 @ localhost/atj-live-trial/podcast:2, runs/team-podcast-*.json (5 total) | evidence/team-podcast/manifest.md — execution_status sandboxed-partial (no ffmpeg/ffprobe in image blocks populating the library; iPhone-specific claims remain team claims by nature) | `atj validate reports` PASS at the time; SUPERSEDED by the podcast:3 package at 00:24:30 |
| 2026-09-17T00:06:11Z | team-podcast evidence, first pass: e2e blocked at stage 1 of 11 by a missing ffmpeg in the approved image | f3fdd342 @ podcast:2 | evidence/team-podcast/manifest.md | superseded |
| 2026-09-17T00:11:01Z | Image amended to podcast:3 (c3670644bc7b) adding ffmpeg, a README prerequisite. Authorized by the event-director. Omitting it was an operator error that disadvantaged this team relative to team-ledger, whose image already carries poppler-utils on identical reasoning | README prerequisites | event.md, podcast:3 | not-audited |
| 2026-09-17T00:15:00Z | Evidence prepared for team-ledger: 10 new sandboxed executions (CLI help surface, CSV ingest + D0, ingest rejection/idempotency paths, Amazon ingest + match tiers + D1, analyze/render/dispute, PDF-adapter parsing grammar via synthetic layout text x2, vault/file permission check), plus the existing pytest run | 9d21b770 @ localhost/atj-live-trial/ledger:2, runs/team-ledger-*.json (11 total) | evidence/team-ledger/manifest.md — execution_status sandboxed-partial (real end-to-end PDF-file CLI ingest not exercisable: no PDF-authoring tool in image) | `atj validate reports` PASS, 0 blocking |
| 2026-09-17T00:15:00Z | team-ledger evidence package complete, 11 run records, sandboxed-partial | 9d21b770 @ ledger:2 | evidence/team-ledger/manifest.md | not-audited |
| 2026-09-17T00:21:06Z | team-podcast execution evidence re-run against the corrected image | f3fdd342 @ podcast:3 | evidence/team-podcast/manifest.md, runs/ | pending evidence audit |
| 2026-09-17T00:24:30Z | team-podcast manifest revised in place: transcode/index/serve pipeline demonstrated end to end (podcast:3), tests/e2e.py reached stage 7 of 11 (up from stage 1), 64 MB tmpfs recorded as the framework's cap (not the submission's), two candidate findings (stage-7 stall, 1-vs-2-episode download timing) recorded as inconclusive rather than confirmed defects; e2e-attempt-01 kept as the record of the original blocked attempt | f3fdd342 @ podcast:3, runs/team-podcast-*.json (11 total) | evidence/team-podcast/manifest.md — execution_status sandboxed-partial (stages 8-11 and all iPhone-specific claims remain unexecuted) | `atj validate reports` PASS, 0 blocking |
| 2026-09-17T18:35:00Z | Evidence stage audited by `judging-auditor@1.0.0` | event.md, teams.md, status.md, both manifests, 22 run records, both Containerfiles | audits/evidence.md | FAIL — F1, F2, F3, F4 major |
| 2026-09-17T18:35:52Z | F6 repair: the four podcast:2 runs still carrying current evidence repeated on the approved podcast:3 | f3fdd342 @ podcast:3 | runs/team-podcast-runsh-attempt-02, -media-progress-02, -env-probe-03, -server-boot-02 — identical results; :3 runtime probed directly | pending re-audit |
| 2026-09-17T18:36:28Z | F5 repair: the two-episode e2e scenario repeated in isolation, no concurrent container | f3fdd342 @ podcast:3 | runs/team-podcast-e2e-full-02.json — did not reproduce the 90s stall; Chromium `Target crashed` at stage 3, a third distinct outcome | pending re-audit |
| 2026-09-17T18:41:56Z | F1 repair: Containerfile.ledger reconciled against `podman history` for ledger:2 (7780b2b9e6e1), adding the omitted poppler-utils layer. Not rebuilt: a rebuild would resolve new package versions, change the image ID and invalidate 11 run records. Authorized by the event-director | podman history | evidence/Containerfile.ledger, event.md | pending re-audit |
| 2026-09-17T18:41:56Z | F2 repair: team-podcast `evidence_limited_criteria` set to `[reliability]` — three executions of tests/e2e.py, three different outcomes, none classified | audits/evidence.md F2; ev-podcast-15, -16, -20 | evidence/team-podcast/manifest.md | pending re-audit |
| 2026-09-17T18:41:56Z | F4/F7 repair: nine misdirected evidence citations in the team-ledger requirements table repointed; R3 and R6 marked partial; subcommand count corrected to ten | audits/evidence.md F4, F7 | evidence/team-ledger/manifest.md | pending re-audit |
| 2026-09-17T18:41:56Z | F6/F8/F9 and A1-A4 repairs: podcast:2 listed in event.md with scope, activity log restamped from run records and both amendments attributed, `.agentic/project.yaml` corrected to six lines, run-timeout justification and the tmpfs-versus-image distinction recorded | audits/evidence.md F6, F8, F9, A1-A4 | event.md, status.md, both manifests | pending re-audit |
| 2026-09-17T18:50:00Z | Evidence stage re-audited after the first repair round | audits/evidence.md (first pass), commit 44e5f87, both manifests, 27 run records | audits/evidence.md (replaced) | FAIL — F1-F9 and A1-A4 closed or partially closed; new F10, F11 major, F12 minor |
| 2026-09-17T18:56:46Z | F10 repair: R1, R5, R12, R14 and R16 recited in the team-ledger requirements table; ev-ledger-20 added recording the grep over all 22 files of `src/fin/` that R12's network/HTTP/LLM claim and R16 actually rest on | audits/evidence.md F10; `src/fin/**/*.py` @ 9d21b770 | evidence/team-ledger/manifest.md | pending re-audit |
| 2026-09-17T18:56:46Z | F11 repair: ev-podcast-21's `playwright 1.56.0` was unmeasured and contradicted — no run record contains it. Corrected to 1.63.0, sourced from runs/team-podcast-server-boot-02.json, and env-probe-03's failed version probe recorded | audits/evidence.md F11 | evidence/team-podcast/manifest.md | pending re-audit |
| 2026-09-17T18:56:46Z | F12 repair: `*.bak` added to .gitignore and status.md.bak removed from the index. `atj/event.py:745` writes it as crash recovery on every ledger update, so ignoring it is the only closure that holds | audits/evidence.md F12; atj/event.py:745 | .gitignore | pending re-audit |
| 2026-09-17T18:56:46Z | F8 residual repair: four rows stamped after the commit that recorded them restamped to 18:41:56Z; the audit row restamped to its artifact's completed_at; the provenance note below corrected | audits/evidence.md F8; git log, runs/*.json | status.md | pending re-audit |
| 2026-09-17T19:20:00Z | Evidence stage audited, third pass | audits/evidence.md (second pass), commit 4ac09ba, both manifests, 27 run records, re-run of the src/fin/ grep | audits/evidence.md (replaced) | PASS WITH ADVISORIES — F1-F12 closed; new F13-F17 minor, A10-A13 advisory |
| 2026-09-17T19:20:00Z | F13-F17 and A10-A13 repaired: two Missing-evidence bullets repointed from ev-ledger-10 to ev-ledger-20; ev-podcast-21's starlette and Debian values marked as :3-only measurements; req-03 now names ev-ledger-20's re-test; four rows restamped to commit 4ac09ba's time and the F6 row to the last of its records; Containerfile.ledger's caller path corrected to src/fin/adapters/citi_pdf.py:198; the activity log rejoined into one table; R3 corrected to five tiers with tier 2 also unexercised; the 24.5s figure separated into 17.3s transcode and ~7s suite | audits/evidence.md F13-F17, A10-A13 | both manifests, evidence/Containerfile.ledger, status.md, atj/cli.py | pending gate |
| 2026-09-17T19:20:00Z | A10 repair: `atj render judgment` now scores and checks every file before writing any, so a run that will refuse refuses having written nothing, and reports `forced_over_approval` in `--json` | audits/evidence.md A10 | atj/cli.py, tests/test_end_to_end.py | pending gate |
| 2026-09-17T19:20:52Z | Four independent judgments for team-ledger, staged then promoted together | ev:live-trial-2026:team-ledger:9d21b7707f20:b859a240 @ 9d21b770 | judgments/team-ledger/{judge-backend,judge-frontend-ux,judge-product-agentic,judge-security-ops}.md | not-audited |
| 2026-09-17T19:35:00Z | FRAMEWORK DEFECT found: the four judge personas declare `tools: Read, Grep, Glob` and cannot write the artifact judge-submission requires of them. All four returned their document as text; the orchestrator persisted each verbatim, which the skill's step 4 permits ("hold each returned report in the orchestrator's own context"). Personas were NOT changed — judging had begun, and CLAUDE.md forbids changing a persona mid-event. Needs a new persona version before the next event | .claude/agents/judge-*.md | judgments/team-ledger/*.md, this entry | pending judgments audit |
| 2026-09-17T19:35:00Z | FRAMEWORK DEFECT found: `schemas/judgment.schema.json` requires a `model` block that `framework/templates/individual-judgment.md` does not show. Four judgments failed validation on it and the block was added from each file's own front matter | atj validate reports | judgments/team-ledger/*.md | pending judgments audit |
| 2026-09-17T19:35:00Z | Scores table generated for all four by `atj render judgment`; no weight or total was typed by any judge | framework/rubrics/submission-evaluation.md | judgments/team-ledger/*.md | not-audited |
| 2026-09-17T19:35:00Z | team-ledger panel consolidated by `atj score`: 76.3 of 100, all seven criteria aligned, no NE, no outlier, no adjudication required | judgments/team-ledger/ | summaries/team-ledger.json | not-audited |
| 2026-09-17T20:23:16Z | Four independent judgments for team-podcast, staged under `workspaces/live-trial-2026/staging/team-podcast/` then promoted together | ev:live-trial-2026:team-podcast:f3fdd342465f:d06f90cc @ f3fdd342 | judgments/team-podcast/{judge-backend,judge-frontend-ux,judge-product-agentic,judge-security-ops}.md | not-audited |
| 2026-09-17T20:23:16Z | Scores tables generated for all four by `atj render judgment`; no weight or total was typed by any judge. Each table records `not finalizable (unresolved NE)` rather than a sum | framework/rubrics/submission-evaluation.md | judgments/team-podcast/*.md | not-audited |
| 2026-09-17T21:02:28Z | team-podcast panel consolidated by `atj score`: **no official total**. `reliability` is `NE` from all four judges independently, which blocks finalization. Six scored criteria all `aligned`, no outlier. **Adjudication IS required**: `summaries/team-podcast.json` records `adjudication_required: [{criterion: reliability, trigger: unresolved-ne}]` and `framework/policies/disagreement-and-adjudication.md:5` requires it for an `NE` that prevents scoring. `adjudications/` was empty when this row was first written at 21:02:28Z; the adjudication was written at 21:20:42Z and is now recorded in the Blockers and adjudications table above. The operator's original entry here said the opposite, taken from `atj score`'s console output, which prints `blocked_reasons` but not `adjudication_required` (judgments audit F2, A3). Provisional sum of scored criteria 58.25 of 100, explicitly not an official total and not usable for bye seeding | judgments/team-podcast/ | summaries/team-podcast.json | not-audited |
| 2026-09-17T21:02:28Z | EVIDENCE DEFECT found after the evidence gate passed. Attribution, corrected by the judgments audit (F3): the stage count was flagged by two judges, the check-count error by one (`judge-backend`), and the `evidence_limited_criteria` contradiction by none — the operator's original entry credited three judges with all three. The defects: the team-podcast manifest contradicts itself on evidence limits (Scope section says no criterion is listed in `evidence_limited_criteria`; front matter and the Missing-evidence section both say `reliability` is), states `tests/e2e.py` has 11 stages where the file prints 13, and ev-podcast-05's `check()` count of 43 includes the function definition, so the team's own "42/42" claim is consistent with the source and the manifest's "neither figure matches" is wrong. Audit F1 re-derived 42 call sites and ruled that three judges repeated the manifest's 43 adversely against the team — `judge-product-agentic` listing it as a confirmed defect on "direct file inspection" — while `judge-backend` caught it. No score moves. Not repaired here: the evidence package is frozen for a judged team. Belongs to the judging-stage audit | judgments/team-podcast/*.md | this entry | pending judgments audit |
| 2026-09-17T21:20:00Z | Initial-judging stage audited by `judging-auditor@1.0.0`, first pass, both teams | judgments/{team-ledger,team-podcast}/, both summaries, status.md, 27 run records | audits/judgments.md | FAIL — F1, F2 major |
| 2026-09-17T21:20:42Z | `reliability` NE adjudicated for team-podcast and ACCEPTED. The evidence cannot resolve the criterion and every traced failure points at the sandbox, not the submission. Evidence stage deliberately NOT reopened: `CLAUDE.md` forbids changing evidence once judging begins, and a re-run would invalidate four judgments that cite this package. team-podcast completes the event with no official total, for a framework and operator reason, not a team one | summaries/team-podcast.json, ev-podcast-15/-16/-17/-18/-20 | adjudications/team-podcast-reliability-ne.md (resolution resolved, decided_by event-director) | pending judgments re-audit |
| 2026-09-17T21:20:42Z | Adjudication impact confirmed against the two rubric front matters: the bracket is unaffected (2 teams, `min_teams: 2`, no byes, so no bye seeding reads a total) and the head-to-head is unaffected (`head-to-head.md` compares criteria directly and forbids selecting on initial totals). `reliability` is expected to take comparison value `0` in the matchup, which the head-to-head rubric defines as "substantially equal **or** insufficient comparative evidence" — a finding the matchup panel makes on the common evidence, not a value this adjudication can impose. If the panel does return `0`, `reliability` contributes no margin and the effective tie-break for this pairing falls to functional then product | framework/rubrics/head-to-head.md, framework/rubrics/bracket-assignment.md | adjudications/team-podcast-reliability-ne.md | pending judgments re-audit |
| 2026-09-17T21:20:42Z | FRAMEWORK DEFECTS D10, D11 found while writing that adjudication: the adjudication template invites a human persona the validator rejects, and no vocabulary exists for an adjudication that accepts an `NE` rather than clearing it, so `atj score` still reports it as unresolved with `adjudication_required` outstanding | framework/templates/adjudication-report.md, atj score output | docs/framework-fix-plan.md | not-audited |
| 2026-09-17T21:20:42Z | F2/F3 repaired and the `reliability` NE adjudicated; F4/F6/F7/A3 logged as D7-D9; D10/D11 found and logged | audits/judgments.md (first pass) | status.md, adjudications/team-podcast-reliability-ne.md, docs/framework-fix-plan.md | pending re-audit |
| 2026-09-17T21:33:00Z | Initial-judging stage re-audited after the first repair round | audits/judgments.md (first pass), commits ebb76c2, 01f559f, bdf369d | audits/judgments.md (replaced) | FAIL — F2, F3, F6, F7 closed; adjudication passes; new F8 major, F9-F14 minor, A6-A10 advisory |
| 2026-09-17T21:37:32Z | F8-F13 repaired: the adjudication recorded in the Blockers table, the stale "`adjudications/` is empty" claim corrected, the tie-break overstatement corrected here and in the adjudication, stage-audit rows added, `last_updated` brought forward. F12 and the A6 independence figure corrected. F14 logged as D13 | audits/judgments.md (second pass) | status.md, adjudications/team-podcast-reliability-ne.md, docs/framework-fix-plan.md | pending re-audit |
| 2026-09-17T21:38:36Z | Repair round self-verified before the gate. The F11 stage-audit rows had been appended out of order (21:14:00Z after 21:20:42Z), re-breaking the ascending-order rule the evidence audit established at F8. Caught and re-sorted; all 52 rows now ascend. This is the fifth repair-introduced defect of the event and the first caught before an audit saw it. The F8-F13 repair round was operator-verified, NOT independently audited; the final event audit covers it | audits/judgments.md (second pass) | status.md | operator-verified, pending final audit |
| 2026-09-17T21:49:23Z | Initial-judging stage audited, third pass. F8, F9, F13, F14, A6 closed; F1 and F5 correctly parked as carry-forward to consolidation; A8 ruled advisory. New F15-F19 and D14-D16. **F17 is a false finding**: it claims branch `fix/framework-d7-d10-d12` has no D12, but that branch carries D12 as a defect-table row and a full section — the audit's pickaxe search missed it. F18 was real and is closed: an agent worktree inside the repo made `release-check` FAIL, because four validators walk the filesystem rather than git; removing the worktree restored PASS | audits/judgments.md (second pass), commits 3667c00, cbf76e1, 9ad8a12 | audits/judgments.md (replaced) | PASS WITH ADVISORIES |
| 2026-09-17T21:49:30Z | F10, F12, F15, F16, F19 repaired and F17 rebutted with evidence; worktree removed closing F18. Repair round self-verified against deterministic commands, per the third pass's instruction not to commission a fourth | audits/judgments.md (third pass) | status.md, adjudications/team-podcast-reliability-ne.md, docs/framework-fix-plan.md | operator-verified, pending final audit |
| 2026-09-17T21:58:17Z | Both consolidated panel reports written by `panel-consolidator@1.0.0`, run concurrently and independently. team-ledger finalized at 76.3; team-podcast carries no official total and keeps the provisional 58.25 out of its score block entirely. team-podcast's report carries the two corrections the judging audit ordered (check count is 42 not 43; one judge's attribution unsupported) and records the `agentic` 2/3/3/3 split as an unresolved interpretation disagreement rather than a settled mean | judgments/{team-ledger,team-podcast}/, both summaries/*.json, adjudications/team-podcast-reliability-ne.md | summaries/team-ledger.md, summaries/team-podcast.md | not-audited |
| 2026-09-17T21:58:17Z | FRAMEWORK DEFECT D18: `atj render consolidated` and `atj consolidate` are both cited by the consolidated template and neither exists, so neither report's score block could be generated. Both consolidators disclosed the hand transcription unprompted. Each table was instead verified cell by cell against the canonical JSON by a deterministic script — zero mismatches on both teams — and the consolidation audit re-derived both independently, twice | framework/templates/consolidated-team-report.md, `atj render --help` | docs/framework-fix-plan.md | not-audited |
| 2026-09-17T22:35:00Z | Consolidation stage audited by `judging-auditor@1.0.0`, FIRST pass. The auditor was given D16's scope rule up front — block only on event-scope findings — and returned PASS WITH ADVISORIES in one pass rather than the three the judging stage needed. Arithmetic re-derived twice: `atj score --json` against both committed summaries at 311 and 318 leaves with 0 diffs, then every criterion recomputed independently from the eight judgment front matters and the rubric weights | summaries/*.md, summaries/*.json, the eight judgments, both manifests, the adjudication | audits/consolidation.md | PASS WITH ADVISORIES |
| 2026-09-17T22:40:00Z | C1-C5 and C7 repaired: the template boilerplate claiming `atj consolidate` generated the block and that it was "never transcribed by hand" corrected in place (D19), two unanimity overstatements corrected, both reports restamped to their real run bounds, and the one hand-edited cell inside the generator-owned region restored to the tool's own wording. Both tables re-verified against canonical JSON after the edits, zero mismatches | audits/consolidation.md | summaries/*.md, status.md | operator-verified |

One exception to the audit rule below, recorded rather than hidden: the third-pass
judging audit's artifact carries `completed_at: 2026-09-17T22:19:00Z` while the commit
that recorded it landed at 21:49:23Z. Auditors have no clock (audit A7), and that
fabricated value sorted after work that genuinely happened later. Those two rows carry
their commit time instead. The same defect in judges is why every judgment's timestamps
were replaced by the orchestrator.

Timestamp provenance in this log, stated exactly rather than loosely. A row
describing an execution carries the `completed_at` of the last run record it
describes, read from `runs/*.json`. A row describing a document change carries
the commit time of the commit that recorded it. A row describing an audit
carries that audit artifact's own `completed_at`. The two `2026-09-17T00:15:00Z` rows carry the
`prepared_at` of the manifest they describe, which is neither a run record nor a
commit. Rows predating the evidence stage carry the stamp they were originally
written with. Four rows previously
shared a single `2026-09-17T00:10:14Z` stamp that placed them before work they
happened after, and four more were stamped later than the commit that recorded
them; the evidence audit required the order to ascend and the stamps not to
misstate when work happened (F8).