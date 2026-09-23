---
event_id: trial-2-2026
audit_scope: bracket stage, rounds one through three — the draw, the override records, the bracket report, the disclosure decision, the ledger, and two repair rounds
audit_id: bracket
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.1.0
persona: judging-auditor@1.1.0
framework_commit: 92e922e0e4b53d6ba5d02d5b57c76e2b4a6d1f4e
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: '2026-09-23T10:55:00Z'
completed_at: '2026-09-23T14:36:00Z'
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
  repair: deferred to docs/0.5.0-beta-plan.md W15, verified accurate in round two. Every line reference in W15 resolves and the scope is correctly framework. Round two also demonstrated it — the repair rewrote bracket.md and the bracket:draw unit stayed non-stale
  state: deferred
- id: F2
  severity: major
  scope: event
  blocking: false
  summary: bracket.md:120 cites `atj/versions.py:144-164` for reading framework_commit from git; that range is require_personas, components_available and the head of check_personas, and contains no git call
  artifact: events/trial-2-2026/bracket.md:120
  repair: done and verified in round two — bracket.md:135-136 now reads `atj/versions.py:216-238`, the `framework_commit` function, with the `git rev-parse HEAD` call at `:225`. Both resolve exactly
  state: repaired
- id: F3
  severity: major
  scope: event
  blocking: false
  summary: the publication and disclosure approval — a decision event.md reserves to the event-director — was written into the event configuration as prose instead of recorded as a manual override record, so no validated artifact carries an authorized_by for it
  artifact: events/trial-2-2026/event.md:186-221
  repair: 'done and verified in round two — the decision is `overrides/ovr-trial-2-2026-publication-disclosure.md`, `scope: event`, category `publication`, `authorized_by: event-director`, and `atj validate reports` now reaches it as one of 24 artifacts. event.md:187-204 is a pointer. The new record carries its own defects: N1, N2, N6, N7, N8, N10, N11, N12'
  state: repaired
- id: F4
  severity: minor
  scope: event
  blocking: false
  summary: the override cites event.md:96-107 — "event-director holds all four authorities" — as authority for a `rules exception`, which is not one of the four officials keys event.md declares
  artifact: events/trial-2-2026/overrides/ovr-trial-2-2026-bracket-affiliation.md:44-48
  repair: done and verified in round two — the Authority section now leads with `framework/policies/disagreement-and-adjudication.md:9`, names `event.md:103` for the official, and states the four-of-five gap and where it is recorded. All four citations resolve
  state: repaired
- id: F5
  severity: minor
  scope: framework
  blocking: false
  summary: schemas/event.schema.json officials declares four keys while the framework reserves five decisions to humans; rules exceptions and unresolved final ties have no event-level owner
  artifact: schemas/event.schema.json:30-38
  repair: deferred to docs/0.5.0-beta-plan.md W16, verified accurate in round two. "The first override this framework has ever produced" checks out — only two override records exist anywhere under events/, both written by this stage
  state: deferred
- id: F6
  severity: minor
  scope: event
  blocking: false
  summary: event.md:177 says "`public/` was empty until the decision below"; `public/` holds only .gitkeep and this decision produced no public artifact
  artifact: events/trial-2-2026/event.md:176-177
  repair: 'done and verified in round two — event.md:176-178 now reads "`public/` stays empty until an artifact passes `atj validate publication` under the decision below", which is true. The 11:09:00Z ledger row misdescribes how it was fixed: N4'
  state: repaired
- id: F7
  severity: minor
  scope: event
  blocking: false
  summary: event.md:204-205 "A reader learns where to look, not what the code says" is contradicted by the artifacts it approves — summaries/team-scribe.md:243 quotes the KDF input literal verbatim
  artifact: events/trial-2-2026/event.md:204-205
  repair: done and verified in round two — the sentence now reads "A reader mostly learns where to look rather than what the code says, though not always" and cites summaries/team-scribe.md:243 as the exception. The concession is the right repair and the citation resolves
  state: repaired
- id: F8
  severity: minor
  scope: event
  blocking: false
  summary: bracket.md:52 and the 10:51:23Z ledger row say `atj/bracket.py:161` returns; :161 is the `if count == 0:` guard, the return is :162, and the first `.score` access is :169
  artifact: events/trial-2-2026/bracket.md:52
  repair: 'done and verified in round two in both places — ":161-162 is a `count == 0` guard that returns from `choose_byes` before the first `.score` access, which is at `:169`". All three line numbers resolve. The same shape was reintroduced elsewhere in the same repair: N9'
  state: repaired
- id: F9
  severity: minor
  scope: framework
  blocking: false
  summary: nothing enforces build-bracket step 6 — `feasible` is read nowhere in atj/event.py and no code reads events/<event>/overrides/, so an event can advance past the bracket stage on a feasible false draw with no override record and every deterministic check passes
  artifact: atj/event.py
  repair: deferred to docs/0.5.0-beta-plan.md W17, verified accurate in round two. Re-checked after the repair added a second override record — still no code path reads overrides/
  state: deferred
- id: F10
  severity: minor
  scope: framework
  blocking: false
  summary: framework/templates/bracket-report.md declares table shapes atj/render.py bracket_tables does not produce
  artifact: framework/templates/bracket-report.md:32-38
  repair: deferred to docs/0.5.0-beta-plan.md W18, verified accurate in round two
  state: deferred
- id: F11
  severity: minor
  scope: event
  blocking: false
  summary: event.md:91-94 pre-registered that the shared affiliation would be carried as a cost rather than a constraint; the draw returned feasible false, and no stage artifact recorded that the event's own stated expectation was wrong
  artifact: events/trial-2-2026/bracket.md
  repair: 'a paragraph was added at bracket.md:107-117 and event.md was correctly left alone, so the omission is closed. The paragraph''s content is defective: N3 (the policy is miscounted and the cause is misassigned), N5 (the framework finding underneath it) and N9 (the `:760` citation)'
  state: repaired
- id: F12
  severity: minor
  scope: event
  blocking: false
  summary: 'no ledger unit was recorded for the draw — status.md front matter was `units: []`'
  artifact: events/trial-2-2026/status.md
  repair: done and verified in round two by recomputation — `derive_digests` returns `bracket:draw = 3c88ccc1e0f9f863`, matching the recorded unit exactly, `stale_units` returns empty, and `completed_at` is stamped 2026-09-23T01:55:10Z, the build time rather than the record time
  state: repaired
- id: F13
  severity: advisory
  scope: event
  blocking: false
  summary: event.md:201 presents the `subprocess.run(..., shell=True)` call site among "the weaknesses it names"; the panel files it under D3 minority findings
  artifact: events/trial-2-2026/event.md:199-202
  repair: done and verified in round two — the example is gone from the relocated reasoning and appears nowhere in the new override record
  state: repaired
- id: F14
  severity: advisory
  scope: event
  blocking: false
  summary: all three disclosure examples came from ScribeVault while the decision covers both reports; team-demos was never shown against the reasoning
  artifact: events/trial-2-2026/event.md:199-207
  repair: not repaired. The new record gives a count instead of a citation and the count is wrong. See N2. The `H4` half is repaired — `overrides/ovr-trial-2-2026-publication-disclosure.md:85` now reads "`H4` in `docs/0.5.0-beta-plan.md`"
  state: open
- id: F15
  severity: advisory
  scope: event
  blocking: false
  summary: 'the bracket override carries `scope: stage` with a populated `match_id`'
  artifact: events/trial-2-2026/overrides/ovr-trial-2-2026-bracket-affiliation.md:5-6
  repair: done and verified in round two — a paragraph at :42-47 states that the draw is what is accepted, that `atj bracket build` reports the exception against the bracket rather than a pairing, and that the match_id is populated because the stage produced exactly one match. Explained rather than changed, which the finding permitted
  state: repaired
- id: F16
  severity: advisory
  scope: framework
  blocking: false
  summary: atj bracket verify --reproduce raises an unhandled TypeError on a roster JSON that is a bare list
  artifact: atj/cli.py:1015
  repair: deferred to docs/0.5.0-beta-plan.md W19, verified accurate in round two
  state: deferred
- id: N1
  severity: major
  scope: event
  blocking: false
  summary: the new record's whole justification for treating team-demos no differently — "its weaknesses are its subject matter ... discloses nothing the repository does not set out to teach" — is contradicted by the panel report it summarizes, whose five confirmed team-demos defects are documentation, missing tests, a broken guard, over-broad tool pre-approvals and a bypassable gate
  artifact: events/trial-2-2026/overrides/ovr-trial-2-2026-publication-disclosure.md:77-80
  repair: 'done and verified in round three — the paragraph retracts the ''weaknesses are its subject matter'' ground in terms, states PD3, PD4 and PD5, and approves on the ground that actually holds. PD4''s restatement was re-derived at the pin: screen-pile-audited.md:4 carries Bash(rm:*) and line 30 holds the one fixed rm. PD5''s was checked against 06-approval-is-the-architecture/demo/README.md:19-22,66-74,88. The ''does not currently teach'' judgement holds for all three: the demo-09 README at :117 asserts the opposite of PD3. Residual defects: P1 and P4'
  state: repaired
- id: N2
  severity: major
  scope: event
  blocking: false
  summary: F14 is not repaired and the ledger certifies that it is; the record names no team-demos citation and its substitute count, "thirteen file-and-line citations", is wrong — summaries/team-demos.md carries 20 occurrences and 16 distinct file-and-line references, and thirteen is the line count of a .py-only pattern taken from this audit's round one without re-derivation
  artifact: events/trial-2-2026/overrides/ovr-trial-2-2026-publication-disclosure.md:71
  repair: 'the count is gone and two citations are named, which closes the count half. One of the two is a strength citation and not a weakness: P1'
  state: repaired
- id: N3
  severity: major
  scope: event
  blocking: false
  summary: the new F11 paragraph miscounts the policy and misassigns the cause — bracket-assignment.md states affiliation separation at :22, :27, :28, :29 and :30, not twice, and the omitted :22 is the governing Priority entry that says "Maximize", which is exactly the reading event.md:91-94 took
  artifact: events/trial-2-2026/bracket.md:107-117
  repair: 'done and verified in round three — bracket.md:107-128 now states the divergence, and the negative claim was re-checked across the whole 44-line policy: the word ''hard'' does not appear in framework/rubrics/bracket-assignment.md at all. P2 and P5 are residual'
  state: repaired
- id: N4
  severity: minor
  scope: event
  blocking: false
  summary: the 11:09:00Z ledger row misdescribes the repair in three places — it groups F6 with "repaired by moving the reasoning into the override record" when F6 was a reword of event.md:176-178, it says the record states "the citations it approves in full" when it states two and a count, and it says "including a team-demos one" when no team-demos citation is named
  artifact: events/trial-2-2026/status.md
  repair: done and verified in round three — F6 separated as a reword of event.md:176-178, F7 and F13 described by what the record does, F14 recorded as attempted and not repaired pointing at N2. Every claim in the restated row checks out
  state: repaired
- id: N5
  severity: minor
  scope: framework
  blocking: false
  summary: framework/rubrics/bracket-assignment.md states affiliation separation only as a priority to "maximize" and as targets, and never as a hard constraint, while atj/bracket.py:543-554 emits it with kind hard and atj/bracket.py:758-761,775 lets it set feasible false — a policy that says maximize produces an infeasible bracket
  artifact: framework/rubrics/bracket-assignment.md:22,25-30
  repair: 'carried to docs/0.5.0-beta-plan.md W20, verified in round three. Every line reference in W20 resolves. Its closing sentence about what may land mid-event is imprecise: P3'
  state: deferred
- id: N6
  severity: minor
  scope: event
  blocking: false
  summary: 'the new record cites event.md:25 for officials.publication_approval in three places including the Authority section and a Validation checkbox; :25 is `adjudication: event-director` and publication_approval is at :26'
  artifact: events/trial-2-2026/overrides/ovr-trial-2-2026-publication-disclosure.md:40,46,120
  repair: 'done and verified in round three — event.md:26 in all four places, and :26 is `publication_approval: event-director`'
  state: repaired
- id: N7
  severity: minor
  scope: event
  blocking: false
  summary: the Validation checkbox says "three of the five do not exist yet"; the Downstream effects table marks two rows not yet written, and event.md, public/ and the summaries and judgments all exist
  artifact: events/trial-2-2026/overrides/ovr-trial-2-2026-publication-disclosure.md:126-127
  repair: done and verified in round three — "two of the five", which matches the table
  state: repaired
- id: N8
  severity: minor
  scope: event
  blocking: false
  summary: '"Original artifact preserved unmodified" is ticked while the artifact the record names at :39 as the thing overridden — event.md Publication — was rewritten in the same commit'
  artifact: events/trial-2-2026/overrides/ovr-trial-2-2026-publication-disclosure.md:123-125
  repair: done and verified in round three — the checkbox now records that event.md Publication was rewritten in the same commit and names what was preserved instead of ticking past it
  state: repaired
- id: N9
  severity: minor
  scope: event
  blocking: false
  summary: 'the new F11 paragraph says atj/bracket.py:760 "makes any hard constraint at violated or infeasible set feasible: false"; :758-761 is the predicate that collects hard failures and :775 is where feasible is assigned — the guard-versus-assignment shape F8 had just repaired, reintroduced in the same commit, and it contradicts what round one of this audit recorded'
  artifact: events/trial-2-2026/bracket.md:113-115
  repair: done and verified in round three — :758-761 for the selection and :775 for the assignment, both resolving
  state: repaired
- id: N10
  severity: minor
  scope: event
  blocking: false
  summary: 'event.md:195-196 calls the new override record "a validated artifact carrying who decided"; its own front matter is `validation_state: unvalidated` and `approval_state: draft`'
  artifact: events/trial-2-2026/event.md:195-196
  repair: done and verified in round three — event.md:194-196 now reads "an artifact `atj validate reports` checks"
  state: repaired
- id: N11
  severity: minor
  scope: event
  blocking: false
  summary: the new record cites summaries/team-scribe.md:343 for the unescaped markdown-to-setHtml render path; :343 ends the previous sentence and the render path is named at :344, with the confirmed-weakness statement at :230
  artifact: events/trial-2-2026/overrides/ovr-trial-2-2026-publication-disclosure.md:70
  repair: done and verified in round three — summaries/team-scribe.md:230,344, both of which carry the render path
  state: repaired
- id: N12
  severity: minor
  scope: event
  blocking: false
  summary: the new record carries started_at 2026-09-23T10:47:00Z, copied from the bracket override; it was written at 11:09 in answer to a finding that did not exist until 11:03, and the decision it relocates is stamped 10:52:05Z in the ledger
  artifact: events/trial-2-2026/overrides/ovr-trial-2-2026-publication-disclosure.md:14
  repair: done and verified in round three — started_at is 2026-09-23T11:03:00Z, which is the audit row that produced the finding and is after the 10:52:05Z decision it records
  state: repaired
- id: N13
  severity: minor
  scope: event
  blocking: false
  summary: this audit's round-one front matter carried completed_at 2026-09-23T11:12:00Z while the commit containing it is authored 11:10:26Z, so the report's own completion stamp ran 94 seconds ahead of the commit that holds it
  artifact: events/trial-2-2026/audits/bracket.md
  repair: closed in round two
  state: repaired
- id: N14
  severity: advisory
  scope: event
  blocking: false
  summary: both override records carry persona build-bracket@1.0.0; the bracket-building skill did not produce a publication disclosure record, and the template says persona is what produced the document
  artifact: events/trial-2-2026/overrides/ovr-trial-2-2026-publication-disclosure.md:10
  repair: 'carried into W16 and stated in the record body at :29-33. The explanation offered for the field value is not supported by the ledger: P6'
  state: repaired
- id: N15
  severity: advisory
  scope: framework
  blocking: false
  summary: the repair rewrote bracket.md and the bracket:draw ledger unit stayed non-stale, because derive_digests covers bracket.json, teams.md and the summaries and not the report — W15 demonstrated rather than argued
  artifact: atj/event.py:959-975
  repair: folded into W15, verified in round three — the demonstration is stated accurately
  state: deferred
- id: P1
  severity: major
  scope: event
  blocking: false
  summary: one of the two team-demos citations the record names as an example of what publication discloses is a confirmed strength, not a weakness — summaries/team-demos.md:418-419 credits 10-show-your-work/demo/scripts/explain.py:85-110 for deriving integrity flags from source trust, and :261 cites it as structural enforcement the judges scoring 4 weight positively; it appears nowhere in the report as a defect
  artifact: events/trial-2-2026/overrides/ovr-trial-2-2026-publication-disclosure.md:78-81
  repair: replace it with a real team-demos weakness citation — hardened/clear_the_pile_hardened.py:42-43 for PD5, or 10-show-your-work/demo/.claude/commands/screen-pile-audited.md:4 for PD4, which the same paragraph already names two sentences later — or keep 09-toolbox-you-didnt-audit/demo/tools/toolbox.py:47-51 alone, which is PD17 and is correct. Correct the 11:26:00Z ledger row, which says the paragraph "names two of its citations". The citation was suggested by audits/bracket.md N2 and adopted without checking what the report says about it, the third round running in which this audit own text became the artifact defect
  state: open
- id: P2
  severity: minor
  scope: event
  blocking: false
  summary: '"It changes nothing about this draw" is true of the pairing and false of everything else — under the policy as written the constraint is soft, hard_failures at atj/bracket.py:758-761 is empty, :775 assigns feasible true, and no override record would have been required at all'
  artifact: events/trial-2-2026/bracket.md:126-128
  repair: '"It changes nothing about the pairing — at two teams from one group there is no alternative under either reading — but it is why the draw is `feasible: false` and why this stage needed a human override at all"'
  state: open
- id: P3
  severity: minor
  scope: framework
  blocking: false
  summary: W20 closes "Changing either is a bracket-policy change and may not land while an event is judging"; changing atj/bracket.py:550 is not a bracket-policy change under CLAUDE.md source-of-truth table, which maps bracket policy to framework/rubrics/bracket-assignment.md, and the asymmetry is sharper than W20 states
  artifact: docs/0.5.0-beta-plan.md W20
  repair: 'state the two halves separately: changing the policy file is a frozen-contract change that .claude/hooks/pre-write.sh:41 already blocks for framework/rubrics/*, and changing atj/bracket.py alters a frozen event draw semantics without moving bracket-assignment@1.0.0 and is guarded by nothing. The conclusion — neither lands mid-event — is right and stays'
  state: open
- id: P4
  severity: minor
  scope: event
  blocking: false
  summary: '"Those are real defects in the fix" covers PD4 and PD5 and not PD3, whose guard is the containment rail around demo 09 optional code-POST exfil variant rather than one of the four hardened controls; the record also drops what the panel recorded, that all four judges state there is no observable consequence and urllib rejects the schemeless form so no egress path is demonstrated'
  artifact: events/trial-2-2026/overrides/ovr-trial-2-2026-publication-disclosure.md:88-91
  repair: 'separate PD3 from the two hardened-example defects and carry summaries/team-demos.md:484-485 no-consequence qualifier. PD3 stays in the paragraph on its own merit: 09-toolbox-you-didnt-audit/demo/README.md:117 asserts the guard refuses any host but localhost, which is exactly what makes the gap undisclosed'
  state: open
- id: P5
  severity: advisory
  scope: event
  blocking: false
  summary: the constraint name is attributed to atj/bracket.py:550; :549 carries the name and :550 the kind. The claim the sentence makes, that :550 supplies the hardness, is exactly right and the appositive spills one line
  artifact: events/trial-2-2026/bracket.md:113-115
  repair: cite the audit block as :548-554, or move the constraint name to :549
  state: open
- id: P6
  severity: minor
  scope: event
  blocking: false
  summary: the record explains persona build-bracket@1.0.0 as "the skill that was running when this was written"; it was written at 11:09 and revised at 11:26, both in rounds the ledger records as repairs against audits/bracket.md, and build-bracket own step list ends at writing and auditing the bracket report
  artifact: events/trial-2-2026/overrides/ovr-trial-2-2026-publication-disclosure.md:29-30
  repair: drop the first clause. The second half of the same paragraph — no persona in framework/personas.md produces a human decision record taken outside a stage own skill, which W16 now carries — is both true and checkable, and is the whole explanation the field needs
  state: open
---

# Judging Audit — bracket stage, first pass

## Result

**FAIL**, superseded in place after round three. Round one: sixteen findings —
three major, nine minor, four advisory. Round two, scoped to `ebeb4bd`: eleven
repaired, five deferred to `W15`-`W19`, one open, and fifteen new. Round three,
scoped to `92e922e`: thirteen of the fifteen repaired and verified, two carried
to the plan as `W20` and into `W15`, and **six new findings, one of them
major** — a confirmed strength named as a disclosed weakness, `P1`. No finding
in any round is blocking. Round three's record is the last section of this file.

**FAIL**, as recorded after round two. Round one: sixteen findings —
three major, nine minor, four advisory, none blocking. Round two, scoped to the
repair diff `ebeb4bd`: eleven of the sixteen repaired and verified, five
deferred to the framework plan as `W15`-`W19` and each verified accurate, one —
`F14` — left open, and **fifteen new findings the repair itself introduced**,
three of them major. No finding in either round is blocking.

Round one's original text follows unchanged below. The round-two record is the
section after it.

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

---

# Round two — the repair audited

**FAIL.** Eleven of sixteen repaired and verified, five deferred to the plan and
each verified accurate, one open, and fifteen new findings — three major, ten
minor, two advisory. None blocking.

Scope: the repair diff `git diff ebeb4bd~1 ebeb4bd`, seven files. The draw was
not re-audited. `bracket.json` is byte-identical to the file round one verified
and `bracket verify` still returns `PASS (constraints re-derived from the
roster)`; round one's verification of the draw stands and is not repeated here.

The repair is the best of the five this event has produced. It fixed every
mechanical thing it was asked to fix, it moved the reasoning rather than
restating it, it deferred framework work instead of landing it mid-event, and
two of the five deferrals are sharper as `W` entries than they were as findings.
Its three major defects are all of one kind: **the repair states its reasons
more strongly than the artifacts it cites support**, in the record that
authorizes publication and in the paragraph that explains a falsified
prediction.

## Deterministic validation, re-run after the repair

| Command | Result |
|---|---|
| `python3 -m atj event validate events/trial-2-2026` | PASS, 0 problems, stage bracket |
| `python3 -m atj validate reports events/trial-2-2026` | PASS, **24** artifacts, 0 findings |
| `python3 -m atj validate publication events/trial-2-2026` | CLEAR, 24 artifacts, 0 blocking |
| `python3 -m atj release-check` | PASS, every section |
| `python3 -m pytest tests/ -q` | 517 passed, 5 skipped, 286 subtests passed |
| `python3 -m atj bracket verify bracket.json --event-dir events/trial-2-2026` | `PASS (constraints re-derived from the roster)` |
| `python3 -m atj event status events/trial-2-2026` | stage bracket, gate pending, `units: {'complete': 1}` |
| `atj.event.derive_digests` recomputed | `bracket:draw = 3c88ccc1e0f9f863`, matching the ledger; `stale_units` empty |

24 artifacts is 22 plus `audits/bracket.md` and the new override record.
`bracket.md` is still not one of them, which is `F1` and now `W15`.

## What was repaired, checked one at a time

| Finding | Repair | Verified |
|---|---|---|
| `F2` | `bracket.md:135-136` now cites `atj/versions.py:216-238`, git call at `:225` | yes — `:216` is `def framework_commit`, `:225` is `["git", "-C", str(base), "rev-parse", "HEAD"]`, `:238` ends the function |
| `F3` | new record `overrides/ovr-trial-2-2026-publication-disclosure.md`, `scope: event`, category `publication`, `authorized_by: event-director`; `event.md:187-204` reduced to a pointer | yes for the shape — `validate reports` now reaches it. The record carries eight new defects of its own |
| `F4` | bracket override Authority rewritten to lead with `framework/policies/disagreement-and-adjudication.md:9`, name `event.md:103`, and state the four-of-five gap | yes — all four citations resolve and the quoted policy line is exact |
| `F6` | `event.md:176-178` reworded | yes — the new sentence is true. How it was fixed is misdescribed in the ledger (`N4`) |
| `F7` | the sentence now concedes `summaries/team-scribe.md:243` | yes — the concession is exact and the line quotes the KDF literal |
| `F8` | `bracket.md:52-54` and the 10:51:23Z row now read `:161-162` guard and return, `:169` first access | yes in both places, all three lines resolve |
| `F11` | new paragraph at `bracket.md:107-117`; `event.md` correctly untouched | the omission is closed; the content is wrong in three ways (`N3`, `N5`, `N9`) |
| `F12` | `bracket:draw` unit recorded | yes — digest recomputed independently to `3c88ccc1e0f9f863`, `completed_at` stamped at the build time rather than the record time, which is what `atj/event.py:818-830` intends |
| `F13` | the `shell=True` example dropped | yes — it appears nowhere in the new record |
| `F14` | — | **not repaired.** See `N2` |
| `F15` | a paragraph at `:42-47` explaining the pairing | yes — explaining rather than changing is what the finding permitted, and the explanation is coherent |

## The five deferrals, audited as artifacts

`W15` through `W19` land in `docs/0.5.0-beta-plan.md` after `W14`. Every line
reference in all five resolves, every quotation is exact, and all five are
correctly marked framework scope with no trigger, which matches how `F1`, `F5`,
`F9`, `F10` and `F16` were scoped.

| Entry | Checked |
|---|---|
| `W15` | `atj/reports.py:26-45`, `validate_event_reports`, `atj/event.py:959-975`, `atj/event.py:61` all resolve. "22 artifacts before it was written and 22 after" is right: the override record preceded the report and the report added nothing to the count |
| `W16` | `disagreement-and-adjudication.md:9`, `manual-override-record.md:34-35`, `schemas/event.schema.json:30-38` all resolve. "The first override this framework has ever produced" verified — `find events -path '*/overrides/*.md'` returns exactly the two records this stage wrote |
| `W17` | re-checked after the repair added a second override record. `feasible` still appears nowhere in `atj/event.py` and no code path reads `overrides/`. The sharpest of the five |
| `W18` | `framework/templates/bracket-report.md:32-38`, `atj/render.py:212` and `:220` all resolve and the column names are quoted correctly |
| `W19` | `atj/cli.py:1015`, `atj/bracket.py:918-921` and `build-bracket` step 5 all resolve; the crash is the one round one reproduced |

`W15` also gained a demonstration this round: the repair rewrote `bracket.md` and
`stale_units` still returns empty, because `derive_digests` never hashed the
report. That is `N15`, recorded as evidence for `W15` rather than as work.

## The new override record

Schema-valid, template-complete, reachable by `atj validate reports`, and it
does what `F3` asked. Its authority chain is sound in substance: `event.md:26`
assigns `publication_approval` to `event-director`, `event.md:103` names the
holder, and `manual-override-record.md:34-35` lists publication approval among
the reserved decisions.

Two of its factual claims verify cleanly and are worth naming because they are
the ones a later reader will lean on. `live-trial-2026`'s two submissions are
genuinely private — `gh repo view` reports `PRIVATE` for
`beekeeper-lab/podcast-listener` and `beekeeper-lab/hive-ledger` — so "that guard
was written for `live-trial-2026`, whose two submissions are private" is true and
is the first time this event has said *why* the guard does not reach it. And
"ten demonstrations of attacks against LLM agents" is verbatim from
`submissions/team-demos.md:108`, corroborated at `evidence/team-demos/manifest.md:76`
and `:99`.

**`N1` is the defect that matters.** The record's entire justification for
treating `team-demos` no differently reads:

> Its weaknesses are its subject matter, written to be read and published as
> such, and a report naming them at line level discloses nothing the repository
> does not set out to teach.

The panel's confirmed `team-demos` defects are not its subject matter.
`summaries/team-demos.md` PD1 is a documentation defect — the documented run
instruction cannot reach the offline dry run. PD2 is the absence of any
automated test. PD3 is a POST guard in the author's own safety code that admits
an empty hostname. PD4 is `Bash(rm:*)` pre-approved in seventeen command files
across all ten demos, the seventeenth of which is the capstone's *audited*
screener. PD5 is an approval gate that is a code constant in one run path and a
model-supplied argument in the other, presented by the README as the same fix.

PD4 and PD5 disclose that the repository's own hardened examples are not
hardened. That is the opposite of what it sets out to teach, and it is precisely
the kind of thing a disclosure decision exists to weigh. The decision may well
still be right — both repositories are the operator's own and public, which is
the reason that actually holds and which the record gives two sentences earlier.
The sentence that does the work is the one contradicted by the report it
summarizes.

**`N2`: `F14` is not repaired, and the ledger says it is.** `F14` asked for a
named `team-demos` citation. The record gives a count instead —
"on `team-demos`, thirteen file-and-line citations of its own" — and the count is
wrong. `summaries/team-demos.md` carries 20 file-and-line references, 16 of them
distinct, including `README.md:19-21`, `05/reset-demo.md:3`,
`02-invisible-ink/demo/README.md:66-70`, `06-approval-is-the-architecture/demo/README.md:118-122`
and `09-toolbox-you-didnt-audit/demo/README.md:68-79`, none of which a `.py`-only
pattern sees.

Thirteen is the number of *lines* in that file matching a `.py:` pattern. It is
the figure `audits/bracket.md` reported in round one, adopted without
re-derivation. Round one was wrong twice — it counted lines rather than
citations, and it excluded `.md` citations — and the repair inherited both
errors. This is the event's own recorded lesson about audit findings carrying
their own errors, arriving on schedule.

**Six smaller defects in the same record.** `event.md:25` is cited three times
for `publication_approval`, which is at `:26` — another round-one error copied
forward (`N6`). "Three of the five do not exist yet" is two (`N7`). "Original
artifact preserved unmodified" is ticked while the artifact the record names as
overridden, `event.md` Publication, was rewritten in the same commit (`N8`).
`summaries/team-scribe.md:343` should be `:230,344` (`N11`). `started_at` is
`10:47:00Z`, copied from the bracket override, for a record written at 11:09 in
answer to a finding that did not exist until 11:03 (`N12`). And `persona:
build-bracket@1.0.0` says the bracket-building skill produced a publication
disclosure record (`N14`).

`event.md:195-196` calls the record "a validated artifact" while its own front
matter reads `validation_state: unvalidated`, `approval_state: draft` (`N10`).

## The F11 paragraph

`bracket.md:107-117` closes the omission `F11` named, and `event.md` was
correctly left alone. The paragraph then explains the miss, and the explanation
does not hold.

> The policy states affiliation separation twice: "Two teams from one group:
> target opposite halves" and "When perfect separation is impossible, maximize
> the earliest round in which affiliated teams can meet". `atj/bracket.py:549-550`
> implements the first as a hard constraint and `:573-574` the second as a soft
> one, and `:760` makes any hard constraint at `violated` or `infeasible` set
> `feasible: false`. The prediction read the fallback and missed the target.

Three problems, in increasing order of consequence.

`:549-550` and `:573-574` resolve correctly — `:550` is `"kind": "hard"` and
`:574` is `"kind": "soft"`. `:760` does not. `atj/bracket.py:758-761` is the
comprehension that collects hard failures and `:775` is `"feasible": not
hard_failures`, where the value is actually set. Round one of this audit recorded
`:775`; the repair contradicts it without saying so, and it is the same
guard-versus-assignment shape `F8` repaired four lines earlier in the same file
(`N9`).

"States affiliation separation twice" is wrong.
`framework/rubrics/bracket-assignment.md` states it at `:22`, `:27`, `:28`, `:29`
and `:30`. The omitted `:22` is not a minor one: it is entry 4 of the numbered
**Priority** list that governs the whole policy, and it reads "Maximize
separation among teams sharing an `affiliation_group` such as a school" (`N3`).

Which makes the conclusion wrong. "The prediction read the fallback and missed
the target" says the operator misread the policy. The policy nowhere declares
any affiliation rule a hard constraint. Its governing priority says *maximize*;
its section states targets without hardness; the hardness is supplied by
`atj/bracket.py:550` and by nothing in the policy. `event.md:91-94` read the
policy correctly and the implementation is stricter than the policy states.

That matters beyond the wording. This event's subject is the framework, and its
falsified pre-registration found a real divergence between a policy and the code
that enforces it — a policy that says "maximize" can return `feasible: false` and
require a human override. The repair recorded an operator error instead and the
finding went with it. It is raised here as `N5`, framework scope, for a `W`
entry alongside `W15`-`W19`.

## The ledger

`last_updated` is `11:09:15Z`, written by `atj event unit`, and the commit is
authored `2026-09-23 07:10:26 -0400` = `11:10:26Z`. Both new rows — `11:03:00Z`
for the audit and `11:09:00Z` for the repair — are in order, after the
`10:52:05Z` row, and before the commit. Local time is UTC-4 and every stamp is
UTC. The recorded unit's `completed_at` is `01:55:10Z`, the build time, which is
correct and not the record time.

The `11:03:00Z` audit row is accurate: every claim in it — the reproduction, both
verify modes, byte-identical tables, the permutation experiment, both pins, three
visibilities, `public_scores` unchanged, nothing scored or judged — is something
round one established and this round re-checked.

The `11:09:00Z` repair row is long and mostly right. Ten of its thirteen claims
verify, including the digest, the five deferrals, and "no score, judgment,
evidence reference or bracket value moved", which the diff confirms — the seven
changed files are two overrides, `event.md`, `bracket.md`, `status.md`,
`docs/0.5.0-beta-plan.md` and this audit. Three claims in one clause do not
(`N4`): `F6` was a reword of `event.md:176-178` and not a relocation of
reasoning; the record states two citations and a count, not "the citations it
approves in full"; and "including a `team-demos` one" describes a citation the
record does not contain.

## This audit's own round-one errors

Three, all caught by re-deriving rather than re-reading, and all recorded rather
than quietly fixed.

`audits/bracket.md` round one said `event.md:25` names
`publication_approval: event-director`. It is `:26`. The repair copied the wrong
line into three places in the record that authorizes publication (`N6`).

Round one said `summaries/team-demos.md` carries 13 file-and-line citations. It
carries 20, 16 distinct. Thirteen was a line count from a `.py`-only pattern. The
repair used the number as given (`N2`).

Round one's front matter carried `completed_at: 2026-09-23T11:12:00Z` while the
commit holding it is authored `11:10:26Z` — the report's own completion stamp ran
94 seconds ahead of the commit that contains it. Corrected in this round's front
matter, recorded as `N13`, and noted because it is the same defect class this
audit checks the ledger for.

## Untrusted-content scan, round two

The seven files in the repair diff were scanned for reader-directed instruction,
role reassignment, system-prompt framing and suppression directives. Zero
matches. No `team-demos` content was quoted into any of them; the record's claims
about that repository all trace to `submissions/team-demos.md`,
`evidence/team-demos/manifest.md` and `summaries/team-demos.md`, never to the
repository's own text.

## Findings — round two

| Severity | Rule | Artifact | Scope | Blocking | Finding | Required repair |
|---|---|---|---|---|---|---|
| major | claim contradicted by its source | `overrides/...-publication-disclosure.md:77-80` | event | no | `N1`. "`team-demos` needs no different treatment. It is ten demonstrations of attacks against LLM agents. Its weaknesses are its subject matter ... a report naming them at line level discloses nothing the repository does not set out to teach." The panel's five confirmed `team-demos` defects are a documentation defect (PD1), no automated test of any kind (PD2), a POST guard admitting an empty hostname (PD3), `Bash(rm:*)` pre-approved in seventeen command files including the capstone's audited screener (PD4), and an approval gate that is a constant in one path and a model-supplied argument in the other (PD5). PD4 and PD5 disclose that the repository's own hardened examples are not hardened, which is the opposite of what it teaches. The one sentence carrying the whole justification is contradicted by `summaries/team-demos.md` | restate against PD1-PD5. Give the reason that holds — the repository is the operator's own and public, the same reason as team-scribe — or say what is disclosed beyond the subject matter and why it is approved anyway |
| major | finding not repaired, repair certified | `overrides/...-publication-disclosure.md:71`, `status.md` 11:09:00Z row | event | no | `N2`. `F14` asked for a named `team-demos` citation. The record gives "thirteen file-and-line citations of its own" and names none, and thirteen is wrong: `summaries/team-demos.md` carries 20 file-and-line references, 16 distinct, including five `.md` references a `.py`-only pattern cannot see. Thirteen is the line count this audit reported in round one, adopted without re-derivation. The ledger row states the repair as done and as including a `team-demos` citation | name a citation — `09-toolbox-you-didnt-audit/demo/tools/toolbox.py:47-51` or `10-show-your-work/demo/scripts/explain.py:85-110` — and either drop the count or write sixteen distinct references across `.py` and `.md`. Correct the ledger row |
| major | cause misassigned, source miscounted | `events/trial-2-2026/bracket.md:107-117` | event | no | `N3`. "The policy states affiliation separation twice" — `framework/rubrics/bracket-assignment.md` states it at `:22`, `:27`, `:28`, `:29` and `:30`, and the omitted `:22` is entry 4 of the governing Priority list, "Maximize separation among teams sharing an `affiliation_group`". That is the line `event.md:91-94` tracked. "The prediction read the fallback and missed the target" therefore misassigns the cause: the policy declares no affiliation rule hard anywhere, `atj/bracket.py:550` supplies the hardness, and the prediction matched the policy. In a trial whose subject is the framework, this records an operator error in place of a policy-versus-implementation divergence | restate the cause as the divergence, cite `:22` as the line the prediction tracked, and drop "Nothing in the draw is wrong; the expectation was" |
| minor | ledger misdescribes the repair | `events/trial-2-2026/status.md` 11:09:00Z row | event | no | `N4`. Three claims in one clause are wrong: `F6` is grouped under "repaired by moving the reasoning into the override record" when it was a reword of `event.md:176-178`; "stating the citations it approves in full" describes two citations and a count; "including a `team-demos` one" describes a citation the record does not contain. Ten of the row's thirteen claims verify | restate the clause to what the diff does |
| minor | policy and implementation diverge | `framework/rubrics/bracket-assignment.md:22,25-30` | framework | no | `N5`. The policy states affiliation separation only as a priority to "maximize" and as targets, never as a hard constraint. `atj/bracket.py:543-554` emits it with `kind: hard`, and `atj/bracket.py:758-761,775` lets it set `feasible: false` and require a human override. A policy that says "maximize" produced an infeasible bracket. This is the framework finding `N3` obscured and the substantive result of this event's falsified pre-registration | state the hard form in the policy or downgrade the implementation to soft. Add a `W` entry alongside `W15`-`W19`. Framework scope, do not land mid-event |
| minor | wrong line in an authority citation | `overrides/...-publication-disclosure.md:40,46,120` | event | no | `N6`. `event.md:25` is cited three times — in "What was overridden", in Authority, and in a Validation checkbox — for `officials.publication_approval`. `:25` is `adjudication: event-director`; `publication_approval` is `:26`. Originated in this audit's round-one `F3` text and was copied | `event.md:26` in all three places |
| minor | count wrong in a validation checkbox | `overrides/...-publication-disclosure.md:126-127` | event | no | `N7`. "Three of the five do not exist yet". The Downstream effects table marks two rows "not yet written"; `event.md`, `public/`, the summaries and the judgments all exist | two of the five |
| minor | checkbox ticked against its own record | `overrides/...-publication-disclosure.md:123-125` | event | no | `N8`. "Original artifact preserved unmodified" is ticked while `:39` names `events/trial-2-2026/event.md` — Publication as the artifact, and that section was rewritten in the same commit. The `public_scores: false` half of the claim is true | mark the checkbox not-applicable with the reason, or name what was preserved |
| minor | guard cited as assignment | `events/trial-2-2026/bracket.md:113-115` | event | no | `N9`. "`:760` makes any hard constraint at `violated` or `infeasible` set `feasible: false`". `atj/bracket.py:758-761` collects the hard failures; `:775` is `"feasible": not hard_failures`. Round one of this audit recorded `:775`, so the repair contradicts it silently, and it is the same shape `F8` repaired four lines earlier in the same file | cite `:758-761` for the selection and `:775` for the assignment |
| minor | claim stronger than the field | `events/trial-2-2026/event.md:195-196` | event | no | `N10`. The new record is called "a validated artifact carrying who decided"; its front matter is `validation_state: unvalidated`, `approval_state: draft`. What is true and sufficient is that `atj validate reports` now reaches it | "an artifact `atj validate reports` checks, carrying who decided" |
| minor | line reference off by one | `overrides/...-publication-disclosure.md:70` | event | no | `N11`. `summaries/team-scribe.md:343` is cited for the unescaped markdown-to-`setHtml` render path. `:343` ends the previous sentence; the render path is named at `:344`, and the confirmed-weakness statement is at `:230` | `summaries/team-scribe.md:230,344` |
| minor | provenance stamp | `overrides/...-publication-disclosure.md:14` | event | no | `N12`. `started_at: "2026-09-23T10:47:00Z"`, copied from the bracket override. The record was written at 11:09 in answer to `audits/bracket.md` F3, which did not exist until 11:03, and the decision it relocates is stamped `10:52:05Z` in the ledger | a start time that does not precede the decision it records or the finding that caused it |
| minor | this audit's own stamp | `events/trial-2-2026/audits/bracket.md` | event | no | `N13`. Round one carried `completed_at: 2026-09-23T11:12:00Z` while the commit containing it is authored `11:10:26Z`, 94 seconds earlier. Corrected in this round's front matter and recorded rather than silently fixed | none outstanding |
| advisory | persona field | `overrides/...-publication-disclosure.md:10` | event | no | `N14`. Both override records carry `persona: build-bracket@1.0.0`. The bracket-building skill did not produce a publication disclosure record, and `framework/templates/manual-override-record.md:24-27` says `persona` is what produced the document. There is no persona for a human decision outside the bracket, which is `W16`'s gap one field over. Round one missed this on the bracket override | pick an accurate persona, or extend `W16` to cover the producing-persona gap for human decisions |
| advisory | `W15` demonstrated | `atj/event.py:959-975` | framework | no | `N15`. The repair rewrote `bracket.md` and `stale_units` still returns empty, because `derive_digests` hashes `bracket.json`, `teams.md` and the summaries and not the report. `W15` is no longer an argument about what could go unnoticed | record the demonstration in `W15`. No repair inside this event |

## Completion gate — round two

- [x] No blocking findings
- [ ] No major findings — three, `N1`, `N2` and `N3`; round one's `F1`, `F2` and `F3` are deferred or repaired
- [x] Calculations valid — the `bracket:draw` digest recomputes to the recorded value, `stale_units` is empty, the draw is unchanged from the file round one verified, and no score exists to calculate
- [ ] Evidence references resolve — `N1` cites a report that says the opposite, `N2` states a count no file supports, `N6`, `N9` and `N11` resolve one line off
- [x] Version and identity checks pass — `release-check` PASS, 24 artifacts clean, no version moved in the repair
- [x] Privacy boundary passes — `public/` still holds only `.gitkeep`, `public_scores: false` untouched at `event.md:14`, `atj validate publication` CLEAR over 24 artifacts. `N1` is a defective justification for a decision, not a leak
- [x] Every finding recorded in `findings:` with a `scope` and a `blocking` flag
- [ ] Approved with `atj event approve <this file>`

## Required repairs before round three

1. `N1` — restate the `team-demos` justification against `summaries/team-demos.md`
   PD1-PD5. This is the one that changes what the record means.
2. `N2` — name a `team-demos` citation, fix or drop the count, and correct the
   ledger row that certifies `F14` repaired. `F14` stays open until both are
   done.
3. `N3` and `N9` — rewrite the causal sentences in `bracket.md:107-117` and fix
   the `:760` citation.
4. `N4` — correct the three claims in the `11:09:00Z` ledger row.
5. `N6`, `N7`, `N8`, `N10`, `N11`, `N12` — six single-value corrections in the
   new override record and one in `event.md`.
6. `N5` — a new `W` entry for the policy-versus-implementation divergence.
   `N14` and `N15` fold into `W16` and `W15`. Framework scope, do not land
   mid-event.

Nothing in round three should touch `bracket.json`, the summaries, the judgments,
the manifests or the roster; none of them has moved in either round and none
needs to. Re-audit the round-two repair diff before the tournament stage. Three
of this round's fifteen findings — `N2`, `N6` and `N13` — are errors this audit
made in round one and the repair adopted, which is the strongest argument
available for auditing the repair rather than the finding list.

---

# Round three — the round-two repair audited

**FAIL**, on one open major. All fifteen round-two findings addressed: thirteen
repaired and verified, two carried to the plan as `W20` and into `W15`. Six new
findings — one major, four minor, one advisory. None blocking.

Scope: `git diff 92e922e~1 92e922e`, six files. `bracket.json` was not
re-audited; it is byte-identical to the file round one verified and
`bracket verify` still returns `PASS (constraints re-derived from the roster)`.

This is the strongest repair round this event has produced, and the first whose
central judgement I could confirm against something outside the framework. The
claim that publishing PD3, PD4 and PD5 tells a reader something
`beekeeper-lab/ai-security-demos` does not currently teach was checked against
that repository's own READMEs at the pin `dc35f696`, not against the panel
report that made the claim, and it holds for all three.

The one major is narrow and one line wide. Of the two `team-demos` citations the
record names as examples of what publication discloses, one is a **confirmed
strength**. I suggested that citation in round two's `N2` repair text and the
repair took it without checking what the report says about it. That is now three
consecutive rounds in which this audit's own words became the artifact's defect.

## Deterministic validation, re-run

| Command | Result |
|---|---|
| `python3 -m atj event validate events/trial-2-2026` | PASS, 0 problems, stage bracket |
| `python3 -m atj validate reports events/trial-2-2026` | PASS, 24 artifacts, 0 findings |
| `python3 -m atj validate publication events/trial-2-2026` | CLEAR, 24 artifacts, 0 blocking |
| `python3 -m atj release-check` | PASS |
| `python3 -m pytest tests/ -q` | 517 passed, 5 skipped, 286 subtests |
| `python3 -m atj bracket verify bracket.json --event-dir events/trial-2-2026` | `PASS (constraints re-derived from the roster)` |
| `derive_digests` recomputed | `bracket:draw = 3c88ccc1e0f9f863`, unchanged; `stale_units` empty |

## The `team-demos` paragraph, re-derived at the pin

`N1` and `N2` were repaired together. The paragraph now opens by retracting its
old ground in terms — "not because its weaknesses are its subject matter. They
are not" — states three defects, and approves on the ground that actually holds.
The coordinating instruction was explicit that none of the restatement had been
re-derived from the repository, so none of it is taken from the panel report.

**PD4 — verified directly.** `10-show-your-work/demo/.claude/commands/screen-pile-audited.md`
at `dc35f696` carries `allowed-tools: Read, Glob, Write, Bash(python3:*), Bash(rm:*)`
on line 4, describes itself on line 2 as the "HARDENED/AUDITED screener", and
holds exactly one `rm` — `rm -f reports/decisions/*.json` — on line 30. The
record's sentence is correct in every particular.

**PD5 — verified directly.** `06-approval-is-the-architecture/demo/README.md:19-22`
names path A, Claude Code, and says "**This is the hero path.**" `:88` records
`act.py` with "Safe defaults: `--actor sift-agent --mode gate` (fail closed)",
which is a default and not a constraint. `:66-74` presents the fix as two
constants changed in the Python path, `IDENTITY` and `MODE`, and says nothing
about the hero path supplying the same values as model-written CLI arguments.
"The README presenting the weaker path as the hero path" is a fair compression
of both the report and the README.

**PD3 — verified, and the strongest of the three on the disclosure question.**
`09-toolbox-you-didnt-audit/demo/README.md:117` states: "The POST path is
hard-guarded: it **refuses any host but localhost**. Nothing leaves the machine."
PD3 is that the guard admits an empty hostname. The repository does not merely
fail to teach this; it asserts the opposite.

**So the judgement holds.** "A reader of the public artifact learns something the
repository does not currently teach" is true for all three. The nearest thing to
a counter-example is `10-show-your-work/demo/README.md:115-116`, which does
disclose that `rm` is pre-approved in `allowed-tools` — but scopes it to
"`/reset-demo` and the stage/unstage commands", which is precisely the sixteen
PD4 sets aside. The seventeenth, the audited screener, is not disclosed
anywhere. The record is not wrong in the other direction.

**`P1`, the one major.** The paragraph two sentences earlier names two
`team-demos` citations as examples of what publication discloses, under the
heading "What is actually disclosed" and in a sentence whose subject is
"weaknesses at exact file and line":

> on `team-demos`, its own citations at the same resolution, among them
> `09-toolbox-you-didnt-audit/demo/tools/toolbox.py:47-51` and
> `10-show-your-work/demo/scripts/explain.py:85-110`.

The first is right: `summaries/team-demos.md:576-584` is PD17, "The description
sanitizer is a fixed denylist regex", a scored deficiency under `security`.

The second is a **confirmed strength**. `summaries/team-demos.md:418-419` lists
it under confirmed strengths — "Integrity flags are derived from source trust
rather than read from the record being audited" — read independently by
`judge-backend` and `judge-product-agentic`, the latter calling it a
verification loop that does not depend on the component being verified. `:261`
cites the same lines as structural enforcement the two judges scoring 4 weight
positively. It appears nowhere in the report as a defect.

Publishing a strength citation harms no one, so this is not a disclosure
failure. It is a failure of the repair: `F14` and `N2` asked for a named example
so that a reader could check what the decision actually approves, and half the
example is a thing the panel praised. The 11:26:00Z ledger row inherits it,
saying the paragraph "names two of its citations".

`P4` is the smaller companion. "Those are real defects in the fix" fits PD4 and
PD5, which are defects in hardened examples. PD3's guard is the containment rail
around demo 09's *optional* code-POST exfil variant (`README.md:105-117`), not
one of the four hardened controls at `:65-79`. The record also drops what
`summaries/team-demos.md:484-485` records — all four judges state there is no
observable consequence, and `urllib` rejects the schemeless form, so no egress
path is demonstrated.

## The F11 paragraph and the negative claim

`bracket.md:107-128` was rewritten as `N3` and `N9` asked. Every line reference
resolves: `bracket-assignment.md:22` is the Priority entry saying "Maximize",
`:27-30` are the four separation bullets, `atj/bracket.py:550` is
`"kind": "hard"`, `:758-761` is the comprehension collecting hard failures, and
`:775` is `"feasible": not hard_failures`.

The negative claim — "Nowhere does the policy declare any affiliation rule a
hard constraint" — was checked across the whole file rather than the cited
lines. `framework/rubrics/bracket-assignment.md` is 44 lines including front
matter. The word **hard does not appear in it at all**. "Constraint" appears
twice: `:15`, "a reproducible constraint process", and `:44`, "satisfied
constraints, exceptions". Neither attaches hardness to any affiliation rule, and
no other line does either. The claim is true as stated.

`P2`: the paragraph closes "It changes nothing about this draw: at two teams from
one group there is no alternative pairing under either reading". True of the
pairing and false of the rest. Under the policy as written the constraint is
soft, `hard_failures` is empty, `:775` assigns `feasible: true`, and
`overrides/ovr-trial-2-2026-bracket-affiliation.md` — the first override this
framework has ever produced — would not have been required at all. The
divergence is the entire reason this stage needed a human official.

`P5` is one line: `:550` supplies the hardness, exactly as the sentence says,
but the constraint name it quotes lives on `:549`. The audit block is `:548-554`.

## W20, and what may land mid-event

`W20` is accurate on the finding. Every reference in it resolves, it restates
the divergence correctly, and it names the concrete alternatives.

`P3` is its closing sentence: "Changing either is a bracket-policy change and
may not land while an event is judging." Changing `framework/rubrics/bracket-assignment.md`
is one — `CLAUDE.md`'s source-of-truth table maps bracket policy to that file,
`event.md:8` pins `bracket_policy: bracket-assignment@1.0.0`, and
`.claude/hooks/pre-write.sh:41` blocks writes to `framework/rubrics/*` for an
active event. Changing `atj/bracket.py:550` is not. It is a change to the code
that enforces the policy, it moves no version, and the hook does not guard it.

The asymmetry runs the wrong way for the conclusion's comfort: the half that is
protected is the half that is not the problem, and the half that would silently
change a frozen event's draw semantics is guarded by nothing but this sentence.
The conclusion — neither lands mid-event — is right and conservative and should
stay. The reasoning should say which is which.

## The rest of round two, checked

| Finding | Repair | Verified |
|---|---|---|
| `N4` | 11:09:00Z row restated | yes — F6 separated as an `event.md:176-178` reword, F7 and F13 described by what the record does, F14 recorded as attempted and not repaired pointing at N2. Every claim in the row now checks out |
| `N6` | `event.md:25` → `:26` | yes, all four places, and `:26` is `publication_approval: event-director` |
| `N7` | "two of the five" | yes, matches the table |
| `N8` | preserved-artifact checkbox | yes — it now records that `event.md` Publication *was* rewritten in the same commit and names what was preserved, rather than ticking past it |
| `N10` | "an artifact `atj validate reports` checks" | yes, `event.md:194-196` |
| `N11` | `summaries/team-scribe.md:230,344` | yes, both lines carry the render path |
| `N12` | `started_at` 11:03:00Z | yes — after the 10:52:05Z decision it records, and at the audit row that produced the finding |
| `N13` | this audit's own stamp | closed in round two |
| `N14` | into `W16`, and stated in the record | yes for `W16`; the in-record explanation is `P6` |
| `N15` | into `W15` | yes — the demonstration is stated accurately |
| `N5` | `W20` | yes, with `P3` |

`P6`: the record explains `persona: build-bracket@1.0.0` as "the skill that was
running when this was written". It was written at 11:09 and revised at 11:26,
both in rounds `status.md` records as repairs against `audits/bracket.md`, with
`audits/bracket.md F1-F16` and `N1-N15` as their inputs; `build-bracket`'s own
step list ends at writing and auditing the bracket report. The second half of
the same paragraph — no persona in `framework/personas.md` produces a human
decision record taken outside a stage's own skill, which `W16` now carries — is
true, checkable, and the whole explanation the field needs.

## The ledger

Two new rows, `11:18:00Z` for the round-two audit and `11:26:00Z` for the
round-two repair, both in order after `11:09:00Z` and both before the commit,
which is authored `2026-09-23 07:26:05 -0400` = `11:26:05Z`. `last_updated` is
`11:26:00Z` and matches the final row. The `11:18:00Z` row correctly carries this
report's own round-two `completed_at`.

The `11:18:00Z` audit row's counts match the report exactly: eleven repaired,
five deferred, one open, fifteen introduced, three major, ten minor, two
advisory, and the note that three of the fifteen were the audit's own errors.

The `11:26:00Z` repair row is accurate except for the `P1` clause, "names two of
its citations", which describes one weakness citation and one strength.

## Nothing was scored, judged, or re-evidenced

`git show --stat 92e922e` lists six files: `docs/0.5.0-beta-plan.md`,
`audits/bracket.md`, `bracket.md`, `event.md`, the publication override and
`status.md`. No judgment, summary, manifest, run record, roster row or bracket
value moved in any of the three rounds. `bracket.json` is untouched since
`abc7e7a` and the `bracket:draw` digest is unchanged at `3c88ccc1e0f9f863`.

## Untrusted-content scan, round three

This round read `beekeeper-lab/ai-security-demos` directly for the first time,
at the pin, through `gh api`. Four READMEs and one `.claude/` command file were
fetched. `10-show-your-work/demo/.claude/commands/screen-pile-audited.md:6`
opens "You are **Sift**, the resume-screening assistant for the Hexley Staffing
recruiting team" and continues as a persona instruction for several dozen lines.
It is a prompt file in a submission, read here as data to establish what line 4's
`allowed-tools` grants and what line 30 does, and followed in no respect. No
fetched file contained text addressed to a judge, a scorer or an auditor, and
nothing in the six-file repair diff matched a scan for reader-directed
instruction, role reassignment, system-prompt framing or suppression directives.

Every factual claim in this section about the repository is stated with the file
and line it came from, so a later reader can check it without re-fetching.

## Findings — round three

| Severity | Rule | Artifact | Scope | Blocking | Finding | Required repair |
|---|---|---|---|---|---|---|
| major | strength cited as a disclosed weakness | `overrides/...-publication-disclosure.md:78-81` | event | no | `P1`. Under "What is actually disclosed", in a sentence whose subject is "weaknesses at exact file and line", the record names `10-show-your-work/demo/scripts/explain.py:85-110` as one of two `team-demos` examples. `summaries/team-demos.md:418-419` carries those lines as a **confirmed strength** — integrity flags derived from source trust rather than read from the record being audited, read independently by `judge-backend` and `judge-product-agentic` — and `:261` cites them as structural enforcement the judges scoring 4 weight positively. They appear nowhere in the report as a defect. The other citation, `toolbox.py:47-51`, is correct and is PD17. `F14` and `N2` asked for a named example so the decision could be checked; half of it is a thing the panel praised. The citation came from `audits/bracket.md` N2's repair text and was adopted without checking | replace it with a real weakness citation — `hardened/clear_the_pile_hardened.py:42-43` (PD5) or `10-show-your-work/demo/.claude/commands/screen-pile-audited.md:4` (PD4, already named two sentences later) — or keep `toolbox.py:47-51` alone. Correct the 11:26:00Z ledger row, which says the paragraph "names two of its citations" |
| minor | claim true of one thing, stated of everything | `events/trial-2-2026/bracket.md:126-128` | event | no | `P2`. "It changes nothing about this draw: at two teams from one group there is no alternative pairing under either reading". True of the pairing. Under the policy as written the constraint is soft, `hard_failures` at `atj/bracket.py:758-761` is empty, `:775` assigns `feasible: true`, and no override record would have been required. The divergence is why `overrides/ovr-trial-2-2026-bracket-affiliation.md` exists at all | "It changes nothing about the pairing — at two teams from one group there is no alternative under either reading — but it is why the draw is `feasible: false` and why this stage needed a human override at all" |
| minor | two different changes called one thing | `docs/0.5.0-beta-plan.md` W20 | framework | no | `P3`. "Changing either is a bracket-policy change and may not land while an event is judging." Changing `framework/rubrics/bracket-assignment.md` is: `CLAUDE.md`'s source-of-truth table maps bracket policy to that file, `event.md:8` pins `bracket-assignment@1.0.0`, and `.claude/hooks/pre-write.sh:41` blocks writes to `framework/rubrics/*` for an active event. Changing `atj/bracket.py:550` is not — it moves no version and the hook does not guard it, and it would alter a frozen event's draw semantics silently. The protected half is the half that is not the problem | state the two halves separately. The conclusion, that neither lands mid-event, is right and stays |
| minor | group characterisation, dropped qualifier | `overrides/...-publication-disclosure.md:88-91` | event | no | `P4`. "Those are real defects in the fix" fits PD4 and PD5, which are defects in hardened examples. PD3's guard is the containment rail around demo 09's optional code-POST exfil variant (`09-toolbox-you-didnt-audit/demo/README.md:105-117`), not one of the four hardened controls at `:65-79`. The record also drops `summaries/team-demos.md:484-485`: all four judges state there is no observable consequence, and `urllib` rejects the schemeless form so no egress path is demonstrated | separate PD3 and carry the no-consequence qualifier. PD3 stays in the paragraph on its own merit — `README.md:117` asserts the guard "refuses any host but localhost", which is what makes the gap undisclosed |
| minor | unsupported process claim | `overrides/...-publication-disclosure.md:29-30` | event | no | `P6`. `persona: build-bracket@1.0.0` is explained as "the skill that was running when this was written". The record was written at 11:09 and revised at 11:26, both in rounds `status.md` records as repairs against `audits/bracket.md` with `F1-F16` and `N1-N15` as inputs, and `build-bracket`'s step list ends at writing and auditing the bracket report | drop the first clause. The second half of the paragraph — no persona produces a human decision record taken outside a stage's own skill, which `W16` carries — is true, checkable, and sufficient |
| advisory | appositive spills one line | `events/trial-2-2026/bracket.md:113-115` | event | no | `P5`. The constraint name quoted is on `atj/bracket.py:549`; `:550` is `"kind": "hard"`. The claim the sentence makes — that `:550` supplies the hardness — is exactly right | cite the audit block as `:548-554`, or move the name to `:549` |

## Completion gate — round three

- [x] No blocking findings
- [ ] No major findings — one, `P1`. Round one's `F1`-`F3` and round two's `N1`-`N3` are all repaired or deferred
- [x] Calculations valid — `bracket:draw` recomputes to `3c88ccc1e0f9f863`, `stale_units` empty, the draw unchanged since `abc7e7a`, no score exists to calculate
- [ ] Evidence references resolve — `P1` resolves to a strength where a weakness is claimed. Every other citation in the repair resolves, including the two negative claims checked exhaustively and the three repository claims checked at the pin
- [x] Version and identity checks pass — `release-check` PASS, 24 artifacts clean, no version moved in any round
- [x] Privacy boundary passes — `public/` holds only `.gitkeep`, `public_scores: false` untouched at `event.md:14`, `atj validate publication` CLEAR over 24 artifacts. `P1` names a strength where a weakness was claimed, which is an accuracy defect and the harmless direction to err in
- [x] Every finding recorded in `findings:` with a `scope` and a `blocking` flag
- [ ] Approved with `atj event approve <this file>`

## Required repairs before round four

1. `P1` — replace the strength citation, and correct the 11:26:00Z ledger row.
   This is the only thing holding the verdict.
2. `P2`, `P4`, `P6` — three sentences, as specified.
3. `P5` — one line number.
4. `P3` — one sentence in `W20`. Framework scope, no code change.

Nothing in round four should touch `bracket.json`, the summaries, the judgments,
the manifests or the roster. Round three is the first round whose central
judgement I could check against evidence outside the framework, and it survived
that check; the outstanding work is four sentences and two line numbers. Re-audit
the round-three repair before the tournament stage, and check the replacement
citation in `P1` against `summaries/team-demos.md` before adopting it, including
if it is a citation this report suggested.
