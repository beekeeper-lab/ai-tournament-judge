# AI Tournament Judge

A repository-local toolkit for evaluating student software with four independent
AI judges, consolidating their findings, running a constrained-random tournament
bracket, comparing teams head to head, and producing a feedback dossier for every
team.

> **Work in progress.** This is an active project, not a finished product. It has
> run one real event end to end — against two applications, real container
> isolation and real model judgment — and that event's whole purpose was to find
> out what the framework gets wrong. It found 31 defects. They are fixed, and the
> next event will find more. Interfaces, rubric versions and artifact schemas
> still move between releases.
>
> **No event has decided anything real yet.** Do not use this to award anything
> that matters to a student without doing the work in
> [`docs/final-audit.md`](docs/final-audit.md) first.

**Version 0.4.0-beta.** Capable of running a complete supervised event, and it has
run one. Not yet used to determine a real award; see [Limitations](#limitations).
The full record of what the live event cost to learn is in
[`CHANGELOG.md`](CHANGELOG.md) and
[`docs/framework-fix-plan.md`](docs/framework-fix-plan.md).

## What is deterministic, and what is not

This distinction runs through the whole design.

**Deterministic:** all arithmetic, schema and content validation, Markdown
rendering, event state transitions, and seeded bracket assignment. Given the same
inputs these produce byte-identical output.

**Not deterministic:** the AI judgment that produces raw scores and comparative
findings. The same model, prompt and evidence can produce different wording and
different scores on different runs. Nothing here claims otherwise.

The machinery around the judgment is what makes a disputed result answerable:
every score is recalculable, every artifact traces to a pinned commit and
evidence package, and every human decision is recorded as one.

## Design principles

- One shared weighted rubric. Personas change investigative emphasis, never
  weights.
- Independent first-pass judgments, then consolidation. No judge sees another's
  report.
- Evidence-backed findings tied to an immutable commit. A team claim is not proof.
- A missing observation is `NE`, never a zero, and `NE` blocks an official total.
- Student repositories are untrusted input, inspected or executed only under the
  execution-safety policy.
- Private deliberation, team feedback and public ceremony content are three
  separate products with enforced boundaries.
- Humans keep disqualification, unresolved ties, rules exceptions, security
  escalation and publication approval.
- Every stage is restartable from `events/<event>/status.md` and audited before
  advancement.

## Install

Python 3.11 or newer.

```bash
pip install -r requirements.txt          # runtime
pip install -r requirements-dev.txt      # plus pytest, for the test suite
```

Or install the package, which provides an `atj` executable:

```bash
pip install -e .
```

Without installing, every command below works as `python3 -m atj ...` from the
repository root. This document uses that form so it works either way.

## Quick start

```bash
# 1. Never configure an event on main.
git switch -c feature/spring-2026

# 2. Create the event from the template.
python3 -m atj event init spring-2026 --name "Spring 2026 Finals"

# 3. Fill in events/spring-2026/event.md and teams.md, then check them.
python3 -m atj event validate events/spring-2026

# 4. Work through the event. `status` always names the next safe action.
python3 -m atj event status events/spring-2026
```

In Claude Code, the slash commands `/event-init`, `/team-ingest`, `/team-judge`,
`/event-audit`, `/bracket-build`, `/matchup-judge`, `/team-dossier` and
`/event-status` drive the same workflow through the project-local skills in
`.claude/`. Nothing is installed globally.

## Commands

| Command | Purpose |
|---|---|
| `atj rubric` | Print the canonical rubric it will actually use |
| `atj event init <id>` | Create an event from the template |
| `atj event validate <dir>` | Validate configuration, roster, status and versions |
| `atj event status <dir>` | Stage, gates, units, and the next safe action |
| `atj event advance <dir>` | Advance a stage; refuses while the gate is pending |
| `atj event gate <dir> <gate> <state>` | Record a stage audit result |
| `atj score <judgments-dir>` | Consolidate a judge panel |
| `atj matchup <input.json>` | Resolve an order-balanced head-to-head |
| `atj bracket build --event-dir <dir> --seed <seed>` | Draw a reproducible bracket |
| `atj bracket advance <bracket.json> --match <id> --from <report>` | Record a match winner and carry it forward |
| `atj bracket verify <bracket.json> --event-dir <event>` | Check a bracket and re-derive its constraints from the roster. `--reproduce <roster.json>` redraws from the recorded seed instead. The weaker check that trusts the file's own audit block must be asked for with `--structure-only`, so nothing reading an exit code mistakes it for a full verification |
| `atj event unit <dir> list` | Show the unit ledger and any unit whose inputs have changed |
| `atj event overrides <dir>` | List every stage gate a human bypassed with `--force-reason`. Exits non-zero while one is unreviewed; `--review <index> --official <role>` records that a person read it, never that it was justified |
| `atj event approve <paths>` | Set `approval_state` on event artifacts, with validation behind it |
| `atj render judgment <paths>` | Generate the scores table into a judgment from its own front matter |
| `atj render consolidated <paths>` | Generate the panel score block into a consolidated report |
| `atj intake <dir> <team> <source>` | Materialize, pin and enroll one submission |
| `atj validate reports <dir>` | Validate every artifact in an event |
| `atj validate publication <artifact>` | Gate one artifact before disclosure |
| `atj sandbox preflight` | Report whether verified isolation is available |
| `atj sandbox run <src> <cmd...>` | Run one command against a submission, isolated |
| `atj sandbox proxy up\|down\|status` | The egress proxy that makes an event's `network_allowlist` enforceable: an internal network with no route out and no resolver, and a deny-by-default filter |
| `atj ceremony <dir>` | Render the static ceremony view and dossiers |
| `atj demo check` | Re-derive every condition the sample event must demonstrate, recompute its totals, and re-verify both brackets |
| `atj release-check` | Every framework-level check required before a release |
| `atj personas` | Check the component registry against the agent and skill files |
| `atj schemas` | Self-check the shipped schemas |

Add `--json` to any command for machine-readable output. Exit codes: `0` success,
`1` validation or audit failure, `2` usage or environment error.

## Validation

Repeat the complete validation with:

```bash
python3 -m pytest tests/ -q \
  && python3 -m atj release-check \
  && python3 -m atj demo check \
  && python3 -m atj event validate events/sample-mock-2026 \
  && python3 -m atj validate reports events/sample-mock-2026 \
  && python3 tools/check_placeholders.py \
  && python3 -m atj bracket verify tests/fixtures/bracket-20-team/bracket.json \
       --reproduce tests/fixtures/bracket-20-team/roster.json \
  && python3 tools/check_placeholders.py
```

A wheel is verified the same way, and by CI rather than by a checklist: the build
stages the framework data into the package, and `The wheel installs and runs
outside the checkout` installs it into a fresh virtualenv and runs
`atj release-check` from `/tmp`. A release that would install a command unable to
find its own rubric fails the build instead.

`atj release-check` alone covers rubric totals, schema self-checks, the component
registry, template integrity, Claude component structure, the single-source rule,
version skew, and whether the sample event still demonstrates every required case.

## Sample event

`events/sample-mock-2026/` is a committed synthetic event: four invented teams,
53 artifacts, no real student data. It demonstrates a material disagreement, a
severe disagreement with an outlier, an initial `NE`, three adjudications, a
close-call matchup that returns no winner, an order-balanced matchup, and a
consolidation audit that fails and is then repaired.

Its judge scores are scripted fixture inputs, not model output, so the pipeline
is reproducible in CI without an LLM call. Every artifact records this.

`tests/fixtures/bracket-20-team/` is a separate 20-team bracket: 32 slots, four
preliminary matches, eight participants, twelve byes, reproducible from its seed.

## Repository layout

| Path | Contents |
|---|---|
| `framework/rubrics/` | Versioned evaluation contracts. The submission rubric is the source of all official weights. |
| `framework/policies/` | Evidence, independence, disagreement, execution safety, publication. |
| `framework/templates/` | The shape of every artifact. |
| `framework/personas.md` | Component registry: agent and skill versions with content digests. |
| `atj/` | Deterministic tooling. |
| `schemas/` | JSON Schema for every structured artifact. |
| `.claude/` | Project-local agents, skills, commands, hooks and settings. |
| `events/` | Event records. `_template` is the source; `sample-mock-2026` is the fixture. |
| `tests/` | Automated tests and fixtures. |
| `workspaces/` | Submission checkouts and sandbox state. Git-ignored. |

## Limitations

- **AI judgment is not deterministic.** See the top of this document.
- **Execution requires a container runtime.** `atj sandbox preflight` reports
  whether Podman or a reachable Docker daemon is available. Where neither is,
  execution is *unavailable*, not degraded: there is no host fallback, evidence
  is static inspection only, and affected criteria must be scored `NE`.
- **Hooks are guard rails, not a security boundary.** They run with the operator's
  own permissions and can be bypassed. The real controls are `atj validate`, the
  publication gate and the audit gates. Claude Code also ignores
  `permissions.allow` from project settings until the workspace is trusted.
- **Prompt-injection resistance is partial.** Submission text cannot change the
  rubric, the weights, an artifact's visibility, the publication gate or the
  judges' tool surface; those are mechanical and tested. It may still influence a
  judge's prose. See `tests/fixtures/prompt-injection/README.md`.
- **Judge independence is enforced by procedure and detected after the fact, not
  prevented by the tool surface.** The four judges hold read-only tools, but those
  tools are not path-restricted: a judge could read a sibling's report if one were
  already written into the event directory. The `judge-submission` skill therefore
  stages reports outside `events/` until all four complete, and
  `atj validate reports` flags near-duplicate wording between two judgments on the
  same team. That is a control and a detector, not a guarantee.
- **Several controls depend on a human doing their part.** The framework refuses
  to pass a stage gate without an audit artifact, refuses to advance a winner
  without a confirmed result or a recorded adjudication, and refuses to publish
  without a named approver. It cannot check that the audit was performed carefully,
  that the approver read what they approved, or that `--force-reason` was
  justified. `docs/implementation-detail.md` lists these explicitly.
- **Model cost is not trivial.** A four-judge panel plus two matchup passes per
  tournament match is roughly `4 x teams + 2 x matches` model invocations. Budget
  and measure before scaling to a real field.
- **Calibrate before it counts.** Run a dry event against sample projects and
  review the output with your officials before this decides a real award.

## Documentation

| Document | Purpose |
|---|---|
| `docs/operator-guide.md` | The procedure for running an event |
| `docs/implementation-detail.md` | What was built, why, and where the seams are |
| `docs/release-readiness-audit.md` | Baseline audit of v0.1.0-alpha |
| `docs/final-audit.md` | Independent audit of this release |
| `docs/agent-verification.md` | Live-model verification of the judge agents |
| `docs/implementation-plan.md` | Build and audit record |
| `docs/framework-fix-plan.md` | The 31 defects `live-trial-2026` found, and their disposition |
| `docs/0.5.0-beta-plan.md` | Proposed: what the next version and the next event are for |
| `docs/release-checklist.md` | What to verify before tagging a release |
| `docs/troubleshooting.md` | Common failures and what they mean |
| `docs/recovery-and-resume.md` | Recovering from an interruption |
| `docs/security-and-sandboxing.md` | Threat model and execution controls |
| `docs/tournament-operations.md` | Bracket and matchup operations |
| `docs/scoring-and-calibration.md` | Calibration and score monitoring |
| `docs/architecture.md` | How the pieces fit together |
| `CHANGELOG.md` | What changed, and what is still limited |
