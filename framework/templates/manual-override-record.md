---
event_id: EVENT-ID
override_id: OVERRIDE-ID
scope: team
team_id: TEAM-ID
match_id: null
commit: IMMUTABLE-COMMIT
evidence_package_id: EVIDENCE-ID
rubric: submission-evaluation@1.1.0
persona: PERSONA@VERSION
framework_commit: FRAMEWORK-COMMIT
model_requested: not-applicable
model_used: not-applicable
started_at: YYYY-MM-DDTHH:MM:SSZ
completed_at: YYYY-MM-DDTHH:MM:SSZ
visibility: private
approval_state: draft
validation_state: unvalidated
authorized_by: HUMAN-OFFICIAL-ROLE
---

# Manual Override Record

`persona` is what produced this document and must resolve in
`framework/personas.md` as `name@x.y.z`. `authorized_by` is who decided, and
carries the human official's role. The registry pins a file digest, which a human
does not have, so a human's name never goes in `persona` — the same distinction
D10 settled for adjudications, one artifact over. `HUMAN-OFFICIAL` was one
hyphenated word short of the real placeholder and so was never caught.

A human official has overridden a framework result. Overrides are legitimate and
expected for the decisions reserved to humans. They are never silent.

Reserved to humans: disqualification, unresolved final ties, rules exceptions,
security escalation, publication approval.

## What was overridden

| Field | Value |
|---|---|
| Artifact | path |
| Framework result | what the tooling produced |
| Override result | what the official decided |
| Category | disqualification / tie / rules exception / security / publication / other |

## Authority

Cite the event rule or published policy that grants this authority. An override
with no cited authority is a finding.

## Reason

State the reason in terms a participant could be shown. If the reason cannot be
disclosed to participants, say so and record where the private explanation lives.

## Downstream effects

| Affected artifact | Effect | Re-run required |
|---|---|---|

An override that changes a score or a winner invalidates dependent artifacts.
Mark them stale rather than editing them in place.

## Disclosure

| Audience | What is disclosed | Approved by |
|---|---|---|

## Validation

- [ ] Human official identified by role
- [ ] Authority cited
- [ ] Original artifact preserved unmodified
- [ ] Downstream artifacts marked stale
- [ ] Disclosure decided
