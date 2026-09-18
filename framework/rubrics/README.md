# Rubric Set

These files are versioned evaluation contracts. Every report records the exact rubric ID and version it used. Do not edit a rubric after an active event begins. Copy it, increment the version, and explicitly decide whether existing work must be rerun.

`submission-evaluation.md` scores each team. `panel-consolidation.md` combines independent results without creating a new opinion. `head-to-head.md` compares two teams. `bracket-assignment.md` controls assignment rather than team merit.

Official calculations are performed by repository scripts. Persona definitions may change investigative emphasis but never weights or formulas.

## A repair round is audited before the gate

When an audit pass specifies repairs, **the repair round must itself be audited
before the stage gate is set.** An audit cycle that stops at the first PASS stops
one round too early.

This is not a precaution. In `live-trial-2026` the evidence stage took three
audit rounds and the judging stage five, and **nine of the defects found were
introduced by the repairs**: a fabricated `playwright 1.56.0`, a
`starlette 1.6.0` attributed to a measurement never taken, a `Containerfile`
comment citing a path that does not exist at the pinned commit, a manifest Scope
paragraph left contradicting its own front matter by the repair that was meant to
fix it, and the ascending-order rule in an activity log broken twice.

Repair is a source of defects, not only a sink. The reviewer of a repair is never
the party that wrote it, and `atj event gate` reads the audit of the **last**
round, not the first one that passed.

## What validation cannot tell you

A green `atj validate reports` means an artifact is well-formed. It does not mean
it is true.

In `live-trial-2026` it returned zero findings at every stage on manifests
containing nine citations pointing at the wrong observation, a scan credited to
an observation that never examined the code in question, and a fabricated version
number. Validation checks that an evidence id *resolves*; until T3.1 it could not
check that the target *contains the claim made of it*, and both look identical to
a schema.

T3.1 narrows that gap: a requirement and the observation it cites must each claim
the other, so one author's slip stops passing silently. It does not close it. An
observation that is itself wrong, or a fabricated number inside one, remains the
audit's job. The LLM audit is load-bearing, and on that event it was the only
thing that caught any substantive error.
