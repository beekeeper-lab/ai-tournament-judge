---
name: build-bracket
description: Builds a reproducible constrained-random tournament bracket from audited eligible teams.
---

# Build Bracket

Read the event configuration, eligible consolidated results, `framework/rubrics/bracket-assignment.md`, and bracket report template.

1. Freeze the eligible team list and relevant affiliation and prior-finalist metadata.
2. Resolve the configured bye policy before drawing the bracket.
3. Use a supplied seed or generate and record one before assignment.
4. Run `python3 -m atj bracket build --event-dir <event> --seed <seed> --output <event>/bracket.json`; never place teams by hand.
5. Run `python3 -m atj bracket verify <event>/bracket.json --reproduce <roster.json>` and read the constraint audit it emits. Every constraint reports satisfied, maximized, violated, not-applicable, or infeasible.
6. A bracket with `feasible: false` must not be used until an event official accepts the listed exceptions in writing. Record that acceptance as a manual override record.
7. Write the bracket report and audit it before tournament matchups begin.

Changing the team list, seed, or policy invalidates the draw and requires a versioned redraw before any matchup is judged.
