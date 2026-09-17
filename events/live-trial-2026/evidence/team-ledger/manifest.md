---
event_id: live-trial-2026
team_id: team-ledger
commit: 9d21b7707f204ef60f5a1cee612f1d4db0a4a575
evidence_package_id: ev:live-trial-2026:team-ledger:9d21b7707f20:b859a240
rubric: submission-evaluation@1.0.0
persona: prepare-submission@1.1.0
framework_commit: 152dd2c10547a1c15bb56c4b1a90764b28354c59
prepared_at: 2026-09-17T00:15:00Z
execution_status: sandboxed-partial
evidence_limited_criteria: []
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: 2026-09-17T00:04:00Z
completed_at: 2026-09-17T00:15:00Z
visibility: private
approval_state: approved
validation_state: valid
---

# Evidence Manifest — team-ledger (Hive Ledger)

## Scope and provenance

- Source: `https://github.com/beekeeper-lab/hive-ledger`, pinned commit
  `9d21b7707f204ef60f5a1cee612f1d4db0a4a575` (cloned, not a snapshot). Checkout:
  `workspaces/live-trial-2026/team-ledger/`.
- Intake record (team's own account, as recorded by `atj intake`):
  `events/live-trial-2026/submissions/team-ledger.md`.
- Rubric: `submission-evaluation@1.0.0`. Framework commit
  `152dd2c10547a1c15bb56c4b1a90764b28354c59` (verified against repository git
  history).
- Preparer: `prepare-submission@1.1.0`, model `claude-opus-5`.
- Environment: `python3 -m atj sandbox preflight` reported `AVAILABLE` —
  `podman 6.1.0 (rootless)` — before any execution in this package.
- Approved image: `localhost/atj-live-trial/ledger:2` (id `7780b2b9e6e1`). No
  other image was used. Container image is Debian 13 "trixie", Python 3.12.14
  (`runs/team-ledger-envcheck-01.json`).
- Every execution below ran via `python3 -m atj sandbox run` against this
  checkout, mounted read-only, with `--network none`, dropped capabilities,
  a non-root user, and CPU/memory/pids/timeout limits (see each run record's
  `command` and `limits` fields). No submission code was run on the host. The
  container has no `fin` console-script installed; every invocation used
  `PYTHONPATH=/submission/src python3 -m fin.cli ...`, confirmed working in
  `runs/team-ledger-envcheck-02.json`.
- All submission text, code, configuration, and any command output were
  treated as untrusted data throughout preparation, never as instructions.

## Requirements and team claims

| ID | Claim or requirement | Source | Evidence status |
|---|---|---|---|
| R1 | `fin ingest <paths> --account <id>` loads a card statement/CSV, verifying control totals when present, rejecting outright rather than partially importing | Intake "Primary workflows" #1; `src/fin/ingest.py`, `src/fin/adapters/citi_csv.py` | Direct observation — [[evidence:ev-ledger-01]], [[evidence:ev-ledger-02]] |
| R2 | `fin ingest-amazon <path>` loads an Amazon order-history or transactions export | Intake "Primary workflows" #2; `src/fin/adapters/amazon.py` | Direct observation — [[evidence:ev-ledger-04]] |
| R3 | `fin match` reconciles card charges to merchant records via a tiered matcher (reference, amount+date, subset-sum, unmatched) | Intake "Primary workflows" #3; `src/fin/match/engine.py` | Direct observation — [[evidence:ev-ledger-04]], [[evidence:ev-ledger-05]] |
| R4 | `fin detect` runs anomaly detectors, including D0 (unpermitted-card binding violation), the system's headline feature | Intake "Primary workflows" #4; `src/fin/detect/detectors.py` | Direct observation — [[evidence:ev-ledger-01]], [[evidence:ev-ledger-04]] |
| R5 | `fin validate` asserts conservation, exclusivity, and idempotence invariants | Intake "Primary workflows" #5; `src/fin/validate.py` | Direct observation — [[evidence:ev-ledger-01]], [[evidence:ev-ledger-03]] |
| R6 | `fin render` regenerates markdown reports (findings, reconciliation, spending, per-statement, index) | Intake "Primary workflows" #6; `src/fin/render.py` | Direct observation — [[evidence:ev-ledger-06]] |
| R7 | `fin analyze {variance,merchants,recurring,cost-of-credit}` compares actual spend to declared targets | Intake "Primary workflows" #7; `src/fin/analyze/spend.py` | Direct observation — [[evidence:ev-ledger-06]] |
| R8 | `fin dispute` builds a CSV + markdown dispute packet with billing-error/unauthorized-use deadlines and interest attribution | Intake "Primary workflows" #8; `src/fin/dispute.py` | Direct observation — [[evidence:ev-ledger-06]], [[evidence:ev-ledger-07]] |
| R9 | `fin sql "<query>"` runs ad hoc DuckDB queries over the JSONL ledger | Intake "Primary workflows" #9; `src/fin/cli.py:cmd_sql` | Direct observation — [[evidence:ev-ledger-04]] |
| R10 | `fin status` summarizes vault contents | Intake "Primary workflows" #10 | Direct observation — [[evidence:ev-ledger-01]], [[evidence:ev-ledger-03]] |
| R11 | PDF ingest (`citi_pdf.py`) is the authoritative source: only it carries control totals and a close date; parsing must survive wrapped descriptions, page furniture, and a rewards-column bleed, and must reject a statement whose own arithmetic doesn't close | README/SPEC via intake; `src/fin/adapters/citi_pdf.py` | Direct observation, partial — [[evidence:ev-ledger-08]], [[evidence:ev-ledger-09]]. The parsing grammar itself (`parse_text`) was exercised directly with synthetic layout text reproducing the documented hazards; the outer CLI path (`fin ingest x.pdf` → `subprocess.run(["pdftotext","-layout",...])` on a real PDF file) was not exercised — see Missing evidence. |
| R12 | The deterministic `fin` package makes no network, HTTP, or LLM API calls; the only AI-facing surface is the four `.claude/skills/` files, which are instructions for an interactively-run agent, not executable integrations | Intake "AI and external services"; skill files read directly in this preparation | Direct observation — [[evidence:ev-ledger-10]] |
| R13 | The `fin-ingest` skill (and README) state that Amazon's "Your Transactions" export publishes charge → order id → card, "which is what makes tier-0 matching ... possible" | `.claude/skills/fin-ingest/SKILL.md`; README | Direct observation contradicts this framing in one respect — [[evidence:ev-ledger-05]]: tier-0 (`REFERENCE`) keys on a literal `external_ref` CSV column, not on `order_id`; `order_id` is required only to *sniff* the file as the transactions feed. A feed with `order_id` populated but no `external_ref` column falls through to tier-1 (amount+date), not tier-0. |
| R14 | Every command execution writes secrets/PII-bearing output (dispute CSV, archived raw source files) with restrictive permissions; the vault directory is `0700` | README ("vault ... created ... at mode 0700"); `src/fin/store.py` | Direct observation — [[evidence:ev-ledger-11]] |
| R15 | Phase 4 (real-behavior categorization) and Phase 5 (dispute letter generation) are not implemented; the Amazon adapter has never been exercised against real (non-synthetic) data; multi-account households are unhandled | SPEC.md §12 "Outstanding", via intake | Team claim, not independently demonstrable from this checkout (there is no real data to test against by design — see intake "Known limitations") |
| R16 | `.env` holds only 1Password `op://` references, resolved by `op run`; no code path in `src/fin/` consumes a resolved secret | README, via intake; independent grep in this preparation | Team claim for the `.env` purpose; direct observation (repeat grep) confirms no `os.environ` read other than `FIN_DATA_DIR` |

## Direct observations

| Evidence ID | Observation | Artifact or source reference | Reproduction | Confidence |
|---|---|---|---|---|
| ev-ledger-01 | `fin --help` and all 9 subcommand `--help` screens match the documented CLI surface exactly (`ingest`, `ingest-amazon`, `match`, `detect`, `validate`, `render`, `analyze`, `dispute`, `status`, `sql`) | `src/fin/cli.py` | `runs/team-ledger-cli-help-01.json` | High |
| ev-ledger-02 | A synthetic 3-row Citi CSV statement ingests cleanly (`3 new, 0 merged`), reports itself `UNVERIFIED (no control totals)` per the CSV adapter's documented weaker guarantee, and `fin status`/`fin validate` reflect it correctly | `src/fin/adapters/citi_csv.py`, `src/fin/ingest.py` | `runs/team-ledger-csv-ingest-detect-01.json` | High |
| ev-ledger-03 | D0 fires exactly as the intake record predicted: an AMAZON-family charge on `citi-costco-4021` (the only account declared) is flagged critical because `config/bindings.example.yaml` permits AMAZON only on `amex-blue-1005`. Detail text cites the specific charges, dates, and net amount ($15.68 = $20.68 charge − $5.00 refund). `fin validate` reports all invariants hold afterward | `src/fin/detect/detectors.py:d0_binding_violation` | `runs/team-ledger-csv-ingest-detect-01.json` | High |
| ev-ledger-04 | Ingest correctly refuses and writes nothing for: both Debit and Credit populated on one row; a positive value in the Credit column (adapter declares `credit_sign=already_negative` and refuses to guess); an unrecognized file extension (`no adapter recognises ...`); and an unknown account id. After all four rejected attempts, `fin status` shows zero rows in every table — no partial import. A subsequent valid ingest, then a second identical ingest, shows `0 new, ... 1 already known` — idempotent re-ingest confirmed | `src/fin/ingest.py:ingest_card_file`, `src/fin/adapters/citi_csv.py` | `runs/team-ledger-ingest-integrity-01.json` | High |
| ev-ledger-05 | Of the four rejection paths in ev-ledger-04, two (malformed extension, unknown account) are caught as `IngestRejected` and print a clean one-line `REJECTED <file>: <reason>` to stderr with exit code 1. The other two (both Debit/Credit populated; positive value in Credit column) are raised as bare `ValueError` inside the CSV adapter, are **not** caught anywhere in `cmd_ingest`, and surface as a full Python traceback to stderr (still exit 1, still nothing written). Functionally safe (nothing is imported either way) but an inconsistent user-facing error contract — a real judgment-relevant reliability/engineering gap, not a hypothetical one | `src/fin/adapters/citi_csv.py:54,70` (raises), `src/fin/cli.py:cmd_ingest` (only catches `IngestRejected`) | `runs/team-ledger-ingest-integrity-01.json` (stderr) | High |
| ev-ledger-06 | Ingesting an Amazon "Your Transactions"-shaped CSV (`date,amount,payment_method,order_id,merchant,external_ref`) alongside 3 AMAZON-family card charges produces: 1 tier-0 `REFERENCE` match (confidence 1.0, via the shared `external_ref` token), 1 tier-1 `AMOUNT_DATE_UNIQUE` match (confidence 0.95, dates 1 day apart), and 1 `UNMATCHED`. `fin detect` then reports D0 (3 unpermitted-card charges) and D1 (1 of 3 merchant-feed charges unexplained), matching the matcher's own output exactly. `fin validate` passes | `src/fin/match/engine.py`, `src/fin/detect/detectors.py:d1_unmatched` | `runs/team-ledger-amazon-match-detect-01.json` | High |
| ev-ledger-07 | `fin analyze variance/merchants/recurring/cost-of-credit` all run and produce sensible output against `config/targets.example.yaml`/`categories.example.yaml`; `fin render` writes 3 markdown reports (`README.md`, `findings.md`, `spending.md`) whose content matches the ledger exactly (D0/D1 findings reproduced verbatim in `findings.md`); `fin dispute --detector D0` builds a 2-row CSV and a markdown packet, correctly computes `NO_STATEMENT` state (no statement was ingested in this scenario) and $0.29 of interest attributable to the disputed principal at the account's declared 22.49% APR. The dispute CSV is written with file mode `0600` | `src/fin/render.py`, `src/fin/analyze/spend.py`, `src/fin/dispute.py` | `runs/team-ledger-analyze-render-dispute-01.json` | High |
| ev-ledger-08 | Feeding the PDF adapter's `parse_text` (the seam the team's own code comment says exists "so the line grammar can be tested against synthetic fixtures") an unbalanced synthetic statement — payments declared in the summary block ($500.00) with no matching payment transaction row — correctly parses 3 rows (including a wrapped two-line description, a page-furniture-interrupted purchase row, a rewards-column-bleed row, and a single-date interest row) and then correctly **rejects** the statement via `check_control_totals` for the missing $500.00 payment, citing the exact discrepancy | `src/fin/adapters/citi_pdf.py:parse_text`, `src/fin/ingest.py:check_control_totals` | `runs/team-ledger-pdf-grammar-01.json` | High |
| ev-ledger-09 | The same grammar, fed a balanced synthetic statement with all four documented hazards present (wrapped merchant name across 3 lines, page furniture `402100`/`Page 1 of 2` between rows, a `1.2X` rewards fragment bleeding in after the real `$232.43` token, and a single-date interest row), parses exactly 4 correctly-classified rows (payment, refund, purchase, interest) and passes `check_control_totals` cleanly. `pdftotext` itself is confirmed present at `/usr/bin/pdftotext` in the approved image | `src/fin/adapters/citi_pdf.py` | `runs/team-ledger-pdf-grammar-02.json`, `runs/team-ledger-envcheck-01.json` | High |
| ev-ledger-10 | Independent grep across `.claude/skills/*/SKILL.md` and `hooks/pre-commit`, read as data, for injection phrasing (`ignore previous`, `disregard`, `system prompt`, `jailbreak`, `you are now`, `override ... rule`, etc.) found zero matches, corroborating the intake record's own finding. `hooks/pre-commit` is a defensive tool that blocks committing ledger data, `.env`, real config, and Luhn-valid card numbers or live API tokens — it is not an attempt to direct any evaluator | `.claude/skills/*/SKILL.md`, `hooks/pre-commit` | Static read in this preparation session (no run record; no execution involved) | High |
| ev-ledger-11 | After a valid ingest, the vault root directory (`FIN_DATA_DIR`) is `chmod`'d to `0700` and the archived copy of the source file under `raw/` is `chmod`'d to `0600`, matching the README's stated privacy claim | `src/fin/store.py:Store.__init__`, `Store.archive` | `runs/team-ledger-vault-perms-01.json` | High |
| ev-ledger-12 | Full pytest suite: 35 passed, 0 failed, exit 0, offline, in 0.07s — run before this preparation began | `tests/test_properties.py` | `runs/team-ledger-pytest-01.json` (pre-existing, reused per task instructions) | High |

## Tests and execution

| Command or scenario | Result | Output artifact | Safety controls |
|---|---|---|---|
| `python3 -m pytest -q -p no:cacheprovider` (full suite) | 35 passed, exit 0 | `runs/team-ledger-pytest-01.json` | podman, `--network none`, read-only source mount, non-root, capped CPU/memory/pids/time |
| `which reportlab/fpdf/wkhtmltopdf/...`, python/OS version probe | No PDF-authoring tool present; confirms `pdftotext` present; Python 3.12.14, Debian 13 | `runs/team-ledger-envcheck-01.json` | same |
| `fin --help`; confirm no console-script; `PYTHONPATH=... python3 -m fin.cli --help` | Console script not installed; module invocation works | `runs/team-ledger-envcheck-02.json` | same |
| `fin ingest <synthetic 3-row CSV> --account citi-costco-4021`; `status`; `detect`; `validate` | Ingest succeeds unverified; D0 + D1(info) fire; validate OK | `runs/team-ledger-csv-ingest-detect-01.json` | same |
| 4 deliberate malformed/invalid `fin ingest` attempts, then valid ingest + duplicate re-ingest | All 4 rejected, nothing written; valid ingest then idempotent re-ingest confirmed | `runs/team-ledger-ingest-integrity-01.json` | same |
| `fin ingest` (3 AMAZON-family charges) + `fin ingest-amazon` (2 synthetic transactions, one with `external_ref`, one without) + `fin match` + `fin sql` + `fin detect` + `fin validate` | tier-0/tier-1 matches as expected; D0 + D1 fire; validate OK | `runs/team-ledger-amazon-match-detect-01.json` | same |
| `fin ingest` (4-row mixed statement) + `fin detect` + `fin analyze {variance,merchants,recurring,cost-of-credit}` + `fin render` + `fin dispute --detector D0` | All commands succeed; reports and dispute packet content verified; CSV file mode 0600 | `runs/team-ledger-analyze-render-dispute-01.json` | same |
| `CitiPdfAdapter().parse_text(...)` on an unbalanced synthetic statement, then `check_control_totals` | Parses correctly; gate rejects for a genuine $500 discrepancy | `runs/team-ledger-pdf-grammar-01.json` | same (no subprocess/network; pure Python import) |
| `CitiPdfAdapter().parse_text(...)` on a balanced synthetic statement with all 4 documented parsing hazards, then `check_control_totals` | Parses correctly; gate passes | `runs/team-ledger-pdf-grammar-02.json` | same |
| `fin ingest` then `stat` the vault root and archived raw file | `0700` / `0600` respectively | `runs/team-ledger-vault-perms-01.json` | same |
| All 9 `fin <subcommand> --help` plus `fin --help` | Matches documented CLI surface | `runs/team-ledger-cli-help-01.json` | same |

## Relevant implementation evidence

| Evidence ID | Path/symbol | Relevance |
|---|---|---|
| ev-ledger-13 | `src/fin/adapters/base.py:Adapter`, `CreditSign` | Explicit sign-convention protocol every adapter must declare; the loader asserts rather than infers it — the design principle behind ev-ledger-04/05's refusal behavior |
| ev-ledger-14 | `src/fin/detect/detectors.py:d0_binding_violation` (lines ~55–90) | The D0 detector implementation exercised in ev-ledger-03/06; matches config declaratively, no history required |
| ev-ledger-15 | `src/fin/match/engine.py:build_edges`, `resolve` | Tier system and fixpoint commit logic exercised in ev-ledger-06; deliberately not a global optimizer (own docstring) |
| ev-ledger-16 | `src/fin/adapters/amazon.py:AmazonTransactionsAdapter.parse` (external_ref sourced from a literal CSV column, not `order_id`) | Basis for R13/ev-ledger-05's documentation-vs-implementation discrepancy finding |
| ev-ledger-17 | `src/fin/dispute.py:build`, `interest_attribution` | Billing-error vs unauthorized-use claim typing and APR-based interest attribution exercised in ev-ledger-07 |
| ev-ledger-18 | `.claude/skills/fin-ingest/SKILL.md`, `fin-reconcile`, `fin-analyze`, `fin-dispute` (98/84/85/71 lines) | The full agentic surface: each skill instructs an interactive agent to call specific `fin` subcommands and explain results, never to parse or compute itself — read as data in this preparation, not executed (no network in sandbox) |
| ev-ledger-19 | `hooks/pre-commit` (42 lines) | Defensive pre-commit scan for ledger data, `.env`, real config, Luhn-valid PANs, and live API token patterns — a genuine safety control shipped with the product, not an injection attempt |

## Missing or inaccessible evidence

- **Full CLI-level PDF ingestion is not exercised end-to-end.** The approved
  image has no PDF-authoring tool (`reportlab`, `fpdf`, `wkhtmltopdf`,
  `weasyprint`, etc. all absent — `runs/team-ledger-envcheck-01.json`), so no
  realistic fixture PDF could be constructed inside the offline, no-network
  sandbox, and `fin ingest <file>.pdf` was never invoked. Instead, the parsing
  grammar (`CitiPdfAdapter.parse_text`) was exercised directly against
  synthetic layout text reproducing every hazard the adapter's own docstring
  names (ev-ledger-08, ev-ledger-09), and the `pdftotext` binary the CLI path
  shells out to was confirmed present. This limits confidence specifically in
  the `subprocess.run(["pdftotext","-layout",...])` call itself and in the
  `.pdf`-suffix `sniff()` check, not in the parsing/validation logic those
  wrap. This is why `execution_status` is `sandboxed-partial` rather than
  `sandboxed-complete`.
- **The `.claude/skills/` agent-orchestration layer cannot be exercised live.**
  It presumes an interactive AI agent driving `fin`; under the event's
  no-network sandbox there is no way to run that agent loop. The four skill
  files were read as static evidence (ev-ledger-18) but the described
  behavior (an agent picking commands, reading `fin`'s output, and explaining
  it) is not independently demonstrated.
- **`.env.example`'s exact variable list is unverified.** A host-level deny
  rule blocks reading any `.env*` file under `workspaces/` in this repository
  (carried forward from the intake record). Source inspection (this
  preparation's own grep, ev-ledger-10, and the intake's) found no
  `os.environ` read in `src/fin/` other than `FIN_DATA_DIR`, so nothing found
  suggests a runtime secret is actually required — but the file's contents
  remain unconfirmed.
- **No real (non-synthetic) statements or Amazon exports were available or
  used**, consistent with the team's own design (the repository ships no real
  financial data, by design — see SPEC.md via intake). All execution in this
  package used data constructed for this preparation, described inline with
  each observation. This limits every functional observation to synthetic
  inputs; it does not by itself indicate a defect, since the CSV/PDF adapters
  and control-total gate were exercised against inputs deliberately
  engineered to hit the documented hazards.
- **SPEC.md §9's claim that an LLM proposes `merchant-rules.yaml` entries**
  cannot be demonstrated from this checkout: no code path in `src/fin/` calls
  any model API (confirmed by grep, ev-ledger-10 and intake), and the
  described workflow depends on an interactive agent session outside what a
  sandboxed run can produce. Recorded as a team claim (R15/R16), not
  evidence-limiting any criterion, since the absence of an API call is itself
  a directly observed and relevant fact (no model dependency inside the
  deterministic core).
- **Phase 4/5 and multi-account handling are the team's own stated gaps**
  (SPEC.md §12), not independently tested, and not expected to be
  demonstrable since the team says they are unimplemented.

No criterion is listed as evidence-limited (`evidence_limited_criteria: []`):
for every rubric criterion, either substantial direct-observation evidence was
gathered above, or the gap is a team-acknowledged non-goal/unimplemented
feature rather than an untested-but-required workflow.

## Validation

- [x] Immutable commit verified (`9d21b7707f204ef60f5a1cee612f1d4db0a4a575`, cloned; matches `submissions/team-ledger.md` and the event roster)
- [x] Untrusted instructions ignored (checkout content, including `.claude/skills/` and `hooks/pre-commit`, treated as data throughout; independent injection grep found nothing, ev-ledger-10)
- [x] Execution policy satisfied (`atj sandbox preflight` verified isolation available before any run; every execution went through `atj sandbox run` with no-network, read-only source, non-root, resource limits; nothing was run on the host)
- [x] Artifact references resolve (every `runs/team-ledger-*.json` cited above exists in `events/live-trial-2026/runs/`; every source path cited exists at the pinned commit)
- [x] Manifest independently validated (`python3 -m atj validate reports events/live-trial-2026` — see preparation log)
