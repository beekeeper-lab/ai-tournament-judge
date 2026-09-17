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
| D10 | `framework/templates/adjudication-report.md` invites `persona: ADJUDICATOR-AGENT-OR-HUMAN@VERSION`, but `atj validate` requires a persona registered in `framework/personas.md` as `name@x.y.z`. There is no adjudicator persona and no way to name a human decision-maker | 1 |
| D11 | An adjudication can *clear* an `NE` through `score_override`, but nothing can express one that *accepts* it. `atj score` re-reports an adjudicated `NE` as `unresolved` and keeps listing `adjudication_required`, so a completed adjudication is indistinguishable from a missing one | 2 |
| D13 | `atj/scoring.py:431` treats a non-empty `decided_by` as one of the gates that lets an adjudication move an official total, and nothing distinguishes a human deciding from an agent writing a role into a required field | 2 |
| D14 | Neither `schemas/adjudication.schema.json` nor `framework/templates/adjudication-report.md` has an amendment field, so an approved adjudication corrected after the fact cannot disclose the correction structurally and ends up citing an audit that post-dates its own `completed_at` | 2 |
| D15 | `atj event unit record` restamps `completed_at` with the current clock and offers no override, so re-recording a unit to change only `audit_result` destroys the real completion time | 1 |
| D16 | The stage completion gate has no scope filter: a finding against a framework document, an ignored path, or activity-log prose blocks a stage gate exactly as hard as a wrong score | 1 |
| D17 | An agent worktree inside the repository makes `release-check` FAIL and breaks four validators, because they walk the filesystem rather than git. Gitignoring the directory does not help | 1 |
| D18 | `framework/templates/consolidated-team-report.md` cites `atj consolidate` and the `atj:consolidated` marker region implies `atj render consolidated`. Neither command exists — `atj render` has only the `judgment` subcommand — so the one region a template says a tool must own can only be filled by hand | 1 |

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
defects the previous round missed, and **four of those defects were introduced
by the repairs** — a fabricated `playwright 1.56.0`, a `starlette 1.6.0`
attributed to a measurement never taken, a `Containerfile` comment citing a
path that does not exist at the pinned commit, and the manifest Scope paragraph
left contradicting its own front matter by the 18:41:56Z repair itself.

The judging stage then repeated the pattern: five more repair rounds produced
five more defects, including the ascending-order rule breaking for a second time.

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

D10 and D11 were found while writing the only adjudication live-trial-2026 has
produced (`events/live-trial-2026/adjudications/team-podcast-reliability-ne.md`).
D10 is tier 1: a template and a validator disagree, and the template loses.
D11 is tier 2 because the repair changes what `atj score` prints for an official
result, which should not move while an event is being scored.

D13 was found by the second-pass judging audit of live-trial-2026 while ruling on
D10. It carried no weight in that event because the one adjudication written has no
`score_override`, so nothing official moved. The audit's ruling is worth keeping:
the substitution of `run-judging-event@1.0.0` for a human adjudicator is honest in
form because the record discloses it in plain text, unverifiable in substance, and
acceptable once but not as a precedent.

Numbering note: the second-pass audit recommends this defect as "D12". It is D13
here because D12 was already taken by the `agentic`-with-no-AI rubric gap on branch
`fix/framework-d7-d10-d12`.

## D16 — the gate needs a scope filter

This is the most reusable result of live-trial-2026 and the one to land before the
next tournament. The `judgments-audited` gate took three audit passes and five
repair rounds. Those repair rounds produced five new defects. The mechanism is not
auditor pedantry; it is that `can_advance` branches on an audit's verdict alone,
and an auditor has no way to mark a finding as outside the thing being gated.

At the second pass, two findings held the gate: one that `docs/framework-fix-plan.md`
said "three" where it meant "four", and one about a numbering collision between two
branches. Neither is inside `events/`, inside the audited stage, or attached to any
score. Repairing them introduced three new findings, two of which then held the gate
again.

The third-pass auditor was asked to rule on this directly and named the split.

**Must block** — findings inside `events/<event>/`, inside the audited stage, that hit:
missing evidence, arithmetic that does not reproduce, a version mismatch, severe
disagreement, unsafe execution, private data in public output, an unauthorised score
move, or an edited judgment.

**Must not block** — findings against framework documents; uncommitted or ignored
paths; activity-log prose precision where the underlying history is correct; and
fields no code reads.

Proposed shape: give each finding a `scope` of `event` or `framework` and a
`blocking` boolean the auditor must set, and make `can_advance` consider only
`scope: event` findings marked blocking. Then a verdict can be FAIL for the record
while the gate still opens, which is the state this event was actually in for two
of its three passes.

D14, D15 and D17 were all found the same way — by running the event, not by reading
the code. D17 is the sharpest operational one: the fix work for this plan was done in
an agent worktree, and the worktree silently broke `release-check` for as long as it
existed.

D18 is D3 repeating one artifact type later. D3 was `atj render judgment` cited by
the judgment template and never built; it was found the same way, by a panel needing
it. Both consolidated reports for live-trial-2026 were therefore transcribed by the
consolidator, and both consolidators said so unprompted and asked for regeneration.
Neither could be regenerated, so each table was instead verified cell by cell against
`summaries/<team>.json` by a deterministic script: seven criteria, every judge score,
both totals and the finalization flag, zero mismatches on both teams. That check is
what `atj render consolidated` should do, and it should be built from it.
