---
event_id: live-trial-2026
audit_scope: initial-judging stage, both teams
audit_id: judgments
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.0.0
persona: judging-auditor@1.0.0
framework_commit: 92c66879b382115957dd395e0f76855c0cd17ee0
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-17T21:05:00Z"
completed_at: "2026-09-17T21:20:00Z"
visibility: private
approval_state: approved
validation_state: valid
result: FAIL
---
# Judging Audit — initial-judging stage, team-ledger and team-podcast

`team_id`, `commit` and `evidence_package_id` are `null` because this audit
covers two teams, two pinned commits and two evidence packages. Each finding
names its own.

## Result

**FAIL.** No blocking finding. Two major findings. Five minor, four advisory.

Neither major requires a judge to rescore, a submission to be re-run, or a
frozen evidence package to be edited. Both are text corrections — three
sentences across three judgments, and one row of the ledger.

The stage is in better shape than that verdict sounds, and it is worth saying
where, because the repairs must not disturb it:

- **Every official number reproduces.** Both consolidations, both summary JSON
  files, and all eight rendered score tables regenerate byte-identically from
  the front-matter scores and `framework/rubrics/submission-evaluation.md`. No
  judge typed a weight, a weighted point value or a total anywhere.
- **`NE` is handled correctly end to end.** `reliability` carries
  `weighted_points: null`, `mean: null`, `total: null`, `finalized: false`. It
  is never a zero, it is excluded from the provisional sum rather than counted
  as 0, and it blocks the official total exactly as the rubric requires. 58.25
  appears in three places and is labelled provisional in all three.
- **Independence holds.** Maximum pairwise wording overlap is 0.8% against the
  tool's 80% threshold, and every shared phrase traces to a document both judges
  legitimately read. No cross-team material appears in either panel.
- **Citation accuracy is high on the ledger panel and good on the podcast
  panel.** I re-derived roughly thirty-five citations against the pinned
  checkouts and the run records. The ledger panel produced zero misdirected
  citations across four judgments. The podcast panel produced one, inherited
  from its evidence package, in three judgments — F1.

What fails is F1, a false and team-adverse factual claim that three of four
podcast judges inherited from a wrong observation in a frozen manifest, and F2,
a ledger row that states the opposite of the tool output it cites on whether an
adjudication is required.

## Scope and artifacts inspected

- `events/live-trial-2026/judgments/team-ledger/` and `judgments/team-podcast/`
  — all eight judgments in full, front matter and body.
- `events/live-trial-2026/summaries/team-ledger.json` and
  `summaries/team-podcast.json` — every field, diffed against freshly derived
  `atj score --json` output.
- `events/live-trial-2026/status.md` (the ledger), `event.md`, `teams.md`, both
  evidence manifests, all 27 run records, both `Containerfile`s.
- `events/live-trial-2026/audits/evidence.md` as the specification for what the
  previous gate already ruled on, so this audit does not re-litigate it.
- The pinned checkouts `workspaces/live-trial-2026/team-ledger` (`9d21b770`) and
  `team-podcast` (`f3fdd342`), both confirmed clean at the pinned commit with
  `git rev-parse HEAD`.
- `framework/rubrics/submission-evaluation.md`,
  `framework/rubrics/panel-consolidation.md`,
  `framework/policies/judge-independence.md`,
  `framework/policies/evidence-and-citation.md`,
  `framework/policies/disagreement-and-adjudication.md`,
  `framework/templates/individual-judgment.md`,
  `framework/templates/consolidated-team-report.md`,
  `schemas/judgment.schema.json`, `framework/personas.md`.
- `atj/reports.py` (`check_judge_independence`, `check_consolidation`) and
  `docs/framework-fix-plan.md`, to avoid re-reporting D1-D6.
- `git diff 0677b6cf..3da42c5 -- framework/ schemas/ atj/ VERSION` and
  `git log 152dd2c1..HEAD -- framework/rubrics/`.

I read no bracket, matchup, dossier or publication artifact; none exists.

## Deterministic validation results

| Command | Result |
|---|---|
| `python3 -m atj validate reports events/live-trial-2026` | PASS — 15 artifacts, 0 blocking, 0 major, 0 minor, 0 advisory |
| `python3 -m atj score events/live-trial-2026/judgments/team-ledger` | 76.3 of 100, all seven criteria `aligned`, no `NE` |
| `python3 -m atj score events/live-trial-2026/judgments/team-podcast` | no official total; `reliability` unresolved `NE`; provisional 58.25 |
| `python3 -m atj render judgment` re-run over copies of all eight | all eight `unchanged`; `diff -r` against the committed files reports no differences |
| `python3 -m atj event unit events/live-trial-2026 list` | 4 units, **0 stale**; both `judging:` units `complete`, `not-audited` |
| `python3 -m atj event status events/live-trial-2026` | blocked on `judgments-audited = pending`, which is this audit |
| `python3 -m pytest tests/ -q` | 355 passed, 51 subtests passed |
| `python3 -m atj release-check` | PASS — rubric, schemas, personas, templates, single-source, version-skew, sample event |
| `python3 -m atj personas` | PASS, 15 agents; all four judge personas `@1.0.0` |

`atj validate reports` covers 15 artifacts: eight judgments, two manifests, two
intake records, `event.md`, `teams.md` and `status.md`. It does not cover
`summaries/*.json` (see A3) and it does not schema-check audit reports —
`atj/reports.py:33` maps `audits` to schema `None`.

## Calculation integrity, re-derived

### Both consolidations reproduce exactly

I regenerated both with `atj score --json` and compared every key against the
committed summaries. Both are **structurally identical** — no key missing, no
key extra, no value different.

`team-ledger`: `total: 76.25`, `display_total: 76.3`, `finalized: true`,
`blocked_reasons: []`, `adjudication_required: []`, `integrity_problems: []`.
The 76.25 → 76.3 step is the rubric's declared `rounding: half-up` at
`display_decimals: 1`; Python's default banker's rounding is not in play at this
value and would not change it.

`team-podcast`: `total: null`, `display_total: null`, `finalized: false`,
`provisional_total: 58.25`, `blocked_reasons: ["reliability: unresolved NE from
judge-backend, judge-frontend-ux, judge-product-agentic, judge-security-ops"]`.

### No judge typed a weight, a weighted point value or a total

I copied both judgment directories to a scratch path and re-ran
`atj render judgment` over the copies. All eight reported `unchanged`, and
`diff -r` against the committed originals reported no differences. The rendered
blocks are therefore derivable from front-matter scores plus the canonical
rubric alone.

I then scanned every judgment body outside the `atj:scores` block for a typed
weight, weighted value or total. Every match is either prose using "weight" as a
verb ("I weight it lightly", "if the panel weights demonstrated agent behavior
heavily") or the judge's own declaration that it typed none. No numeric weight,
no weighted point value and no total appears outside a generated block in any of
the eight files.

### Agreement classification is correct against the consolidation rubric

`framework/rubrics/panel-consolidation.md` front matter: `aligned_max_range: 1`,
`material_max_range: 2`, `outlier_distance: 2`, `minimum_panel: 2`. Every scored
criterion on both teams has a range of 0 or 1, so `aligned` is correct in all
thirteen cases, `possible_outliers` is empty everywhere, and no criterion
reaches material or severe disagreement. Panel size is 4 against a minimum of 2.

There is no severe disagreement anywhere in this stage. The lone one-off
directional score — `judge-security-ops` at 4 on team-ledger `reliability` where
the other three are at 3 — is range 1, `aligned`, and its rationale is
independently grounded (I verified `src/fin/store.py:109-121`,
`src/fin/detect/detectors.py:36-37`, `src/fin/cli.py:53`,
`src/fin/adapters/citi_pdf.py:87` and `src/fin/validate.py:45`; all five support
the claims made of them).

### 58.25 is never presented as an official total

It appears in exactly three places, and all three label it:
`summaries/team-podcast.json` as `provisional_total` alongside `total: null`;
`status.md:74` as "no official total — NE blocks finalization; provisional sum
of scored criteria 58.25"; `status.md:133` as "explicitly not an official total
and not usable for bye seeding". `atj score`'s own output appends the same
warning. Correct.

## `NE` handling

`NE` is treated as a missing observation and never as a zero, at every layer:

- **In the rubric.** "`NE` means not enough evidence and is not a numeric zero."
- **In the summary.** The `reliability` block carries `mean: null`,
  `weighted_points: null`, `range: null`, `agreement: "not-scored"`,
  `scores: []`, `mean_inputs: []`, and `ne_judges` listing all four judges. A
  zero would have produced `mean: 0.0` and `weighted_points: 0.0`.
- **In the arithmetic.** The provisional sum is 58.25 over the six scored
  criteria carrying 90 weight. Had `NE` been read as 0, the sum would be the
  same number but presented against 100 weight as a finalizable total. It is
  not: `total` and `display_total` are both `null` and `finalized` is `false`.
- **In the rendered tables.** All four podcast judgments print
  `| reliability | NE | 10 | — | ... |` and
  `**not finalizable (unresolved NE)**` in the total row, followed by the line
  "`NE` on reliability — this judge produced no finalizable total. `NE` is not a
  zero." No judge-level total was produced for team-podcast.
- **In the gate.** `finalized: false` and a populated `blocked_reasons` are what
  stop the official total. This is correct and must survive the repairs below.

Every one of the four podcast judges states in prose that `NE` is a statement
about the evidence rather than a finding against the submission, and none of
them converts it to a low score by another route.

## Evidence support — the priority check

`atj validate reports` confirms a citation resolves. It cannot confirm the
target contains the claim (D4). So I sampled citations across both panels and
checked each against ground truth rather than against the manifest.

**Coverage.** Every file-path citation in all eight judgments was machine-checked
against the pinned checkouts: all resolve, and no cited line number exceeds its
file's length. Three apparent misses are not citations —
`config/accounts.yaml` and `config/merchant-rules.yaml` appear inside quoted
error-message text and a description of a file the system writes, and
`tests/e2e-smoke.py` is a file `judge-security-ops` proposes the team should
add. I then hand-verified roughly thirty-five substantive citations.

**team-ledger — zero misdirected citations across four judgments.** Verified
among others:

- `judge-backend` F2, "tier 3 `SUBSET_SUM` can never produce a `COMMITTED`
  match". Confirmed at source: `resolve()` is called only on
  `build_edges(...)` (`src/fin/match/engine.py:218-219`), and
  `subset_sum_edges` is generated afterward straight into `by_txn`, whose only
  output is an `outcome="AMBIGUOUS"` link. A correct and high-value finding the
  evidence package did not contain.
- `judge-backend` F7, "`UNMATCHED` links persist `method="AMOUNT_DATE_UNIQUE"`",
  `src/fin/match/engine.py:283`. Exact.
- `judge-frontend-ux` on `src/fin/render.py:29-32` (the DO-NOT-EDIT banner),
  `:158-162` (unmatched ordered before explained) and `:216` (dispute states
  ordered `EXPIRING, OPEN, EXPIRED, NO_STATEMENT`). All three exact.
- `judge-product-agentic` on the dispute clock, `src/fin/cli.py:174` and
  `src/fin/analyze/spend.py:141`. Exact: `as_of = args.as_of or
  spend.as_of(transactions)`, and `as_of()` returns `max(post_date, default=
  date.today())`.
- `judge-security-ops` on `src/fin/validate.py:45` checking only the
  sources→transactions direction, so the torn state it describes passes
  validation clean. Exact.

**team-podcast — one inherited misdirection (F1), otherwise sound.** Verified
among others:

- `judge-backend` C1, the data-loss chain. Every link holds:
  `prune_missing` issues a bare `DELETE FROM episodes` when `present` is empty
  (`server/db.py:94-98`), it is called unconditionally from `index_library()`
  (`server/app.py:64`), `progress` cascades (`server/db.py` `ON DELETE
  CASCADE`) with `PRAGMA foreign_keys = ON`, and `README.md:53` labels that
  directory "Safe to delete".
- `judge-backend` C6, `/api/rescan` returning `transcode.failed` while the UI
  reads only `data.indexed` (`server/app.py:96-97` versus
  `web/js/app.js:368`). Exact.
- `judge-security-ops` F4, `web/js/storage.js:13-31` registering only
  `worker.onmessage`. Confirmed: no `onerror`, no `onmessageerror`, no timeout
  on the promise at `:49-76`. A dead worker leaves it unsettled.
- The `hidePlayed` chain cited by `judge-backend` R2 and `judge-security-ops`:
  `web/js/app.js:19` default `"1"`, and the filter at `:105-118` reading
  `(!hidePlayed || !isFinished(e.id) || playing?.id === e.id)`. Quoted
  verbatim, correctly.
- Every run-record claim I checked reconciles. `judge-product-agentic`
  independently re-derived the 71-second container overlap; I re-derived it
  again from both windows (`e2e-full-01` 00:15:30-00:17:26, `e2e-02`
  00:16:15-00:19:19 → 71s). `e2e-full-02` `duration_seconds: 24.474` → "24.5s".
  `GET /api/media/1 200 OK` is present in both stage-3 failure records, as two
  judges claim. No podman invocation in any record sets `--shm-size`, as
  `judge-backend` claims.

The one failure is F1: the manifest's own `ev-podcast-05` miscounts `check()`
call sites, and three judges repeated the miscount.

## The three known evidence defects, verified and ruled on

`status.md:134` records three defects found during podcast judging and not
repaired, because the evidence package is frozen for a judged team. I verified
each independently against the pinned checkout and rule on each below. The
question is whether the judgments stand, not whether the manifest can be edited.

### (a) `tests/e2e.py` stage count — real, judgments stand

**Verified.** The file prints numbered stage headers at
`tests/e2e.py:54,90,98,140,171,181,202,214,225,238,258,305,337,379` — that is
1 through 13, plus an "11b" at `:305`. The manifest describes the suite as
"11 stages" in `ev-podcast-06`, in the Scope section, and in the Missing-evidence
section, and reports the best run as "stage 7 of 11".

**Effect.** It overstates executed coverage. "Stage 7 of 11" is really stage 7
of 13, and the unexecuted remainder is stages 8-13 — including "12. Delete
downloads" and "13. No JavaScript errors" — not stages 8-11.

**Ruling: invalidates no judgment.** Three of four judges used the correct
figure. `judge-security-ops:147` and `judge-product-agentic:69-74,452-453` both
raise it explicitly as a package correction, with line numbers;
`judge-backend:68` writes "stage 7 of 13" and "42 checks across 13 printed
sections" without labelling it. `judge-frontend-ux` never states a stage total
and enumerates the unreached stages individually (`:158`), so it is not wrong
either. See F5 for the one residual.

### (b) The `evidence_limited_criteria` self-contradiction — real, judgments stand

**Verified.** `evidence/team-podcast/manifest.md:74-76` reads "No criterion is
listed in `evidence_limited_criteria` because every criterion has at least
partial direct evidence or corroborated artifact evidence", while line 11 of its
own front matter reads `evidence_limited_criteria: [reliability]` and line 220
of its Missing-evidence section reads "**`reliability` is recorded in
`evidence_limited_criteria`.**" The Scope sentence is stale text left behind by
the F2 repair of 2026-09-17T18:41:56Z, which set the front-matter field and
added the Missing-evidence bullet. The third-pass evidence audit did not catch
it — exactly the pattern `docs/framework-fix-plan.md` T3.2 describes.

**Ruling: invalidates no judgment.** The operative signal reaching the judges was
consistent: front matter said `[reliability]`, the Missing-evidence section said
`[reliability]` and gave a page of reasoning for it. No judge cited the stale
Scope sentence; `judge-backend:419` reads the front matter correctly and the
other three reason from the run records. The contradiction pointed toward
scoring `reliability` anyway, and no judge took that path.

See F3 — the ledger's attribution of this defect to "three judges independently"
is not supported. No judge reported it.

### (c) `ev-podcast-05`'s `check()` count — real, and the manifest's conclusion is wrong

**Verified.** Against `workspaces/live-trial-2026/team-podcast` at `f3fdd342`:
`grep -c "check("` returns 43; `grep -n "def check("` returns exactly one hit,
the definition at `tests/e2e.py:33`; 43 minus that definition is **42 call
sites**.

So the team's "42/42" claim (`README.md:285`, `DECISIONS.md:9`) is **consistent
with the source**. The manifest's `req-07` conclusion — "contradicted —
internally inconsistent, and neither figure matches the 43 `check()` call sites
actually in `tests/e2e.py`" — is wrong in its second half. The real defect is
narrower: `README.md:7` is stale at "34/34" against a suite of 42.

**Ruling: the judgments stand, but three of them carry the error and must be
corrected before consolidation.** That is F1.

## Independence

**Tool check.** `atj validate reports` runs `check_judge_independence`
(`atj/reports.py:199`) at a 0.80 overlap threshold on 6-grams. It reports no
finding.

**My own check, stricter.** I measured pairwise Jaccard overlap on 9-grams with
code spans and `[[evidence:…]]` links stripped, so shared citations cannot
inflate the score. Maximum across all twelve pairs is **0.0076** (podcast
backend vs security-ops); the ledger maximum is 0.0069. That is two orders of
magnitude below any contamination threshold.

**Every shared phrase traces to a shared source, not to a sibling.** I checked
the top shared n-grams individually. They fall into three groups: the template's
own declaration checklist; sentences quoted from the evidence manifest that all
four judges legitimately read ("a statement about the evidence, not a finding
against the submission" is the manifest's own wording at
`evidence/team-podcast/manifest.md:230-232`; "against the same commit and the
same image produced three different outcomes" is its wording at `:221-224`); and
one phrase quoted from the submission itself ("an AWS bill is not retail Amazon
fraud" is `tests/test_properties.py:325` in the ledger checkout).

**No cross-team leakage.** The only occurrences of `team-ledger` in the podcast
panel are the four negative assertions in the independence declarations ("no
`team-ledger` material was read"). There are zero occurrences of `team-podcast`,
`ev-podcast` or the podcast submission in the ledger panel.

**Every declaration is complete.** All eight judgments carry all four checkboxes
checked, and six of the eight add a specific account of what was and was not
opened.

### The four-way `NE` on `reliability`: convergence, not contamination

I treated this as the highest-risk independence question in the stage and
resolved it against the texts rather than the outcome.

It is **convergence**, for four reasons:

1. **Each judge added analysis the others did not have.** `judge-backend`
   introduces the `--shm-size` / 64 MB `/dev/shm` hypothesis from the recorded
   podman command lines. `judge-product-agentic` introduces a second, different
   hypothesis the package does not name — Chromium's profile under `HOME=/tmp`
   inside the same 64 MB tmpfs that already held 12 MB of media — and
   independently re-derived the 71-second overlap from the run windows.
   `judge-frontend-ux` notices a pattern the manifest does not draw out, that
   both two-episode runs failed at the same stage-3 wait while the isolated
   single-episode probe completed in 1s. `judge-security-ops` raises F4, the
   missing `worker.onerror`, and explicitly notes it pulls in the *opposite*
   direction from the host-contention reading. Four different additions is not
   what a copied report looks like.
2. **The improvement recommendations differ completely** — unit tests under the
   range parser and the last-write-wins comparison; a self-creating fixture
   library with live console capture and a generated check count; nothing
   (deferred to a separate section); and `worker.onerror` plus a promise
   timeout.
3. **The wording overlap is 0.3%-0.8%.**
4. **There is a shared, legitimate cause.** The manifest's front matter and
   Missing-evidence section both told all four judges that `reliability` is
   evidence-limited, and gave the reasoning: three executions, three outcomes,
   none classified. Four judges reading one explicit package signal and each
   independently verifying it against the run records is the expected result,
   not a suspicious one.

Point 4 carries a caveat recorded as A1 below: because the package pre-declared
the limit, the panel should not describe this as four wholly independent
arrivals at the same conclusion. Each judge verified it; none discovered it
unprompted.

## Completeness, versions and identity

- **Four judgments per team**, eight total, one per configured judge id, matching
  `judge_ids` and `judge_run_ids` in both summaries.
- **All required template sections present in all eight**: Executive assessment,
  Scores, Criterion findings, Surprises, Blocking and major issues, Calculation
  and independence declaration. Five of eight add a "Most valuable single
  improvement" section, which the rubric's required criterion response asks for
  per criterion and which no template rule forbids.
- **Rubric and persona versions correct and uniform**: all eight declare
  `rubric: submission-evaluation@1.0.0` and `persona: judge-<id>@1.0.0`, matching
  `framework/personas.md` (`atj personas` PASS).
- **Pinned commit and evidence package id correct in every front matter.** All
  four ledger judgments carry `commit: 9d21b7707f204ef60f5a1cee612f1d4db0a4a575`
  and `evidence_package_id:
  ev:live-trial-2026:team-ledger:9d21b7707f20:b859a240`; all four podcast
  judgments carry `commit: f3fdd342465fa6bc2a52d226a8613b082ad329e0` and
  `ev:live-trial-2026:team-podcast:f3fdd342465f:d06f90cc`. Both match
  `teams.md`, both manifests and both checkouts' `git rev-parse HEAD`.
- **The rubric was not touched during judging.** `git log 152dd2c1..HEAD --
  framework/rubrics/` is empty. Weights, criteria, scale, rounding and the `NE`
  rule are byte-identical to what both panels scored against. Personas remain
  `@1.0.0` for all four judges, as `docs/framework-fix-plan.md` requires.
- **The two panels carry different `framework_commit`s** — ledger `0677b6cf`,
  podcast `3da42c5`. See A4; this is disclosed, permitted and affects no number.

## Privacy and visibility

- All eight judgments declare `visibility: private`. No judgment is anything
  else.
- `events/live-trial-2026/public/` contains only `.gitkeep`.
- No email address, personal name or student-facing identifier appears in any
  judgment. The only identifiers are team ids, the `beekeeper-lab` repository
  org from the roster, and persona ids.
- No judgment quotes an evaluator's or official's name.
- Evidence-stage advisory A5 still applies and is carried as A2 below: the 27
  run records embed absolute host paths and a `65534:65534` uid map. Private
  only. Nothing has left the panel; `atj validate publication` takes a single
  artifact path, not an event directory, and must be run per artifact before
  anything does.

## Findings

| Severity | Rule | Artifact | Finding | Required repair |
|---|---|---|---|---|
| major (F1) | `framework/policies/evidence-and-citation.md`: "Every material conclusion must be traceable to the pinned evidence package" and "Reports must distinguish these classes"; `framework/rubrics/submission-evaluation.md`: "Separate observation from inference" | `events/live-trial-2026/judgments/team-podcast/judge-frontend-ux.md:369`, `judge-product-agentic.md:184,466`, `judge-security-ops.md:187,323` | Three of four podcast judges state that `tests/e2e.py` contains 43 `check()` call sites and that the team's "42/42" claim therefore fails to match the source. It contains **42**; the 43rd `grep -c "check("` match is the definition at `tests/e2e.py:33`, which I verified directly at `f3fdd342`. The team's "42/42" is correct and the only stale figure is `README.md:7`'s "34/34". The error originates in the frozen manifest's `ev-podcast-05` and `req-07`; `judge-backend:606-615` caught it and corrected it in-panel, and the other three repeated it. It is used adversely: `judge-security-ops:187` lists it in the `product` deficiencies and `:323` gives it as a reason it "cannot fall back on" the team's own claim when setting `reliability` to `NE`; `judge-product-agentic:466` lists it as **Confirmed defect 1** attributed to "direct file inspection", an evidence class that judge did not exercise on this claim and that the source contradicts. **No score changes.** `judge-product-agentic` and `judge-frontend-ux` score `product` 4 regardless; `judge-security-ops`'s `product` 3 rests in its score rationale on the library-size contradiction (28 vs 33 vs 56 files), which I verified independently and which stands; `reliability` is `NE` on all four | Do **not** edit the frozen manifest and do **not** change any score. Record the correction once, at panel level, in the consolidated team-podcast report: `tests/e2e.py` has 42 `check()` call sites, the team's "42/42" is consistent with the source, and the documentation defect is `README.md:7` alone. Carry `judge-backend`'s correction forward as the panel's position. In `judge-product-agentic`'s Confirmed defect 1, the evidence-class label "direct file inspection" must not survive into any team-facing artifact attached to this claim |
| major (F2) | `framework/policies/disagreement-and-adjudication.md`: "Adjudication is required for an `NE` that prevents scoring"; `CLAUDE.md`, Source of truth: event state lives in `status.md` | `events/live-trial-2026/status.md:133` | The ledger row for the team-podcast consolidation states "no outlier, **no adjudication required**". `summaries/team-podcast.json`, the artifact that row names as its own output, records `adjudication_required: [{"criterion": "reliability", "trigger": "unresolved-ne"}]`, and the policy requires adjudication for exactly this condition. The "no outlier" half is correct; the adjudication half states the opposite of both the tool output and the policy. `events/live-trial-2026/adjudications/` contains only `.gitkeep`, so the required adjudication does not exist. Left uncorrected, the next stage advances believing none is owed. The most likely origin is A3 below: `atj score`'s human-readable output prints `blocked_reasons` but never prints `adjudication_required`, so an operator reading the console sees no adjudication mentioned | Correct the `2026-09-17T21:02:28Z` row in `status.md` to state that adjudication **is** required on `reliability`, trigger `unresolved-ne`, per `summaries/team-podcast.json` and `framework/policies/disagreement-and-adjudication.md`. Do not alter the summary; it is correct. The adjudication record itself belongs to the consolidation stage, not to this one |
| minor (F3) | `CLAUDE.md`, Source of truth: event state lives in `status.md`; the ledger must state what happened | `events/live-trial-2026/status.md:134` | The row reads "EVIDENCE DEFECT found by three judges independently" and then lists all three defects. Checked against the judgment texts, the attribution does not hold per defect. The `evidence_limited_criteria` contradiction (b) was reported by **no** judge — `judge-backend:419` reads the front-matter value correctly and no judgment mentions the Scope sentence. The `check()` miscount (c) was reported by **one**, `judge-backend:606-615`; the other three repeated the error, which is F1. Only the stage count (a) approaches three, and only if `judge-backend:68`'s silent use of the correct figure counts alongside `judge-security-ops:147` and `judge-product-agentic:69-74`, which raise it explicitly. The ledger currently credits the panel with two catches it did not make, and hides F1 | Restate the row per defect with its actual finder: stage count — `judge-security-ops` and `judge-product-agentic` explicitly, `judge-backend` implicitly; `check()` miscount — `judge-backend` only, with the other three repeating it (F1); `evidence_limited_criteria` contradiction — found by this audit, not by the panel |
| minor (F4) | `framework/templates/evidence-manifest.md`; `framework/policies/evidence-and-citation.md` | `events/live-trial-2026/evidence/team-podcast/manifest.md:74-76` versus `:11` and `:220` | The Scope section states "No criterion is listed in `evidence_limited_criteria`" while the front matter and the Missing-evidence section both list `reliability`. Verified. Stale text from the 18:41:56Z F2 repair that the third-pass evidence audit passed over. It invalidates no judgment (ruling (b) above), but it is a live contradiction in an approved, frozen package that the consolidation stage and any later matchup will read | The package is frozen for a judged team, so do not edit it. Record the defect against `ev:live-trial-2026:team-podcast:f3fdd342465f:d06f90cc` here and in `docs/framework-fix-plan.md` as further evidence for T3.2, and state in the consolidated report that the front matter and Missing-evidence section are authoritative. If the package is ever unfrozen, delete the sentence at `:74-76` |
| minor (F5) | `framework/policies/evidence-and-citation.md`: cite what the artifact contains | `events/live-trial-2026/judgments/team-podcast/judge-security-ops.md:460` versus `:143` and `:525` | Internal inconsistency inside one judgment. This judge correctly establishes at `:143` and `:525` that the suite has 13 sections and that sections 4 and 8 **through 13** are unexecuted — and then its `functional` improvement line at `:460` asks the team to "get sections 4 and 8 through 11 of the suite to run", reverting to the manifest's wrong figure. The judgment's own correction at `:147` is right; this one line contradicts it | Correct `:460` to "sections 4 and 8 through 13" when the consolidated report quotes this improvement. Do not disturb `:143`, `:147` or `:525`, which are correct, and do not change the score |
| minor (F6) | `framework/templates/individual-judgment.md` and `schemas/judgment.schema.json`: `confidence` is `low` / `medium` / `high` with no stated meaning for an `NE` criterion | `events/live-trial-2026/judgments/team-podcast/judge-security-ops.md` front matter versus `judge-frontend-ux.md`, `judge-backend.md`, `judge-product-agentic.md` | New framework defect, not D1-D6. `confidence` is undefined for a criterion scored `NE`, and the four podcast judges split on identical reasoning. `judge-frontend-ux` writes "Low confidence in any numeric score, which is the point. High confidence that `NE` is the correct disposition" and records `low`. `judge-security-ops` writes "High confidence in the `NE` determination itself" and records `high`. `judge-backend` records `low` and explains that it "describes the evidence state, not a suppressed numeric score". The rendered scores table then shows `high` in the Confidence column beside `NE` for one judge and `low` for the other three, which reads as disagreement about the evidence where none exists. The schema accepts both and `atj validate reports` cannot see it | Framework repair, next version, not this event: state in `framework/templates/individual-judgment.md` and in the rubric that for an `NE` criterion `confidence` describes confidence in the `NE` determination, and have `atj render judgment` label the column accordingly. Change no judgment; both readings are defensible under the current text |
| minor (F7) | `schemas/common.schema.json` `model_record`; `framework/templates/individual-judgment.md`: "`verified`: how the model identity was established, or why it could not be" | `events/live-trial-2026/judgments/team-podcast/judge-backend.md` front matter versus the other three podcast judgments | New framework defect, not D1-D6. `model.verified` has no defined threshold, and four judges in the same panel, on materially the same basis, split. `judge-backend` records `verified: false` and reasons that it "has no means of attesting its own model identity from inside the run, so `verified` is false rather than assumed true". The other three record `verified: true` while their notes describe the same situation — runtime self-report plus orchestrator dispatch, "no external attestation", "a corroborated assertion rather than a cryptographic verification". One of them adds that "the timestamps are placeholders supplied by the orchestrator, not clock readings taken here" and still records `true`. All four are schema-valid, so the field currently carries no comparable information. The team-ledger panel's four all record `true` with an identical orchestrator-written note, which is a third pattern | Framework repair, next version: define `verified` as true only for an attestation external to the run, and require the basis in `note`. Change no judgment |

## Advisories

**A1 — the four-way `NE` is anchored convergence, and the panel report should
say so.** The team-podcast manifest declared `evidence_limited_criteria:
[reliability]` in its front matter and devoted a Missing-evidence bullet to the
reasoning before any judge read it. Four judges independently *verified* that
limit against the run records, and each added distinct analysis (see the
Independence section) — which is why I rule convergence rather than
contamination. But none of them discovered it unprompted. The consolidated
report should describe the `NE` as four independent confirmations of a
package-declared limit, not as four independent discoveries. The distinction
matters if the head-to-head later weighs how much of this team's evidence gap is
the framework's doing.

**A2 — run records still embed host paths; nothing may be published without a
per-artifact publication check.** Carried from evidence advisory A5. All 27
records contain an absolute host path and the `65534:65534` uid map, and the
judgments quote run-record content extensively. This is correct for private
artifacts. Note that `atj validate publication` takes a single artifact path and
fails with "Is a directory" when handed an event directory, so the pre-publication
gate has to be run per artifact and cannot be satisfied in one command.

**A3 — `atj score`'s human-readable output omits `adjudication_required`.** The
text rendering prints the criteria table, `**Finalization blocked:**` with
`blocked_reasons`, and the provisional-sum warning. It never prints
`adjudication_required`, which is present in `--json` and in the written summary.
An operator working from the console can therefore state "no adjudication
required" while the committed artifact says the opposite — which is F2. New
framework defect, not D1-D6, and the cheapest of the four to close: print the
field. Related: `summaries/*.json` is covered by no validator.
`check_consolidation` (`atj/reports.py:238`) globs `summaries/*.md`, so it will
engage at the consolidation stage against the `.md` report and has correctly
found nothing to check so far. I verified both JSON summaries by regenerating
and diffing them instead.

**A4 — the two panels ran against different framework commits, and the template
changed between them.** team-ledger's four judgments record `framework_commit:
0677b6cf`; team-podcast's record `3da42c5`. `git diff` between them touches three
files: `atj/cli.py` (+40, the A10 render guard) and two templates, including
`framework/templates/individual-judgment.md` (+33/-11, the D2 fix that moved
`scores`/`confidence` into front matter and added the `model` block). The rubric,
personas, schemas and `atj/scoring.py` are byte-identical across both, so no
number is affected, and `CLAUDE.md`'s freeze list — rubric version, weights,
personas, bracket policy, evidence — is not breached. The ledger discloses the
consequence at `status.md:128`: the four team-ledger judgments failed validation
on the `model` block and had it added from their own front matter. Recording it
here so the head-to-head does not have to rediscover that the two panels
followed different template text.

**A5 — all eight judgments remain `approval_state: draft` /
`validation_state: unvalidated` while both units are `complete`.** This is the
template's default and neither the schema nor any policy requires promotion, so
it is not a finding. But the intake stage promoted its records to approved/valid
on audit (ledger, A2 of the intake audit), and the same should happen here once
the F1/F2 repairs land, so that `atj render judgment`'s approval guard has
something to protect.

## Completion gate

- [x] **No blocking findings** — no missing required evidence, no invalid
      arithmetic, no version mismatch, no severe disagreement (every scored
      criterion is `aligned` at range ≤ 1), no submission executed during
      judging by any judge, and nothing private in `public/`, which holds only
      `.gitkeep`
- [ ] **No major findings** — **two.** F1, a false and team-adverse factual
      claim inherited from `ev-podcast-05` into three of four podcast
      judgments. F2, a ledger row asserting no adjudication is required where
      the tool output it cites and the adjudication policy both say one is
- [x] **Calculations valid** — both consolidations and all eight rendered score
      tables reproduce byte-identically from `atj score` and
      `atj render judgment`; both summary JSON files are structurally identical
      to freshly derived output; 76.25 → 76.3 follows the rubric's declared
      half-up rounding; team-podcast has `total: null`, `finalized: false`, and
      58.25 is labelled provisional in all three places it appears; `NE` is
      never a zero at any layer
- [x] **Evidence references resolve** — `atj validate reports` PASS with zero
      problems; every file-path citation in all eight judgments resolves against
      its pinned checkout with no line number past end of file; roughly
      thirty-five substantive citations hand-verified against ground truth, with
      zero misdirected on the ledger panel and one inherited class on the
      podcast panel, recorded as F1
- [x] **Version and identity checks pass** — `rubric:
      submission-evaluation@1.0.0` and `persona: judge-*@1.0.0` in all eight and
      matching `framework/personas.md`; the correct pinned commit and evidence
      package id in every front matter; `git log 152dd2c1..HEAD --
      framework/rubrics/` empty, so the rubric was not touched during judging;
      `atj release-check` PASS; `atj personas` PASS; 355 tests pass. The
      cross-panel `framework_commit` difference is A4 and affects no number
- [x] **Privacy boundary passes** — all eight `visibility: private`; `public/`
      holds only `.gitkeep`; no personal identifier in any judgment; no
      cross-team material in either panel beyond four negative assertions in the
      independence declarations

**FAIL.**

**The `judgments-audited` gate may not be set.** `atj event gate
events/live-trial-2026 judgments-audited passed --audit audits/judgments.md`
must not be run until F1 and F2 are repaired and re-audited.

Nothing here requires a judge to rescore, a submission to be re-run, or a frozen
evidence package to be edited. No score in this stage changes. The repairs, in
order:

1. Repair **F2** and **F3** — two rows of `status.md`. Neither is a unit output,
   so neither changes a `judging:` input digest.
2. Repair **F1** and **F5** by writing the corrections into the consolidated
   team-podcast report when it is produced, and by recording F1 against the
   panel now so it cannot be lost between stages. Do not edit the eight
   judgments: they are the judges' own records, `atj render judgment` guards
   them, and rewriting a judge's finding is outside an auditor's authority under
   `framework/policies/judge-independence.md` ("An audit may inspect all
   artifacts but may not rewrite substantive judgment"). If the panel decides
   the three affected judgments must carry the correction themselves, that is an
   adjudication under `framework/policies/disagreement-and-adjudication.md`
   attached as a versioned addendum, not an edit.
3. Record **F4**, **F6**, **F7** and **A3** in `docs/framework-fix-plan.md`. F4
   is further evidence for T3.2. F6, F7 and A3 are new defects, none of them
   D1-D6, and A3 is a one-line fix that would have prevented F2.
4. Re-audit this stage. `docs/framework-fix-plan.md` T3.2 is explicit that a
   repair round must itself be audited before the gate, and this event has
   already produced three repair-introduced defects at the evidence stage.
5. Then re-record both units with the result and set the gate:
   `python3 -m atj event unit events/live-trial-2026 record --id
   judging:team-ledger --stage initial-judging --output judgments/team-ledger
   --audit-result "<result>"`, the same for `judging:team-podcast`, and
   `python3 -m atj event gate events/live-trial-2026 judgments-audited passed
   --audit audits/judgments.md`.

One thing the repairs must not undo: team-podcast has no official total and must
not acquire one. `reliability` stays `NE` until an adjudication resolves it on
the evidence, and 58.25 is not a score, not a ranking input, and not a bye seed.
