---
document: release-readiness-audit
framework_version_audited: 0.1.0-alpha
target_version: 0.2.0-beta
audit_date: 2026-09-16
auditor: lead engineer (baseline, pre-implementation)
result: FAIL — not release ready
visibility: private
---

# Release Readiness Audit — baseline of v0.1.0-alpha

This is the Phase 0 baseline. It records what the scaffold **does** when executed,
not what its documents claim. Every finding below was reproduced against the
imported scaffold at baseline commit `7048815` before any implementation work.

Environment used for verification:

| Item | Value |
|---|---|
| Python | 3.14.7 |
| Claude Code | 2.1.273 |
| `jsonschema` | 4.26.0 (installed, unused by the scaffold) |
| `PyYAML` | 6.0.3 (installed, unused by the scaffold) |
| Container runtime | `podman` absent; `docker` client present, **daemon unreachable** (`docker version` hangs, 8s and 20s timeouts) |
| Git | repository did not exist; initialized during this phase |

Baseline test run: `python3 -m unittest discover -s tests -p 'test_*.py'` → 11 tests, OK.
Baseline config validation: `python3 scripts/validate_configuration.py events/_template` → PASS, 4 warnings.
Both pass, and both are far weaker than the documentation implies. That gap is the
central theme of this audit.

---

## 1. Present and working

| ID | Item | Verified behavior |
|---|---|---|
| W1 | Rubric, policy, and template prose | Internally coherent, versioned front matter, seven criteria summing to 100. |
| W2 | `scripts/calculate_scores.py` core arithmetic | `score/5*weight` summed across criteria is correct; perfect = 100.0, midpoint = 60.0. Verified at 0/3/5. |
| W3 | Agreement thresholds | `aligned ≤1`, `material =2`, `severe ≥3` matches `panel-consolidation.md`. Verified at ranges 0,1,2,3,5. |
| W4 | Outlier detection | `abs(value - median) >= 2` matches the policy text. |
| W5 | `scripts/build_bracket.py` bracket shape | For every team count 2–32: correct power-of-two size, correct bye count, every team placed exactly once, correct first-round unit count. Verified exhaustively. |
| W6 | Bracket seed reproducibility | Identical payload + seed produces byte-identical output. |
| W7 | `performance-qualified` bye selection | Top-scoring teams receive byes; ties fall back to seeded shuffle order. |
| W8 | `scripts/initialize_event.py` | Copies the template, enforces the event-ID pattern, refuses to overwrite an existing event. |
| W9 | Claude component front matter | All 7 agents, 8 skills, and 8 commands parse as valid Claude Code 2.1.273 components (`name`/`description`, `tools`, `model`, `argument-hint`). |
| W10 | `.gitignore` | Correctly excludes `workspaces/`, sandboxes, `.env`, caches. |
| W11 | Judge personas | Four personas differ only in investigative emphasis; none restates or overrides weights. Agent `tools:` lists are read-only (`Read, Grep, Glob`), which structurally supports judge independence. |

---

## 2. Present but incomplete

| ID | Item | Gap |
|---|---|---|
| I1 | `calculate_scores.py` | Computes one team's consolidation only. No panel-membership check, no minimum panel size, no identity/version cross-check between judge reports, no structured output the templates can be rendered from. |
| I2 | `build_bracket.py` | Produces only round 1. No later rounds, no advancement, no constraint-satisfaction audit, no exception record, no infeasibility report. |
| I3 | `validate_configuration.py` | Purely structural: existence of four files, presence of a `---` block, presence of the literal substring `event_id:`, existence of eight directories. Does not parse YAML or apply any schema. |
| I4 | `validate_reports.py` | Checks front-matter substrings and a five-item placeholder blocklist. No section, score, identity, version, evidence, or visibility-boundary validation. |
| I5 | `tests/` | 11 tests over three scripts. No tests for `initialize_event.py`, no negative/boundary coverage for the validators, no multi-seed or multi-size bracket coverage, no end-to-end coverage. `tests/fixtures/` is empty. |
| I6 | `schemas/` | Five schemas exist but **nothing loads them**. No schema for evidence manifests, consolidated reports, adjudications, dossiers, public reports, matchup results, or model-run records. |
| I7 | `events/_template` | Directory skeleton and stub front matter only. `status.md` has empty progress and activity tables and no machine-readable stage record. |
| I8 | `docs/implementation-plan.md` | Every one of 30 checklist items is unchecked, including Stage 1–4 items whose artifacts already exist. Accurate as a plan; useless as a completion record. |

---

## 3. Documented but not implemented

These are described in prose as if they exist. They do not.

| ID | Documented in | Claim | Reality |
|---|---|---|---|
| D1 | `head-to-head.md`, `judge-matchup` skill, `docs/tournament-operations.md` | Order-balanced matchup calculation, reversal normalization, close-call band, adjudication trigger | **No matchup calculator exists.** There is no script, function, or test. `schemas/matchup.schema.json` describes a shape nothing produces or consumes. |
| D2 | `execution-safety.md`, `docs/security-and-sandboxing.md`, `prepare-submission` skill | Isolated disposable sandbox, no secrets, no network, resource limits, command/output recording, teardown | **Documentation only.** No sandbox runner, no container invocation, no preflight, no recording. Nothing prevents an operator from running submission code on the host. |
| D3 | `run-judging-event` skill, `docs/recovery-and-resume.md` | `configuration → intake → … → complete` state machine, legal transitions, stale-dependency detection, resume from first incomplete unit | **No implementation.** Transitions exist only as prose an agent is asked to honor. |
| D4 | `report-publication.md`, `build-team-dossier` skill | Private / team-facing / public boundaries enforced before publication | **Not enforced.** Reproduced: a file in `public/` carrying `visibility: private`, a hard-coded AWS key, explicit judge deliberation, and an unapproved numeric score passes `validate_reports.py` with zero errors. |
| D5 | `CLAUDE.md`, `README.md` | "Use scripts for scoring, report validation, and bracket assignment. Never perform official arithmetic or randomness only in prose." | No rendering path connects script output to the Markdown templates, so every official number in every template is transcribed by hand today. |
| D6 | `panel-consolidation.md` | "Require all configured reports to reference the same team, commit, evidence package, and rubric version." | Nothing performs this check. |
| D7 | `docs/scoring-and-calibration.md` | Calibration exercise with recorded distributions | No calibration template, script, or record format. |
| D8 | `judge-independence.md` | Independence enforced | Enforced only by convention in skill prose. No mechanical check that two judgments are distinct, or that a judge report was not reused. |
| D9 | `submission-evaluation.md` | "Use `scripts/calculate_scores.py`" for per-judge totals | The script only does panel consolidation. There is no individual-judgment calculator, so the template's per-judge "Weighted points" column has no generator. |

---

## 4. Missing

| ID | Missing item | Required by |
|---|---|---|
| M1 | Canonical rubric reader — a single parser making `submission-evaluation.md` the authoritative source of criteria, weights, scale, and version | Stage 1 |
| M2 | Stable identifier scheme (event, team, submission commit, evidence package, rubric version, persona version, framework commit, judge run, matchup, adjudication) | Stage 1 |
| M3 | Version-incompatibility failure (currently no version comparison exists at all) | Stage 1 |
| M4 | Cohesive CLI; five disconnected scripts with incompatible I/O conventions | Stage 2 |
| M5 | Head-to-head matchup calculator | Stage 2 |
| M6 | Roster validation; event-state transition enforcement; staleness detection; resume | Stage 2 |
| M7 | Deterministic Markdown rendering from structured results | Stage 2 |
| M8 | Templates: `adjudication-report.md`, `calibration-report.md`, `model-run-record.md`, `manual-override-record.md`, `release-readiness-report.md` | Stage 3 |
| M9 | Model-requested vs model-actually-used recording anywhere in the system | Stage 3 |
| M10 | Project-local hooks — `.claude/settings.json` contains only four `deny` permission rules and no `hooks` block | Stage 4 |
| M11 | Sandboxed execution implementation and preflight | Stage 5 |
| M12 | Prompt-injection fixture and test proving repository content cannot redefine judge role, rubric, tools, destination, or publication policy | Stage 5 |
| M13 | Synthetic sample event; 20-team bracket fixture; end-to-end test | Stage 6 |
| M14 | Public ceremony output; printable team dossier | Stage 7 |
| M15 | `VERSION`, `CHANGELOG.md`, dependency declaration, CI workflow, packaging, release checklist, troubleshooting | Stage 8 |
| M16 | `docs/implementation-detail.md`, `docs/final-audit.md` | Final artifacts |
| M17 | Git repository (created during this phase) | Operating rules |

---

## 5. Incorrect or internally inconsistent

Each was reproduced. Severity: **B** blocking, **J** major, **N** minor.

| ID | Sev | Defect | Reproduction |
|---|---|---|---|
| X1 | B | **Official weights are duplicated.** `calculate_scores.DEFAULT_WEIGHTS` is a second editable copy of the rubric table. They agree today; nothing keeps them agreeing. Directly violates the Stage 1 rule and `CLAUDE.md`'s single-source-of-truth rule. | Compared the dict against the parsed rubric table. |
| X2 | B | **Previous-finalist separation is broken for every bracket except 32 slots.** `placement_penalty` hard-codes `position // 8` as "half", which is only true when there are exactly 16 first-round units. | 40 seeds per size. Champion and runner-up land in the same half: n=4 → 17/40, n=6 → 21/40, n=8 → 14/40, n=12 → 20/40, n=16 → 8/40; n=20/24/32 → 0/40. The existing test only covers n=20, so it passes while the constraint is broken everywhere else. |
| X3 | B | **Avoidable same-affiliation first-round pairings are produced.** `pair_play_in_teams` is greedy with no backtracking: it can strand two same-group teams as the final pair even when a collision-free pairing exists. | 40 seeds, 4 affiliation groups: n=8 → 6 collisions, n=16 → 5, n=20 → 12, n=32 → 4. The policy calls separation a maximization goal; the code violates it silently with no exception record. |
| X4 | B | **Publication boundary is not enforced.** See D4. A `public/` artifact containing a credential, private deliberation, and `visibility: private` validates clean. | Direct call to `validate_file`. |
| X5 | B | **Invalid bye policy is silently accepted.** `choose_byes` returns before validating `policy` when `bye_count == 0`. A misspelled policy on a power-of-two field produces a bracket with a bogus `bye_policy` recorded in the output. | `bye_policy: "bogus"`, 4 teams → built successfully. |
| X6 | J | **Weight validation only checks the sum.** Any set totalling 100 is accepted, including a silently wrong split. | `functional: 24, product: 16` → accepted, total 100.0. |
| X7 | J | **Arbitrary non-rubric criteria are accepted.** Passing `{"alpha":50,"beta":50}` produces a clean official-looking result with criteria that do not exist in the rubric. | Direct call. |
| X8 | J | **No panel-integrity checks.** A one-judge panel is accepted. Four judgments carrying the *same* `judge_id` are accepted. Nothing detects a duplicated or reused report. | Direct calls; both returned totals. |
| X9 | J | **`validate_configuration.py` accepts structurally invalid configuration.** `event_id: NOT A VALID ID!!`, `bye_policy: nonsense-policy`, `expected_judges: 7` → zero errors, zero warnings, PASS. It never parses YAML; `"event_id:" in text` is the whole check. | Synthetic event directory. |
| X10 | J | **`validate_reports.py` accepts an empty report and an out-of-range score.** A judgment file with only front matter, and one asserting "score 9 of 5", both pass. | Direct calls. |
| X11 | J | **Schemas are dead code.** Five JSON Schemas ship and nothing validates against them, so the contract they express is unenforced. | `grep -r jsonschema scripts tests` → no matches. |
| X12 | N | **`judgment.schema.json` hard-codes `"rubric": {"const": "submission-evaluation@1.0.0"}`.** A third editable copy of the official rubric version. Bumping the rubric silently invalidates every judgment until a human remembers to edit the schema. | Read. |
| X13 | N | **`possible-outlier` is not an agreement level.** The policy lists four cases; the script returns three and reports outliers in a separate field, so the template's single "Agreement" column cannot express it. | `[5,3,3,3]` → `material-disagreement`, outliers `['j0']`. |
| X14 | N | **`initialize_event.py` leaves `TBD`, `YYYY-MM-DD…`, and unfilled tables behind** and does not run validation, so a freshly initialized event is immediately in a state the strict validator rejects. | `--strict` on `events/_template` → 4 errors. |
| X15 | N | **`README.md` overstates the validation command.** "Validation" documents two commands that together check file existence and arithmetic on three scripts. | Read against behavior. |
| X16 | N | **`docs/implementation-plan.md` stage numbering does not match the release stages** used for this work, so audit results cannot be filed against it without renumbering. | Read. |
| X17 | N | **`ai-tournament-judge.zip` (65 KB) is a committed duplicate of the working tree.** Harmless but it will drift and be mistaken for a release artifact. | `unzip -l` → 117 entries mirroring the tree. |

---

## 6. Security concerns

| ID | Sev | Concern |
|---|---|---|
| S1 | B | **No execution isolation exists.** `execution-safety.md` reads as though controls are in place. Nothing implements them and nothing blocks host execution of untrusted submission code. Until a sandbox exists, the honest position is that execution is *disabled*, not *safe*. |
| S2 | B | **This host cannot currently provide isolation.** `podman` is absent. The `docker` client is present but the daemon does not respond (`docker version` hangs past 20s). Therefore executable evidence must be marked unavailable for this release and affected criteria must use `NE`. |
| S3 | B | **Nothing prevents private data reaching public output.** See X4/D4. This is the highest-consequence defect for a student-facing event. |
| S4 | J | **No prompt-injection fixture or test.** Every judge prompt tells the agent to treat submission text as untrusted. No artifact demonstrates that the instruction holds, so the claim is unverified. |
| S5 | J | **No secret scanning** of evidence manifests, judgments, dossiers, or public artifacts. A key pasted from a student repo into an evidence manifest would be committed. |
| S6 | J | **Judge independence is unenforced.** Agent `tools:` are read-only, which is good, but nothing detects an orchestrator that hands judge B judge A's report, and nothing detects the resulting duplicate content. |
| S7 | N | `.claude/settings.json` denies `Read(./.env*)`, `git push --force*`, and `git reset --hard*`. Reasonable, but it is not a security boundary and should not be described as one. No hooks provide defense in depth. |
| S8 | N | No model-run record, so there is no evidence trail proving which model produced which judgment — a requirement for disputing an award. |

---

## 7. Release blockers

Ordered. Each must close before v0.2.0-beta can be called ready.

| ID | Blocker | Closes |
|---|---|---|
| RB1 | Official weights read from the rubric; no second editable copy anywhere | X1, X12, M1 |
| RB2 | Publication boundary enforced mechanically before any public artifact is written | X4, D4, S3, S5 |
| RB3 | Execution either genuinely sandboxed or explicitly disabled with `NE` consequences | D2, S1, S2, M11 |
| RB4 | Bracket constraint defects fixed and proven across sizes and seeds, with a constraint-satisfaction audit | X2, X3, X5, I2, M13 |
| RB5 | Head-to-head calculator implemented with order normalization and close-call handling | D1, M5 |
| RB6 | Event state machine, staleness detection, and resume implemented | D3, M6 |
| RB7 | Real schema and section validation replacing substring checks | X9, X10, X11, I3, I4 |
| RB8 | Panel-integrity checks: configured judges present, distinct, version-matched | X6, X7, X8, D6 |
| RB9 | Prompt-injection fixture proving judge role/rubric/tools/destination cannot be redefined | S4, M12 |
| RB10 | End-to-end synthetic event that actually runs, with an interruption/resume proof | M13 |
| RB11 | Release engineering: version, changelog, dependencies, CI, validation command | M15 |
| RB12 | Documentation corrected to match behavior | D5, X15, X16, I8 |

---

## 8. Recommended implementation order

1. **Canonical data model** — rubric reader, identifiers, schemas, version enforcement. Everything else depends on it. (RB1)
2. **Deterministic tooling** — one CLI over: event ops and state machine, validation, scoring, head-to-head, bracket, rendering. (RB4–RB8)
3. **Templates and publication boundaries** — missing templates plus the mechanical private/team/public gate. (RB2)
4. **Claude components and hooks** — verify agents/skills/commands behave, add project-local hooks. (M10)
5. **Safe submission handling** — sandbox with honest preflight and refusal to fall back to the host; injection fixture. (RB3, RB9)
6. **Synthetic sample event and end-to-end test** — including interruption and resume. (RB10)
7. **Public ceremony output and dossiers** — generated only from approved artifacts.
8. **Release engineering** — version, changelog, CI, packaging, docs. (RB11, RB12)
9. **Final independent audit.**

---

## 9. Baseline verdict

**FAIL — not release ready.**

The scaffold is a well-written specification with a thin and partly incorrect
implementation underneath it. Its documentation describes a system with enforced
safety, enforced privacy, enforced independence, and deterministic tournament
mechanics. Executed, it provides correct weighted arithmetic, a correctly shaped
bracket, and file-existence checks. Three of the five constraint and safety
properties the documents promise are either absent (D1, D2, D3, D4) or actively
broken (X2, X3).

The gap between claim and behavior is itself the most serious finding: an operator
reading `execution-safety.md` or `report-publication.md` would reasonably believe
controls exist that do not.
