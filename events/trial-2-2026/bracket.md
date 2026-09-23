---
event_id: trial-2-2026
policy: bracket-assignment@1.0.0
rubric: submission-evaluation@1.1.0
persona: build-bracket@1.0.0
framework_commit: c728437466d0940734bee600765af298eebb062d
roster_version: 1
team_count: 2
bracket_size: 2
bye_count: 0
bye_policy: performance-qualified
random_seed: trial-2-2026
input_digest: 0fa1d02b4c6f44c3
feasible: false
override_ids: [ovr-trial-2-2026-bracket-affiliation]
model_requested: not-applicable
model_used: not-applicable
started_at: "2026-09-23T01:55:10Z"
completed_at: "2026-09-23T10:51:23Z"
visibility: private
approval_state: draft
validation_state: unvalidated
---

# Bracket Report

`bracket.json` is what `atj bracket build` produced and is the source of every
value here. The two tables below are `atj/render.py`'s `bracket_tables` output
over that file, written in whole and not transcribed.

**This draw is `feasible: false`.** One hard constraint could not be satisfied
and its acceptance is recorded at
`overrides/ovr-trial-2-2026-bracket-affiliation.md`. The draw may not be used
without that record.

## Frozen inputs

Roster version 1, frozen at the intake gate on 2026-09-21 and unmodified since.
2 eligible teams, bracket size 2, format `single-elimination`, 1 round.

| Team | Consolidated score used for byes | Affiliation group | Previous finalist |
|---|---|---|---|
| team-scribe | **not used** (no byes); none exists — `finalized: false`, `total: null` | beekeeper-lab | no |
| team-demos | **not used** (no byes); none exists — `finalized: false`, `total: null` | beekeeper-lab | no |

Neither team has an official total. `adj:trial-2-2026:team-scribe:01` and
`adj:trial-2-2026:team-demos:01` record the event director accepting an `NE`
rather than supplying a score, so both panels stay unfinalized by decision and
the provisional sums 32.5 and 52.5 are not official and not usable for seeding.

No score was read by this assignment, proved two ways. By code path:
`atj/bracket.py:161-162` is a `count == 0` guard that returns from `choose_byes`
before the first `.score` access, which is at `:169`; 2 teams is an exact power
of two, so `count` is 0. By
experiment: rebuilding at seed `trial-2-2026` under six score permutations —
both `None`, the two provisional sums in each order, a tie at 0.0, and 100.0
against 1.0 in each order — leaves `rounds`, `constraint_audit` and `bye_teams`
identical every time. `input_digest` does move across those rebuilds, which is
correct: `atj/bracket.py:911` folds each team's score into the digest so a
changed roster is detectable. The digest detects change; it does not steer the
draw.

Both teams carry `affiliation_group: beekeeper-lab`
(`teams.md:11-12`), because both submissions are the operator's own
applications. That is what makes the draw infeasible, below.

## Assignment result

| Slot | Entrant A | Entrant B | Entry | Notes |
|---:|---|---|---|---|
| 1 | team-demos | team-scribe | final | |

Byes: none. `bye_policy` is `performance-qualified` and it never runs.

The single match is `mu:trial-2-2026:final:01`, round `final`, round index 1,
entrants `team-demos` and `team-scribe`. Drawn with `winner: null`; `atj bracket
advance` recorded `winner: team-demos` on 2026-09-23 from `matchups/mu-final-01.md`,
after the tournament stage audit. Nothing else in the draw changed.
Presentation order in the bracket is not presentation order in the matchup: the
head-to-head pass is order-balanced and `judge-matchup@1.0.0` runs both.

## Constraint audit

6 constraints evaluated: 3 hard satisfied, 1 hard not-applicable, 1 hard
**infeasible**, 1 soft maximized. `unsatisfied_hard_constraints` holds one
entry.

| Constraint | Kind | Status | Detail |
|---|---|---|---|
| Every eligible team appears exactly once | hard | satisfied | 2 of 2 teams placed |
| Bye count and match count match the bracket size | hard | satisfied | 0 byes, 1 first-round matches, 1 first-round slots |
| Bye policy 'performance-qualified' applied consistently | hard | satisfied | no byes: the team count is an exact power of two |
| Previous champion and runner-up in opposite halves | hard | not-applicable | previous finalists present: [] |
| No avoidable same-affiliation or previous-finalist first-round match | hard | infeasible | affiliation 'beekeeper-lab' holds 2 of 2 play-in teams; at most 1 can be paired without a same-affiliation match |
|  |  | exception | team-scribe vs team-demos (affiliation beekeeper-lab) |
| Affiliation separation maximized | soft | maximized | beekeeper-lab (2 teams): earliest meeting round 1 |
|  |  | exception | team-scribe vs team-demos (affiliation beekeeper-lab) |

### The infeasible constraint

Both eligible teams are in one affiliation group, the bracket has one match, and
every possible draw pairs them. There is no assignment in which
`No avoidable same-affiliation or previous-finalist first-round match` holds.
The tooling reports it `infeasible` rather than `violated`, which is the
distinction between an exception it could not avoid and one it created; the soft
constraint below it reports `maximized` for the same reason, round 1 being the
only round there is.

`event.md:91-94` pre-registered this and the prediction did not hold, though
not through any misreading. It expected `bracket-assignment.md` to treat the
shared affiliation "as a cost rather than a constraint, so the bracket record is
expected to carry that cost as a reason string rather than fail". That is what
the policy says. `framework/rubrics/bracket-assignment.md:22` lists affiliation
separation under Priority as something to "Maximize", and `:27-30` give targets
— opposite halves at two teams, separate quarters at three or four — and a
fallback when perfect separation is impossible. Nowhere does the policy declare
any affiliation rule a hard constraint.

`atj/bracket.py:548-554` supplies the hardness the policy does not, naming
`No avoidable same-affiliation or previous-finalist first-round match` at `:549`
and giving it `kind: hard` at `:550`; `:758-761` collects every hard constraint at `violated` or
`infeasible` and `:775` is where `feasible` is assigned from that. So the draw
returned `feasible: false` on a rule its own policy states only as a priority
and a target.

The event's expectation matched the policy and the implementation did not. That
divergence is the finding, recorded as `audits/bracket.md` N5 and carried to
`docs/0.5.0-beta-plan.md` as `W20`. It changes nothing about the pairing — at two teams from
one group there is no alternative under either reading — but it is why the draw
is `feasible: false` and why this stage needed a human override at all. Under
the policy as written the constraint is soft, `atj/bracket.py:758-761` collects
nothing, `:775` assigns `feasible: true`, and no override record would have been
required.

Accepted by the event director at
`overrides/ovr-trial-2-2026-bracket-affiliation.md`, category `rules exception`,
authority `framework/policies/disagreement-and-adjudication.md:9` and
`event.md:103`. `bracket.json` is unmodified by that acceptance and still
records `feasible: false` and still names the constraint.

## Reproduction

```
python3 -m atj bracket build --event-dir events/trial-2-2026 --seed trial-2-2026
```

Roster version 1, input digest `0fa1d02b4c6f44c3`. Rebuilding from this seed
against the frozen roster reproduces `rounds`, `constraint_audit`,
`input_digest` and `bye_teams` identically. `framework_commit` is read from git
at build time (`atj/versions.py:216-238`, the `framework_commit` function; the
`git rev-parse HEAD` call is at `:225`) and is not derived from the seed, so it
is the one field that moves between rebuilds; it is
`c728437466d0940734bee600765af298eebb062d` here.

```
python3 -m atj bracket verify events/trial-2-2026/bracket.json --event-dir events/trial-2-2026
```

re-derives every constraint from the roster and reports
`PASS (constraints re-derived from the roster)`. Verification passing and the
draw being infeasible are not in tension: `verify` checks that the recorded
constraint audit is the one the roster produces, and the roster produces an
infeasible one.

- [x] Every eligible team appears once — hard constraint `satisfied`, 2 of 2
- [x] Bye count is correct — hard constraint `satisfied`, 0 byes for 1 match and
      1 first-round slot
- [x] Previous finalists are separated when feasible — `not-applicable`, no
      previous finalists exist; this is the event's first tournament
- [x] Affiliation separation is maximized — soft constraint `maximized`; the
      hard form is infeasible at this roster and is accepted, not ignored
- [x] Exceptions are documented — one, in `bracket.json`'s constraint audit, in
      the table above, and in the override record this report cites
