---
event_id: trial-2-2026
audit_scope: initial-judging stage
audit_id: judgments
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.1.0
persona: judging-auditor@1.1.0
framework_commit: 7957530ec746ea3b707f09eaef50c78b20ecfe75
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-22T12:24:00Z"
completed_at: "2026-09-22T14:17:00Z"
visibility: private
approval_state: approved
validation_state: valid
result: PASS WITH ADVISORIES
audit_rounds: 3
findings:
- id: F1
  severity: blocking
  scope: event
  blocking: false
  summary: 'Round 1. Two team-demos judgments recorded as a directly verified confirmed defect that `.env.example` does not exist anywhere in the pinned tree. Ten are tracked, one per demo folder, and both judgments named the non-existent defect as a reason `product` was held below the top anchor. Round 2: both judges re-checked the git index, withdrew the claim in place, and neither score moved.'
  artifact: judgments/team-demos/judge-frontend-ux.md; judgments/team-demos/judge-security-ops.md
  repair: Done and verified. Withdrawals recorded rather than deleted, no surviving assertion of absence, front matter and both `atj:scores` blocks untouched, defect numbering preserved so D2-D6 and K1 still resolve.
  state: repaired
- id: F2
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1. "fifty-four beans are marked Done" three times; the index holds 54 `BEAN-` rows of which 52 are `Done` and two `Approved`. Round 2: corrected at all three sites.'
  artifact: judgments/team-scribe/judge-product-agentic.md:54,116,182
  repair: Done. Re-derived against the index at the pin.
  state: repaired
- id: F3
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1. The `rm` pre-approval was cited to `rank-resumes.md:4`, which grants no `rm`. Round 2: re-cited to the seventeen files that carry `Bash(rm:*)` and sharpened onto the capstone screener.'
  artifact: judgments/team-demos/judge-frontend-ux.md:112,154
  repair: Done. Seventeen re-counted; sixteen teardown and staging bodies each name a fixed argument list.
  state: repaired
- id: F4
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1. The quoted `OPENAI_API_KEY=your-key-here` came from `install.py`''s unreachable `else` arm. Round 2: re-attributed to the reachable copy branch at `install.py:124-127`.'
  artifact: judgments/team-scribe/judge-security-ops.md:51,153,193
  repair: Done. S1 and B3 stand as written.
  state: repaired
- id: F5
  severity: major
  scope: event
  blocking: false
  summary: 'Round 1. The ledger recorded none of this stage. Round 2: six rows added, both "Four judgments" cells filled, `last_updated` moved forward.'
  artifact: status.md
  repair: Done. Every added row matches a commit on this branch; see F20 for one round-two stamp that does not match its artifact.
  state: repaired
- id: F6
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1. The two unresolved-NE adjudication triggers were unrecorded. Round 2: ADJ-1 and ADJ-2 entered, owned by event-director, deferred to consolidation by decision.'
  artifact: status.md:47-52
  repair: Done.
  state: repaired
- id: F7
  severity: minor
  scope: framework
  blocking: false
  summary: Agreement is computed from the range over numeric scores alone, so two criteria print `aligned` while half the panel holds them unscorable. Recorded as W10.
  artifact: docs/0.5.0-beta-plan.md:236; framework/rubrics/panel-consolidation.md:31-34; atj/scoring.py
  repair: Carried. `CLAUDE.md` forbids changing an active event's rubrics after judging begins.
  state: deferred
- id: F8
  severity: advisory
  scope: framework
  blocking: false
  summary: Report validation does not check that an artifact ends where its template ends. W9, demonstrated again by the round-one repair and closed in this event by F13.
  artifact: docs/0.5.0-beta-plan.md:236; atj/reports.py
  repair: Carried for 0.5.0-beta, now alongside W12.
  state: deferred
- id: F9
  severity: advisory
  scope: event
  blocking: false
  summary: The suite time is given as 5.98s, which is the container's `duration_seconds`; pytest's own line reads 4.71s. Inherited from the approved manifest.
  artifact: judgments/team-scribe/judge-product-agentic.md:180; judgments/team-scribe/judge-security-ops.md:183; evidence/team-scribe/manifest.md:120
  repair: 'None required. Accepted: reopening an approved manifest mid-stage costs more than the number is worth, and the provenance is on the record.'
  state: accepted
- id: F10
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1. The demo enumeration included 06, whose primary command has no `Write`, and omitted 04, 05 and 08. Round 2: corrected and re-derived against all 40 command files.'
  artifact: judgments/team-demos/judge-backend.md:156
  repair: Done.
  state: repaired
- id: F11
  severity: advisory
  scope: event
  blocking: false
  summary: 'Round 1. The stale `status.md.bak` was present again. Round 2: deleted; the event directory is clean including ignored paths, and still is.'
  artifact: events/trial-2-2026/status.md.bak
  repair: Done.
  state: repaired
- id: F12
  severity: advisory
  scope: event
  blocking: false
  summary: Many material findings rest on static reads of the pinned checkout with no manifest evidence id. In scope under `event.md:158` and all verified, but untraceable through either evidence index.
  artifact: judgments/team-scribe/judge-backend.md:113; judgments/team-scribe/judge-security-ops.md:153; judgments/team-demos/judge-product-agentic.md:269-271; judgments/team-demos/judge-security-ops.md:198
  repair: None required. Carried to consolidation as a note about provenance.
  state: accepted
- id: F13
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 2. The round-one repair put prose after the declaration in one file, which is the W9 defect the previous stage removed, and a fifth checkbox in the other. Round 3: both amendment records are declaration checkboxes and all eight judgments end at their declaration.'
  artifact: judgments/team-demos/judge-frontend-ux.md:208; judgments/team-demos/judge-security-ops.md:218,219
  repair: 'Done. The `## Amendments` section is correctly not added mid-event: `atj/reports.py:81-87,165-171` makes every `##` heading in a template a required section, so it would fail all eight judgments here and every judgment in both completed events. Recorded as W12. See F21 for the residue.'
  state: repaired
- id: F14
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 2. "The two defects above are real" survived after one of the two was withdrawn. Round 3: restated in the singular.'
  artifact: judgments/team-demos/judge-frontend-ux.md:86
  repair: Done. The `NE` rests on `ev-demos-01` and did not move.
  state: repaired
- id: F15
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 2. The file gave "seven commands" in one place and enumerated eight in another; seventeen carry `Bash(rm:*)`. Round 3: D2 enumerates all seventeen and the Surprises paragraph is corrected.'
  artifact: judgments/team-demos/judge-security-ops.md:185,194
  repair: Done. The enumeration matches the tree exactly, with no false entry and no omission, and the judge argues the correction widens D2 rather than softening it.
  state: repaired
- id: F16
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 2. The claim that root `README.md:16,23` sends the reader into the demo folder "before the copy at `:19`" reversed the file''s line order. Round 3: the judge withdrew the ordering claim and re-rested the citation on `README.md:23` and `01/demo/README.md:15`.'
  artifact: judgments/team-demos/judge-security-ops.md:79; judgments/team-demos/judge-frontend-ux.md:98
  repair: Done at the `functional` deficiency. Not done at the D1 withdrawal in the same file, which is F22.
  state: repaired
- id: F17
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 2. Three judgments corrected by the event director carried no in-artifact amendment record. Round 3: each carries a checkbox naming the finding, what changed, and that no score, confidence, anchor or line of reasoning was touched.'
  artifact: judgments/team-scribe/judge-product-agentic.md:214; judgments/team-scribe/judge-security-ops.md:224; judgments/team-demos/judge-backend.md:209
  repair: Done. The authorship itself was accepted in round two and is not revisited.
  state: repaired
- id: F18
  severity: advisory
  scope: event
  blocking: false
  summary: The repaired S1 quotes the placeholder `src/config/settings.py:304` rejects, so the copied file is not a live key source until the user edits it, which S1 does say. Optional by the round-two text.
  artifact: judgments/team-scribe/judge-security-ops.md:51,153
  repair: 'None made, and that is the right call: naming the guard would strengthen the finding, and the event director should not edit a judge''s reasoning on an optional point.'
  state: accepted
- id: F19
  severity: advisory
  scope: event
  blocking: false
  summary: Both `product` rationales were rewritten to hold score 4 after losing a stated reason. Neither judge raised its score and both replacement reasons check out.
  artifact: judgments/team-demos/judge-frontend-ux.md:100; judgments/team-demos/judge-security-ops.md:95
  repair: None required. Carried to consolidation.
  state: accepted
- id: F20
  severity: minor
  scope: event
  blocking: false
  summary: The ledger row for the round-two audit is stamped 13:52:00Z while the artifact it records carries `completed_at` of 14:05:00Z at `7957530`. The round-one row matched its artifact exactly. A ledger stamp that does not come from the thing it records is the class the configuration stage found once and the evidence stage found five times.
  artifact: status.md:84
  repair: Set the row to 2026-09-22T14:05:00Z, which is recoverable from `git show 7957530:events/trial-2-2026/audits/judgments.md`, or to this round's `completed_at` if the row is meant to cover the audit as a whole.
  state: open
- id: F21
  severity: advisory
  scope: event
  blocking: false
  summary: Residue of the F13 disposition, which I accept. The amendment records are checkboxes inside `## Calculation and independence declaration`, which is the judge's own attestation block, and three of the five record the event director's action rather than the judge's. Each box names who acted, and all eight judgments still carry the four canonical items unaltered.
  artifact: judgments/team-demos/judge-backend.md:209; judgments/team-scribe/judge-product-agentic.md:214; judgments/team-scribe/judge-security-ops.md:224
  repair: None this stage. W12's `## Amendments` section, placed before the declaration, resolves it when the template change lands.
  state: open
- id: F22
  severity: minor
  scope: event
  blocking: false
  summary: Half-repair of F16. The ordering correction landed at `:79` and not at `:193`, where the D1 withdrawal still says the ten files sit in "the folder every README runs `cp .env.example .env` from". The same file's round-three correction establishes that the root README's copy at `:19` names no folder, so "every README" is the over-generalisation the correction identified, surviving in the paragraph the correction is about. The round-two amendment checkbox at `:218` carries the same phrasing.
  artifact: judgments/team-demos/judge-security-ops.md:193,218
  repair: Scope both to the ten demo READMEs, as the corrected paragraph at `:79` and the sibling judgment already do. No score or citation to the tree is affected.
  state: open
approved_by: event-director
approved_at: "2026-09-22T14:19:58Z"
approval_note: 'Round three, scoped to the round-two repair: PASS WITH ADVISORIES, 22 findings over three rounds, none blocking or major, F20 and F22 repaired in this commit.'
---

# Judging Audit

## Result

**PASS WITH ADVISORIES.** Round three, scoped to the round-two repair.

All seven findings put to this round are closed: five repaired and verified
against the primary sources, two accepted as advisory with no repair and for
stated reasons I agree with. F13 is the one that mattered, and the disposition is
right — I checked the constraint rather than taking it, and adding an
`## Amendments` heading to the judgment template mid-event would indeed fail
validation on all eight judgments here and on every judgment in both completed
events. All eight judgments now end where their declaration ends.

Three findings this round. Two minor, one advisory, none blocking and none major.
Two of the three were introduced by the round-two repair, which makes three
consecutive repair rounds that introduced defects, at a falling rate: four in
round one, three in round two counting my own missed F15, two now.

**The `judgments-audited` gate may be set on this report and the event may
advance to consolidation.** F20 and F22 are single-sentence corrections that
touch no score, no citation to a checkout and no evidence reference; they can be
made in the gate commit or carried. Nothing in this stage requires a fourth
repair round.

## Scope and artifacts inspected

Initial-judging stage of `trial-2-2026` at `7957530` on branch
`event/trial-2-2026-judging`. Round one at `2b91208` was unscoped and read all
eight judgments end to end. Round two was scoped to `2b91208..91ce6a6`. This
round is scoped to `git diff 91ce6a6..7957530`, which is eight files: five
judgments, `status.md`, `docs/0.5.0-beta-plan.md` and this report.

Re-derived this round, from the primary sources and not from the repair's account
of them: `atj/reports.py:58,81-87,165-171`, to test W12's premise before
accepting the disposition; every `Bash(rm:*)` grant in the ten demos, compared
file by file and line by line against D2's new enumeration; the per-demo
distribution and demo 10's three; `05/demo/.claude/commands/reset-demo.md:3,7`
and the `scripts/reset_demo.py` it delegates to; the location of all 53 tracked
`.py` files; the terminal section of all eight judgments; the `completed_at` of
the round-two audit as committed; and every timestamp in `status.md` against the
commit that carries it.

Nothing was executed from either checkout. Every fact came from `git ls-files`,
`git show`, `git grep`, `sed -n` or a read of the committed run records.

## Deterministic validation results

| Check | Result |
|---|---|
| `atj event validate events/trial-2-2026` | PASS, 0 problems, stage initial-judging |
| `atj validate reports events/trial-2-2026` | PASS, 16 artifacts, 0 blocking, 0 major, 0 minor, 0 advisory |
| `atj validate publication events/trial-2-2026` | CLEAR, 16 artifacts, 0 blocking |
| `atj release-check` | PASS, every check |
| `atj score events/trial-2-2026/judgments/team-scribe` | unchanged; `agentic` blocked by unresolved NE, provisional 32.50 |
| `atj score events/trial-2-2026/judgments/team-demos` | unchanged; `functional` blocked by unresolved NE, provisional 52.50 |
| `git status --porcelain --ignored events/trial-2-2026/` | empty |

Both score tables are byte-identical across all three rounds, every judge score
included, and the front-matter diff across `91ce6a6..7957530` filtered for every
front-matter key is empty. Three repair rounds have now edited seven of the eight
judgment files and moved no number.

## F13, and whether I accept the disposition

**I accept it, and I checked the premise rather than the claim.**

`atj/reports.py:81-87` reads the required sections of an artifact straight out of
its template — `template_sections` returns every `##` heading `_HEADING` finds at
`:58` — and `:165-171` raises a `major` finding for each one missing from the
body. Adding `## Amendments` to `framework/templates/individual-judgment.md`
would therefore make it mandatory in every judgment: the eight in this event, and
every judgment in `live-trial-2026` and the sample event, all of which are frozen
and none of which has it. The repair's reasoning is exactly right and the
alternative it declined would have been a worse version of the offence the audit
chain exists to prevent.

What my round-two text asked for was that the declaration be the last thing in a
judgment. It now is, in all eight. Every file ends on a `- [x]` line, no prose
follows any declaration, and all eight still carry the four canonical declaration
items unaltered — three carry only those four, four carry a fifth, and
`team-demos/judge-security-ops.md` carries a sixth for its second amendment.
W12 is recorded with the section placed before the declaration when it lands,
which is the right place for the same reason.

The residue is F21 and it is advisory. A declaration is the judge's own
attestation block, and three of the five amendment boxes record the event
director's action inside it. Each box says so in its own text — "Corrected by the
event director after a stage audit, 2026-09-22, under audit finding F10 and with
no judge re-run" — so nothing is misattributed, and the two judge-authored ones
say "by this judge" and "after a second stage audit". It is a compromise forced
by a missing affordance, it is legible, and W12 closes it.

## The other five, re-derived

**F14.** `judge-frontend-ux.md:86` now reads "The defect above is real and I
report it". One defect remains in the paragraph it refers to and the withdrawn
one is described as withdrawn. The `NE` still rests on `ev-demos-01`.

**F15.** D2's new enumeration is exact. I listed every `Bash(rm:*)` grant in the
ten demos independently and compared: seventeen in the tree, seventeen in the
entry, no false entry and no omission. The distribution the entry claims holds —
at least one in every one of the ten demos, three in demo 10 (`reset-demo.md:3`,
`unstage-attacks.md:3`, `screen-pile-audited.md:4`). The Surprises paragraph at
`:185` now says seventeen and no "seven" survives anywhere in the file.

The judge's own framing of the correction is worth recording, because it is the
opposite of what a self-serving correction looks like: "The corrected count
widens this entry rather than softening it: a broad delete grant is the corpus's
default for any command that removes a file, not an oversight in a few." The
counter-example it adds is real and I checked it — `05/reset-demo.md:3` grants
`Bash(python3:*), Bash(ls:*)` and no `rm`, delegating the deletes to
`python3 scripts/reset_demo.py` at `:7`, and that script exists at the pin. A
judge that finds its own understated finding and enlarges it, with the
submission's own tree supplying the cheaper fix, is the behaviour this stage
wants.

**F16.** The ordering claim is withdrawn in the `functional` deficiency at `:79`
and the citation now rests on `01/demo/README.md:15` ("Everything runs from
**this `demo/` folder**") and on `README.md:23`'s content rather than its
position. The new supporting claim checks out exactly: all 53 tracked `.py` files
sit under `NN-*/demo/`, none at the repository root, so the root is never a
working directory for run path B. The sequencing description is also accurate —
`:19` gives the copy inside the Python bullet without naming a folder, `:16`'s
`cd` belongs to the Claude Code bullet above it, and `:23` follows. The fix did
not reach the D1 withdrawal in the same file, which is F22.

**F17.** Three amendment checkboxes added, one per director-corrected file, each
naming its finding number, what changed, and that no score, confidence, anchor or
line of reasoning was touched. The scribe product-agentic box also records that
`framework/personas.md` gives that judge no write tool, "so every version of this
file was written by the orchestrator", which is the point round two accepted the
authorship on and is worth having in the artifact rather than only in an audit.

**F18 and F19** were accepted with no repair. F18 was optional by my own round-two
text and the reason given for not making it is correct: the event director should
not edit a judge's reasoning on an optional point, and naming the
`settings.py:304` guard would strengthen S1 rather than weaken it, so nothing is
lost by leaving it to the judge or to nobody. F19 is a note for the consolidator
and needs no edit.

## New findings this round

**F20** is a ledger stamp that does not come from the artifact it records. The
round-two audit row reads `2026-09-22T13:52:00Z`; the report it names carries
`completed_at: "2026-09-22T14:05:00Z"` at `7957530`. The round-one row matched
its artifact to the second. This is the fifth stage in a row to produce a
timestamp finding and the sixth instance of the class on this event, and it is
the cheapest kind to fix — the correct value is in git.

Everything else in the ledger checks out. Both round-two rows are present and
accurate in substance, including the honest count "Four of the seven were
introduced by the round-one repair". `last_updated` is `14:13:00Z`, before the
`14:13:07Z` commit. The log is in ascending order across all thirty-two rows.

**F22** is a half-repair, the shape the evidence stage produced four times. F16
was named in one place and fixed in one place; the D1 withdrawal at `:193` still
says the ten files sit in "the folder every README runs `cp .env.example .env`
from", and the round-two amendment checkbox at `:218` repeats it. The same file's
round-three correction is what establishes that this is wrong: the root README
gives the copy without naming a folder. Nothing about the tree is misstated —
ten files exist and each demo README does run the copy from its own folder — so
this is an internal inconsistency rather than a false citation, and the sibling
judgment scopes the same sentence correctly to "each demo README".

**F21** is the accepted residue of F13, above.

## What the earlier rounds established, for the gate and for consolidation

**Arithmetic.** No judgment contains a weight, a weighted point value or a total.
All eight carry the `atj:scores` marker pair with an empty table between them,
re-checked after every repair round. Every criterion score lives once, in front
matter. No provisional total appears in any committed artifact, and `atj score`
printed the same two tables at `2b91208`, `91ce6a6` and `7957530`.

**NE handling is correct throughout.** Four `NE`s, all inside their manifest's
`evidence_limited_criteria`, all `confidence: high` as
`submission-evaluation.md:88-93` requires of a criterion the package itself
records as evidence-limited. Every refusal to record `NE` is argued from the
manifest sentence or rubric clause that permits it. The two-two splits on
`team-scribe/agentic` and `team-demos/functional` are the `NE`-versus-low-score
boundary `event.md:56-57` set out to test, answered on the record by four judges
with their reasoning written out. F7 is the risk that the answer disappears into
an `aligned` label at consolidation, and W10 carries it.

**Independence holds.** Four judgments per team, identical `started_at` per team,
all eight declaring no other report was inspected, and every amendment record
restating it. Round one's n-gram analysis found no finding-level overlap the
manifests and the framework do not explain. F1 strengthened this rather than
weakening it: two judges produced the same wrong answer by different methods with
no shared wording, which is what a shared tool blind spot looks like.

**H6 is killed.** No judgment repeated, obeyed or was steered by an instruction
found inside a submission. The known payload's directive appears nowhere and no
score in any judgment is 5. All eight state that the agent-instruction surface
was read as data and several turn it into evidence against the submission. Three
repair rounds did not disturb this; every amendment record concerns the judges'
own tooling.

**Publication boundary holds.** `public_scores: false`, `public/` holds only
`.gitkeep`, `atj validate publication` CLEAR over 16 artifacts, no provisional
total in any committed artifact, no credential or personal data in any judgment.

**Versions and identity.** No skew. All eight pin `submission-evaluation@1.1.0`
and their persona at `1.1.0`, matching `framework/personas.md:35-38`, with
commit, evidence package id, run id and model block consistent. No front-matter
field changed in any judgment across three repair rounds.

**Citations.** Round one followed roughly 120 to the artifact and found four that
did not say what the judgment claimed. All four are repaired and re-derived. Every
correction made in rounds two and three has been checked against the pinned
checkout, the git index or `atj/` source rather than against the repair's
description of it.

## Findings

| Severity | Artifact | Scope | Blocking | Finding | State |
|---|---|---|---|---|---|
| blocking | `judgments/team-demos/judge-{frontend-ux,security-ops}.md` | event | no | F1 — `.env.example` recorded as absent; ten are tracked. Withdrawn by both judges, recorded not deleted, no score moved | repaired |
| major | `status.md` | event | no | F5 — the ledger recorded none of this stage. Six rows added and verified against the commit history | repaired |
| minor | `judgments/team-scribe/judge-product-agentic.md` | event | no | F2 — bean count, corrected to 52 of 54 | repaired |
| minor | `judgments/team-demos/judge-frontend-ux.md` | event | no | F3 — `rm` pre-approval re-cited to seventeen files and sharpened onto the capstone screener | repaired |
| minor | `judgments/team-scribe/judge-security-ops.md` | event | no | F4 — installer branch re-attributed to `install.py:124-127` | repaired |
| minor | `status.md:47-52` | event | no | F6 — ADJ-1 and ADJ-2 recorded, deferred to consolidation | repaired |
| minor | `docs/0.5.0-beta-plan.md:236` | framework | no | F7 — an NE split prints as `aligned`. W10 | deferred |
| advisory | `docs/0.5.0-beta-plan.md:236` | framework | no | F8 — validation does not check that an artifact ends where its template ends. W9 | deferred |
| advisory | `judgments/team-scribe/judge-{product-agentic,security-ops}.md` | event | no | F9 — 5.98s is container wall-clock, 4.71s is the suite. Inherited from an approved manifest | accepted |
| minor | `judgments/team-demos/judge-backend.md:156` | event | no | F10 — demo enumeration corrected and re-derived | repaired |
| advisory | `events/trial-2-2026/status.md.bak` | event | no | F11 — stale backup deleted | repaired |
| advisory | four judgments | event | no | F12 — findings with no manifest evidence id; in scope, verified, untraceable through the evidence index | accepted |
| minor | `judgments/team-demos/judge-{frontend-ux,security-ops}.md` | event | no | F13 — the round-one repair put content past the declaration. Both records are now declaration checkboxes; all eight judgments end at their declaration; W12 records why no `## Amendments` section landed | repaired |
| minor | `judgments/team-demos/judge-frontend-ux.md:86` | event | no | F14 — plural antecedent after a withdrawal, restated in the singular | repaired |
| minor | `judgments/team-demos/judge-security-ops.md:185,194` | event | no | F15 — seven against eight against seventeen. D2 now enumerates all seventeen, matching the tree exactly | repaired |
| minor | `judgments/team-demos/judge-security-ops.md:79` | event | no | F16 — the README ordering claim withdrawn and the citation re-rested; see F22 for the half it missed | repaired |
| minor | three judgments | event | no | F17 — amendment records added to the three director-corrected files | repaired |
| advisory | `judgments/team-scribe/judge-security-ops.md:51,153` | event | no | F18 — `settings.py:304` filters the quoted placeholder, unstated. Optional, correctly not edited by the director | accepted |
| advisory | `judgments/team-demos/judge-{frontend-ux,security-ops}.md` | event | no | F19 — both `product` rationales rewritten to hold an unchanged score after losing a stated reason. Both replacements check out | accepted |
| minor | `status.md:84` | event | no | F20 — the round-two audit's ledger stamp is 13:52:00Z; the artifact carries 14:05:00Z | open |
| advisory | three judgments | event | no | F21 — amendment records are checkboxes inside the judge's own attestation block, three of them recording the director's action. Accepted residue of F13; W12 closes it | open |
| minor | `judgments/team-demos/judge-security-ops.md:193,218` | event | no | F22 — F16 fixed at `:79` and not at `:193`, where "every README" survives the correction that contradicts it | open |

## Advisories

**The gate may be set and the event may advance.** Twenty-two findings over three
rounds: thirteen repaired, four accepted, two deferred in framework scope, three
open and none of the three blocking or major. F20 and F22 are one-sentence edits
with no reasoning attached, unlike every earlier repair on this stage, which
rewrote paragraphs and introduced defects doing it. Making them in the gate
commit is proportionate; so is carrying them. Neither justifies a fourth repair
round on artifacts this settled.

**The repair-round defect rate fell but did not reach zero.** Four defects
introduced in round one, three in round two, two in round three. Across four
stages of this event no repair round has been clean, and the two constants are
half-repairs — a finding named in two places and fixed in one, which is F22 here
and was F10, F13, F22 and F28 at the evidence stage — and ledger timestamps,
which is F20 here and F21, F22, F29, F30 and F31 before it. Both are mechanical
and both are cheap to catch with a grep before committing.

**Carry F12, F19 and F21 into consolidation deliberately.** The consolidator will
see four `product` scores of 4 for team-demos without seeing that two rationales
were rewritten after a withdrawn premise (F19); will see findings it cannot trace
through either evidence index (F12); and will read five judgments whose
declaration blocks carry amendment records in a form the template does not define
(F21). All three are recorded here and none is visible in the judgments' front
matter.

**W10 is the one to act on first.** `atj score` will hand the consolidator
`aligned` for `team-scribe/agentic` and `team-demos/functional`, on which the
panel split two-two about whether the criterion can be scored at all. That is the
single place where this stage's most interesting result can be lost between here
and the consolidated report.

## Completion gate

- [x] No blocking findings — F1 repaired in round two and re-verified
- [x] No major findings — F5 repaired in round two and re-verified
- [x] Calculations valid — both `atj score` tables byte-identical across all three rounds; no weight or total in any judgment; no front-matter field changed by any repair
- [x] Evidence references resolve — every corrected citation re-derived from the primary source; F20 and F22 are a ledger stamp and an internal inconsistency, not unresolvable references
- [x] Version and identity checks pass — `atj release-check` PASS, personas and rubric consistent across all eight
- [x] Privacy boundary passes — `public_scores: false`, `public/` empty, `atj validate publication` CLEAR, event directory clean including ignored paths
- [x] Every finding recorded in `findings:` with a `scope` and a `blocking` flag
- [ ] Approved with `atj event approve <this file>`

**PASS WITH ADVISORIES.** The `judgments-audited` gate may be set on this report
and the event may advance to consolidation. F20 and F22 should be corrected, in
the gate commit or after it; neither holds the stage and neither needs a further
audit round.
