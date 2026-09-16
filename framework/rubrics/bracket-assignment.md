---
policy_id: bracket-assignment
version: 1.0.0
format: single-elimination
seeding_mode: constrained-random
default_bye_policy: performance-qualified
record_random_seed: true
---

# Bracket Assignment Policy

Bracket assignment is a reproducible constraint process, not another judgment of team quality.

## Priority

1. Produce a valid bracket containing every eligible team exactly once.
2. Apply the declared bye policy consistently.
3. Put the previous champion and runner-up in opposite halves when both participate.
4. Maximize separation among teams sharing an `affiliation_group` such as a school.
5. Randomize every remaining choice using the recorded seed.

## Affiliation separation

- Two teams from one group: target opposite halves.
- Three or four: target separate quarters.
- More than four: distribute across the smallest available regions before repeating a region.
- When perfect separation is impossible, maximize the earliest round in which affiliated teams can meet.

## Byes

The event must select one policy before drawing:

- `performance-qualified`: highest consolidated scores receive byes; cutoff ties use seeded randomness.
- `random-lottery`: all eligible teams have equal seeded-random bye probability.
- `banded-lottery`: eligibility is divided into declared performance bands, then randomized within bands.

For 20 teams in single elimination, eight teams play four preliminary matches and twelve receive byes into the round of 16.

The final report records inputs, seed, policy, slots, byes, satisfied constraints, exceptions, and the reason for every non-random restriction. Changing inputs or rules invalidates the bracket.
