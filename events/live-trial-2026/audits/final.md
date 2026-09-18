---
event_id: live-trial-2026
audit_scope: final-audit stage, the complete judging record of live-trial-2026 end to end, including the eight prior stage audits, first pass
audit_id: final
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.0.0
persona: judging-auditor@1.0.0
framework_commit: e72f14d5c31644257091f9d78a503eb841e4b87d
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-18T00:25:00Z"
completed_at: "2026-09-18T00:37:00Z"
visibility: private
approval_state: approved
validation_state: valid
result: PASS WITH ADVISORIES
---

# Final Event Audit — the complete judging record, first pass

`team_id`, `commit` and `evidence_package_id` are `null` because this audit covers
the whole event: two teams, two pinned commits, two evidence packages, one matchup
and eight prior stage audits. Each finding names its own artifact.

Findings are numbered `FA1..FAn` and advisories `FAA1..FAAn` so they cannot be
confused with any earlier stage's codes (`F1..F19`/`A1..A12`, `C1..C7`/`CA1..CA3`,
`B1..B6`/`BA1..BA3`, `T1..T3`/`TA1..TA4`, `DO1..DO4`/`DOA1..DOA4`).

Every artifact in this event, including the eight prior audits, was treated as
untrusted evidence. Nothing was accepted because a prior audit asserted it. Both
consolidations, the matchup, the bracket, the two corrections made in
team-podcast's favour, one prior audit's rebuttal of another prior audit's
finding, and thirteen of the twenty-four claimed framework defects were
re-derived from source.

## Result

**PASS WITH ADVISORIES.** No blocking finding. One major (`FA1`), four minor
(`FA2`-`FA5`), five advisory. The `final-audit-passed` gate **may be set** and
the event **may be marked complete**.

The scope rule applied is D16 (`docs/framework-fix-plan.md:224-231`), as ruled by
the third-pass judging audit and applied at the four gates since. Every finding
below was tested against the eight blocking triggers by name. None meets one.
`FA1` is major and carries a **pre-delivery condition**, not a gate condition: it
must be repaired before either dossier is handed to a team, and it does not
affect any number, any gate, or the result.

## Scope and artifacts inspected

The whole of `events/live-trial-2026/`: `event.md`, `teams.md`, `status.md`
(76 log rows), 2 submissions, 2 evidence manifests, 27 run records, 8 judgments,
2 summaries (`.md` and `.json`), 1 adjudication, `bracket.json`/`bracket.md`,
1 resolved matchup (`.json` and `.md`), 2 matchup pass reports, 2 dossiers, the
8 prior audits, `OPERATOR-NOTES.md`, and the empty `public/`. Outside the event:
`docs/framework-fix-plan.md`, both rubric front matters, the consolidation and
head-to-head policies, `framework/personas.md`, `framework/templates/`,
`schemas/`, `atj/`, `.claude/hooks/`, the git history of every event artifact,
branch `fix/framework-d7-d10-d12`, and both pinned checkouts under
`workspaces/live-trial-2026/`.

Working-tree note: `status.md` carries one uncommitted change at audit time,
`current_stage: dossiers` → `final-audit` with `last_updated` moved to
`00:23:31Z`. The `final-audit-passed` gate is `pending`, which is the correct
state for an event being audited here. Nothing else in the tree is modified.

## Deterministic validation results

| Command | Result |
|---|---|
| `python3 -m pytest tests/ -q` | **355 passed, 51 subtests passed** |
| `python3 -m atj release-check` | **PASS**, all nine sections including single-source |
| `python3 -m atj validate reports events/live-trial-2026` | **PASS WITH ADVISORIES** — 26 artifacts, 0 blocking, 0 major, 0 minor, 2 advisory (both the known `foreign-team` notice on a dossier naming its opponent) |
| `python3 -m atj event validate events/live-trial-2026` | **FAIL, 1 problem** — D20 alone, confirmed below |
| `python3 -m atj event status events/live-trial-2026` | stage `final-audit`, 2 eligible, 6 units complete, gate `final-audit-passed` pending |
| `python3 -m atj score .../judgments/team-ledger --json` vs committed `summaries/team-ledger.json` | **0 differing keys** across the fully flattened structure |
| `python3 -m atj score .../judgments/team-podcast --json` vs committed `summaries/team-podcast.json` | **0 differing keys**; exit status 1, finalization blocked |
| `python3 -m atj matchup <judges' own raw values> --event-dir events/live-trial-2026` vs committed `matchups/mu-final-01.json` | **0 differing keys** |
| `python3 -m atj bracket verify bracket.json --event-dir …` | **PASS (constraints re-derived from the roster)** |
| `python3 -m atj validate publication` on each dossier | **CLEAR (0 blocking)** on both |
| `atj.event.audit_supports_gate` replayed against all 8 gate artifacts | **0 problems** on all 8 |

## 1 — End-to-end arithmetic

Both consolidations and the matchup reproduce exactly. Nothing was accepted from a
prior audit's arithmetic.

**team-ledger, 76.3.** The four judgments' `scores:` front matter blocks were read
directly and match `source_scores` in the committed JSON judge by judge. Recomputed
by hand from the canonical weights (`score / 5 × weight`): 20.00 + 11.25 + 10.50 +
12.00 + 6.50 + 8.00 + 8.00 = **76.25** exact, displayed **76.3** under the rubric's
own `display_decimals: 1` / `rounding: half-up`
(`framework/rubrics/submission-evaluation.md:7-8,45-51`, implemented at
`atj/scoring.py:48,157`). `finalized: true`, no `NE`, no outlier, all seven
criteria `aligned` under `aligned_max_range: 1`. Re-running `atj score` over the
committed judgments produced a structure identical to the committed JSON on every
key. The dossier's `76.25`-versus-`76.3` note at `dossiers/team-ledger.md:180` is
correct and correctly sourced.

**team-podcast, no total.** Six criteria scored, `reliability` `NE` from all four
judges. `total: null`, `display_total: null`, `finalized: false`,
`blocked_reasons` populated, `adjudication_required` still listing
`{criterion: reliability, trigger: unresolved-ne}` after the adjudication is
applied. The six scored criteria sum to 58.25, recorded only as
`provisional_total` and nowhere presented as a result. Recomputed by hand:
15.00 + 11.25 + 8.25 + 11.25 + 6.00 + 6.50 = **58.25**. `reliability` carries
`mean: null` and `weighted_points: null` — not `0`.

**The matchup, +35.00.** I did not re-use the committed JSON. I transcribed each
judge's own `comparisons` block from that judge's own pass report — a-first
`{functional 1, product 0, agentic 1, engineering 1, reliability 0, security 1,
innovation 0}`, b-first `{functional -1, product 0, agentic -1, engineering -1,
reliability 0, security -1, innovation -1}` oriented positive-to-team-podcast —
built a fresh input and ran `atj matchup`. Result: winner `team-ledger`, combined
margin **35.0**, outcome `confirmed`, `order_disagreement: false`, a-first margin
32.5, b-first normalized 37.5, every per-criterion margin identical to the
committed file, **zero differing, missing or extra keys**. Checked against the
rubric's own formula `criterion_margin = comparison_value / 2 × criterion_weight`
and against the close-call band of 5 read from `head-to-head.md` front matter:
35.00 is seven times the band, so `confirmed` is correct and no tie-break was
reached.

`innovation` is the only criterion where the two passes differ (0 a-first, +1
b-first normalized). That is a magnitude difference within one direction, not a
sign flip, so `order_disagreement` is correctly `false` and the criterion
contributes the mean, +2.50. Even setting `innovation` to 0 in both passes the
winner and the confirmation are unchanged.

## 2 — Gate integrity

Nine gates, eight recorded `passed`. For each I did three things: confirmed the
named artifact exists and is the audit of that stage; replayed
`atj.event.audit_supports_gate` against it for that stage's name; and checked out
the version of the audit file that was **in the tree at the commit that set the
gate**.

| Gate | Set in | Audit result in the tree at that commit | `audit_supports_gate` today |
|---|---|---|---|
| configuration-audited | `7dab838` | PASS WITH ADVISORIES | 0 problems |
| roster-frozen | `8af6858` | PASS WITH ADVISORIES | 0 problems |
| evidence-validated | `0677b6c` | PASS WITH ADVISORIES | 0 problems |
| judgments-audited | `4ecbdb4` | PASS WITH ADVISORIES | 0 problems |
| consolidation-audited | `7591d48` | PASS WITH ADVISORIES | 0 problems |
| bracket-audited | `aa3b62f` | PASS WITH ADVISORIES | 0 problems |
| tournament-audited | `888e132` | PASS WITH ADVISORIES | 0 problems |
| dossiers-approved | `e72f14d` | PASS WITH ADVISORIES | 0 problems |

**No gate was set on a FAIL.** Each of the eight artifacts carries
`result: PASS WITH ADVISORIES`, `visibility: private`, `approval_state: approved`,
a non-empty body, the right `event_id`, and an `audit_scope` naming its own stage —
the six things `atj/event.py:92-127` checks.

The `judgments-audited` refusal is real, not asserted. I checked out each of the
three historical versions of `audits/judgments.md` and ran the gate function
against them:

- `ebb76c2` (first pass) — `result: FAIL` → refused: *"result is 'FAIL'; a gate needs PASS or PASS WITH ADVISORIES"*
- `956c2b1` (second pass) — `result: FAIL` → refused, same reason
- `4cd5dd3` (third pass) — `result: PASS WITH ADVISORIES` → 0 problems, and the gate was set two commits later

The evidence stage shows the same shape across three passes. The mechanism worked:
a gate could not be set while the audit of record said FAIL.

No stage advanced past a pending gate. `event.md` and both evidence manifests
have no commit after `0677b6c` (the evidence gate), which precedes `4a96452` (the
first four judgments) — so no rubric, weight, persona, bracket policy or evidence
changed after judging began. Each of the eight judgment files has **exactly one
commit in its entire history**: no judgment was edited after promotion, at any
point, by anyone. `score_override` appears nowhere in the event except in four
sentences stating its absence.

The one recorded sequencing error (`TA4`, the dossier stage started before
`tournament-audited` passed) stands as the tournament audit wrote it. I confirmed
the mitigation independently: no gate was falsified, and the tournament inputs are
byte-identical across `96e3f32..a8c0cf8`. The finding is correctly logged in
`status.md:181` in the terms the audit demanded, including the sentence that the
only reason it cost nothing is that the result came back PASS.

## 3 — The `NE` chain

Traced end to end. `reliability` was never treated as a zero and was never charged
to team-podcast at any point.

1. **Four independent judges.** Each of the four `judgments/team-podcast/*.md`
   front matters records `reliability: NE` in its own `scores:` block. No judgment
   body references another judge; each carries its own evidence citations (14 to 18
   unique `ev-podcast-*` ids each).
2. **`atj score` refused to finalize.** Re-run today: exit status 1,
   `total: null`, `display_total: null`, `finalized: false`, criterion `mean: null`,
   `weighted_points: null`, `agreement: not-scored`, `ne_judges` listing all four.
   The provisional sum is fenced off in `provisional_total` and the console output
   states it "is not an official total and must not be published or used for bye
   seeding".
3. **The adjudication accepted rather than cleared.** `resolution: resolved`,
   `decided_by: event-director`, `resolved_score: null`, no `score_override`. The
   committed JSON records the resolution **alongside** the source scores with the
   note "no source score was modified", and `atj score` still refuses the total
   after applying it — which is defect D11, and which here is the correct
   conservative behaviour.
4. **The matchup.** `reliability` took comparison value `0` in **both** passes,
   from each judge independently. The a-first report states the basis at `:99` and
   `:397`: the defined value for "substantially equal **or** insufficient
   comparative evidence", recorded "as my own finding on the common evidence" and
   explicitly not imposed by the adjudication. A `0` contributes no margin to
   either side; team-podcast lost no ground to it. The adjudication had predicted
   this outcome without binding it (`status.md:160`), and the prediction was kept
   as a prediction.
5. **The dossier.** `dossiers/team-podcast.md:41-69` states that `NE` is not a
   zero, that nothing was scored zero or penalised, that no adverse inference was
   drawn, and that the cause is the framework's and the operator's. The criterion
   table shows `NE` for reliability with no points column at all.

The one place a reader could reconstruct a number is the per-criterion mean table
(`DOA4`, carried forward from the dossiers audit): the six means times the rubric
weights give 58.25. That sentence at `:166-168` — the means "are not combined into
an overall result for this team" — is the only thing standing between the table
and a fabricated total, and it must survive every future edit. The table itself
carries no weight column and no points column, which is the right mitigation. I
agree with the dossiers audit that withholding the six means would have converted
an operator-caused `NE` into the suppression of results that are not in doubt.

## 4 — Ledger accuracy

`status.md` holds 76 activity rows. Machine-checked: **every timestamp ascends**,
no descending pair. The first row is `2026-09-16T23:27:41Z`, the last
`2026-09-18T00:50:00Z`. The provenance convention at `:196-207` is stated exactly
and the documented exception at `:189-194` (the third-pass judging audit's
fabricated `22:19:00Z`) is disclosed rather than hidden.

Claims spot-checked against artifacts rather than accepted:

| Ledger claim | Verified against | Outcome |
|---|---|---|
| "35 passed, exit 0, no network" | `runs/team-ledger-pytest-01.json` | exact: `exit_status: 0`, stdout `35 passed in 0.07s`, `--network none`, read-only mount, `--user 65534` |
| "27 run records" | `runs/*.json` | exactly 27 |
| bracket "2 entrants, 1 final, 0 byes", digest `5bd7a2f7e711e721` | `bracket.json` | exact on every field |
| "A-first margin +32.50, B-first normalized +37.50, combined +35.00" | re-derivation above | exact |
| `check()` count corrected to 42 | pinned checkout `f3fdd342` | `grep -c 'check('` → 43, call sites → **42**, one `def check(`. The correction is right and the frozen manifest's 43 is wrong |
| `tests/e2e.py` stage count corrected to 13 | pinned checkout | 14 numbered headers, 1-13 with an `11b` at line 305. Correct |
| "diff reports `118a119,433` and nothing else" (tournament audit) | staged vs promoted a-first | reproduced exactly; b-first staged copy byte-identical |
| judging audit F17 "is a false finding" | branch `fix/framework-d7-d10-d12` | the operator is right: D12 is there as a defect-table row at `:195` and a full section at `:275` |

The rows recording operator errors are accurate, not self-flattering, and in two
cases are harder on the operator than they had to be. `status.md:129` records the
missing `ffmpeg` as "an operator error that disadvantaged this team relative to
team-ledger". `:156` records that the ledger once asserted the opposite of the
committed JSON about adjudication and names the cause. `:157` **corrects an
earlier correction**, downgrading a claim that three judges caught three evidence
defects to the true attribution (two, one, and none). `:165` records that a repair
round re-broke the ascending-order rule and calls it "the fifth repair-introduced
defect of the event". `:181` accepts the concurrency finding in the auditor's own
words. `:182` retracts an overstatement about the provisional figure and names the
two private lines where it does appear. I checked that last one: `58.25` appears
in exactly two private pass reports, both as explicit negations, and in no
dossier, no matchup artifact and no public file.

Two ledger defects remain, both minor: `FA2` (checkbox) and `FA3` (operator
notes), below.

## 5 — Privacy end to end

- `public/` contains only `.gitkeep`, tracked and empty. Nothing was ever written
  to it; `event.md` sets `public_scores: false` and declares no ceremony.
- Every private artifact carries `visibility: private`: both manifests, all eight
  judgments, both summaries, the adjudication, the matchup, both pass reports,
  the bracket, and all eight audits. Both dossiers carry `visibility: team`.
- **No judge persona appears in either dossier.** Neither file contains any
  `judge-backend`, `judge-frontend-ux`, `judge-product-agentic` or
  `judge-security-ops` string. Attribution is by count only ("three of the four
  judges", "one judge").
- **No cross-team private material.** `dossiers/team-ledger.md` contains zero
  matches for `ev-podcast-*`, `f3fdd342` or `58.25`. `dossiers/team-podcast.md`
  contains zero matches for `ev-ledger-*`, `9d21b770`, `76.3` or `76.25`. Each
  names the other only as the opponent in a match both were in, which is
  match-public and is exactly what the `foreign-team` advisory asks a human to
  confirm.
- `atj validate publication` returns **CLEAR, 0 blocking** on both dossiers.
- All 27 run records ran under `podman 6.1.0` with `--network none`, a read-only
  source mount and a non-root user. No submission was executed on the host at any
  point in the event.

## 6 — Framework defects: spot check of the deliverable

`docs/framework-fix-plan.md` is the trial's main output, so I checked whether its
claims are true rather than whether they are numerous. Thirteen were verified
directly against code, schemas, templates or live commands:

| Defect | Verified how | Verdict |
|---|---|---|
| D7 | ran `atj score` on team-podcast | Real. The console prints `blocked_reasons` and the provisional sum; `adjudication_required` never appears |
| D11 | applied the adjudication via `atj score` | Real. "applied adjudication … to reliability" prints, and the criterion is still `not-scored` with `adjudication_required` outstanding |
| D13 | `atj/scoring.py:429-432` | Real. `approval_state == approved` and a non-empty `decided_by` are the gates; nothing distinguishes a human from a role string |
| D15 | `atj/event.py:533` | Real. `completed_at` is `versions.now()` with no override |
| D17 | **created a real worktree** at the gitignored `.claude/worktrees/`, ran `release-check`, removed it | Real, and the strongest one. `single-source FAIL — duplicate-number: …/tests/test_canonical_model.py holds an editable copy of the official weight for 'functional' (25)`. Gitignoring genuinely does not help. PASS restored on removal |
| D18 | `atj render --help` | Real. The only subcommand is `judgment` |
| D19 | `framework/templates/consolidated-team-report.md:30-31` | Real, verbatim |
| D20 | `atj event validate` | Real. The sole failure, quoted below |
| D21 | `atj/event.py:604-617` | Real. Digests exist only for `evidence:`, `judging:`, `consolidation:` |
| D22 | `schemas/matchup.schema.json` `$defs/pass/properties/comparisons` | Real. `minProperties: 1` on both passes |
| D23 | `.claude/hooks/pre-advance.sh:79-101` | Real. The `case "$command"` match reads pre-command gate state with no sequencing |
| D24 | `atj validate publication events/live-trial-2026` | Real. `cannot read artifact: [Errno 21] Is a directory` |
| D12 | branch `fix/framework-d7-d10-d12` | Real and correctly described as proposed-not-landed |

None of the thirteen is misattributed or overstated. Two rows in the defect table
are now **stale in the framework's favour**, which is `FA4`: D2 and D6 are both
closed in `25624c7` — the judgment template carries the `model` block at
`framework/templates/individual-judgment.md:24-28`, and the hook strips heredoc
bodies — but neither row is marked `done` the way D3 and D5 are. A plan that
understates its own progress is a smaller problem than one that overstates it, but
this list is the deliverable and the next reader will act on the table.

One defect class this event produced is **not** in the plan, and it is the
mechanism behind this audit's only major finding. I propose it as **D25**:
nothing in `atj` ever writes `approval_state`. Six sites read it —
`atj/ceremony.py:372`, `atj/publication.py:305,311`, `atj/cli.py:457,652`,
`atj/event.py:119`, `atj/scoring.py:429` — and not one can set it. There is no
`atj approve`, no gate that inspects the approval state of the artifact a stage
produced (only of the audit that reviewed it), and no reminder anywhere in the
pipeline. The sample event cannot catch this because `atj/demo_writer.py` writes
`approval_state: approved` into every artifact directly, so no persona or command
ever has to perform the transition.

A second, narrower one, proposed as **D26**: `framework/templates/audit-report.md`
ships `approval_state: draft`, while `atj/event.py:119` refuses any audit that is
not `approved` as gate authorization — so an audit written exactly to its own
template can never open a gate, and all nine audits in this event were hand-
promoted. Related: `atj/reports.py:32` maps `audits` to schema `None`. The one
artifact kind that authorizes every stage transition in the framework is the only
kind with no schema at all; it is checked for placeholders and template shape and
nothing else.

## 7 — Known outstanding issues, confirmed

All three confirmed as described, not rediscovered.

**D20 is the sole `atj event validate` failure.** Verbatim:

    ERROR roster: performance-qualified byes need a consolidated score for every
    eligible team; missing for ['team-podcast']
    Event validation: FAIL (1 problems, stage final-audit)

One problem, and it is the bye-policy rule firing with `bye_count: 0` in
`bracket.json`. The two repairs available inside the event — fabricating a total
for team-podcast, or changing `event.md`'s bye policy mid-event — are each a
blocking offence under CLAUDE.md, so the event correctly did neither. I reach the
same ruling as the bracket audit: framework, not event, and not blocking here.

**D22: `matchup-passes/` is still undeclared.** `atj validate reports` covered
exactly 26 artifacts today; I enumerated them and all 26 are `.md` files inside
the ten `ARTIFACT_KINDS` directories. Neither pass report is among them, so no
schema, template or citation check reaches the only written record of the
comparative reasoning. The mitigation holds: the directory is outside every
declared subdirectory, so `atj validate publication` on a pass report fails closed
with `BLOCKING [location-unknown]` and nothing there can be cleared for release.

**D24: `atj validate publication` cannot take a directory.** Confirmed. Each
dossier had to be named individually, which is how I ran it.

## Findings

| Severity | Rule | Artifact | scope / blocking | Finding | Required repair |
|---|---|---|---|---|---|
| **major** | `framework/policies/report-publication.md` ("Every published artifact records its visibility level and approval status"); `atj/ceremony.py:372`; D16 scope rule | 16 artifacts: `judgments/*/*.md` (8), `summaries/*.md` (2), `bracket.md`, `matchups/mu-final-01.md`, `matchup-passes/*.md` (2), `dossiers/*.md` (2) | scope: event / blocking: **no** | **FA1.** Every artifact produced from the initial-judging stage onward still carries `approval_state: draft` and `validation_state: unvalidated`, while its stage gate is recorded `passed` and `atj validate reports` reports it valid. Two concrete consequences, both verified in code, not inferred. First, `atj/ceremony.py:372` refuses to render a dossier that is not `approved` — so the two deliverables this event exists to produce cannot be released as committed, under a gate literally named `dossiers-approved`. Second, `atj/cli.py:457`'s guard against silently rewriting an approved judgment's scores table only arms on `approval_state == approved`, so it protected nothing for the entire event. Mitigating and checked: each judgment has exactly one commit in its history, so the unarmed guard cost nothing in fact. Carried as advisory since intake `A2`, re-raised as judging `A5` and consolidation `CA3`, never closed, and it now sits on the event's exit state. Tested against all eight blocking triggers: no number is wrong, no gate lacks a passing audit, no `NE` became a zero, no score moved, no judgment was edited, nothing private reached public output, no stage jumped a pending gate, and no conclusion lacks evidence. Non-blocking. | Before either dossier is delivered: set `approval_state: approved`, `validation_state: valid` and `approved_by` on the two dossiers by the `publication_approval` official named in `event.md:29`, and either promote or deliberately leave the other fourteen with one ledger row saying which and why. Log the mechanism as **D25** (below) in the fix plan. |
| minor | `status.md` front matter is the source of truth for gate state; dossiers audit `DO4` | `events/live-trial-2026/status.md:87` | scope: event ledger / blocking: **no** | **FA2.** The human checklist still reads `- [ ] All team dossiers approved` while `stage_gates.dossiers-approved` is `passed`. This is the third recurrence of the same defect: the bracket audit found it on two boxes, `DO4` found it on two more and required them ticked "when the dossiers gate is recorded", the repair ticked those two, and the dossiers box was then left behind by the very commit that passed its gate. The front matter is what `atj.event` reads, so no tool is misled. | Tick `All team dossiers approved`, and tick `Final event audit passed` and `Event marked complete` as those gates are recorded. Better: stop maintaining a second copy of the gate state by hand, since the front matter already holds it. |
| minor | CLAUDE.md, "Event state lives in `events/<event>/status.md`" | `events/live-trial-2026/OPERATOR-NOTES.md:8-10,62` | scope: event / blocking: **no** | **FA3.** The operator notes are stale to the point of contradicting the ledger: they state the event is at stage `initial-judging` and that "team-podcast has none of its four yet", and that defects are "Tracked as D1-D6" against a plan that now runs to D24. The file disclaims official status in its first four lines and nothing official rests on it, which is why this is minor rather than major. | Refresh it to a completion note, or delete it and let `status.md` stand alone. |
| minor | Accuracy of the trial's primary deliverable | `docs/framework-fix-plan.md:24,28` | scope: framework / blocking: **no** | **FA4.** D2 and D6 are listed as open Tier 1 work. Both landed in `25624c7`, which `OPERATOR-NOTES.md:70,88` states and which I verified in the template and the hook. D3 and D5 carry `done` in the same column, so the table's own convention exists and these two rows simply did not get it. | Mark D2 and D6 `done` with their commit, as D3 and D5 already are. |
| minor | D18; consolidation finding `C1` | `summaries/team-podcast.md:86-88` and the team-ledger twin | scope: event / blocking: **no** | **FA5.** The `C1`/D19 repair replaced a false provenance claim ("Generated by `atj consolidate` … Never transcribed by hand") with an unsatisfiable instruction: "The block must be regenerated by `atj render consolidated` before `atj validate` runs against this file." That command does not exist, `atj validate reports` passes the file anyway, and a reader is told a required step was skipped. No number is affected — both blocks reproduce exactly against the canonical JSON. | Reword to what is true: the block is transcribed from `summaries/<team>.json`, verified cell by cell against it, and cannot be generated because `atj render consolidated` does not exist (D18). |

## Advisories

**FAA1 — D25, proposed.** Nothing in `atj` can set `approval_state`; six sites
read it and none writes it. This is the mechanism behind `FA1` and it will recur
in every event until there is an `atj approve` (or equivalent) and a gate that
looks at the artifacts a stage produced, not only at the audit that reviewed them.
The sample event is structurally unable to catch it: `demo_writer.py` writes
`approved` directly.

**FAA2 — D26, proposed.** `framework/templates/audit-report.md` ships
`approval_state: draft`, which `atj/event.py:119` then refuses as gate
authorization; and `atj/reports.py:32` gives the `audits` kind no schema at all.
The artifact that authorizes every stage transition is the least validated kind in
the framework and cannot open a gate if written exactly to its own template.

**FAA3 — tournament `T3` is still open.**
`workspaces/live-trial-2026/staging/matchup/pass-a-first.md` is still the 118-line
first extraction against a 433-line promotion. I reproduced the audit's claim
exactly: `diff` reports `118a119,433` and nothing else, and the b-first staged
copy is byte-identical to its promotion. The staged front matter carries the same
comparison values that were promoted, so the provenance record is incomplete
rather than inconsistent. `workspaces/` is untracked and `status.md:180` records
the discrepancy, so this is bookkeeping.

**FAA4 — the ledger's timestamp convention is now unstable.** Several late rows
carry stamps ahead of their own commit times (the `00:50:00Z` repair row was
committed at `00:23:22Z` real time), and the dossiers audit's `completed_at` of
`01:40:00Z` is ahead of the real clock entirely. A genuinely later entry therefore
cannot be added without either inventing a larger number or breaking the ascending
rule that evidence finding `F8` established. This audit's own front matter carries
real clock readings. Underlying history is correct and traceable through git, so
this is explicitly non-blocking under D16, but the next event should take audit
timestamps from the commit rather than from an agent that has no clock.

**FAA5 — `event.md:20` records `model_used: null`** while every artifact produced
under it records `claude-opus-5`. A field no code reads.

## 8 — Does this record hold?

Yes, with one qualification, and the qualification is about delivery, not about
the result.

Put the challenge concretely. A team or an outside reviewer has three plausible
lines of attack, and the record answers all three from artifacts rather than
assertions.

**"team-podcast was denied a total by the organiser's own mistake."** True, and
the record says so before the team does. The event under-provisioned the sandbox,
discovered it after judging had begun, and declined to re-run because re-running
would have invalidated four judgments that cite the frozen package. That trade is
argued in the adjudication, not hidden in it, and the decision is recorded as the
framework's and the operator's failure rather than the team's, in those words, in
the artifact the team receives. More importantly the record can show the missing
criterion changed nothing: two teams is an exact power of two so the bye policy
never reads a total (proved twice by the bracket audit, once by code path and once
by rebuilding the draw under five score permutations including the unofficial
58.25, bit-identical every time); the head-to-head rubric forbids selecting on
initial totals and both passes recorded that they did not; and `reliability` came
back `0` from both matchup judges independently, on the defined value for
insufficient comparative evidence. The strongest available answer to this
challenge, short of not having made the error, is the one the record gives.

**"the winner was picked by the same model that wrote the judgments."** True, and
disclosed in every artifact's `model_used`. The defences are structural rather
than rhetorical: four judges ran concurrently and blind, each judgment has exactly
one commit and none references another judge, the head-to-head ran in both
presentation orders with each pass blind to the other, and every number in the
event came out of `atj`, not out of a model — I reproduced all three of them from
the judges' own raw inputs with zero differing keys. What the record cannot claim
is reproducibility of the judgment itself, and it does not claim it anywhere.

**"the judges held a factual error against the team."** True on one point, caught,
and corrected in the team's favour without any score moving. Three judges repeated
the evidence package's wrong 43-`check()` figure; one caught it; the judging audit
re-derived 42 and ordered the correction; the consolidated report and the dossier
both carry it. I verified 42 myself at the pinned commit, and the 13-stage
correction too. The frozen manifest still contains the wrong 43 and still
contradicts itself on `evidence_limited_criteria` at `:74` — deliberately, because
evidence is frozen once judging begins — and both defects are disclosed downstream
in the artifacts anyone would actually read.

What makes the record stand is not that it is clean. It is that its errors were
found by its own process, are written down with their attribution corrected where
the first attempt got it wrong, and none of them moved a number. Three stages
needed a second or third audit pass and two of those FAILs were on the operator's
own ledger, not on the teams' work. Five defects were introduced by repair rounds
and every one of them was recorded as such.

The qualification: **the two dossiers are not in a deliverable state** (`FA1`).
They are correct, privacy-clean and audited, but the framework's own renderer
would refuse both, and the gate that says they are approved is not a statement the
artifacts themselves make. That is twenty minutes of work and one ledger row, and
it must happen before either team sees its dossier. It does not change the result
and it does not hold the gate.

One thing this event proves that no test in the repository does. `atj validate
reports` returned zero findings at every stage, on manifests holding nine
misdirected citations, a fabricated version number, a scan credited to the wrong
observation, a self-contradicting scope paragraph and a wrong check count that
three judges then repeated against a team. Every substantive error in this event
was caught by an LLM audit, and none by a validator. The fix plan says this at
`:171-189`. It is the most useful thing the trial produced and it should lead the
event report.

## Completion gate

- [x] No blocking findings
- [ ] No major findings — one (`FA1`), scope `event`, `blocking: no` under D16, carrying a pre-delivery condition
- [x] Calculations valid — both consolidations and the matchup re-derived from source with zero differing keys
- [x] Evidence references resolve — `atj validate reports`, 26 artifacts, 0 blocking
- [x] Version and identity checks pass — `release-check` PASS on all nine sections, 355 tests pass, personas registry PASS
- [x] Privacy boundary passes — `public/` empty, publication CLEAR on both dossiers, no persona and no cross-team private material in any team-facing artifact

## Verdict

**PASS WITH ADVISORIES.**

`final-audit-passed` **may be set** and `live-trial-2026` **may be marked
complete**.

The judging record reproduces from source at every point where a number exists, no
gate was opened without a passing audit behind it, the one unscorable criterion
was never charged to the team that it cost, and nothing private left the panel.

Two conditions attach to completion, neither of which holds the gate:

1. `FA1` must be repaired **before either dossier is delivered to a team**. The
   dossiers are `approval_state: draft` and `atj/ceremony.py:372` will refuse
   them.
2. `FA2`-`FA5` are cheap and should be closed as part of the completion commit.

Log `D25` and `D26` in `docs/framework-fix-plan.md` before the next event opens.
`D20` will make `atj event validate` return FAIL for this event permanently until
it is fixed in `atj/`; that is a known framework defect with no permitted in-event
repair, and it must not be repaired by touching this event.
