---
event_id: live-trial-2026
policy: bracket-assignment@1.0.0
rubric: submission-evaluation@1.0.0
persona: build-bracket@1.0.0
framework_commit: 1e761e639141d099f975cd6b4e3efaa296e6602f
roster_version: 1
team_count: 2
bracket_size: 2
bye_count: 0
bye_policy: performance-qualified
random_seed: live-trial-2026
input_digest: 5bd7a2f7e711e721
feasible: true
model_requested: not-applicable
model_used: not-applicable
started_at: "2026-09-17T22:50:00Z"
completed_at: "2026-09-17T22:50:00Z"
visibility: private
approval_state: draft
validation_state: unvalidated
---

# Bracket Report

Generated from `bracket.json` by script, not transcribed. `bracket.json` is the
artifact `atj bracket build` produced and is the source of every value here.

## Frozen inputs

Roster version 1, frozen at commit `6321a18` and unmodified since.
2 eligible teams, bracket size 2, format `single-elimination`.

| Team | Consolidated score used for byes | Affiliation group | Previous finalist |
|---|---|---|---|
| team-ledger | **not used** (no byes) | south-campus | no |
| team-podcast | **not used** (no byes); none exists — `finalized: false`, `display_total: null` | north-campus | no |

No score was read by this assignment. The bye policy is `performance-qualified`, which
would consume a consolidated score, but `2` teams is an exact power of two and
yields `0` byes, so the policy never runs. The bracket audit proved this twice:
by code path (`atj/bracket.py:160-161` returns before any `.score` access at
`count == 0`) and by experiment (rebuilding under five score permutations, including
team-podcast's unofficial provisional 58.25, leaves `rounds` and `constraint_audit`
bit-identical). team-podcast's missing official total therefore does not affect this
bracket, as `adjudications/team-podcast-reliability-ne.md` predicted.

## Assignment result

| Slot | Team or bye | Region | Entry round | Constraint notes |
|---:|---|---|---|---|
| 1 | team-ledger vs team-podcast | not-applicable | final | `mu:live-trial-2026:final:01` |

Byes: none.

**Result:** `team-ledger` advances from `mu:live-trial-2026:final:01`,
recorded into `bracket.json` by `atj bracket advance` from the private matchup report.
Combined margin +35.00, outcome `confirmed`, no adjudication required.

## Constraint audit

5 hard constraints evaluated: 4 satisfied, 2 not-applicable.
`unsatisfied_hard_constraints` is empty.

| Constraint | Status | Evidence or exception |
|---|---|---|
| Every eligible team appears exactly once | satisfied | 2 of 2 teams placed |
| Bye count and match count match the bracket size | satisfied | 0 byes, 1 first-round matches, 1 first-round slots |
| Bye policy 'performance-qualified' applied consistently | satisfied | no byes: the team count is an exact power of two |
| Previous champion and runner-up in opposite halves | not-applicable | previous finalists present: [] |
| No avoidable same-affiliation or previous-finalist first-round match | satisfied | a conflict-free play-in pairing was available and used |
| Affiliation separation maximized | not-applicable | no affiliation group has two or more teams |

## Reproduction

```
python3 -m atj bracket build --event-dir events/live-trial-2026 --seed live-trial-2026
```

Roster version 1, input digest `5bd7a2f7e711e721`. Rebuilding from this seed
against the frozen roster reproduces `rounds`, `constraint_audit`, `input_digest` and
`bye_teams` identically. `framework_commit` is read from git at build time
(`atj/versions.py:144-164`) and is not derived from the seed, so it is the one field
that moves between rebuilds; it is `1e761e639141d099f975cd6b4e3efaa296e6602f` here.

`atj bracket verify events/live-trial-2026/bracket.json --event-dir events/live-trial-2026`
re-derives every constraint from the roster and passes.
