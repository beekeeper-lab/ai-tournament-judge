---
event_id: trial-2-2026
override_id: ovr-trial-2-2026-model-substitution
scope: event
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.1.0
persona: run-judging-event@1.0.0
framework_commit: c0a55dfb6c2339c691c13bfe3a1ce3fe42eb126c
model_requested: not-applicable
model_used: not-applicable
started_at: "2026-09-23T20:18:07Z"
completed_at: "2026-09-23T20:18:07Z"
visibility: private
approval_state: draft
validation_state: valid
authorized_by: event-director
---

# Manual Override Record

This record closes `audits/tournament.md` F8. The event-director decided on
2026-09-23, in the dossiers-stage session, to accept the substitution with a dated
record and no re-run.

## What was overridden

| Field | Value |
|---|---|
| Artifact | `events/trial-2-2026/event.md` front matter `model_requested: claude-opus-5` |
| Framework result | `matchup-passes/mu-final-01-pass-a-first.md`, `matchup-passes/mu-final-01-pass-b-first.md`, `matchups/mu-final-01.md`, `dossiers/team-demos.md` and `dossiers/team-scribe.md` record `model_used: claude-opus-5-5[1m]`. Nothing recorded a decision to accept it |
| Override result | `claude-opus-5-5[1m]` is accepted for the tournament and dossiers stages. `event.md` is not changed. The eight panel judgments record `claude-opus-5` and are not affected. The three matchup artifacts also record `model_requested: opus`, not `claude-opus-5`; that field is left as recorded |
| Category | rules exception |

## Authority

`framework/policies/disagreement-and-adjudication.md:9`: "A human event official
owns disqualification, rules exceptions, and unresolved final ties." Departing from
`event.md`'s `model_requested` is a rules exception. `event.md:103-105` records that
`event-director` holds all four named authorities, none of which is rules
exceptions, and that with a single operator no other official is available.
`audits/tournament.md` F8 is why this record exists, not its authority.

## Reason

Both matchup passes ran on the same model, so presentation order was balanced
under one model and the order check in `matchups/mu-final-01.md` is unaffected.
The matchup judges compared the panel judgments as evidence and did not re-score
them. A re-run would reopen a closed, audited stage to change a model identifier
without a stated effect on the outcome. The deviation stays visible in every
affected artifact's `model_used`, which is left as recorded.

## Downstream effects

| Affected artifact | Effect | Re-run required |
|---|---|---|
| `matchups/mu-final-01.md` and both pass reports | none; `model_used` stays as recorded | no |
| `dossiers/team-demos.md`, `dossiers/team-scribe.md` | none; `model_used` stays as recorded | no |

## Disclosure

| Audience | What is disclosed | Approved by |
|---|---|---|
| Panel | this record | event-director |
| Teams | the two dossiers carry `model_used` in front matter; no dossier body mentions the substitution | event-director |
| Public | nothing; `public/mu-final-01.md` names no model | event-director |

## Validation

- [x] Human official identified by role
- [x] Authority cited
- [x] Original artifact preserved unmodified
- [x] Downstream artifacts marked stale — none are stale; no value changed
- [x] Disclosure decided
