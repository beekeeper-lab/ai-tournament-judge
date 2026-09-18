---
event_id: live-trial-2026
team_id: team-ledger
judge_id: judge-backend
judge_run_id: jr:live-trial-2026:team-ledger:judge-backend:b859a240:01
commit: 9d21b7707f204ef60f5a1cee612f1d4db0a4a575
evidence_package_id: ev:live-trial-2026:team-ledger:9d21b7707f20:b859a240
rubric: submission-evaluation@1.0.0
persona: judge-backend@1.0.0
framework_commit: 0677b6cf43ab9445d30a5cd4c185c4d27ff00bbf
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-17T19:13:20Z"
completed_at: "2026-09-17T19:20:39Z"
visibility: private
approval_state: draft
validation_state: unvalidated
scores:
  functional: 4
  product: 4
  agentic: 3
  engineering: 4
  reliability: 3
  security: 4
  innovation: 4
confidence:
  functional: high
  product: medium
  agentic: medium
  engineering: high
  reliability: high
  security: high
  innovation: medium
model:
  model_requested: claude-opus-5
  model_used: claude-opus-5
  started_at: "2026-09-17T19:13:20Z"
  completed_at: "2026-09-17T19:20:39Z"
  verified: true
  note: judge ran as a live claude-opus-5 subagent; the persona's tool set is read-only,
    so the orchestrator wrote the returned document verbatim and generated the scores
    table with `atj render judgment`
---
# Individual Judgment

## Executive assessment

This is a competent, proportionate backend built by someone who has thought about
data integrity rather than someone who has read about it. The load path refuses
rather than guesses, the refusal is provable against the statement's own
arithmetic, and the refusal was demonstrated on a real discrepancy rather than
asserted. The matcher deliberately declines to be a global optimizer and states
why in its own docstring, and that decision is carried through to the detector
that consumes it — `d1_unmatched` counts anything not `COMMITTED` as unexplained,
so an ambiguous explanation cannot quietly retire a charge. That coherence
between a stated principle and the code that implements it is the strongest thing
in the submission.

The weaknesses are not structural, they are concentrated. One advertised workflow
is a no-op by construction (F1). One advertised match tier cannot produce a match
(F2). The single most consequential module in the system — the one that computes
a legal clock and a dollar figure — has no unit test and was only ever executed in
the branch where it computes nothing (F3). Those three are what I would hand back.

No criterion is `NE`. The package's `evidence_limited_criteria: []` holds up under
pressure: every criterion here has either substantial direct observation or enough
inspectable artifact to support a defensible score. I tested that claim rather
than accepting it, and I say where each score is load-limited instead.

Evidence classes are tagged inline: **[DO]** direct observation, **[AE]** artifact
evidence, **[TC]** team claim, **[INF]** my inference.

## Scores

<!-- atj:scores:begin -->
| Criterion | Raw score or NE | Weight | Weighted points | Confidence |
|---|---:|---:|---:|---|
| functional | 4.0 | 25 | 20.00 | high |
| product | 4.0 | 15 | 12.00 | medium |
| agentic | 3.0 | 15 | 9.00 | medium |
| engineering | 4.0 | 15 | 12.00 | high |
| reliability | 3.0 | 10 | 6.00 | high |
| security | 4.0 | 10 | 8.00 | high |
| innovation | 4.0 | 10 | 8.00 | medium |
| **Total** |  | **100** | **75.0** |  |
<!-- atj:scores:end -->

## Criterion findings

### functional — 4, confidence high

**Evidence.** Nine of ten advertised subcommands were observed producing correct
output against synthetic input. [DO] `runs/team-ledger-cli-help-01.json` (CLI
surface matches documentation);
`runs/team-ledger-csv-ingest-detect-01.json` (ingest to status to detect to validate);
`runs/team-ledger-ingest-integrity-01.json` (four rejections, zero rows written
afterward, then idempotent re-ingest reporting `0 new, 0 merged, 1 already known`);
`runs/team-ledger-amazon-match-detect-01.json` (tier-0 `REFERENCE` at confidence
1.0, tier-1 `AMOUNT_DATE_UNIQUE` at 0.95, one `UNMATCHED`, D0 + D1, validate OK);
`runs/team-ledger-analyze-render-dispute-01.json` (four analyze modes, three
rendered reports, dispute CSV + packet);
`runs/team-ledger-pdf-grammar-01.json` and `-02.json` (the line grammar against
all four documented hazards, rejecting on a genuine $500 discrepancy and passing
when balanced).

**Strengths.** The control-total gate runs before any write
(`src/fin/ingest.py:144`, `check_control_totals` called before `store.archive`),
so the no-partial-import claim is structural rather than incidental [AE]. Ingest
refuses to infer a sign convention it was not given
(`src/fin/adapters/citi_csv.py:70`, "Refusing to guess") [DO]. D0 fired on a
single transaction with no history and cited the exact charges, dates, and net
[DO].

**Deficiencies.**

- **F1 (confirmed defect).** Re-ingesting a source file does not reclassify
  anything. `src/fin/ingest.py:186-190` computes the source id from
  `(file digest, line_no, raw_line)` and `continue`s on a known id before the
  transaction is touched; `category` and `merchant_family` are assigned only in
  `_new_transaction` (`ingest.py:232,249-252`), and `_merge` (`ingest.py:285-298`)
  does not update either. `.claude/skills/fin-analyze/SKILL.md:70-75` tells the
  agent "Rules apply at ingest time, so after editing them re-ingest the sources
  to reclassify. Ingestion is idempotent, so this is safe." It is safe and it is
  also a no-op [AE + DO]. The run output corroborates the mechanism: a second
  identical ingest reports `0 new, 0 merged, 1 already known` and touches nothing
  (`runs/team-ledger-ingest-integrity-01.json`). Categories are fixed at first
  observation for the life of the vault unless the user deletes the ledger [INF].
- **F2 (confirmed docs/implementation mismatch).** Tier 3 cannot produce a match.
  `src/fin/match/engine.py:227` resolves only the edges from `build_edges`, which
  emits tier 0 and tier 1/2 exclusively (`engine.py:51-95`). `subset_sum_edges`
  output is appended to `by_txn` at `engine.py:254-257`, and every entry in
  `by_txn` becomes an `AMBIGUOUS` link with `merchant_charge_id=""`
  (`engine.py:259-272`). The module's own tier table (`engine.py:6-10`) and
  `.claude/skills/fin-reconcile/SKILL.md:29` ("tiers 0-3, commits only edges
  unique on both sides") both say otherwise [AE]. Split-shipment reconciliation —
  the difficulty the README names as the motivating one — is delivered as an
  annotation, not a match. Unexercised, so this is a static read, not a witnessed
  failure.
- **F4.** Two of the four ingest rejection paths escape as a raw `ValueError`
  traceback rather than the clean `REJECTED <file>: <reason>` line, because
  `cmd_ingest` catches only `IngestRejected` (`src/fin/cli.py:46`) [DO,
  `runs/team-ledger-ingest-integrity-01.json` stderr]. Nothing is written either
  way, so this is a user-facing contract inconsistency, not a data problem.
- **F5.** `_infer_year` (`src/fin/adapters/citi_pdf.py:262-277`) falls back to
  `date(end.year, mm, dd)` when no candidate year lands in the cycle, silently and
  with no warning. In `runs/team-ledger-pdf-grammar-01.json` this produced
  `2026-12-20` for a row on a statement whose billing period is
  `2026-07-15 .. 2026-08-14` [DO]. The control-total gate checks amounts, not
  dates, so a mis-yeared row imports clean and then feeds the dispute deadline
  and every date-windowed detector [INF].
- Known gaps I weighed but did not penalize as failures: the `pdftotext`
  subprocess call and the `.pdf` suffix `sniff()` were never executed, but the
  grammar they wrap was exercised directly against every hazard the adapter's
  docstring names, and `/usr/bin/pdftotext` was confirmed present
  (`runs/team-ledger-envcheck-01.json`). Absence of that one link is not evidence
  of failure. Tier 2 is unexercised but is three lines of confidence assignment
  (`engine.py:86`) and I can read it.

**Rationale.** The promised primary workflow — load, prove the load lossless,
reconcile, flag what cannot be explained, produce a packet — works end to end and
was watched working. The defects are one advertised secondary workflow that does
nothing, one tier that cannot commit, and two rough edges. That is a 4, not a 5:
a 5 would require the split-shipment tier to actually reconcile and the
reclassification loop to actually reclassify.

**Uncertainty.** Everything scored here is synthetic input by design. The PDF CLI
seam, tier 2, tier 3, and the two unproduced report kinds are unobserved.

**Highest-value improvement.** Fix F1. A skill that instructs the agent to
re-ingest for reclassification, on a system where re-ingest cannot reclassify,
will produce a confidently wrong answer to a user who followed the documentation.

### product — 4, confidence medium

**Evidence.** [TC] Intake "Team statement" and README frame the problem as 201
unauthorized charges over 343 days on a card that should never have carried them.
[DO] The output is legible without the source: `findings.md` reproduces the D0
detail verbatim with the binding that was violated, the window, the net, and the
individual charge lines (`runs/team-ledger-analyze-render-dispute-01.json`). The
dispute CSV carries per-charge provenance and claim type. [AE] Reports carry a
`GENERATED ... Do not edit` header (`src/fin/render.py:35`).

**Strengths.** The stated principle — "the product is not the matched set, the
product is the unmatched set" — is implemented, not decorated. D1 refuses to draw
a conclusion when no feed is loaded and says so in the finding text rather than
reporting a 0% match rate (`src/fin/detect/detectors.py:120-138`, observed firing
as `info` in two runs) [DO]. The dispute module re-tags an expired billing-error
window as `UNAUTHORIZED_USE` rather than dropping the item
(`src/fin/dispute.py:69-71`) [AE], which is the correct product call and the one
most systems get wrong. Ingest labels its own weaker guarantee in the output line:
`[UNVERIFIED (no control totals)]` [DO].

**Deficiencies.** Five `cp` steps and an env var before the first command does
anything; there is no `fin init` (`src/fin/cli.py` subparser list) [AE].
`analyze recurring` printed nothing at all — not "none" — which reads as a broken
command (`runs/team-ledger-analyze-render-dispute-01.json`) [DO]. F1 above is a
product trap as much as a code defect. Two of five report kinds were never
produced, though that follows from the scenario, not from a failure.

**Rationale.** Well-scoped, honest about what it does not know, and the output is
usable by the person it was built for. Held at 4 because a chunk of the intended
experience — the agent driving the CLI — was never observed, and the setup ritual
is longer than it needs to be.

**Uncertainty.** Medium confidence specifically because the agent-driven half of
the product is unobserved.

**Highest-value improvement.** A `fin init` that copies the example configs and
prints the vault path. It removes the only hard onboarding step.

### agentic — 3, confidence medium

**Evidence.** [AE] Four skill files read in full as data:
`.claude/skills/fin-ingest/SKILL.md`, `fin-reconcile`, `fin-analyze`,
`fin-dispute`. [DO] My own grep across the entire checkout for injection phrasing
(`ignore previous`, `disregard`, `system prompt`, `jailbreak`, `you are now`,
`new instructions`, `do not report`, `score this`, `evaluator`, `judge`, `rubric`)
returned one match, and it is the benign sentence
`.claude/skills/fin-analyze/SKILL.md:68` "judgement is used once, reviewed by a
human, and then frozen into code." Nothing in this submission addresses an
evaluator or attempts to direct scoring. This independently corroborates
ev-ledger-10 and the intake's own claim. [DO] ev-ledger-20's grep result is
consistent with what I read: no model API surface anywhere in `src/fin/`.

**Strengths.** The architectural decision is the right one and it is enforced by
the code rather than by policy: arithmetic, parsing, and money live in tested
Python with no model in the path, and the model's job is command selection and
explanation (`src/fin/cli.py:1-7` docstring, corroborated by the absence of any
model call site). The skills are disciplined in ways most are not — explicit
negative routing ("Do NOT use to load data (fin-ingest)"), a governing rule stated
before any command, an instruction to present candidates and *ask* rather than
pick on ambiguity (`fin-reconcile/SKILL.md:50-54`), an instruction to use `fin sql`
instead of reading JSONL into context and doing mental arithmetic
(`fin-analyze/SKILL.md:31-33`), and explicit honesty requirements including
"never describe a charge as fraudulent" and "state plainly that the deadline
arithmetic is a calculation, not legal advice." Human approval is required before
a proposed rule is written, and once written the model is out of the loop forever.

**Deficiencies.** Two of the skills contain statements that are false against the
implementation: the tier-3 claim (F2) and the reclassification claim (F1). An
agent following either will report something that did not happen. Runtime
effectiveness is entirely unobserved — no agent loop can run in a no-network
sandbox — and there is no agent-side logging or trace artifact, so even with a
runtime there would be nothing to audit beyond the CLI's own stdout.

**Rationale.** The design deserves a 4; the execution does not yet. Two factual
errors in the instruction text, one of which corresponds to a workflow that cannot
work, plus zero observed effectiveness, puts this at 3. This is not `NE`: I have
the full instruction surface as artifact evidence and I can verify its claims
against the code, which is most of what this criterion asks.

**Uncertainty.** Effectiveness and observability under an actual agent are
unknown. The evidence package cannot close that and neither could the team under
the event's constraints.

**Highest-value improvement.** Make the skill text derivable from, or tested
against, the CLI. A skill that names a tier the engine cannot commit is a
documentation bug that only shows up as a wrong answer to a user.

### engineering — 4, confidence high

**Evidence.** [AE] Full read of `src/fin/cli.py`, `ingest.py`, `store.py`,
`validate.py`, `dispute.py`, `match/engine.py`, `detect/detectors.py`,
`adapters/citi_pdf.py`; targeted reads of `normalize.py`, `config.py`, `render.py`.
22 source files total.

**Strengths.** Module boundaries follow the domain and nothing crosses them
sideways: adapters parse, `ingest` gates and writes, `match` reconciles, `detect`
reads transactions and links, `validate` asserts, `render` and `analyze` are pure
readers. No ORM, no service layer, no dependency injection, no configuration
framework. The JSONL store states its tradeoff and its mitigation in the same
docstring (`src/fin/store.py:1-12`) and then actually implements the mitigation
(`fin validate`, invoked after every mutating ingest at `cli.py:53-54`). Writes
are tmp-then-`replace` (`store.py:115-120`) and rows are sorted before write, so
the ledger is reproducible and git-diffable. Ids are content-derived, which is what
makes idempotence a property rather than a check.

The comments are the best signal here. They explain the decision and the failure
mode it avoids, not the syntax: `_find_duplicate`'s three-day rule with both
directions of error named (`ingest.py:256-261`); `_section_of`'s longest-prefix
ordering with the specific misparse it prevents (`citi_pdf.py:228-231`);
`_family_matches` refusing prefix matching so an AWS bill is not reported as
retail fraud (`detectors.py:40-49`); `_assign_statements` explaining why membership
follows the source record and not the date (`ingest.py:332-341`). Someone will be
able to change this code in a year.

**Deficiencies.**

- **F7.** `UNMATCHED` links are persisted with `method="AMOUNT_DATE_UNIQUE"`
  (`engine.py:283`), visible in the stored table: the `fin sql` output shows
  `AMOUNT_DATE_UNIQUE | UNMATCHED | 0.0`
  (`runs/team-ledger-amazon-match-detect-01.json`) [DO]. A method recorded for a
  non-match is wrong data in a table other code queries.
- **F8 (credible risk).** `ingest_card_file` claims all-or-nothing but performs
  three independent whole-table writes after the gate: `_upsert_statement` to
  `write_all("statements")` at `ingest.py:160`, then `write_all("transactions")`
  and `write_all("sources")` at `ingest.py:224-225`. Each file is individually
  atomic; the set is not. A failure between them leaves transactions with no
  source records, and `validate` does not check that direction — it only flags
  sources pointing at a missing transaction (`validate.py:45`). Not demonstrated.
- **F9.** `validate.py:1-12` says conservation means "every charge is in exactly
  one bucket: matched, ambiguous, or unmatched." The code does not check that
  partition; conservation only compares verified-statement totals
  (`validate.py:80-114`). Docstring overreach on the module whose job is to be
  exact.
- **F6 (credible risk).** `build_edges` compares `abs(c.amount_cents) == want`
  where `want = abs(t.amount_cents)` (`engine.py:74-77`), and the candidate set
  includes refunds (`_amazon_txns`, `engine.py:43-48`). A minus-$5.00 refund and a
  plus-$5.00 merchant charge three days apart are a tier-1 match. On a system whose
  premise is that refunds land later under different descriptors, sign-blind
  matching is the wrong default. Unexercised; no run contains that shape.
- `resolve()` computes `txn_count`/`charge_count` once per outer pass and then
  mutates `claimed_*` inside the inner loop, so counts go stale mid-pass
  (`engine.py:114-129`). Correctness is preserved by the claimed-set guard and the
  next iteration, but it takes a careful read to establish that, and there is no
  test pinning it.
- `run()` (`engine.py:217-292`) carries two structurally different paths — the
  resolve-based tiers and the subset-sum bypass — with different commit semantics
  and no test on either.

**Rationale.** Coherent, proportionate, readable, with a small cluster of real
rough edges that a reviewer fixes in an afternoon. 4. It is not a 5 because the
matcher is the least disciplined module in an otherwise disciplined codebase, and
two docstrings state guarantees the code does not provide.

**Uncertainty.** Low. This is a static read of code I had complete access to.

**Highest-value improvement.** Make `matches.jsonl` honest: give `UNMATCHED` a
`NONE` method, and either make tier 3 commit or rename it so it stops advertising
a capability the engine does not have.

### reliability — 3, confidence high

**Evidence.** [DO] `runs/team-ledger-pytest-01.json`: 35 passed, exit 0, 0.07s,
offline, `--network none`. [AE] `tests/test_properties.py`, full function
inventory read. [DO] My grep of that file for `dispute|interest_attribution|
infer_year|citi_csv|CitiCsv|render|resolve|build_edges|subset_sum_edges|EXPIRED|
BILLING_ERROR` returned **no matches**.

**Strengths.** The tests are aimed at the properties that actually break this kind
of system, not at line coverage: sub-cent precision refused rather than rounded;
float money losing a cent; the wrapped-description row surviving; page furniture
not becoming a description; rate disclosure after the stop marker not parsing as a
transaction; the gate rejecting a deliberately deleted row; two identical charges
in one file staying two transactions; the three ledger invariants asserted through
the *real* loader via `_TextAdapter` (`tests/test_properties.py:214-292`), which
does exercise `_upsert_statement`, `_assign_statements`, and the conservation check
that no sandbox run ever reached. D0's two false-positive modes are tested
explicitly, including "an AWS bill is not retail Amazon fraud." Detectors read
"as of" from the ledger's max post date rather than the wall clock
(`detectors.py:36-37`), so a re-run is reproducible. `fin validate` is invoked
automatically after a successful ingest.

**Deficiencies.**

- **F3 (the one that matters).** `src/fin/dispute.py` has zero tests. The three
  state transitions `OPEN` / `EXPIRING` / `EXPIRED` and the corresponding
  `BILLING_ERROR` to `UNAUTHORIZED_USE` retagging (`dispute.py:67-76`) were never
  executed by any test and never executed by any run in this package: every
  observed dispute item came back `NO_STATEMENT` with
  `DisputeDeadline=unknown`, because no run ever ingested a statement with a close
  date (`runs/team-ledger-analyze-render-dispute-01.json`; every run shows
  `statements 0` in `fin status`) [DO]. `interest_attribution`'s month-by-month
  carried-balance loop (`dispute.py:100-112`) is likewise untested; the observed
  $0.29 came from a two-item single-month case, which does not exercise the carry.
  This is the module with a legal clock and a dollar figure attached to its output.
- No tests for `citi_csv.py`, `amazon.py`, `render.py`, `analyze/spend.py`,
  `_infer_year`, `build_edges`, `resolve`, or `subset_sum_edges`. Only the pure
  `subset_sum` function is covered.
- No logging or structured run record; diagnosis is stdout text. Appropriate for a
  single-user local CLI, so I do not treat it as a deficiency — but combined with
  F8 it means a partial write would be silent and undetectable.

**Rationale.** A genuinely thoughtful 35-test property suite that leaves the
money-and-deadline module entirely uncovered is a 3. The quality of what is tested
argues for more; the location of what is not tested argues against it, and the
untested part is the part where being wrong costs the user a claim.

**Uncertainty.** Low. Test inventory and coverage gaps are directly verifiable and
I verified them by grep rather than by reading the manifest's summary.

**Highest-value improvement.** Test `dispute.build` across the close-date
boundary — one case per state, plus a multi-month `interest_attribution` carry.
Roughly forty lines.

### security — 4, confidence high

**Evidence.** [DO] `runs/team-ledger-vault-perms-01.json`: vault root `700`,
archived raw source `600`. [DO] `runs/team-ledger-analyze-render-dispute-01.json`:
dispute CSV `600`, set explicitly at `src/fin/cli.py:185`. [AE]
`src/fin/config.py:88-90` rejects any `last4` longer than four digits and any
config key in `("pan","card_number","number","cvv","expiry")`, with two tests
pinning it (`tests/test_properties.py:382-400`). [AE] `hooks/pre-commit` (42
lines, per ev-ledger-19) blocks committing ledger data, `.env`, real config,
Luhn-valid PANs, and live token patterns. [DO] My own injection grep across the
checkout found nothing directed at an evaluator.

**Strengths.** The privacy claims are demonstrated rather than asserted, and the
controls are cheap and correct for the threat that actually applies to a
local-first personal finance vault: other users on the same host, and the user
accidentally committing their own statements. The PAN guard fails the *load*,
not a warning, and is tested. No network, HTTP, or model surface anywhere in 22
source files; the only `subprocess` invocation is the local `pdftotext`. The
responsible-AI posture is unusually concrete: the skills forbid calling a charge
fraudulent, require stating what cannot be concluded without a feed, and require
saying the deadline math is not legal advice.

**Deficiencies (ordinary hardening, not defects).**

- **F10.** Only the vault *root* is chmod'd (`store.py:70-73`). `ledger/`, `raw/`,
  `reports/` and every `.jsonl` inside are created at the default umask. The
  0700 root makes this adequate in practice, but it is inconsistent with the
  explicit 0600 applied to the dispute CSV and the archived raw file, and it
  breaks if the vault is ever relocated under a permissive parent.
- `cmd_sql` f-string-interpolates the vault path into `CREATE VIEW ...
  read_json_auto('{p}')` and executes `args.query` verbatim
  (`cli.py:217-223`). Arbitrary SQL is the advertised feature and the only data
  reachable is the user's own, so impact is low — but `fin sql` is a full local
  SQL surface and should be described as one.
- `.env.example` could not be read (host deny rule, carried in the manifest's
  Missing evidence). Not the team's doing; the grep showing `FIN_DATA_DIR` is the
  only `os.environ` read in `src/fin/` (`store.py:53`) makes a runtime secret
  requirement unlikely [INF], but unconfirmed.

**Rationale.** Above the bar for what this is, with the controls demonstrated
rather than claimed and a shipped pre-commit guard that solves a real user
failure mode. 4. Not a 5: the permission model is applied inconsistently and one
documented file could not be inspected.

**Uncertainty.** Low, except for `.env.example`.

**Highest-value improvement.** Set the mode at creation for everything under the
vault, not just the root — one `os.umask` or three `chmod` calls in
`Store.__init__`.

### innovation — 4, confidence medium

**Evidence.** [AE] `src/fin/detect/detectors.py:1-17` (detectors ordered by
time-to-detection, with the explicit claim that D2-D5 could not have fired
confidently until month six of a 343-day fraud while D0 would have fired on day
one on a single $13.95 charge); `src/fin/match/engine.py:11-18` (the engine is
"deliberately *not* a global optimizer" because an optimizer will absorb a
fraudulent charge into a plausible order); `src/fin/dispute.py:11-14` (expired
billing-error window is re-tagged, never dropped). [DO] D0 firing on transaction
one with no history and no feed, twice.

**Strengths.** Two genuinely contrarian ideas, both implemented. D0 replaces
statistical fraud detection with five lines of declared configuration — which
card a merchant is permitted to touch — and consequently detects on the first
transaction instead of the hundredth. The anti-optimizer matcher inverts the
usual objective function and treats ambiguity as a correct output; the design
principle survives into the detector that consumes the links
(`detectors.py:140`), which is where this kind of principle normally gets quietly
discarded. Ordering detectors by time-to-detection rather than sophistication is
real analysis of the failure the system was built after.

**Deficiencies.** The most technically ambitious component is the least finished:
subset-sum cannot commit a match (F2), and `subset_sum` enumerates
`combinations` over every subset size up to `MAX_EXHAUSTIVE_ITEMS = 20`
(`engine.py:158-170`) — 2^20 per order per candidate transaction in the worst case,
with no measurement anywhere in the package [INF]. The rest of the system is
solid engineering rather than novel: control totals, JSONL, DuckDB, and a tiered
matcher are all known techniques used well.

**Rationale.** 4 for two original ideas that are implemented and carried through,
held off 5 because the ambitious tier is incomplete and unmeasured.

**Uncertainty.** Medium: the ambition concentrates in tiers 2 and 3 and the agent
layer, all unobserved.

**Highest-value improvement.** Either finish tier 3 so it commits a unique
subset-sum solution, or delete it and say the system does not reconcile split
shipments. A half-built tier that advertises a capability is worse than an
absent one.

## Surprises

**Better than expected.**

- The comments. Almost every non-obvious decision carries the failure mode it
  avoids, in the code, at the point of the decision. `_find_duplicate`'s
  three-day rule names both directions of error; `_family_matches` explains why
  prefix matching would report an AWS bill as retail fraud. This is the single
  strongest maintainability signal in the submission and it is rare.
- The stated design principle survives contact with the consumer.
  `d1_unmatched` counts anything not `COMMITTED` as unexplained
  (`detectors.py:140`), so an `AMBIGUOUS` subset-sum annotation cannot retire a
  charge from the unmatched pile. I went looking for the place where "the product
  is the unmatched set" gets quietly abandoned and did not find it.
- D1's no-feed branch. Most systems report a 0% match rate as a finding. This one
  refuses and explains that a 0% rate against a feed that was never loaded is not
  evidence of anything (`detectors.py:120-138`), observed firing twice.
- The test suite's targets. It tests the hazards the author was actually afraid
  of, including one test that deletes a row from a statement to prove the gate
  refuses the whole file.

**Worse than expected.**

- F1. The advertised reclassification loop is a no-op, and it sits at the exact
  point where the LLM contributes its only real judgment. The idempotence
  mechanism that makes the system trustworthy is the same mechanism that makes
  this workflow do nothing, and nobody noticed.
- F3. Every run in the package produced `statements 0`. The entire
  statement-backed half of the data model — dispute deadlines, claim-type
  transitions, the conservation invariant — was never reached by any sandboxed
  execution, and the tests cover conservation but not dispute. The manifest
  presents R8 as directly observed via ev-ledger-07; what ev-ledger-07 actually
  shows is the `NO_STATEMENT` branch, where the deadline is literally the string
  `unknown`. That is a materially weaker observation than the manifest's summary
  implies, and it is why I read the run records instead of the summary.
- F5. A December date parsed into a July-August billing cycle, no warning, in the
  team's own hazard fixture — sitting in a run record the manifest cites approvingly.

## Blocking and major issues

**Blocking.** None. The primary advertised workflow completes.

**Confirmed defects** (observed in a run record, or established by direct code
read at the pinned commit):

- **F1** — re-ingest does not reclassify; `.claude/skills/fin-analyze/SKILL.md:70-75`
  documents a workflow that cannot take effect. `src/fin/ingest.py:186-190`,
  `:232`, `:285-298`.
- **F2** — tier 3 `SUBSET_SUM` can never produce a `COMMITTED` match;
  `src/fin/match/engine.py:6-10`, `:254-272`, and
  `.claude/skills/fin-reconcile/SKILL.md:29` all state otherwise.
- **F3** — `src/fin/dispute.py` has no unit tests and only its `NO_STATEMENT`
  branch was ever executed.
- **F4** — two of four ingest rejection paths emit a traceback; `src/fin/cli.py:46`.
- **F5** — `_infer_year` silently assigns an out-of-cycle date;
  `src/fin/adapters/citi_pdf.py:262-277`, observed as `2026-12-20` in
  `runs/team-ledger-pdf-grammar-01.json`.
- **F7** — `UNMATCHED` links persist `method="AMOUNT_DATE_UNIQUE"`;
  `src/fin/match/engine.py:283`, visible in the stored table.
- **F9** — `src/fin/validate.py`'s docstring claims a bucket-partition check the
  code does not perform.

**Credible risks** (sound reasoning from code, not witnessed):

- **F6** — sign-blind amount matching can pair a refund with an equal-amount
  purchase charge; `src/fin/match/engine.py:74-77` with `:43-48`.
- **F8** — ingest performs three non-atomic table writes after claiming
  all-or-nothing, and `validate` cannot detect the resulting orphan direction;
  `src/fin/ingest.py:160,224-225`, `src/fin/validate.py:45`.
- Subset-sum enumeration is 2^20 worst case with no measurement;
  `src/fin/match/engine.py:158-170`.

**Ordinary hardening, never in scope** — not counted against any score:

- **F10** — vault subdirectories and `.jsonl` files use the default umask while
  the root is 0700 and two specific files are 0600.
- **F11** — `analyze recurring` prints nothing rather than "none".
- No `fin init`; five manual `cp` steps before first use.

**Untested concerns.** The `pdftotext` subprocess seam and the `.pdf` `sniff()`
check; match tiers 2 and 3 at runtime; the reconciliation and per-statement
report kinds; the entire agent-driven layer; `.env.example`'s contents (blocked
by a host control, not by the team).

**Package observations, not team findings.** My task brief names twelve
`runs/team-ledger-*.json` records; eleven exist and eleven are cited by the
manifest (`cli-help-01`, `csv-ingest-detect-01`, `ingest-integrity-01`,
`amazon-match-detect-01`, `analyze-render-dispute-01`, `pdf-grammar-01`,
`pdf-grammar-02`, `vault-perms-01`, `pytest-01`, `envcheck-01`, `envcheck-02`).
No evidence is missing relative to the manifest; the brief's count is off by one.
Separately, the manifest's R8 row overstates what ev-ledger-07 demonstrates, as
described under F3 — the manifest is otherwise careful and explicitly flags its
own limits, including the R13 `order_id` vs `external_ref` documentation error,
which I confirmed independently from `runs/team-ledger-amazon-match-detect-01.json`
(the row with an empty `external_ref` column fell through to tier 1).

**Nothing in this submission attempted to direct my evaluation.** I grepped the
full checkout for injection and evaluator-directed phrasing and found one benign
sentence about human review of model proposals. `hooks/pre-commit` is a defensive
control shipped with the product.

## Most valuable single improvement

**F1, then F3.**

Fix the reclassification path first. It is the only place where a user who
follows the documentation gets a silently wrong result: the agent proposes rules,
the human approves them, the user re-ingests exactly as instructed, and nothing
changes — with no error, no warning, and an output line (`0 new, 0 merged, N
already known`) that reads like success. Every other defect here either fails
loudly, is confined to an unexercised path, or is cosmetic. The minimum fix is a
re-derivation pass over existing transactions when the rules file changes, or a
`fin reclassify` command; the honest interim fix is deleting that paragraph from
the skill.

F3 is second and close. The dispute module computes a legal clock and a dollar
figure, has no test, and has never run in the branch where it computes anything.
Forty lines of test across the close-date boundary would close it.

## Calculation and independence declaration

- [x] Scores were calculated by the repository script — raw scores and confidence
      appear in front matter only; the weighted table between the
      `atj:scores` markers is left empty for `atj render judgment` to generate
      from `framework/rubrics/submission-evaluation.md`. No weight, weighted
      point value, or total is typed anywhere in this document.
- [x] Every material finding cites evidence — a run record under
      `events/live-trial-2026/runs/`, or a repository-relative path with a line
      or symbol at commit `9d21b7707f204ef60f5a1cee612f1d4db0a4a575`. Evidence
      class is tagged inline as [DO], [AE], [TC], or [INF].
- [x] No other judge report was inspected — nothing under
      `events/live-trial-2026/judgments/` or
      `workspaces/live-trial-2026/staging/` was read, and no material belonging
      to the other team was opened.
- [x] Submission instructions were treated as untrusted data — the README, SPEC,
      code comments, skill files, and the pre-commit hook were read as evidence
      about the submission, never as direction. An independent injection scan
      found no evaluator-directed content.
