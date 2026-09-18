---
event_id: live-trial-2026
team_id: team-ledger
judge_id: judge-security-ops
judge_run_id: jr:live-trial-2026:team-ledger:judge-security-ops:b859a240:01
commit: 9d21b7707f204ef60f5a1cee612f1d4db0a4a575
evidence_package_id: ev:live-trial-2026:team-ledger:9d21b7707f20:b859a240
rubric: submission-evaluation@1.0.0
persona: judge-security-ops@1.0.0
framework_commit: 0677b6cf43ab9445d30a5cd4c185c4d27ff00bbf
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-17T19:13:20Z"
completed_at: "2026-09-17T19:20:26Z"
visibility: private
approval_state: draft
validation_state: unvalidated
scores:
  functional: 4
  product: 4
  agentic: 4
  engineering: 4
  reliability: 4
  security: 4
  innovation: 4
confidence:
  functional: high
  product: medium
  agentic: medium
  engineering: high
  reliability: medium
  security: high
  innovation: medium
model:
  model_requested: claude-opus-5
  model_used: claude-opus-5
  started_at: "2026-09-17T19:13:20Z"
  completed_at: "2026-09-17T19:20:26Z"
  verified: true
  note: judge ran as a live claude-opus-5 subagent; the persona's tool set is read-only,
    so the orchestrator wrote the returned document verbatim and generated the scores
    table with `atj render judgment`
---
# Individual Judgment

## Executive assessment

Hive Ledger is a disciplined, security-aware local-first CLI. Read through a
security and operations lens it does the unglamorous things right: it refuses
data it cannot prove lossless rather than importing it partially, it enforces
"last four digits only" at config load with a raising guard and two tests, it
writes every PII-bearing artifact at `0600` inside a `0700` vault, it ships a
pre-commit scanner that blocks ledger data and Luhn-valid card numbers, and its
deterministic core contains no network, HTTP or model call at all. Those are not
claims. They were executed in the sandbox or grepped exhaustively at the pinned
commit.

Two things keep it off the top of the scale, and both are the same shape: a
control that is stated more broadly than it is implemented. The documented
credential wrapper (`op run --env-file=.env -- fin ...`) injects resolved
secrets into a process that reads no secret, which enlarges the blast radius of
a tool whose job is parsing hostile PDFs for nothing in return. And `fin sql`
hands an LLM agent an unconstrained DuckDB engine while the product's headline
claim is that the model never touches I/O or arithmetic. Neither is a
demonstrated exploit. Both are credible risks I can point at in source.

My seven scores land on 4 uniformly. That is not a default. The submission has
one consistent character across every criterion: the work that was done is
clearly above prototype standard and verified, and in every area the last step
short of complete demonstration is missing. The PDF path is parsed but never
ingested from a file. The agent layer is well designed but never run. The
matcher's ambiguity tier is the stated design principle and is exercised
nowhere, not even in the test suite. Consistent quality, consistent ceiling.

Finding codes below are mine (F1..F12) and are distinct from the manifest's
requirement ids (R1..R16).

## Scores

<!-- atj:scores:begin -->
| Criterion | Raw score or NE | Weight | Weighted points | Confidence |
|---|---:|---:|---:|---|
| functional | 4.0 | 25 | 20.00 | high |
| product | 4.0 | 15 | 12.00 | medium |
| agentic | 4.0 | 15 | 12.00 | medium |
| engineering | 4.0 | 15 | 12.00 | high |
| reliability | 4.0 | 10 | 8.00 | medium |
| security | 4.0 | 10 | 8.00 | high |
| innovation | 4.0 | 10 | 8.00 | medium |
| **Total** |  | **100** | **80.0** |  |
<!-- atj:scores:end -->

## Criterion findings

### functional — 4, confidence high

**Evidence.** Direct observation. Nine of the ten advertised subcommands ran to
correct completion in sandboxed records I read rather than taking from the
manifest summary: `runs/team-ledger-csv-ingest-detect-01.json`,
`runs/team-ledger-ingest-integrity-01.json`,
`runs/team-ledger-amazon-match-detect-01.json`,
`runs/team-ledger-analyze-render-dispute-01.json`,
`runs/team-ledger-vault-perms-01.json`, `runs/team-ledger-cli-help-01.json`.
Outputs are internally consistent: the D0 finding text in stdout reproduces
verbatim in `findings.md`, and the dispute CSV rows match the two transactions
D0 flagged. Artifact evidence: `src/fin/cli.py:242-293` defines exactly the ten
subcommands the README documents.

**Strengths.** The refusal behavior is demonstrated four ways in one run and the
vault is empty afterward (`ingest-integrity-01` stdout, all seven tables at 0),
which is the hard half of "no partial import". Idempotent re-ingest is shown in
the same record (`1 rows -> 0 new, 0 merged, 1 already known`). Tier-0 and
tier-1 matching produce the confidences the code declares (1.0 and 0.95).

**Deficiencies.** F1 (gap, not failure): the authoritative PDF path is exercised
only at `parse_text`. `CitiPdfAdapter.sniff` and the `subprocess.run(["pdftotext",
...])` call at `src/fin/adapters/citi_pdf.py:198` were never run, per the
manifest's own Missing-evidence section, because the approved image has no
PDF-authoring tool (`runs/team-ledger-envcheck-01.json`). F2: the `AMBIGUOUS`
tier (`src/fin/match/engine.py:259-273`) is exercised by no run record and by no
test (grep for `AMBIGUOUS` across `tests/` returns nothing). Tier 3 subset-sum
is better off than the manifest implies, since three unit tests cover it inside
the 35 that passed.

**Reasoning.** Broad, correct, verified coverage of the promised workflows with
two named edges unproven. Not 5, because the authoritative ingest path and the
ambiguity outcome are both inferred from code rather than observed.

**Uncertainty.** Low on what was run, moderate on the PDF file path. Absence of
that evidence is an environment limit, not a sign of failure.

**Highest-value improvement.** Commit one small fixture PDF, or accept
`--from-text` so the CLI path can be exercised without a PDF authoring tool in
the image.

### product — 4, confidence medium

**Evidence.** Artifact evidence: `README.md`, `SPEC.md` sections 1 and 12, the
four skill files. Direct observation: `runs/team-ledger-cli-help-01.json` shows
the CLI surface matching the documentation exactly, and
`runs/team-ledger-analyze-render-dispute-01.json` shows the variance report,
findings report and dispute packet a user would actually consume.

**Strengths.** The scope is honest and narrow: one person, their own cards, local
files, no forecasting, no filing, no multi-user. The generated reports carry a
"do not edit, correct the ledger and re-render" banner, which is the right
instinct for a derived artifact. Dispute output states `NO_STATEMENT` rather
than inventing a deadline.

**Deficiencies.** F3: setup is five manual `cp` commands plus a `git config`
(intake "Run instructions"). There is no `fin init`. F4: two of four ingest
rejection paths present as Python tracebacks (see reliability), which is the
first thing a new user will hit and the worst first impression the product can
make.

**Reasoning.** Solidly above expectation on problem fit and output quality, held
back by setup friction and an error surface that leaks implementation.

**Uncertainty.** Medium. Usability is judged from artifacts and captured stdout,
not from a user.

**Highest-value improvement.** `fin init` that copies the example configs and
prints the next command.

### agentic — 4, confidence medium

**Evidence.** Artifact evidence: `.claude/skills/fin-ingest/SKILL.md`,
`fin-reconcile/SKILL.md`, `fin-analyze/SKILL.md`, `fin-dispute/SKILL.md`.
Direct observation: my own exhaustive grep at the pinned commit found no model
or network call under `src/fin/` (corroborating ev-ledger-20), and my own
injection-phrase grep across the checkout returned only three benign matches
("raise its score" about match rate, "evaluate" about tier order, "scored"
about budget categories), corroborating ev-ledger-10.

**Strengths.** The control model is the best thing in this submission. The skills
tell the agent it does not parse and does not compute (`fin-ingest/SKILL.md:16`,
"You do not parse anything yourself"), forbid hand-transcribing a figure because
it breaks the provenance chain, require human approval before a proposed
merchant rule is written, and freeze the model's judgment into deterministic
config after one use. `fin-dispute/SKILL.md` carries genuine user-safety
boundaries: never file anything, never call a charge fraudulent, say plainly
that deadline arithmetic is not legal advice, never tell the user an expired
window extinguishes the claim. That last one is a documented user-harm mode
being designed against, which is rare at this level.

**Deficiencies.** F5 (credible risk): the one tool the analyze skill pushes the
agent toward is unconstrained. `fin-analyze/SKILL.md:31` says "Reach for `fin
sql` for anything the fixed reports do not cover", and `src/fin/cli.py:223` is
`result = con.execute(args.query)` on a default `duckdb.connect()`. See security
F9. F6: no observability on the agent loop at all. Nothing records which
subcommand an agent chose, with what arguments, or what it told the user. For a
system whose thesis is "the model decides what to run", there is no log of what
it decided. F7 (documentation defect, corroborates manifest R13):
`fin-ingest/SKILL.md:55-58` tells the agent the `order_id` column is "what makes
tier-0 matching possible". `src/fin/adapters/amazon.py` sources `external_ref`
from a literal CSV column and uses `order_id` only to sniff the feed, so an
agent following that text will mispredict which tier a feed will hit.

**Reasoning.** Not NE: the skills are substantial inspectable artifacts and the
absence of any model call in the core is a directly observed fact, so
appropriateness and control are judgeable. Effectiveness is not observed, which
is why this is 4 and not 5, and why confidence is medium.

**Uncertainty.** Medium. The described agent behavior was never executed, by the
event's no-network constraint, not by the team's choice.

**Highest-value improvement.** Have `fin` append every invocation (subcommand,
arguments, exit code, row counts) to an append-only `vault/audit.jsonl`. It costs
twenty lines and turns the agent layer from unobservable into reviewable.

### engineering — 4, confidence high

**Evidence.** Artifact evidence across `src/fin/` at the pinned commit:
`store.py` (atomic temp-file plus `Path.replace`), `models.py` typed dataclasses
with content-derived ids, `adapters/base.py` explicit `CreditSign` protocol,
`config.py` `yaml.safe_load` only. Direct observation:
`runs/team-ledger-pytest-01.json`, 35 tests, exit 0, 0.07s, offline.

**Strengths.** Proportionate. No framework, no service, no abstraction nobody
asked for. The comments explain the non-obvious decision rather than the code
(the date-shift merge rule at `ingest.py:256-276`, the "first currency token,
never the last" rewards-bleed rule at `adapters/citi_pdf.py:33-35`). Sign
convention is declared by the adapter and asserted, not inferred.

**Deficiencies.** F4 (confirmed defect, directly observed): two error contracts.
`adapters/citi_csv.py:54` and `:70` raise bare `ValueError`, `cli.py:cmd_ingest`
catches only `IngestRejected`, and the stderr in
`runs/team-ledger-ingest-integrity-01.json` shows two full tracebacks next to
two clean `REJECTED` lines. Nothing is written either way, so it is safe, but the
user-facing contract is inconsistent. F8: `cli.py:222` builds SQL by f-string
interpolation of the vault path into `read_json_auto('{p}')`. The path is
operator-supplied via `--data-dir`, so this is self-inflicted rather than an
attack path, but it will break on a path containing a quote.

**Reasoning.** Coherent and maintainable with two specific, cheap-to-fix rough
edges.

**Uncertainty.** Low. This is code I read directly at the pinned commit.

**Highest-value improvement.** Convert the two `ValueError` raises in the CSV
adapter to `IngestRejected`. Two lines, and the rejection contract becomes
uniform.

### reliability — 4, confidence medium

**Evidence.** Direct observation: `runs/team-ledger-pytest-01.json` (35 passed),
`runs/team-ledger-ingest-integrity-01.json` (four rejections, empty vault,
idempotent re-ingest), `runs/team-ledger-pdf-grammar-01.json` (the control-total
gate rejecting a genuinely unbalanced statement for the exact $500.00
discrepancy). Artifact evidence: `src/fin/validate.py` (three invariants),
`src/fin/store.py:109-121` (atomic per-table replace),
`src/fin/detect/detectors.py:36-37` (as-of is the latest post date, not the wall
clock, so a detect run is reproducible).

**Strengths.** Prevention and recovery are genuinely strong. The gate refuses
rather than warns. Ids are content-derived, so re-running after a fix is safe
and the skills say so. Derived tables (`matches`, `anomalies`) are rewritten
wholesale, so a stale run cannot leave phantom findings
(`store.py:47-49`). Every transaction carries source records naming the archived
file, its sha256, and the line number, which is real provenance rather than a
log line.

**Deficiencies.** F2 (untested, material): the `AMBIGUOUS` outcome is the
product's stated governing rule ("a false match is strictly worse than no
match", `fin-reconcile/SKILL.md:18`) and it is covered by no test and no run
record. The behavior everything else is justified by is the one behavior nobody
checked. F10 (credible risk, static): `ingest_card_file` writes `statements`,
then `transactions`, then `sources` as three separate atomic replaces
(`ingest.py:160,224,225`). A crash between the second and third leaves
transactions whose `source_ids` point at records that do not exist, and
`validate.py:45` checks only the opposite direction (sources pointing at missing
transactions), so that specific torn state passes validation clean. F11
(documentation versus behavior): `store.py:9-11` says the invariants are
asserted "after every mutation". `cli.py:53` runs `_revalidate` only after a
non-dry-run ingest with `rc == 0`. `fin match` and `fin detect` mutate derived
tables and never revalidate. F12 (diagnosability): `adapters/citi_pdf.py:87`
catches bare `Exception` in `sniff`, so a missing `pdftotext` binary makes a
real PDF report `no adapter recognises statement.pdf` instead of naming the
missing dependency. Unexercised, since the image has `pdftotext`, but it is
plain in the control flow. Finally, the largest ledger in the entire evidence
package is four rows, so nothing about behavior at the stated scale (tens of
thousands of rows, full-table read and rewrite on every upsert, subset-sum
across every order for every unmatched charge) is observed.

**Reasoning.** Prevention, detection and recovery are clearly above event
standard and verified by execution. Understanding a failure is the weak leg, and
it is weak in directly observed ways. That combination is a 4, not a 5.

**Uncertainty.** Medium. F10, F11 and F12 are inferences from source with no
crash-recovery or missing-dependency run to confirm them.

**Highest-value improvement.** Add the reverse orphan check to `validate` (a
transaction whose `source_ids` do not resolve), then test the `AMBIGUOUS`
outcome. Together they close the only failure state ingest can actually produce
undetected and the only untested branch of the matcher.

### security — 4, confidence high

**Evidence.** Direct observation: `runs/team-ledger-vault-perms-01.json` shows
`vault dir perm: 700` and `600 /tmp/data/raw/3f08e4abc066-good.csv`;
`runs/team-ledger-analyze-render-dispute-01.json` ends with `600` for the
dispute CSV. Artifact evidence: `src/fin/config.py:79-98` (the PAN guard),
`tests/test_properties.py:382,393` (two tests for it, inside the 35 that
passed), `hooks/pre-commit`, `src/fin/render.py:43-46` (reports chmod `0600`),
`src/fin/adapters/citi_pdf.py:198` (`subprocess.run` with a list argv, no
shell). My own grep at the pinned commit confirms no network, HTTP or model
import or call site anywhere under `src/fin/`.

**Strengths.** The privacy controls are enforced in code and verified by
execution, not asserted in a README. The PAN guard raises at load and also
rejects the field names `pan`, `card_number`, `number`, `cvv`, `expiry`, which
is defense against the mistake rather than against the attacker. `hooks/pre-commit`
is a real shipped control: it blocks ledger paths, `.env`, the real
configs, and runs a Luhn check over staged content. The responsible-AI posture
in the skills is concrete and user-protective, not boilerplate: no legal advice,
never file, do not call it fraudulent, do not scrape Amazon and say plainly why
if asked.

**Deficiencies.** F9 (credible risk, undemonstrated, my top fix): `fin sql`
executes arbitrary DuckDB on a default connection (`src/fin/cli.py:217-223`). A
default DuckDB can read local files (`read_csv_auto('/home/u/.ssh/id_rsa')`),
write them (`COPY (...) TO '/path'`), and `INSTALL`/`LOAD httpfs` to obtain
network egress. There is no statement-type check, no `enable_external_access =
false`, no `lock_configuration`. For a human querying their own data this is
roughly a shell they already have. The delta that matters is the agent: the
analyze skill directs an LLM to compose queries, and the material it reasons
over (merchant descriptors) arrives from statements and merchant exports that
the user did not author. That is a path from attacker-influenced text to
arbitrary filesystem and network access from a process the product advertises as
offline. I did not attempt it and I am not claiming an exploit. I am claiming the
control is absent and the consequence if it is reached is severe, because the
data it guards is a complete personal financial history. F13: the README's
credential workflow (`README.md:141-142`, `op run --env-file=.env -- fin ...`)
puts resolved 1Password secrets into the environment of a process that reads
exactly one variable, `FIN_DATA_DIR` (`store.py:53`), and that spends its time
parsing untrusted PDFs and CSVs. Secrets in the blast radius for zero
functionality. F14: `hooks/pre-commit:20` blocks `*.pdf|*.CSV` but not lowercase
`*.csv`. `.gitignore:14` covers the common case, but the hook is the backstop
for `git add -f`, and the most common statement export extension slips past it.
A transactions CSV usually carries no PAN, so the Luhn content scan will not
catch it either. F15 (hardening): `store.py:70-73` and `render.py:43-46` swallow
`OSError` on chmod, so on a filesystem that cannot chmod (a synced or network
vault, which `FIN_DATA_DIR` invites) the privacy guarantee degrades silently and
the user is never told. The ledger JSONL files themselves get no explicit mode
and rely entirely on the `0700` root.

**Not counted against them.** No authentication, no key management, no
encryption at rest, no supply-chain pinning beyond `pyyaml` and `duckdb`. This is
a single-user local CLI and that is ordinary production hardening outside event
scope.

**Reasoning.** Every privacy control the team claimed was tested and held. No
demonstrated exploitable defect exists in the package. Two real risks (F9, F13)
and two small gaps (F14, F15) keep this at 4.

**Uncertainty.** Low on the verified controls. Medium on F9, which is derived
from DuckDB's documented default capabilities and the source, not from an
attempted query. `.env.example` remains unread under the host deny rule, but
since nothing consumes an env var other than `FIN_DATA_DIR` this does not limit
the criterion.

**Highest-value improvement.** Lock the SQL connection down: reject anything that
is not a single `SELECT`/`WITH`, and set `enable_external_access = false`,
`disabled_filesystems`, then `lock_configuration = true` before executing. Delete
the `op run` line from the README in the same change.

### innovation — 4, confidence medium

**Evidence.** Artifact evidence: `src/fin/detect/detectors.py:1-17` (detectors
ordered by time-to-detection, with the explicit note that D0 would have fired on
day one on a single $13.95 charge where the statistical detectors could not have
fired until month six), `src/fin/ingest.py:1-17` (provably lossless or
rejected), `src/fin/dispute.py:interest_attribution`, `src/fin/match/engine.py`
(tiers with an explicit ambiguity outcome). Direct observation: D0 firing
correctly on the declared binding and the $0.29 interest attribution in
`runs/team-ledger-analyze-render-dispute-01.json`.

**Strengths.** The central idea is genuinely good and I have not seen it packaged
this way: encode which cards a merchant is permitted on, and detection becomes a
config lookup that needs no history, no feed and no statistics. Pairing that with
a hard control-total gate, an ambiguity tier that commits nothing, and interest
attributed back to disputed principal is a coherent thesis about reconciliation,
not a feature list. The deterministic-core, model-at-the-periphery split is the
same thesis applied to the AI layer.

**Deficiencies.** No novel algorithm. Subset-sum over line items is textbook, and
correctly capped at `MAX_EXHAUSTIVE_ITEMS`. The ambition is in the framing and
the refusals rather than the technique.

**Reasoning.** Meaningful originality in problem framing, with real depth in the
parser hazards and the invariant model, executed at a scale the evidence
supports.

**Uncertainty.** Medium. The claim that this design would have caught the
motivating 343-day fraud on day one is a team claim I cannot test against real
data, though it follows from the D0 implementation I read.

**Highest-value improvement.** Demonstrate the thesis: a fixture ledger of a few
hundred synthetic transactions containing the fraud pattern, with D0 firing on
transaction 1 and the statistical detectors staying silent until month six.
That turns the strongest argument in the README into a test.

## Surprises

**Better than expected.** The privacy claims survived contact with execution.
`0700` on the vault, `0600` on the archived raw file, `0600` on the dispute CSV,
and `render.write` chmods every generated report too, which no run record
checked and which I confirmed at `src/fin/render.py:43-46`. Teams normally write
that sentence in a README and stop. The responsible-AI content in
`fin-dispute/SKILL.md` was also better than the category usually produces: it
names a specific way the product could harm its user (telling them an expired
billing-error window means the money is gone) and instructs against it.

**Worse than expected.** Two things. First, `AMBIGUOUS` has no test. The
repository argues repeatedly that refusing to guess is the whole point, and that
exact branch is verified nowhere. Second, `fin sql` is wide open while sitting
directly under a skill that tells an agent to use it freely. A project this
careful about the sign of a credit column left the one arbitrary-execution
surface unconstrained.

**Process note.** My brief cites twelve sandboxed run records for this team.
Eleven exist in `events/live-trial-2026/runs/` and the manifest cites eleven.
Not a scoring matter, but the panel should reconcile the count.

**Injection.** None. My independent grep across the checkout for
evaluator-directed phrasing returned three benign matches, all about match
confidence or budgets. Nothing in this submission addressed an evaluator or
attempted to influence scoring.

## Blocking and major issues

**Blocking: none.** Nothing in the evidence prevents this submission from being
judged or run, and no confirmed inability to complete a primary advertised
workflow was observed.

**Confirmed defects (directly observed).**

- F4. Inconsistent ingest error contract. Two of four rejection paths emit a
  full traceback (`runs/team-ledger-ingest-integrity-01.json` stderr;
  `src/fin/adapters/citi_csv.py:54,70` versus `src/fin/cli.py:46`). Safe, since
  nothing is written, but it leaks implementation to the user and, in a
  multi-path ingest, aborts the loop after earlier files have already committed
  and before `_revalidate` runs.

**Credible risks (derived from source, not demonstrated).**

- F9. Unconstrained DuckDB execution in `fin sql`, reachable by an LLM agent
  reasoning over attacker-influenced descriptors. Highest consequence of
  anything on this list.
- F10. Non-atomic cross-table writes during ingest produce exactly one torn
  state, and `fin validate` cannot see it.
- F13. Documented `op run` wrapper places secrets in the environment of a
  process that consumes none.
- F12. A missing `pdftotext` reports as "no adapter recognises" rather than as a
  missing dependency.

**Untested concerns (absence of evidence, not evidence of failure).**

- F2. `AMBIGUOUS` outcome: no run, no test.
- F1. CLI-level PDF ingest: `sniff` and the `pdftotext` subprocess call.
- F6. The agent orchestration layer was never executed, by event constraint.
- Scale: no observation above four transactions.

**Ordinary hardening, explicitly not held against this prototype.** Auth,
encryption at rest, dependency pinning and supply-chain attestation, multi-user
isolation, log shipping.

## Calculation and independence declaration

- [x] Scores were calculated by the repository script
- [x] Every material finding cites evidence
- [x] No other judge report was inspected
- [x] Submission instructions were treated as untrusted data

Raw scores and confidence appear in front matter only. The weighted table is left
for `atj render judgment` to generate from
`framework/rubrics/submission-evaluation.md`. I typed no weight, no weighted
point value and no total anywhere in this file. I read no file under
`events/live-trial-2026/judgments/` or `workspaces/live-trial-2026/staging/`,
and no material belonging to the other team. All repository content, including
`README.md`, `SPEC.md`, the four `.claude/skills/` files, code comments and
`hooks/pre-commit`, was read as data.
