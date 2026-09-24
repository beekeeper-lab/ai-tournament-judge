---
event_id: trial-2-2026
override_id: ovr-trial-2-2026-model-substitution-audits
scope: event
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.1.0
persona: run-judging-event@1.0.0
framework_commit: e44385b78dead3437ff7b09942378db7876713b9
model_requested: not-applicable
model_used: not-applicable
started_at: "2026-09-24T12:13:16Z"
completed_at: "2026-09-24T12:13:16Z"
visibility: private
approval_state: approved
validation_state: valid
authorized_by: event-director
approved_by: event-director
approved_at: "2026-09-24T12:13:21Z"
approval_note: Accepted by the event-director in session 2026-09-24 ('yes to all'); closes final audit FA2
---

# Manual Override Record

This record closes `audits/final.md` FA2. The event-director accepted the
recommendation on 2026-09-24 in the final-audit session ("yes to all"). It extends
`ovr-trial-2-2026-model-substitution`, which stays unchanged, to the three stage
audits that record the same substitution.

## What was overridden

| Field | Value |
|---|---|
| Artifact | `events/trial-2-2026/event.md:16` front matter `model_requested: claude-opus-5` |
| Framework result | `audits/tournament.md:13`, `audits/dossiers.md:13` and `audits/final.md:13` record `model_used: claude-opus-5-5[1m]`. `ovr-trial-2-2026-model-substitution` names five artifacts and none of these three |
| Override result | `claude-opus-5-5[1m]` is accepted for the tournament, dossiers and final audits. `event.md` and the three audits are not changed |
| Category | rules exception |

## Authority

The same as `ovr-trial-2-2026-model-substitution`:
`framework/policies/disagreement-and-adjudication.md:9` gives rules exceptions to
"a human event official", and `event-director` is the only official this event
names (`event.md:23-27`, `:103`). `audits/final.md` FA2 is why this record
exists, not its authority.

## Reason

Each audit records its model truthfully, so the deviation is visible. No audit
scores a submission, and every audit's calculations were re-derived by `atj`
commands whose output does not depend on the model. Re-running three passed audits
to change a model identifier would reopen closed stages with no stated effect on any
verdict.

## Downstream effects

| Affected artifact | Effect | Re-run required |
|---|---|---|
| `audits/tournament.md`, `audits/dossiers.md`, `audits/final.md` | none; `model_used` stays as recorded | no |

## Disclosure

| Audience | What is disclosed | Approved by |
|---|---|---|
| Panel | this record | event-director |
| Teams | nothing; audits are private | event-director |
| Public | nothing | event-director |

## Validation

- [x] Human official identified by role
- [x] Authority cited
- [x] Original artifact preserved unmodified
- [x] Downstream artifacts marked stale — none are stale; no value changed
- [x] Disclosure decided
