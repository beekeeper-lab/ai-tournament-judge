---
document: implementation-plan
target_version: 0.2.0-beta
baseline_version: 0.1.0-alpha
renumbered: 2026-09-16
---

# Implementation Plan

Build and audit record for the v0.2.0-beta release. Stages are renumbered to match
the release stages (baseline finding X16). The original v0.1.0-alpha numbering is
preserved in Appendix A.

**Rule:** an item is checked only when its *behavior* has been verified, not when a
file exists. Audit results are recorded under each stage.

Finding IDs referenced here (`X…`, `D…`, `M…`, `S…`, `RB…`) are defined in
`docs/release-readiness-audit.md`.

---

## Stage 0 — Repository and baseline verification

- [x] Initialize Git repository and create baseline commit of the untouched scaffold
- [x] Create and switch to `feature/v0.2-release-readiness`
- [x] Read README, CLAUDE.md, plan, rubrics, policies, skills, agents, commands, templates, scripts, schemas, tests
- [x] Inventory the repository (84 tracked files at baseline)
- [x] Run the existing test suite (11 tests, OK)
- [x] Run existing validators (`validate_configuration.py events/_template` → PASS, 4 warnings)
- [x] Verify Claude agent / skill / command / settings formats against Claude Code 2.1.273
- [x] Identify security-sensitive behavior before executing anything
- [x] Write `docs/release-readiness-audit.md`
- [x] Renumber and extend this plan

**Stage 0 result: FAIL (expected).** 17 defects reproduced, 12 release blockers
recorded. See the baseline audit.

---

## Stage 1 — Canonical data model and versioning

- [x] Rubric Markdown is the single authoritative source for criterion IDs, names, weights, scale, version (RB1, X1)
- [x] Delete every duplicate hard-coded copy of official weights and versions (X1, X12)
- [x] Structured metadata defined and validated for: event configuration, team intake, evidence manifest, individual judgment, consolidated report, adjudication, bracket, matchup, dossier, public report, model run record (M2, I6)
- [x] Stable identifiers for event, team, submission commit, evidence package, rubric version, persona version, framework commit, judge run, matchup, adjudication (M2)
- [x] No two editable copies of any official number
- [x] Version incompatibility fails validation rather than warning (M3)
- [x] Stage 1 independent audit
- [x] Stage 1 findings repaired and re-audited

**Stage 1 audit: FAIL, then PASS after repair.** The first independent audit
returned 3 blocking, 6 major and 10 minor findings; a second independent audit of
the repaired commit returned 1 blocking and 8 major. Every finding is fixed with a
named regression test in `tests/test_audit_regressions.py`. Verified by:
`python3 -m atj release-check`, `python3 -m atj rubric`, `python3 -m atj schemas`,
`python3 -m atj personas`.

## Stage 2 — Deterministic tooling

### Event operations
- [x] Initialize an event from the template
- [x] Validate event configuration against schema (X9)
- [x] Validate the roster (M6)
- [x] Validate required directories and metadata
- [x] Enforce legal event-state transitions (D3)
- [x] Detect stale downstream artifacts when inputs change (D3)
- [x] Resume from the first incomplete valid stage (D3)

### Submission and report validation
- [x] Safe Markdown front-matter parsing (no arbitrary YAML construction)
- [x] Schema validation of structured data (X11)
- [x] Required report sections (X10)
- [x] Judge identity, rubric version, evidence package, source commit (D6)
- [x] Criterion scores, weights, totals, rounding
- [x] Unresolved placeholders
- [x] Missing evidence references
- [x] Visibility classification enforcement (X4)
- [x] Public output cannot contain private-only fields (RB2, S3, S5)

### Scoring and consolidation
- [x] Criteria and weights read from the canonical rubric (RB1)
- [x] Individual weighted scores (D9)
- [x] Per-criterion panel means
- [x] Minimum, maximum, range, source scores preserved
- [x] Aligned / material / severe / possible-outlier detection (X13)
- [x] Unresolved `NE` blocks finalization
- [x] Deterministic structured results renderable to Markdown (D5)
- [x] Panel integrity: configured judges present, distinct, version-matched (X6, X7, X8)

### Head-to-head calculation
- [x] A-first comparison accepted (D1)
- [x] B-first comparison accepted
- [x] Reversed result normalized
- [x] Per-criterion and total margins
- [x] Presentation-order disagreement detected
- [x] Configured close-call band applied
- [x] Winner confirmed vs adjudication required
- [x] Winner never advanced when policy requires human review

### Bracket generation and validation
- [x] All declared bye policies supported, invalid policy rejected (X5)
- [x] Seed recorded and reproducible
- [x] Every eligible team exactly once
- [x] Correct match and bye counts
- [x] Previous champion and runner-up in opposite halves at every size (X2)
- [x] Affiliation separation maximized without avoidable first-round collisions (X3)
- [x] Infeasible constraints detected and reported
- [x] Explicit constraint-satisfaction audit emitted (I2)
- [x] Never silently violates a hard constraint
- [x] 2–32 teams supported
- [x] Tested across many seeds and distributions (I5)

### Report rendering
- [x] Deterministic rendering of structured results into the existing Markdown templates (D5, M7)

- [x] Stage 2 independent audit
- [x] Stage 2 findings repaired and re-audited

**Stage 2 audit: PASS after repair.** Verified by 244 tests including sweeps of
every bracket size, every bye policy and many seeds; 5,580 bracket builds produced
zero avoidable hard-constraint violations. Tampered brackets are caught by
re-derivation rather than by reading the audit block.

## Stage 3 — Templates and policies

- [x] `adjudication-report.md` (M8)
- [x] `calibration-report.md` (M8, D7)
- [x] `model-run-record.md` (M8, M9, S8)
- [x] `manual-override-record.md` (M8)
- [x] `release-readiness-report.md` (M8)
- [x] Every template identifies event, team/matchup, submission commit, evidence package, rubric version, persona/agent version, framework commit, model requested, model used, start and completion time, visibility, approval state, validation state
- [x] Private / team-facing / public boundaries reviewed and mechanically enforced
- [x] Stage 3 independent audit
- [x] Stage 3 findings repaired and re-audited

**Stage 3 audit: PASS.** Verified by `atj release-check` (`templates PASS`,
`version-skew PASS`) and by report validation of the sample event, which derives
required sections from the templates themselves.

## Stage 4 — Agents, skills, commands, hooks

- [x] Seven agents valid and usable in Claude Code 2.1.273
- [x] Four initial judges share rubric and evidence, run independently, never see another report, treat submissions as untrusted, cite evidence, use `NE`, do not alter weights (S6)
- [x] Every skill exercised against realistic inputs, behavior verified not just front matter
- [x] Every slash command exercised with useful errors
- [x] Project-local hooks added and tested (M10)
- [x] Hooks fail safely, are non-destructive, stay inside the repository
- [x] Stage 4 independent audit
- [x] Stage 4 findings repaired and re-audited

**Stage 4 audit: PASS WITH ADVISORIES.** Agents, skills and commands verified by
`atj release-check` (`claude components PASS`) and exercised through the sample
event. Hooks verified firing in Claude Code 2.1.273: a PreToolUse hook blocked a
hand-edit of `events/*/public/` end to end.
Advisory: Claude Code ignores `permissions.allow` from project settings until the
workspace is trusted. Nothing depends on it, and it is documented.

## Stage 5 — Safe submission handling

- [x] Sandbox implementation or explicit disablement (RB3, D2, S1)
- [x] Podman and Docker support with honest preflight
- [x] No host secrets, SSH agent, cloud credentials, personal files, or Docker socket
- [x] Read-only submission mount where practical
- [x] No network by default; explicit allowlist only
- [x] CPU, memory, disk, process, time limits
- [x] Synthetic test data
- [x] Command and exit-status recording; stdout/stderr captured
- [x] Clean teardown; no privileged containers; no insecure host fallback
- [x] Executable evidence marked unavailable and `NE` applied when isolation is unavailable (S2)
- [x] Prompt-injection fixture proving role, rubric, tools, destination, publication policy cannot be redefined (RB9, S4, M12)
- [x] Stage 5 independent audit
- [x] Stage 5 findings repaired and re-audited

**Stage 5 audit: PASS WITH ADVISORIES.** Sandbox construction, refusal behaviour
and the prompt-injection fixture verified by 20 tests.
Advisory: no container runtime is available on the release host (podman absent,
docker daemon unresponsive), so the live execution path is unit-tested but not
exercised against a real runtime. `atj sandbox preflight` reports this.

## Stage 6 — Synthetic sample event and end-to-end test

- [x] Committed synthetic event, obviously non-real, ≥4 teams (M13)
- [x] Two teams sharing an affiliation group
- [x] Previous champion and runner-up
- [x] Different application strengths
- [x] One material criterion disagreement
- [x] One severe disagreement or possible outlier
- [x] One initial `NE`
- [x] One adjudication
- [x] One close-call matchup
- [x] One order-balanced matchup with consistent results
- [x] One failed audit that is repaired
- [x] Private judge reports, consolidated reports, bracket, private matchup reports, public summaries, dossiers, final audit
- [x] Separate 20-team bracket fixture: 32 slots, 4 preliminary matches, 8 preliminary participants, 12 byes, finalist separation, affiliation separation, seed reproducibility
- [x] Complete workflow runs from a clean working directory using documented commands
- [x] Interrupt and resume without duplicating valid completed work
- [x] Stage 6 independent audit
- [x] Stage 6 findings repaired and re-audited

**Stage 6 audit: PASS.** Verified by `atj demo check`, `atj event validate`
(PASS, 0 problems), `atj validate reports` (PASS, 48 artifacts, 0 findings), both
bracket verifications, and the end-to-end and resume tests.

## Stage 7 — Public output and ceremony view

- [x] Event overview, bracket, current round, completed matchups, advancement explanation, champion and finalists, judging-method disclosure (M14)
- [x] Generated only from approved public artifacts
- [x] Printable/downloadable team dossier from approved team-facing Markdown
- [x] Stage 7 independent audit
- [x] Stage 7 findings repaired and re-audited

**Stage 7 audit: PASS.** Verified by `tests/test_ceremony.py`: the rendered page
contains no evidence package id, judge run id, adjudication id, judge persona,
score, commit hash or seed; it loads nothing over the network; and it refuses to
render when any public artifact fails the publication gate.

## Stage 8 — Release engineering

- [x] Version source (M15)
- [x] `CHANGELOG.md`
- [x] Installation and operating instructions
- [x] Dependency declaration
- [x] Test, validation, and end-to-end demonstration commands
- [x] Release checklist
- [x] CI workflow
- [x] Packaging command
- [x] Documented security, model, and cost limitations
- [x] Recovery and troubleshooting guidance
- [x] CI verifies tests, rubric total, schemas, skill structure, template integrity, placeholders, bracket reproduction, score calculation, matchup normalization, state transitions, publication boundaries
- [x] No claim that LLM judgment is deterministic
- [x] Stage 8 independent audit
- [x] Stage 8 findings repaired and re-audited

**Stage 8 audit: PASS.** Version source, changelog, packaging, dependency
declaration, CI workflow, release checklist and troubleshooting are in place and
the documented validation command runs clean.

## Stage 9 — Final independent audit

- [x] Functional completeness
- [x] Internal consistency
- [x] Security
- [x] Prompt-injection resistance
- [x] Judge independence
- [x] Scoring integrity
- [x] Bracket fairness
- [x] Publication privacy
- [x] Failure and recovery
- [x] Test sufficiency
- [x] Documentation accuracy
- [x] Claude Code compatibility
- [x] Release reproducibility
- [x] `docs/final-audit.md` states PASS WITH ADVISORIES
- [x] All blocking and major findings resolved

**Stage 9 result: PASS WITH ADVISORIES.** Five independent audit rounds were run;
four returned FAIL and every finding was repaired with a named regression test.
The advisories that remain are recorded in `docs/final-audit.md` and are stated,
not closed. The release is fit for a supervised mock event and is not yet fit to
decide a real award.
