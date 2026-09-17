---
event_id: live-trial-2026
current_stage: evidence
last_updated: "2026-09-17T19:12:31Z"
blocked: false
blocked_reason: null
stage_gates:
  configuration-audited: passed
  roster-frozen: passed
  evidence-validated: passed
  judgments-audited: pending
  consolidation-audited: pending
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
gate_evidence:
  configuration-audited: audits/configuration.md
  roster-frozen: audits/intake.md
  evidence-validated: audits/evidence.md
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
| team-podcast | done, pinned f3fdd342465fa6bc2a52d226a8613b082ad329e0 | done, repaired after evidence audit FAIL, re-audit pending (ev:live-trial-2026:team-podcast:f3fdd342465f:d06f90cc) — `reliability` evidence-limited | pending | pending | pending | pending |
| team-ledger | done, repaired after evidence audit FAIL, re-audit pending, pinned 9d21b7707f204ef60f5a1cee612f1d4db0a4a575 | done (ev:live-trial-2026:team-ledger:9d21b7707f20:b859a240) | pending | pending | pending | pending |

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
| 2026-09-17T18:56:46Z | F8 residual repair: four rows stamped after the commit that recorded them restamped to 18:41:56Z; the audit row restamped to its artifact's completed_at; the provenance note below corrected | audits/evidence.md F8; git log, runs/*.json | status.md | pending re-audit || 2026-09-17T19:20:00Z | Evidence stage audited, third pass | audits/evidence.md (second pass), commit 4ac09ba, both manifests, 27 run records, re-run of the src/fin/ grep | audits/evidence.md (replaced) | PASS WITH ADVISORIES — F1-F12 closed; new F13-F17 minor, A10-A13 advisory |
| 2026-09-17T19:20:00Z | F13-F17 and A10-A13 repaired: two Missing-evidence bullets repointed from ev-ledger-10 to ev-ledger-20; ev-podcast-21's starlette and Debian values marked as :3-only measurements; req-03 now names ev-ledger-20's re-test; four rows restamped to commit 4ac09ba's time and the F6 row to the last of its records; Containerfile.ledger's caller path corrected to src/fin/adapters/citi_pdf.py:198; the activity log rejoined into one table; R3 corrected to five tiers with tier 2 also unexercised; the 24.5s figure separated into 17.3s transcode and ~7s suite | audits/evidence.md F13-F17, A10-A13 | both manifests, evidence/Containerfile.ledger, status.md, atj/cli.py | pending gate |
| 2026-09-17T19:20:00Z | A10 repair: `atj render judgment` now scores and checks every file before writing any, so a run that will refuse refuses having written nothing, and reports `forced_over_approval` in `--json` | audits/evidence.md A10 | atj/cli.py, tests/test_end_to_end.py | pending gate |

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