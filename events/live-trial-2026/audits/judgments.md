---
event_id: live-trial-2026
audit_scope: initial-judging stage, both teams, second pass over the repair round
audit_id: judgments
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.0.0
persona: judging-auditor@1.0.0
framework_commit: bdf369d41596a4330338336c6ed50cefa2061875
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-17T21:24:00Z"
completed_at: "2026-09-17T21:33:00Z"
visibility: private
approval_state: approved
validation_state: valid
result: FAIL
---
# Judging Audit — initial-judging stage, second pass

This replaces the first-pass audit of the same scope. Finding IDs are preserved:
F1-F7 and A1-A5 mean exactly what they meant in the first pass. New findings from
this pass start at F8 and A6.

`team_id`, `commit` and `evidence_package_id` are `null` because this audit
covers two teams, two pinned commits and two evidence packages. Each finding
names its own.

## Result

**FAIL.** No blocking finding. One major (F8). Six minor (F9-F14). Five new
advisories (A6-A10).

The repair round did its substantive work. **F2 is closed, F3 is closed, F4, F6,
F7 and A3 are recorded, and F1 is correctly parked as a carry-forward with no
score moved and no judgment edited.** The adjudication the round produced is a
good one: its question is narrow, every artifact it cites resolves, its factual
resolution is supported, and its two downstream claims are true — I re-derived
both with the tools rather than accepting them.

What fails is the same class of defect the first pass failed on, in the same
file. `status.md` now records an adjudication in prose but leaves the ledger's
dedicated **Blockers and adjudications** table empty (F8), still asserts
`adjudications/` is empty (F9), carries a `last_updated` that predates its own
newest rows (F10), and has no activity row for the stage audit at all (F11). One
edit plus the two `atj event` commands closes all four.

## What changed since the first pass

Three commits: `ebb76c2` (audit recorded, two ledger rows corrected), `01f559f`
(D7-D9 added to the fix plan), `bdf369d` (adjudication written, three ledger rows
added, `summaries/team-podcast.json` regenerated).

I read every changed line in all three. The judgments were not touched:
`git log --stat 92c6687..HEAD -- events/live-trial-2026/judgments/` is empty, and
the only three commits that have ever written into that directory are `7dab838`,
`4a96452` and `92c6687`.

## Scope and artifacts inspected

- The full diff of `ebb76c2`, `01f559f` and `bdf369d`, line by line.
- `events/live-trial-2026/adjudications/team-podcast-reliability-ne.md` in full,
  against `framework/policies/disagreement-and-adjudication.md`,
  `schemas/adjudication.schema.json` and
  `framework/templates/adjudication-report.md`.
- `events/live-trial-2026/status.md` in full, against `events/_template/status.md`
  and `events/sample-mock-2026/status.md` as the repository's own reference shape.
- `docs/framework-fix-plan.md` D1-D11 and T3.2.
- All eight judgments re-rendered and diffed; both summary JSON files regenerated
  and diffed; the podcast panel re-measured for wording overlap.
- `framework/rubrics/head-to-head.md` and `framework/rubrics/bracket-assignment.md`
  front matter, and `atj/matchup.py:245-278`, `atj/bracket.py:150-178`,
  `atj/scoring.py:397-461`, `atj/event.py:392-435,460-560`, `atj/cli.py:383-420`,
  read to check the adjudication's mechanism claims rather than its prose.
- `workspaces/live-trial-2026/team-podcast/web/js/storage.js` and four run records
  at the pinned commit, to check the adjudication's cited facts.

No submission was executed. This pass added no run record and needed no sandbox.

## Deterministic validation results

| Command | Result |
|---|---|
| `python3 -m atj validate reports events/live-trial-2026` | PASS — **17** artifacts, 0 blocking, 0 major, 0 minor, 0 advisory. `validate_event_reports` (`atj/reports.py:322-326`) walks every `ARTIFACT_KINDS` directory, so the 17 are eight judgments, two evidence manifests, two intake records, four audits and the adjudication. The first pass counted 15 because neither its own audit file nor the adjudication existed yet |
| `python3 -m atj score events/live-trial-2026/judgments/team-ledger` | 76.3 of 100, all seven criteria `aligned`, no `NE` — unchanged |
| `python3 -m atj score events/live-trial-2026/judgments/team-podcast` | no official total; `reliability` still reported as an unresolved `NE`; provisional 58.25 — unchanged |
| `atj score --json` over `judgments/team-podcast` vs the committed summary | 318 leaf values, **zero differences**. The regenerated summary reproduces, including the new `resolution` block |
| `python3 -m atj render judgment` over copies of all eight | all eight `unchanged`; `diff -r` against the committed files reports no differences |
| `python3 -m atj event unit events/live-trial-2026 list` | 4 units, **0 stale** |
| `python3 -m atj event status events/live-trial-2026` | blocked on `judgments-audited = pending`, which is this audit |
| `python3 -m pytest tests/ -q` | 355 passed, 51 subtests passed |
| `python3 -m atj release-check` | PASS — rubric, schemas, personas, templates, claude components, single-source, template schemas, version-skew, sample event |
| `python3 -m atj validate publication adjudications/team-podcast-reliability-ne.md` | CLEAR, 0 blocking. It is correctly classified private (`atj/publication.py:34`) and contains no host path, uid map or personal identifier |
| `check_judge_independence` over the event | no finding; `SIMILARITY_THRESHOLD = 0.80`, measured maximum 0.0248 (see A6) |

`atj score` prints `applied adjudication adj:live-trial-2026:team-podcast:01 to
reliability (decided by event-director)` and then, four lines later, reports the
same criterion as an unresolved `NE` with finalization blocked. Both statements
are true and the combination is misleading. That is D11 and it is correctly
recorded. **No consolidated or public artifact may quote the first line without
the second.**

## First-pass findings, re-ruled

**F1 — open, correctly parked, no score moved.** The eight judgments are
byte-identical to the panel commit, which is the right outcome:
`framework/policies/judge-independence.md` puts rewriting a judge's substantive
finding outside an auditor's authority. The correction is recorded at
`status.md:134` with the ruling "No score moves". The obligation is unchanged and
carries into the consolidation stage: the consolidated team-podcast report must
state that `tests/e2e.py` has **42** `check()` call sites, that the team's
"42/42" is consistent with the source, that the only stale documentation figure
is `README.md:7`'s "34/34", and it must carry `judge-backend`'s in-panel
correction forward as the panel's position. In `judge-product-agentic`'s
Confirmed defect 1, the evidence-class label "direct file inspection" must not
survive into any team-facing artifact attached to this claim.

**F2 — closed.** `status.md:133` now states that adjudication **is** required,
names `summaries/team-podcast.json` and
`framework/policies/disagreement-and-adjudication.md:5` as its authority, and an
adjudication exists. The summary was not altered by hand; it was regenerated and
reproduces exactly. Two residual inaccuracies in the same row are F9.

**F3 — closed.** I re-checked the corrected attribution against the texts.
`judge-security-ops:147` ("`tests/e2e.py` has **13** numbered sections, not 11")
and `judge-product-agentic:73-74` ("The manifest characterizes the suite as 11
stages; the file says otherwise") flag the stage count explicitly;
`judge-backend:68` uses "stage 7 of 13" without flagging it. The check-count
error was caught by `judge-backend` alone. No judgment reports the
`evidence_limited_criteria` contradiction. The corrected row states all three
correctly. It does not name the two judges, which the first pass asked for; the
claim is true either way, so this is closed rather than reopened.

**F4 — half closed. See F12.** The defect is recorded against the frozen package
in `status.md:134`. The fix-plan half was not done.

**F5 — open, carry-forward, and its only record is this file.**
`judgments/team-podcast/judge-security-ops.md:460` asks the team to "get sections
4 and 8 through 11 of the suite to run" while the same judgment establishes 13 at
`:143`, `:147` and `:525`. When the consolidated report quotes that improvement it
must read "sections 4 and 8 through 13". Do not disturb `:143`, `:147` or `:525`,
and do not change the score. Unlike F1 this is not in the ledger; see the repair
list.

**F6 — closed as D8.** `docs/framework-fix-plan.md:30`, tier 2. The split is
still visible in the regenerated summary (`judge-security-ops` records
`confidence: high` beside `reliability: NE`, the other three `low`), which is
correct: no judgment was changed.

**F7 — closed as D9.** `docs/framework-fix-plan.md:31`, tier 2.

**A3 — closed as D7.** `docs/framework-fix-plan.md:29`, tier 1, with the note
that it caused a real defect in this event.

**A1, A2, A4, A5 — unchanged and still open.** A1 (the four-way `NE` is anchored
convergence and the panel report must say so), A2 (run records embed host paths;
publication is per artifact), A4 (the two panels ran against different framework
commits; no number is affected), A5 (all eight judgments remain draft/unvalidated)
all carry forward exactly as written in the first pass.

## The adjudication, audited

Against `framework/policies/disagreement-and-adjudication.md` and
`schemas/adjudication.schema.json`:

- **Trigger.** `unresolved-ne` is a valid enum value and the policy requires
  adjudication for "an `NE` that prevents scoring". Correct.
- **Question.** Narrow and answerable: can `reliability` be scored from the
  pinned package, and if not does the `NE` stand. It asks about one criterion for
  one team and does not reopen the project. Correct.
- **Scope discipline.** The policy says the adjudicator receives the disputed
  claims and original evidence, "not an invitation to rescore the entire
  project". The record gathers no new evidence and states why: re-executing after
  judging began would breach `CLAUDE.md` and invalidate four judgments resting on
  this package. Correct, and the right call.
- **Every cited artifact resolves.** `ev-podcast-05`, `-06`, `-12`, `-15`, `-16`,
  `-17`, `-18`, `-20` all appear in `evidence/team-podcast/manifest.md`. All four
  named run records exist. I verified the underlying facts rather than the
  citations alone: `--memory 1g --cpus 1.0`, `--env HOME=/tmp` and no `--shm-size`
  appear in the podman invocation recorded in
  `runs/team-podcast-e2e-full-02.json`; `Target crashed` appears in that record;
  `GET /api/media/1 200 OK` appears in both `-e2e-full-01` and `-e2e-full-02`;
  the 90-second download timeout is the `90000` in `-e2e-full-01`; the 71-second
  container overlap is in the manifest. `grep -n "onerror\|setTimeout"` over
  `web/js/storage.js` at `f3fdd342` returns nothing, which confirms
  `judge-security-ops`'s claim exactly as the table classes it. One omission is
  A9.
- **Evidence classes.** Four rows classed inference, direct observation and
  artifact evidence, matching what each judge actually did. Correct, and notably
  it does not repeat F1's mislabelling.
- **Impact table.** Correct on every row except the tie-break row, which is F13.
  `score_override` is absent by design and `resolved_score` is `null`, so no
  total moved: the regenerated summary still carries `total: null`,
  `finalized: false`, `weighted_points: null` for `reliability`, and
  `provisional_total: 58.25`. `NE` is a zero nowhere at any layer.
- **Accepting the `NE` is defensible.** The policy reserves disqualification,
  rules exceptions and unresolved final ties for a human official; an
  evidence-limited `NE` is none of those, and `event.md:29` assigns adjudication
  to the event-director, which is what `decided_by` names. `resolution: resolved`
  is the honest value: the adjudication answers its question definitively, and
  the answer is that the criterion cannot be resolved. The alternative — reopening
  the evidence stage for one `--shm-size` re-run — was rejected on the correct
  ground. I agree with the outcome. A low score would ignore that every observed
  failure has a credible environmental cause; a high score would credit a suite
  that has never produced a result.
- **`persona: run-judging-event@1.0.0` with `decided_by: event-director`.**
  Ruling: **honest in form, unverifiable in substance; acceptable here and not a
  precedent.** The persona is registered (`framework/personas.md:34`, kind
  `skill`), so `atj validate` and `versions.require_versions` pass, and the
  document states in plain text why the field reads as it does and files D10
  rather than hiding the substitution. That is the right way to record a
  constraint you cannot satisfy. What no reader can check is whether a human
  event-director decided or an orchestrator wrote the role into the field.
  `atj/scoring.py:431` treats a non-empty `decided_by` as the gate that lets an
  adjudication move an official total, so that field carries real authority. It
  carried none here: nothing moved. Recorded as F14.

## Downstream impact, verified independently

I did not take the adjudication's word for either claim.

**The bracket is genuinely unaffected at two teams.** `bracket-assignment.md`
front matter declares `min_teams: 2`; `event.md:9` declares
`bye_policy: performance-qualified`. `atj/bracket.py:163` returns before the
score check when `count == 0`, and at two entrants the bracket size is an exact
power of two, so `bye_count` is 0. I built a probe bracket from two entrants with
`team-podcast`'s score set to `null` and `--bye-policy performance-qualified`. It
produced one final-round match, `0 byes`, and every hard constraint `satisfied`,
including "Bye policy 'performance-qualified' applied consistently — no byes: the
team count is an exact power of two". The claim holds. It would **not** hold at
three or more teams: `atj/bracket.py:170-174` raises
`performance-qualified byes require a consolidated score for every team` the
moment one bye is needed.

**`head-to-head.md` genuinely does not require an initial total.** The rubric
compares the seven source-rubric criteria directly and says "Do not merely select
the team with the higher initial total" — quoted accurately. `atj/matchup.py`
computes margins from comparison values only; `tie_break()` at `:255-278` reads
`result["criteria"][criterion]["combined_margin"]`, a value produced fresh in the
matchup. No code path in the matchup module reads a consolidated total. The claim
holds. The adjudication's extension of it to the tie-break order does not; that is
F13.

## Findings

| Severity | Rule | Artifact | Finding | Required repair |
|---|---|---|---|---|
| major (F8) | `CLAUDE.md`, Source of truth: event state lives in `status.md`; `events/_template/status.md:40-43` and `events/sample-mock-2026/status.md:241-248` define the row shape | `events/live-trial-2026/status.md:81-85` | The **Blockers and adjudications** table is empty while `adjudications/team-podcast-reliability-ne.md` exists and is applied by `atj score`. This is the ledger's dedicated, structured index of adjudications, and it reads as though the event has none. The reference sample event records all three of its adjudications there with id, scope, description, owner, status and resolution artifact. The activity log carries the fact in prose at `:135`, so nothing is hidden — but the table a reader or a later stage consults first says the opposite of the directory. This is the same class of defect as F2, in the same file, and F2 was rated major | Add one row: `adj:live-trial-2026:team-podcast:01` \| `criterion` \| `Unresolved NE on reliability blocked the official total; adjudicated and accepted` \| `event-director` \| `resolved` \| `adjudications/team-podcast-reliability-ne.md`. Do not restate the adjudication's reasoning in the table; it lives in the record |
| minor (F9) | `CLAUDE.md`, Source of truth; the ledger must state what is true | `events/live-trial-2026/status.md:133` | The corrected F2 row asserts "`adjudications/` is empty." That was true when `ebb76c2` wrote it and false five minutes later when `bdf369d` created the record. Repair-introduced: the commit that invalidated the sentence did not update it. A reader who stops at this row concludes the required adjudication is still missing | Replace "`adjudications/` is empty" with a forward pointer to the `2026-09-17T21:20:42Z` row and to `adjudications/team-podcast-reliability-ne.md`. Leave the rest of the row alone; it is correct |
| minor (F10) | `schemas/status.schema.json` requires `last_updated`; every `atj event` writer sets it from `versions.now()` (`atj/event.py:473,497,540,550`) | `events/live-trial-2026/status.md:4` | `last_updated: "2026-09-17T21:02:13Z"` predates the newest activity rows (`21:20:42Z`) and both repair commits (`21:17:53Z`, `21:22:49Z`). The repairs hand-edited the ledger instead of going through a tool that maintains the field, so the ledger understates when it was last touched by twenty minutes | Self-closing: `atj event gate` and `atj event unit record` both rewrite `last_updated`. Run them as part of the repair and confirm the value moves |
| minor (F11) | `events/live-trial-2026/status.md:139-143`, the log's own provenance rule: "A row describing an audit carries that audit artifact's own `completed_at`" | `events/live-trial-2026/status.md`, activity log | The activity log has **no row for the judging-stage audit**. The evidence stage has three (`:112`, `:119`, `:123`), so the convention is established. The first-pass FAIL at `21:20:00Z` and this second pass are visible only inside other rows' prose. Neither `atj event gate` nor `atj event unit record` appends to the activity log — I read both in `atj/event.py` — so this will not fill itself | Add two rows: `2026-09-17T21:20:00Z` initial-judging stage audited, first pass, FAIL — F1, F2 major; and this pass with its own `completed_at` and result. Input identity: the eight judgments, both summaries, `status.md`; output: `audits/judgments.md` |
| minor (F12) | First-pass F4 required repair: "Record the defect against `ev:live-trial-2026:team-podcast:f3fdd342465f:d06f90cc` here **and in `docs/framework-fix-plan.md` as further evidence for T3.2**" | `docs/framework-fix-plan.md:141-153` | The fix-plan half of F4 was not done. `01f559f` added D7, D8 and D9 and nothing else; there is no mention of `evidence_limited_criteria`, the Scope-section contradiction, or F4 anywhere in the file. T3.2 still reads "**three of those defects were introduced by the repairs**" and lists the three from the evidence stage. F4 is a fourth — the first pass traced it to the `18:41:56Z` F2 repair — and T3.2's own count is now understated, in the section whose whole argument is that repair rounds introduce defects | Add the manifest self-contradiction to T3.2's evidence list and correct "three" to "four". Do not edit the frozen manifest |
| minor (F13) | `framework/rubrics/head-to-head.md`, comparison-value table and `tie_break_order`; `atj/matchup.py:255-278` | `events/live-trial-2026/adjudications/team-podcast-reliability-ne.md`, Impact table final row; repeated at `events/live-trial-2026/status.md:136` | The impact table states that the tie-break is "narrowed", that "`reliability` cannot break a tie for this pairing", and that the order "effectively becomes functional, then product". That does not follow. `tie_break()` reads `combined_margin` — a comparison value produced fresh in the matchup — not the initial score, and value `0` is defined as "Substantially equal **or** insufficient comparative evidence", which is a finding a matchup panel makes on the common evidence, not one the initial `NE` forces. team-ledger has eleven run records including a 35-test suite at exit 0; team-podcast has three unclassified outcomes. A panel could legitimately return a nonzero reliability margin from that. The adjudication's own preceding row hedges correctly ("must be comparison value `0` **unless the common evidence supports otherwise**") and the tie-break row drops the hedge. Nothing has moved yet, but this prejudges a stage that has not run and the ledger now repeats it | Correct `status.md:136` to say the matchup must reach its own comparative finding on `reliability` and that no initial result constrains it. The adjudication record itself is a versioned attachment; if the event-director wants it corrected, issue `adj:live-trial-2026:team-podcast:02` rather than editing this one. Either way the matchup stage must not inherit the unhedged claim |
| minor (F14) | `framework/policies/disagreement-and-adjudication.md`: "A human event official owns disqualification, rules exceptions, and unresolved final ties"; `schemas/adjudication.schema.json` `decided_by` — "A human official's role"; `atj/scoring.py:431` | `events/live-trial-2026/adjudications/team-podcast-reliability-ne.md` front matter | `decided_by: event-director` with `persona: run-judging-event@1.0.0` records a human decision that no reader can distinguish from an agent writing the role into a required field. There is no signature, no separate approval timestamp, and `started_at` equals `completed_at`. `atj/scoring.py:431` uses a non-empty `decided_by` as one of the gates that lets an adjudication move an official total, so the field carries authority the record cannot evidence. Mitigations, which is why this is minor and not major: nothing moved (`score_override` absent, `resolved_score: null`), this trigger is not one of the policy's human-only categories, `event.md:27-31,70` does assign adjudication to the event-director, the commits are authored by the role holder, and the document discloses the persona substitution in plain text and files D10 rather than concealing it | No repair to this record. Record a new framework defect (D12): the adjudication artifact needs a way to record human assent distinctly from agent authorship — an approver field, a decision timestamp, or a human-countersigned approval state. Until it exists, no adjudication may move an official total or name an advancing team on this evidence alone |

## Advisories

**A1, A2, A4, A5 — carried from the first pass, unchanged.** A1: the four-way
`NE` is anchored convergence, not four independent discoveries, and the panel
report must say so. A2: run records embed host paths, and `atj validate
publication` takes one artifact at a time. A4: the two panels ran against
different framework commits; no number is affected. A5: all eight judgments are
still `draft`/`unvalidated` while both units are `complete`.

**A6 — the first pass's 9-gram overlap figure does not reproduce, and the
adjudication quotes it as measured.** The adjudication's Confidence section cites
"a maximum pairwise 9-gram overlap of 0.0076" as something "the stage audit
measured". Reconstructing the stated method (9-grams, fenced and inline code and
`[[evidence:…]]` links stripped) I get a podcast maximum of **0.0149**
(`judge-product-agentic` vs `judge-security-ops`) and a ledger maximum of
**0.0092**, not 0.0076 and not the pair the first pass named. The tool's own
measure (`atj/reports.py:194`, 6-grams, nothing stripped) gives **0.0248** for the
podcast panel and **0.0202** for the ledger panel. Every variant is two orders of
magnitude below `SIMILARITY_THRESHOLD = 0.80`, so the independence conclusion is
unaffected and stands. But a hand-computed statistic a reader cannot reproduce
should not be quoted as a measurement in a second artifact. Prefer the tool
figure and the threshold it is measured against.

**A7 — the adjudication's own metadata is thin.** `started_at` equals
`completed_at` (zero elapsed) for a record that reasons over eight evidence ids
and four run records, and `validation_state: unvalidated` although `atj validate
reports` now validates it as one of 17 artifacts. Same class as A5; neither the
schema nor any policy requires more.

**A8 — re-recording the units will restamp them.** `atj/event.py:record_unit`
writes `completed_at: versions.now()` and the CLI has no override, so recording
the audit result on `judging:team-ledger` and `judging:team-podcast` will
overwrite `19:29:14Z` and `21:02:13Z` with the current clock and misstate when
judging finished. `can_advance` (`atj/event.py:421-426`) only blocks on
`audit_result == "FAIL"`, so `not-audited` does not block the gate. Decide
deliberately: either accept the restamp and record the original values in the
activity log, or leave the units `not-audited` and let this audit and the gate
carry the result.

**A9 — one citation is missing from the adjudication's Evidence reviewed list.**
The Disputed-claims table cites `ev-podcast-12` through `judge-product-agentic`,
and the Evidence reviewed section does not list it. The id is real and resolves in
the manifest, so this is completeness, not accuracy.

**A10 — `events/live-trial-2026/status.md.bak` is present on disk, untracked.**
`atj/event.py:745` writes it on every ledger update; `.gitignore:27` ignores it,
which was the agreed closure of evidence-stage F12/D5. Recorded so a later pass
does not re-raise it. Nothing to do.

## Completion gate

- [x] **No blocking findings** — no missing required evidence, no invalid
      arithmetic, no version mismatch (`atj release-check` PASS,
      `require_versions` passes on the adjudication), no severe disagreement, no
      submission executed in this round, and nothing private in `public/`, which
      holds only `.gitkeep`. The adjudication clears the publication gate as a
      private artifact
- [ ] **No major findings** — **one.** F8, the ledger's adjudication table empty
      while an adjudication exists and is applied by `atj score`
- [x] **Calculations valid** — both consolidations reproduce; the regenerated
      team-podcast summary matches the committed file across all 318 leaf values
      including the new `resolution` block; all eight rendered score tables
      re-render `unchanged` and diff clean; `total: null`, `finalized: false`,
      `weighted_points: null` for `reliability`; 58.25 is provisional everywhere
      it appears; `NE` is never a zero at any layer; no score moved in the repair
      round and no judgment was edited
- [x] **Evidence references resolve** — `atj validate reports` PASS over 17
      artifacts with zero problems; every evidence id and run record the
      adjudication cites resolves, and I re-verified its five load-bearing facts
      against the run records and the pinned checkout rather than against the
      citations
- [x] **Version and identity checks pass** — `rubric:
      submission-evaluation@1.0.0` and `persona: run-judging-event@1.0.0` both
      resolve in `framework/personas.md`; `framework_commit: 01f559fa` is a real
      commit and is the parent of the commit that recorded the adjudication;
      `commit` and `evidence_package_id` match the four judgments; 355 tests
      pass; `atj release-check` PASS
- [x] **Privacy boundary passes** — the adjudication is `visibility: private`,
      contains no host path, uid map, credential or personal identifier, and
      `atj validate publication` returns CLEAR; `public/` still holds only
      `.gitkeep`

**FAIL.**

**The `judgments-audited` gate may not be set yet.** `atj event gate
events/live-trial-2026 judgments-audited passed --audit audits/judgments.md` must
not be run until F8 is closed and F9-F11 are corrected in the same edit.

Nothing here requires a judge to rescore, a submission to be re-run, or a frozen
evidence package to be edited. No score changes. The repairs, in order:

1. **F8, F9, F10, F11** — one edit to `events/live-trial-2026/status.md`: add the
   adjudication row to the Blockers and adjudications table, replace the
   "`adjudications/` is empty" sentence with a pointer to the `21:20:42Z` row,
   and add the two missing audit rows to the activity log. `last_updated` is
   fixed by step 4.
2. **F13** — correct `status.md:136` so it does not tell the matchup stage what
   its `reliability` comparison value must be.
3. **F12 and F14** — `docs/framework-fix-plan.md`: add the manifest
   self-contradiction to T3.2 and correct "three" to "four"; add D12 for the
   missing record of human assent.
4. **Then re-record the units and set the gate**, reading A8 first:
   `python3 -m atj event unit events/live-trial-2026 record --id
   judging:team-ledger --stage initial-judging --output judgments/team-ledger
   --audit-result "PASS WITH ADVISORIES"`, the same for `judging:team-podcast`,
   then `python3 -m atj event gate events/live-trial-2026 judgments-audited
   passed --audit audits/judgments.md`.
5. **Carry F1 and F5 into the consolidation stage.** They are this stage's only
   open substantive obligations and neither can be closed here.

Two things the repairs must not undo. team-podcast has no official total and must
not acquire one: `reliability` is `NE`, the adjudication accepted it rather than
clearing it, and 58.25 is not a score, not a ranking input and not a bye seed.
And `atj score`'s "applied adjudication" line must never be quoted without the
"unresolved NE" line that follows it, until D11 is fixed.
