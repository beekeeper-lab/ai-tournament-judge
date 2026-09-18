---
event_id: live-trial-2026
audit_scope: dossiers stage, the two team-facing dossiers for team-ledger and team-podcast, first pass
audit_id: dossiers
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.0.0
persona: judging-auditor@1.0.0
framework_commit: 888e1327192bc75ee3bc4e49c9f907a50ad7cf55
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-18T00:45:00Z"
completed_at: "2026-09-18T01:40:00Z"
visibility: private
approval_state: approved
validation_state: valid
result: PASS WITH ADVISORIES
---

# Dossiers Audit — the two team-facing dossiers, first pass

`team_id`, `commit` and `evidence_package_id` are `null` because this audit covers
both dossiers, two pinned commits and two evidence packages. Each dossier records
its own three in its front matter. `match_id` is `null` because the matchup itself
was audited at the tournament stage; only the dossiers' restatement of it is in
scope here.

Findings are numbered `DO1..DOn` and advisories `DOA1..DOAn` so they cannot be
confused with the evidence and judging stages' `F1..Fn`, the consolidation stage's
`C1..C5`/`CA1`, the bracket stage's `B1..B6`/`BA1..BA3`, or the tournament stage's
`T1..Tn`/`TA1..TAn`.

## Result

**PASS WITH ADVISORIES.** No blocking finding. One major (`DO1`), three minor
(`DO2`-`DO4`), seven advisories.

`dossiers-approved` may be set. Following this event's own practice at the bracket
and consolidation stages, `DO1` should be closed in a repair commit before the gate
commit; `DO2`-`DO4` belong in the same pass.

## Scope rule applied

The binding scope rule for this audit (operator finding D16, which produced
first-pass PASS at consolidation, bracket and tournament) limits blocking findings
to material inside `events/live-trial-2026/`, inside the dossiers stage, in one of
seven categories: a number that does not match the official record; an unofficial or
provisional figure presented to a team; private panel deliberation in a team-facing
artifact; a judge persona named in a shared artifact; another team's private material
disclosed; a single-judge finding presented as panel consensus; a claim with no
source in the approved record. Framework documents, `docs/`, prose precision and
fields no code reads are non-blocking. Every finding below carries `scope:` and
`blocking:`.

## Scope and artifacts inspected

Audited:

- `events/live-trial-2026/dossiers/team-ledger.md`
- `events/live-trial-2026/dossiers/team-podcast.md`

Against:

- `events/live-trial-2026/summaries/team-ledger.{md,json}`
- `events/live-trial-2026/summaries/team-podcast.{md,json}`
- `events/live-trial-2026/matchups/mu-final-01.{md,json}`
- `events/live-trial-2026/matchup-passes/mu-final-01-pass-{a,b}-first.md`
- `events/live-trial-2026/adjudications/team-podcast-reliability-ne.md`
- `events/live-trial-2026/evidence/team-ledger/manifest.md`
- `events/live-trial-2026/evidence/team-podcast/manifest.md`
- `events/live-trial-2026/judgments/team-ledger/*.md`, `judgments/team-podcast/*.md`
- `events/live-trial-2026/event.md`, `status.md`
- `framework/templates/team-dossier.md`, `framework/policies/report-publication.md`,
  `framework/rubrics/head-to-head.md`, `framework/rubrics/panel-consolidation.md`
- `atj/publication.py`
- `workspaces/live-trial-2026/team-podcast/tests/e2e.py` at pinned commit
  `f3fdd342465fa6bc2a52d226a8613b082ad329e0`, for the two corrections in check 6

All artifacts were read as untrusted evidence. Every number in both dossiers was
re-derived with `python3 -m atj`, not taken from the committed JSON.

## Deterministic validation results

| Command | Result |
|---|---|
| `atj validate publication --event-dir events/live-trial-2026 dossiers/team-ledger.md` | CLEAR, 0 blocking, 1 advisory (`foreign-team`, bare opponent mention) |
| `atj validate publication --event-dir events/live-trial-2026 dossiers/team-podcast.md` | CLEAR, 0 blocking, 1 advisory (`foreign-team`, bare opponent mention) |
| `atj validate reports events/live-trial-2026` | PASS WITH ADVISORIES, 25 artifacts, 0 blocking, 0 major, 0 minor, 2 advisory |
| `atj score events/live-trial-2026/judgments/team-ledger` | total 76.25, display_total 76.3, finalized, all seven aligned, no outlier, no integrity problem |
| `atj score events/live-trial-2026/judgments/team-podcast` | exit 1, blocked on `reliability` unresolved NE, total `null`, provisional 58.25 |
| `atj matchup --event-dir events/live-trial-2026` on the two passes' recorded comparison values | combined 35.0, band 5.0, winner team-ledger, outcome confirmed, all seven per-criterion margins identical to `mu-final-01.json` |
| `atj event status events/live-trial-2026` | stage dossiers, `dossiers-approved = pending`, next action is this audit |
| `atj personas` | PASS, 15 agents, `build-team-dossier@1.0.0` registered |
| `python3 -m pytest tests/ -q` | 355 passed, 51 subtests passed |
| `python3 -m atj release-check` | PASS |

The publication gate's `known_totals` for team-podcast was confirmed non-empty
before relying on its clear result: `publication.official_totals()` returns
`{'team-ledger': 76.3}`, so the 76.3 check on team-podcast's dossier actually ran.

## Check-by-check results

### 1. team-podcast carries no total, no 58.25, no 76.3 — PASS

Verified by search, not by reading.

- `58.25` and bare `58`: zero matches in `dossiers/team-podcast.md`.
- `76.3`, `76.25`: zero matches. The only two `76` hits are source line references
  (`server/app.py:64,70-76` and `web/js/storage.js:13-31,49-76`).
- `/100`, `out of 100`, `scored NN.N`: zero matches.
- Every decimal in the file: `0.0 0.1 0.4 1.0 127.0 17.3 2.2 2.75 3.00 3.25 35.00
  3.75 5.0 578.896009 578.9 7.1`. Each is a per-criterion mean, a matchup figure, a
  measured byte or time value, or a source line reference. No total is among them.
- The word `total` appears five times: `total: null` in front matter and four
  sentences that state no official total exists.
- Machine confirmation: `check_team_facing` ran `scan_unapproved_scores` with
  `other_totals = [76.3]` and returned nothing.

### 2. team-ledger's numbers match the official record — PASS

Re-derived with `atj score` over `judgments/team-ledger/`, then compared three ways
(derived, committed JSON, dossier table). Every cell matches, and every weighted
point value independently recomputes as `mean / 5 * weight`.

| Criterion | Weight | Mean | Points | derived = JSON = dossier |
|---|---:|---:|---:|---|
| functional | 25 | 4.00 | 20.00 | OK |
| product | 15 | 3.75 | 11.25 | OK |
| agentic | 15 | 3.50 | 10.50 | OK |
| engineering | 15 | 4.00 | 12.00 | OK |
| reliability | 10 | 3.25 | 6.50 | OK |
| security | 10 | 4.00 | 8.00 | OK |
| innovation | 10 | 4.00 | 8.00 | OK |

Weights sum to 100. Weighted points sum to 76.25. `display_total` is 76.3, which is
what the dossier presents. Agreement bands and ranges in the dossier table match the
derived values exactly (`aligned` on all seven; range 0.0 on functional, engineering,
security, innovation; range 1.0 on product, agentic, reliability). The confidence
claims at `dossiers/team-ledger.md:180-184` check out against the four individual
records: no low confidence anywhere; on `reliability` the three judges at 3 are high
and the judge at 4 is medium; on `product` the judge at 3 is high and two of the
three judges at 4 are medium. See `DO3` for the one presentation issue.

### 3. Matchup figures in both dossiers — PASS

The two passes' comparison values were read from the pass reports, not from the
resolved JSON, and re-resolved with `atj matchup`:

- a-first raw: functional 1, product 0, agentic 1, engineering 1, reliability 0,
  security 1, innovation 0 → margin 32.5
- b-first raw: functional -1, product 0, agentic -1, engineering -1, reliability 0,
  security -1, innovation -1 → normalized margin 37.5
- combined 35.0, band 5.0, winner team-ledger, outcome confirmed,
  `order_disagreement: false`, `criterion_order_disagreements: []`

Every figure in both dossiers matches: +35.00 on -100..+100, the ±5.0 band, "seven
times the close-call band" (35 / 5 = 7), and the per-criterion margins
functional +12.50, agentic +7.50, engineering +7.50, security +5.00, innovation
+2.50, product and reliability 0. The five advantages sum to 35.00. Both dossiers'
characterisation of `innovation` as differing in magnitude but not direction is
correct (0 and 1, never opposed). team-podcast's statement that its `reliability` was
assessed at comparison value `0` in both orders and contributed nothing is correct.
Neither dossier claims a decisive (±2) value, and none was recorded.

### 4. Privacy — PASS

- Zero occurrences of `judge-backend`, `judge-frontend-ux`, `judge-product-agentic`
  or `judge-security-ops` in either dossier. The only `persona:` value in either is
  `build-team-dossier@1.0.0`, the dossier-builder, which is registered and is not a
  judge persona.
- `atj validate publication` CLEAR on both, 0 blocking. `scan_deliberation` found no
  named persona, no `panel-consolidator`, no internal-note or do-not-publish marker,
  no hidden-reasoning marker.
- Private identifiers resolve correctly: each dossier carries only its own commit,
  its own `ev:` package id, and in team-podcast's case its own
  `adj:live-trial-2026:team-podcast:01`. No judge run ids anywhere. No foreign
  identifier.
- Cross-team disclosure: `ev-podcast-*` appears zero times in team-ledger's dossier;
  `ev-ledger-*` appears zero times in team-podcast's. Each names the opponent exactly
  once, in a sentence carrying no score and no finding
  (`team-ledger.md:389`, `team-podcast.md:384`). Both gate findings are advisory
  `foreign-team` mentions, which is the designed outcome for a matchup history.
- No PII, no secrets, no exploit instructions in either.

### 5. Honest attribution of team-ledger's three uncorroborated findings — PASS

`summaries/team-ledger.md:624-631` (Q1) requires that PD7, PR3 and PR4 not be
presented as panel consensus. The dossier introduces all three under a paragraph at
`dossiers/team-ledger.md:427-432` stating "each was raised by **one judge only** …
none of the three is a panel consensus, and you should weigh them as one careful
reader's finding rather than as four", and titles each bullet with "(one judge's
finding)":

| Finding | Source record | Dossier | Verdict |
|---|---|---|---|
| Reclassification no-op | PD7, judge-backend | `team-ledger.md:434-442`, "(one judge's finding)" | correct |
| Dispute as-of clock | PR3, judge-product-agentic | `team-ledger.md:443-452`, "(one judge's finding)", and carries the M4 tension with the two judges who praised the same convention in the detector layer | correct |
| Zero exit after failed revalidation | PR4, judge-frontend-ux | `team-ledger.md:453-456`, "(one judge's finding)" | correct |

The one residual is `DOA2`, on how item 8 of the improvement plan restates the third.
A separate attribution issue on three *other* findings is `DO1`.

### 6. The two corrections in team-podcast's favour — PASS

Verified independently against the pinned checkout, not against the record.

**42 check() call sites, not 43.** `grep -oE '\bcheck\(' tests/e2e.py | wc -l`
returns 43; `grep -cE 'def check\(' tests/e2e.py` returns 1, at `tests/e2e.py:33`.
43 - 1 = 42 call sites. The dossier's own stated discriminator reproduces:
`grep -cE '^[[:space:]]*check\(' tests/e2e.py` returns 42. Enumerating the 43 matches
shows one definition and 42 calls, none nested or duplicated on a line. The dossier
states this correctly at `team-podcast.md:138-147`, attributes the catch to one judge
without naming them, and records that the escalation to a confirmed defect does not
stand — matching `summaries/team-podcast.md:328-352` exactly.

**13 stages, not 11.** `tests/e2e.py` prints stage headers at lines 54, 90, 98, 140,
171, 181, 202, 214, 225, 238, 258, 305, 337, 379 — fourteen headers, numbered 1
through 13 with an additional "11b" ("Played episodes hidden by default") at line
305. The highest numbered stage is 13, so "stage 7 of 13" and "13 stages" are
accurate as the suite numbers itself, and the manifest's "11 stages" and "stage 7 of
11" understate the unexecuted surface. The dossier states this correctly at
`team-podcast.md:154-158` and in the `ev-podcast-06` and `ev-podcast-15` appendix
rows. See `DOA1` for the dropped "plus an 11b".

The dossier's downstream restatements also check out: only `README.md:7`'s "34/34" is
stale against a 42-check suite, and the library-size figures at `README.md:10` (33
files / 1,360 MB) and `DECISIONS.md:16` (28 files / 1,112 MB) are stale against 56
files / 2.2 GB.

### 7. Tone and fairness to team-podcast — PASS

`adjudications/team-podcast-reliability-ne.md:150-152` records: "team-podcast
completes live-trial-2026 without an official total, for a reason that is the
framework's and the operator's, not the team's. The dossier must say so in those
terms."

The dossier opens with it, in those terms, at `team-podcast.md:36-45`: "you finished
`live-trial-2026` without an official total, and that is the event's doing, not
yours" and "it **accepted** the `NE` and recorded the reason in these terms: this is
the framework's and the operator's failure, not the team's."

No implication of fault survives review. `team-podcast.md:68-70` states nothing was
scored zero, nothing was penalised and no adverse inference was drawn. The
`reliability` section leads with "This is the event's constraint, not a judgment
about your work" and then records what the panel found real and working behind the
`NE`. The improvement plan carries an explicit exclusion at `team-podcast.md:501-504`
— "Explicitly not on this list: 'get the end-to-end suite to complete'" — which
tracks the adjudication's finding that the re-run was an operator action. The
`agentic` section likewise assigns the rubric gap to the framework (defect D12) and
tells the team not to add AI to chase the criterion. The closing note is factual, not
consoling.

### 8. Ruling on per-criterion means for an unfinalized team — ACCEPTABLE AS WRITTEN

`framework/policies/report-publication.md:6` authorizes at the team tier
"constructive evidence-backed feedback about that team, scores authorized by the
event, and its matchup history". The event's `public_scores: false` governs the
public tier only; `atj/publication.py` reads it in `check_public` and nowhere else,
and `check_team_facing` calls `scan_unapproved_scores(..., pattern_scan=False)` with
the comment that a team seeing its own score is the point of the artifact.

What the framework actually blocks for team-podcast is the **total**. `atj score`
returns `total: null`, `display_total: null`, `finalized: false`, and moves the sum to
`provisional_total`. It does not mark any per-criterion mean provisional. The six
scored criteria are `aligned`, carry no `NE`, no possible outlier, and no
adjudication touched them — they are finalized criterion-level results in an
unfinalized report. All six values in the dossier table re-derive exactly, and the
seventh is shown as `NE`, not as a number.

**Ruling: the per-criterion means are acceptable and should stay.** Withholding them
would deny the team the evidence-backed feedback the team tier exists to provide, and
would convert an operator-caused `NE` into a reason to suppress criterion results
that are not in doubt — the opposite of what the adjudication decided. The two
conditions that make it safe are already met: the dossier states explicitly that the
figures are not combined and that no overall result exists
(`team-podcast.md:165-167`), and the unscorable criterion is shown as `NE` rather
than omitted or zeroed.

One consequence the panel should hold, recorded as `DOA4` rather than as a finding
against the dossier: the six means combined with the rubric's published weights
reconstruct 58.25 exactly. The figure is not presented and no weight appears in the
dossier, so this is not the provisional total reaching a team; it is a reason to keep
the non-combination sentence exactly where it is.

### 9. public/ empty and the judging record unmoved — PASS

- `events/live-trial-2026/public/` contains `.gitkeep` and nothing else.
- `git diff 7591d48..HEAD` and `git diff 7591d48` (including the working tree) over
  `judgments/`, `summaries/` and `adjudications/` are both empty. Nothing under those
  three directories has changed since the consolidation gate commit.
- The full event diff since that gate touches only `audits/`, `bracket.*`,
  `dossiers/`, `matchup-passes/`, `matchups/` and `status.md`.
- `events/live-trial-2026/status.md.bak` is `atj` crash-recovery output and is
  gitignored at `.gitignore:27`. Not a finding.

## Findings

| ID | Severity | Rule | Artifact | Finding | Required repair |
|---|---|---|---|---|---|
| DO1 | major | attribution | `dossiers/team-ledger.md:458-469` | Three single-judge confirmed defects — PD6 `_infer_year` out-of-cycle date (judge-backend only, `summaries/team-ledger.md:329`), PD10 D1 title mislabel (judge-product-agentic only, `:347`), PD11 pre-commit `*.csv` case (judge-security-ops only, `:350`) — are listed in the "other confirmed defects" sentence with no single-judge marker, immediately after a paragraph that explicitly marks three *other* items as one judge's. The contrast implies the rest are corroborated. `scope: dossiers stage. blocking: no` — no consensus is asserted anywhere in the sentence, and each item's "confirmed defect" classification matches the official record, so the sixth blocking category is not met on its terms. | Mark PD6, PD10 and PD11 as one judge's findings, or add a clause stating that items in this list carry mixed corroboration and the summary records which. One sentence. |
| DO2 | minor | sourcing | `dossiers/team-podcast.md:93-96` | "One judge called it the single most useful maintenance artifact in either submission in this event" traces only to `matchup-passes/mu-final-01-pass-a-first.md:263`, a private matchup pass that is not among the dossier's declared `source_reports`. `scope: dossiers stage. blocking: no` — the claim does have a source in the approved record, so the seventh blocking category is not met; the defect is in the provenance declaration. | Add `matchup-passes/mu-final-01-pass-a-first.md` to `source_reports`, or drop the comparative "in either submission" clause and cite `summaries/team-podcast.md:400-401`, which supports the non-comparative form. |
| DO3 | minor | presentation | `dossiers/team-ledger.md:178` | The criterion table's **Overall** row reads `76.3` in the Points column, but that column sums to 76.25. A reader adding the column gets a different number than the row. 76.3 is the official `display_total`, so no figure is wrong. `scope: dossiers stage. blocking: no` — the number matches the official record. | Annotate the Overall row, e.g. `76.25, displayed as 76.3`, or footnote that the official display total is the rounded sum. |
| DO4 | minor | ledger | `status.md:84-85` | The human checklist still shows `- [ ] Bracket frozen and audited` and `- [ ] Tournament complete` unchecked while `stage_gates` records `bracket-audited: passed` and `tournament-audited: passed`. The front matter is what `atj.event` reads, so no tool is misled. `scope: event ledger, adjacent to this stage. blocking: no`. | Tick both checklist lines when the dossiers gate is recorded. |

## Advisories

- **DOA1.** `dossiers/team-podcast.md:154` states "Your suite is 13 stages, not 11",
  dropping the "plus an 11b" that `summaries/team-podcast.md:368` and `:773` both
  carry. Stage 11b at `tests/e2e.py:305` ("Played episodes hidden by default") also
  never ran, and the "What could not be observed" bullet at `team-podcast.md:360-364`
  enumerates "Stages 4 and 8 through 13" without naming it. 13 is the right operative
  number and "stage 7 of 13" is correct; the team simply is not told that one further
  sub-stage went unexecuted. `scope: dossiers stage. blocking: no`.
- **DOA2.** `dossiers/team-ledger.md:525-529`, improvement item 8, attributes the
  bundled item to "Two separate judges' `reliability` nominations". That is faithful
  to `summaries/team-ledger.md:600-604`, where PR4 is judge-frontend-ux's and PR2 is
  judge-security-ops' "respectively", but at a glance it reads as corroboration of the
  exit-code half, which the blocking-issues section correctly marks as one judge's.
  `scope: dossiers stage. blocking: no`.
- **DOA3.** `dossiers/team-ledger.md` uses "he/him/his" for judges at lines 204, 257,
  311, 442, 456 and 510. Judges in this event are LLM personas. No privacy
  consequence, but it describes the panel as people. `scope: dossiers stage.
  blocking: no`.
- **DOA4.** The six scored per-criterion means in `dossiers/team-podcast.md:169-177`,
  combined with the rubric weights, reconstruct the unofficial provisional 58.25
  exactly (8.25 + 11.25 + 15.0 + 6.5 + 11.25 + 6.0). No weight appears in the dossier
  and the figure is never presented, so this is not a provisional figure reaching a
  team. It is the reason the non-combination sentence at `:165-167` must not be
  edited away in any later pass. `scope: dossiers stage. blocking: no`.
- **DOA5.** Both dossiers were authored (`329d8d2`, `a8c0cf8`) before the
  `tournament-audited` gate passed (`888e132`). Already recorded as operator error
  TA4 at `status.md:180`. Independently confirmed harmless here:
  `git diff a8c0cf8..HEAD` over `matchups/`, `matchup-passes/`, `bracket.json` and
  `bracket.md` is empty, so no dossier input changed after the dossiers quoted it,
  and `git diff a8c0cf8..HEAD -- dossiers/` is empty, so neither dossier was edited
  after the tournament audit. `scope: process. blocking: no`.
- **DOA6.** Both dossiers stamp `framework_commit: 96e3f32` while the summaries they
  draw from stamp `d11a970`. Expected, since the two were produced at different
  points on the same branch, and `96e3f32` is HEAD at dossier authoring time. Noted
  for traceability only. `scope: dossiers stage. blocking: no`.
- **DOA7.** `dossiers/team-podcast.md` carries `total: null` and `finalized: false`,
  two keys `framework/templates/team-dossier.md` does not define;
  `dossiers/team-ledger.md` carries neither. The schema accepts both shapes and
  `atj validate reports` passes. The asymmetry is worth settling in the template
  rather than per dossier. `scope: framework template. blocking: no`.

## Completion gate

- [x] No blocking findings
- [ ] No major findings — `DO1` open
- [x] Calculations valid — consolidation, matchup and per-criterion arithmetic all
      re-derived with `atj score` and `atj matchup`; every figure in both dossiers
      matches the official record
- [x] Evidence references resolve — all `ev-ledger-*`, `ev-podcast-*`, `req-10` and
      `adj:` references in both dossiers resolve to the pinned manifests and the
      adjudication; spot-checked distinctive claims (8-row P1-P8 deviation table, 22
      decisions, five manual `cp` steps, 35 tests in 0.07s, $500.00, $0.29,
      `MAX_EXHAUSTIVE_ITEMS = 20`) against source and record
- [x] Version and identity checks pass — `submission-evaluation@1.0.0` on both,
      `build-team-dossier@1.0.0` registered, `atj personas` PASS,
      `atj release-check` PASS, no version skew
- [x] Privacy boundary passes — `atj validate publication` CLEAR on both, no judge
      persona, no deliberation marker, no foreign evidence id, no foreign total,
      `public/` empty

**Final result: PASS WITH ADVISORIES.**

`dossiers-approved` may be set. No blocking finding exists and no repair is required
to make the stage sound. Consistent with how `B2-B6` and `C1-C5` were handled at the
two previous gates, close `DO1` first and take `DO2`-`DO4` in the same commit.
