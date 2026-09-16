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

| Agent ID | Version | Role | Content digest |
|---|---|---|---|
| judge-backend | 1.0.0 | initial judge | 7571907d5863c02d |
| judge-frontend-ux | 1.0.0 | initial judge | 34886aeec5849399 |
| judge-security-ops | 1.0.0 | initial judge | bd24c6d8650ebc79 |
| judge-product-agentic | 1.0.0 | initial judge | 401cb9c840e00a99 |
| panel-consolidator | 1.0.0 | consolidator | b7062819bfbde0d0 |
| matchup-judge | 1.0.0 | comparative judge | 06f6ff913e17f638 |
| prepare-submission | 1.0.0 | skill | 4b6f99855da6d7eb |
| judge-submission | 1.0.0 | skill | 40bf61069212948f |
| consolidate-judgments | 1.0.0 | skill | 5f6a8d87f008b947 |
| build-bracket | 1.0.0 | skill | 9fdf42e23550bbcf |
| judge-matchup | 1.0.0 | skill | b4a93e8cbfaca472 |
| build-team-dossier | 1.0.0 | skill | 39213ede471ffe71 |
| audit-judging-run | 1.0.0 | skill | d43476babfebee41 |
| run-judging-event | 1.0.0 | skill | 1871381348a82b61 |
| judging-auditor | 1.0.0 | auditor | 2fb3edc39c0a5260 |
## Change procedure

1. Edit the agent or skill definition.
2. Increment its version here (patch for wording, minor for emphasis, major for
   scope or authority).
3. Run `atj personas --refresh` to recompute the digest.
4. Decide explicitly whether affected artifacts must be re-run, and record that
   decision in the event's status ledger.

A persona version never changes the shared rubric, weights, or formulas.
