# Framework fix plan — defects found by live-trial-2026

Source of truth for the remediation work. The review surface is
`artifacts/html/reports/live-trial-2026-status.html`.

Written 2026-09-17, during `live-trial-2026` at stage `initial-judging`.

## The constraint that shapes this plan

An active event's rubric version, weights, personas, bracket policy and evidence
are frozen once judging begins. Judging has begun: `team-ledger` has four
judgments recording `persona: judge-*@1.0.0`.

That splits the work in three. Tier 1 touches nothing the event depends on and
lands now. Tier 2 changes persona versions and must wait for the event to reach
`complete`. Tier 3 changes an artifact schema and belongs to the next framework
version.

## Defects

| ID | Defect | Tier |
|---|---|---|
| D1 | Judge personas declare `tools: Read, Grep, Glob` and cannot write the artifact `judge-submission` requires of them | 2 |
| D2 | `schemas/judgment.schema.json` requires a `model` block that `framework/templates/individual-judgment.md` does not show | 1 |
| D3 | `atj render judgment` did not exist though the template cited it by name | done |
| D4 | `atj validate reports` verifies that a citation resolves, not that its target contains the claim | 3 |
| D5 | `atj/event.py:745` writes `status.md.bak` on every ledger update; it was committed twice | done |
| D6 | `.claude/hooks/pre-advance.sh` inspects the whole command string, so prose naming a submission path trips the run-on-host guard | 1 |
| D7 | `atj score`'s text output prints `blocked_reasons` but never `adjudication_required`, so an operator reading the console can state the opposite of the committed JSON | 1 |
| D8 | `confidence` is undefined for an `NE` criterion; four judges on identical reasoning split between `low` and `high` because one described the evidence and one described the determination | 2 |
| D9 | `model.verified` has no defined threshold; on the same basis `judge-backend` recorded `false` and three judges recorded `true` | 2 |

D3 fixed in `3a798ad` (command added, reproduces the committed sample byte for
byte) and `4ac09ba` (refuses to rewrite an approved judgment without `--force`,
checks every file before writing any, reports `forced_over_approval` in `--json`).
D5 fixed by gitignoring `*.bak` with the `atj/event.py:745` reason recorded.

D7, D8 and D9 were found by the `initial-judging` stage audit of live-trial-2026
(`events/live-trial-2026/audits/judgments.md`). D7 is tier 1 because it caused a real
defect in that event: the operator wrote "no adjudication required" into the ledger
while `summaries/team-podcast.json` recorded the opposite. It is a print statement.
D8 and D9 are tier 2 because they set what a judge must write, and personas and
templates are frozen while an event is judging.


## Tier 1 — land during the event

### T1.1 — template and schema agree (D2)

Add the `model` block to `framework/templates/individual-judgment.md`. This
documents what the schema already enforces; it changes no validation behavior and
no number.

Then add a `release-check` assertion that every template in
`framework/templates/` satisfies the schema for its artifact kind. D2 existed
because nothing compared the two, and the same gap can hide in any of the other
sixteen templates.

**Done when:** a judge following the template produces a file that passes
`atj validate reports` on the first attempt, and `release-check` fails if a
template drops a schema-required field.

### T1.2 — the execution guard stops firing on documentation (D6)

`.claude/hooks/pre-advance.sh` blocked a `git commit` whose message body named a
submission's test file. Narrow it to inspect the command being executed rather
than the entire command string including heredoc content and commit-message
bodies.

The guard must stay blunt about actual execution. The failure mode to avoid is
an operator learning to work around a hook that cries wolf.

**Done when:** a commit whose message discusses a submission's internals is not
blocked, and an attempt to actually run submission code on the host still is.

## Tier 2 — after live-trial-2026 reaches `complete`

### T2.1 — judges can write their own artifact (D1)

Give `judge-backend`, `judge-frontend-ux`, `judge-security-ops` and
`judge-product-agentic` a `Write` tool scoped to
`workspaces/<event>/staging/<team>/`. Bump each to `@1.1.0` in
`framework/personas.md`.

Scoped to staging, not to `events/`, because staging is what makes judge
independence structural: a report written into the event directory while another
judge is still running is a report that judge could read.

Add an end-to-end test that spawns one persona and asserts it produces its own
artifact. The sample event cannot catch this class because `demo_writer.py`
generates those files directly and no persona ever runs.

**Cannot land earlier.** `team-ledger`'s judgments record `@1.0.0`. If
`team-podcast`'s recorded `@1.1.0`, the two panels would come from different
personas and the head-to-head comparing them would be comparing unlike things.

**Done when:** a judge persona writes its own file, and `atj personas` reflects
`@1.1.0` for all four.

### T2.2 — release-check compares declared tools against required outputs

Extend `atj release-check` to cross-check each agent definition's tool list
against the artifacts its skill requires it to produce. A persona that cannot
write a file its skill demands is a contract violation, and nothing currently
compares the two.

**Done when:** removing `Write` from a judge persona fails `release-check`.

## Tier 3 — next framework version

### T3.1 — make a misdirected citation structurally detectable (D4)

Semantic truth is not checkable. This specific failure is, through bidirectional
linking:

```
Requirements table              Direct observations table
  R2 → cites ev-ledger-06         ev-ledger-06 → supports [R2, R3, R4, R9]

atj validate reports asserts the two agree.
```

A requirement citing an observation that does not claim to support it becomes a
blocking finding. This catches the exact nine-row failure from evidence audit
round 1 deterministically, because the observation's author has to independently
assert the same link — one person's slip stops passing silently.

Requires a change to `schemas/evidence-manifest.schema.json`, an update to
`framework/templates/evidence-manifest.md`, and a migration for existing
manifests. Hence next version, not this event.

**Done when:** repointing a requirement row at the wrong observation produces a
blocking finding from `atj validate reports`.

**What it still will not catch:** an observation that is itself wrong, or a
fabricated number inside an observation. Those remain the audit's job, and the
next item says so out loud.

### T3.2 — record that one audit pass is not enough

Add to `framework/rubrics/README.md`: when an audit pass also specifies repairs,
the repair round must itself be audited before the gate.

Evidence from this event: three rounds on the evidence stage, each finding real
defects the previous round missed, and **three of those defects were introduced
by the repairs** — a fabricated `playwright 1.56.0`, a `starlette 1.6.0`
attributed to a measurement never taken, and a `Containerfile` comment citing a
path that does not exist at the pinned commit.

Repair is a source of defects, not only a sink. An audit cycle that stops at the
first PASS stops one round too early.

## The finding that outranks all six defects

`atj validate reports` returned **zero findings at every stage** — before audit
1, between every repair round, and after audit 3 — on manifests containing nine
misdirected citations, a scan credited to an observation that never examined the
code in question, and a fabricated version number.

This is structural, not a bug. Validation checks that an evidence id resolves.
It cannot check that the target contains the claim made of it, and both look
identical to a schema.

Two things follow, and they belong in the final event report:

1. A green `atj validate reports` means the artifact is well-formed, not true.
2. The LLM audit is load-bearing. On this event it was the only thing that caught
   any substantive error.

T3.1 narrows the gap. It does not close it, and the framework's documentation
should stop implying that validation and correctness are the same property.
