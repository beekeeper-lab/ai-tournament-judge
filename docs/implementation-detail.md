---
document: implementation-detail
framework_version: 0.2.0-beta
written: 2026-09-16
---

# Implementation Detail

What was actually built for v0.2.0-beta, why it is shaped that way, where it
deviates from the original plan, what it cannot do, and where to extend it.

This is not a restatement of the specification. Where the specification asked for
something and the answer was "no, and here is why", that is recorded here.

---

## 1. The problem the alpha actually had

`v0.1.0-alpha` was a well-written specification with a thin implementation under
it. Executed rather than read, it provided correct weighted arithmetic, a
correctly shaped bracket, and file-existence checks. Its documents described
enforced safety, enforced privacy, enforced independence and deterministic
tournament mechanics; three of those were absent and two were actively broken.

The gap between claim and behaviour was the real defect. An operator reading
`execution-safety.md` would reasonably conclude that sandboxing existed. It did
not. `docs/release-readiness-audit.md` records the full baseline with
reproductions.

Everything below follows from one decision: **make the documents true, or change
the documents.**

---

## 2. Architecture

```
framework/rubrics/*.md      canonical facts, versioned, human-editable
framework/policies/*.md     prose policy
framework/templates/*.md    artifact shape, including required sections
framework/personas.md       agent and skill versions with content digests
schemas/*.json              structured metadata contracts
atj/                        deterministic tooling
.claude/                    project-local agents, skills, commands, hooks
events/<id>/                one event's records; status.md is the ledger
```

`atj` modules, in dependency order:

| Module | Responsibility |
|---|---|
| `errors` | Stable error codes so hooks, CI and audits can match on a code, not prose |
| `frontmatter` | Bounded YAML front-matter parsing for untrusted content |
| `canon` | Reads the rubrics and policies. The only place official numbers enter the system |
| `ids` | Derived, verifiable identifiers |
| `schema` | Offline JSON Schema registry |
| `versions` | Framework commit, component registry, version compatibility |
| `scoring` | Individual scores, panel consolidation, panel integrity |
| `matchup` | Order-balanced head-to-head resolution |
| `bracket` | Constrained-random assignment with a constraint audit |
| `event` | Lifecycle, state machine, staleness, resume |
| `publication` | The private / team / public boundary |
| `reports` | Artifact validation, composed from the above |
| `render` | Structured results into Markdown blocks |
| `ceremony` | Static HTML from approved public artifacts only |
| `sandbox` | Isolated execution, or an honest refusal |
| `demo`, `demo_writer` | The synthetic sample event |
| `cli` | One operator-facing entry point |

---

## 3. Design decisions

### D1 — The rubric Markdown is the only editable source of official numbers

`atj.canon` parses `framework/rubrics/submission-evaluation.md`: front matter for
the version and scale, the Markdown table for criterion IDs, names and weights.
If the table's total disagrees with the front matter's declared `total_weight`,
that is fatal, because it means one of the two was edited alone.

The same treatment extends to the other contracts. Agreement thresholds and the
minimum panel size live in `panel-consolidation.md` front matter. Comparison
value bounds, the close-call band and the tie-break order live in
`head-to-head.md`. The bye policy list, the default and the team range live in
`bracket-assignment.md`.

`atj release-check` scans the whole tree — Python, JSON, YAML and Markdown — for
a second editable copy of any official weight, and fails the build if it finds
one. That check exists because the alpha's duplicate was a Python dict, and the
next one would just as easily be a Markdown table.

**Deviation from the plan:** the plan said "deterministic scripts must read the
canonical rubric definition". We went further and deleted the scripts. Five
scripts with five I/O conventions, each holding its own copy of some official
fact, could not be made consistent by adding a read; they are now shims over a
single CLI and will be removed in 0.3.

### D2 — Identifiers are derived, never assigned

An evidence package ID is `ev:<event>:<team>:<commit12>:<digest8>`, where the
digest covers the manifest's content. Re-preparing identical evidence yields the
same ID; changing any recorded evidence yields a different one. That property is
what makes staleness detectable: a unit's recorded input digest either still
matches reality or it does not.

The same applies to the bracket's `input_digest`, which covers the roster, every
score, every affiliation, the seed and the policy. Change any of them and the
existing draw is visibly stale rather than quietly wrong.

### D3 — Version incompatibility is fatal, never a warning

`atj.versions.require_versions` checks every contract an artifact pins: the
submission rubric, the consolidation policy, the head-to-head rubric, the bracket
policy, and the persona. Any mismatch raises. There is no "warn and continue"
path, because the situation it describes — an artifact produced under different
rules than the one being applied — has no safe continuation.

`framework/personas.md` pins each agent and skill to a version *and* a content
digest of its definition file. Editing a persona without incrementing its version
fails validation. This is what stops a judge's instructions changing silently
underneath an active event.

### D4 — The close-call band is a floor, not a ceiling

This one was wrong in the first implementation and an independent audit caught
it. A *narrower* band means fewer matchups are treated as close, so more are
decided automatically. A *wider* band sends more to a human. The safe direction
is wider.

An event may widen the band through validated event configuration. It may not
narrow it, and it cannot set it at all from a matchup input file, because that
file is derived from model output.

### D5 — Bracket placement is a seeded search, not a greedy walk

The alpha hard-coded `position // 8` as "half", which is only true for a 32-slot
bracket. Here, the earliest round two slots can meet is computed from the bracket
size, and placement minimises a cost where same-affiliation pairs are penalised
by how early they can meet and a previous-finalist pair carries a penalty large
enough that no affiliation arrangement can buy it off.

The search is a fixed number of seeded restarts with a fixed improvement order
and incremental swap evaluation, so the result is a pure function of the seed.
Incremental evaluation is what makes it affordable to test: the suite builds
thousands of brackets across every size, every policy and many seeds.

Play-in pairing takes one team from the largest affiliation group and pairs it
with a non-conflicting team from the next largest, then runs a repair pass. The
repair pass exists because greedy pairing can strand the two previous finalists
as the last available pair even when a conflict-free pairing exists.

**Every constraint reports a status** — `satisfied`, `maximized`, `violated`,
`not-applicable` or `infeasible` — with detail and exceptions. `feasible: false`
is a legitimate outcome that an official must accept in writing; it is not a
failure to hide.

### D6 — Verification re-derives; it does not read the audit

`bracket.verify(result, teams)` recomputes the constraints from the placement and
the roster. Given only the bracket file it checks structure; given the roster it
re-derives the bye selection, the finalist separation and the first-round
conflicts. Trusting the constraint audit shipped inside the file being verified
would mean a hand-edited bracket verifies clean, which an audit caught us doing.

### D7 — The publication boundary is enforced in four independent places

A public artifact must: sit in `public/`, declare `visibility: public`, carry no
private-only field anywhere in its metadata including nested, name a human
approver, list its source artifacts, and survive a scan for credentials, private
identifiers, deliberation markers and unapproved scores.

The gate **fails closed**. An artifact whose location it cannot determine is
blocked, not passed, because the alternative was demonstrated: it reported
`CLEAR` on a file full of credentials.

`atj.ceremony` reads only `public/` and the bracket's structural facts. The
private record is not an input, so a template bug cannot leak it. The renderer
refuses rather than skipping a non-conforming artifact: a ceremony display that
silently omits a match is worse than one that does not build.

### D8 — Execution is genuinely isolated, or genuinely unavailable

`atj.sandbox` builds a container invocation with no network, a read-only
submission mount, all capabilities dropped, `no-new-privileges`, non-root user,
and CPU, memory, PID, disk and time limits. It refuses to mount any directory
holding host credentials, and refuses a network allowlist without an egress
proxy — because container flags cannot filter by destination, so honouring an
allowlist with `--network` alone would in fact grant unrestricted access.

**There is no host fallback.** If preflight cannot verify isolation, execution
raises. The evidence manifest records `execution_status: unavailable`, names the
evidence-limited criteria, and those criteria are scored `NE`. A judge with less
evidence is a correct outcome; running a student's code on the operator's laptop
is not.

On the host that produced this release, Podman is absent and the Docker daemon
does not respond, so the sample event records execution as unavailable throughout.

### D9 — Prompt-injection resistance is scoped honestly

Two layers, and only one is a guarantee.

**Mechanical, and tested:** no text in a submission can change the rubric, the
weights, a rubric version, an artifact's visibility, the publication gate, or a
judge's tool surface, because none of those is ever read from a submission. The
four initial judges hold `Read, Grep, Glob` and nothing else, so a successfully
manipulated judge still cannot run code, fetch a URL or write a file.

**Model-level, and not a guarantee:** the judge personas instruct the model to
treat submission content as untrusted. That is a mitigation. This repository does
not claim an LLM cannot be manipulated, and `tests/fixtures/prompt-injection/`
says so explicitly.

One live panel run is recorded in `docs/agent-verification.md`: all four judges
refused all 13 attempts in the fixture and disclosed them despite being told not
to. One run is evidence, not proof, and that document says so.

The claim that *is* made is narrower and testable: a successful manipulation of a
judge's prose cannot alter a score's arithmetic, a rubric version, an artifact's
visibility, or the set of approved public output.

### D10 — The sample event's judge scores are scripted

The sample event must be reproducible in CI, which rules out invoking a model.
Its scores are therefore fixed inputs chosen to produce exactly the conditions the
release must demonstrate. Every artifact records `model_used: not-applicable
(scripted fixture)`.

This is a deliberate trade and it is stated everywhere it could mislead. The
fixture demonstrates the *pipeline*, not model behaviour.

### D11 — Hooks are guard rails and say so

`.claude/hooks/lib.sh` opens by stating that hooks are not a security boundary:
they run with the operator's own permissions, and anything they check can be done
another way. They fail open on their own errors, because a hook that blocked on
its own bug would be worse than no hook, and its blocking would be mistaken for a
guarantee it cannot provide.

They were verified firing in Claude Code 2.1.273: a `PreToolUse` hook blocked a
hand-edit of `events/*/public/` end to end. Separately, Claude Code **ignores
`permissions.allow` from project settings until the workspace is trusted**, so
nothing in this framework depends on it.

### D12 — Official numbers are verified, not trusted

An agent writes a consolidated report. The numbers in it come from `atj score`,
but *writing* them is a transcription step, and until the final audit nothing
compared them back. `atj score` being deterministic is true and was irrelevant to
what actually shipped.

`reports.check_consolidation` reloads each team's judgments, reapplies their
approved adjudications, re-runs consolidation, and fails on any mismatch of
`total`, `display_total`, `finalized` or the judge run IDs. The generated number
and the written number must agree or nothing passes.

### D13 — A gate needs the audit behind it

`atj event gate <g> passed` used to set a boolean. An event could reach
`complete` in eighteen commands with no evidence, no judgments, no matchups and
no dossiers, and `validate reports` would say "PASS — 0 artifacts".

Passing a gate now requires `--audit <artifact>`, and that artifact must exist,
schema-validate, be approved, be private, carry a scope, have content, and record
a result in `PASS_RESULTS`. Separately, each stage declares the work it requires,
and `can_advance` refuses while that work is absent. The framework still cannot
check that the audit was performed *carefully* — that is the human's part, and it
is stated as such.

### D14 — Winners are advanced, and only ever by something that named one

A bracket with no advancement is a draw sheet, not a tournament record.
`atj bracket advance` writes a winner and carries it into the next round. It
reads the winner from the private matchup report, and when that report says
`adjudication-required` — which means the framework deliberately returned no
winner — it refuses unless an approved adjudication for that match names the
advancing team.

Match identifiers now come out of the drawn bracket rather than being assigned
independently. They were assigned in two places and disagreed: the bracket
recorded one pairing under an identifier and the matchup report recorded another.

---

## 4. Deviations from the original plan

| Plan said | What was done | Why |
|---|---|---|
| Complete the existing scripts | Retired them to shims over one CLI | Each held its own copy of an official fact and they could not see each other's output |
| Stage numbering 1-8 from the alpha | Renumbered to the release stages 0-9 | The alpha numbering did not map onto the work; Appendix A in the plan records the mapping |
| "Select the default bye policy" | Kept `performance-qualified`, made the list canonical | The default was right; its being a hard-coded duplicate was not |
| Implement the execution-safety policy | Implemented it *and* made unavailability a first-class outcome | The host cannot provide isolation, and pretending otherwise was the alpha's worst failure mode |
| Simulate a full event with real judges | Scripted the sample; verified the agent layer structurally | A CI-reproducible fixture and a non-deterministic model are incompatible; see D10 |
| Templates carry weights | Removed weight columns from templates | A hand-copied weight is how official numbers drift |

The seven rubric criteria and their weights are unchanged. No defect was found in
them.

---

## 5. Known limitations

1. **LLM judgment is not deterministic** and is not claimed to be.
2. **The sample event's scores are not model output.** See D10.
3. **Execution needs a container runtime.** Neither Podman nor a reachable Docker
   daemon exists on the release host, so the end-to-end path through
   `atj sandbox run` is implemented and unit-tested but has not been exercised
   against a live runtime. `atj sandbox preflight` reports this honestly.
4. **A network allowlist needs an egress proxy** that this repository does not
   provide. Until one is configured, the answer is no network.
5. **Prompt-injection resistance is partial.** See D9.
6. **Hooks are bypassable.** See D11.
7. **Affiliation separation is best-effort by design.** Where a group holds more
   than half the play-in field, no collision-free pairing exists; the bracket
   reports `infeasible` with the exceptions rather than hiding them.
8. **Model cost scales with the field.** Roughly `4 x teams + 2 x matches` model
   invocations. Measure before scaling.
9. **`canon` caches on file mtime and size.** A rewrite that forges both serves a
   stale rubric within a running process. Contrived, but real.
10. **Calibration is a documented procedure, not an automated one.** The template
    exists; running it is an operator activity.
11. **Judge independence is procedural and detected, not prevented.** The judges'
    tools are read-only but not path-restricted. The `judge-submission` skill
    stages reports outside `events/` until the panel completes, and
    `reports.check_judge_independence` flags near-duplicate wording between two
    judgments on the same team. A judge that was contaminated but paraphrased
    well would not be caught.
12. **Several controls end in a human, and cannot be verified further.** The
    framework refuses to pass a gate without an audit artifact, to advance a
    winner without a confirmed result or a recorded adjudication, and to publish
    without a named approver. It cannot check that the audit was thorough, that
    the approver read what they approved, or that an `--force-reason` override
    was justified. `status.overrides` records every override; no command
    currently surfaces them in a summary view.
13. **The independence detector is a similarity heuristic.** It compares
    six-word shingles and flags 80% overlap or more. It will not catch
    contamination that was reworded, and a tightly templated evidence package
    could in principle produce a false positive.

---

## 6. Commands

See `README.md` for the full table. The ones that matter most:

```bash
python3 -m atj release-check                      # every framework-level check
python3 -m atj event status events/<id>           # the next safe action
python3 -m atj score events/<id>/judgments/<team> # official consolidation
python3 -m atj bracket verify <bracket.json> --event-dir events/<id>
python3 -m atj validate publication <artifact> --event-dir events/<id>
python3 -m atj sandbox preflight                  # is isolation real right now?
python3 -m atj demo check                         # is the sample still honest?
python3 -m atj event overrides events/<id>        # what did a human step over?
python3 -m atj render consolidated events/<id>/summaries
```

## 7. Tests

487 tests plus 234 subtests, at 0.3.0-beta.

| File | Covers |
|---|---|
| `test_canonical_model.py` | Rubric parsing, identifiers, schemas, persona drift |
| `test_scoring.py` | Individual and panel scoring, `NE`, agreement, panel integrity |
| `test_matchup.py` | Normalization, margins, outcomes, tie-break, determinism |
| `test_bracket.py` | Shape, hard constraints, infeasibility, policies, reproducibility |
| `test_publication.py` | The private / team / public boundary and secret scanning |
| `test_event.py` | Initialization, validation, transitions, staleness, resume |
| `test_prompt_injection.py` | The mechanical injection-resistance layer |
| `test_ceremony.py` | Public-only rendering and refusal behaviour |
| `test_end_to_end.py` | The committed sample event and interrupt-and-resume |
| `test_audit_regressions.py` | One test per finding from the independent audits |
| `test_intake.py` | Pinning, archive refusal, snapshot reproducibility |
| `test_hooks.py` + `tests/hooks/` | The project-local guard rails, both directions |
| `test_live_trial_regressions.py` | The defects the first live event exposed |
| `test_final_audit_regressions.py` | One test per finding from the release audit |
| `test_release_audit_regressions.py` | The baseline audit's release blockers |
| `test_tier1_regressions.py` | Tier-1 defects: gate scope, approval, schemas, renderers |
| `test_tier2_regressions.py` | Supersession, write contracts, the rubric's own rules, adjudication authority |
| `test_tier3_regressions.py` | Citation symmetry, unit digests, hook sequencing |
| `test_operator_surface.py` | The release advisories that were closed, and the packaging wiring |

Each regression file names the defect it locks down in the test's own docstring,
and says what the pre-fix behaviour did. A test whose name records a defect
number is worth more than a test whose name records a function.

The bracket tests sweep every supported size, every bye policy and many seeds.
That breadth is deliberate: the alpha's two constraint defects both survived a
suite that tested one size with one seed.

## 8. Extension points

- **A new criterion:** add a row to the rubric table, bump its version, decide
  whether in-flight work re-runs. Nothing else needs editing; every consumer
  reads the table.
- **A new bye policy:** add it to `bye_policies` in `bracket-assignment.md`, then
  implement its branch in `bracket.choose_byes`.
- **A different tournament format:** `bracket.py` assumes single elimination.
  Round-robin or double elimination would need a new module and a new schema; the
  constraint-audit shape is reusable.
- **A fifth judge or a new persona:** add the agent, register it in
  `framework/personas.md`, add it to the event's `expected_judges`. Panel
  integrity checks read that list.
- **A different artifact kind:** add a schema, add a template, register the pair
  in `reports.ARTIFACT_KINDS`. Required sections come from the template, so there
  is no second list to maintain.
- **A real network allowlist:** implement an egress proxy and pass its URL as
  `egress_proxy`; `sandbox.build_command` already routes through it and refuses
  without it.
- **A different ceremony design:** `ceremony.render_ceremony` returns a string.
  The constraint that matters is its input set, not its styling.
