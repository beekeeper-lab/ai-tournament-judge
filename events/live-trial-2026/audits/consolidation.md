---
event_id: live-trial-2026
audit_scope: consolidation stage, both teams, first pass
audit_id: consolidation
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.0.0
persona: judging-auditor@1.0.0
framework_commit: 1ece86927e0085f46bc597894806289c4fa25ebd
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-17T22:08:40Z"
completed_at: "2026-09-17T22:42:00Z"
visibility: private
approval_state: approved
validation_state: valid
result: PASS WITH ADVISORIES
---
# Consolidation Audit — both teams, first pass

`team_id`, `commit` and `evidence_package_id` are `null` because this audit covers
two teams, two pinned commits and two evidence packages. Each finding names its own.

New findings from this pass are numbered `C1..Cn` and `CA1..CAn` so they cannot be
confused with the judging stage's `F1..F19` and `A1..A12`, two of which
(judging F1, judging F5) were carried into this stage and are ruled on below.

## Result

**PASS WITH ADVISORIES.** No blocking finding. One major (C1), five minor
(C2-C6), three advisory (CA1-CA3). Both carry-forward obligations from the
judging stage — judging F1 and judging F5 — are **closed**, verified against the
pinned checkout rather than against the report that claims them.

**The `consolidation-audited` gate may be set.** Every finding below is outside
the blocking set defined by D16 (`docs/framework-fix-plan.md:37`, ruled at
`audits/judgments.md:494-505`). C1 is in scope and in stage and is ruled
non-blocking on stated grounds with a one-sentence mechanical repair.

The eight things this gate exists to protect were re-derived here, not accepted:

- **Both score blocks reproduce cell for cell.** Every criterion mean, weight,
  weighted-points value, agreement band, judge score and total was recomputed
  from the eight judgment front matters and the canonical weights in
  `framework/rubrics/submission-evaluation.md`, independently of `atj`. Zero
  differences. `atj score --json` against the committed summaries gives **311
  leaf values, 0 differences** for team-ledger and **318 leaf values, 0
  differences** for team-podcast.
- **team-podcast has no official total anywhere.** `total: null`,
  `display_total: null`, `finalized: false`, `weighted_points: null` for
  `reliability`. 58.25 appears four times, none of them inside the
  `atj:consolidated` block, and all four labelled unofficial and unpublishable.
- **No score moved and no judgment was edited.**
  `git log --stat 92c6687..HEAD -- events/live-trial-2026/judgments/` is
  **empty**. `score_override` is absent, `resolved_score` is `null`, all eight
  `source_scores` sets are intact.
- **No finding in either report originates with the consolidator** on the sample
  taken, and no disagreement was resolved by splitting it.
- **The two ordered corrections are true and are carried accurately.**
- **The `agentic` 2/3/3/3 split is presented as unresolved**, not settled by the
  2.75 mean.
- **Nothing private leaked.** Both reports are `visibility: private`, both return
  CLEAR from `atj validate publication`, `public/` holds only `.gitkeep`.
- **No submission was executed in this round.** No run record was added since
  `92c6687`. `atj sandbox preflight` reports AVAILABLE and was not used.

## Scope and artifacts inspected

- `summaries/team-ledger.md` and `summaries/team-podcast.md` in full, against
  `summaries/team-ledger.json` and `summaries/team-podcast.json`,
  `framework/templates/consolidated-team-report.md`,
  `schemas/consolidated-report.schema.json` and
  `framework/rubrics/panel-consolidation.md` front matter.
- All eight judgments: front-matter identity fields and score blocks parsed
  programmatically; every judge finding code cited in the team-ledger report
  (`judge-backend F1-F11`, `judge-frontend-ux B2-B4, K1, P4, R4`,
  `judge-product-agentic F1-F11`, `judge-security-ops F3, F4, F6, F9-F15`)
  resolved in the named judgment and checked against the subject the
  consolidated report gives it; every quoted sentence in the team-ledger report
  located verbatim in its source judgment.
- The pinned team-podcast checkout at `f3fdd342465fa6bc2a52d226a8613b082ad329e0`
  (`workspaces/live-trial-2026/team-podcast`, git-ignored, `git rev-parse HEAD`
  confirmed) to re-derive the check count, the stage numbering and the
  documentation figures, and the pinned server sources to re-check W1's
  citations.
- `adjudications/team-podcast-reliability-ne.md` in full, including the F16
  amendment disclosure added in the judging repair round.
- Both evidence manifests, for citation resolution: every `ev-ledger-*` (20),
  `ev-podcast-*` (19) and `req-*` (5) id cited in either report resolves in the
  corresponding manifest. `ev-podcast-01` and `ev-podcast-04` are the only
  manifest ids not cited; both are superseded `podcast:2` observations.
- `status.md` in full, against the units it records and the commits behind them.
- `framework/personas.md`, `docs/framework-fix-plan.md` D11/D12/D18, and branch
  `fix/framework-d7-d10-d12` at `bdf369d` for the D12 citation (CA1).

No submission was executed. This pass added no run record and needed no sandbox.

## Deterministic validation results

| Command | Result |
|---|---|
| `python3 -m atj validate reports events/live-trial-2026` | PASS — 19 artifacts, 0 blocking, 0 major, 0 minor, 0 advisory |
| `python3 -m atj score events/live-trial-2026/judgments/team-ledger` | 76.3 of 100, seven criteria `aligned`, no `NE` — unchanged since the panel commit |
| `python3 -m atj score events/live-trial-2026/judgments/team-podcast` | no official total; `reliability` an unresolved `NE`; provisional 58.25 — unchanged |
| `atj score --json` vs both committed summaries | ledger **311 leaves, 0 diffs**; podcast **318 leaves, 0 diffs** |
| Independent recompute from the eight judgment front matters and the canonical weights | every mean, weight, points, range and band identical; ledger sum `305/4 = 76.25`; podcast scored-criteria sum `233/4 = 58.25` |
| `atj:consolidated` block vs `atj score` table, cell by cell | ledger **10 of 10 rows byte-identical**; podcast **9 of 10 byte-identical**, one differing cell (C7/CA2) |
| `git log --stat 92c6687..HEAD -- events/live-trial-2026/judgments/` | **empty** |
| `git log --stat 92c6687..HEAD -- events/live-trial-2026/runs/` | **empty** — no submission executed |
| `python3 -m atj event unit events/live-trial-2026 list` | 6 units, **0 stale** — both consolidation digests still match their inputs |
| `python3 -m atj event status events/live-trial-2026` | blocked on `consolidation-audited = pending`, which is this audit |
| `python3 -m atj validate publication` on both summaries | CLEAR, 0 blocking, both |
| `python3 -m atj release-check` | **PASS**, all nine sections including single-source |
| `python3 -m pytest tests/ -q` | **355 passed, 51 subtests passed**, 0 failures |
| `git worktree list` | one worktree, the repository itself — judging F18 stays closed |
| `python3 -m atj sandbox preflight` | AVAILABLE (podman 6.1.0 rootless), not used |

`release-check` and the test suite are green in the working copy as well as in the
index, which is the condition the judging stage's F18 left open.

## Arithmetic integrity — the check this audit exists for

Neither consolidator had a renderer. `atj consolidate` and `atj render consolidated`
do not exist: `atj render` exposes only the `judgment` subcommand. Both
`atj:consolidated` blocks were therefore filled by hand. I re-verified them two
ways that do not share a failure mode.

**First, against the tool.** `atj score` was re-run over both judgment directories
and its table compared to the committed block line by line. team-ledger: ten rows,
all ten byte-identical. team-podcast: ten rows, nine byte-identical; the only
difference is the Overall status cell, which reads
`**not finalizable — unresolved `NE` on reliability**` in the report where the tool
prints `**not finalized**`. No number differs.

**Second, without the tool.** Weights were parsed straight out of
`framework/rubrics/submission-evaluation.md` (25/15/15/15/10/10/10, sum 100) and
raw scores straight out of the eight judgment front matters, and every criterion
recomputed as `mean(raw) / scale_max * weight` with exact fractions:

| Team | Criterion | Scores | Mean | Weight | Points | Range | Band |
|---|---|---|---:|---:|---:|---:|---|
| ledger | functional | 4,4,4,4 | 4.00 | 25 | 20.00 | 0 | aligned |
| ledger | product | 4,3,4,4 | 3.75 | 15 | 11.25 | 1 | aligned |
| ledger | agentic | 3,3,4,4 | 3.50 | 15 | 10.50 | 1 | aligned |
| ledger | engineering | 4,4,4,4 | 4.00 | 15 | 12.00 | 0 | aligned |
| ledger | reliability | 3,3,3,4 | 3.25 | 10 | 6.50 | 1 | aligned |
| ledger | security | 4,4,4,4 | 4.00 | 10 | 8.00 | 0 | aligned |
| ledger | innovation | 4,4,4,4 | 4.00 | 10 | 8.00 | 0 | aligned |
| podcast | functional | 3,3,3,3 | 3.00 | 25 | 15.00 | 0 | aligned |
| podcast | product | 4,4,4,3 | 3.75 | 15 | 11.25 | 1 | aligned |
| podcast | agentic | 2,3,3,3 | 2.75 | 15 | 8.25 | 1 | aligned |
| podcast | engineering | 4,4,4,3 | 3.75 | 15 | 11.25 | 1 | aligned |
| podcast | reliability | NE ×4 | — | 10 | — | — | not-scored |
| podcast | security | 3,3,3,3 | 3.00 | 10 | 6.00 | 0 | aligned |
| podcast | innovation | 3,4,3,3 | 3.25 | 10 | 6.50 | 1 | aligned |

Exact sums: team-ledger `305/4 = 76.25`, displayed `76.3` under the rubric's own
`rounding: half-up` and `display_decimals: 1`. team-podcast's six scored criteria
sum to `233/4 = 58.25`, which is the provisional figure and not a total. No band
exceeds `aligned_max_range: 1`, so no criterion reaches material or severe
disagreement, and `possible_outliers` is empty on all fourteen criteria.

Every judge score in both blocks matches its judgment's front matter. Both
markdown front matters agree with their JSON on `total`, `display_total`,
`finalized`, `blocked_reasons`, `rubric` and `judge_run_ids`. The team-ledger
report's individual judge totals (75.0, 72.0, 78.0, 80.0) match the JSON
`individuals` block. The confidence distribution quoted in both reports —
including the three claims that could hide an error, `engineering` high for three
of four on podcast, `reliability` high-high-high-medium on ledger, and `product`
high for the judge scoring lowest on ledger — matches the JSON exactly.

**Finalization flags.** team-ledger `finalized: true` with a total in both the
front matter and the JSON. team-podcast `finalized: false`, `total: null`,
`display_total: null`, `weighted_points: null` on `reliability`, `blocked_reasons`
carrying the four-judge `NE` string verbatim from the JSON. `NE` is a zero at no
layer.

The hand transcription is correct. What is wrong is what the team-ledger report
says about how it got there (C1).

## The missing total

team-podcast's report presents no official total and states the absence in its own
first sentence. The `atj:consolidated` block's Overall row carries no number.
58.25 appears exactly four times, all outside the block:

| Line | Context | Labelled |
|---|---|---|
| `:42-46` | executive summary | "not an official total", "must not be published, must not be used for seeding, must not be compared against any other team's total" |
| `:106-107` | below the block | "unofficial, unpublishable, and not a seeding input" |
| `:720-722` | unresolved questions | "not a total and must not reach a bracket, a seed, a team-facing report or a public artifact" |
| `:763` | publication instruction | any derivative "must not contain 58.25" |

The team-ledger report does not mention team-podcast or 58.25 anywhere, so the
provisional figure is not in circulation as a comparison.

The report states the cause in the adjudication's terms, at `:48-63`: the `NE` is
"a limit of the evidence package and of the event's sandbox constraints, not a
defect traced to the submission", the three executions produced three unclassified
outcomes, every traced failure points away from the submission, the one run that
would likely have settled it was an operator action, and "**This is the
framework's and the operator's failure, not the team's, and the event report must
say so in those terms**". Each of those propositions is in
`adjudications/team-podcast-reliability-ne.md:65-89` and `:142-152`. The report
also carries D11 correctly (`:271-276`): it never quotes `atj score`'s "applied
adjudication" line without the unresolved-`NE` line, which is the constraint the
judging audit set.

## Neutrality

**No finding without a source was found in either report.** The sample was not
thin. Every judge finding code cited in the team-ledger report resolves to the
right finding in the right judgment, and the subject matches. In the team-podcast
report, which attributes by evidence id rather than by judge code, I traced W1-W11
and R1-R9 by their distinguishing terms: `prune_missing` (backend, product-agentic,
security-ops), scan-order `rowid` (security-ops), `0.0.0.0` (product-agentic,
security-ops), the all-or-nothing suite and the missing summary line (all four),
no unit tests (backend, product-agentic), `downloadAll` and `timeupdate` and
`aria-live` (frontend-ux), `putAll` ghost rows (backend), `worker.onerror`
(security-ops), `ThreadPoolExecutor` amplification (backend),
`check_same_thread` (backend, product-agentic, security-ops), the 3650-day CA
(security-ops), missing CSP (backend, frontend-ux, security-ops), the committed
dashboard (backend), `NoNewPrivileges` (backend). Every one has a judge behind it.

**No disagreement was resolved by splitting it.** On `agentic` the report refuses
the mean explicitly. On `product` and `engineering` it names persona emphasis and
preserves the minority score. On W1 it preserves a three-way classification split
(two confirmed defect, one risk) rather than picking one. On the team-ledger side,
M1-M7 each record the divergence and state "no judge's score was adjusted"; M5 in
particular keeps three compatible statements about tier-3 test coverage side by
side rather than choosing.

Two attribution claims overstate how many judges stand behind them — C2 and C3
below. Both are overstatements of agreement, not inventions: the underlying
findings exist and belong to real judges. Neither changes a score.

The consolidator's citation work is in one respect better than the judgments it
packages: the team-podcast report cites `server/app.py:64` for the
`prune_missing()` call where two judges cite the enclosing range `43-67`. I
checked the pinned file: line 64 is the call, `server/db.py:94-103` is the bare
`DELETE FROM episodes`, `db.py:25` is the cascade, `db.py:37` the pragma, and
`db.py:13` the `NOT NULL UNIQUE` on `filename`. All correct.

## The ordered corrections — verified true, then verified carried

**Correction 1, the check count (judging F1) — CLOSED.**

I re-derived the claim from the pinned checkout before reading what the report
says about it:

| Check | Command | Result |
|---|---|---|
| Raw grep count | `grep -c "check(" tests/e2e.py` | **43** |
| The 43rd match | `grep -n "def check(" tests/e2e.py` | **line 33**, `def check(ok: bool, label: str, detail: str = "") -> bool:` |
| Call sites | `grep -c "^\s*check(" tests/e2e.py` | **42** |
| Non-definition matches | `grep -n "check("` piped through `grep -v "def check("` | **42** |
| Team claim | `README.md:285`, `DECISIONS.md:9` | "42/42" — consistent with the source |
| Stale figure | `README.md:7` | "34/34" — the only wrong number |

The claim is true in every part. The origin is `ev-podcast-05`
(`evidence/team-podcast/manifest.md:115`), which recorded "43 `check(...)` call
sites (`grep -c "check("` against the file)", and `req-07` at `:102`, which
concluded "neither figure matches". `judge-product-agentic.md:463-467` lists it
under **Confirmed defects** citing "(`ev-podcast-05`, direct file inspection)" —
an attribution the evidence does not support, because the figure came from the
manifest rather than from a count of the calls. `judge-frontend-ux.md:369` and
`judge-security-ops.md:187,323` carried the 43 forward without escalating it.
`judge-backend.md:607-611` caught it independently and recorded the
discriminating counts.

The report's Correction 1 (`:329-353`) carries all four required elements: 42 not
43, the `def check(` match at `tests/e2e.py:33`, the origin in `ev-podcast-05`,
and `judge-product-agentic`'s escalation on an unsupported attribution. It adds
the two things the judging audit required around them — "No score moves" and the
instruction that any team-facing or public artifact must use 42 — and it repeats
the correction in the evidence index at `:772` against `ev-podcast-05` itself.
The evidence-class label "direct file inspection" does not survive anywhere as an
endorsed attribution.

**Correction 2, the section range (judging F5) — CLOSED.** The report quotes the
improvement as "sections 4 and 8 through 11" only to name it as the error, states
the correct range, and uses "Stages 4 and 8 through 13" in its own Untested
concerns at `:559`. Verified against `judge-security-ops.md`: `:460` is inside the
`innovation` section (which begins at `:436`) and says "8 through 11"; `:143`,
`:525` and the confirmed-defects list say "8 through 13". The judgment was not
edited.

**Panel note, the stage count.** The report's claim that the suite prints 13
numbered stages plus an "11b" is true at the pinned commit: headers at lines
54, 90, 98, 140, 171, 181, 202, 214, 225, 238, 258, 337, 379 and "11b." at 305,
exactly the line list the report gives. "Stage 7 of 11" does overstate coverage.

## The `agentic` interpretation split

Correctly handled. The report gives it a dedicated subsection (`:164-209`) and a
Material-disagreements entry (`:618-627`), and in both it states that the
consolidator "does not resolve it, does not treat the mean as a settlement", that
"No score moves", and that "The mean of 2.75 is the arithmetic the policy requires
and is not a panel finding that the submission is deficient on this axis".
Resolution status is recorded as **open**, cause **rubric ambiguity**, referred to
the event director.

The three judge quotes used to establish that all four wanted the panel to settle
it are verbatim: `judge-backend.md:302`, `judge-product-agentic.md:232-237`,
`judge-security-ops.md:229`. The report's observation that the `aligned` band
"understates it" is characterisation, not a new finding — `judge-product-agentic`
wrote that a judge reading the criterion as requiring a demonstrated AI system
"would score it much lower, and that reading is available from the anchors". The
facts underneath are unanimous and the report says so before it says anything
else.

The only defect here is the register pointer for D12 (CA1), not the treatment.

## Findings

| Severity | Rule | Artifact | scope | blocking | Finding | Required repair |
|---|---|---|---|---|---|---|
| major (C1) | `CLAUDE.md`, What is deterministic — "do not present a score as recalculated unless `atj score` produced it"; D18 (`docs/framework-fix-plan.md:39`) | `events/live-trial-2026/summaries/team-ledger.md:69-70` | event | **false** | The score section states the block was "Generated by `atj consolidate` from the canonical rubric and the valid individual judgments. Never transcribed by hand." Neither `atj consolidate` nor `atj render consolidated` exists; `atj render` has only `judgment`. The block was transcribed by hand from `summaries/team-ledger.json`. The sentence is unedited template boilerplate (`framework/templates/consolidated-team-report.md:31`) and it contradicts the same file's own Calculation audit at `:708-712`, which describes the true provenance. **Numbers are unaffected** — the block is byte-identical to `atj score`'s table on all ten rows | Replace the two sentences with the team-podcast report's wording at `:85-88` — transcribed from the named JSON, no arithmetic performed by the consolidator, verified cell by cell — and cite D18. Propose **D19** so the template stops shipping the false sentence |
| minor (C2) | `framework/rubrics/panel-consolidation.md`, Evidence synthesis — "Repeated wording is not independent confirmation"; the report's own rule at `:247-249` | `events/live-trial-2026/summaries/team-ledger.md:430-431` | event | false | "All four judges independently excluded the same class of items: no GUI, no packaging beyond `pyproject.toml`, no telemetry, no multi-user support, no authentication or encryption at rest, no supply-chain pinning…" is not supported. `judge-product-agentic` has no not-counted section at all; "telemetry" appears only in `judge-frontend-ux`, "encryption at rest" and "supply-chain" only in `judge-security-ops`. Three judges wrote such a section (`judge-backend:548`, `judge-frontend-ux:542`, `judge-security-ops:347`) | Name the three judges who wrote a not-counted section, or attribute item by item. Do not claim four-way independent exclusion of items three judges never mention |
| minor (C3) | Same rule; the report's own ranking rationale | `events/live-trial-2026/summaries/team-podcast.md:658` | event | false | "Three of the four judges named the first item as the single most valuable change." Two did, in their dedicated sections: `judge-backend.md:694-701` and `judge-security-ops.md:534-545`. `judge-product-agentic.md:498-506` names the e2e fail-soft change, which this report ranks third, and names the prune guard only as his `engineering` improvement at `:294`. `judge-frontend-ux.md:596` names the `timeupdate` decoupling, ranked fourth here. The ranking itself is sound; the count is wrong | "Two judges named it as their single most valuable change; a third named it as his highest-value `engineering` fix." Leave the order alone |
| minor (C4) | `events/live-trial-2026/status.md:165-168`, the log's own provenance rule; judging F15 and A7, same class | both `summaries/*.md` front matter; `status.md:50-65` | event | false | Both reports carry `started_at: "2026-09-17T22:30:00Z"` and `completed_at: "2026-09-17T22:30:00Z"`. The commit that recorded them, `1ece869`, is at `22:00:01Z` — the artifacts claim to have been completed 30 minutes after the commit containing them, and 21 minutes after this audit began at `22:08:40Z`. The ledger's own unit rows record `completed_at: "2026-09-17T22:00:01Z"` for both consolidation units, contradicting the reports. `started_at == completed_at` implies a zero-length run. No code reads either field for advancement | Restamp both to the real run window, ending no later than `22:00:01Z`, with `started_at` before `completed_at`; or restamp to the commit time and say so |
| minor (C5) | The activity log's per-stage row convention, established by evidence-stage F11 and judging F11 | `events/live-trial-2026/status.md:80,91,92,107-163` | event | false | The consolidation stage produced two units and two reports and the activity log has **no row for any of it**; the newest rows are the `22:19:00Z` judging rows. The team-progress table still reads "scored 76.3, panel report pending" for team-ledger and names no report for team-podcast, both stale as of `1ece869`. The stage-gates checklist still shows "[ ] All initial judgments audited" while the front matter records `judgments-audited: passed` — the gate command writes front matter only, so the box is hand-maintained and was missed | Add the consolidation rows and this audit's row, refresh both team-progress cells, tick the judging box. The log rows take `1ece869`'s commit time `22:00:01Z` and this audit's own `completed_at` respectively |
| minor (C6, judging F10 recurred) | `schemas/status.schema.json` requires `last_updated`; every `atj event` writer sets it from `versions.now()` | `events/live-trial-2026/status.md:4` | event | false | `last_updated: "2026-09-17T22:00:01Z"` predates the newest activity rows at `22:19:00Z`. Same mechanism as judging F10: rows are hand-added above a machine-written field. Mechanically self-closing | Add the C5 rows **first**, then run `atj event gate`, then confirm `last_updated` exceeds the newest row. The gate command must be the last write to the ledger |
| minor (C7) | The `atj:consolidated` region is generator-owned (`framework/templates/consolidated-team-report.md:33-35`) | `events/live-trial-2026/summaries/team-podcast.md:100` | event | false | The Overall status cell reads `not finalizable — unresolved `NE` on reliability` where `atj score` prints `not finalized`. It is the single cell in either block that is not byte-identical to generator output. It carries no number, it is more informative than the tool's text, and it cannot currently be produced by any tool — but it is a hand edit inside a region a template says a tool owns | Leave the text, or align it with the tool. Whichever is chosen must be the renderer's output when D18 is fixed, so that regenerating the block is a no-op |
| closed (judging F1) | `audits/judgments.md:120-128` | `summaries/team-podcast.md:329-353` | event | n/a | Closed. Claim re-derived from the pinned checkout and every element of the ordered correction is present and accurate | None |
| closed (judging F5) | `audits/judgments.md:137-142` | `summaries/team-podcast.md:356-362,559` | event | n/a | Closed. "sections 4 and 8 through 13" used in the report's own voice; the judgment was not edited | None |

## Advisories

**CA1 — the D12 citation does not resolve on this branch.** The team-podcast
report logs the `agentic` rubric gap as "framework defect **D12**" at `:76`,
`:204`, `:626` and `:728-739`. On `feature/first-live-event` the defect table in
`docs/framework-fix-plan.md` runs D11 → D13 with a numbering note at `:198-200`
saying D12 is taken by this exact gap on branch `fix/framework-d7-d10-d12`. I
checked that branch: `docs/framework-fix-plan.md:195` does carry a D12 row,
marked **"proposed, not landed"**, plus a full section at `:275`. So the judging
audit's F17 was indeed wrong to call the reference fabricated, and status.md's
rebuttal at `:162` is right. The reference is nonetheless to a defect that exists
only on an unmerged branch, and a reader of the event's own branch cannot resolve
it. Framework scope, non-blocking. Land D12 or qualify the citation in the next
report that uses it.

**CA2 — both reports instruct the reader to run a command that does not exist.**
`summaries/team-podcast.md:88` says the block "must be regenerated by
`atj render consolidated` before `atj validate` runs against this file", and
`:821-823` repeats it; `summaries/team-ledger.md:710-712` says the block "must be
regenerated by the renderer before this report is validated". `atj validate
reports` has already run and passed over 19 artifacts without it, so the stated
precondition is both unexecutable and already bypassed. This is D18's downstream
effect, not a new defect. The ledger report's unchecked box at `:723-725`
("Publication gate — not run") is now stale in the other direction: `atj validate
publication` returns CLEAR for both reports.

**CA3 — carried forward from the judging stage, unchanged.** A2 (run records
embed host paths; publication remains per artifact). A5 recurs one artifact type
later: both summaries are `approval_state: draft` and `validation_state:
unvalidated` while both consolidation units are `complete` and `atj validate
reports` passes them. A9 remains open: `ev-podcast-12` is cited in the
adjudication's Disputed-claims table at `:50` and is still absent from its
Evidence reviewed section at `:55-63`; the id resolves in the manifest, so this is
completeness. A10 is still a no-op (`status.md.bak` ignored). A12's lesson held
again here: `status.md:162` and the `1ece869` commit message both assert the two
blocks were "verified cell by cell… zero mismatches", and that assertion is true,
but it was re-derived here rather than accepted, and one cell (C7) does differ
from generator output.

Two further observations, neither a finding. `judge-security-ops.md:75`
(team-ledger) declares "Finding codes below are mine (F1..F12)" and then uses F13,
F14 and F15 — a judging-stage artifact defect nobody has recorded; it is not
editable now and no consolidated citation is wrong because of it. And
`workspaces/live-trial-2026/` is git-ignored, so the checkout I used to re-derive
the 42-check count is reproducible only while that directory survives; the
counts themselves are restated here so the result outlives it.

## Proposed framework defect

**D19 — `framework/templates/consolidated-team-report.md:31` ships a provenance
sentence that is false for every report produced under it.** The template says
the score block is "Generated by `atj consolidate`… Never transcribed by hand",
and D18 records that `atj consolidate` does not exist. Any consolidator who
follows the template faithfully publishes a false statement about how the
official numbers reached the artifact; the one who noticed rewrote it, and the
one who did not is C1. Until the renderer exists, the template must say the block
is transcribed from the `atj score` JSON and verified cell by cell. Tier 1 — it
produced a defect in this event's first consolidated report. Pairs with D18.

## Why this passes

Measured against the D16 ruling at `audits/judgments.md:494-505`, which this
audit was instructed to apply:

**Must block a stage gate.** A finding inside `events/live-trial-2026/`, inside
the consolidation stage, that is missing required evidence, arithmetic that does
not reproduce, a version or identity mismatch, unresolved severe disagreement
handled wrongly, a submission executed without isolation, private information in
public output, a score moved without authority, or a judgment edited by anyone
but its judge. **Zero of those are present, and each was re-derived rather than
accepted.** Arithmetic: two independent recomputations, 629 leaf values, one
deviation and it is a text cell. Evidence: 44 cited ids, all resolve. Identity:
all four team-ledger judgments carry `framework_commit: 0677b6cf…`, all four
team-podcast judgments `3da42c51…`, the manifest `152dd2c1…` and both reports
`d11a9706…`, which is exactly what both Calculation audits claim; `rubric`,
`commit`, `evidence_package_id`, `consolidation_policy: panel-consolidation@1.0.0`
and `persona: panel-consolidator@1.0.0` agree across every artifact and resolve in
`framework/personas.md`. Nothing in `framework/`, `atj/`, `schemas/` or `VERSION`
changed between `d11a970` and `HEAD`, so the reports' `framework_commit` is
accurate for everything the consolidation reads. Disagreement: no criterion
exceeds range 1.0 against `aligned_max_range: 1`; the one real split is recorded
as unresolved and the mean is explicitly refused as a settlement. Execution: no
run record added. Privacy: both private, both CLEAR, `public/` holds `.gitkeep`.
Score movement: none; `git log` over `judgments/` since `92c6687` is empty.

**Must not block a stage gate.** C1 is in scope and in stage, and I weighed it
hardest, because a false sentence about the provenance of official numbers is the
kind of defect this framework exists to catch. It does not block for three
reasons I checked rather than assumed. The numbers it describes are correct and
byte-identical to the generator's own table, so no reader is misled about a value.
The same artifact states the true provenance two screens later, so the record
contains its own correction. And the sentence is the template's, not the
consolidator's: the framework put it there and D18 already records why (D19
above). The repair is two sentences and its result is verifiable by reading them,
not a judgment that needs a second auditor. C2, C3 and C7 are precision defects
where the underlying facts are right and no score depends on them. C4, C5 and C6
are ledger and timestamp fields that no advancement path reads — `can_advance`
(`atj/event.py:421-426`) branches on `audit_result` only. CA1 is a framework
register pointer, outside `events/`.

An event that cannot clear a gate because each pass finds new prose drift is the
failure D16 names. This stage's substance is clean, and it is cleaner than the
stage before it: no score moved, no judgment was touched, both corrections the
judging audit ordered were carried accurately, and the hardest number in the
event — the total that must not exist — does not exist anywhere in the artifact
that would have been the easiest place to invent it.

**Three mechanical actions before the gate command runs.** None touches a score, a
judgment, an evidence package or a number:

1. **C1** — replace the false provenance sentence in
   `summaries/team-ledger.md:69-70`. Confirm `python3 -m atj validate reports
   events/live-trial-2026` still reports 19 artifacts, 0 findings, and that the
   `atj:consolidated` block still matches `atj score` on all ten rows.
2. **C2, C3, C4, C7** — the four precision repairs above, in one edit.
3. **C5 then C6** — add the consolidation and audit rows and refresh the progress
   table and the checklist, **then** run `atj event gate`, then confirm
   `last_updated` exceeds the newest activity row. The gate command must be the
   last write to the ledger.

## Completion gate

- [x] **No blocking findings** — no missing required evidence, no invalid
      arithmetic, no version or identity mismatch, no unresolved severe
      disagreement, no submission executed in this round, nothing private in
      `public/`, which holds only `.gitkeep`. Both summaries and this audit clear
      `atj validate publication` as private artifacts
- [x] **No major findings in scope that block** — one major, C1, in scope and in
      stage, ruled non-blocking on stated grounds with a two-sentence required
      repair. Its numbers are correct and byte-identical to generator output, the
      same artifact states the true provenance, and the false sentence is the
      template's (D18, D19)
- [x] **Calculations valid** — both blocks reproduce twice over: `atj score --json`
      against the committed summaries gives 311 and 318 leaves with zero
      differences, and an independent recompute from the eight judgment front
      matters and the canonical weights reproduces every mean, weight, points,
      range and band. Exact sums `305/4 = 76.25` (displayed 76.3, half-up, 1
      decimal) and `233/4 = 58.25` provisional. `total: null`, `display_total:
      null`, `finalized: false` and `weighted_points: null` for team-podcast's
      `reliability`; 58.25 is labelled unofficial at all four occurrences and
      appears nowhere in the score block; `NE` is a zero at no layer; no score
      moved and no judgment was edited
- [x] **Evidence references resolve** — `atj validate reports` PASS over 19
      artifacts with zero problems; all 20 `ev-ledger-*`, 19 `ev-podcast-*` and 5
      `req-*` ids cited in the two reports resolve in the corresponding manifest;
      every judge finding code cited in the team-ledger report resolves to the
      right finding in the right judgment; the check-count and stage-count claims
      were re-derived from the pinned checkout. `ev-podcast-12` remains cited but
      unlisted in the adjudication (A9), which is completeness
- [x] **Version and identity checks pass** — `rubric: submission-evaluation@1.0.0`,
      `consolidation_policy: panel-consolidation@1.0.0` and `persona:
      panel-consolidator@1.0.0` resolve and agree across all artifacts;
      `framework_commit` values are exactly what both Calculation audits state;
      nothing in `framework/`, `atj/`, `schemas/` or `VERSION` changed between the
      reports' `framework_commit` and `HEAD`; `release-check` PASS on all nine
      sections and 355 tests pass with zero failures in the working copy; 6 units,
      0 stale
- [x] **Privacy boundary passes** — both reports are `visibility: private`, both
      return CLEAR from `atj validate publication`, `public/` holds only
      `.gitkeep`, no host path, address or personal identifier appears in either
      report, and the one submission artifact containing unpublished titles is
      cited by path without reproducing any of them

**PASS WITH ADVISORIES.**

The `consolidation-audited` gate may be set once the three mechanical actions
above are done, in that order:

```
python3 -m atj event gate events/live-trial-2026 consolidation-audited passed \
  --audit audits/consolidation.md
```

**Carry into the bracket and matchup stages.** team-podcast has no official total
and must not acquire one: 58.25 is not a score, not a ranking input and not a bye
seed, and any team-facing or public derivative must use 42 for the check count,
must not contain 58.25, and must state the reason for the missing total in the
adjudication's terms. `reliability`'s comparison value is the matchup panel's
finding to make on the common evidence, not something this stage imposed. The
`agentic` interpretation question is open and referred to the event director; it
is not settled by 2.75. `atj score`'s "applied adjudication" line must never be
quoted without the "unresolved NE" line until D11 is fixed.

**Carry into the framework backlog.** D19 above, alongside D18. A9 and A5 remain
open advisories.
