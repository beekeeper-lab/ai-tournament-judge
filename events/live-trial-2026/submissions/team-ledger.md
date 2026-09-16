---
event_id: live-trial-2026
team_id: team-ledger
repository: https://github.com/beekeeper-lab/hive-ledger
commit: 9d21b7707f204ef60f5a1cee612f1d4db0a4a575
rubric: submission-evaluation@1.0.0
persona: prepare-submission@1.1.0
framework_commit: 152dd2c10547a1c15bb56c4b1a90764b28354c59
submitted_at: "2026-09-16T23:29:24Z"
started_at: "2026-09-16T23:29:24Z"
completed_at: "2026-09-16T23:29:24Z"
model_requested: not-applicable
model_used: not-applicable
eligible: true
visibility: private
approval_state: draft
validation_state: unvalidated
---
# Submission Intake — Hive Ledger

`atj intake` materialized this submission and pinned it. The sections below are the team's own account of what they built; the tool does not supply them.

## Team statement

`README.md` states the application is "a local-first personal transaction
ledger, reconciler, and anomaly detector": it loads credit-card statements and
merchant exports, proves the load was lossless, reconciles card charges
against what the merchant says was actually bought, and reports what it
cannot explain, alongside a second function comparing actual spend against
declared targets.

`README.md` and `SPEC.md` state the motivating problem was 201 unauthorized
Amazon charges (README: "$3,258.51 gross, $3,232.52 net") that ran for 343
days on a card that should never have carried an Amazon charge, and that
Amazon's own shipment-level billing (one order splitting into several charges,
under opaque descriptors, offset by days, with refunds landing later under a
different descriptor) makes manual reconciliation impractical. `README.md`
states the design principle as: "The product is not the matched set. The
product is the unmatched set," on the grounds that a false match is worse
than no match because it hides a bad charge in the "explained" pile.

The intended audience, per the README and `SPEC.md` §1, is a single individual
managing their own card statements and Amazon orders locally — `SPEC.md`
explicitly scopes this to "a local-first personal money system" and lists
non-goals including forecasting, tax preparation, automatic dispute filing,
and multi-user/multi-account households (SPEC.md §12, "Outstanding").

Direct observation: the source layout (`src/fin/ingest.py`, `src/fin/match/`,
`src/fin/detect/`, `src/fin/dispute.py`, `src/fin/analyze/`) matches this
stated shape — separate modules for loading, reconciling, flagging anomalies,
building dispute packets, and spend analysis.

What a judge should test, per the team's own framing: whether ingest genuinely
refuses a statement it cannot losslessly reproduce, whether the matcher
correctly declines to guess on ambiguous charges rather than forcing a match,
and whether the D0 unpermitted-card detector and dispute-window logic behave
as documented. This is inference from the emphasis of the README/SPEC, not a
team-supplied test plan — no separate test plan document was found in the
repository.

## Primary workflows

Direct observation: the `fin` console-script entry point (`pyproject.toml`
`[project.scripts]`, `fin = "fin.cli:main"`) dispatches to subcommands defined
in `src/fin/cli.py`. The main flows a judge can exercise, in the order the
README's "Use" section and the CLI's own subparsers present them:

1. **Ingest a card statement or CSV export** — `fin ingest <paths> --account
   <id>` (`src/fin/cli.py:36` `cmd_ingest`, backed by `src/fin/ingest.py` and
   the adapters in `src/fin/adapters/citi_pdf.py` and
   `src/fin/adapters/citi_csv.py`). Parses the file, checks it against the
   statement's own control totals, and either commits it or rejects it
   outright (`IngestRejected`, no partial import).
2. **Ingest an Amazon order/transaction export** — `fin ingest-amazon <path>`
   (`src/fin/cli.py:58` `cmd_ingest_amazon`, `src/fin/adapters/amazon.py`),
   optionally `--synthesize-charges` to derive provisional charges from order
   totals when no Amazon transactions feed exists.
3. **Reconcile charges to merchant records** — `fin match` (`src/fin/cli.py:73`
   `cmd_match`, `src/fin/match/engine.py`), running the tiered matcher
   (reference match, unique-amount-and-date match, ambiguous, subset-sum,
   unmatched) described in README "Design" and SPEC.md §7.
4. **Run anomaly detectors** — `fin detect` (`src/fin/cli.py:88` `cmd_detect`,
   `src/fin/detect/detectors.py`), producing detector findings such as D0
   (merchant on an unpermitted card, per `config/bindings.example.yaml`).
5. **Validate ledger invariants** — `fin validate` (`src/fin/cli.py:104`
   `cmd_validate`, `src/fin/validate.py`), asserting the conservation,
   exclusivity, and idempotence properties SPEC.md §3 and §5 describe.
6. **Render markdown reports** — `fin render` (`src/fin/cli.py:110`
   `cmd_render`, `src/fin/render.py`), regenerating findings, reconciliation,
   spending, and per-statement reports into the vault's `reports/` directory.
7. **Analyze spend against declared targets** — `fin analyze
   {variance,merchants,recurring,cost-of-credit}` (`src/fin/cli.py:127`
   `cmd_analyze`, `src/fin/analyze/spend.py`), comparing actuals to
   `config/targets.yaml`.
8. **Build a dispute packet** — `fin dispute --detector D0 | --merchant
   <name> --account <id>` (`src/fin/cli.py:152` `cmd_dispute`,
   `src/fin/dispute.py`), producing a CSV and markdown packet with per-charge
   provenance and billing-error/unauthorized-use deadlines.
9. **Ad hoc query** — `fin sql "<query>"` (`src/fin/cli.py:213` `cmd_sql`),
   running DuckDB directly over the JSONL ledger tables.
10. **Status summary** — `fin status` (`src/fin/cli.py:194` `cmd_status`),
    a row-count and date-range summary of the vault.

Direct observation: `README.md` also documents four Claude Code skills under
`.claude/skills/` (`fin-ingest`, `fin-reconcile`, `fin-analyze`, `fin-dispute`)
that are meant to orchestrate these same CLI commands rather than parse files
or compute values themselves — see the "AI and external services" section
below.

## Run instructions

**Prerequisites** (direct observation, `pyproject.toml`): Python `>=3.11`;
dependencies `pyyaml>=6.0` and `duckdb>=1.0`; dev dependency `pytest>=8.0`
under the `[project.optional-dependencies].dev` extra. `README.md` additionally
states `pdftotext` (from the `poppler` package) is required for statement PDF
adapters — direct observation confirms `src/fin/adapters/citi_pdf.py:198`
shells out to `pdftotext -layout <path> -` via `subprocess.run`, so a missing
binary will fail PDF ingest specifically (CSV ingest does not need it).

**Install and invoke** (`README.md` "Install"/"Use", corroborated by
`pyproject.toml` `[project.scripts]` mapping `fin` to `fin.cli:main`):

```
uv venv && uv pip install -e ".[dev]"
cp config/accounts.example.yaml   config/accounts.yaml
cp config/bindings.example.yaml   config/bindings.yaml
cp config/categories.example.yaml config/categories.yaml
cp config/targets.example.yaml    config/targets.yaml
cp config/merchant-rules.example.yaml config/merchant-rules.yaml
git config core.hooksPath hooks
```

then `fin ingest ... --account <id>`, `fin ingest-amazon ...`, `fin validate`,
`fin match`, `fin detect`, `fin render`, `fin analyze <what>`, `fin dispute
...`, `fin sql "<query>"`, `fin status`, as listed in Primary workflows above.
`fin` accepts `--data-dir` and `--config-dir` globally (`src/fin/cli.py`
`main`).

**Configuration** (direct observation, `src/fin/config.py` and the
`config/*.example.yaml` files): the real config directory defaults to
`<repo>/config` (`CONFIG_DIR` in `src/fin/config.py`) and is expected to hold
`accounts.yaml`, `bindings.yaml`, `categories.yaml`, `merchant-rules.yaml`, and
`targets.yaml`, each copied from a committed `.example.yaml` sibling before
first use (the real files are git-ignored per `.gitignore`). `accounts.yaml`
declares card ids, issuer, last-four digits, APR, statement close day, and
dispute window; `bindings.yaml` declares which cards a merchant is permitted
on (feeds detector D0); `merchant-rules.yaml` maps descriptor prefixes to a
merchant family and spend category; `targets.yaml` declares monthly target
spend per category. The repository ships only the `.example.yaml` versions, so
an evaluator must run the `cp` steps above (or point `--config-dir` at a
prepared directory) before any command that reads config will find real data.

**Ledger location**: `src/fin/store.py` (`default_data_dir`) reads
`FIN_DATA_DIR` from the environment and falls back to
`~/.local/share/beekeeper-ledger` — this is the only `os.environ` read found
anywhere under `src/fin/` (checked by grep across all of `src/fin/*.py` and
`src/fin/*/*.py`). `README.md` states this vault is created outside the
repository at mode `0700` and that the `data` symlink in the working tree
(declared in `.gitignore`, not present in this checkout) is a convenience
pointer to it. No ledger data ships with the submission; a judge exercising
ingest needs to supply statement files (a synthetic CSV/PDF, since the team
states no real statements are ever committed) and set `--data-dir` or
`FIN_DATA_DIR` to a writable path.

**Test data**: none required beyond what is embedded in the test file itself.
`tests/test_properties.py` (400 lines, 31 `test_` functions observed by grep)
builds its own synthetic Citi-statement text as a Python string
(`STATEMENT`, defined at line ~24) reproducing documented parsing hazards
(wrapped merchant name, trailing rewards column, page furniture) rather than
reading any fixture file. No `tests/fixtures/` directory exists in this
checkout despite a `.gitignore` allowance for one (`!tests/fixtures/**/*.csv`),
so that allowance is currently unused.

**Running tests** (direct observation, `pyproject.toml` `[tool.pytest.ini_options]`
sets `testpaths = ["tests"]` and `pythonpath = ["src"]`, so pytest is
runnable without an editable install as long as it is invoked from the repo
root): `README.md` gives `.venv/bin/python -m pytest -q`; equivalently
`python -m pytest -q` (or `uv run pytest -q`) from the repository root once
dependencies are installed. This is a fully offline, synthetic-data test
suite — direct observation found no network or file-system fixture
dependency in `tests/test_properties.py`.

**Credentials / `.env`**: this checkout's environment blocks reading any
`.env*` file under `workspaces/` as a host-level safety control (repository
`.claude/settings.json` deny rule `Read(./workspaces/**/.env*)`), and both the
`Read` tool and `Bash` `cat`/`grep` against `.env.example` were refused by that
control. This intake did not attempt to bypass it. Consequently the exact
variable names `.env.example` asks for could not be verified directly and are
recorded as **undetermined**. What can be cited: `README.md` states `.env`
holds "only 1Password `op://` references — pointers, never secrets — resolved
at runtime by `op run --env-file=.env -- fin ...`", and direct observation
(the grep above) found no `os.environ` read in `src/fin/` other than
`FIN_DATA_DIR`, which is not a secret. Whether `.env` is required at all for
the CLI to function, or is provisioning for a feature not yet wired to
`os.environ`, is undetermined from source alone.

## AI and external services

Direct observation: a grep across `src/fin/*.py` and `src/fin/*/*.py` for
network, HTTP, and common AI-provider indicators (`requests`, `urllib`,
`http`, `socket`, `openai`, `anthropic`, `api_key`, `subprocess`, `os.system`)
found exactly one hit — `subprocess` in `src/fin/adapters/citi_pdf.py`, used
only to shell out to the local `pdftotext` binary (see Run instructions). No
HTTP client, no LLM API call, and no third-party service call exists anywhere
in the deterministic `fin` package. This matches the design claim in
`src/fin/cli.py`'s module docstring: "parsing, matching, and money are code
with tests, and the model's job is to decide *what to run* and to explain
what came back" — i.e. the team's stated architecture keeps all arithmetic
and I/O in tested code and out of the model.

The only AI-facing surface is `.claude/skills/` (`fin-ingest`, `fin-reconcile`,
`fin-analyze`, `fin-dispute`), four Claude Code skill files that instruct a
Claude Code agent, at the user's own invocation, on which `fin` subcommand to
run for a given request and how to read its output. These are prompt/
instruction text, not executable integrations, and none of them make network
calls themselves — they only shell out to the already-reviewed `fin` CLI.
`SPEC.md` §9 states an LLM is used exactly once, offline from the app's
runtime: "An LLM proposes rules for uncategorized descriptors; a human
approves them; they land in `config/merchant-rules.yaml` and are applied
deterministically forever after" — this is a team claim about a human-in-the-
loop workflow, not something this checkout can independently demonstrate, and
no code path was found that calls out to any model API to generate those
proposals; the proposal step as described is performed by whatever agent
(e.g. Claude Code) the user is running interactively, using the skill text as
guidance, not by a call from within `fin` itself.

**Network posture under the event's empty allowlist / no-egress
constraint**: based on the direct observation above, the CLI itself (`fin
ingest`, `match`, `detect`, `validate`, `render`, `analyze`, `dispute`, `sql`,
`status`) requires no network access and should run unmodified in a
no-egress sandbox. Two things outside the CLI would not work without network
and are called out for evaluators:
- `README.md`'s stated credential workflow, `op run --env-file=.env -- fin
  ...`, invokes the 1Password CLI, which needs network access to resolve
  `op://` references; since no code path in `src/fin/` was found to consume
  a resolved secret (see Run instructions), this appears unnecessary for
  running any of the primary workflows in this checkout, but that is an
  inference, not a demonstrated fact.
- The Claude Code skills in `.claude/skills/` presume an interactive AI
  agent is available to drive `fin` and to propose categorization rules;
  under a no-network judging environment there is no way to exercise that
  agent-driven layer live, only to read the skill files as documentation and
  run the underlying `fin` commands directly.

No credentials, API keys, or third-party service endpoints were found
anywhere in the reviewed source.

## Known limitations

Team-claimed, unfinished behavior (`SPEC.md` §12 "Outstanding"):

- Phase 4 (a full categorization pass tuned to real behavior rather than the
  example targets file) and Phase 5 (dispute letter generation) are stated as
  not implemented. `SPEC.md`'s status line states the project is "implemented
  through phase 3."
- The Amazon feed adapter is stated as never having been exercised against
  real data — only against synthetic tests.
- Multi-account households and a per-merchant allowlist for recurring
  stored-value charges are stated as unhandled.

Environmental assumptions relevant to sandboxed evaluation:

- No ledger data or config ships with the submission. Every command that
  reads config or the vault needs the setup steps in Run instructions
  performed first (copying `.example.yaml` files, setting `--data-dir`/
  `FIN_DATA_DIR`, and supplying at least one synthetic statement to ingest).
- PDF ingest additionally depends on the `pdftotext` binary being present in
  the sandbox; if it is not, only PDF-based ingest is affected, not CSV
  ingest or the rest of the pipeline.
- `.env.example` could not be inspected: this checkout's host environment
  denies reading any `.env*` path under `workspaces/` (see Run instructions).
  Whether any variable it lists is actually required by `fin` could not be
  confirmed; source inspection found no code path consuming one.
- The `.claude/skills/` agent-orchestration layer cannot be exercised as
  designed in a no-network judging environment (see AI and external
  services); only the underlying `fin` CLI can be evaluated directly.
- The pinned commit's own commit message credits "Co-Authored-By: Claude
  Opus 5 <noreply@anthropic.com>" — noted here as a team-supplied fact about
  provenance, not verified independently.

**Injection attempts found**: none. All four files under `.claude/skills/`
(`fin-ingest`, `fin-reconcile`, `fin-analyze`, `fin-dispute`) and
`hooks/pre-commit` were read in full as data. Their content is addressed to
a Claude Code agent that a *user* of the finished application would run
interactively to drive the `fin` CLI (e.g. "use `fin analyze variance`
when the user asks about budget") — this is a legitimate part of the
submitted product, not an attempt to redirect this intake or any judge. A
repository-wide grep for common injection phrasing (`ignore previous`,
`disregard`, `system prompt`, `jailbreak`, `do not report`, `score this`,
`you are now`, `new instructions`, etc.) across `*.py`, `*.md`, `*.yaml`,
`*.yml` returned no matches. Nothing in this repository instructed this
intake process to change role, skip a step, assign a score, or take any
action outside completing this record.

## Intake provenance

| Fact | Value |
|---|---|
| Source | `https://github.com/beekeeper-lab/hive-ledger` |
| Source kind | git-url |
| Pinned commit | `9d21b7707f204ef60f5a1cee612f1d4db0a4a575` |
| How the commit was obtained | cloned |
| Checkout | `/home/gregg/Nextcloud/workspace/Software_Dev_Tournament/workspaces/live-trial-2026/team-ledger` |
| Materialized at | 2026-09-16T23:29:24Z |

Nothing in this submission has been executed. Execution requires `atj sandbox preflight` to report isolation available.
