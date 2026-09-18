# Troubleshooting

Error messages carry a stable code (`canon`, `version`, `schema`, `validation`,
`state`, `constraint`, `safety`) so you can match on the code rather than prose.

## `canon: framework root not found`

You ran `atj` from outside a checkout, or the rubric is missing. Pass `--root
/path/to/repo`, or run from the repository root.

## `version: rubric mismatch`

An artifact pins a rubric version that is not the canonical one. This is fatal by
design: it means either the rubric moved under an in-flight event, or the
artifact came from a different framework version. Do not edit the artifact to
match. Decide explicitly whether affected work is re-run, and record that
decision in the event's status ledger.

## `version: persona mismatch` or `persona changed without a version bump`

An agent or skill file was edited without incrementing its version in
`framework/personas.md`. Increment the version, then
`python3 -m atj personas --refresh`. Then decide whether artifacts produced by
the old version must be re-run.

## `version: close_call_band ... is below the rubric floor`

An event tried to narrow the close-call band. Narrowing converts matchups that
require human review into automatic advancements, so it is refused. An event may
widen the band.

## `validation: performance-qualified byes require a consolidated score`

The bracket is being drawn before consolidation finished. Scores are read from
`events/<event>/summaries/<team>.md`, and only when that report is `finalized:
true`. Finish consolidation, resolve any blocking `NE` or disagreement, then
redraw.

## `constraint: ...` or a bracket reporting `feasible: false`

A hard constraint could not be satisfied. Read the `constraint_audit` in the
bracket: each entry says `satisfied`, `maximized`, `violated`, `not-applicable`
or `infeasible`, with the reason. `infeasible` usually means one affiliation
group holds more than half the play-in field, or the two previous finalists are
the only two play-in teams. An event official must accept the listed exceptions
in writing before the draw is used; record that as a manual override.

## `safety: execution refused`

No container runtime was verified. Run `python3 -m atj sandbox preflight` for the
reason. Common causes: Podman not installed, or a Docker client present whose
daemon does not answer. There is no host fallback. Continue with static
inspection, record `execution_status: unavailable`, and score the affected
criteria `NE`.

## `atj validate publication` reports BLOCKED

Read each finding. The common ones:

- `visibility` — the artifact's declared visibility does not match its directory.
- `private-field` — a private-only key is present, possibly nested.
- `approval` — no human official has approved publication.
- `provenance` — `source_artifacts` is empty, so the artifact is untraceable.
- `secret` — something matching a credential shape is present.
- `location-unknown` — the gate cannot tell which rules apply. Pass the correct
  `--event-dir`.

Do not weaken the check to get past it.

## `state: cannot advance from ...`

The stage gate has not passed, a unit is incomplete, or an audit failed. Run
`python3 -m atj event status <dir>` for the specific reason. Record an audit
result with `atj event gate`. A human override needs `--force-reason` and is
written into the ledger.

## `validation: unparseable front matter: front matter uses a YAML anchor`

Anchors and aliases are refused because nested aliases expand multiplicatively
and this content is untrusted. Write the values out.

## `next action: repair-incomplete-unit`

A unit is recorded complete but its output is missing, which is what an
interruption looks like. Re-run that unit only; completed audited units with
unchanged inputs are not redone.

## `next action: rerun-stale-units`

An input changed after the unit completed. A changed evidence package invalidates
its judgments, its consolidation, dependent matchups and the dossier. Preserve
the old artifacts under versioned names rather than overwriting the audit trail.

## The sample event fails after a code change

Expected: the sample is a regression fixture. Run `python3 -m atj demo build`,
inspect `git diff` to confirm the change is the one you intended, and commit the
regenerated artifacts.

## Tests pass but CI fails on "Sample event is current"

You changed behaviour without regenerating the sample. See above.
