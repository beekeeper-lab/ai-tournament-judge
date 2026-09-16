---
registry_id: personas
version: 1.0.0
---

# Persona Registry

Canonical version record for every project-local Claude agent used to produce an
official artifact. Agent definitions live in `.claude/agents/` in plain Claude
Code format; this file is the only place their versions are declared.

`content_digest` is the first 16 hex characters of the SHA-256 of the agent file.
`atj validate personas` recomputes it. **An edited persona fails validation until
its version is incremented and the digest is refreshed**, which is what stops a
persona from changing silently underneath an active event.

| Agent ID | Version | Role | Content digest |
|---|---|---|---|
| judge-backend | 1.0.0 | initial judge | 7571907d5863c02d |
| judge-frontend-ux | 1.0.0 | initial judge | 34886aeec5849399 |
| judge-security-ops | 1.0.0 | initial judge | bd24c6d8650ebc79 |
| judge-product-agentic | 1.0.0 | initial judge | 401cb9c840e00a99 |
| panel-consolidator | 1.0.0 | consolidator | b7062819bfbde0d0 |
| matchup-judge | 1.0.0 | comparative judge | 06f6ff913e17f638 |
| judging-auditor | 1.0.0 | auditor | 2fb3edc39c0a5260 |
## Change procedure

1. Edit the agent definition.
2. Increment its version here (patch for wording, minor for emphasis, major for
   scope or authority).
3. Run `atj personas --refresh` to recompute the digest.
4. Decide explicitly whether affected artifacts must be re-run, and record that
   decision in the event's status ledger.

A persona version never changes the shared rubric, weights, or formulas.
