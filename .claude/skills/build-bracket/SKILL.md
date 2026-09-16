---
name: build-bracket
description: Builds a reproducible constrained-random tournament bracket from audited eligible teams.
---

# Build Bracket

Read the event configuration, eligible consolidated results, `framework/rubrics/bracket-assignment.md`, and bracket report template.

1. Freeze the eligible team list and relevant affiliation and prior-finalist metadata.
2. Resolve the configured bye policy before drawing the bracket.
3. Use a supplied seed or generate and record one before assignment.
4. Run `scripts/build_bracket.py`; do not manually place teams.
5. Validate uniqueness, slot count, byes, prior-finalist separation, and best-effort school separation.
6. Record every unsatisfied or waived constraint and its reason.
7. Write the bracket report and audit it before tournament matchups begin.

Changing the team list, seed, or policy invalidates the draw and requires a versioned redraw before any matchup is judged.
