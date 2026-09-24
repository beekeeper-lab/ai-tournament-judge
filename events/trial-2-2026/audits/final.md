---
event_id: trial-2-2026
audit_scope: final-audit stage, the complete judging record of trial-2-2026 end to end (intake, evidence, judgments, consolidation, bracket, tournament, dossiers, public), including the eight prior stage audits; round two scoped to the repair diff de797ea..916a66a; round three scoped to 93cfb5e..957bc66 and the annotated tag; round four scoped to 9d1be78..d8a001a; round five scoped to e44385b..58cd942 (FA2, FA7, CF11 settlement); round six scoped to 61b3a0d..06b0d5b (FE1, FE4 re-runs)
audit_id: final
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.1.0
persona: judging-auditor@1.1.0
framework_commit: 06b0d5bf9738c06b249053bc8907c75a0c2d1f94
model_requested: claude-opus-5
model_used: claude-opus-5-5[1m]
started_at: '2026-09-24T02:48:05Z'
completed_at: '2026-09-24T12:18:34Z'
visibility: private
approval_state: approved
validation_state: valid
result: PASS WITH ADVISORIES
findings:
- id: FA1
  severity: minor
  scope: framework
  blocking: false
  summary: atj bracket verify --reproduce fails on the committed bracket.json because atj/cli.py:1039 compares whole rounds, including the winner field that atj bracket advance writes. The draw itself reproduces
  artifact: atj/cli.py:1033-1040
  repair: Leave the event alone. Add a W entry beside W25 so that reproduction compares rounds with winner excluded
  state: deferred
- id: FA2
  severity: minor
  scope: event
  blocking: false
  summary: The model-substitution override accepts claude-opus-5-5[1m] for five named artifacts. audits/tournament.md:13, audits/dossiers.md:13 and this audit also record that model against event.md:16, and no record accepts them
  artifact: overrides/ovr-trial-2-2026-model-substitution.md:36-37
  repair: Before atj event complete, the event-director records acceptance for the three audit artifacts, as a new override record or a dated amendment, and approves it with atj event approve
  state: repaired
- id: FA3
  severity: minor
  scope: event
  blocking: false
  summary: Two ledger defects no audit recorded. status.md:150 (14:53:00Z) sits above status.md:151 (14:52:44Z), and :151 itself says the :150 repairs came after it. The status.md:127 stamp 14:22:00Z is 77 s after 4fa5714 (14:20:43Z), the first commit that contains it
  artifact: events/trial-2-2026/status.md:127,150-151
  repair: Add one activity row that records both. Do not restamp. status.md is not a unit input, so the edit stales nothing
  state: repaired
- id: FA4
  severity: minor
  scope: event
  blocking: false
  summary: audits/consolidation.md:11 framework_commit 7ac67fb, and the whole consolidation-stage history (7ac67fb, 5b4c0ac, 4ce5cbb, a8cbc9b, 923ffce), can be reached only from origin/event/trial-2-2026-consolidation. PR 22 was squash-merged as c728437
  artifact: events/trial-2-2026/audits/consolidation.md:11
  repair: Before that branch is deleted, keep it or tag 923ffce, and record the ref in status.md
  state: repaired
- id: FA5
  severity: advisory
  scope: event
  blocking: false
  summary: Consolidation-stage stamps run ahead of the commits that contain them. summaries/*.md completed_at 18:52:00Z is committed in 7ac67fb at 18:21:39Z, and ledger rows :129-:135 (18:55-23:55Z) run ahead of every branch commit. consolidation.md:852-857 discloses this only from round two onward
  artifact: events/trial-2-2026/summaries/team-demos.md, summaries/team-scribe.md, status.md:129-135
  repair: Record only. Editing the summaries would stale bracket:draw and both dossier units. This is configuration F20 evidence
  state: open
- id: FA6
  severity: advisory
  scope: event
  blocking: false
  summary: 'No evidence:, judging: or consolidation: unit was ever recorded (status.md:17-49), although atj/event.py:907-941 derives all six. For those stages, drift is checked only by git history, which this audit re-checked'
  artifact: events/trial-2-2026/status.md:17-49
  repair: None for this event. Framework question for the next version, whether atj event status should name missing standard units
  state: open
- id: FA7
  severity: advisory
  scope: event
  blocking: false
  summary: Fourteen private artifacts are still approval_state draft (8 judgments, 2 summaries, bracket.md, matchups/mu-final-01.md, 2 pass reports) plus event.md. Nothing requires otherwise. Once the event is complete the state is frozen
  artifact: judgments/*/*.md, summaries/*.md, bracket.md, matchups/mu-final-01.md, matchup-passes/*.md, event.md
  repair: The event-director decides before completion whether to approve them or leave them draft, and records the choice in one ledger row
  state: repaired
- id: FA8
  severity: advisory
  scope: event
  blocking: false
  summary: status.md.bak is atj/event.py:1129's pre-advance backup. It is gitignored (.gitignore:27), untracked, read by nothing, and differs from status.md only in current_stage and last_updated
  artifact: events/trial-2-2026/status.md.bak
  repair: Optional. Delete it, as evidence F15 and judgments F11 did with earlier backups
  state: open
- id: FA9
  severity: advisory
  scope: framework
  blocking: false
  summary: All four units hold their original completed_at although each was recorded later, and no field records when. The status.md:177 phrase "the last edit to the dossiers" means the last content edit. The approval at 00:14:24Z also wrote both dossiers
  artifact: events/trial-2-2026/status.md:25,33,41,49,177
  repair: Framework. Add a recorded_at field to units, or define completed_at in the runbook
  state: deferred
- id: CF1
  severity: minor
  scope: event
  blocking: false
  summary: Carried DO2. The erratum at summaries/team-demos.md:426 is correct. Three judges name demo 06's byte-identical prompt, not four. The dossier (team-demos.md:110-113) carries three. public/ does not mention it
  artifact: events/trial-2-2026/summaries/team-demos.md:426
  repair: None in-event. The erratum stands at status.md:170, and the route to fix it is DOA8
  state: accepted
- id: CF2
  severity: minor
  scope: event
  blocking: false
  summary: Carried DO3. The erratum at summaries/team-scribe.md:203-204 is correct. Two judges (judge-backend.md:95, judge-product-agentic.md:106), not three, make the main.py:50 fix their top improvement. The dossier (team-scribe.md:191-193) says two
  artifact: events/trial-2-2026/summaries/team-scribe.md:203-204
  repair: None in-event. The erratum stands at status.md:170
  state: accepted
- id: CF3
  severity: minor
  scope: event
  blocking: false
  summary: Carried DO4. The erratum at summaries/team-scribe.md:166 is correct. PipelineStatus is credited by backend (:52,:115,:129), frontend-ux (:53,:114) and product-agentic (:140). Security-ops never names it and credits retry.py (:109,:117,:135). The dossier does not repeat the count
  artifact: events/trial-2-2026/summaries/team-scribe.md:160-166
  repair: None in-event. The erratum stands at status.md:170
  state: accepted
- id: CF4
  severity: advisory
  scope: framework
  blocking: false
  summary: Carried DOA8. There is still no errata route for audited summaries, and docs/0.5.0-beta-plan.md has no W entry for it (no errata, DOA8 or W26 text anywhere)
  artifact: docs/0.5.0-beta-plan.md
  repair: Add a W entry (W26) naming the three errata at status.md:170 as its evidence
  state: deferred
- id: CF5
  severity: advisory
  scope: framework
  blocking: false
  summary: Carried W21-W25, all present at docs/0.5.0-beta-plan.md:255-259, not fixed. FA1 is a sibling of W25
  artifact: docs/0.5.0-beta-plan.md:255-259
  repair: Next version
  state: deferred
- id: CF6
  severity: advisory
  scope: framework
  blocking: false
  summary: Carried evidence F14. atj/reports.py:41 still maps runs/ to model-run, and report validation globs *.md (atj/reports.py:716,786), so the 11 runs/*.json are still validated by nothing. This audit checked all 11 by hand for podman, --network none, --read-only, a :ro mount, --cap-drop ALL and uid 65534
  artifact: atj/reports.py:41
  repair: Next version, a sandbox-run schema
  state: open
- id: CF7
  severity: advisory
  scope: framework
  blocking: false
  summary: Carried intake F7, the event-director's decision. framework/templates/team-roster.md has eight identity fields, while teams.md:1-5 has three. Still open
  artifact: framework/templates/team-roster.md
  repair: The event-director decides. Does not hold the gate
  state: open
- id: CF8
  severity: advisory
  scope: framework
  blocking: false
  summary: Carried configuration F10, the event-director's decision. The submissions no longer carry absolute paths, because intake F8 repaired them. /home/gregg/... remains in all 11 runs/*.json command strings and in audits/consolidation.md. None is in dossiers/ or public/
  artifact: events/trial-2-2026/runs/*.json
  repair: The event-director decides whether the residue in a public repository is acceptable
  state: open
- id: CF9
  severity: minor
  scope: framework
  blocking: false
  summary: Carried configuration F20, the event-director's decision. Nothing validates timestamps. FA3 and FA5 are new instances
  artifact: atj/reports.py, atj/event.py
  repair: Next version
  state: open
- id: CF10
  severity: minor
  scope: framework
  blocking: false
  summary: Carried configuration F23, the event-director's decision. atj intake still writes model_used not-applicable, now at atj/intake.py:405-406
  artifact: atj/intake.py:405-406
  repair: Next version
  state: open
- id: CF11
  severity: advisory
  scope: framework
  blocking: false
  summary: Carried DOA2, open, and the event-director's decision. Every human approval in the stage was run by the orchestrator on a stated in-session delegation (dossier approval_note, override:22, status.md:167,177). The repository cannot show a human acted
  artifact: events/trial-2-2026/status.md:167,177
  repair: The event-director confirms the delegation in person. Attestations are the 1.0 line (docs/0.5.0-beta-plan.md:261-264)
  state: accepted
- id: CF12
  severity: advisory
  scope: event
  blocking: false
  summary: Carried DEA1, now closed. The model-substitution override is approval_state approved, approved_at 00:14:24Z, in c732850 (00:15:18Z)
  artifact: overrides/ovr-trial-2-2026-model-substitution.md:17-22
  repair: none
  state: repaired
- id: CF13
  severity: advisory
  scope: event
  blocking: false
  summary: Carried DGA1, confirmed and classified as no defect. The status.md:171 stamp 20:30:25Z precedes ef6d656 (20:31:18Z) by 53 s. A row stamped before its commit is the permitted direction. The defects are stamps after their commits (FA3, FA5)
  artifact: events/trial-2-2026/status.md:171
  repair: none
  state: accepted
- id: FB1
  severity: minor
  scope: framework
  blocking: false
  summary: W28 (docs/0.5.0-beta-plan.md:262) misstates the code. It says a unit re-recorded after a stale digest carries no trace. In fact atj/event.py:826-829,845-846 stamps a changed-digest re-record with the clock. This event kept the original times only because the operator passed --completed-at (status.md:161,164). The gap is that no field records when a re-recording happened
  artifact: docs/0.5.0-beta-plan.md:262
  repair: Restate W28 from atj/event.py:818-846. When the digest is unchanged, the old time stands and the re-record leaves no trace. When the digest changes, the default is now() and the work time is lost unless --completed-at is passed. Keep the recorded_at fix
  state: repaired
- id: FB2
  severity: minor
  scope: event
  blocking: false
  summary: The repair row was first stamped 02:59:30Z, 4 s after its own commit 574f95c (02:59:26Z, on origin by 02:59:27Z). It was restamped to 02:59:26Z, and the amend 916a66a was made with GIT_COMMITTER_DATE forced back to 02:59:26Z. The local reflog shows the force-push at 02:59:34Z, so the committer date is not when 916a66a was made. Git commit time is the independent clock that FA3, FA5 and DGA1 relied on. The row does not disclose the restamp, and it reads "without restamping"
  artifact: events/trial-2-2026/status.md:179; commit 916a66a
  repair: 'Do not rewrite history again. Add one ledger row with the facts: first stamp 02:59:30Z in 574f95c (02:59:26Z), restamped, amended with a forced committer date, real amend at or before the 02:59:34Z push. From here on, restamp rows and never commit dates'
  state: repaired
- id: FB3
  severity: advisory
  scope: event
  blocking: false
  summary: status.md:4 last_updated is still 00:14:43Z although rows :178-:179 (02:58:32Z, 02:59:26Z) were added. This is configuration F22 and tournament R4 recurring
  artifact: events/trial-2-2026/status.md:4
  repair: Bump last_updated in the FB2 disclosure commit
  state: repaired
- id: FB4
  severity: advisory
  scope: event
  blocking: false
  summary: The tag trial-2-2026-consolidation-history is lightweight. It points at 923ffce1dd15f9df49a619fcebfb5bd55f95eb2b locally and on origin, but it records no tagger, date or reason
  artifact: refs/tags/trial-2-2026-consolidation-history
  repair: Optional. Replace it with an annotated tag on the same commit
  state: repaired
- id: FC1
  severity: minor
  scope: framework
  blocking: false
  summary: The restated W28 (docs/0.5.0-beta-plan.md:262) gets the code right (atj/event.py:831-846) but misattributes its evidence. It says bracket:draw and the dossier units were re-recorded after a digest change, citing status.md:161,164,177. :161 is matchup:mu-final-01, not bracket or dossier. :177 is the first recording of both dossier units, which first appear in c732850. Only :164 (bracket:draw) and :161 (matchup) are re-records after a digest change
  artifact: docs/0.5.0-beta-plan.md:262
  repair: Restate the evidence clause. bracket:draw (:164) and matchup:mu-final-01 (:161) were re-recorded after a digest change with --completed-at set to the original work time. Both dossier units were first recorded (:177) with --completed-at set to their last content edit. In neither case does the ledger unit record when it was recorded
  state: repaired
- id: FC2
  severity: advisory
  scope: event
  blocking: false
  summary: The last-row wording at status.md:181 was edited again in 957bc66 (03:02:01Z), after that row's own stamp. last_updated stays 03:01:53Z, which is 710a4db. The edit is a wording clarification (:180 to :179), and the commit message records it
  artifact: events/trial-2-2026/status.md:4,181
  repair: None required. Bump last_updated with the next ledger edit
  state: repaired
- id: FD1
  severity: advisory
  scope: event
  blocking: false
  summary: status.md:182 puts the round-three audit (9d1be78, 03:03:24Z) and its repair (d8a001a) in one row. The row is stamped at the repair commit and reads PASS WITH ADVISORIES for a repair that no audit had yet seen. Rows :178/:179 and :180/:181 kept audit and repair apart. Round four has now audited the repair, and every fact in the row is correct
  artifact: events/trial-2-2026/status.md:182
  repair: None required. From now on, write the audit row and the repair row separately, and mark the repair not-audited until it is re-audited
  state: accepted
- id: FE1
  severity: minor
  scope: event
  blocking: false
  summary: The four re-recorded units (status.md unit rows for bracket:draw, matchup:mu-final-01 and both dossiers) now carry completed_at 12:13:47Z-12:13:48Z on 2026-09-24. atj/event.py:820-829 defines completed_at as the time the work finished, which was 01:55:10Z, 17:26:17Z and 20:30:25Z on 09-23. status.md:196 discloses it, but the ledger values are wrong, and completion freezes them
  artifact: events/trial-2-2026/status.md:17-49
  repair: 'Before advancing to complete, re-record each unit with --completed-at set to its work time: bracket:draw 2026-09-23T01:55:10Z, matchup:mu-final-01 2026-09-23T17:26:17Z, both dossier units 2026-09-23T20:30:25Z. Add one row'
  state: repaired
- id: FE2
  severity: advisory
  scope: event
  blocking: false
  summary: The new override sets started_at equal to completed_at, 12:13:16Z (overrides/ovr-trial-2-2026-model-substitution-audits.md:14-15), so it records no real start time. All its citations resolve
  artifact: overrides/ovr-trial-2-2026-model-substitution-audits.md:14-15
  repair: None required
  state: accepted
- id: FE3
  severity: advisory
  scope: event
  blocking: false
  summary: Both summaries are now approved while still carrying the three wrong counts (CF1-CF3). Their approval_note does not point to the errata at status.md:170, so a reader of the approved summary cannot see them. status.md:195 says so, and W26 is the fix
  artifact: summaries/team-demos.md, summaries/team-scribe.md
  repair: None in-event. W26
  state: accepted
- id: FE4
  severity: advisory
  scope: event
  blocking: false
  summary: Round five landed after final-audit-passed was set in 7b9ad0f (03:04:56Z). This is correct in kind, because FA2, FA7 and CF11 were pre-completion conditions and not gate conditions. But the gate and the 03:04:22Z approval of this file attest to its round-four text. This round-five edit changes the file, so final:audit goes stale and the approval covers an earlier version
  artifact: events/trial-2-2026/audits/final.md
  repair: Re-approve this file, re-record final:audit, and re-set the gate on it, as listed under Recommended commands, round five
  state: repaired
- id: FF1
  severity: advisory
  scope: event
  blocking: false
  summary: final:audit was recorded with completed_at 12:17:58Z, the commit time of the round-five report, not the 12:16:24Z this report recommended as its completed_at. Both are defensible. The row at status.md:198 states which one was used
  artifact: events/trial-2-2026/status.md:50-57,198
  repair: None required
  state: accepted
approved_by: event-director
approved_at: '2026-09-24T12:18:00Z'
approval_note: Re-approved after round five on the event-director's delegation, 2026-09-24
---

# Final Event Audit: the complete judging record, first pass

`team_id`, `commit` and `evidence_package_id` are `null` because this audit covers
the whole event: two teams, two pins, two evidence packages, one matchup, one
public artifact and eight prior stage audits. New findings are `FA1`-`FA9`.
Items carried from earlier audits are `CF1`-`CF13`, and each names its original
code.

Every event artifact, including the eight prior audits, was treated as untrusted
evidence. I did not accept a count, a total or a repair because an earlier audit
asserted it. I re-derived the three consolidated-summary errata from the eight
judgments, the two panels with `atj score`, the matchup with `atj matchup` from
the pass front matter, and the draw with `atj bracket verify --reproduce` from a
roster I wrote by hand from `teams.md`.

**Disclosure about this audit.** It ran on `claude-opus-5-5[1m]` against
`event.md:16`'s `claude-opus-5`. That is part of `FA2`.

## Result

**Round six: PASS WITH ADVISORIES.** FE1 and FE4 are repaired. It adds `FF1` (advisory). Nothing at minor or above is open. The event may advance to complete after the closing sequence in round six.

**Round five: PASS WITH ADVISORIES.** FA2 and FA7 are repaired and CF11 is accepted. It adds `FE1` (minor, the units lost their work times) and `FE2`-`FE4` (advisory). The event may advance to complete after the three re-runs listed under round five. The `FE1` repair is strongly recommended first.

**Round four: PASS WITH ADVISORIES.** FC1 and FC2 are repaired. It adds `FD1` (advisory). Nothing is open at minor or above from rounds two to four. The gate may be set.

**Round three: PASS WITH ADVISORIES.** It adds `FC1` (minor, framework) and `FC2` (advisory). FB1-FB4 are repaired. The gate may be set.

**Round two: PASS WITH ADVISORIES.** It adds `FB1`-`FB4`: two minor, two advisory, none blocking or major. See [Round two](#round-two-the-repair-diff-de797ea916a66a). The gate may still be set.

**Round one: PASS WITH ADVISORIES.** There is no blocking finding and no major finding.
Four new findings are minor (`FA1`-`FA4`) and five are advisory (`FA5`-`FA9`).
Of the thirteen carried items, six are minor or advisory framework items, two are
closed and five are accepted or deferred. None holds the gate.

The `final-audit-passed` gate **may be set**. I tested each finding against the
template's blocking triggers:

- **Arithmetic.** Both panels and the matchup reproduce with zero differing keys.
- **Versions.** Every rubric and persona version matches `framework/personas.md`
  and the rubric front matter. The model deviation is recorded truthfully in
  every artifact.
- **Disagreement.** There is no unresolved severe disagreement. Both `NE`
  triggers are adjudicated.
- **Execution.** Execution was safe. All 11 runs were isolated.
- **Privacy.** No private information is in public output.
- **Scores.** No score was moved without authority. All eight judgment score
  blocks are identical across every commit.
- **Official totals.** No official total is claimed while an `NE` blocks it.
- **Gates.** No gate was set on a failing or unapproved audit.

Three items are pre-completion conditions, not gate conditions:

- `FA2`: the event-director accepts the model used by the three audits.
- `FA7`: the event-director decides the approval state of the draft private
  artifacts.
- `CF11`: the event-director confirms the approval delegation.

All three belong to Gregg as event-director. Each should be settled before
`current_stage: complete` freezes the record.

## Scope and artifacts inspected

- **The event directory.** The whole of `events/trial-2-2026/` as tracked at
  `10c7973`: `event.md`, `teams.md`, `status.md` (85 activity rows), 2
  submissions, 2 manifests, 2 Containerfiles, 11 run records, 8 judgments, 2
  adjudications, 2 summaries (`.md` and `.json`), `bracket.json` and `bracket.md`,
  3 override records, `matchups/mu-final-01.{md,json}`, 2 pass reports, 2
  dossiers, `public/mu-final-01.md`, the 8 prior audits, and the untracked
  `status.md.bak`.
- **Outside the event.** `framework/personas.md`, the four rubric front matters,
  `framework/templates/audit-report.md`, `framework/policies/`,
  `docs/0.5.0-beta-plan.md` (W15-W25), `atj/event.py`, `atj/cli.py`,
  `atj/reports.py` and `atj/intake.py`.
- **Checkouts.** Both pinned checkouts under `workspaces/trial-2-2026/`. They are
  detached at `dc35f6962130…` and `67969dd9479c…`, with a clean worktree.
- **Git history.** The history of every event artifact, and the remote branch
  `origin/event/trial-2-2026-consolidation`.

The working tree was clean at the start. The only file this audit wrote is this
report.

## Deterministic validation results

| Command | Result |
|---|---|
| `python3 -m atj event validate events/trial-2-2026` | **PASS**, 0 problems, stage final-audit |
| `python3 -m atj event status events/trial-2-2026` | stage `final-audit`, 2 eligible, units `{'complete': 4}`, gate `final-audit-passed` pending, nothing stale |
| `python3 -m atj validate reports events/trial-2-2026` | **PASS WITH ADVISORIES**, 33 artifacts, 0 blocking/major/minor, 1 advisory: `foreign-team` on `dossiers/team-scribe.md` (confirmed match-public only; see Privacy) |
| `python3 -m atj validate publication` on `public/mu-final-01.md` and on each dossier | **CLEAR**, 0 blocking on all three |
| `python3 -m atj release-check` | **PASS**, all ten sections |
| `python3 -m pytest tests/ -q` | 520 passed, 5 skipped, 288 subtests passed |
| `python3 -m atj bracket verify bracket.json --event-dir events/trial-2-2026` | **PASS (constraints re-derived from the roster)** |
| `python3 -m atj bracket verify bracket.json --reproduce <hand-built roster>` | **FAIL**, "bracket does not reproduce from its recorded seed and roster". The cause is `FA1` |
| same, on the committed file with `winner` set to `null` | **PASS (reproduced from seed)** |
| same, on `bracket.json` at `321efa0` (bracket gate, before advance) | **PASS (reproduced from seed)** |
| `git diff 321efa0 HEAD -- bracket.json` | one line: `"winner": null` → `"team-demos"` |
| `python3 -m atj event overrides events/trial-2-2026` | "no stage gate was ever bypassed" |
| `atj score judgments/team-scribe --json` vs `summaries/team-scribe.json` | **0 differing keys** (flattened), exit 1, finalization blocked |
| `atj score judgments/team-demos --json` vs `summaries/team-demos.json` | **0 differing keys** (flattened), exit 1, finalization blocked |
| `atj matchup <pass front-matter comparisons> --event-dir` vs `matchups/mu-final-01.json` | **identical** (`==` true) |
| `atj.event.derive_digests` vs the four recorded units | all four match; `stale_units` empty |

All scratch output went to the session scratchpad. Nothing was written into the
event.

## 1. Arithmetic, re-derived

**team-scribe.** The weighted points are functional 5.00, product 6.00,
engineering 6.00, reliability 4.00, security 5.50 and innovation 6.00, which sum
to **32.50** = `provisional_total`. `agentic` is `NE` from judge-frontend-ux and
judge-security-ops. `atj score` computes 7.50 over the two scored judges and
correctly excludes it. The result is `total: null`, `display_total: null`,
`finalized: false`, with `blocked_reasons` naming the accepted adjudication and
`adjudication_required: []`.

**team-demos.** The weighted points are product 12.00, agentic 10.50,
engineering 9.00, reliability 5.50, security 7.50 and innovation 8.00, which sum
to **52.50** = `provisional_total`. `functional` is `NE` from the same two judges
and is excluded. Otherwise the result has the same shape.

**Checks.** Each weighted value is `mean / 5 × weight`, with weights 25/15/15/15/10/10/10
read through `atj score`. Every criterion is `aligned`, and none has an outlier.

**Matchup.** I extracted the comparisons from the two pass front matters. A-first
is `{functional 1, product 2, agentic 0, engineering 1, reliability 0, security 1,
innovation 0}`, with team-demos presented first. B-first is `{-2, -2, -1, -1, 0,
-1, 0}`, with team-scribe presented first. Re-running `atj matchup` gives:

- combined margin **50.0**
- a-first 40.0, b-first normalized 60.0
- `confirmed`, winner team-demos
- no order disagreement

The close-call band is 5 (`framework/rubrics/head-to-head.md:5`). Agentic and
functional differ between the passes in magnitude only, never in sign. The
output is identical to the committed file.

## 2. Gates and stage transitions against git

For each gate I found the first commit whose `status.md` front matter records it
`passed`. I then read the stage audit as it stood in that commit's tree.

| Gate | Set in (commit time, UTC) | Audit in that tree | Stage in that tree |
|---|---|---|---|
| configuration-audited | `a8a0f4e` 22:34:58Z 09-21 | PASS WITH ADVISORIES, approved | intake |
| roster-frozen | `2dec830` 23:55:52Z 09-21 | PASS WITH ADVISORIES, approved | intake → `b9b7554` evidence |
| evidence-validated | `75d24b0` 01:11:35Z 09-22 | PASS WITH ADVISORIES, approved | initial-judging |
| judgments-audited | `4fa5714` 14:20:43Z | PASS WITH ADVISORIES, approved | consolidation |
| consolidation-audited | `c728437` 21:27:19Z (squash; see `FA4`) | PASS WITH ADVISORIES, approved | bracket |
| bracket-audited | `321efa0` 14:53:55Z 09-23 | PASS WITH ADVISORIES, approved | tournament |
| tournament-audited | `f9bbfb5` 18:54:07Z | PASS WITH ADVISORIES, approved | dossiers |
| dossiers-approved | `c732850` 00:15:18Z 09-24 | PASS WITH ADVISORIES, approved | final-audit |

No stage's work began before the previous gate:

- the judgments at `5752c04` came after `75d24b0`
- the bracket at `abc7e7a` came after `c728437`
- the matchup at `77fcc6a` came after `321efa0`
- the dossiers at `ffcf150` came after `f9bbfb5`

The consolidation stage's own commits sit on the remote branch, from `7ac67fb`
at 18:21:39Z to `923ffce` at 21:12:42Z, all after `4fa5714`. The squash tree
equals that branch's tip.

The rubrics show no change after judging began. `submission-evaluation`,
`head-to-head` and `panel-consolidation` were last changed in `54caa05`
(09-17), and `bracket-assignment` in `7579c3e` (09-16). The one persona-file
change during the event was `196aa42` at configuration, before any judgment, and
it is a whitespace/line join. `event.md` changed after judging only in prose, the
disclosure pointer (`abc7e7a`, `ebeb4bd`, `92e922e`). Its front matter, weights,
personas and bracket policy did not change. Neither manifest has a commit after
`75d24b0`.

## 3. Versions and identity

- **Rubrics.** Every artifact records `submission-evaluation@1.1.0` (rubric
  front matter `version: 1.1.0`), or `head-to-head@1.1.0` for the matchup
  artifacts. The bracket records `bracket-assignment@1.0.0`, and both match their
  files.
- **Personas and skills.** Every persona and skill version matches
  `framework/personas.md:35-49`:
  - judges `@1.1.0`
  - `panel-consolidator@1.1.0`
  - `matchup-judge@1.1.0`
  - `judging-auditor@1.1.0`
  - `prepare-submission@1.1.0`
  - `consolidate-judgments@1.0.0`, `build-bracket@1.0.0`, `build-team-dossier@1.0.0`
    and `run-judging-event@1.0.0`

  `release-check` version-skew passes.
- **Framework.** `VERSION` is `0.4.0-beta`.
- **Pins.** `teams.md`, both submissions, both manifests, all eight judgments,
  both summaries, both adjudications and both dossiers carry the same full
  commit for their team, and the evidence package IDs embed it. Both checkouts
  are detached at those hashes.
- **Framework commits.** Every recorded `framework_commit` resolves as an
  ancestor of HEAD except `audits/consolidation.md:11` (`FA4`).
- **Models.** The judgments, adjudications, summaries, manifests and first six
  audits record `claude-opus-5`. The tournament and dossier artifacts and two
  audits record `claude-opus-5-5[1m]` (`FA2`).

## 4. Judge independence

The four judgments per team share one `started_at` (10:28:16Z for team-scribe
and 10:37:22Z for team-demos), which matches a concurrent launch. Each has its
own `judge_run_id`. No judgment names another judge persona anywhere in its
text.

All eight score blocks hash identically at every commit in each file's history.
`judgments/team-demos/judge-security-ops.md` has five commits, and two of them
fall after the judgments gate (`4fa5714` and `c728437`). Both edit prose only:

- "seven" → "seventeen"
- the egress guard narrowed to three of five forms, which matches
  `runs/team-demos-egress-guards-01.json`

Each carries a dated amendment checkbox naming the event director as the one who
acted. The consolidation audit reviewed them.

That is an edited judgment. I do not raise it as blocking, because:

- no score, confidence or anchor moved
- each edit makes the text agree with a run record
- each is disclosed in the file
- a later audit round verified each one

The two matchup passes started 8 s apart (a-first 17:23:53Z, b-first 17:24:01Z,
`status.md:152`). Each pass's front matter holds only its own comparisons.

## 5. NE and adjudication

Both `NE` splits are two of four judges (frontend-ux and security-ops), on
`agentic` for team-scribe and `functional` for team-demos. `ADJ-1` and `ADJ-2`
(`status.md:86-87`) resolve them. Both adjudications (`adjudications/*.md`) carry:

- `resolution: resolved`
- `decision_authority: human-official`
- `decided_by: event-director`
- `resolved_score: NE`
- `approved_at: 2026-09-22T18:07:45Z`

`atj score` records the resolution "alongside the source scores; no source score
was modified".

No official total is claimed anywhere. `32.5` and `52.5` appear only in private
artifacts (`summaries/*`, `bracket.md:49`, `status.md:79-80,129`), each labelled
provisional. The dossiers show `NE` for the criterion with no points column and
no partial mean (`dossiers/team-scribe.md:136`). `matchups/mu-final-01.md:175`
attests that no total was used. The public artifact carries
`scores_published: false` and no number.

## 6. The carried errata (status.md:170), re-derived

I counted judges per claim from the eight judgments, not from the summaries or
the dossiers audit.

- **DO2 → `CF1`, correct.** Demo 06's byte-identical prompt is named by
  judge-backend (`:51`, `:107`, `:168`), judge-frontend-ux (`:166`) and
  judge-product-agentic (`:256`, `:454-458`). judge-security-ops `:49` and `:153`
  discuss demo 06's gate, never the constant prompt. That makes three, and
  `summaries/team-demos.md:426` says "all four".
- **DO3 → `CF2`, correct.** Only `judge-backend.md:95` and
  `judge-product-agentic.md:106` make narrowing `main.py:50` a
  "Highest-value improvement". Frontend-ux (`:82-166`) and security-ops
  (`:91-179`) choose other fixes. That makes two, and
  `summaries/team-scribe.md:203-204` says three.
- **DO4 → `CF3`, correct.** `PipelineStatus` is credited by the three judges
  listed in `CF3`. Security-ops mentions only `src/utils/retry.py`.
  `summaries/team-scribe.md:166` says "All four credit the design".

**No team-facing or public artifact repeats a wrong count:**

- `dossiers/team-demos.md:112` says "three judges" and names them.
- `dossiers/team-scribe.md:192-193` says "The backend and product reviewers both".
- The team-scribe dossier makes no count claim about `PipelineStatus`. Its
  retry bullet (`:104-107`) names backend, product and security. Frontend-ux has
  no `retry.py` mention, so this is correct.
- `public/mu-final-01.md` makes none of the three claims.

I also re-checked two "all four" claims in the dossiers. The empty-hostname claim
at `dossiers/team-demos.md:217` holds: all four judgments mention it, including
frontend-ux `:154` and product-agentic `:430`. The pin checks all resolve
(`qt_app.py:11`, `main.py:50`, `pytest.ini:1`, `clear_the_pile_hardened.py:42-43`,
`act.py:106-107`, `toolbox.py:47-51`). Every run-record path in both dossiers
exists. Of 60 file citations, the only non-resolving one is `setup.cfg` at
`dossiers/team-scribe.md:234`. It is named as a section-name convention, not as
a file in the tree, and is correct.

## 7. Units against their inputs

| Unit | Inputs' last commit | Recorded in | Digest now | `completed_at` |
|---|---|---|---|---|
| `bracket:draw` | `bracket.json` `f9bbfb5` (winner), `teams.md` `2dec830`, summaries `c728437` | `f9bbfb5` (row :164, 18:53:23Z) | matches | 01:55:10Z, the draw time |
| `matchup:mu-final-01` | `mu-final-01.md` `d5c8f32` 18:49:41Z; `.json` and passes `77fcc6a` | `9f75c13` 18:52:39Z | matches | 17:26:17Z, the matchup time |
| `dossier:team-demos` | dossier `c732850` (approval fields); summary `c728437`; matchup `d5c8f32` | `c732850`, after the approve | matches | 20:30:25Z, the last content edit |
| `dossier:team-scribe` | same | `c732850` | matches | same |

Each recording postdates the last edit to its inputs, and each digest re-derives
to the recorded value. The `completed_at` fields describe the work, not the
recording (`FA9`). No `evidence:`, `judging:` or `consolidation:` unit exists
(`FA6`). For those stages I checked by git instead:

- the manifests are unchanged since the evidence gate
- the judgment scores are unchanged throughout
- the summaries have one commit, `c728437`

## 8. Ledger against git

The 85 rows were machine-checked. Two pairs descend:

- `:135→:136`, 23:55:00Z → 21:11:39Z. `:136` itself and
  `audits/consolidation.md:852-857` disclose it.
- `:150→:151`, 14:53:00Z → 14:52:44Z. Not disclosed (`FA3`).

Six stamps come after the first commit that contains them:

- `:127` (77 s, `FA3`)
- `:131-:135` (by 761-8861 s against `c728437`). The consolidation audit
  disclosed these as reconstructed.

The summaries' own `completed_at` is a seventh, undisclosed, instance (`FA5`).
The operator rows at `:153`, `:166` and `:170` record the orchestrator's own
defects plainly.

## 9. Privacy and publication

- `event.md:14` `public_scores: false` is unchanged. The disclosure override
  (`overrides/ovr-trial-2-2026-publication-disclosure.md`) keeps it.
- `public/` holds one file. It is `visibility: public`, `approved_by:
  event-director`, `approved_at: 20:17:22Z`, `scores_published: false`, with a
  short `framework_commit` (W21).
- The public file names no model, persona, run ID, commit, package ID or score.
  Its execution claims match the manifest (`evidence/team-demos/manifest.md:109-113`)
  and `runs/team-demos-egress-guards-01.json`. `is_localhost` refused all six
  hostile forms, and "a localhost check" is singular and refers to that one guard.
- Both dossiers are `visibility: team`.
- `dossiers/team-demos.md` does not name its opponent. `dossiers/team-scribe.md:340-342`
  names it by display name, in the match outcome only. Neither dossier contains
  the other team's commit, package ID or provisional sum. No judge persona string
  appears in either dossier.
- All 11 runs used podman 6.1.0 with `--network none`, `--read-only`, a `:ro`
  source mount, `--cap-drop ALL` and `--user 65534:65534`. Nothing ran on the
  host.
- Absolute operator paths remain only in private artifacts (`CF8`).

## 10. status.md.bak

The file is `atj/event.py:1129`'s backup, written at 00:14:43Z local-mtime by the
advance to final-audit. `.gitignore:27` (`*.bak`) ignores it, and no commit has
ever tracked it. It differs from `status.md` only in `current_stage: dossiers`
and `last_updated`. No `atj` code reads it, so no gate, unit or validator can
see it. It does not matter (`FA8`).

## Findings

| Severity | Rule | Artifact | Scope / blocking | Finding | Required repair |
|---|---|---|---|---|---|
| minor | reproducibility of the draw | `atj/cli.py:1033-1040`; `bracket.json:73` | framework / no | **FA1.** `--reproduce` compares `rebuilt["rounds"] != result["rounds"]`. `atj bracket advance` wrote `winner: team-demos`, so every completed bracket fails reproduction. The draw does reproduce: stripped of `winner` it passes, and so does the `321efa0` copy. The one-line diff shows only the winner moved | W entry beside W25. Compare rounds with `winner` excluded |
| minor | version and identity | `overrides/ovr-trial-2-2026-model-substitution.md:36-37`; `audits/tournament.md:13`; `audits/dossiers.md:13`; this file | event / no | **FA2.** The override names five artifacts. Three audits also ran on `claude-opus-5-5[1m]` against `event.md:16`, and nothing accepts that. The model is recorded truthfully, so this is a missing acceptance, not a hidden mismatch | The event-director extends the acceptance to the three audits before `complete` |
| minor | ledger order | `status.md:127,150-151` | event / no | **FA3.** `:150` is above `:151` and 16 s later. `:151`'s text says the `:150` repairs followed it. `:127` is stamped 77 s after its first commit | One activity row recording both. No restamp |
| minor | provenance durability | `audits/consolidation.md:11` | event / no | **FA4.** `7ac67fb` and the consolidation stage's five commits can be reached only from `origin/event/trial-2-2026-consolidation` | Keep the branch, or tag `923ffce`, and note the ref in `status.md` |
| advisory | timestamps (F20) | `summaries/*.md` `completed_at`; `status.md:129-135` | event / no | **FA5.** Stamps run 30 min to 2.5 h ahead of their commits. Only round two onward is disclosed | Record only |
| advisory | unit coverage | `status.md:17-49` | event / no | **FA6.** No evidence, judging or consolidation units. Checked by git instead | None this event |
| advisory | approval state | 14 private artifacts plus `event.md` | event / no | **FA7.** Still `draft` | The event-director's decision before `complete` |
| advisory | stray file | `status.md.bak` | event / no | **FA8.** Ignored backup, read by nothing | Optional delete |
| advisory | unit semantics | `status.md:25,33,41,49,177` | framework / no | **FA9.** `completed_at` is held at the work time, and no recorded-at field exists | Framework |

## Carried forward

| Code | Origin | Current state | Owner | Blocks final gate? |
|---|---|---|---|---|
| CF1 | dossiers DO2, `status.md:170` | Erratum verified correct (3 judges). The summary is unedited by decision. The dossier is correct. Public is silent | orchestrator (record); framework via CF4 | No. It is a private summary, no score depends on it, and the team-facing copy is right |
| CF2 | dossiers DO3 | Verified correct (2 judges). The dossier is correct | same | No, same reason |
| CF3 | dossiers DO4 | Verified correct (3 judges). The dossier makes no count claim | same | No, same reason |
| CF4 | dossiers DOA8 | Deferred. No W entry exists yet | framework maintainer | No. Framework scope |
| CF5 | tournament W21-W25 | Deferred at `docs/0.5.0-beta-plan.md:255-259` | framework maintainer | No. Framework scope |
| CF6 | evidence F14 | Open. The 11 runs were checked by hand here | framework maintainer | No. Framework scope. The runs verify |
| CF7 | intake F7 | Open | **Gregg (event-director)** | No. Framework template decision |
| CF8 | configuration F10 | Repaired in the submissions. Residue in runs and consolidation audit | **Gregg** | No. It is in private artifacts, and disclosure was settled for a public repository |
| CF9 | configuration F20 | Open, with new instances FA3 and FA5 | **Gregg** | No. Framework |
| CF10 | configuration F23 | Open, now `atj/intake.py:405-406` | **Gregg** | No. Framework |
| CF11 | dossiers DOA2 | Open. Approvals were run by the orchestrator on delegation | **Gregg** | No. This is the framework's attestation gap, and Gregg's confirmation is a pre-completion step |
| CF12 | dossiers DEA1 | Closed. The override was approved at 00:14:24Z in `c732850` | - | No |
| CF13 | dossiers DGA1 | Confirmed (53 s). Not a defect | - | No |

## Advisories

`FA5`-`FA9` and the advisory carried items are listed above. One more
observation for the trial record: the three errata are all the same direction
of error, overcounting corroboration by one judge. This is the direction the
consolidation audit found ten times. Once the errata are recorded, no
team-facing artifact inherits them, because the dossier writers re-counted from
the judgments.

## Completion gate

- [x] No blocking findings
- [x] No major findings
- [x] Calculations valid (`atj score` x2, `atj matchup`, bracket reproduced on the draw)
- [x] Evidence references resolve (sampled: 60 dossier file citations, 6 pin line checks, 11 run records)
- [x] Version and identity checks pass (model deviation recorded; acceptance gap is `FA2`)
- [x] Privacy boundary passes
- [x] Every finding recorded in `findings:` with a `scope` and a `blocking` flag
- [ ] Approved with `atj event approve <this file>`

## Recommended commands

The orchestrator runs these. This audit ran none of them.

```bash
# 1. Event-director approves this audit
python3 -m atj event approve events/trial-2-2026/audits/final.md --official event-director
# 2. Record the final-audit unit (atj/event.py:994-1002 digests audits/final.md)
python3 -m atj event unit events/trial-2-2026 record --id final:audit --stage final-audit \
  --output audits/final.md --audit-result "PASS WITH ADVISORIES"
# 3. Set the gate
python3 -m atj event gate events/trial-2-2026 final-audit-passed passed --audit audits/final.md
# 4. Before advancing to complete: FA2 acceptance record, FA7 decision, CF11 confirmation
#    (all Gregg), then approve any new override record:
python3 -m atj event approve events/trial-2-2026/overrides/<new-record>.md --official event-director
# 5. Ledger row for FA3 and this audit; W entries for FA1 and CF4 in docs/0.5.0-beta-plan.md;
#    keep or tag the consolidation branch (FA4):
git tag trial-2-2026-consolidation-history 923ffce
# 6. Re-verify, then advance
python3 -m atj event validate events/trial-2-2026 && python3 -m atj release-check
python3 -m atj event advance events/trial-2-2026
# Optional (FA8)
rm events/trial-2-2026/status.md.bak
```

## Round two: the repair diff `de797ea..916a66a`

Scope: `git diff de797ea..916a66a`. It adds two rows to `status.md`, which are
now `:178` and `:179`, and W26-W28 at `docs/0.5.0-beta-plan.md:260-262`. It also
covers the tag `trial-2-2026-consolidation-history`, and the amend of `574f95c`
into `916a66a`. At `916a66a`: `atj event validate` gives PASS, 0 problems.
`atj release-check` gives PASS. `atj event status` shows 4 units complete and
gate pending.

### What landed

| Round-one item | Repair | Verified against | Verdict |
|---|---|---|---|
| FA1 | W27 | `atj/cli.py:1039` is `if rebuilt["rounds"] != result["rounds"]:`, as cited. W27 sits beside W25 (`:259`) | correct, deferred |
| FA3 | row `:179` | `:150` is 14:53:00Z and sits above `:151` at 14:52:44Z. `:127` is 14:22:00Z, and its first containing commit `4fa5714` is 14:20:43Z, 77 s earlier. All three facts match `status.md` | repaired |
| FA4 | tag | `git ls-remote --tags origin` shows `923ffce1dd15…` for `refs/tags/trial-2-2026-consolidation-history`, and `rev-parse` matches locally. `923ffce` is the consolidation branch tip. The ledger records the ref at `:179` | repaired (FB4 advisory) |
| FA9 | W28 | `atj/event.py:818-846` | the W entry is inaccurate (`FB1`) |
| CF4 | W26 | Summary digests enter the dossier unit at `atj/event.py:949` and `bracket:draw` at `:974`, so an edit to a summary stales them as W26 says. The three counts are CF1-CF3 | correct, deferred |

The round-one audit row at `:178` (02:58:32Z) matches `de797ea`'s commit time
and follows this report's `completed_at` (02:55:42Z). Its counts match
round one. The two new rows ascend.

### The restamp and forced committer date (`FB2`)

**Facts from git.**
- `574f95c`: author and committer both 1790218766, which is 02:59:26Z. The
  remote-tracking reflog shows it on origin at 02:59:27Z. Its row read 02:59:30Z,
  a stamp 4 s after the commit that contains it. That is the FA3 and FA5 defect
  class.
- `916a66a`: the amend. Its tree differs from `574f95c` only in that stamp.
  Author and committer are again both 02:59:26Z. The remote-tracking reflog shows
  the force-push at 02:59:34Z, so the amend was made between 02:59:27Z and
  02:59:34Z. `574f95c` is no longer on any remote ref.

**Judgment.**
- **The restamp is acceptable and correct in direction.** A row may equal or
  precede its commit (CF13). 02:59:26Z is plausibly when the work was committed.
- **Forcing `GIT_COMMITTER_DATE` is a defect.** The difference is seconds, so the
  size does not matter. What matters is which clock it corrupts. Every
  timestamp finding in this event, including FA3, FA5, CF13 and consolidation F24
  and F25, was found by comparing ledger stamps against git's committer time,
  because that is the one clock the operator does not type. Setting it by hand
  makes a later row-versus-commit check pass by construction. It was also
  unnecessary: an amend with the real committer date (at or before 02:59:34Z)
  would already have put the restamped row before its commit.
- **It is not blocking.** It is inside the repair commit, it touches no score or
  artifact, the author date is original, and this report records it.
- **The ledger should disclose it.** The row at `:179` says "without restamping"
  about FA3's rows while its own stamp was restamped. And without a row, the
  only other record is a local reflog that dies with this clone. A second
  history rewrite would cost more than a disclosure row, so the repair is a new
  row and not another amend.

### Findings, round two

| Severity | Rule | Artifact | Scope / blocking | Finding | Required repair |
|---|---|---|---|---|---|
| minor | accuracy of the deliverable | `docs/0.5.0-beta-plan.md:262` | framework / no | **FB1.** W28 describes the unchanged-digest path as the stale-digest path. With a changed digest, `atj/event.py:845-846` stamps `now()`. This event kept work times only by passing `--completed-at` (`status.md:161,164`) | Restate W28 from `atj/event.py:818-846` |
| minor | independent clock | commit `916a66a`; `status.md:179` | event / no | **FB2.** Committer date forced back to 02:59:26Z. The amend was made at or before 02:59:34Z. Not disclosed | A disclosure row, no further rewrite. From here on, restamp rows, never commit dates |
| advisory | ledger | `status.md:4` | event / no | **FB3.** `last_updated` is 00:14:43Z, behind rows `:178-:179` | Bump it with the FB2 row |
| advisory | provenance | tag | event / no | **FB4.** Lightweight tag, no tagger or date | Optional annotated tag on `923ffce` |

### Recommended commands, round two

```bash
# FB1, FB2, FB3 in one ordinary commit (no amend, no forced dates):
#   docs/0.5.0-beta-plan.md W28 restated; status.md: one row disclosing FB2, last_updated bumped
git commit -m "event: trial-2-2026 final audit round two repairs (FB1-FB3)" && git push
# FB4, optional
git tag -a -f trial-2-2026-consolidation-history 923ffce -m "consolidation history of trial-2-2026, squashed in c728437" && git push -f origin trial-2-2026-consolidation-history
# then, unchanged from round one
python3 -m atj event approve events/trial-2-2026/audits/final.md --official event-director
python3 -m atj event unit events/trial-2-2026 record --id final:audit --stage final-audit --output audits/final.md --audit-result "PASS WITH ADVISORIES"
python3 -m atj event gate events/trial-2-2026 final-audit-passed passed --audit audits/final.md
```

## Round three: `93cfb5e..957bc66` and the annotated tag

Scope: rows `status.md:180-181`, `last_updated`, W28 at
`docs/0.5.0-beta-plan.md:262`, the follow-up wording commit `957bc66`, and
`refs/tags/trial-2-2026-consolidation-history`. There were no amends this round.
Commits `93cfb5e`, `710a4db` and `957bc66` have author date equal to committer
date. Origin's reflog shows pushes at 03:01:44Z, 03:01:54Z and 03:02:03Z, each
within 2 s of its commit.

| Item | Checked against | Verdict |
|---|---|---|
| FB1: W28 restated | `atj/event.py:831` `unit = find_unit(...)` through `:846` `stamp = versions.now()`. The unchanged-digest path keeps `completed_at` (`:838-844`), the changed-digest path uses the clock (`:845-846`), and `--completed-at` overrides both (`:834-837`). The code description is now correct | repaired. The evidence clause is wrong (`FC1`) |
| FB2: disclosure row `:181` | first stamp 02:59:30Z in `574f95c`, committer 02:59:26Z: 4 s, correct. Restamped to 02:59:26Z, and `GIT_COMMITTER_DATE` forced to 02:59:26Z: `916a66a` author and committer 1790218766, correct. Made between 02:59:27Z (the `574f95c` push) and 02:59:34Z (the `916a66a` push), from the origin reflog: correct. "without restamping" is explained. "History is not rewritten again": no amend since, and `916a66a` is an ancestor of `957bc66` | repaired, every fact matches git |
| FB3: `last_updated` | 03:01:53Z = `710a4db` | repaired (FC2 notes the 957bc66 follow-up) |
| FB4: tag | `git cat-file -t` gives `tag`. It points at object `923ffce1dd15f9df49a619fcebfb5bd55f95eb2b`, tagger time 1790218904 (03:01:44Z), and the message names c728437, PR #22 and 7ac67fb. On origin, `refs/tags/trial-2-2026-consolidation-history` is `d405953…`, peeled `^{}` to `923ffce1…` | repaired |
| Row `:180` | 03:01:42Z = `93cfb5e`. The round-two counts match this report | correct |
| Ordering | `:179` 02:59:26Z, `:180` 03:01:42Z, `:181` 03:01:53Z ascend. Each row is at or before its commit | correct |

`atj event validate`, `atj validate reports` and `atj release-check` were re-run at
`957bc66` with this section in place. The results are unchanged from round two.

### Findings, round three

| Severity | Rule | Artifact | Scope / blocking | Finding | Required repair |
|---|---|---|---|---|---|
| minor | accuracy of the deliverable | `docs/0.5.0-beta-plan.md:262` | framework / no | **FC1.** W28 cites `:161,164,177` as bracket and dossier re-records after a digest change. `:161` is the matchup unit, and `:177` is the dossiers' first recording | Restate the evidence clause as in `findings:` |
| advisory | ledger | `status.md:4,181` | event / no | **FC2.** `:181` was reworded at 03:02:01Z, after `last_updated` 03:01:53Z | Bump with the next ledger edit |

### Recommended commands, round three

```bash
# FC1 (and FC2's bump) in one ordinary commit
git commit -m "docs: W28 evidence clause corrected (FC1)" && git push
python3 -m atj event approve events/trial-2-2026/audits/final.md --official event-director
python3 -m atj event unit events/trial-2-2026 record --id final:audit --stage final-audit --output audits/final.md --audit-result "PASS WITH ADVISORIES"
python3 -m atj event gate events/trial-2-2026 final-audit-passed passed --audit audits/final.md
```

## Round four: `9d1be78..d8a001a`

Scope: W28 at `docs/0.5.0-beta-plan.md:262`, `status.md:4` and the new row
`status.md:182`. `9d1be78` changes only this file. `d8a001a` changes only the
plan and `status.md` (3 lines). Both commits have author date equal to committer
date. Origin's reflog records the pushes at 03:03:25Z and 03:03:26Z. At
`d8a001a`, `atj event validate` and `atj release-check` both pass.

| Item | Checked against | Verdict |
|---|---|---|
| FC1: W28 evidence clause | `:161` is `matchup:mu-final-01`. Its commit `d5c8f32` moves `input_digest` `d3d4bf06…` → `0ddde002…` with `completed_at` unchanged, so it is a re-record after a digest change that holds the work time. `:164` is `bracket:draw`. Its commit `f9bbfb5` moves `3c88ccc1…` → `7c5f7f20…`, again with `completed_at` unchanged. `:177` covers both dossier units, which first appear in `c732850`, so that is a first recording at 20:30:25Z, the last content edit. The code clause matches `atj/event.py:831-846`, which is unchanged since round three | repaired. The ledger cannot show whether the held times came from `--completed-at` or from a hand edit. W28's fix covers both |
| FC2: `last_updated` | 03:03:25Z = `d8a001a` | repaired |
| Row `:182` stamp | 03:03:25Z = `d8a001a` committer time, so equal, which is permitted. It follows `:181` (03:01:53Z) | correct |
| Row `:182` facts | "scoped to `93cfb5e..957bc66`", "FB1-FB4 repaired", "FC1 minor … `:161,177`", "FC2 advisory", and the repair description all match round three and the diff | correct. Its form is `FD1` |

### Findings, round four

| Severity | Rule | Artifact | Scope / blocking | Finding | Required repair |
|---|---|---|---|---|---|
| advisory | ledger form | `status.md:182` | event / no | **FD1.** One row carries both the audit and its repair, and it records a PASS for the unaudited repair. The facts are correct | None. Keep the two separate from now on |

### Recommended commands, round four

```bash
# Commit this report, then:
python3 -m atj event approve events/trial-2-2026/audits/final.md --official event-director
python3 -m atj event unit events/trial-2-2026 record --id final:audit --stage final-audit --output audits/final.md --audit-result "PASS WITH ADVISORIES"
python3 -m atj event gate events/trial-2-2026 final-audit-passed passed --audit audits/final.md
# Before `atj event advance` to complete: Gregg settles FA2, FA7, CF11
```

## Round five: `e44385b..58cd942` (FA2, FA7, CF11 settled)

Scope:
- the new override `overrides/ovr-trial-2-2026-model-substitution-audits.md`
- the 13 approval rewrites
- the four unit re-records
- W29 and W30 at `docs/0.5.0-beta-plan.md`
- rows `status.md:194-196` and `last_updated`

`58cd942` has author date equal to committer date (12:14:47Z). At `58cd942`:
- `atj event validate`: PASS, 0 problems
- `atj validate reports`: PASS WITH ADVISORIES over 35 artifacts
- `atj release-check`: PASS
- `atj validate publication` on `public/mu-final-01.md`: CLEAR
- `stale_units`: empty
- `atj event overrides`: no gate bypassed

The event-director's "yes to all" reaches me through the coordinator and the
ledger. I cannot verify it from the repository, and I record it as the
repository states it.

### The approval rewrite changed nothing else

For each of the 13 files I parsed the front matter at `e44385b` and at `58cd942`,
compared every key, and compared the bodies byte for byte. The result:

- **All 13 bodies are identical.**
- **Every front-matter difference is one of five keys.** `approval_state` moved
  draft → approved and `validation_state` moved unvalidated → valid.
  `approved_by: event-director`, `approved_at: 2026-09-24T12:13:32Z` and
  `approval_note` were added. No score, confidence, comparison, provenance or
  identity field moved. The reflowed YAML parses to the same values.

**The numbers still reproduce after the rewrite:**
- `atj score` on each panel against its committed `summaries/*.json`: **0
  differing keys**, provisional 32.5 and 52.5, `total: null`. The JSON files are
  unchanged since `c728437`.
- `atj matchup`, on comparisons parsed from the *rewritten* pass front matter:
  **identical** to `matchups/mu-final-01.json`, which is unchanged since `77fcc6a`.

### The new override: every citation

| Cite | Resolves to | Verdict |
|---|---|---|
| `event.md:16` | `model_requested: claude-opus-5` | correct |
| `audits/tournament.md:13`, `audits/dossiers.md:13`, `audits/final.md:13` | `model_used: claude-opus-5-5[1m]` in each | correct |
| "names five artifacts" | `ovr-trial-2-2026-model-substitution.md:36` | correct |
| `framework/policies/disagreement-and-adjudication.md:9` | "A human event official owns disqualification, rules exceptions, and unresolved final ties." | correct |
| `event.md:23-27` | `officials:` and four keys, each `event-director` | correct |
| `:103` | "`event-director` holds all four authorities and Gregg Reed holds that role" | correct |
| `approved_at` 12:13:21Z | row `:194` says "approved 12:13:21Z" | correct |

The reason paragraph restricts "does not depend on the model" to the audits'
calculations, which is accurate. The start stamp is `FE2`. FA2 is **repaired**.

### W29 and W30 against source

- **W29 is correct.** `atj/publication.py:470` calls `expected_visibility`.
  `:471-476` returns blocking `location-unknown` when that is `None`.
  `expected_visibility` (`:427-432`) maps only `relative.parts[0]` through
  `DIRECTORY_VISIBILITY`, so the event-root files `event.md` and `bracket.md`
  have no visibility. Both templates ship `approval_state: draft`
  (`framework/templates/event-configuration.md:21`,
  `framework/templates/bracket-report.md:20`).
- **W30 is correct.** `atj/cli.py:340` binds `existing = find_unit(...)`.
  `record_unit` then finds the same dict and calls `unit.update(payload)`
  (`atj/event.py:860`). So the condition at `atj/cli.py:353-357` compares an
  object with itself and always prints "completed_at kept". I cannot see the
  tool's output from the repository. The code makes the false message certain
  whenever a unit already exists.

### Rows `:194-196` against git and the tools

| Row | Stamp | Tool times it cites | Commit | Verdict |
|---|---|---|---|---|
| `:194` FA2, CF11 | 12:13:21Z | override `approved_at` 12:13:21Z | `58cd942` 12:14:47Z | correct |
| `:195` FA7 | 12:13:32Z | `approved_at` 12:13:32Z in all 13 files | same | correct. The facts match the comparison above |
| `:196` units | 12:13:48Z | unit `completed_at` 12:13:47Z (`bracket:draw`) and 12:13:48Z (other three). The original times it quotes match round one's table | same | correct, and see `FE1` |
| `last_updated` | 12:14:20Z | after all three rows, before the commit | same | correct |

All three rows ascend from `:193` and precede their commit.

### Dispositions

- **FA7 is repaired.** The event-director decided and one row records the
  decision. 13 of 15 artifacts are approved. `event.md` and `bracket.md` stay
  `draft` because the tool cannot approve them. That limit is the framework's
  (W29), and it was correct not to hand-edit them.
- **CF11 is accepted.** The confirmation is recorded at `:194`. The
  repository still cannot show a human acted, which is the 1.0 attestation line.
- **Whether the event may advance to complete: yes.** Nothing blocking or major
  is open. `FE4`'s three re-runs are required first, because this edit stales
  `final:audit`. `FE1` should be repaired before completion freezes the ledger,
  although it is not a gate condition.

### Findings, round five

| Severity | Rule | Artifact | Scope / blocking | Finding | Required repair |
|---|---|---|---|---|---|
| minor | unit semantics (`atj/event.py:820-829`) | `status.md` unit rows | event / no | **FE1.** The four units now carry the re-record clock time instead of the work time. The loss is disclosed, but the values are wrong | Re-record with `--completed-at` set to the work times |
| advisory | record shape | override `:14-15` | event / no | **FE2.** `started_at` = `completed_at` | None |
| advisory | errata visibility | `summaries/*.md` | event / no | **FE3.** The summaries are approved with the known wrong counts and no pointer to the errata | W26 |
| advisory | gate record | `audits/final.md` | event / no | **FE4.** This edit follows the gate and the 03:04:22Z approval of this file | The re-runs below |

### Recommended commands, round five

The orchestrator runs these, in this order. This audit ran none of them.

```bash
E=events/trial-2-2026
# FE4: this file changed after its approval, so re-approve it, re-record its unit, and re-set the gate on it
python3 -m atj event approve $E/audits/final.md --official event-director
python3 -m atj event unit $E record --id final:audit --stage final-audit --output audits/final.md \
  --audit-result "PASS WITH ADVISORIES" --completed-at 2026-09-24T12:16:24Z
python3 -m atj event gate $E final-audit-passed passed --audit audits/final.md
# FE1: restore the work times (the inputs are unchanged, so the digests stay as recorded)
python3 -m atj event unit $E record --id bracket:draw --output bracket.json --audit-result "PASS WITH ADVISORIES" --completed-at 2026-09-23T01:55:10Z
python3 -m atj event unit $E record --id matchup:mu-final-01 --output matchups/mu-final-01.md --audit-result "PASS WITH ADVISORIES" --completed-at 2026-09-23T17:26:17Z
python3 -m atj event unit $E record --id dossier:team-demos --output dossiers/team-demos.md --audit-result "PASS WITH ADVISORIES" --completed-at 2026-09-23T20:30:25Z
python3 -m atj event unit $E record --id dossier:team-scribe --output dossiers/team-scribe.md --audit-result "PASS WITH ADVISORIES" --completed-at 2026-09-23T20:30:25Z
# one ledger row for FE1 and FE4 (separate from any audit row, per FD1), then
python3 -m atj event validate $E && python3 -m atj release-check && python3 -m atj event status $E
python3 -m atj event advance $E
```

`atj event unit record` prints "completed_at kept" in every case (W30). Check
the ledger values after the re-records, not the tool's message.

## Round six: `61b3a0d..06b0d5b` (FE1 and FE4 re-runs)

The commit `06b0d5b` has author date equal to committer date, 12:18:11Z. Origin
received it at 12:18:13Z.

At `06b0d5b` the repository checks pass:
- `atj event validate` gives PASS, 0 problems.
- `atj release-check` gives PASS.
- `atj event status` shows 5 units complete, `final-audit-passed = passed`, and
  "ready to advance to complete".

| Check | Result |
|---|---|
| Units against `derive_digests` | all five match, and `stale_units` is empty. The four restored units keep their round-five digests unchanged: `0d1340ab…`, `7e743af1…`, `dcf08319…` and `fdd24159…` |
| Unit `completed_at` values | `bracket:draw` 2026-09-23T01:55:10Z, `matchup:mu-final-01` 17:26:17Z, both dossiers 20:30:25Z. These are the work times from round one, section 7. `final:audit` is 12:17:58Z (`FF1`). Every `audit_result` is PASS WITH ADVISORIES |
| This file's approval | `approved_at` is 12:18:00Z, with an added `approval_note`. The only other change is quote style on two stamps. The body is unchanged |
| Row `:197` | 12:17:58Z = `61b3a0d`. Its counts match round five |
| Row `:198` | 12:18:00Z = `approved_at`. The digest `08bdbb01` and each restored time match the front matter. The row precedes its commit, 12:18:11Z |
| `last_updated` | 12:18:10Z, between the row and the commit |
| Gate evidence | `stage_gates.final-audit-passed: passed`, and `gate_evidence` names `audits/final.md`. `audit_supports_gate` returns 0 problems. The gate first passed in `7b9ad0f`. The re-set is a no-op in the front matter, and row `:198` records it |

| Severity | Rule | Artifact | Scope / blocking | Finding | Required repair |
|---|---|---|---|---|---|
| advisory | unit semantics | `status.md:50-57,198` | event / no | **FF1.** `final:audit` records the report's commit time, 12:17:58Z, and not the report's `completed_at`. Both are defensible, and the row discloses the choice | None |

### Closing sequence

The orchestrator proposed a closing sequence. It is **acceptable without another
round**, because this edit adds no finding at minor or above. The sequence:

1. Commit this report.
2. Run `atj event approve` on `audits/final.md` as the event-director.
3. Run `atj event unit … record --id final:audit … --completed-at <that commit time>`.
4. Advance.

Three conditions apply:
- **Check the approve diff.** It should change only the approval fields and the
  quote style. If it changes anything else, stop and re-audit.
- **Check the unit values, not the tool message.** Before advancing, `atj event
  status` must show nothing stale. `final:audit`'s digest must equal
  `derive_digests`, and its `completed_at` must be the value passed. The tool's
  message is unreliable (W30).
- **Keep the ledger rows separate.** One row records the re-approval and the
  re-record, and it is distinct from the round-six audit row (FD1).

Re-running `atj event gate` is optional, since the gate is already `passed` on
this file.
