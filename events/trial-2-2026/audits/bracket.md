---
event_id: trial-2-2026
audit_scope: bracket stage, first pass — the draw, the override record, the bracket report, the disclosure decision and the four ledger rows committed at abc7e7a
audit_id: bracket
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.1.0
persona: judging-auditor@1.1.0
framework_commit: abc7e7a39361a1bdd879ee42659b806c272d9006
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-23T10:55:00Z"
completed_at: "2026-09-23T11:12:00Z"
visibility: private
approval_state: draft
validation_state: unvalidated
result: FAIL
findings:
- id: F1
  severity: major
  scope: framework
  blocking: false
  summary: bracket.md is validated by nothing — ARTIFACT_KINDS maps only event subdirectories, the report sits at the event root, there is no bracket-report schema, and the bracket:draw ledger digest does not cover it
  artifact: atj/reports.py:26-45,782-793
  repair: register a `bracket-report` kind with a schema and route root-level artifacts through `validate_event_reports`, or move the report under a validated subdirectory. Until then record in the directory map that `bracket.md` is a required file no validator reads. Framework work, out of scope for this stage to fix mid-event
  state: open
- id: F2
  severity: major
  scope: event
  blocking: false
  summary: 'bracket.md:120 cites `atj/versions.py:144-164` for reading framework_commit from git; that range is require_personas, components_available and the head of check_personas, and contains no git call'
  artifact: events/trial-2-2026/bracket.md:120
  repair: 'cite `atj/versions.py:216-238`, which is the `framework_commit` function; the git call is at `:225`. The claim itself is true and was verified by rebuild'
  state: open
- id: F3
  severity: major
  scope: event
  blocking: false
  summary: the publication and disclosure approval — a decision event.md reserves to the event-director — was written into the event configuration as prose instead of recorded as a manual override record, so no validated artifact carries an authorized_by for it
  artifact: events/trial-2-2026/event.md:186-221
  repair: 'record the decision as `overrides/ovr-trial-2-2026-publication-disclosure.md`, category `publication`, `authorized_by: event-director`, and have the event.md subsection cite it rather than carry it. The same commit did exactly this for the bracket exception'
  state: open
- id: F4
  severity: minor
  scope: event
  blocking: false
  summary: 'the override cites event.md:96-107 — "event-director holds all four authorities" — as authority for a `rules exception`, which is not one of the four officials keys event.md declares'
  artifact: events/trial-2-2026/overrides/ovr-trial-2-2026-bracket-affiliation.md:44-48
  repair: 'add the line that actually grants it, `framework/policies/disagreement-and-adjudication.md:9` ("A human event official owns disqualification, rules exceptions, and unresolved final ties"), and `framework/templates/adjudication-report.md:112`, alongside the event.md role citation'
  state: open
- id: F5
  severity: minor
  scope: framework
  blocking: false
  summary: 'schemas/event.schema.json officials declares four keys while the framework reserves five decisions to humans; rules exceptions and unresolved final ties have no event-level owner, which is what made F4 possible'
  artifact: schemas/event.schema.json:30-38
  repair: add `rules_exception` and `tie_resolution` to the `officials` properties, or state in the schema description that those two are covered by `adjudication`
  state: open
- id: F6
  severity: minor
  scope: event
  blocking: false
  summary: 'event.md:177 says "`public/` was empty until the decision below"; `public/` holds only .gitkeep and this decision produced no public artifact'
  artifact: events/trial-2-2026/event.md:176-177
  repair: '"`public/` stays empty until an artifact passes `atj validate publication` under the decision below"'
  state: open
- id: F7
  severity: minor
  scope: event
  blocking: false
  summary: 'event.md:204-205 "A reader learns where to look, not what the code says" is contradicted by the artifacts it approves — summaries/team-scribe.md:243 quotes the KDF input literal verbatim'
  artifact: events/trial-2-2026/event.md:204-205
  repair: drop the sentence or restate it as "a reader learns where to look, and in a few places what one line says", which is what the reports do
  state: open
- id: F8
  severity: minor
  scope: event
  blocking: false
  summary: 'bracket.md:52 and the 10:51:23Z ledger row say `atj/bracket.py:161` returns; :161 is the `if count == 0:` guard, the return is :162, and the first `.score` access is :169'
  artifact: events/trial-2-2026/bracket.md:52
  repair: 'cite `atj/bracket.py:161-162`, and name `:169` as the first `.score` access the guard precedes'
  state: open
- id: F9
  severity: minor
  scope: framework
  blocking: false
  summary: nothing enforces build-bracket step 6 — `feasible` is read nowhere in atj/event.py and no code reads events/<event>/overrides/, so an event can advance past the bracket stage on a feasible false draw with no override record and every deterministic check passes
  artifact: atj/event.py
  repair: 'have `atj event validate` require, at stage index >= bracket, that a `feasible: false` bracket be matched by an override record naming the unsatisfied constraint. Framework work, out of scope for this stage to fix mid-event'
  state: open
- id: F10
  severity: minor
  scope: framework
  blocking: false
  summary: 'framework/templates/bracket-report.md declares table shapes atj/render.py bracket_tables does not produce — "Team or bye / Region / Entry round" against "Entrant A / Entrant B / Entry", and a three-column constraint table against a four-column one'
  artifact: framework/templates/bracket-report.md:32-38
  repair: align the template's two table headers with `atj/render.py:212` and `:220`, which are what the renderer emits and what any correct report will contain
  state: open
- id: F11
  severity: minor
  scope: event
  blocking: false
  summary: 'event.md:91-94 pre-registered that the shared affiliation would be carried "as a cost rather than a constraint ... rather than fail"; the draw returned feasible false, and no stage artifact records that the event''s own stated expectation was wrong'
  artifact: events/trial-2-2026/bracket.md
  repair: add a sentence to bracket.md's infeasible-constraint section recording that event.md:91-94 expected a cost and got a hard infeasibility, and why. Do not edit event.md
  state: open
- id: F12
  severity: minor
  scope: event
  blocking: false
  summary: 'no ledger unit was recorded for the draw — status.md front matter is `units: []` and `atj event status` reports "units: none recorded" — so the bracket:draw digest D21 added cannot detect a later edit to bracket.json'
  artifact: events/trial-2-2026/status.md
  repair: 'python3 -m atj event unit events/trial-2-2026 record --id bracket:draw --stage bracket --output bracket.json --audit-result not-audited --completed-at 2026-09-23T01:55:10Z'
  state: open
- id: F13
  severity: advisory
  scope: event
  blocking: false
  summary: 'event.md:201 presents the `subprocess.run(..., shell=True)` call site among "the weaknesses it names"; the panel files it under D3 minority findings and says the judge recorded it as a pattern to fix rather than a demonstrable defect'
  artifact: events/trial-2-2026/event.md:199-202
  repair: 'pick an example the panel carries as a confirmed weakness, or qualify this one as the minority observation summaries/team-scribe.md:415-419 records'
  state: open
- id: F14
  severity: advisory
  scope: event
  blocking: false
  summary: all three disclosure examples come from ScribeVault, while the decision covers both reports and summaries/team-demos.md carries 13 file-and-line citations of its own into an LLM-attack demonstration repository
  artifact: events/trial-2-2026/event.md:199-207
  repair: name one team-demos citation and say why a repository whose stated purpose is demonstrating attacks needs no different treatment
  state: open
- id: F15
  severity: advisory
  scope: event
  blocking: false
  summary: 'the override carries `scope: stage` with a populated `match_id`; the schema permits both and no code reads either, but a populated match_id reads as `scope: match`'
  artifact: events/trial-2-2026/overrides/ovr-trial-2-2026-bracket-affiliation.md:5-6
  repair: 'keep `scope: stage` and null the `match_id`, or keep both and say in the body that the stage scope is deliberate and the match_id is the only match the stage produced'
  state: open
- id: F16
  severity: advisory
  scope: framework
  blocking: false
  summary: 'atj bracket verify --reproduce raises an unhandled TypeError on a roster JSON that is a bare list, while atj/bracket.py:918-921 states a validator that raises on malformed input has failed at its job; build-bracket step 5 does not state the required shape'
  artifact: atj/cli.py:1015
  repair: 'validate the `--reproduce` payload and report "expected an object with a `teams` array"; state the shape in .claude/skills/build-bracket/SKILL.md step 5'
  state: open
---

# Judging Audit — bracket stage, first pass

## Result

**FAIL.** Three major findings, nine minor, four advisory. **No blocking
finding.**

The draw itself is sound and nothing in this stage touched a score, a judgment,
an evidence manifest or the roster. `atj bracket build` reproduces `rounds`,
`constraint_audit`, `input_digest` and `bye_teams` byte for byte from the
recorded seed; `atj bracket verify` passes both `--event-dir` and `--reproduce`;
the two tables in `bracket.md` are byte-identical to `atj/render.py`'s
`bracket_tables` output; the six-permutation experiment the report describes
reproduces exactly as described; and the `feasible: false` result has the
written acceptance `build-bracket` step 6 requires.

The stage fails on three things, none of which is about the draw. One citation
in the bracket report points at unrelated code (`F2`). A human decision reserved
to an official — publication approval — was recorded as an edit to the event
configuration rather than as the artifact type the framework provides for it
(`F3`). And `bracket.md`, a file `atj/event.py:61` requires every event to have,
is read by no validator, checked against no schema, and excluded from the ledger
digest that detects drift (`F1`).

`F1`, `F9`, `F10` and `F16` are framework-scope and are recorded, not repaired.
Fixing them means changing framework shape during an active event, which the
evidence-stage audit refused for the same reason at its own `F14`.

**What this verdict does to the gate.** Nothing sets `blocking: true`. Per
`framework/templates/audit-report.md:52-64`, `atj event gate bracket-audited`
reads the findings list rather than the verdict, so it will open the gate and
write the FAIL into the ledger. That is the correct mechanical outcome and it is
not permission to advance: `F2`, `F3` and `F11` are event-scope repairs to
artifacts this stage wrote, and this event's four prior audits each found that
the previous round's repair introduced new defects. Repair, then re-audit this
scope before the tournament stage.

## Scope and artifacts inspected

| Artifact | What was checked |
|---|---|
| `bracket.json` | rebuilt from the recorded seed and diffed field for field; `verify --event-dir` and `verify --reproduce`; constraint audit re-derived; every value the report quotes traced back to it |
| `bracket.md` | every factual claim resolved against `bracket.json`, the cited code, the roster, the adjudications and the summaries; both tables byte-compared against `bracket_tables`; front matter against `framework/templates/bracket-report.md` |
| `overrides/ovr-trial-2-2026-bracket-affiliation.md` | against `schemas/manual-override.schema.json`, `framework/templates/manual-override-record.md` and `.claude/skills/build-bracket/SKILL.md` step 6; authority chain followed to its source; downstream-staleness claim checked against the working tree |
| `event.md` "The disclosure decision, 2026-09-23" | repository visibility checked independently with `gh`; each named weakness traced to the judgment and summary that carries it; `public_scores` diffed; checked against `CLAUDE.md`, the Publication section above it, `audits/consolidation.md` F34 and `docs/0.5.0-beta-plan.md` H4 and R5 |
| `status.md` | four new rows for order, clock, and support for every claim; front matter `last_updated`, gate state, `units` |
| `teams.md` | affiliation groups, roster version, freeze date against git history |
| `atj/bracket.py`, `atj/versions.py`, `atj/render.py`, `atj/reports.py`, `atj/event.py`, `atj/cli.py` | every line reference the stage's artifacts make, resolved by line number, not by function name |
| `framework/rubrics/bracket-assignment.md`, `framework/personas.md`, `schemas/`, `framework/templates/` | the policies and shapes the artifacts are measured against |

Out of scope: the matchup, which has not been drawn against; the consolidation
findings, audited over four rounds at `audits/consolidation.md`; the eight
judgments and two summaries, untouched by this commit and re-confirmed untouched
below.

## Deterministic validation results

| Command | Result |
|---|---|
| `python3 -m atj event validate events/trial-2-2026` | PASS, 0 problems, stage bracket |
| `python3 -m atj validate reports events/trial-2-2026` | PASS, 22 artifacts, 0 blocking, 0 major, 0 minor, 0 advisory |
| `python3 -m atj validate publication events/trial-2-2026` | CLEAR, 22 artifacts, 0 blocking |
| `python3 -m atj release-check` | PASS, every section |
| `python3 -m pytest tests/ -q` | 517 passed, 5 skipped, 285 subtests passed |
| `python3 -m atj bracket verify bracket.json --event-dir events/trial-2-2026` | `PASS (constraints re-derived from the roster)` |
| `python3 -m atj bracket verify bracket.json --reproduce <roster>` | `PASS (reproduced from seed)` |
| `python3 -m atj bracket build --event-dir events/trial-2-2026 --seed trial-2-2026` | rc 1 with the infeasibility warning; output diffs against the committed file in exactly one field, `framework_commit` |
| `python3 -m atj event status events/trial-2-2026` | stage bracket, gate `bracket-audited` pending, **units: none recorded** |

The 22 artifacts `validate reports` sees do not include `bracket.md`. See `F1`.

## The draw reproduces

`atj bracket build --event-dir events/trial-2-2026 --seed trial-2-2026` against
the frozen roster produced a file identical to the committed `bracket.json`
except for `framework_commit`, which moved from `c728437466d0940734bee600765af298eebb062d`
to the current HEAD. That is the behaviour `bracket.md:118-122` predicts, and
`c728437` was HEAD when the draw was built at `2026-09-23T01:55:10Z`.

`bracket_size(2) = 2`, so `bye_count = 0`, so `choose_byes` returns at
`atj/bracket.py:162` before the `.score` reads at `:169` and `:177`. The bye
policy name is still validated at `:154-158` and at `atj/bracket.py:657-662`; it
is the bye *selection* that never runs, which is what `bracket.md:72` means.

## The permutation experiment, re-run

`bracket.md:53-60` claims six score permutations at seed `trial-2-2026` leave
`rounds`, `constraint_audit` and `bye_teams` identical while `input_digest`
moves. Re-run independently through `atj.bracket.build`:

| Scores (scribe, demos) | `rounds` + `constraint_audit` + `bye_teams` | `input_digest` |
|---|---|---|
| None, None | reference | `0fa1d02b4c6f44c3` |
| 32.5, 52.5 | identical | `67fda1f9821f0099` |
| 52.5, 32.5 | identical | `231cbc513b9a232f` |
| 0.0, 0.0 | identical | `a234dd81678253cd` |
| 100.0, 1.0 | identical | `c78c569532e1d7eb` |
| 1.0, 100.0 | identical | `f8bd5b8c70f354e6` |

The claim holds exactly as stated. The `None, None` row reproduces the committed
digest, which independently confirms the draw was built against a roster with no
scores. `atj/bracket.py:911` is the line that folds `team.score` into the digest
and the report cites it correctly.

## Every line reference in bracket.md, resolved

| Report claim | Cited | Actually at | Verdict |
|---|---|---|---|
| returns before any `.score` access at zero byes | `atj/bracket.py:161` | `:161` is the `if count == 0:` guard; the return is `:162`; first `.score` at `:169` | off by one — `F8` |
| folds score into `input_digest` | `atj/bracket.py:911` | `:911` is the f-string fragment holding `team.score` inside `roster_digest` | correct |
| `framework_commit` read from git at build time | `atj/versions.py:144-164` | `require_personas`, `components_available`, head of `check_personas`; no git call. The function is `framework_commit` at `:216-238`, git at `:225` | wrong range — `F2` |
| both teams `affiliation_group: beekeeper-lab` | `teams.md:11-12` | `:11` team-scribe, `:12` team-demos, both `beekeeper-lab` | correct |
| override authority | `event.md:96-107` | "Eligibility and human officials"; `:103` names the role | resolves, but see `F4` |
| adjudications accepting the `NE`s | `adj:trial-2-2026:team-scribe:01`, `adj:trial-2-2026:team-demos:01` | both IDs present in `adjudications/` front matter | correct |
| roster frozen 2026-09-21, unmodified since | — | last commit touching `teams.md` is `2dec830`, 2026-09-21 19:55 -0400 | correct |
| verify reports `PASS (constraints re-derived from the roster)` | — | exact string reproduced | correct |
| `judge-matchup@1.0.0` runs both passes | — | `framework/personas.md:45`, skill, version 1.0.0 | correct |

`F2` is the one that matters. The sentence it supports is true — I proved it by
rebuild — but the reader who follows the citation lands on persona-drift code and
has no way to check it. A citation that resolves is not a citation that supports.

## The two tables are the renderer's output

`atj/render.py:bracket_tables` was run over the committed `bracket.json` and its
output diffed against `bracket.md` lines 68-70 and 85-94. Both diffs are empty.
The only permitted departures — the trailing "Reproduce with:" line dropped, and
prose between the two tables — are the only departures present. The command in
the report's Reproduction block carries the same seed and digest the dropped line
would have carried.

`bracket.md`'s two table headers do not match `framework/templates/bracket-report.md`.
That is the template's defect, not the report's: see `F10`.

## The infeasible constraint and its acceptance

`bracket.json` reports six constraints — three hard satisfied, one hard
not-applicable, one hard infeasible, one soft maximized — and
`unsatisfied_hard_constraints` holds exactly one entry. `bracket.md:81-83` counts
them correctly.

The infeasibility is real and unavoidable. Two teams, one affiliation group, one
match: `pairing_feasible` has no assignment to find. `atj/bracket.py:775` sets
`feasible` from the hard failures and `verify` at `:969-978` would reject a file
claiming otherwise. The soft form reporting `maximized` at round 1 is what
`framework/rubrics/bracket-assignment.md:30` prescribes when perfect separation
is impossible.

The override record satisfies `build-bracket` step 6 in substance. It names the
right constraint and the right exception string, it is schema-valid against
`schemas/manual-override.schema.json`, it carries `authorized_by: event-director`,
and its central claim — that `bracket.json` is unmodified — is true: the
committed file is bit-identical to a fresh build but for `framework_commit`.

Its "nothing downstream is stale" claim is also true. No score, winner, ranking
or placement exists to move; the commit touched five files and none is a
judgment, a summary, a manifest or the roster; `git show --stat abc7e7a` confirms
it. The row that says this audit is "not yet written" was accurate when written
and is now discharged.

Two defects. The authority is cited to an enumeration that does not contain the
category being claimed (`F4`), and `scope: stage` sits beside a populated
`match_id` (`F15`).

There is also a gap underneath the record that is not the record's fault.
`feasible` appears nowhere in `atj/event.py`. No validator, no gate and no
advance command reads it, and no code reads `events/<event>/overrides/` at all.
The only thing that stopped an infeasible draw from being used silently here is
that an operator read step 6 and an auditor checked it. That is `F9`.

## The disclosure decision

`audits/consolidation.md` F34 recorded, as an accepted advisory, that both
summaries enumerate weaknesses in the submissions at exact file and line, and
required the question be settled with the event director before the dossier
stage. It is settled at the bracket stage, which is earlier, and the reasoning is
checkable. Four of its five load-bearing claims verify.

**Repository visibility — verified independently.** `gh repo view` reports
`PUBLIC` and `isPrivate: false` for `beekeeper-lab/ScribeVault`,
`beekeeper-lab/ai-security-demos` and `beekeeper-lab/ai-tournament-judge` as of
2026-09-23. Both pinned commits resolve through the public API:
`67969dd9479c096f05d998d8c50e5ea1968e3245` and
`dc35f6962130af5e5be3fe16672e3d4964850eb9`. The private-source condition
`event.md:182-184` guards is genuinely not met, and "every cited line is already
readable by anyone at the pin" is true. This event's own memory of a false
visibility reason surviving three rounds of correct numbers is why this was
checked against the API rather than against the sentence.

**The three named weaknesses — all present, one overstated.** The unescaped
markdown-to-`setHtml` path is at `judgments/team-scribe/judge-security-ops.md:155`
and `summaries/team-scribe.md:230`. The four `OPENAI_API_KEY` read sites are at
`judge-product-agentic.md:110`, `judge-backend.md:103` and
`summaries/team-scribe.md:241`. The `subprocess.run(..., shell=True)` call site is
at `judge-security-ops.md:125` and `summaries/team-scribe.md:417` — where the
judge records it as "a pattern to remove rather than a finding" and the summary
files it under D3, minority findings. Calling it a weakness draws it stronger
than its source: `F13`. All three examples come from one team: `F14`.

**`public_scores` — unchanged and still false.** `event.md:14` is untouched by
the diff. `atj/publication.py:284` confirms the flag controls numeric scores in
public artifacts, not whether public artifacts exist, so approving artifacts
while keeping scores out is coherent with the code.

**No safety, evidence or privacy rule is weakened.** The decision does not touch
the rubric, weights, personas, bracket policy or evidence, which is the list
`CLAUDE.md` freezes during an active event. It leaves per-artifact approval
intact and explicitly keeps `atj validate publication` in front of `public/`. The
report boundaries stand.

**Two claims do not hold.** `event.md:177` says `public/` "was empty until the
decision below"; `public/` contains only `.gitkeep` and this decision produced no
public artifact (`F6`). And `event.md:204-205` says "A reader learns where to
look, not what the code says", which the artifacts it approves contradict —
`summaries/team-scribe.md:243` quotes the KDF input literal in full, and
`judge-security-ops.md:153` quotes the `.env` key literal (`F7`). Neither changes
the decision. Both are the kind of sentence that gets quoted later as if it had
been verified.

**The process is the larger problem.** Publication approval is one of the five
decisions `framework/templates/manual-override-record.md:34-35` reserves to
humans, and `event.md:25` names `publication_approval: event-director`. This
commit recorded its bracket rules exception as an override record and its
publication approval as prose in the event configuration. `event.md` sits at the
event root, so `atj validate reports` never sees it; no validated artifact
carries `authorized_by` for this decision; and the approval is now mixed into a
file that also holds frozen configuration. That is `F3`.

**Against F34 and against the plan.** The decision does not contradict F34. F34
called the repositories "third-party"; `event.md:100` and `teams.md` say they are
the operator's own, so the decision corrects F34 rather than contradicting it,
though it does not say it is doing so. The `H4` reference at `event.md:212` is
bare — `H4` is defined at `docs/0.5.0-beta-plan.md:107`, not in `event.md`, and
`event.md:69` establishes the convention of saying "in the plan". H4's stated
observation asks for `public_scores` set; the decision keeps it false and asserts
H4 becomes a real test anyway. That is defensible here only because neither team
carries an official total, which `event.md:219` says. Folded into `F14` rather
than raised separately; it changes nothing.

`docs/0.5.0-beta-plan.md:287-294` R5 reserves its display-name mitigation for
third-party projects that did not consent. Neither team is one. R5 does not apply
and the decision correctly does not invoke it.

## Status ledger

Four new rows, all in chronological order among themselves and all after the
`2026-09-22T21:11:39Z` row they follow. The pre-existing out-of-order rows above
that one are the reconstructed timestamps `audits/consolidation.md` round four
already recorded, and are out of this scope.

| Row | Claim | Checked |
|---|---|---|
| `2026-09-23T01:55:10Z` | build at seed, then verify, re-derived from roster and passed, no team placed by hand; digest `0fa1d02b4c6f44c3`, one match, 0 byes, `feasible: false` | every value matches `bracket.json`; rebuild and both verify modes reproduce |
| `2026-09-23T10:49:58Z` | director accepted; both teams `beekeeper-lab`; category `rules exception`; authority `event.md:96-107`; `bracket.json` unmodified | matches the override record and the roster; the authority citation carries `F4` |
| `2026-09-23T10:51:23Z` | tables are `bracket_tables` output; the no-score claim proved twice via `:161` and six permutations | tables byte-identical; permutations reproduce; `:161` carries `F8` |
| `2026-09-23T10:52:05Z` | three repositories checked public; publication approved with citations intact; `public_scores` stays false | visibility verified by `gh`; `public_scores` unchanged in the diff |

No timestamp runs ahead of real clock. The last is `10:52:05Z`; the commit is
authored `2026-09-23 06:53:15 -0400`, which is `10:53:15Z`, 70 seconds later.
Local time is UTC-4 and every stamp is written in UTC, correctly. `last_updated`
matches the final row.

One omission: `units: []`. `atj/event.py:959-975` derives a `bracket:draw` digest
over `bracket.json`, `teams.md` and the summaries specifically so the draw can be
a ledger unit — D21 added it because the bracket stage was invisible to
`stale_units` and to the `can_advance` drift check. No unit was recorded, so an
edit to `bracket.json` after this point would be invisible to both. This event has
recorded no units at any stage, so it is not a bracket-stage regression, but the
bracket is the first stage for which the framework built the digest on purpose.
`F12`.

`status.md.bak` sits in the event directory. It is gitignored, was not committed,
and reaches no public surface. Not a finding.

## Nothing was scored, judged, or re-evidenced

`git show --stat abc7e7a` lists five files: `bracket.json`, `bracket.md`,
`event.md`, the override record and `status.md`. No judgment, no summary, no
evidence manifest, no run record and no roster row was touched. Neither team has
an official total and neither gained one. `atj event validate` reports 0 problems
and `atj validate reports` reports 0 findings over all 22 artifacts it can see.
The provisional sums 32.5 and 52.5 appear in `bracket.md:49` labelled not
official and not usable for seeding, which is what `status.md` and both
adjudications say.

## Untrusted-content scan

`team-demos` is a repository of LLM-attack demonstrations and its own content is
designed to instruct a reader. None of it reached this stage. The four artifacts
in scope, plus `bracket.json`, were scanned for reader-directed instruction,
role reassignment, system-prompt framing and suppression directives; there are
zero matches. `event.md:143-163` already states the rule for quoted
agent-instruction files, and no such file is quoted in anything this stage wrote.
Every claim in this audit that rests on a submission rests on a judgment or a
summary that cites it, never on the submission's own text.

## Findings

| Severity | Rule | Artifact | Scope | Blocking | Finding | Required repair |
|---|---|---|---|---|---|---|
| major | artifact shape | `atj/reports.py:26-45,782-793` | framework | no | `F1`. `bracket.md` is validated by nothing. `ARTIFACT_KINDS` maps only event subdirectories and `validate_event_reports` walks only those, so the 22 artifacts reported both before and after the report was written never included it. There is no `bracket-report` schema. `atj/event.py:61` requires the file to exist and checks nothing about it, and the `bracket:draw` ledger digest at `atj/event.py:959-975` covers `bracket.json`, `teams.md` and the summaries but not the report. Same family as evidence `F14`: a required artifact outside every check | register a `bracket-report` kind with a schema and route root-level artifacts, or move the report under a validated subdirectory. Framework work; do not change framework shape mid-event |
| major | evidence citation | `events/trial-2-2026/bracket.md:120` | event | no | `F2`. The report cites `atj/versions.py:144-164` for "`framework_commit` is read from git at build time". That range holds `require_personas`, `components_available` and the head of `check_personas` and contains no git invocation. The real function is `framework_commit` at `:216-238`, with the `rev-parse HEAD` call at `:225`. The claim is true and I verified it by rebuild; the citation cannot be used to check it | cite `atj/versions.py:216-238` |
| major | authority and record type | `events/trial-2-2026/event.md:186-221` | event | no | `F3`. Publication approval is reserved to a human official by `framework/templates/manual-override-record.md:34-35` and assigned to `event-director` by `event.md:25`. It was recorded as a new subsection of the event configuration rather than as a manual override record. `event.md` is at the event root, so `atj validate reports` does not see it; no validated artifact carries an `authorized_by` for this decision; and an approval now lives inside a file that also holds frozen configuration. The same commit handled the bracket exception correctly | record it as `overrides/ovr-trial-2-2026-publication-disclosure.md`, category `publication`, `authorized_by: event-director`, and reduce the `event.md` subsection to a pointer |
| minor | authority citation | `overrides/ovr-trial-2-2026-bracket-affiliation.md:44-48` | event | no | `F4`. The record declares category `rules exception` and cites `event.md:96-107`, which says `event-director` "holds all four authorities". The four are the `officials` keys at `event.md:23-27`: disqualification, adjudication, publication_approval, security_escalation. "Rules exception" is not among them. The authority that does grant it is `framework/policies/disagreement-and-adjudication.md:9`, which the record does not cite. The template warns at `:49` that an override with no cited authority is a finding; this one has an authority that does not cover its own category | add `framework/policies/disagreement-and-adjudication.md:9` and `framework/templates/adjudication-report.md:112` to the Authority section |
| minor | schema coverage | `schemas/event.schema.json:30-38` | framework | no | `F5`. The framework reserves five decisions to humans and the `officials` object declares four keys. Rules exceptions and unresolved final ties have no event-level owner, which is the root cause of `F4` | add `rules_exception` and `tie_resolution`, or state in the description that `adjudication` covers them |
| minor | false statement | `events/trial-2-2026/event.md:176-177` | event | no | `F6`. "`public/` was empty until the decision below" implies it is no longer empty. It holds only `.gitkeep`; this decision produced no public artifact and the matchup stage has not run | "`public/` stays empty until an artifact passes `atj validate publication` under the decision below" |
| minor | claim stronger than source | `events/trial-2-2026/event.md:204-205` | event | no | `F7`. "A reader learns where to look, not what the code says" is contradicted by the artifacts the same paragraph approves. `summaries/team-scribe.md:243` quotes the KDF input literal verbatim and `judgments/team-scribe/judge-security-ops.md:153` quotes the `.env` key literal. The decision survives without the sentence | drop it or restate it to what the reports actually do |
| minor | line reference | `events/trial-2-2026/bracket.md:52`, `status.md` 10:51:23Z row | event | no | `F8`. "`atj/bracket.py:161` returns from `choose_byes`" — `:161` is `if count == 0:`, the return is `:162`, the first `.score` access is `:169`. The proof holds; the pointer is one line short of the thing it proves | cite `:161-162` and name `:169` as the access it precedes |
| minor | unenforced policy | `atj/event.py` | framework | no | `F9`. `build-bracket` step 6 is enforced by prose alone. `feasible` is read nowhere in `atj/event.py`; `atj event validate`, `gate` and `advance` never look at it; no code reads `events/<event>/overrides/`. Only `atj/cli.py:894` warns, at build time, and an operator who does not read stdout loses it. An event can pass every deterministic check on a `feasible: false` draw with no acceptance on record | require, at stage index >= bracket, an override record naming each unsatisfied hard constraint. Framework work |
| minor | template drift | `framework/templates/bracket-report.md:32-38` | framework | no | `F10`. The template declares `\| Slot \| Team or bye \| Region \| Entry round \| Constraint notes \|` and a three-column constraint table; `atj/render.py:212` and `:220` emit `\| Slot \| Entrant A \| Entrant B \| Entry \| Notes \|` and a four-column constraint table. A report that is correct is guaranteed to diverge from the template, and `F1` is why nobody noticed | align the template with `bracket_tables` |
| minor | falsified pre-registration unrecorded | `events/trial-2-2026/bracket.md` | event | no | `F11`. `event.md:91-94` pre-registered that the shared affiliation would be "a cost rather than a constraint, so the bracket record is expected to carry that cost as a reason string rather than fail". The draw returned `feasible: false`. For a trial whose subject is the framework and which pre-registers its expectations, a falsified expectation that no artifact records is lost data. `event.md` may not be edited to fix it | add a sentence to bracket.md's infeasible-constraint section recording the miss and its cause. Do not edit `event.md` |
| minor | ledger | `events/trial-2-2026/status.md` | event | no | `F12`. `units: []`; `atj event status` reports "units: none recorded". `atj/event.py:959-975` builds a `bracket:draw` digest precisely so the draw can be a ledger unit (D21, which exists because the bracket stage was invisible to `stale_units` and the `can_advance` drift check). No unit was recorded, so a later edit to `bracket.json` is undetectable by either | `python3 -m atj event unit events/trial-2-2026 record --id bracket:draw --stage bracket --output bracket.json --audit-result not-audited --completed-at 2026-09-23T01:55:10Z` |
| advisory | claim stronger than source | `events/trial-2-2026/event.md:199-202` | event | no | `F13`. The `subprocess.run(..., shell=True)` call site is offered among "the weaknesses it names". `judgments/team-scribe/judge-security-ops.md:125` records it as "a pattern to remove rather than a finding" and `summaries/team-scribe.md:415-419` files it under D3, minority findings, with "recorded both as patterns to fix rather than demonstrable defects" | substitute a confirmed weakness or qualify this one as the minority observation it is |
| advisory | coverage of the reasoning | `events/trial-2-2026/event.md:199-207` | event | no | `F14`. All three examples come from ScribeVault while the decision covers both reports. `summaries/team-demos.md` carries 13 file-and-line citations into a repository whose stated purpose is demonstrating attacks, a case the reasoning never addresses. The bare `H4` at `:212` also resolves only in `docs/0.5.0-beta-plan.md:107`, and H4's observation there asks for `public_scores` set, which this decision keeps false | name one team-demos citation, say why the attack-demo case needs no different treatment, and write "`H4` in the plan" as `event.md:69` does |
| advisory | field coherence | `overrides/...-bracket-affiliation.md:5-6` | event | no | `F15`. `scope: stage` with `match_id: mu:trial-2-2026:final:01`. `schemas/manual-override.schema.json` permits both and no code reads either, so nothing breaks; but `scope` is the field that says how far an override reaches and a populated `match_id` reads as `scope: match` | null the `match_id`, or state in the body that the stage scope is deliberate and the match_id is simply the only match the stage produced |
| advisory | validator robustness | `atj/cli.py:1015` | framework | no | `F16`. `atj bracket verify --reproduce` raises an unhandled `TypeError` on a roster JSON that is a bare list instead of `{"teams": [...]}`, while `atj/bracket.py:918-921` states that a validator raising on malformed input has failed at its job. `.claude/skills/build-bracket/SKILL.md` step 5 says `--reproduce <roster.json>` and does not state the shape | validate the payload and report the expected shape; state it in the skill |

## Advisories

Three things are right in a way worth recording, because the next round will be
tempted to undo them.

`bracket.json` was not edited to make the draw look feasible. The override
changes what the event does with the result and leaves the result alone. That is
the correct shape for a manual override and it is the first one this framework
has produced against a real infeasibility.

The bracket report proves its central claim two independent ways — a code path
and an experiment — and the experiment reproduces exactly. It is the first
artifact in this event whose reasoning I could re-run rather than re-read. The
three defects in it are all citation defects; no conclusion in it is wrong.

The disclosure decision was checked against the API rather than against a
sentence, and it is right. This event's own record includes a false visibility
claim that survived three rounds of correct numbers. This one is true.

One thing to carry forward: `F1`, `F9` and `F10` together say that the bracket
stage is the least-instrumented stage in the framework. The draw is checked
exhaustively; everything wrapped around it — the report, the acceptance, the
template — is checked by an auditor reading prose. The consolidation stage had
`atj score` and `atj render consolidated` to fall back on. This stage had
`bracket verify` and nothing else.

## Completion gate

- [x] No blocking findings
- [ ] No major findings — three, `F1`, `F2` and `F3`
- [x] Calculations valid — the draw reproduces from its seed; the digest moves only with the roster; no score exists to calculate
- [ ] Evidence references resolve — `F2` resolves to unrelated code; `F4` and `F14` resolve to text that does not carry the claim
- [x] Version and identity checks pass — `release-check` PASS including version-skew; `build-bracket@1.0.0`, `judge-matchup@1.0.0` and `judging-auditor@1.1.0` all current in `framework/personas.md`; no superseded pin in any artifact this stage wrote
- [x] Privacy boundary passes — `public/` empty, `public_scores` unchanged and false, `atj validate publication` CLEAR over 22 artifacts, no private data in any public surface. The decision at `F3` is a record-type defect, not a leak
- [x] Every finding recorded in `findings:` with a `scope` and a `blocking` flag
- [ ] Approved with `atj event approve <this file>`

## Required repairs before re-audit

1. `F2` — correct the `atj/versions.py` citation in `bracket.md:120` to
   `:216-238`.
2. `F3` — write `overrides/ovr-trial-2-2026-publication-disclosure.md` and cut
   the `event.md` subsection down to a pointer at it.
3. `F4` — add the policy line that actually grants a rules exception to the
   override's Authority section.
4. `F6`, `F7`, `F8` — three sentences, as specified in the findings table.
5. `F11` — record the falsified `event.md:91-94` expectation in `bracket.md`,
   not in `event.md`.
6. `F12` — record the `bracket:draw` ledger unit.
7. `F1`, `F5`, `F9`, `F10`, `F16` — framework scope. Record them for the next
   framework window; do not change framework shape inside this event.

Re-audit the repair diff before the tournament stage. Each of this event's four
prior repair rounds introduced new defects, and every one of the seven repairs
above touches an artifact this audit has now read closely enough to have its own
errors.
