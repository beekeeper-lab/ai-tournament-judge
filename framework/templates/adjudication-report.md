---
event_id: EVENT-ID
adjudication_id: ADJUDICATION-ID
question: the single decision this adjudication settles, stated as a question
scope: team
team_id: TEAM-ID
match_id: null
criterion: null
trigger: severe-disagreement
advances_team: null
commit: IMMUTABLE-COMMIT
evidence_package_id: EVIDENCE-ID
rubric: submission-evaluation@1.1.0
persona: PERSONA@VERSION
framework_commit: FRAMEWORK-COMMIT
model_requested: MODEL-REQUESTED
model_used: MODEL-USED
started_at: YYYY-MM-DDTHH:MM:SSZ
completed_at: YYYY-MM-DDTHH:MM:SSZ
visibility: private
approval_state: draft
validation_state: unvalidated
resolution: unresolved
decided_by: HUMAN-OFFICIAL-ROLE
decision_authority: human-official
substitution_reason: null
amendments: []
---

# Adjudication Report

`decided_by` is the event official's role, and it must be one the event
configuration names. `decision_authority` says which kind of decision this was:
`human-official` when that official decided, and `agent-substituted` when an agent
stood in, which requires `substitution_reason` and can never move an official
total. Leaving the field out means the same thing as substituting, and is treated
the same way.

`resolution_detail` plus `score_override` carry the outcome. An `NE` may be
*cleared* by supplying `score_override.resolved_score`, or **accepted** by
setting it to `NE`, which records that the official reviewed the criterion and
the `NE` stands. An accepted `NE` still leaves the panel unfinalized, because the
rubric permits no official total while a criterion is `NE` — but it is
unfinalized by decision, and `atj score` stops asking for an adjudication that
has already happened.

`amendments` is append-only. An approved record is never silently edited: a
correction is disclosed as an entry with its own `amended_at`, `reason` and
`amended_by`, and the trail must read forward from the record's own
`completed_at`.

Adjudication resolves a specific disputed question. It is **not** a rescore of the
project and it never edits an original report. Original judgments are immutable;
this record attaches to them.

`persona` records **what produced this document**, not who decided. It must name a
component registered in `framework/personas.md` as `name@x.y.z` — the skill or
agent that ran the adjudication, such as `run-judging-event` or
`judging-auditor` at the version the registry declares for it. `atj validate`
rejects any value that is not in that registry, so a human's name or role never
goes here. **Who decided** is `decided_by`, which is required and carries the
human official's role. The two fields answer different questions and an
adjudication normally fills in both.

## Question

State the single question under adjudication in one sentence.

## Trigger

One of: `unresolved-ne`, `severe-disagreement`, `possible-outlier`,
`contradictory-facts`, `order-disagreement`, `close-call`, `rules-exception`,
`security-escalation`. Cite the artifact and calculation that raised it.

## Disputed claims

| Source artifact | Claim | Evidence cited | Class |
|---|---|---|---|

Evidence class is direct observation, artifact evidence, team claim, or inference.

## Evidence reviewed

List only evidence already present in the pinned evidence package. Adjudication
does not gather new evidence about the project; if new evidence is required, that
is a finding, not a resolution.

## Factual resolution

State what the evidence establishes, what it does not, and which disputed claim
is supported. Write "not resolvable from the available evidence" when that is
the answer.

## Impact on the result

| Affected criterion or outcome | Before | After | Mechanism |
|---|---|---|---|

`Mechanism` records how the change took effect: an added panel-level resolution,
an `NE` cleared by located evidence, or no change.

## Confidence

`low` / `medium` / `high`, with the reason.

## Human decision

For a matchup adjudication, record the advancing team in the `advances_team`
front-matter field. `atj bracket advance` reads it from there and refuses to act
without it; prose is not a decision a tool can safely parse.

Required for disqualification, rules exceptions, unresolved final ties, security
escalation, and publication. Record the deciding role, the decision, and the date.
Leave `resolution: referred-to-human` until a human has actually decided.

## Validation

- [ ] Question is narrow and answerable
- [ ] Every cited artifact resolves
- [ ] No original report was modified
- [ ] Impact recalculated by `atj score`, not by hand
- [ ] Human decision recorded where policy requires one
- [ ] `persona` names a component registered in `framework/personas.md`;
      the deciding human is in `decided_by`, never in `persona`
