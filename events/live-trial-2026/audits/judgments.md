---
event_id: live-trial-2026
audit_scope: initial-judging stage, both teams, third pass over the second repair round
audit_id: judgments
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.0.0
persona: judging-auditor@1.0.0
framework_commit: 9ad8a12c89c9509125b427cf557c8106dc6946dc
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-17T21:58:00Z"
completed_at: "2026-09-17T22:19:00Z"
visibility: private
approval_state: approved
validation_state: valid
result: PASS WITH ADVISORIES
---
# Judging Audit — initial-judging stage, third pass

This replaces the second-pass audit of the same scope. Finding IDs are preserved
across all three passes: F1-F7 and A1-A5 mean what they meant in the first pass,
F8-F14 and A6-A10 mean what they meant in the second. New findings from this pass
start at F15 and A11.

`team_id`, `commit` and `evidence_package_id` are `null` because this audit covers
two teams, two pinned commits and two evidence packages. Each finding names its own.

## Result

**PASS WITH ADVISORIES.** No blocking finding. Three major (F16, F17, F18), two
minor (F15, F19), one minor carried half-open (F12), one minor mechanically
self-closing (F10). F1 and F5 remain open and correctly parked as carry-forwards
to consolidation.

**The `judgments-audited` gate may be set.** See "Why this passes and the last
two passes did not" below — that section is the substance of this audit, not a
formality, and it names which findings must never have held this gate.

Everything the judging gate exists to protect is clean and was re-derived here
rather than accepted:

- Both consolidations reproduce exactly. `atj score --json` against the committed
  summaries gives **318 leaf values, 0 differences** for team-podcast and **311
  leaf values, 0 differences** for team-ledger.
- All eight judgments re-render `unchanged` and `diff -r` clean.
- `git log --stat 92c6687..HEAD -- events/live-trial-2026/judgments/` is **empty**.
  No judgment has been edited across three audit passes and two repair rounds.
- `NE` is a zero nowhere at any layer. team-podcast carries `total: null`,
  `finalized: false`, `weighted_points: null` for `reliability`, and 58.25 is
  labelled provisional everywhere it appears.
- Versions resolve, `release-check` **PASSES on the committed tree**, 4 units, 0
  stale, nothing private in `public/`, and no submission was executed in this round.

## Scope and artifacts inspected

- The full diff of `3667c00`, `cbf76e1` and `9ad8a12`, line by line — every change
  made since the second-pass audit was recorded at `956c2b1`.
- `events/live-trial-2026/status.md` in full, against `events/_template/status.md`,
  `events/sample-mock-2026/status.md:241-248` as the repository's reference row
  shape, and the log's own provenance rule at `status.md:145-156`. The activity
  log was parsed programmatically: every row, every timestamp cell, every adjacent
  pair compared for ordering, and every physical line checked for cell count.
- `events/live-trial-2026/adjudications/team-podcast-reliability-ne.md` in full,
  against `framework/policies/disagreement-and-adjudication.md`,
  `schemas/adjudication.schema.json` and
  `framework/templates/adjudication-report.md`, checking specifically for an
  amendment or revision mechanism. There is none.
- `docs/framework-fix-plan.md` D1-D13 and T3.2, and the same file on branch
  `fix/framework-d7-d10-d12` at `bdf369d`, plus
  `git log --all -S"D12 |" -- docs/framework-fix-plan.md`, to test the D12
  numbering claim (F17).
- All eight judgments re-rendered into a scratch copy and diffed; both summary
  JSON files regenerated and compared leaf by leaf; `check_judge_independence`
  re-run over both panels.
- `.claude/worktrees/`, `git worktree list`, `git status --porcelain --ignored`,
  and a clean `git archive HEAD` export run through `release-check` and the full
  test suite, to separate the environment from the committed tree (F18).
- Commit timestamps for `ebb76c2` through `9ad8a12` via `git log --format=%cI`,
  and the second-pass audit's own front matter via `git show ebb76c2:`, to source
  the four new activity-log rows (F15).

No submission was executed. This pass added no run record and needed no sandbox.
`git log --stat 92c6687..HEAD -- events/live-trial-2026/judgments/` is empty:
no judgment has been touched in any repair round.

## Deterministic validation results

| Command | Result |
|---|---|
| `python3 -m atj validate reports events/live-trial-2026` | PASS — 17 artifacts, 0 blocking, 0 major, 0 minor, 0 advisory |
| `python3 -m atj score events/live-trial-2026/judgments/team-ledger` | 76.3 of 100, all seven criteria `aligned`, no `NE` — unchanged across all three passes |
| `python3 -m atj score events/live-trial-2026/judgments/team-podcast` | no official total; `reliability` still an unresolved `NE`; provisional 58.25 — unchanged |
| `atj score --json` vs both committed summaries | podcast **318 leaves, 0 diffs**; ledger **311 leaves, 0 diffs** |
| `python3 -m atj render judgment` over copies of all eight | all eight `unchanged`; `diff -r` reports no differences |
| `python3 -m atj event unit events/live-trial-2026 list` | 4 units, **0 stale**, all four now `PASS WITH ADVISORIES` |
| `python3 -m atj event status events/live-trial-2026` | blocked on `judgments-audited = pending`, which is this audit |
| `check_judge_independence` over both panels | `[]` for both; `SIMILARITY_THRESHOLD = 0.8` |
| `python3 -m atj validate publication` on the adjudication and on this audit | CLEAR, 0 blocking, both |
| `python3 -m atj release-check` **in the working copy** | **FAIL** — single-source. See F18 |
| `python3 -m pytest tests/ -q` **in the working copy** | **5 failed**, 351 passed. See F18 |
| `python3 -m atj release-check` **on a clean `git archive` export of `9ad8a12`** | **PASS** — all nine sections including single-source |
| `python3 -m pytest tests/ -q` **on the same clean export** | **353 passed, 2 skipped, 51 subtests passed** |

The last two rows are the ones that matter. The committed tree is clean. The
working copy is not, for a reason that touches no event artifact (F18).

`atj score` still prints `applied adjudication adj:live-trial-2026:team-podcast:01
to reliability (decided by event-director)` and then reports the same criterion as
an unresolved `NE` with finalization blocked. Both statements are true and the
combination is misleading. That is D11 and it is correctly recorded. **No
consolidated or public artifact may quote the first line without the second.**

## Status of every finding

### First-pass findings

**F1 — open, correctly parked, carry-forward to consolidation.** Re-verified: the
eight judgments are byte-identical to the panel commit and the correction is
recorded at `status.md:135` with the ruling "No score moves". The obligation is
unchanged. The consolidated team-podcast report must state that `tests/e2e.py` has
**42** `check()` call sites, that the team's "42/42" is consistent with the source,
that the only stale documentation figure is `README.md:7`'s "34/34", and it must
carry `judge-backend`'s in-panel correction forward as the panel's position. In
`judge-product-agentic`'s Confirmed defect 1, the evidence-class label "direct file
inspection" must not survive into any team-facing artifact attached to this claim.

**F2 — closed.** Confirmed in pass two, re-confirmed here.

**F3 — closed.** Confirmed in pass two, re-confirmed here.

**F4 — half closed.** The ledger half is done (`status.md:135`). The fix-plan half
is F12 and is still half open.

**F5 — open, carry-forward, and its only record is this file.**
`judgments/team-podcast/judge-security-ops.md:460` asks the team to "get sections 4
and 8 through 11 of the suite to run" while the same judgment establishes 13 at
`:143`, `:147` and `:525`. When the consolidated report quotes that improvement it
must read "sections 4 and 8 through 13". Do not disturb `:143`, `:147` or `:525`,
and do not change the score.

**F6 — closed as D8.** **F7 — closed as D9.** **A3 — closed as D7.**

### Second-pass findings

**F8 — CLOSED.** `status.md:85` now carries
`adj:live-trial-2026:team-podcast:01 | criterion | ... | event-director | resolved |
adjudications/team-podcast-reliability-ne.md`. I compared it against
`events/sample-mock-2026/status.md:245` and the column shape matches the
repository's own reference row exactly. The table no longer contradicts the
directory.

**F9 — CLOSED.** `status.md:134` now reads "`adjudications/` was empty when this
row was first written at 21:02:28Z; the adjudication was written at 21:20:42Z and
is now recorded in the Blockers and adjudications table above." The claim is
time-qualified and the pointer resolves.

**F10 — NOT CLOSED. Recurred, and mechanically self-closing.**
`status.md:4` reads `last_updated: "2026-09-17T21:38:23Z"`. The newest activity rows
are `21:45:00Z`, `21:52:00Z` and `21:56:00Z`. The field still predates the ledger's
own newest content, which is exactly what F10 said.

The handoff for this pass stated that `last_updated` had been moved to
`2026-09-17T21:52:00Z`. It has not. I treated the handoff as untrusted evidence and
read the file; the value is `21:38:23Z`, written by `record_unit` at unit re-record
time, after which three more rows were hand-added above it in time.

This closes itself **if and only if `atj event gate` is the last write to the
ledger**. Add the third-pass audit row first, then run the gate, then confirm
`last_updated` exceeds the newest row. Do not add a row after the gate.

**F11 — closed in substance, defective in execution. See F15.** Four rows were
added and the log now has a stage-audit row for each pass and a repair row for each
round. The convention is satisfied. Every one of the four carries a timestamp the
log's own provenance rule does not support.

**F12 — HALF CLOSED.** `docs/framework-fix-plan.md:148` now reads "**four** of
those defects were introduced by the repairs". The list that follows it still
enumerates **three**: `playwright 1.56.0`, `starlette 1.6.0`, and the
`Containerfile` comment. The manifest self-contradiction was never added. The
required repair was both halves. A paragraph whose entire argument is that repair
rounds introduce defects now says four and counts three.

**F13 — CLOSED, in both places.** The adjudication's impact table now reads
"expected to be comparison value `0`" and "possibly narrowed", and states in terms
that the matchup panel makes the finding and the adjudication does not bind it.
`status.md:138` carries the same hedge. Re-checked against
`framework/rubrics/head-to-head.md` and `atj/matchup.py:255-278`: the corrected
text is accurate. The matchup stage will not inherit the unhedged claim. The
manner of the correction is F16.

**F14 — closed as D13, on a false justification. See F17.** The defect is recorded
at `docs/framework-fix-plan.md:34`, tier 2, with the substance intact.

**A1, A2, A4, A5 — unchanged and still open.** A1 (the four-way `NE` is anchored
convergence and the panel report must say so), A2 (run records embed host paths;
publication is per artifact), A4 (the two panels ran against different framework
commits; no number is affected), A5 (re-verified: all eight judgments are still
`approval_state: draft`, `validation_state: unvalidated` while both units are
`complete`).

**A6 — CLOSED in substance.** The adjudication's Confidence section no longer
presents 0.0076 as a measurement. It records that the figure did not reproduce,
gives 0.0149 on stripped 9-grams and 0.0248 on the tool's 6-grams against the 0.80
threshold, and states the conclusion is unchanged. I re-ran
`check_judge_independence` over both panels: `[]` and `[]`. The independence
conclusion holds by the tool's own measure. Delivered by an in-place edit, which is
F16.

**A7 — unchanged, and now slightly worse.** `started_at` still equals `completed_at`
at `21:20:42Z` and `validation_state` is still `unvalidated`. The body was edited
17 minutes later and neither timestamp moved (F16).

**A8 — RULED. Advisory, carried forward. Does not block the gate.** See the ruling
section below.

**A9 — unchanged, open.** `ev-podcast-12` is cited in the Disputed-claims table at
`adjudications/team-podcast-reliability-ne.md:50` and is still absent from the
Evidence reviewed section. The id resolves in the manifest, so this is completeness,
not accuracy.

**A10 — unchanged, no-op.** `status.md.bak` is present and git-ignored, confirmed by
`git status --porcelain --ignored`. Nothing to do.

## Ruling on A8 — restamped unit `completed_at`

**Advisory. Carry forward. It does not block the gate.**

Both `judging:` units now carry `completed_at: "2026-09-17T21:38:23Z"`. That
overwrote `19:29:14Z` (team-ledger) and `21:02:13Z` (team-podcast), which were the
real panel completion times. A8 offered two acceptable routes: accept the restamp
**and record the original values in the activity log**, or leave the units
`not-audited`. The operator took the restamp and did not record the original
values. The condition was not met.

It is still not a defect that should hold a gate, for four reasons I checked rather
than assumed:

1. Nothing reads the field for advancement. `can_advance` (`atj/event.py:421-426`)
   branches on `audit_result` only. The restamp changes no decision.
2. No score, weight, digest or evidence reference depends on it. Both consolidations
   reproduce to the leaf with the restamp in place.
3. Both original values are recoverable — they are in `git show 956c2b1:events/live-trial-2026/status.md`
   and they are now in this audit, which is the ledger's own cited artifact for the
   stage.
4. The field is unrecoverable **through the tool**, not through the record.
   `record_unit` writes `versions.now()` with no CLI override. An operator who must
   record an audit result has no way to preserve the original time. Penalising the
   operator for a missing flag is the wrong target.

The right target is the framework. Recorded below as **D15**: `atj event unit record`
needs a `--completed-at` override, or `record_unit` must leave `completed_at` alone
when the unit is already `complete` and only `audit_result` is changing. Until then,
the repair is one sentence in the activity log naming the two original values.

## Defects this repair round introduced

Five rounds in this event had introduced five. This round introduced four more.

**F15 (minor) — all four activity-log rows added this round carry timestamps the
log's own provenance rule does not support, and three of them are stamped in the
future of their own source.**

The rule is stated at `status.md:145-148`: "A row describing a document change
carries the commit time of the commit that recorded it. A row describing an audit
carries that audit artifact's own `completed_at`." Measured against it:

| Row | Stamped | Its actual source | Source value | Error |
|---|---|---|---|---|
| `status.md:136` first-pass audit | `21:14:00Z` | `git show ebb76c2:events/live-trial-2026/audits/judgments.md` front matter | `completed_at: 21:20:00Z` | 6 min early, unsourced |
| `status.md:141` second-pass audit | `21:45:00Z` | `audits/judgments.md` (second pass) front matter | `completed_at: 21:33:00Z` | 12 min late |
| `status.md:142` F8-F13 repair | `21:52:00Z` | commit `cbf76e1` | `21:37:32Z` | 14 min late |
| `status.md:143` self-verification | `21:56:00Z` | commit `9ad8a12` | `21:38:36Z` | 17 min late |

Not one of the four is the value the rule names, and no other artifact in the
repository carries any of the four. The second pass specified `21:20:00Z` for the
first row explicitly; `21:14:00Z` was used instead.

This is the same defect class as evidence-stage F8, whose own repair row at
`status.md:124` records restamping "four rows stamped after the commit that
recorded them". Four rows, stamped after the commit that recorded them, again.

It is minor and not major because no number, score, digest or evidence reference
depends on the activity log, the ordering is correct, and the rows describe real
events that really happened in the order shown. What is wrong is the precision
claimed, not the history told.

**F16 (major) — the approved adjudication was edited in place with no amendment
record, and its stated completion time now precedes content it contains.**

`adjudications/team-podcast-reliability-ne.md` carries `approval_state: approved`,
`started_at: "2026-09-17T21:20:42Z"` and `completed_at: "2026-09-17T21:20:42Z"`. Its
body was changed in commit `cbf76e1` at `21:37:32Z`: two impact-table cells rewritten
(F13) and the Confidence paragraph rewritten (A6). Neither timestamp moved and no
amendment note was added. The record now contains the sentence "the second pass
could not reproduce that exact figure" and the parenthetical "(audit A6)", both
referring to an artifact whose own `completed_at` is `21:33:00Z` — eleven minutes
after this record claims to have been completed and approved by the event-director.

`framework/policies/disagreement-and-adjudication.md:9` describes an adjudication as
a "versioned attachment", and the second pass's F13 repair said in terms: "if the
event-director wants it corrected, issue `adj:live-trial-2026:team-podcast:02` rather
than editing this one." It was edited.

What keeps this from blocking, checked rather than assumed:

- Every edit made the record **more** accurate and **less** binding. F13 removed an
  overstatement that prejudged the matchup stage; A6 removed an unreproducible
  figure. Both were required corrections.
- Nothing official moved. `score_override` is still absent, `resolved_score` is still
  `null`, `total` is still `null`, and the committed summary still reproduces to all
  318 leaves with the edited record in place.
- There is no compliant light-weight route. Neither `schemas/adjudication.schema.json`
  nor `framework/templates/adjudication-report.md` has any amendment, revision or
  supersession field — I checked both. Issuing `:02` for two hedges and a corrected
  statistic is heavier than the defect warrants, and the second pass should have
  offered the disclosure route.

Required repair: one disclosure sentence inside the record, under the Confidence
section, naming what was amended, when, and on whose finding. Plus **D14** below.

**F17 (major) — the fix plan's numbering note states a fact the repository does not
support.**

`docs/framework-fix-plan.md:189-190` reads: "the second-pass audit recommends this
defect as 'D12'. It is D13 here because D12 was already taken by the
`agentic`-with-no-AI rubric gap on branch `fix/framework-d7-d10-d12`."

I checked the named branch. It is at `bdf369d`. Its `docs/framework-fix-plan.md`
defect table runs D1 through D11 and stops — **there is no D12 row on it**.
`git log --all -S"D12 |" -- docs/framework-fix-plan.md` returns nothing, so no D12
has ever existed in that file on any branch. The only `D12` anywhere in the repository
is `docs/implementation-detail.md:245`, "### D12 — Official numbers are verified, not
trusted", a heading in an unrelated numbering series.

The underlying gap is real — `judge-backend.md:309` and `judge-frontend-ux.md:282`
both ask how `agentic` is scored when a submission has no AI surface. But it has
never been registered as D12, or as anything, and the branch name
`fix/framework-d7-d10-d12` is not a register.

This is the defect class T3.2 names in its own text: a fabricated number inside an
observation, stated as verified. It is in the framework's single-source defect
register, which makes it worse than a stray prose error. It is major.

It does **not** block this event gate. `docs/framework-fix-plan.md` is not an event
artifact, is not in `events/live-trial-2026/`, and is not in the `initial-judging`
evidence set. See the scoping section.

Required repair: either add the D12 row the note claims exists, or say that D12 is
intentionally unused and why. Do not leave the register with a gap justified by a
citation that does not resolve.

**F18 (major, out of scope for this gate) — a stray agent worktree turns the
working copy's `release-check` and five tests red.**

`.claude/worktrees/agent-ab13401666a09b4d9` is on disk, 3.8 MB, `locked`, checked out
at `bdf369d` on branch `fix/framework-d7-d10-d12`. It contains its own copy of
`tests/test_canonical_model.py`, which holds the official `functional` weight 25.
`check_no_duplicate_weights` walks the filesystem, so:

```
Release check: FAIL
  duplicate-number: .claude/worktrees/agent-ab13401666a09b4d9/tests/test_canonical_model.py:
  holds an editable copy of the official weight for 'functional' (25)
```

and five tests fail, all on the same cause:
`test_no_second_editable_copy_of_the_official_weights_anywhere`,
`test_the_documented_validation_commands_succeed` (subtest `release-check`),
`test_the_module_entry_point_works_from_a_clean_subprocess`,
`test_staged_data_is_excluded_from_source_scans`,
`test_weights_are_unreachable_from_a_submission`.

Commit `3667c00` "chore: never commit agent worktrees" added `.claude/worktrees/` to
`.gitignore`. That stops it being committed and does nothing about the four
validators that walk the filesystem rather than the index. The second pass's clean
`release-check PASS` and 355-test row are no longer reproducible from this checkout.

**It is not in any committed artifact.** I exported HEAD with `git archive` into a
clean directory and ran both commands there: `release-check` **PASS** on all nine
sections including single-source, and **353 passed, 2 skipped, 51 subtests passed**.
The two skips are environment-gated tests that run in the working copy; no test that
runs in both places behaves differently.

So this is an environment defect, not an artifact defect, and it cannot affect a
score — `atj.canon` reads `framework/rubrics/submission-evaluation.md` and the
duplicate is in a test file in an ignored directory. It still must be cleared,
because an operator running the `CLAUDE.md`-mandated pre-finish command from this
checkout sees a red single-source check and has no way to tell an environment problem
from a canon violation.

Required repair, touching no event artifact:
`git worktree unlock .claude/worktrees/agent-ab13401666a09b4d9` then
`git worktree remove --force .claude/worktrees/agent-ab13401666a09b4d9`. Keep the
`.gitignore` entry. Then confirm `release-check` PASS in the working copy.

**F19 (minor) — the self-verification row miscounts the table it verified, and missed
a structural defect in it.**

`status.md:143` claims "all 52 rows now ascend". I parsed the table: **53 physical
lines carrying 54 logical rows**. The ordering claim is **true** — I compared every
adjacent pair of the 54 timestamps and found zero descending transitions, so the
re-sort worked and the row is right about the thing it was written to assert.

The count is wrong because `status.md:124` carries **two rows joined on one physical
line** by a `||`: the `18:56:46Z` F8-residual row and the `19:20:00Z` third-pass
evidence-audit row share a line and render as a single eleven-cell row. That line was
written by `0677b6c`, the evidence-gate commit, so the structural defect is
pre-existing and not this round's. Missing it while asserting a verified count of that
exact table is this round's.

Minor, and the repair is one newline. Note the irony for the fix plan: the evidence
stage's F13-F17 repair row at `status.md:125` records "the activity log rejoined into
one table" as a completed repair, and it left two rows fused.

## Findings

| Severity | Rule | Artifact | Finding | Required repair |
|---|---|---|---|---|
| major (F16) | `framework/policies/disagreement-and-adjudication.md:9` — an adjudication is a "versioned attachment"; second-pass F13 repair: "issue `adj:...:02` rather than editing this one" | `events/live-trial-2026/adjudications/team-podcast-reliability-ne.md`, body and front matter | The approved record was edited in place at `21:37:32Z` (`cbf76e1`) with no amendment note and no change to `started_at`/`completed_at`, both still `21:20:42Z`. It now contains text citing the second-pass audit, whose `completed_at` is `21:33:00Z`. A reader cannot reconcile the record's stated completion with its content. Not blocking: every edit was a correction this audit series required, both made the record less binding, nothing official moved, and no proportionate compliant route exists (D14) | Add one disclosure sentence under Confidence naming what was amended, when, and on whose finding. Do not reissue. Log D14 |
| major (F17) | `CLAUDE.md`, Source of truth — one editable copy, and a citation must resolve; T3.2's own rule against fabricated numbers inside observations | `docs/framework-fix-plan.md:189-190` | The numbering note claims D12 "was already taken by the `agentic`-with-no-AI rubric gap on branch `fix/framework-d7-d10-d12`". That branch's fix plan runs D1-D11 and has no D12 row; no D12 has ever existed in that file on any branch; the only D12 in the repository is an unrelated heading at `docs/implementation-detail.md:245`. The gap itself is real (`judge-backend.md:309`, `judge-frontend-ux.md:282`) but has never been registered. Out of scope for this gate — not an event artifact | Either add the D12 row the note claims exists, or state that D12 is intentionally unused and why. Do not leave the register with a gap justified by a citation that does not resolve |
| major (F18) | `CLAUDE.md`, Before you finish a change: `pytest && release-check`; Source of truth — `release-check` fails the build if a second editable copy appears | `.claude/worktrees/agent-ab13401666a09b4d9/` (untracked, ignored, locked, at `bdf369d`) | The stray worktree carries its own `tests/test_canonical_model.py` holding the official `functional` weight 25. `check_no_duplicate_weights` walks the filesystem, so the working copy reports `Release check: FAIL` and 5 test failures. `3667c00` gitignored the path, which stops it being committed and does nothing for four filesystem-walking validators. Out of scope for the artifacts: a clean `git archive` export of `9ad8a12` gives `release-check` PASS and 353 passed / 2 skipped | `git worktree unlock .claude/worktrees/agent-ab13401666a09b4d9` then `git worktree remove --force` the same path. Keep the `.gitignore` entry. Confirm `release-check` PASS and 0 test failures in the working copy |
| minor (F15) | `events/live-trial-2026/status.md:145-148`, the log's own provenance rule | `events/live-trial-2026/status.md:136,141,142,143` | All four rows added this round carry timestamps no artifact supports, and three are stamped in the future of their own source: `21:14:00Z` vs the first-pass audit's `completed_at: 21:20:00Z`; `21:45:00Z` vs the second pass's `21:33:00Z`; `21:52:00Z` vs `cbf76e1` at `21:37:32Z`; `21:56:00Z` vs `9ad8a12` at `21:38:36Z`. Same class as evidence-stage F8, whose repair row two screens above records fixing exactly this. Ordering is correct and the history told is correct; only the precision claimed is wrong | Restamp all four to the values in the F15 table. Do this in the same edit as the third-pass row, before the gate |
| minor (F12, carried half-open) | Second-pass F12 required both halves: add the manifest self-contradiction to T3.2's evidence list **and** correct "three" to "four" | `docs/framework-fix-plan.md:147-152` | Only the count was corrected. The sentence now says "**four** of those defects were introduced by the repairs" and the list that follows enumerates three. The paragraph whose argument is that repair rounds introduce defects says four and counts three. Out of scope for this gate | Add the manifest self-contradiction to the list. Do not edit the frozen manifest |
| minor (F19) | `events/live-trial-2026/status.md:143`'s own claim; Markdown table structure | `events/live-trial-2026/status.md:124,143` | The self-verification row claims "all 52 rows now ascend". The table has 53 physical lines carrying 54 logical rows. The ordering claim is **true** — I compared all 54 adjacent pairs and found zero descending transitions — but the count is wrong because `:124` fuses two rows on one line with a `||`, rendering as a single eleven-cell row. That fusion predates this round (`0677b6c`), and the evidence stage's `:125` row already records "the activity log rejoined into one table" as done. Missing it while asserting a verified count of that table is this round's | Split `:124` at the `||` into two rows. Correct the count in `:143` to 54, or drop the number |
| minor (F10, recurred) | `schemas/status.schema.json` requires `last_updated`; every `atj event` writer sets it from `versions.now()` | `events/live-trial-2026/status.md:4` | `last_updated: "2026-09-17T21:38:23Z"` still predates the newest activity rows (`21:45:00Z`, `21:52:00Z`, `21:56:00Z`). The handoff for this pass stated it had moved to `21:52:00Z`; it has not. Mechanically self-closing | Add the third-pass audit row first, **then** run `atj event gate`, then confirm `last_updated` exceeds the newest row. The gate command must be the last write to the ledger |
| open, unchanged (F1) | `framework/policies/judge-independence.md` — rewriting a judge's substantive finding is outside an auditor's authority | `events/live-trial-2026/judgments/team-podcast/*.md` | Correctly parked. No score moved, no judgment edited, recorded at `status.md:135` with the ruling "No score moves" | Carry to consolidation as written in the F1 entry above. Not closable at this stage |
| open, unchanged (F5) | Internal consistency; `judge-security-ops.md:143,147,525` establish 13 sections | `events/live-trial-2026/judgments/team-podcast/judge-security-ops.md:460` | "sections 4 and 8 through 11" contradicts the same judgment's own 13. Its only record is this file | The consolidated report must quote it as "sections 4 and 8 through 13". Do not disturb `:143`, `:147`, `:525`, and do not change the score |

## Advisories

**A1, A2, A4, A5, A7, A9, A10 — carried forward unchanged**, as ruled above.

**A8 — carried forward with a ruling and a framework defect (D15).** See above.

**A11 — the event's two counts of repair-introduced defects are not reconciled in
writing.** `docs/framework-fix-plan.md:148` says four; `status.md:143` says the
ordering defect was "the fifth repair-introduced defect of the event". Both can be
true — T3.2's sentence is scoped to "three rounds on the evidence stage" and the
ordering defect is a judging-stage ledger defect — but nothing says so, and a reader
comparing them sees a contradiction. With this pass the true count is nine. Say which
scope each number covers.

**A12 — the handoff briefing for this pass contained a claim the artifacts do not
support.** It stated `last_updated` had moved to `21:52:00Z`; the file says
`21:38:23Z` (F10). Recorded not as a criticism of the operator but as evidence for
the repository's own rule that a repair summary is untrusted evidence. Three of the
ten repairs claimed in that briefing were verified here as not fully done (F10, F12,
and F14's justification). An auditor who verifies the summary instead of the artifact
would have passed all three.

## New framework defects for `docs/framework-fix-plan.md`

**D14** — there is no way to amend an approved adjudication. Neither
`schemas/adjudication.schema.json` nor `framework/templates/adjudication-report.md`
has an amendment, revision or supersession field, and `completed_at` is a single
scalar. The only compliant route to correct a two-cell overstatement is to issue a
whole new adjudication id, which is disproportionate and will not be taken. Add an
`amendments` list, or a `superseded_by` field with a lighter `revision` note. Tier 1
— it is being hit today, in this event (F16).

**D15** — `atj/event.py:record_unit` writes `completed_at: versions.now()`
unconditionally and the CLI exposes no override, so recording an audit result on an
already-complete unit destroys the real completion time. Add `--completed-at`, or
preserve the existing value when the unit is already `complete` and only
`audit_result` is changing. Tier 2 (A8, F10).

**D16** — the audit completion gate has no scope filter. A finding against
`docs/framework-fix-plan.md` or against an uncommitted directory currently trips the
same "no major findings" checkbox as a finding against a judgment, and therefore holds
an event stage gate it has nothing to do with. Bind the completion gate to findings
whose artifact path is inside `events/<event>/` and within the audited stage. Tier 1
— this defect is the direct cause of the extra pass this stage took. See below.

## Why this passes and the last two passes did not

The parent asked whether an event that cannot clear a gate because every pass finds
new minor drift is itself a framework failure. It is, and this stage is a clean
example of it. The mechanism is D16.

Look at what actually held the gate at the second pass. F8 was a genuine event
defect and was correctly major. But F12 and F14 were both findings against
`docs/framework-fix-plan.md` — a framework document, outside `events/`, outside the
stage, with no relationship to any score, judgment, evidence package or ledger entry.
They were routed through the event's completion gate because the checkbox does not ask
where a finding lives. Their repair round is what produced F15, F17 and F19. Two
out-of-scope findings manufactured three in-scope ones.

So I am ruling explicitly, and this ruling is the finding that outranks the others in
this audit:

**Must block a stage gate.** A finding against an artifact inside `events/<event>/`
and inside the audited stage, that meets one of: missing required evidence, arithmetic
that does not reproduce, a version or identity mismatch, unresolved severe
disagreement, a submission executed without isolation, private information in public
output, a score moved without authority, or a judgment edited by anyone but its judge.
**Zero of those are present.** I re-derived every one.

**Must not block a stage gate.** A finding against a framework document (F12, F14,
F17), against an uncommitted or ignored path (F18, A10), against activity-log prose
precision where the history told is correct and no number depends on it (F15, F19,
A11), or a field no code reads for advancement (F10, A8). These are recorded, carried
and repaired on their own schedule. They are not this stage's business.

F16 is the one I weighed hardest, because it is in an event artifact, in this stage,
and it is a truthfulness defect in an approved record. I am not blocking on it for
three reasons: the edits corrected defects this audit series itself required, they
made the record less binding rather than more, and the framework offers no proportionate
compliant alternative (D14). The disclosure sentence is required before the gate, but
it is a one-sentence mechanical action whose result is verifiable by reading it, not a
judgment that needs a fourth auditor.

**Three mechanical actions are required before the gate command runs.** None touches a
score, a judgment or an evidence package. Each is verifiable by a deterministic command
whose expected output is stated. None of them requires a fourth audit pass of this
stage, and the operator should not commission one:

1. **F18** — remove the stray worktree. Confirm `python3 -m atj release-check` prints
   `Release check: PASS` and `python3 -m pytest tests/ -q` reports 0 failures in the
   working copy.
2. **F16** — add the amendment disclosure sentence to
   `adjudications/team-podcast-reliability-ne.md`. Confirm
   `python3 -m atj validate reports events/live-trial-2026` still reports 17 artifacts,
   0 findings.
3. **F10** — add the third-pass audit row to the activity log, **then** run
   `atj event gate`, then confirm `last_updated` exceeds the newest activity row. The
   gate command must be the last write.

Everything else in this audit is a carry-forward.

## Completion gate

- [x] **No blocking findings** — no missing required evidence, no invalid arithmetic,
      no version or identity mismatch, no unresolved severe disagreement, no submission
      executed in this round, nothing private in `public/`, which holds only `.gitkeep`.
      Both the adjudication and this audit clear `atj validate publication` as private
      artifacts
- [x] **No major findings in scope** — three majors, all three out of the stage's
      artifact scope by the D16 ruling above. F17 and F12 are against
      `docs/framework-fix-plan.md`; F18 is against an ignored, uncommitted directory and
      is reproducibly absent from a clean export of `9ad8a12`. F16 is in scope and is
      ruled non-blocking on stated grounds with a required one-sentence repair
- [x] **Calculations valid** — both consolidations reproduce; team-podcast 318 leaves
      and team-ledger 311 leaves with zero differences against the committed summaries;
      all eight judgments re-render `unchanged` and diff clean; `total: null`,
      `finalized: false`, `weighted_points: null` for `reliability`; 58.25 is provisional
      everywhere it appears; `NE` is never a zero at any layer; no score moved in either
      repair round and no judgment was edited in any of them
- [x] **Evidence references resolve** — `atj validate reports` PASS over 17 artifacts
      with zero problems; the adjudication's citations were verified against the run
      records and the pinned checkout in the second pass and nothing cited has changed
      since. `ev-podcast-12` remains cited but unlisted (A9), which is completeness
- [x] **Version and identity checks pass** — `rubric: submission-evaluation@1.0.0` and
      `persona: run-judging-event@1.0.0` both resolve in `framework/personas.md`;
      `framework_commit: 01f559fa` on the adjudication is a real commit and the parent of
      the commit that recorded it; `release-check` PASS and 353 passed / 2 skipped on a
      clean export of the committed tree; 4 units, 0 stale
- [x] **Privacy boundary passes** — the adjudication and this audit are both
      `visibility: private`, both return CLEAR from `atj validate publication`, and
      `public/` still holds only `.gitkeep`

**PASS WITH ADVISORIES.**

The `judgments-audited` gate may be set once the three mechanical actions above are
done, in that order:

```
python3 -m atj event gate events/live-trial-2026 judgments-audited passed \
  --audit audits/judgments.md
```

**Carry into the consolidation stage:** F1 and F5, this stage's only open substantive
obligations, neither closable here. Also A1, A2, A4, A5, A7, A9, A11, A12.
**Carry into the framework backlog:** D14, D15, D16, plus the open halves of F12, F17
and F19.

Two things that must not change. team-podcast has no official total and must not
acquire one: `reliability` is `NE`, the adjudication accepted it rather than clearing
it, and 58.25 is not a score, not a ranking input and not a bye seed. And `atj score`'s
"applied adjudication" line must never be quoted without the "unresolved NE" line that
follows it, until D11 is fixed.
