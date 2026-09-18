---
event_id: live-trial-2026
audit_scope: tournament stage, the order-balanced head-to-head mu:live-trial-2026:final:01 and its advance, first pass
audit_id: tournament
team_id: null
match_id: mu:live-trial-2026:final:01
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.0.0
persona: judging-auditor@1.0.0
framework_commit: 96e3f32bda27a489ab09778ba43aec20f85d7119
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-17T23:50:00Z"
completed_at: "2026-09-18T00:40:00Z"
visibility: private
approval_state: approved
validation_state: valid
result: PASS WITH ADVISORIES
---

# Tournament Audit — the final matchup and the advance, first pass

`team_id`, `commit` and `evidence_package_id` are `null` because the matchup is a
two-team artifact covering two pinned commits and two evidence packages, all four
recorded in `matchups/mu-final-01.md` front matter. `match_id` is set, because unlike
the bracket this audit has exactly one match in scope.

Findings from this pass are numbered `T1..Tn` and `TA1..TAn` so they cannot be
confused with the bracket stage's `B1..B6` / `BA1..BA3`, the consolidation stage's
`C1..C7` / `CA1..CA3`, or the judging stage's `F1..F19` / `A1..A12`.

**This audit was taken against `96e3f32`.** `HEAD` moved twice while it ran, to
`329d8d2` and `a8c0cf8`. Both are dossier-stage commits, they add two files and
nothing else, and `git diff 96e3f32..a8c0cf8` across `matchups/`, `matchup-passes/`,
`bracket.json`, `bracket.md`, `status.md`, `summaries/` and `judgments/` is **empty**.
Every finding below therefore stands unchanged at `a8c0cf8`. That the commits exist at
all is **TA4**.

## Result

**PASS WITH ADVISORIES.** No blocking finding. Three major (T1-T3), three minor
(T4-T6), four advisory (TA1-TA4). TA4 is a process finding against the *next* stage,
raised here because it was discovered here.

**The `tournament-audited` gate may be set.** Every finding below falls outside the
blocking set defined by D16 (`docs/framework-fix-plan.md:37`, ruled at
`audits/judgments.md:494-505`, applied at `audits/consolidation.md:36-39` and
`audits/bracket.md`). Two findings are inside `events/live-trial-2026/` and inside the
tournament stage — T1 and T2 — and neither touches any of the eight blocking triggers,
for reasons given in full at each.

The eight things this gate exists to protect were re-derived here, not accepted:

- **The resolution reproduces exactly.** An independent `atj matchup` run, built from
  each judge's raw values read out of that judge's own report, produced a result
  **byte-identical to the committed `matchups/mu-final-01.json` on every key**. Zero
  keys added, zero missing, zero differing.
- **Both presentation orders were judged, and neither pass saw the other.** Every
  substantive phrase the two passes share traces to a document both were entitled to
  read. Nothing is shared that does not have an upstream source.
- **The B-first negation was performed by the tool.** Confirmed from the raw values,
  which are stored unnegated in the artifact.
- **No total selected anything.** Confirmed in the tool (no score is an input to
  `atj matchup`) and in both passes' own text.
- **The `reliability` zero is each judge's own finding on the common evidence**, taken
  from the rubric's own definition of the value, and is not charged to team-podcast by
  either pass.
- **`bracket.json` and `bracket.md` agree and no match is pending.**
- **`public/` is empty** and nothing under `judgments/`, `summaries/` or
  `adjudications/` has moved since the consolidation gate.
- **`atj release-check` PASS, `atj validate reports` PASS, 355 tests + 51 subtests
  pass.**

## Scope and artifacts inspected

| Artifact | Read | Re-derived |
|---|---|---|
| `matchups/mu-final-01.json` | yes | yes, full-key diff against a fresh calculation |
| `matchups/mu-final-01.md` | yes, all 129 lines | every figure reconciled to the JSON |
| `matchup-passes/mu-final-01-pass-a-first.md` | yes, all 433 lines | completeness and coherence, see T3 and check 7 |
| `matchup-passes/mu-final-01-pass-b-first.md` | yes, all 403 lines | orientation re-resolved two ways, see T4 |
| `bracket.json`, `bracket.md` | yes | `atj bracket verify`, pending-match scan, diff since the gate |
| `status.md` | yes | gate states, the four tournament activity rows |
| `summaries/team-ledger.md`, `summaries/team-podcast.md` | yes, for provenance of shared phrasing | phrase-origin trace |
| `adjudications/team-podcast-reliability-ne.md` | yes | the accepted `NE` and its stated cause |
| `framework/rubrics/head-to-head.md` | yes | band, values, tie-break order |
| `atj/matchup.py`, `atj/reports.py`, `atj/event.py`, `atj/bracket.py`, `schemas/matchup.schema.json` | yes | the D22 ruling |
| `workspaces/live-trial-2026/staging/matchup/` | yes | staged-versus-promoted diff, see T3 |

## Deterministic validation results

| Command | Result |
|---|---|
| `python3 -m pytest tests/ -q` | 355 passed, 51 subtests passed |
| `python3 -m atj release-check` | PASS, all nine checks |
| `python3 -m atj validate reports events/live-trial-2026` | PASS — 22 artifacts, 0 blocking, 0 major, 0 minor, 0 advisory |
| `python3 -m atj matchup --event-dir events/live-trial-2026` on independently transcribed values | combined margin **35.0**, winner **team-ledger**, outcome **confirmed**, `order_disagreement: false`, `criterion_order_disagreements: []`, `adjudication_reasons: []`, band 5.0 |
| Full-key diff, my result versus `matchups/mu-final-01.json` | **identical** — no key only in mine, none only in the committed file, none differing |
| `python3 -m atj bracket verify events/live-trial-2026/bracket.json` | PASS (structure) |
| `python3 -m atj validate publication matchups/mu-final-01.md --event-dir events/live-trial-2026` | CLEAR, 0 blocking |
| `python3 -m atj event status events/live-trial-2026` | stage `tournament`, next action `complete-tournament`, blocked on this gate |
| `python3 -m atj event validate events/live-trial-2026` | FAIL, one problem — D20 only, see TA2 |

## Check 1 — reproduce the resolution

I transcribed each judge's raw comparison values from that judge's own report, not
from `mu-final-01.json`:

- a-first, from the `## Comparison values` fenced block at
  `matchup-passes/mu-final-01-pass-a-first.md:120-122`, cross-checked against its own
  front matter at `:24-31`: `{functional 1, product 0, agentic 1, engineering 1,
  reliability 0, security 1, innovation 0}`, `presented_first: team-ledger`.
- b-first, from its front matter at `matchup-passes/mu-final-01-pass-b-first.md:27`:
  `{functional -1, product 0, agentic -1, engineering -1, reliability 0, security -1,
  innovation -1}`, `presented_first: team-podcast`.

Fed to `atj matchup` with `--event-dir events/live-trial-2026`, the result is:

- a-first margin **+32.50**, picks team-ledger
- b-first margin normalized **+37.50**, picks team-ledger
- combined **+35.00**, `outcome: confirmed`, `winner: team-ledger`
- `order_disagreement: false`, `criterion_order_disagreements: []`,
  `adjudication_reasons: []`, `close_call_band: 5.0`

A full-key comparison of my result against the committed `matchups/mu-final-01.json`
found **no differing key, no missing key and no extra key.** The committed artifact is
what the tool produces from the judges' own values.

**The negation was the tool's.** `matchups/mu-final-01.json` stores b-first's
`raw_comparisons` as the five negatives the judge actually returned and
`normalized_comparisons` as the five positives, side by side in the same object. That
shape is only produced by `atj/matchup.py:152-168`, which calls `normalize_pass` at
`:42-70`; the sign is derived at `:55` from `presented_first` against `team_a`, and the
judge's values are stored unaltered at `:163`. No judge or operator could have produced
that pairing by hand without also hand-writing the raw block, and the raw block matches
the b-first report's front matter exactly. Neither pass report contains a margin, a
combined margin, a winner or a normalized value anywhere — both say so explicitly and
both are correct on inspection.

**The band was not narrowed.** `framework/rubrics/head-to-head.md` front matter declares
`close_call_band: 5`; the matchup used `5.0`. `atj/matchup.py:135-142` raises on any
value below the rubric floor, so a narrowed band was not reachable. 35.00 is seven times
the band, and `abs(combined) > band` at `:219` is satisfied by a wide margin.

**Weights and values are the canonical ones.** `criterion_margin` at
`atj/matchup.py:73-78` is `value / max * weight`, matching the rubric's stated
`criterion_margin = comparison_value / 2 * criterion_weight`. Every per-criterion figure
in `mu-final-01.md`'s table matches `mu-final-01.json` and both match my recomputation.

## Check 2 — independence

**No contamination found.** Four independent lines of evidence:

1. **Phrase-origin trace.** I extracted every 8-, 10- and 12-word shared n-gram between
   the two pass reports and subtracted the n-grams of every document both judges were
   entitled to read (`summaries/`, `judgments/`, `evidence/`, `adjudications/`,
   `submissions/`). Everything that survived was either front-matter and template
   boilerplate — identical timestamps, model ids, framework commit, the template's own
   table header and its "not computed here" phrasing — or resolved to an upstream source
   once whitespace and code-span differences were normalized. The two strongest
   candidates both resolve cleanly:
   - "classes it a risk because it was ... which is what all three descriptions support"
     is a paraphrase of `summaries/team-podcast.md:437-439`, which reads "classes the
     same finding a risk because it was never executed. The panel records it as
     confirmed-by-source-read with the execution status stated, which is what all three
     descriptions actually support."
   - "a scan-order rowid used as a durable cross-device key when a stable natural key
     already exists" is `summaries/team-podcast.md:440-447` plus
     `judgments/team-podcast/judge-backend.md:602-604`, near-verbatim.

   Both judges read the same consolidated report. Convergence on its wording is expected
   and is the opposite of cross-exposure.
2. **The corrections both passes carry are inherited, not invented.** The check-count
   correction (43 to 42) and the stage-count correction (11 to 13 plus an "11b") both
   originate at `summaries/team-podcast.md:329-331` and `:367-371`, and the stage-count
   phrasing traces further back to `judgments/team-podcast/judge-product-agentic.md:69`.
   Neither pass is the source of either correction.
3. **They disagree.** A contaminated pair converges. These two differ on `innovation`
   (a-first `0`, b-first `-1`, i.e. `+1` normalized), on how many criteria they call
   meaningful advantages (four versus five), and on a point of fact (T5).
4. **Structure differs.** b-first opens with an `## Orientation` section the template
   does not have and carries a six-item audit checklist; a-first has no Orientation
   section, adds a `## Comparison values` section instead, and carries the template's
   four items. Two judges working from one shared draft would not diverge this way.

**Staging.** Both passes are present at
`workspaces/live-trial-2026/staging/matchup/pass-a-first.md` and `pass-b-first.md`,
consistent with the declared stage-then-promote procedure. The b-first staged copy is
byte-identical to the promoted artifact. The a-first staged copy is not — see **T3**.

## Check 3 — initial totals not used

**Neither pass selected on totals, and the tool cannot.** No score of any kind is an
input to `atj matchup`: `calculate()` at `atj/matchup.py:111-242` takes team ids, the two
passes, a band and the two rubrics, and nothing else. There is no code path from a
consolidated total to a comparison value or a margin.

Both passes state the prohibition and apply it.
`matchup-passes/mu-final-01-pass-a-first.md:63-69` quotes `head-to-head.md`'s "Do not
merely select the team with the higher initial total" and records that the two figures
"are not commensurable and were not compared."
`matchup-passes/mu-final-01-pass-b-first.md:89-96` does the same independently. Both then
compare the seven criteria directly on common evidence, and every nonzero value is
supported by evidence ids and file-and-line citations, not by a score.

**Correction to the premise of this check.** The figure 58.25 does **not** appear
nowhere in the tournament stage. It appears twice, in both pass reports — see **T2**.
It appears in neither `matchups/mu-final-01.json` nor `matchups/mu-final-01.md`.

## Check 4 — the `reliability` zero

**Each pass reached `0` as its own finding, on the rubric's own definition, and neither
charged the `NE` to team-podcast.**

`framework/rubrics/head-to-head.md:18` defines the value `0` as "Substantially equal
**or** insufficient comparative evidence". Both passes invoke the second limb by name,
which is the correct reading for this pairing.

- a-first, `:397-415`: "`reliability` is recorded as `0` as my own finding on the common
  evidence, for the reason the value is defined: there is insufficient comparative
  evidence to establish a difference ... This is explicitly **not** a deficiency charged
  to team-podcast." It then argues the merits both ways on common evidence —
  team-ledger's untested `dispute.py`, no test importing `fin.cli`, the uncovered
  `AMBIGUOUS` branch, `cmd_ingest` returning 0 after `_revalidate` reports problems,
  against team-podcast's `/healthz`, `Restart=on-failure`, `storage.reconcile()` and
  `flushQueue()`, against its missing `worker.onerror` — and concludes "Neither side is
  clearly ahead even before the `NE` is taken into account."
- b-first, `:354-381`: "I reached `0` on the common evidence, and it is my finding, not
  an inheritance ... Any nonzero value I assigned would convert that unresolved
  uncertainty into a comparative finding ... **It is explicitly not a finding against
  team-podcast**, and nothing in either package shows team-podcast's suite failing for a
  reason traced to its own code."

The two arrive by different routes. a-first leads with the asymmetry argument and lists
team-ledger's own coverage gaps; b-first leads with team-podcast's positive reliability
properties (`server/app.py:210-213`, `deploy/podcast-listener.service:27-31`,
`web/js/storage.js:117-128`, `tests/e2e.py:57-67`) before its gaps, then does the same
for team-ledger. Same disposition, independently reasoned, different evidence emphasis.

Both also state the downstream consequence without acting on it: with `reliability` at
`0` it contributes no tie-break signal, which
`adjudications/team-podcast-reliability-ne.md` anticipated. Neither applied a tie-break,
correctly, because the margin is far outside the band.

## Check 5 — bracket advance

**Recorded, consistent, and nothing is pending.**

- `git diff aa3b62f..HEAD -- events/live-trial-2026/bracket.json` is a **one-line**
  change: `"winner": null` becomes `"winner": "team-ledger"`. That is exactly and only
  the field `atj/bracket.py:823` writes, with the guards at `:808-822` — match must
  exist, winner must be an entrant, an existing different winner refuses rather than
  overwrites. No other byte of the bracket moved, so the draw, the seed, the input
  digest and the constraint audit are the audited ones.
- `bracket.md` agrees with `bracket.json`: the added block at `:56-59` names
  `team-ledger` advancing from `mu:live-trial-2026:final:01`, combined margin +35.00,
  outcome `confirmed`, no adjudication. All three figures reconcile to
  `mu-final-01.json`. See **T6** on how that block got there.
- **No further match is pending.** The bracket has one round and one match, it is not a
  bye, and it has a winner. A programmatic scan for matches lacking a winner returns
  empty. `atj bracket verify` passes.
- The advance was taken from the private matchup report, per `bracket.md:57` and
  `status.md`'s `23:40:00Z` row. I cannot prove from the repository which process wrote
  the field, but the diff is exactly what the tool writes and nothing more, and the
  winner it records is the one the tool independently derives.

## Check 6 — ruling on D22

**The defect is real and is stated accurately in `docs/framework-fix-plan.md:288-305`.**
I confirmed both halves:

- `schemas/matchup.schema.json` requires `passes` to carry both `a_first` and `b_first`,
  and each pass requires `comparisons` with `"minProperties": 1`. A single
  order-balanced pass report — whose empty opposite block *is* the evidence of
  independence — therefore cannot validate.
- `matchup-passes` is in no `EVENT_SUBDIRS` list (`atj/event.py:41-44`) and in no
  `ARTIFACT_KINDS` map (`atj/reports.py:26-37`), so the walk at `atj/reports.py:322-326`
  never reaches it.

**Does anything validate their contents? No.** `atj validate reports` reported exactly
**22 artifacts**, which is precisely the count of `.md` files in the ten covered
subdirectories — 2 evidence manifests, 8 judgments, 2 summaries, 1 matchup, 1
adjudication, 6 audits, 2 submissions. The two pass reports are not among them. No
schema check, no template conformance check, no placeholder scan, no evidence-reference
resolution, and no automatic privacy scan touches those two files.

**Ruling: storing them there is acceptable for this event, and only because four things
are true.** I checked each rather than assuming it.

1. **The alternative was worse.** The two in-schema repairs are to fabricate a non-empty
   opposite block, which falsifies the independence record the empty block exists to
   prove, or to discard the judges' reasoning entirely and keep only the JSON input. The
   first is an evidence offence. The second destroys the only written record of the
   comparative evidence.
2. **It is declared, not hidden.** The directory is committed and tracked, named from
   `matchups/mu-final-01.md:31-32`, named in the `23:35:00Z` and `23:40:00Z` activity
   rows, and logged as framework defect D22 with the reason stated as "purely so the
   event would validate." Nothing about it is concealed.
3. **The privacy gate fails closed on it, which I verified rather than assumed.**
   `python3 -m atj validate publication events/live-trial-2026/matchup-passes/mu-final-01-pass-a-first.md --event-dir events/live-trial-2026`
   returns `BLOCKING [location-unknown] ... cannot determine the required visibility for
   this artifact`. Nothing in that directory can be cleared for disclosure. That is the
   behaviour I would want, and it is why T2 is not a privacy breach.
4. **Nothing in those files was relied on unchecked.** Every figure that mattered was
   re-derived here from the tool, and I resolved all 23 evidence ids in the a-first
   report's recovered tail and every evidence id in the b-first report against the two
   manifests by hand. All resolve.

**What is not acceptable is leaving it here.** The gap is coverage, and it compounds:
the one directory holding the judges' comparative reasoning is the one directory with no
automated check of any kind, which is how T2, T4 and T5 all survived to this audit. This
is **T1**, a major finding with a required repair, and the repair belongs in `atj/` and
`schemas/`, not in the event. D22 is already Tier 2 in the fix plan; this audit adds the
publication-gate finding to it, which the fix plan does not currently record, and it
raises the practical urgency: a two-team event has one matchup and two unvalidated
files, an eight-team event has seven and fourteen.

## Check 7 — the a-first extraction

**The promoted `matchup-passes/mu-final-01-pass-a-first.md` is complete and internally
coherent.** Six independent tests, all passing:

1. **The truncated copy still exists, and the promoted file is a strict extension of
   it.** `workspaces/live-trial-2026/staging/matchup/pass-a-first.md` is the first,
   118-line extraction, cut at the `## Comparison values` heading — the line immediately
   before the nested ` ```json ` fence, exactly as described. `diff` between it and the
   promoted file reports **`118a119,433` and nothing else**: a pure append, zero modified
   lines and zero deleted lines across the first 118 lines. The re-extraction recovered
   the tail without disturbing the head. This is the strongest available evidence that
   the depth-aware scan did not rewrite anything.
2. **Front matter is complete and parses.** Lines 1-43, all template fields present,
   `presentation_order: a-first`, `visibility: private`, and a `passes` block whose
   `b_first.comparisons` is `{}` — the independence marker.
3. **All template sections present, in template order.**
   `framework/templates/matchup-report.md` declares seven `##` sections under the H1;
   the report has all seven — Eligibility and common evidence `:53`, Order-balanced
   results `:91`, Margin and outcome `:103`, Decisive evidence `:126`, Conflicting
   evidence `:342`, Tie-break or adjudication `:378`, Audit `:417` — plus one addition,
   `## Comparison values` at `:118`. Nothing from the template is missing.
4. **The Comparison values block is intact and agrees with everything else.** The fence
   at `:120-122` holds
   `{"functional": 1, "product": 0, "agentic": 1, "engineering": 1, "reliability": 0, "security": 1, "innovation": 0}`,
   which matches the report's own front matter at `:24-31` field for field, and matches
   `matchups/mu-final-01.json` `passes.a_first.raw_comparisons` field for field. The file
   contains exactly two ` ``` ` markers, so the fence is balanced and no fence was
   swallowed.
5. **The audit checklist is complete.** All four of the template's items are present and
   all four are checked, `:419-433`. The file ends mid-nowhere in no sense: the last line
   is a complete sentence with a terminating period and a trailing newline.
6. **Internally coherent.** The report declares four nonzero values and the Decisive
   evidence section carries exactly four `###` criterion blocks — functional `:131`,
   agentic `:191`, engineering `:243`, security `:290` — one per nonzero value, each
   headed with the value it is defending. "No criterion reached `2` or `-2`" at `:128` is
   true of its own values. All 23 evidence ids cited in the recovered tail (lines
   119-433) resolve to `evidence/team-ledger/manifest.md` or
   `evidence/team-podcast/manifest.md`.

**Its stated values match `mu-final-01.json`.** Three places agree: the report's front
matter, its Comparison values fence, and the JSON's `raw_comparisons`. And the Margin
and outcome section at `:105-116` computes nothing, names no winner and no margin, which
is what the pass was required to do.

The residual risk from the recovery is **T3**, and it is a record-keeping problem in
`workspaces/`, not a defect in the promoted artifact.

## Check 8 — public boundary and artifact stability

**`public/` is empty.** It contains `.gitkeep` and nothing else, one byte.
`atj validate reports` found zero `public` artifacts and zero findings. No ceremony view
has been rendered. No dossier exists.

**No judgment has been touched.** `git log 92c6687..HEAD -- events/live-trial-2026/judgments/`
is empty, as the bracket audit also found.

**Correction to the premise, TA3.** The consolidated reports were not merely untouched
since `92c6687` — they did not exist at `92c6687`. `summaries/team-ledger.md` and
`summaries/team-podcast.md` were created at `1ece869`, and `summaries/team-podcast.json`
was edited at `aa564f0` closing C1-C5/C7/CA1. Both commits are inside the consolidation
stage and inside the scope the consolidation audit already passed. The claim that holds
exactly is the stronger one for this gate: **since the consolidation gate passed at
`7591d48`, `git diff` across `judgments/`, `summaries/` and `adjudications/` is empty.**
Nothing the tournament stage consumed has moved while the tournament stage ran.

**Everything that changed since the bracket gate is accounted for.**
`git diff aa3b62f..HEAD` touches eight files: the two matchup artifacts and two pass
reports (new), `bracket.json` (one line, check 5), `bracket.md` (+4 lines, T6),
`status.md` (stage plus four activity rows), and `docs/framework-fix-plan.md` (D22).
No surprises.

**Privacy sweep.** A scan of `matchups/` and `matchup-passes/` for email addresses,
external URLs, credential patterns and government-id patterns returns nothing. Both
pass reports and the matchup report carry `visibility: private`. The one private figure
present is 58.25 — **T2** — and it is present in two files the publication gate refuses
to clear.

## Findings

| Severity | scope / blocking | Rule | Artifact | Finding | Required repair |
|---|---|---|---|---|---|
| Major | scope: framework + event / blocking: **no** | CLAUDE.md "Artifact shape lives in `framework/templates/` and `schemas/`, read by `atj.reports`, `atj.schema`"; D22 | `matchup-passes/*.md`, `atj/reports.py:26-37`, `atj/event.py:41-44`, `schemas/matchup.schema.json` | **T1.** Nothing validates the two pass reports. `atj validate reports` covered 22 artifacts, exactly the `.md` files in the ten directories in `ARTIFACT_KINDS`; these two are in none of them. No schema, template, placeholder, or evidence-reference check reaches the only written record of the comparative evidence. The publication gate does reach them and fails closed. | Framework, not event: add a `matchup-pass` artifact kind whose schema requires exactly one populated pass, or declare a subdirectory the matchup validator skips and the report validator covers. Already D22, Tier 2. Must land before an event with more than one matchup. |
| Major | scope: event, tournament stage / blocking: **no** | `summaries/team-podcast.md:763` — any derivative "must not contain 58.25" | `matchup-passes/mu-final-01-pass-a-first.md:431`, `matchup-passes/mu-final-01-pass-b-first.md:94` | **T2.** The unofficial provisional 58.25 appears in both pass reports. Not blocking: both occurrences are explicit negations ("were not compared", "is not a total"), both files are `visibility: private`, `matchups/mu-final-01.{json,md}` are free of it, no total is reachable by `atj matchup`, and the publication gate refuses to clear anything in that directory. But the consolidation stage's instruction is unenforced here because of T1. | Leave the text — striking a sentence that records a prohibition being honoured would make the record worse. When T1 is fixed, the 58.25 check must extend to the new artifact kind. Until then, no artifact under `matchup-passes/` may be promoted toward `public/` or a dossier without a manual read. |
| Major | scope: `workspaces/` / blocking: **no** | CLAUDE.md "stage-then-promote"; the staging copy is the provenance record | `workspaces/live-trial-2026/staging/matchup/pass-a-first.md` | **T3.** The staged a-first is still the truncated 118-line first extraction and was never refreshed after the depth-aware re-extraction. The staging record no longer matches what was promoted, so a later provenance check comparing the two would report a 315-line discrepancy against a correct artifact. The b-first staged copy is byte-identical to its promotion. | Re-stage the complete a-first, or delete the stale staged copy and note in `status.md` that the a-first staging record was superseded by the re-extraction. `workspaces/` is untracked, so this is an operator action with no commit. |
| Minor | scope: event, tournament stage / blocking: **no** | `atj/matchup.py:170-174` order-balancing guard; canonical A/B orientation | `matchup-passes/mu-final-01-pass-b-first.md:5-6,22-27` | **T4.** The b-first report's front matter declares `team_a: team-podcast` / `team_b: team-ledger`, inverting the canonical orientation held by `matchups/mu-final-01.json` and `bracket.json`, and sets `passes.a_first.presented_first: team-podcast` — the same team as `b_first.presented_first`. Fed to the tool as written, that front matter trips "order balancing failed: both passes presented the same team first". **Proven harmless:** re-resolved under the report's own labelling, the winner is still team-ledger (margin -35.0, favouring its `team_b`). The prose at `:40-49` states the orientation unambiguously and the tool applied it correctly. | Normalize the two pass reports' front matter to the canonical `team_a`/`team_b` from `bracket.json`, keeping the Orientation prose. Best done as part of the T1 schema fix so the new artifact kind pins the orientation. |
| Minor | scope: event, tournament stage / blocking: **no** | Every factual conclusion must cite evidence in the package | `matchup-passes/mu-final-01-pass-a-first.md:232`, `matchup-passes/mu-final-01-pass-b-first.md:197` | **T5.** The two passes state different counts of the same fact: a-first "Two of the skill statements are false against the implementation", b-first "three statements in the instruction text that are false against the implementation". Both cite the same underlying items; a-first names two (tier-0 `order_id`, the reclassification no-op), b-first names three (adding the tier-3 match claim). One is wrong. Neither moved a comparison value — both landed `agentic` at meaningful-advantage strength for the same reason — and the discrepancy is itself evidence of independence. | Record the discrepancy in `status.md`. No score moves and no value is recalculated. If a dossier quotes either figure, it must use the itemized list, not the count. |
| Minor | scope: event / blocking: **no** | B3 repair established `bracket.md` as regenerated from `bracket.json` by script | `events/live-trial-2026/bracket.md:56-59` | **T6.** The four-line "**Result:**" block is a prose addition to a file the bracket audit's B3 repair had just established as script-generated, so `bracket.md` is again part generated and part hand-written. Its three figures all reconcile to `mu-final-01.json`, so nothing is wrong with the content. | Fold the result into the renderer so `bracket.md` regenerates whole from `bracket.json` plus the matchup artifact, or note in `status.md` that `bracket.md` carries a hand-maintained result block. Either is acceptable; drifting between the two is not. |

## Advisories

**TA1 — "consistent" is doing quiet work on `innovation`.**
`matchups/mu-final-01.md:73` marks the `innovation` row `consistent` where a-first is `0`
and b-first normalized is `+1`. That is faithful to the tool: `atj/matchup.py:184` flags
a criterion only on strictly opposite signs, and this pair is not opposite. The report
does not hide it — `:96-99` says the passes "differed in magnitude (0 in A-first, +1
normalized in B-first) without disagreeing in direction." No change wanted. Noting only
that a reader scanning the table alone would not learn that one judge saw no advantage
where the other saw one, on the criterion carrying the whole 2.50 of difference between
the two pass margins.

**TA2 — D20 still fails `atj event validate`, and still should not block.**
`python3 -m atj event validate events/live-trial-2026` returns FAIL with the single
problem "performance-qualified byes need a consolidated score for every eligible team;
missing for ['team-podcast']" — `atj/event.py:356-364` demanding a score without asking
whether any bye exists. There are none. This is the pre-existing framework defect logged
at the bracket stage (`docs/framework-fix-plan.md:41`, Tier 1), it is unchanged by the
tournament stage, and both in-event repairs remain blocking offences. `atj event status`
reports the correct next action regardless.

**TA3 — the check-8 framing, restated exactly.** See check 8. `92c6687..HEAD` is empty
for `judgments/` but not for `summaries/`, because the consolidated reports were written
after `92c6687`. The claim that holds for this gate is that nothing under `judgments/`,
`summaries/` or `adjudications/` has changed since the consolidation gate `7591d48`.

**TA4 — the dossier stage started before this gate passed.**
`events/live-trial-2026/dossiers/team-ledger.md` and `team-podcast.md` were written and
committed at `329d8d2` and `a8c0cf8` while this audit was in progress, and both list
`matchups/mu-final-01.md` in their `source_reports` — they consume the artifact this
audit exists to clear. CLAUDE.md requires the applicable audit to be complete and
recorded with `atj event gate` before an event stage advances.

Ruled **advisory, not blocking**, on three grounds, and it is a close call I am stating
rather than burying:

1. It is outside the blocking scope. The finding is inside
   `events/live-trial-2026/` but in the **dossiers** stage, not the tournament stage,
   and it touches none of the eight blocking triggers.
2. **No gate was falsified.** `status.md` still reads `tournament-audited: pending` and
   `dossiers-approved: pending`. Nobody claimed a pass that had not happened.
3. **Nothing was consumed wrongly.** The audit it front-ran now passes, and the figure
   the dossiers took from the matchup — the +35.00 combined margin, in both files — is
   the figure this audit independently reproduced. Had the audit failed, that work would
   have had to be redone; it did not.

Two things to check at the dossiers gate rather than here, since they are that audit's
business and not mine: neither dossier contains 58.25, and `76.3` appears only in
team-ledger's own dossier. `atj validate reports` raises `[foreign-team]` advisories on
both, each naming the other team, which is expected for a head-to-head dossier and is
for the dossiers audit to confirm against the match-public boundary.

The process point stands: an audit whose result is not yet known should not have
downstream work built on it, because the only reason this cost nothing is that the
result came back PASS.

## The eight blocking triggers, one by one

| Trigger | Status | Basis |
|---|---|---|
| A matchup not judged in both presentation orders | **clear** | Two passes exist, `presented_first` differs, `atj/matchup.py:170-174` would have refused otherwise |
| One pass exposed to the other | **clear** | Phrase-origin trace, structural divergence, and a genuine disagreement on `innovation` — check 2 |
| Normalization done by hand | **clear** | Raw and normalized blocks stored side by side by `atj/matchup.py:152-168`; raw matches the judge's own front matter |
| A winner not supported by the recorded margins | **clear** | Both passes picked team-ledger independently; combined +35.00 at seven times the band |
| Arithmetic that does not reproduce | **clear** | Full-key identity between my independent run and the committed JSON |
| Initial totals used to select a winner | **clear** | No score is an input to `atj matchup`; both passes state and apply the prohibition — T2 is disclosure in a private file, not use |
| An unauthorised score move | **clear** | No judgment, summary or adjudication changed since `7591d48`; `bracket.json` moved one field, the winner |
| Private information in public output | **clear** | `public/` empty; the matchup report clears the publication gate; `matchup-passes/` fails the gate closed |

## Completion gate

- [x] No blocking findings
- [x] No major findings **inside the blocking scope** — T1, T2 and T3 are major and all three are outside it, ruled per finding
- [x] Calculations valid — full-key identity against an independent `atj matchup` run
- [x] Evidence references resolve — every evidence id in both pass reports checked against the two manifests
- [x] Version and identity checks pass — `release-check` PASS, rubric `head-to-head@1.0.0`, persona `matchup-judge@1.0.0`, framework commit consistent across all three matchup artifacts
- [x] Privacy boundary passes — `public/` empty, matchup report CLEAR, `matchup-passes/` fails closed

**PASS WITH ADVISORIES. The `tournament-audited` gate may be set.**

Recommended order:

1. Fix **T3** in `workspaces/` — re-stage or delete the stale truncated a-first. No commit.
2. Record **T5** and the **T6** decision in `status.md`, and add this audit's activity row.
3. Carry the **T1** publication-gate finding into `docs/framework-fix-plan.md` under D22,
   and raise its practical urgency note. **T2** and **T4** close with the D22 fix; neither
   is repairable inside this event without making the record worse.
4. Then, and last:

```
python3 -m atj event gate events/live-trial-2026 tournament-audited passed \
  --audit audits/tournament.md
```

5. Confirm `status.md` `last_updated` exceeds the newest activity row.
