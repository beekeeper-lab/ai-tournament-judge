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

- [ ] Rubric Markdown is the single authoritative source for criterion IDs, names, weights, scale, version (RB1, X1)
- [ ] Delete every duplicate hard-coded copy of official weights and versions (X1, X12)
- [ ] Structured metadata defined and validated for: event configuration, team intake, evidence manifest, individual judgment, consolidated report, adjudication, bracket, matchup, dossier, public report, model run record (M2, I6)
- [ ] Stable identifiers for event, team, submission commit, evidence package, rubric version, persona version, framework commit, judge run, matchup, adjudication (M2)
- [ ] No two editable copies of any official number
- [ ] Version incompatibility fails validation rather than warning (M3)
- [ ] Stage 1 independent audit
- [ ] Stage 1 findings repaired and re-audited

## Stage 2 — Deterministic tooling

### Event operations
- [ ] Initialize an event from the template
- [ ] Validate event configuration against schema (X9)
- [ ] Validate the roster (M6)
- [ ] Validate required directories and metadata
- [ ] Enforce legal event-state transitions (D3)
- [ ] Detect stale downstream artifacts when inputs change (D3)
- [ ] Resume from the first incomplete valid stage (D3)

### Submission and report validation
- [ ] Safe Markdown front-matter parsing (no arbitrary YAML construction)
- [ ] Schema validation of structured data (X11)
- [ ] Required report sections (X10)
- [ ] Judge identity, rubric version, evidence package, source commit (D6)
- [ ] Criterion scores, weights, totals, rounding
- [ ] Unresolved placeholders
- [ ] Missing evidence references
- [ ] Visibility classification enforcement (X4)
- [ ] Public output cannot contain private-only fields (RB2, S3, S5)

### Scoring and consolidation
- [ ] Criteria and weights read from the canonical rubric (RB1)
- [ ] Individual weighted scores (D9)
- [ ] Per-criterion panel means
- [ ] Minimum, maximum, range, source scores preserved
- [ ] Aligned / material / severe / possible-outlier detection (X13)
- [ ] Unresolved `NE` blocks finalization
- [ ] Deterministic structured results renderable to Markdown (D5)
- [ ] Panel integrity: configured judges present, distinct, version-matched (X6, X7, X8)

### Head-to-head calculation
- [ ] A-first comparison accepted (D1)
- [ ] B-first comparison accepted
- [ ] Reversed result normalized
- [ ] Per-criterion and total margins
- [ ] Presentation-order disagreement detected
- [ ] Configured close-call band applied
- [ ] Winner confirmed vs adjudication required
- [ ] Winner never advanced when policy requires human review

### Bracket generation and validation
- [ ] All declared bye policies supported, invalid policy rejected (X5)
- [ ] Seed recorded and reproducible
- [ ] Every eligible team exactly once
- [ ] Correct match and bye counts
- [ ] Previous champion and runner-up in opposite halves at every size (X2)
- [ ] Affiliation separation maximized without avoidable first-round collisions (X3)
- [ ] Infeasible constraints detected and reported
- [ ] Explicit constraint-satisfaction audit emitted (I2)
- [ ] Never silently violates a hard constraint
- [ ] 2–32 teams supported
- [ ] Tested across many seeds and distributions (I5)

### Report rendering
- [ ] Deterministic rendering of structured results into the existing Markdown templates (D5, M7)

- [ ] Stage 2 independent audit
- [ ] Stage 2 findings repaired and re-audited

## Stage 3 — Templates and policies

- [ ] `adjudication-report.md` (M8)
- [ ] `calibration-report.md` (M8, D7)
- [ ] `model-run-record.md` (M8, M9, S8)
- [ ] `manual-override-record.md` (M8)
- [ ] `release-readiness-report.md` (M8)
- [ ] Every template identifies event, team/matchup, submission commit, evidence package, rubric version, persona/agent version, framework commit, model requested, model used, start and completion time, visibility, approval state, validation state
- [ ] Private / team-facing / public boundaries reviewed and mechanically enforced
- [ ] Stage 3 independent audit
- [ ] Stage 3 findings repaired and re-audited

## Stage 4 — Agents, skills, commands, hooks

- [ ] Seven agents valid and usable in Claude Code 2.1.273
- [ ] Four initial judges share rubric and evidence, run independently, never see another report, treat submissions as untrusted, cite evidence, use `NE`, do not alter weights (S6)
- [ ] Every skill exercised against realistic inputs, behavior verified not just front matter
- [ ] Every slash command exercised with useful errors
- [ ] Project-local hooks added and tested (M10)
- [ ] Hooks fail safely, are non-destructive, stay inside the repository
- [ ] Stage 4 independent audit
- [ ] Stage 4 findings repaired and re-audited

## Stage 5 — Safe submission handling

- [ ] Sandbox implementation or explicit disablement (RB3, D2, S1)
- [ ] Podman and Docker support with honest preflight
- [ ] No host secrets, SSH agent, cloud credentials, personal files, or Docker socket
- [ ] Read-only submission mount where practical
- [ ] No network by default; explicit allowlist only
- [ ] CPU, memory, disk, process, time limits
- [ ] Synthetic test data
- [ ] Command and exit-status recording; stdout/stderr captured
- [ ] Clean teardown; no privileged containers; no insecure host fallback
- [ ] Executable evidence marked unavailable and `NE` applied when isolation is unavailable (S2)
- [ ] Prompt-injection fixture proving role, rubric, tools, destination, publication policy cannot be redefined (RB9, S4, M12)
- [ ] Stage 5 independent audit
- [ ] Stage 5 findings repaired and re-audited

## Stage 6 — Synthetic sample event and end-to-end test

- [ ] Committed synthetic event, obviously non-real, ≥4 teams (M13)
- [ ] Two teams sharing an affiliation group
- [ ] Previous champion and runner-up
- [ ] Different application strengths
- [ ] One material criterion disagreement
- [ ] One severe disagreement or possible outlier
- [ ] One initial `NE`
- [ ] One adjudication
- [ ] One close-call matchup
- [ ] One order-balanced matchup with consistent results
- [ ] One failed audit that is repaired
- [ ] Private judge reports, consolidated reports, bracket, private matchup reports, public summaries, dossiers, final audit
- [ ] Separate 20-team bracket fixture: 32 slots, 4 preliminary matches, 8 preliminary participants, 12 byes, finalist separation, affiliation separation, seed reproducibility
- [ ] Complete workflow runs from a clean working directory using documented commands
- [ ] Interrupt and resume without duplicating valid completed work
- [ ] Stage 6 independent audit
- [ ] Stage 6 findings repaired and re-audited

## Stage 7 — Public output and ceremony view

- [ ] Event overview, bracket, current round, completed matchups, advancement explanation, champion and finalists, judging-method disclosure (M14)
- [ ] Generated only from approved public artifacts
- [ ] Printable/downloadable team dossier from approved team-facing Markdown
- [ ] Stage 7 independent audit
- [ ] Stage 7 findings repaired and re-audited

## Stage 8 — Release engineering

- [ ] Version source (M15)
- [ ] `CHANGELOG.md`
- [ ] Installation and operating instructions
- [ ] Dependency declaration
- [ ] Test, validation, and end-to-end demonstration commands
- [ ] Release checklist
- [ ] CI workflow
- [ ] Packaging command
- [ ] Documented security, model, and cost limitations
- [ ] Recovery and troubleshooting guidance
- [ ] CI verifies tests, rubric total, schemas, skill structure, template integrity, placeholders, bracket reproduction, score calculation, matchup normalization, state transitions, publication boundaries
- [ ] No claim that LLM judgment is deterministic
- [ ] Stage 8 independent audit
- [ ] Stage 8 findings repaired and re-audited

## Stage 9 — Final independent audit

- [ ] Functional completeness
- [ ] Internal consistency
- [ ] Security
- [ ] Prompt-injection resistance
- [ ] Judge independence
- [ ] Scoring integrity
- [ ] Bracket fairness
- [ ] Publication privacy
- [ ] Failure and recovery
- [ ] Test sufficiency
- [ ] Documentation accuracy
- [ ] Claude Code compatibility
- [ ] Release reproducibility
- [ ] `docs/final-audit.md` states PASS or PASS WITH ADVISORIES
- [ ] All blocking and major findings resolved

---

## Appendix A — original v0.1.0-alpha stage numbering

The alpha plan had eight stages: repository foundation, rubrics and policies,
agents and personas, templates and schemas, deterministic tooling, skills and
commands, event simulation, production readiness. All 30 items were unchecked
(finding I8). They map to the stages above as:
alpha 1→0, alpha 2→3, alpha 3→4, alpha 4→1/3, alpha 5→2, alpha 6→4,
alpha 7→6, alpha 8→8/9.
