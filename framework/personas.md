---
registry_id: personas
version: 1.0.0
---

# Component Registry

Canonical version record for every project-local Claude component that produces
an official artifact: the agents in `.claude/agents/` and the skills in
`.claude/skills/`. Their definitions stay in plain Claude Code format; this file
is the only place their versions are declared.

`content_digest` is the first 16 hex characters of the SHA-256 of the component's
definition file. `atj personas` recomputes it. **An edited component fails
validation until its version is incremented and the digest is refreshed**, which
is what stops a persona or a workflow from changing silently underneath an active
event.

`writes` says who persists the component's artifact. A path means the component
writes there itself and must hold the `Write` tool. `-` means it returns its
completed document as its final message and the orchestrator writes the file --
the deliberate arrangement for every component that reads untrusted submission
content, because a judge that can write a file is a judge an injected
instruction can aim at one.

Either way it is a contract, not a description. `atj release-check` fails when a
component declares a path and its definition withholds `Write`, and when it
declares `-` and holds `Write` anyway. Before this column existed, four judges
ran a whole event under a skill that required each to produce a judgment document
while their definitions granted `Read, Grep, Glob`; both facts were written down,
in different files, and nothing read them together.

| Agent ID | Version | Role | Writes | Content digest |
|---|---|---|---|---|
| judge-backend | 1.1.0 | initial judge | - | 4d53b23833d3b78d |
| judge-frontend-ux | 1.1.0 | initial judge | - | 37aac548ad01a0d6 |
| judge-security-ops | 1.1.0 | initial judge | - | a634b3a9bcef35b1 |
| judge-product-agentic | 1.1.0 | initial judge | - | 5e63b35eaec70da9 |
| panel-consolidator | 1.1.0 | consolidator | - | aeedd15f1ff0e187 |
| matchup-judge | 1.1.0 | comparative judge | - | 688762e6ec10147b |
| prepare-submission | 1.1.0 | skill | - | c7c0aa083a37e284 |
| judge-submission | 1.1.0 | skill | - | 7f3ec4b12a898ed5 |
| consolidate-judgments | 1.0.0 | skill | - | 5f6a8d87f008b947 |
| build-bracket | 1.0.0 | skill | - | 9fdf42e23550bbcf |
| judge-matchup | 1.0.0 | skill | - | b4a93e8cbfaca472 |
| build-team-dossier | 1.0.0 | skill | - | 39213ede471ffe71 |
| audit-judging-run | 1.0.0 | skill | - | d43476babfebee41 |
| run-judging-event | 1.0.0 | skill | - | 1871381348a82b61 |
| judging-auditor | 1.1.0 | auditor | events/<event>/audits/ | bc5d7a79103c139b |## Superseded versions

Append-only. A row here records a version that has been retired: **no new
artifact may pin it, and every artifact that already pins it stays valid.**

Without this table a version bump falsifies the record of every completed event
judged under the old version. `atj validate reports` reported four blocking
version mismatches against `live-trial-2026` the moment `judge-backend` was
bumped, and the only repair available inside a completed event is to rewrite a
frozen artifact — the offence the audit chain exists to prevent. `retired_on` is
the date the replacement landed; `content_digest` is the digest the retired
version carried, kept so a historical artifact's provenance can still be checked
against something.

| Agent ID | Version | Retired | Superseded by | Content digest |
|---|---|---|---|---|
| judge-backend | 1.0.0 | 2026-09-18 | 1.1.0 | 7571907d5863c02d |
| judge-frontend-ux | 1.0.0 | 2026-09-18 | 1.1.0 | 34886aeec5849399 |
| judge-security-ops | 1.0.0 | 2026-09-18 | 1.1.0 | bd24c6d8650ebc79 |
| judge-product-agentic | 1.0.0 | 2026-09-18 | 1.1.0 | 401cb9c840e00a99 |
| panel-consolidator | 1.0.0 | 2026-09-18 | 1.1.0 | b7062819bfbde0d0 |
| matchup-judge | 1.0.0 | 2026-09-18 | 1.1.0 | 06f6ff913e17f638 |
| judging-auditor | 1.0.0 | 2026-09-18 | 1.1.0 | 2fb3edc39c0a5260 |

## Change procedure

1. Edit the agent or skill definition.
2. Increment its version here (patch for wording, minor for emphasis, major for
   scope or authority).
3. Run `atj personas --refresh` to recompute the digest.
4. Decide explicitly whether affected artifacts must be re-run, and record that
   decision in the event's status ledger.

A persona version never changes the shared rubric, weights, or formulas.
