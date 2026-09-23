---
event_id: trial-2-2026
override_id: ovr-trial-2-2026-bracket-affiliation
scope: stage
team_id: null
match_id: mu:trial-2-2026:final:01
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.1.0
persona: build-bracket@1.0.0
framework_commit: c728437466d0940734bee600765af298eebb062d
model_requested: not-applicable
model_used: not-applicable
started_at: "2026-09-23T10:47:00Z"
completed_at: "2026-09-23T10:49:58Z"
visibility: private
approval_state: approved
validation_state: valid
authorized_by: event-director
approved_by: event-director
approved_at: "2026-09-23T14:52:44Z"
---

# Manual Override Record

`atj bracket build` returned `feasible: false` on one hard constraint and the
build command said so: "An event official must accept these exceptions before
the draw is used." This record is that acceptance. Without it the draw may not
be used and the tournament cannot start.

## What was overridden

| Field | Value |
|---|---|
| Artifact | `events/trial-2-2026/bracket.json` |
| Framework result | `feasible: false`; `unsatisfied_hard_constraints: ["No avoidable same-affiliation or previous-finalist first-round match"]`, exception `team-scribe vs team-demos (affiliation beekeeper-lab)` |
| Override result | The exception is accepted. The draw is used as built, unmodified, at seed `trial-2-2026` and input digest `0fa1d02b4c6f44c3` |
| Category | rules exception |

No team, slot, seed, policy or constraint status was edited. `bracket.json`
still records `feasible: false` and still names the unsatisfied constraint. The
override changes what the event does with that result, not the result.

`scope` is `stage` and not `match` on purpose: what is accepted is the draw, and
`atj bracket build` reports the exception against the bracket rather than
against a pairing. `match_id` is populated because at this bracket size the
stage produced exactly one match and the exception is about that pairing. The
two fields do not disagree.

## Authority

`framework/policies/disagreement-and-adjudication.md:9` — "A human event
official owns disqualification, rules exceptions, and unresolved final ties."
That is the line that grants this authority. A bracket exception is a rules
exception, which `framework/templates/manual-override-record.md:34-35` also
lists among the decisions reserved to humans.

`events/trial-2-2026/event.md:103` names the official: `event-director` holds
all four reserved authorities and Gregg Reed holds that role. Rules exceptions
are not one of the four keys `event.md:23-27` declares under `officials` — the
framework reserves five decisions to humans and the event schema declares four
owners, which `audits/bracket.md` F5 records as a framework finding. The event
has one human official holding every authority it does declare, so the gap
changes nothing here about who decided.

`.claude/skills/build-bracket/SKILL.md` step 6 requires this record by name: "A
bracket with `feasible: false` must not be used until an event official accepts
the listed exceptions in writing. Record that acceptance as a manual override
record."

The event has one operator and no separation of duties, which
`event.md:103-107` states and `R3` in `docs/0.5.0-beta-plan.md` records. The
official accepting this exception is the same person who entered both
submissions. That is a known limit of this event and not a defect of this
record.

## Reason

Both eligible teams carry `affiliation_group: beekeeper-lab`
(`events/trial-2-2026/teams.md`), because both submissions are the operator's
own applications. Two teams make a bracket of size two, one match and one round.
Every possible draw pairs the two teams against each other, so there is no
assignment in which the constraint holds.

`framework/rubrics/bracket-assignment.md` anticipates this: "When perfect
separation is impossible, maximize the earliest round in which affiliated teams
can meet." The soft constraint `Affiliation separation maximized` reports
`maximized` for exactly that reason — round 1 is the only round there is. The
hard constraint reports `infeasible` rather than `violated`, which is the
tooling distinguishing an exception it could not avoid from one it created.

The purpose the affiliation rule serves — keeping teammates from eliminating one
another before the bracket has run — has no application at two teams from one
group. There is nothing to protect and no alternative to protect it with.

A participant could be shown this reason as written. Nothing here is private.

## Downstream effects

| Affected artifact | Effect | Re-run required |
|---|---|---|
| `events/trial-2-2026/bracket.json` | None. Unmodified by this record and still the source of every bracket value | no |
| `events/trial-2-2026/bracket.md` | Cites this record as the acceptance that permits the draw's use | no |
| `mu:trial-2-2026:final:01` | Proceeds. The matchup is judged on the head-to-head rubric, which does not read affiliation | no |
| `events/trial-2-2026/audits/bracket.md` | Must confirm this record exists and that the exception is the one `bracket.json` names | not yet written |

No score, winner or ranking is changed by this override, so nothing is marked
stale.

## Disclosure

| Audience | What is disclosed | Approved by |
|---|---|---|
| Panel and event record | This record in full | event-director |
| Both teams | That the only match is a same-affiliation final and why | event-director |
| Public artifacts | The same, if public artifacts are produced. Both teams belong to one group and the final pairs them; the bracket report says so and there is nothing to withhold | event-director |

## Validation

- [x] Human official identified by role — `authorized_by: event-director`, the
      role `event.md:96-107` defines and grants this authority
- [x] Authority cited — `event.md:96-107` and `build-bracket@1.0.0` step 6
- [x] Original artifact preserved unmodified — `bracket.json` still reports
      `feasible: false` and still lists the unsatisfied constraint; this record
      sits beside it and edits nothing
- [x] Downstream artifacts marked stale — none are stale. No score, winner or
      placement moves, and the table above says so artifact by artifact
- [x] Disclosure decided — the reason is stated in terms a participant could be
      shown and carries nothing private
