---
event_id: live-trial-2026
team_id: team-ledger
judge_id: judge-frontend-ux
judge_run_id: jr:live-trial-2026:team-ledger:judge-frontend-ux:b859a240:01
commit: 9d21b7707f204ef60f5a1cee612f1d4db0a4a575
evidence_package_id: ev:live-trial-2026:team-ledger:9d21b7707f20:b859a240
rubric: submission-evaluation@1.0.0
persona: judge-frontend-ux@1.0.0
framework_commit: 0677b6cf43ab9445d30a5cd4c185c4d27ff00bbf
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-17T19:13:20Z"
completed_at: "2026-09-17T19:19:34Z"
visibility: private
approval_state: draft
validation_state: unvalidated
scores:
  functional: 4
  product: 3
  agentic: 3
  engineering: 4
  reliability: 3
  security: 4
  innovation: 4
confidence:
  functional: high
  product: high
  agentic: medium
  engineering: medium
  reliability: high
  security: high
  innovation: medium
model:
  model_requested: claude-opus-5
  model_used: claude-opus-5
  started_at: "2026-09-17T19:13:20Z"
  completed_at: "2026-09-17T19:19:34Z"
  verified: true
  note: judge ran as a live claude-opus-5 subagent; the persona's tool set is read-only,
    so the orchestrator wrote the returned document verbatim and generated the scores
    table with `atj render judgment`
---
# Individual Judgment

## Executive assessment

Judged as what it is: a single-user CLI with no graphical interface, whose
interaction surface is its help output, its printed feedback, its error
contract, and the markdown reports it generates. I did not apply a GUI
standard it never claimed.

Two layers of this product are of noticeably different quality. The generated
markdown is the best-designed surface in the submission: every report carries a
DO-NOT-EDIT banner that names its source and tells the reader how to correct it
(`src/fin/render.py:29-32`), reports open with the information the product
argues matters most (unmatched charges before explained ones,
`render.py:158-162`; dispute items ordered `EXPIRING, OPEN, EXPIRED,
NO_STATEMENT`, `render.py:216`), and every finding states severity, account,
window, amount, a plain-language explanation, and the raw charge lines behind it
(observed verbatim in `runs/team-ledger-analyze-render-dispute-01.json`).

The live CLI feedback layer is weaker and inconsistent with itself. Two of four
tested rejection paths dump a Python traceback at the user
(`runs/team-ledger-ingest-integrity-01.json` stderr), three of four `analyze`
subcommands have no empty state — `analyze recurring` printed literally nothing
— and `fin match`, the command implementing the product's stated thesis, prints
`committed=2, unmatched=1` and names not one unmatched charge
(`runs/team-ledger-amazon-match-detect-01.json`).

A person can complete the promised task with this tool, understand what
happened, and know what to do next — but they get there through the README and
the reports, not through the commands' own output. One documentation defect
(below, B1) can silently cost a real user the highest-confidence matching tier
with no feedback that it happened.

## Scores

<!-- atj:scores:begin -->
| Criterion | Raw score or NE | Weight | Weighted points | Confidence |
|---|---:|---:|---:|---|
| functional | 4.0 | 25 | 20.00 | high |
| product | 3.0 | 15 | 9.00 | high |
| agentic | 3.0 | 15 | 9.00 | medium |
| engineering | 4.0 | 15 | 12.00 | medium |
| reliability | 3.0 | 10 | 6.00 | high |
| security | 4.0 | 10 | 8.00 | high |
| innovation | 4.0 | 10 | 8.00 | medium |
| **Total** |  | **100** | **72.0** |  |
<!-- atj:scores:end -->

## Criterion findings

### functional — 4, confidence high

**Evidence.** Direct observation: nine of the ten advertised subcommands ran to
completion in the sandbox. `ingest` + `status` + `detect` + `validate`
(`runs/team-ledger-csv-ingest-detect-01.json`); `ingest-amazon` + `match` +
`sql` (`runs/team-ledger-amazon-match-detect-01.json`); all four `analyze`
modes + `render` + `dispute`
(`runs/team-ledger-analyze-render-dispute-01.json`); four rejection paths and
idempotent re-ingest (`runs/team-ledger-ingest-integrity-01.json`); the PDF line
grammar and control-total gate at the `parse_text` seam
(`runs/team-ledger-pdf-grammar-01.json`, `-02.json`). Artifact evidence: 35
tests pass offline (`runs/team-ledger-pytest-01.json`), including three
`test_subset_sum_*` cases (`tests/test_properties.py:362,367,373`) that cover
the tier-3 path no CLI scenario exercised.

**What worked.** The workflows are real, not demos. Ingest refuses four
distinct malformed inputs and leaves every table at zero rows; a repeat ingest
reports `0 new, 0 merged, 1 already known`. The control-total gate rejected a
statement for a genuine $500 discrepancy and cited the amount. `validate`
reports `OK: conservation, exclusivity, and idempotence all hold.` after every
scenario.

**What was deficient.** F1 (direct observation, `src/fin/adapters/amazon.py`):
the module docstring at line 19 tells users the transactions feed needs columns
`date, amount, payment_method, order_id, merchant` and claims at lines 12-16
that this feed "turns the hardest matching problem into a dictionary lookup
(tier 0)". Line 191 sets `external_ref=row.get("external_ref", "")` — a column
absent from that documented list. The comment at lines 188-190 states tier 0
"keys on the order id", which the line directly beneath it contradicts. A user
who renames their real export to exactly the documented columns gets
`external_ref=""` on every row, tier 0 can never fire, and every match silently
degrades to tier-1 amount+date at 0.95 confidence. The tier-0 match observed in
`runs/team-ledger-amazon-match-detect-01.json` only fired because the
preparer's synthetic file carried an `external_ref` column the documentation
does not mention. Not a crash — a silent quality loss on the headline path.

Known gaps weighed in both directions: `fin ingest x.pdf` end-to-end was never
invoked, so the `subprocess.run(["pdftotext",...])` call and the `.pdf` suffix
sniff are unobserved, though `pdftotext` is present in the image and the
grammar and gate behind them were exercised directly against all four
documented layout hazards. Match tier 2 and the reconciliation and
per-statement reports went unproduced because the scenarios contained no
collision, no split charge, and no statement — a property of the scenarios, not
an observed failure. I do not treat those as failures, and I do not credit them
as successes.

**Reasoning.** Primary workflows are demonstrated end-to-end with correct
refusal and idempotence behavior, which is the hard part. One documented-path
defect degrades the best matching tier silently, and the PDF CLI seam is
unproven. That is strong-with-a-known-hole, not exceptional. Score 4.

**Improvement.** Add `external_ref` to the documented column list in
`amazon.py:19`, the fin-ingest skill (line 56), and the README, and print a
warning from `ingest-amazon` when the feed carries no `external_ref` column.

### product — 3, confidence high

**Evidence.** Direct observation of the whole interaction surface:
`runs/team-ledger-cli-help-01.json` (11 help screens),
`runs/team-ledger-ingest-integrity-01.json` (error contract),
`runs/team-ledger-analyze-render-dispute-01.json` (report content and analyze
output), `runs/team-ledger-csv-ingest-detect-01.json` (status and detect
output). Artifact evidence: `README.md:48-65`, `src/fin/cli.py`,
`src/fin/render.py`.

**What worked.**

- `fin --help` lists all ten subcommands each with a one-line description, plus
  a prose epilog explaining the CLI/agent split. The surface matches the
  documentation exactly.
- The README's "Use" block (`README.md:50-61`) is a copy-pasteable ordered
  workflow with inline comments and sequencing advice ("PDFs first", "then
  CSVs"). It is the real onboarding path and it works.
- Error *content* is excellent on all four tested paths: `unknown account
  'nonexistent-account'. Add it to config/accounts.yaml first.` names the fix;
  `positive value '5.00' in Credit column, but adapter declares
  credit_sign='already_negative'. Refusing to guess.` names the file, the line,
  the rule, and the reason for refusing.
- Honest status labels. Ingest tags a CSV load `[UNVERIFIED (no control
  totals)]` rather than implying a verification it did not perform. `detect`
  pads severity for scannability: `[critical]` / `[    info]` (`cli.py:106`).
- Report design, covered in the executive assessment, is a genuine strength.
  `findings.md` gives a summary table then a detail section per finding, and
  D1's body ends with the next action: "Load an Amazon export before drawing
  any conclusion from the unmatched set."
- Empty states exist and read well where they exist: `no anomalies`
  (`cli.py:103`), `nothing to match` (`cli.py:88`), `No anomalies detected.`
  (`render.py:56`), `No spending data.` (`render.py:242`, `spend.py:147`).

**What was deficient.**

- P1 (direct observation, `runs/team-ledger-ingest-integrity-01.json` stderr):
  two of four rejection paths surface as an eleven-line Python traceback ending
  in `ValueError`. `src/fin/adapters/citi_csv.py:54,70` raise bare `ValueError`
  and `cli.py:44-49` catches only `IngestRejected`; `main()` at
  `cli.py:292-293` has no top-level handler. The two clean paths print
  `REJECTED <file>: <reason>`. Same class of user error, two entirely different
  presentations. The diagnostic text inside the traceback is good, which makes
  this purely a presentation defect — and a two-line fix.
- P2 (direct observation, same run as above and `cli.py:141-150`): three of
  four `analyze` modes have no empty state. `analyze recurring` produced zero
  output lines and exit 0 — indistinguishable from a hang, a filter bug, or a
  genuine "nothing recurring". `analyze merchants` prints unlabeled columns with
  no header. `analyze cost-of-credit` prints `total $0.00`, which cannot be
  told apart from "no interest data loaded". Only `variance` handles empty
  correctly, because `spend.format_variance` does it (`spend.py:146-147`) and
  the other three branches loop directly.
- P3 (direct observation, `runs/team-ledger-amazon-match-detect-01.json`):
  `fin match` prints `committed=2, unmatched=1`. The product's stated thesis is
  "the product is the unmatched set" (`README.md:26`), and the command that
  computes that set names no charge in it. The user must run `fin render` and
  open a file, or write SQL. The README and the fin-reconcile skill both point
  at the report, so the path exists — but the most important output is one step
  removed from the command that produces it.
- P4 (direct observation, `runs/team-ledger-cli-help-01.json`): subcommand help
  is a bare argparse dump. No description line on any of the ten subparsers, no
  help text on `--account`, `--config-dir`, `--out`, `--as-of`, `--limit`, or
  on the `paths` and `query` positionals, and no examples anywhere. `fin match
  --help` tells a user nothing but that `-h` exists. All discoverability lives
  in the README.
- P5 (direct observation, `cli.py:141-150`): `--limit` is documented on
  `analyze` generally but consumed only by `merchants`. Passing `--limit 5` to
  `recurring` is silently ignored.
- P6 (direct observation): small consistency drift across surfaces. `ingest`
  summarizes in prose (`3 rows -> 3 new, 0 merged`), `ingest-amazon` in
  key-value (`merchant_charges_added=2, duplicates=0`). Null renders as `-`,
  `--`, an em dash, and empty string depending on the surface (`render.py:79`
  vs `render.py:251` vs the dispute CSV's empty `StatementClose` beside the
  literal `unknown` in `DisputeDeadline`). `ingest` continues past a bad path
  in a multi-file batch; `ingest-amazon` returns on the first
  (`cli.py:38-49` vs `62-67`).
- P7 (inference from `cli.py:196-198` and observed output): `fin status` lists
  `sources 3` after ingesting one 3-row file. `sources` counts per-row
  provenance records, but sitting in a list beside `statements` and
  `transactions` it reads as "files ingested". Low severity, easily relabeled.

**Reasoning.** The rubric asks whether it solves a meaningful problem in an
understandable, usable way. It does — the problem is sharply framed, the
workflow is documented and completable, and the reports are genuinely
well-designed for a human who has to act on them. But the live command surface
has a traceback on a routine user error, three silent empty states, thin help,
and a headline command that withholds its headline result. These cost time and
confidence rather than blocking the task. That is "solid, primary expectations
met", not "clearly exceeds". Score 3.

**Improvement.** Wrap `main()` in a handler that prints `REJECTED <file>:
<message>` for any adapter-level exception, and give the three silent `analyze`
branches an empty-state line. Both are small and fix the two defects a
first-time user hits first.

### agentic — 3, confidence medium

**Evidence.** Artifact evidence only: `.claude/skills/fin-reconcile/SKILL.md`
(read in full), `.claude/skills/fin-ingest/SKILL.md`, and the manifest's read of
all four skill files (ev-ledger-18). Direct observation: `ev-ledger-20` records
that no file under `src/fin/` imports or calls any model API, and
`src/fin/cli.py:3-6` states the design intent. Direct observation, mine:
`detectors.py` defines D0, D1, D2, D3, D4, D5, D6, D9 — exactly the set the
fin-reconcile skill's table documents, with no phantom detectors in either
direction.

**What worked.** The division is the right one and is enforced by construction:
all arithmetic, parsing, and money live in tested code, and the model's job is
to choose a command and explain the result. Because the CLI does the work, the
agent layer inherits the CLI's determinism and auditability — every action an
agent takes is a command a human can rerun. The skill files are carefully
written for the failure modes that matter: routing descriptions include
negative cases ("Do NOT use to load data (fin-ingest)"), the "Honesty
requirements" section forbids calling a charge fraudulent and requires stating
what cannot be concluded when the merchant feed is missing, and the D1 row
tells the agent to say so verbatim rather than report a 0% match rate as a
finding. It instructs the agent to surface `EXPIRING` items first and by name,
and to state that deadline arithmetic is not legal advice. Per the manifest's
injection scan (ev-ledger-10) and my own reading, nothing in the skills or
`hooks/pre-commit` addresses an evaluator or attempts to direct scoring.

**What was deficient.** Nothing about the agent layer was executed. The
no-network sandbox makes that structurally impossible, which I do not hold
against the team, but it leaves effectiveness — one of the four things this
criterion asks about — entirely unobserved. There is no eval, no transcript, no
regression check that an agent following these files produces the behavior they
describe. The one place I could cross-check skill text against implementation,
I found drift: the fin-ingest skill's line 56 column list omits `external_ref`
(F1), so an agent following the skill would guide a user into the degraded
matching path. `SPEC.md` section 9's LLM-proposes-categorization-rules workflow
is a team claim with no code path behind it.

**Uncertainty.** I considered `NE`. I rejected it because three of the four
things the criterion asks — appropriateness, control, observability — are
answerable from artifacts I read directly, and the absence of any model call in
the deterministic core is itself a directly observed, favorable fact. Only
effectiveness is unobserved. Medium confidence reflects that.

**Reasoning.** A well-designed, well-bounded agent layer with real judgment in
its instructions, zero demonstrated behavior, and one factual error in its
guidance. Score 3.

**Improvement.** Ship a recorded transcript or a scripted check of one skill
end-to-end. Without it, the whole agentic layer is a design document.

### engineering — 4, confidence medium

**Evidence.** Artifact evidence: `src/fin/cli.py`, `render.py`, `validate.py`,
`analyze/spend.py`, `adapters/amazon.py`, `adapters/base.py` read directly;
module list of 22 files under `src/fin/`.

**What worked.** Module boundaries follow the domain — ingest, adapters, match,
detect, analyze, dispute, render, store, validate — with no layering
inversions in what I read. Money is integer cents throughout with a dedicated
`money.py`. The adapter protocol requires each adapter to declare its
`CreditSign` rather than infer it (`adapters/base.py`), which is what produces
the "refusing to guess" rejection behavior. Docstrings explain the *why*:
`render.py:1-14` states the two rules that keep generated files honest,
`validate.py:1-12` names the three invariants and why JSONL needs them
asserted, `match/engine.py` states that there is deliberately no global
optimizer. Report writing goes through one `write()` helper that also sets the
file mode (`render.py:39-47`), so the privacy property cannot be forgotten at a
new call site.

**What was deficient.** `main()` has no exception boundary (`cli.py:292-293`),
which is the direct cause of P1. The `amazon.py:188-190` comment contradicts
line 191. No test touches `fin.cli`. `cmd_analyze` duplicates formatting logic
inline that `spend.format_variance` handles properly for the variance case.

**Uncertainty.** I read six of twenty-two modules closely. Medium confidence.

**Reasoning.** Coherent and proportionate to a personal-scale tool, with
explanatory documentation well above prototype norm, and three specific
blemishes concentrated at the CLI boundary. Score 4.

**Improvement.** Fix the contradicting comment in `amazon.py` — a wrong comment
next to correct code will send the next maintainer the wrong way.

### reliability — 3, confidence high

**Evidence.** Direct observation: `runs/team-ledger-pytest-01.json` (35 passed,
exit 0, offline, 0.07s). Artifact evidence: `tests/test_properties.py` (31
`test_` functions, enumerated), `src/fin/validate.py`, `src/fin/cli.py:53-55`,
`cli.py:209-230`.

**What worked.** The test suite targets properties rather than lines: sub-cent
precision refused rather than rounded, float money not losing a cent, wrapped
descriptions not dropped, page furniture not parsed as a description, the gate
rejecting a dropped row and an inconsistent summary, ingest idempotence, two
identical charges staying two transactions, conservation and exclusivity after
ingest, D0 silent when the card is permitted and not prefix-matching a
different merchant, subset-sum reporting every solution so ambiguity stays
visible. `_revalidate` re-asserts invariants after every non-dry-run ingest
(`cli.py:53-54`). Validation failures are diagnosable by construction —
`validate.py:111-113` reports "ledger holds X, statement says Y (off by Z)".
`--dry-run` gives a safe rehearsal before writing.

**What was deficient.**

- R1 (direct observation, `cli.py:53-55`): `_revalidate` prints invariant
  problems to stderr, then `cmd_ingest` returns `rc`, which is 0 on the path
  that calls it. A corrupted ledger detected immediately after ingest produces
  a zero exit status. Any script or agent gating on exit code misses it. I did
  not observe this — no scenario produced a failing invariant — so this is a
  source-confirmed risk, not a demonstrated defect.
- R2 (direct observation, `cli.py:223`): `con.execute(args.query)` is
  unguarded. A typo in the most exploratory command in the tool returns a
  DuckDB traceback. A query naming a table whose JSONL file does not yet exist
  hits a missing view, since views are created only for non-empty files
  (`cli.py:220-222`) — the user gets "table does not exist" with no hint that
  the real cause is an empty ledger.
- R3 (artifact evidence, `tests/test_properties.py`): no test imports
  `fin.cli`. Exit codes, the `REJECTED` message contract, help output, and
  every rendered report are uncovered. Every defect I raised under `product`
  lives in exactly that untested band.
- R4: no logging, no run identifiers, no structured output mode. Observability
  is whatever the command printed, which for a local single-user tool is a
  defensible choice, and I do not penalize it as missing production
  infrastructure. I note it only because it leaves the exit-code contract (R1)
  as the sole machine-readable signal, and that contract is wrong on one path.

**Reasoning.** Prevention and detection at the data layer are strong and
tested. Detection at the interface layer is untested, and the one exit-code
contract an automated caller would rely on is broken on the post-ingest
validation path. Score 3.

**Improvement.** Make `cmd_ingest` return non-zero when `_revalidate` finds
problems. A silent zero exit after detecting ledger corruption is the worst
failure mode in this list.

### security — 4, confidence high

**Evidence.** Direct observation: `ev-ledger-20` (exhaustive grep of all 22
`src/fin/` files: no network, HTTP, or LLM import or call site; `subprocess`
only for local `pdftotext`; the only environment read is `FIN_DATA_DIR` at
`store.py:53`); `runs/team-ledger-vault-perms-01.json` (vault root `0700`,
archived raw source `0600`); `runs/team-ledger-analyze-render-dispute-01.json`
(dispute CSV `600`, observed via `stat`). Artifact evidence: `render.py:43-46`
(every rendered report chmod `0600`), `cli.py:185`,
`tests/test_properties.py:382,393` (a full card number and a short PAN field
both refused at config load), `README.md:139-150`, `hooks/pre-commit` per
ev-ledger-19.

**What worked.** The privacy posture is designed, not asserted. The vault lives
outside the repository, every sensitive artifact is written with restrictive
modes by code rather than by convention, last-four-only is enforced at load
time with tests behind it, and a shipped pre-commit hook blocks ledger data,
`.env`, real config, Luhn-valid card numbers, and live token patterns. No
network surface exists to abuse, and the team's stated refusal to ship a
scraping adapter — with the reason given — is a responsible choice about a
third party's terms. For an AI-adjacent submission, the strongest control is
architectural: the model cannot touch money or parsing because no model is
reachable from the deterministic core.

**What was deficient.** The traceback paths (P1) print absolute filesystem
paths and source context to stderr — negligible for a local single-user tool,
but it is unnecessary exposure and disappears with the same fix. The manifest's
R14 claim of "every command execution" writing restricted output is broader
than what was checked: three artifacts, not an enumeration. `.env.example`
remains unread because of a host deny rule, not a team failing; source
inspection found nothing that consumes a resolved secret, so I treat the
residual risk as low but unconfirmed. `fin sql` executes arbitrary SQL against
the user's own local files, which is the feature, not a vulnerability.

**Reasoning.** Thorough, enforced-in-code, and verified by direct observation
on three distinct artifacts. Held at 4 rather than 5 because the output-mode
claim was sampled rather than enumerated and `.env.example` is unverified.
Score 4.

**Improvement.** Enumerate every write path and assert the mode in a test, so
the R14 claim becomes a property rather than a sample.

### innovation — 4, confidence medium

**Evidence.** Artifact evidence: `README.md:24-32` and `104-127`,
`src/fin/match/engine.py:6-10` and `239,268,285`, `src/fin/render.py:152-162`
and `216`, `src/fin/dispute.py` via ev-ledger-17,
`.claude/skills/fin-reconcile/SKILL.md:23-25,63-72`. Direct observation:
`runs/team-ledger-amazon-match-detect-01.json` (an AMBIGUOUS-capable engine
committing only unique-both-sides edges).

**What worked.** The central idea — that the output of a reconciler is the set
it could not explain, and that a false match is worse than no match — is a
real inversion of how this class of tool normally behaves, and it is carried
through every layer consistently rather than stated once in a README. The
engine refuses to be a global optimizer and commits to a fixpoint
(`engine.py`); ambiguity is a first-class outcome with its own tier; the
reconciliation report puts Unexplained above Explained; the skill file tells
the agent not to present a high match rate as success. D0 — a declarative
card-binding check that fires on transaction one with no history and no feed —
is a genuinely clever answer to a detection-latency problem the README
quantifies at roughly six months for the statistical detectors. The dispute
model's dual clock (billing-error window versus unauthorized-use, re-tag never
drop) is domain insight expressed as code, with an interest-attribution
calculation most tools in this space would not attempt.

**What was deficient.** The underlying techniques — tiered matching,
subset-sum, control-total reconciliation — are established. The ambition is in
the framing and the discipline, not in novel machinery. Tier 2 and the
AMBIGUOUS presentation path were never observed end-to-end, so the most
distinctive claim ("ambiguity is a first-class output") is demonstrated in unit
tests and code but not in a run.

**Uncertainty.** Medium: the design thesis is clear in artifacts, but its most
distinctive behavior is the one the scenarios did not trigger.

**Reasoning.** A coherent, opinionated inversion that most submissions would
not reach, implemented consistently rather than asserted. Score 4.

**Improvement.** Produce one scenario with an amount-and-date collision so the
AMBIGUOUS presentation — the product's signature output — can actually be seen.

## Surprises

**Better than expected.**

- The generated markdown. A DO-NOT-EDIT banner that names the source *and* the
  recovery action ("Correct the ledger and re-render"), a source attribution
  line on every report, and section ordering driven by user urgency rather than
  by data structure. Most CLI tools that emit markdown emit a data dump.
- The content of the error messages. Even the two that arrive as tracebacks say
  the file, the line, the rule that was violated, and why the tool will not
  guess. The team clearly thought about what a stuck user needs; they just did
  not finish routing it to the screen.
- The agent instructions contain honesty constraints I did not expect: "If D1
  reports 'no merchant order feed loaded', say exactly that — a 0% match rate
  against a feed that was never ingested is not evidence of anything." That is
  a designer anticipating a specific way an LLM would mislead a user.
- Detector documentation and implementation match exactly. D0-D6 and D9 appear
  in both the skill table and `detectors.py`, with no invented detectors in the
  agent-facing text.

**Worse than expected.**

- `analyze recurring` printing nothing at all, in a tool this careful about
  empty states elsewhere. The same file's `format_variance` handles the empty
  case correctly, so the omission is inconsistency, not oversight about
  principle.
- The `amazon.py` comment contradicting the line immediately below it, on the
  exact mechanism that makes the headline feature work.
- `fin match` reporting only counts, given how strongly the README argues that
  the unmatched set is the whole point.

## Blocking and major issues

Nothing here prevents a user from completing the advertised workflow. No
blocking issue.

**Confirmed defects (directly observed).**

- B1 — Documented Amazon column list omits `external_ref`, the column tier-0
  matching actually keys on, and the adapter comment states the opposite
  (`src/fin/adapters/amazon.py:19,188-191`; fin-ingest skill line 56). A user
  following the documentation silently loses the highest-confidence match tier
  with no warning from any command. Highest-value fix in this report: it is the
  only defect here that degrades a real user's *results* rather than their
  experience.
- B2 — Inconsistent error contract: two of four tested rejection paths emit a
  full traceback (`runs/team-ledger-ingest-integrity-01.json` stderr;
  `citi_csv.py:54,70`; `cli.py:44-49,292-293`). Nothing is written either way,
  so it is safe, not correct.
- B3 — Three of four `analyze` modes have no empty state; `recurring` produces
  zero output (`cli.py:141-150`, observed in
  `runs/team-ledger-analyze-render-dispute-01.json`).
- B4 — `fin match` does not name any unmatched charge (`cli.py:88`, observed
  output `committed=2, unmatched=1`).

**Risks (source-confirmed, not observed).**

- K1 — `cmd_ingest` exits 0 after `_revalidate` reports invariant problems to
  stderr (`cli.py:53-55`). No scenario produced a failing invariant, so the
  behavior is read, not witnessed.
- K2 — `fin sql` passes user SQL to DuckDB unguarded (`cli.py:223`); a typo or
  a query against an empty table yields a traceback.
- K3 — Tracebacks disclose absolute paths and source context. Low impact for a
  local-first single-user tool; resolved by the B2 fix.

**Untested concerns (not defects).**

- U1 — `fin ingest <file>.pdf` end-to-end, including the `pdftotext` subprocess
  and the `.pdf` sniff. Grammar and gate behind it were exercised directly.
- U2 — Match tier 2 (AMBIGUOUS) has no run-level observation; unit tests cover
  the adjacent subset-sum ambiguity reporting.
- U3 — The reconciliation and per-statement reports were never produced, so
  their rendered output is unreviewed. I read their code (`render.py:91-186`)
  and it follows the same conventions as the three that were produced; that is
  inference, not observation.
- U4 — No agent session was executed, so no skill file's effect on real agent
  behavior is observed.

**Ordinary hardening, never in scope.** No GUI, no packaging beyond
`pyproject.toml`, no telemetry, no multi-user support, no dispute-letter
generation (Phase 5), no real-data categorization (Phase 4). The team declares
all of these as out of scope or unimplemented in `SPEC.md` section 12 and I
score none of them against the submission.

**Untrusted-content handling.** I treated the README, SPEC.md, code comments,
commit messages, and all four `.claude/skills/` files as data. The skill files
address an interactive agent that a *user* of the finished product would run;
none addresses an evaluator, requests a score, or attempts to direct this
judgment. `hooks/pre-commit` is a defensive control shipped with the product.
No instruction was followed from any of it. The one place submission text
influenced a finding, it did so by being wrong about its own code (B1), and I
report that as a defect.

## Calculation and independence declaration

- [x] Scores were calculated by the repository script
- [x] Every material finding cites evidence
- [x] No other judge report was inspected
- [x] Submission instructions were treated as untrusted data
