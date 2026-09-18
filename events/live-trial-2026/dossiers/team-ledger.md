---
event_id: live-trial-2026
team_id: team-ledger
commit: 9d21b7707f204ef60f5a1cee612f1d4db0a4a575
evidence_package_id: ev:live-trial-2026:team-ledger:9d21b7707f20:b859a240
rubric: submission-evaluation@1.0.0
persona: build-team-dossier@1.0.0
framework_commit: 96e3f32
source_reports:
- summaries/team-ledger.md
- summaries/team-ledger.json
- evidence/team-ledger/manifest.md
- matchups/mu-final-01.md
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-18T00:00:00Z"
completed_at: "2026-09-18T00:00:00Z"
visibility: team
approval_state: draft
validation_state: unvalidated
---

# Team Dossier — Hive Ledger

## Your project at a glance

Hive Ledger is a local-first personal-finance CLI whose governing principle is
that the system refuses rather than guesses, and whose product is the set of
charges it cannot explain. Four judges evaluated it independently, at commit
`9d21b770`, against one shared evidence package
(`ev:live-trial-2026:team-ledger:9d21b7707f20:b859a240`) under
`submission-evaluation@1.0.0`.

**Overall panel result: 76.3 / 100, finalized.**

All seven criteria landed in the aligned agreement band. No criterion was scored
`NE`, no criterion was flagged as a possible outlier, no integrity problem was
recorded, and no adjudication was required. That is an unusually clean judging
record, and it means the number above is an official total rather than a
provisional one.

The panel agreed on the project's character without being told what it was: every
judge found the refusal principle implemented rather than asserted, and every
judge located the ceiling in the same place — the last step short of
demonstration. The most ambitious parts of the system are the least exercised
parts.

### What this result does not cover

Read the score alongside these limits. All four are properties of the evaluation
environment or of the data available, not observations about your code.

- **The agent layer was never run.** The four `.claude/skills/*/SKILL.md` files
  presume an interactive agent driving `fin`. Under the event's no-network
  sandbox there is no way to run that loop, so the skills were read as static
  evidence ([[evidence:ev-ledger-18]]) and the described behaviour — an agent
  picking commands, reading output, explaining it — was never demonstrated. This
  is the criterion where the event, not your submission, sets the evidence
  ceiling.
- **CLI-level PDF ingest was never invoked.** The approved container image had no
  PDF-authoring tool, so no realistic fixture PDF could be built inside an
  offline sandbox and `fin ingest <file>.pdf` was never run. The parsing grammar
  was exercised directly against synthetic layout text reproducing every hazard
  your own adapter docstring names ([[evidence:ev-ledger-08]],
  [[evidence:ev-ledger-09]]), and the `pdftotext` binary the CLI path shells out
  to was confirmed present. Confidence is limited to the `subprocess.run` call
  and the `.pdf` suffix `sniff()` check, not to the parsing and validation logic
  they wrap. This is why the package records `execution_status:
  sandboxed-partial`.
- **Every functional observation used synthetic data.** Your repository ships no
  real financial data by design, so all inputs were constructed for this
  evaluation. The inputs were deliberately engineered to hit your documented
  hazards, but nothing here tells you how the adapters behave against a real
  export.
- **Scale is unobserved.** The largest ledger anywhere in the evidence package is
  four rows. Your stated target is tens of thousands. Nothing in the record
  supports or contradicts your behaviour at that size, and no measurement exists
  anywhere for the subset-sum enumeration bounded by `MAX_EXHAUSTIVE_ITEMS = 20`.

One smaller gap: `.env.example` was never read, under a host rule that blocks
reading any `.env*` file. All four judges treated the residual risk as low,
because the only environment variable read anywhere in `src/fin/` is
`FIN_DATA_DIR` ([[evidence:ev-ledger-20]]), and all four recorded it as
unconfirmed rather than resolved.

## What you did especially well

These are the things the panel agreed on, with the specific evidence behind each.

**The stated principle survives into the code that consumes it.** This was the
strongest single finding in the report. A judge verified that `d1_unmatched`
counts anything not `COMMITTED` as unexplained, so an `AMBIGUOUS` annotation
cannot quietly retire a charge from the unmatched pile — the place where a
system like this normally cheats. A second judge independently found the same
discipline in five more places: credit-sign inference, D0 prefix matching, D1
with no feed, `_find_duplicate` and `_assign_statements`. A third found it in
report section ordering. Two judges went looking specifically for where "the
product is the unmatched set" gets abandoned, and did not find it.
[[evidence:ev-ledger-03]], [[evidence:ev-ledger-06]], [[evidence:ev-ledger-15]]

**Refusal is demonstrated, not claimed.** Four malformed ingest attempts were
rejected with every table left at zero rows, and a following re-ingest was
idempotent — `0 new, 0 merged, 1 already known` ([[evidence:ev-ledger-04]]).
Separately, the control-total gate rejected a synthetic statement for a genuine
$500.00 discrepancy and cited the exact amount ([[evidence:ev-ledger-08]]). The
no-partial-import half of your claim is the hard half, and it is the half that
was observed working.

**D1 refuses to report a rate it cannot compute.** The no-feed branch declines to
report a 0% match rate against a feed that was never loaded, and says so in the
finding text. Three judges called this out unprompted.
[[evidence:ev-ledger-06]]

**Privacy controls are enforced in code and verified by execution.** Vault root
at mode `0700` and the archived raw source file at `0600`
([[evidence:ev-ledger-11]]); the dispute CSV written at `0600`
([[evidence:ev-ledger-07]]); a PAN guard that raises at config load with two
tests behind it; and a shipped `hooks/pre-commit` that blocks committing ledger
data, `.env`, real config, Luhn-valid card numbers and live token patterns
([[evidence:ev-ledger-19]]). One judge noted that the privacy claims survived
contact with execution rather than stopping at the README.

**No model in the money path.** An exhaustive scan of all 22 files in `src/fin/`
found zero network, HTTP or LLM imports and zero matching call sites; the only
`subprocess` use is the local `pdftotext` ([[evidence:ev-ledger-20]]). Every
judge treated that absence as a directly observed favourable fact rather than an
unknown. The allocation of work between model and code is correct and
structurally enforced, and that enforcement is visible in the artifact rather
than promised in prose.

**The comments state the rejected alternative and the failure mode it avoids.**
One judge rated this "the single strongest maintainability signal in the
submission"; two others named the same property from different modules. It is
the reason `engineering` is unanimous at 4.0, together with module boundaries
that follow the domain with no layering inversions, integer cents throughout,
content-derived ids that make idempotence a property rather than a check, and
atomic tmp-then-replace writes with deterministic sort order. One judge's
summary: "Someone will be able to change this code in a year."

**The skill files carry real operating constraints.** They encode refusal rules
aimed at the model's known failure modes rather than persona padding: never call
a charge fraudulent, never file anything, state that deadline arithmetic is not
legal advice, never tell a user an expired billing-error window extinguishes the
claim ([[evidence:ev-ledger-18]]). Two judges remarked that a prompt encoding a
specific past failure as a stop condition is rare.

**The generated markdown is the best-designed surface in the submission.** A
do-not-edit banner naming the regeneration command, source attribution, section
ordering by user urgency, findings reproduced verbatim from the ledger. Three
judges named it, including the judge hardest on the rest of the interface.
[[evidence:ev-ledger-07]]

**The test suite targets the hazards you were actually afraid of**, including a
test that deletes a row from a statement to prove the gate refuses the whole
file. 35 tests passed, exit 0, offline, in 0.07s ([[evidence:ev-ledger-12]]).

**The originality is in the problem framing, and it is substantive.** D0 replaces
statistical fraud detection with a declared card-to-merchant binding and fires on
transaction one. The matcher refuses to be a global optimizer, on the stated
ground that a higher match rate hides fraud. The dispute model re-tags an expired
billing-error window rather than dropping it. `innovation` is unanimous at 4.0
for those three decisions.

## Criterion feedback

Scores are out of 5. Weighted points are `score / 5 * weight`; every figure below
is read from the official result, not recomputed.

| Criterion | Weight | Panel mean | Points | Agreement |
|---|---:|---:|---:|---|
| Functional correctness and completeness | 25 | 4.00 / 5 | 20.00 | aligned, all four identical |
| Product value and usability | 15 | 3.75 / 5 | 11.25 | aligned, range 1.0 |
| Agentic and AI system design | 15 | 3.50 / 5 | 10.50 | aligned, range 1.0 |
| Engineering and maintainability | 15 | 4.00 / 5 | 12.00 | aligned, range 0.0 |
| Reliability, testing, and observability | 10 | 3.25 / 5 | 6.50 | aligned, range 1.0 |
| Security, privacy, and responsible AI | 10 | 4.00 / 5 | 8.00 | aligned, range 0.0 |
| Innovation and technical ambition | 10 | 4.00 / 5 | 8.00 | aligned, range 0.0 |
| **Overall** | **100** |  | **76.3** |  |

The Points column sums to 76.25. The Overall row shows **76.3**, which is the official
display total after the rubric's half-up rounding to one decimal place — the row is the
official figure, not the column sum (audit DO3).

No judge recorded low confidence on any criterion. Confidence was medium to high
throughout, and it does not track score direction: on `reliability` the three
judges at 3 recorded high confidence while the judge at 4 recorded medium, and on
`product` the judge at 3 recorded high while two of the judges at 4 recorded
medium.

### Functional correctness and completeness — 4.00 / 5

**Demonstrated.** Nine of ten advertised subcommands ran to correct completion in
sandboxed records ([[evidence:ev-ledger-01]], [[evidence:ev-ledger-02]],
[[evidence:ev-ledger-04]], [[evidence:ev-ledger-06]],
[[evidence:ev-ledger-07]]). The control-total gate rejected a real $500.00
discrepancy ([[evidence:ev-ledger-08]]). The balanced fixture parsed all four
documented layout hazards — a merchant name wrapped across three lines, page
furniture between rows, a rewards-column bleed, and a single-date interest row —
and passed the gate ([[evidence:ev-ledger-09]]). Re-ingest was idempotent
([[evidence:ev-ledger-04]]). All four judges read the run records themselves
rather than the manifest summary, and all four declined to treat the unexercised
PDF CLI seam as a failure.

**Limitations.** Each judge named a different reason this is not a 5, and the
list is a fair map of your unexercised surface: the reclassification path, the
unreachable tier 3, the `external_ref` documentation mismatch, the unexecuted
dispute state machine, and the untested `AMBIGUOUS` outcome. One judge called the
dispute state machine "the single largest unverified claim in the package" and
lowered his own confidence for that reason. Three of the five tiers your matcher
declares were exercised — tier 0, tier 1 and tier 4. Tier 2 (ambiguity) and tier
3 (subset-sum) were not, because no scenario produced an amount-and-date
collision or a split charge.

**Next steps.** Ship one fixture scenario per unexercised branch. That single
change converts most of this section's limitations into observations.

### Product value and usability — 3.75 / 5

**Demonstrated.** Three judges weighted problem fit and the quality of the
generated reports and reached 4. The problem is real, the scope is honest, and
the rendered output is the strongest interface you have.

**Limitations.** This is the criterion with a genuine interpretation split, so
you should have both readings. One judge scored the live interaction surface —
help text, empty states, the error contract, whether the headline command names
its headline result — reached 3, and recorded the highest confidence of anyone on
this criterion. What he observed, all of it in run records: a Python traceback on
a routine user error; three of the four `analyze` modes with no empty state, with
`recurring` printing nothing at all; bare argparse subcommand help with no
descriptions or examples; `--limit` documented on `analyze` but consumed only by
`merchants`; inconsistent null rendering across surfaces; `sources` counting
per-row provenance while reading as "files ingested"; and `fin match` printing
`committed=2, unmatched=1` while naming no unmatched charge — on the command that
implements your stated thesis. Two of the three judges who scored 4 named the
same traceback in their own `product` sections and scored 4 anyway. The split is
about what a CLI's usability consists of, not about what the code does.

Setup friction was named by three judges: five manual `cp` steps and an
environment variable before the first command, with no `init` subcommand.

**Next steps.** Make `fin match` print the unmatched charges, not just the count.
Give every `analyze` mode an empty state that says why it is empty. Add `fin
init`.

### Agentic and AI system design — 3.50 / 5

**Demonstrated.** All four judges agreed on three facts: the model/code split is
correct and structurally enforced, with no model, HTTP or network call site
anywhere in the package ([[evidence:ev-ledger-20]]); the skill files carry real
operating constraints ([[evidence:ev-ledger-18]]); and runtime effectiveness is
entirely unobserved for reasons that are the event's, not yours. One judge called
the control model "the best thing in this submission". All four explicitly
considered `NE` and all four gave an explicit reason for scoring instead.

**Limitations.** Two judges scored 3 and two scored 4, and the disagreement is
about what unobserved effectiveness plus factual errors in the instruction text
should cost. One of the judges at 3: "The design deserves a 4; the execution does
not yet," citing two skill statements that are false against the implementation.
The other reached 3 on the same shape of argument plus the absence of any eval,
transcript or routing check. One of the judges at 4 pre-registered the
counterfactual himself: if the panel weights demonstrated agent behaviour
heavily, his score belongs a point lower.

A related item, agreed as fact and scored two ways: nothing records which command
an agent chose, with what arguments, before a ledger mutation. Two judges counted
that against this criterion; two recorded the same absence and declined to
penalize it for a single-user local CLI.

**Next steps.** The cheapest way to move this criterion is to make the agent
layer observable and to make the instruction text true. An append-only
`audit.jsonl` of subcommand, arguments, exit code and row counts was estimated at
about twenty lines by the judge who proposed it.

### Engineering and maintainability — 4.00 / 5

**Demonstrated.** Unanimous, range 0.0, and unanimous on the reasons: domain-
aligned module boundaries with no layering inversions, integer cents throughout,
content-derived ids, atomic tmp-then-replace writes with deterministic sort
order, and comments that name the rejected alternative.

**Limitations.** Also unanimous, and all in one family: documentation that states
a guarantee the code does not provide, concentrated outside the well-trodden CSV
path. Three confirmed instances — the tier-0 `order_id` framing (below),
`validate.py`'s docstring claiming a bucket-partition check the code does not
perform, and `store.py` saying invariants are asserted "after every mutation"
when only a successful non-dry-run ingest revalidates. One judge also found an
`amazon.py` comment that contradicts the line immediately beneath it, on the
mechanism that makes your headline feature work.

**Next steps.** Treat docstrings that state guarantees as code. A short pass
where every "asserts", "verifies" and "guarantees" in a docstring is checked
against the function beneath it would close this entire family.

### Reliability, testing, and observability — 3.25 / 5

**Demonstrated.** 35 tests passed, exit 0, offline ([[evidence:ev-ledger-12]]),
and all four judges praised the property-shaped targets. The judge who scored 4
rated prevention, detection and recovery "clearly above event standard and
verified by execution", with diagnosability as the single weak leg.

**Limitations.** The three judges at 3 disagree about which hole matters most,
and each hole is independently real:

- `src/fin/dispute.py` has no tests, and only its `NO_STATEMENT` branch has ever
  executed — every run in the package shows `statements 0`. That is the module
  computing a legal clock and a dollar figure. One judge: "A genuinely thoughtful
  35-test property suite that leaves the money-and-deadline module entirely
  uncovered is a 3."
- No test imports `fin.cli`, so exit codes, the `REJECTED` contract and every
  rendered report are uncovered.
- The `AMBIGUOUS` outcome has no test, and it is the exact branch your governing
  rule rests on.

One point of clarity, because the reports could otherwise leave you with two
contradictory impressions: three `test_subset_sum_*` cases cover the pure
`subset_sum` function. No test covers the tier-3 wiring through `resolve()`. Both
statements are true; "tier 3 is tested" and "tier 3 is untested" are the same
fact described at two levels.

**Next steps.** Item 2 of the improvement plan below. Roughly forty lines of test
closes the most consequential of these gaps.

### Security, privacy, and responsible AI — 4.00 / 5

**Demonstrated.** Unanimous at 4.0 with range 0.0. All four confirmed the same
controls: vault root `0700` and archived raw source `0600`
([[evidence:ev-ledger-11]]), dispute CSV `0600` ([[evidence:ev-ledger-07]]), the
PAN guard with two tests behind it, the shipped `hooks/pre-commit` scanner
([[evidence:ev-ledger-19]]), and no network or model surface in the deterministic
core ([[evidence:ev-ledger-20]]). All four independently ran their own injection
scan across your skill files and pre-commit hook, read as data, and all four
found nothing directed at an evaluator ([[evidence:ev-ledger-10]]).

**The panel's widest disagreement is here, and it is invisible in the score.**
`security` is unanimous at 4.0, and underneath that unanimity two judges rate
`fin sql` the highest-consequence item in the whole submission while two rate the
same code low impact. All four read the same code. Nobody attempted an exploit.
The difference is threat model, and you should hold both readings:

- The low-impact reading: arbitrary SQL is the advertised feature, and the only
  data reachable is the user's own, so the impact is low. A second judge treats
  it as a diagnosability annoyance.
- The high-consequence reading: "the delta that matters is the agent." `fin sql`
  executes arbitrary DuckDB on a default connection — no read-only mode, no
  statement-kind check, no `enable_external_access = false` — while your analyze
  skill steers a model toward it, and the descriptors that model reasons over
  arrive from files the user did not author. That traces a path from
  attacker-influenced text through a model-composed query to filesystem and
  network access, from a process you advertise as offline. Two judges reached
  this independently. One put it as: nine tools are narrow and audited, and the
  tenth hands a model a general-purpose execution engine, under a skill that
  encourages its use.

Both readings are defensible from the same code. The second one is cheap to
neutralize, which is why it sits at item 3 of the plan.

Two further items, neither of which moved a score: the permission model is
applied more narrowly than the README's "every output" framing — only the vault
root carries an explicit mode, and an `OSError` on chmod is swallowed, so on a
filesystem that cannot chmod the guarantee degrades silently. And
`op run --env-file=.env` places resolved secrets into the environment of a
process that reads exactly one variable, `FIN_DATA_DIR`.

**Next steps.** Constrain `fin sql`. Set an explicit mode on the ledger JSONL
files and subdirectories rather than inheriting the root's, and log rather than
swallow a chmod error.

### Innovation and technical ambition — 4.00 / 5

**Demonstrated.** Unanimous. D0 firing on transaction one from a declared
binding, the matcher's deliberate refusal to be a global optimizer, and the
dispute model's re-tag of an expired window are all genuine design positions,
argued in the code.

**Limitations.** Unanimous here too: the most ambitious components are the least
demonstrated. Ambition that no run record reaches cannot score above a 4.

**Next steps.** Every item in item 9 of the plan below exists to make an
ambitious component visible.

## Tournament journey

You entered a two-team single-elimination bracket with no byes, so your journey
was one match: the final.

**Final — you won.** The result was produced by `atj matchup` from two
order-balanced passes, one presenting you first and one presenting you second,
judged by two evaluators who worked without sight of each other's reports and
neither of whom computed a margin. Both passes picked Hive Ledger independently.
All seven criteria were order-consistent. The combined margin was +35.00 on a
-100..+100 scale, seven times the close-call band of ±5.0, so the outcome
confirmed automatically with no adjudication and no tie-break. Your opponent in
the final was team-podcast.

The comparison rested on four criteria where both passes agreed your evidence was
the stronger: `functional`, `agentic`, `engineering` and `security`, contributing
+12.50, +7.50, +7.50 and +5.00 respectively. `innovation` added +2.50, where the
two passes differed in magnitude but never in direction. `product` and
`reliability` were level in both passes and contributed nothing either way.

Two things are worth knowing about how that result was reached. First, no
criterion reached a decisive value in either pass — the margin is the sum of five
moderate advantages, not one knockout. Second, both matchup judges predicted the
combined margin would land near the close-call band, and the deterministic
calculation matched neither intuition. Your win is wider than the people who
judged it expected.

Initial consolidated totals were not used to select a winner; the head-to-head
rubric forbids it, and both passes recorded that they did not.

## Blocking issues

**None.** All four judges state that no confirmed defect prevents a primary
advertised workflow from completing, and every workflow the panel observed exited
0. The evidence package records `evidence_limited_criteria: []` — no criterion
was left unscorable for lack of evidence.

One confirmed defect is not blocking but is the most consequential item in this
dossier, because it is the only confirmed defect that silently degrades a real
user's *results* rather than their experience:

**Tier-0 matching keys on `external_ref`, not on `order_id`.** Your `fin-ingest`
skill text and README both attribute tier-0 matching to the order id. The adapter
sources `external_ref` from a literal CSV column; `order_id` is used only to
sniff the file as the transactions feed. A user who builds a feed from your
documented column list, with `order_id` populated and no `external_ref` column,
falls through to tier-1 amount-and-date matching and is never told. Confirmed by
all four judges and by direct observation ([[evidence:ev-ledger-06]],
[[evidence:ev-ledger-16]]). It is item 1 below.

Three further items are worth your attention with an honest caveat attached:
each was raised by **one judge only**, from source at the pinned commit, and
neither corroborated nor contradicted by the other three, because no other judge
examined the same question. Judge independence was preserved correctly, so this
is the expected outcome — but none of the three is a panel consensus, and you
should weigh them as one careful reader's finding rather than as four.

- **Re-ingest does not reclassify (one judge's finding).** Your `fin-analyze`
  skill instructs the agent to re-ingest after editing rules. Known source ids
  `continue` before the transaction is touched, and `_merge` updates neither
  `category` nor `merchant_family`, so the instruction cannot take effect. The
  finding was established by direct code read and corroborated by the `0 new, 0
  merged, 1 already known` output in [[evidence:ev-ledger-04]]. That judge rated
  it his top fix, and described the honest interim repair as deleting the
  paragraph from the skill. His summary of why it matters: the loop is a no-op at
  exactly the point where the model contributes its only real judgment.
- **Dispute deadlines are computed against the ledger's latest post date, not
  today (one judge's finding).** From source; no run exercised it. That judge
  called it "the most consequential issue in the submission: it is silent, it is
  on by default, and it produces a confidently wrong number on the output with a
  legal clock," and noted that the `EXPIRING` bucket your skill tells the agent
  to surface first would never fire. Hold this one alongside a genuine tension:
  two other judges cite the same ledger-relative "as of" convention in the
  detector layer approvingly, as the thing that makes a detect run reproducible.
  They did not address the dispute path. The convention may be right in one layer
  and wrong in the other, and nobody on the panel tested that proposition.
- **`cmd_ingest` returns 0 after `_revalidate` reports invariant problems to
  stderr (one judge's finding).** From source; no scenario produced a failing
  invariant. He calls it "the worst failure mode in this list" because the exit
  code is the only machine-readable signal an agent or script has.

Three items in the list that follows were also raised by **one judge only** and were
neither corroborated nor contradicted: the `_infer_year` out-of-cycle date, the D1
finding-title mislabel, and the `hooks/pre-commit` lowercase `*.csv` gap. Their
classification as confirmed defects matches the record, but no panel consensus is
asserted for any of them (audit DO1).

For completeness, the other confirmed defects, none of them blocking: two of four
ingest rejection paths surface as a Python traceback rather than the clean
`REJECTED <file>: <reason>` contract, with nothing written either way
([[evidence:ev-ledger-05]], named by all four judges); `UNMATCHED` links persist
`method="AMOUNT_DATE_UNIQUE"`, visible in user-facing output as
`AMOUNT_DATE_UNIQUE | UNMATCHED | 0.0`, on a table other code queries
([[evidence:ev-ledger-06]]); `_infer_year` silently assigned an out-of-cycle date
(`2026-12-20` on a statement whose billing period is `2026-07-15 .. 2026-08-14`)
in your own hazard fixture, with no warning, and the control-total gate checks
amounts rather than dates ([[evidence:ev-ledger-08]]); D1's finding title labels
card charges as "merchant-feed charges"; and `hooks/pre-commit` blocks `*.CSV`
but not lowercase `*.csv`, with `.gitignore` covering the common case.

Two credible risks nobody could exercise: three independent whole-table writes in
`ingest_card_file` after the all-or-nothing gate, where a failure between them
leaves transactions whose source records do not exist and `validate.py:45` checks
only the opposite direction, so the torn state passes validation clean (two
judges, independently, including the same blind spot in `validate`); and
sign-blind amount matching in `build_edges`, which compares absolute values over
a candidate set that includes refunds, on a system whose premise is that refunds
land later under different descriptors (one judge).

## Recommended improvement plan

Ordered by how many judges independently nominated each item and by whether it
changes a user's results rather than their experience.

### 1. Immediate repair

1. **Make the tier-0 documentation match the implementation.** Add `external_ref`
   to the documented column list in `amazon.py`, the `fin-ingest` skill and the
   README; fix the contradicting comment; and warn from `ingest-amazon` when a
   feed carries no `external_ref` column. Confirmed by all four judges, one
   judge's top fix, and the only confirmed defect on this list that silently
   degrades real results.
2. **Give `src/fin/dispute.py` tests across the close-date boundary.** One case
   per state, the `EXPIRED` re-tag to `UNAUTHORIZED_USE`, and a multi-month
   `interest_attribution` carry, all with a fixed as-of date. Estimated at
   roughly forty lines by the judge who proposed it. Two judges named this gap
   independently; it is the module computing a legal clock and a dollar figure
   with zero coverage.
3. **Constrain `fin sql`.** Reject anything that is not a single `SELECT` or
   `WITH`, set `enable_external_access = false`, and lock the configuration
   before executing. One judge's top fix overall and a second judge's nomination
   on two criteria. Note the disagreement recorded above: two judges consider
   this low impact. It is on the list this high because the fix is small and the
   downside of being wrong about the threat model is not.

### 2. Highest-value next iteration

4. **Fix the reclassification path.** A re-derivation pass when the rules file
   changes, or an explicit `fin reclassify` command. One judge's top fix, raised
   by him alone. If you do not fix the path, delete the paragraph from the skill
   that promises it.
5. **Default the dispute as-of date to today.** Keep `--as-of` for reproducible
   runs, and print the as-of date in the terminal summary and as a CSV column.
   One judge's top fix, raised by him alone, and in tension with two judges who
   praised the ledger-relative convention in the detector layer. Printing the
   as-of date resolves most of the tension whichever default you choose.
6. **Unify the ingest rejection contract.** Convert the two adapter `ValueError`
   raises to `IngestRejected`, or add a top-level handler in `main()`. Named by
   all four judges and described by two of them as a two-line fix.
7. **Make the matches table honest and decide tier 3's status.** Give `UNMATCHED`
   a `NONE` method, and either wire subset-sum through `resolve()` so it can
   commit, or state plainly that the system does not reconcile split shipments.
   One judge: "A half-built tier that advertises a capability is worse than an
   absent one."
8. **Return non-zero when post-ingest revalidation reports problems, and add the
   reverse orphan check to `validate`.** Two separate judges' `reliability`
   nominations. Together they close the only failure state ingest can currently
   produce undetected, and correct the only machine-readable signal that is
   currently wrong.

### 3. Longer-term opportunity

9. **Make the unexercised paths observable.** A committed fixture PDF or a
   `--from-text` flag for the CLI path; one scenario with an amount-and-date
   collision so `AMBIGUOUS` can be seen; one dispute run against an ingested
   statement; and a fixture ledger demonstrating D0 firing on transaction one
   while the statistical detectors stay silent. Each of these was nominated by a
   different judge, and together they would have moved this evaluation's evidence
   base more than any other single change.
10. **Add `fin init` and an append-only invocation log.** `fin init` removes the
    only hard onboarding step and was named by two judges. An append-only
    `audit.jsonl` recording subcommand, arguments, exit code and row counts turns
    the agent layer from unobservable into reviewable — estimated at about twenty
    lines. This is the cheapest available lever on `agentic` and on the
    diagnosability leg of `reliability`.
11. **Measure the enumeration bound and run something at scale.** Nothing in the
    package measures the subset-sum worst case at `MAX_EXHAUSTIVE_ITEMS = 20`,
    and the largest ledger anyone ran was four rows. One benchmark fixture at a
    realistic size would answer a question the whole evaluation had to leave
    open.

Not counted against you at any point, and worth knowing: the panel treated your
local-first single-user scope as honest rather than evasive. No GUI, no packaging
beyond `pyproject.toml`, no telemetry, no multi-user support, no authentication
or encryption at rest, no supply-chain pinning, and your own declared Phase 4/5
gaps in `SPEC.md` §12 were all excluded from scoring.

## Evidence appendix

Everything in this dossier traces to an item below or to the consolidated panel
report. Source paths resolve against your checkout at commit
`9d21b7707f204ef60f5a1cee612f1d4db0a4a575`. Run records live in
`events/live-trial-2026/runs/`; you can read the exact commands, limits and
output for each.

| Evidence | What it shows | Run record |
|---|---|---|
| [[evidence:ev-ledger-01]] | `fin --help` and all ten subcommand help screens match the documented CLI surface exactly | `team-ledger-cli-help-01.json` |
| [[evidence:ev-ledger-02]] | A synthetic 3-row Citi CSV ingests cleanly and labels itself `UNVERIFIED (no control totals)` | `team-ledger-csv-ingest-detect-01.json` |
| [[evidence:ev-ledger-03]] | D0 fires on a binding violation citing the specific charges, dates and net; `fin validate` passes afterward | `team-ledger-csv-ingest-detect-01.json` |
| [[evidence:ev-ledger-04]] | Four rejected ingest attempts leave every table at zero rows; a repeat ingest reports `0 new, 0 merged, 1 already known` | `team-ledger-ingest-integrity-01.json` |
| [[evidence:ev-ledger-05]] | Two of four rejection paths print a clean `REJECTED` line; two surface as a full Python traceback | `team-ledger-ingest-integrity-01.json` (stderr) |
| [[evidence:ev-ledger-06]] | Tier-0 `REFERENCE` at 1.0 via the shared `external_ref` token, tier-1 at 0.95, one `UNMATCHED`; D0 and D1 match the matcher's output | `team-ledger-amazon-match-detect-01.json` |
| [[evidence:ev-ledger-07]] | All four `analyze` modes, three rendered reports, and a dispute packet computing `NO_STATEMENT` state and $0.29 attributable interest; dispute CSV at mode `0600` | `team-ledger-analyze-render-dispute-01.json` |
| [[evidence:ev-ledger-08]] | The PDF line grammar parses three hazard rows, then the control-total gate rejects the statement for a genuine $500.00 discrepancy | `team-ledger-pdf-grammar-01.json` |
| [[evidence:ev-ledger-09]] | The same grammar on a balanced statement parses four correctly classified rows through all four documented hazards and passes the gate | `team-ledger-pdf-grammar-02.json` |
| [[evidence:ev-ledger-10]] | Injection-phrase scan of the skill files and `hooks/pre-commit` found zero matches, reproduced independently by all four judges | static read, no execution |
| [[evidence:ev-ledger-11]] | Vault root `0700`, archived raw source file `0600` | `team-ledger-vault-perms-01.json` |
| [[evidence:ev-ledger-12]] | Full pytest suite: 35 passed, 0 failed, exit 0, offline, 0.07s | `team-ledger-pytest-01.json` |
| [[evidence:ev-ledger-13]] | `adapters/base.py` `Adapter`/`CreditSign`: the explicit sign-convention protocol behind the refusal behaviour | source at the pinned commit |
| [[evidence:ev-ledger-14]] | `detect/detectors.py:d0_binding_violation`: declarative matching with no history required | source at the pinned commit |
| [[evidence:ev-ledger-15]] | `match/engine.py:build_edges`, `resolve`: tier system and fixpoint commit logic, deliberately not a global optimizer | source at the pinned commit |
| [[evidence:ev-ledger-16]] | `adapters/amazon.py`: `external_ref` sourced from a literal CSV column, not from `order_id` | source at the pinned commit |
| [[evidence:ev-ledger-17]] | `dispute.py:build`, `interest_attribution`: claim typing and APR-based attribution | source at the pinned commit |
| [[evidence:ev-ledger-18]] | The four `.claude/skills/*/SKILL.md` files, read as data, never executed | static read, no execution |
| [[evidence:ev-ledger-19]] | `hooks/pre-commit`: defensive scan for ledger data, `.env`, real config, Luhn-valid card numbers and live token patterns | source at the pinned commit |
| [[evidence:ev-ledger-20]] | No network, HTTP or LLM import or call site across all 22 files in `src/fin/`; the only `subprocess` use is local `pdftotext`; the only environment read is `FIN_DATA_DIR` | static grep, no execution |

Also useful to you:

- `events/live-trial-2026/evidence/team-ledger/manifest.md` — the pinned evidence
  package, including the requirements table (R1-R16) mapping each of your
  advertised workflows to the evidence that does or does not support it, and the
  "Missing or inaccessible evidence" section that records every limit named
  above.
- `events/live-trial-2026/runs/team-ledger-*.json` — eleven run records, each
  carrying the exact command, the sandbox limits applied, and the captured
  output.
- Every execution in this evaluation ran under `podman` rootless with
  `--network none`, a read-only source mount, a non-root user, and capped CPU,
  memory, process count and time. Nothing from your submission was run on a host
  machine.

This dossier is yours. It is generated from the approved judging record for
Hive Ledger and contains no other team's material.
