---
event_id: trial-2-2026
audit_scope: intake stage
audit_id: intake
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.1.0
persona: judging-auditor@1.1.0
framework_commit: d899befdeccdcd43b750ff1e5695943f9ae97207
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-21T23:36:59Z"
completed_at: "2026-09-21T23:46:53Z"
visibility: private
approval_state: draft
validation_state: unvalidated
result: PASS WITH ADVISORIES
audit_rounds: 2
findings:
- id: F1
  severity: major
  scope: event
  blocking: false
  summary: "Round 1 — the ScribeVault record called `beekeeper-lab/claude-kit` a private repository whose content \"cannot be fetched\" and ruled the gitlink out of the eligible scope on that premise. Round 2 repaired it: the record now states the SSH URL and the absent key as the true constraint, states that claude-kit is publicly readable over HTTPS, names the earlier claim as wrong, and rules the gitlink out of scope as an event-director decision with three reasons."
  artifact: events/trial-2-2026/submissions/team-scribe.md:139-165
  repair: "Done. Every corrected fact re-derived: anonymous `ls-remote` succeeds, the pinned commit fetches anonymously, and the record carries the event-director's approval."
  state: repaired
- id: F2
  severity: minor
  scope: event
  blocking: false
  summary: "Round 1 — both records' `completed_at` was the clone minute. Round 2 set them to 23:31:02Z and 23:31:44Z, both in the past, both after `started_at`, both consistent with the file mtimes and the approval that followed."
  artifact: events/trial-2-2026/submissions/team-scribe.md:11
  repair: Done.
  state: repaired
- id: F3
  severity: minor
  scope: event
  blocking: false
  summary: Round 1 — the hand checkbox repair was in no activity row and `last_updated` was stale. Round 2 added three rows (23:16:00Z, 23:16:37Z, 23:35:29Z), each matching what actually happened, and set `last_updated` to the newest.
  artifact: events/trial-2-2026/status.md:4
  repair: Done. Ascending, plausible, and the audit row's severity counts match this report's round one.
  state: repaired
- id: F4
  severity: minor
  scope: framework
  blocking: false
  summary: "Round 1 — a passing gate left `status.md` in the state its own validator rejects. Round 2 added `sync_status_checkboxes`, called from `save_status`, which writes the body's gate checkboxes from the ledger in both directions, with two regression tests."
  artifact: atj/event.py:515-546
  repair: Done. The rewritten `test_a_ticked_pending_gate_is_reported` still covers the only route left to the contradiction. Residual behaviour recorded as F14.
  state: repaired
- id: F5
  severity: minor
  scope: event
  blocking: false
  summary: Round 1 — the untrusted-data wrapper was carried by one example file and a four-demo list. Round 2 made the demos scope every file in the checkout and enumerated the ScribeVault agent-configuration paths. Two counts inside the new text do not re-derive; those are F11 and F12.
  artifact: events/trial-2-2026/submissions/team-demos.md:115-146
  repair: Done for the scope. The 66 `.claude/` files and the nine phrase-scan files re-derive exactly.
  state: repaired
- id: F6
  severity: advisory
  scope: event
  blocking: false
  summary: "Round 1 — both intake records were draft and unvalidated. Round 2 approved both through `atj event approve`: `approval_state: approved`, `validation_state: valid`, `approved_by: event-director`, `approved_at: 2026-09-21T23:33:46Z`."
  artifact: events/trial-2-2026/submissions/team-demos.md:16-21
  repair: Done, and it is what makes F1's scope decision an approved event-director decision rather than a model's sentence.
  state: repaired
- id: F7
  severity: advisory
  scope: framework
  blocking: false
  summary: "Not repaired, deliberately, and correctly so. `framework/templates/team-roster.md` carries eight identity fields that `check_templates` (atj/cli.py:1525-1546) requires of every template, while `events/_template/teams.md` and every roster the framework has produced carry three. Trimming the template fails the contract; adding the fields to the rosters would rewrite two frozen completed events."
  artifact: framework/templates/team-roster.md:1-12
  repair: Decide it rather than patch it. The narrow option nobody has taken is to have `atj event init` write the full front matter for new rosters and leave completed events alone. Does not hold this gate.
  state: open
- id: F8
  severity: advisory
  scope: framework
  blocking: false
  summary: Round 1 — the provenance tables printed the operator's absolute home path into a public repository. Round 2 added `_relative_checkout` with a regression test, and both trial-2 records now read `workspaces/trial-2-2026/<team>`. No absolute path remains in any event artifact.
  artifact: atj/intake.py:361-373
  repair: Done. Leaving `live-trial-2026` untouched is right; see this report's assessment.
  state: repaired
- id: F9
  severity: advisory
  scope: framework
  blocking: false
  summary: Round 1 — repository visibility was asserted without attribution or a repeatable check. Round 2 put the credential-free `git ls-remote` invocation and its result for all five repositories into the plan. Reproduced here exactly.
  artifact: docs/0.5.0-beta-plan.md:188-203
  repair: Done.
  state: repaired
- id: F10
  severity: advisory
  scope: event
  blocking: false
  summary: Round 1 — both checkouts were on an attached `main`. Round 2 detached both at their pinned commits; both report `HEAD` as the branch, both are at the pin, both are clean.
  artifact: workspaces/trial-2-2026/team-scribe
  repair: Done.
  state: repaired
- id: F11
  severity: minor
  scope: event
  blocking: false
  summary: "Introduced by the F5 repair. The ScribeVault agent-file table says `ai/beans/` holds \"168 files across 56 `BEAN-*` directories\". The tree holds 168 files, which is right, across 54 `BEAN-*` directories; 56 is the count of top-level entries, two of which are the files `_bean-template.md` and `_index.md`."
  artifact: events/trial-2-2026/submissions/team-scribe.md:126
  repair: "Write 54 directories plus two files, or write 56 entries. The table is introduced as \"counted with `find`\", so the number has to be what `find` returns."
  state: open
- id: F12
  severity: minor
  scope: event
  blocking: false
  summary: "Introduced by the F5 repair. The demos record says the same phrase scan over `*.py` \"returns ten more\". It returns 13, every one of them matching only \"Top candidate\", a label the demos' own ranking scripts print. The same paragraph gives the pinned tree as `LICENSE`, `README.md` and ten `NN-*/demo/` directories, omitting `.gitignore`."
  artifact: events/trial-2-2026/submissions/team-demos.md:138-140
  repair: Correct the count to 13 and say what it matches, and either name `.gitignore` or drop the tree enumeration, which the class rule does not need.
  state: open
- id: F13
  severity: minor
  scope: event
  blocking: false
  summary: "Introduced by the F5 repair. The inserted wrapper section separates \"Demos 03, 04 and 08 carry poisoned documents …\" from \"Every one of those payloads is **evidence about the submission**\", so the antecedent of \"those payloads\" is now a file list the same section calls \"most of them the demos' own detection and hardened variants rather than payloads\". This is the configuration audit's F12 defect returning in the other record."
  artifact: events/trial-2-2026/submissions/team-demos.md:108-151
  repair: "Move the new section below the 'Every one of those payloads' paragraph, or name the antecedent explicitly as the configuration audit's F12 repair did."
  state: open
- id: F14
  severity: advisory
  scope: framework
  blocking: false
  summary: "Residual of the F4 repair. `save_status` now rewrites the body's gate checkboxes on every ledger write, silently and with no record. A deliberate manual correction to the body is discarded by the next command that touches the ledger, and `validate_status_narrative` can only report a hand edit in the window before that write."
  artifact: atj/event.py:1118-1124
  repair: Optional — report on stderr when the sync changes a box, so an overwritten manual edit is visible rather than silent.
  state: open
- id: F15
  severity: advisory
  scope: event
  blocking: false
  summary: "The two records now treat wrapper scope differently: the demos record rules that every file is wrapped because a per-file allowlist is \"under-inclusive by construction\", and the ScribeVault record then relies on exactly such an allowlist, calling its table \"the full set\". The difference is defensible, since one submission is an attack corpus and the other is not, but no artifact states the reason, and the ScribeVault enumeration has already produced F11."
  artifact: events/trial-2-2026/submissions/team-scribe.md:128-130
  repair: State why ScribeVault's wrapper scope is an enumeration and the demos' is a class, or apply the class rule to both.
  state: open
---

# Judging Audit — intake stage

## Result

**PASS WITH ADVISORIES.** Second round, superseding the first in place. Finding
IDs are stable across both rounds.

`F1`, the major blocking finding of round one, is repaired, and repaired in the
direction the event-director chose rather than the direction that was
convenient. The ScribeVault record no longer rests anything on the claim that
`beekeeper-lab/claude-kit` is private or unreachable; it states the SSH URL and
the missing key as the real constraint, states that the repository is publicly
readable, names its own earlier claim as wrong, and rules the gitlink out of the
eligible scope as a decision with three stated reasons. The record carrying that
decision is now approved by the event-director, which is what turns it from a
model's sentence into an event decision. Nine of the ten round-one findings are
repaired; `F7` is open by choice and does not hold this gate.

Five findings are new, and three of them are the repair round's own residue —
`F11` and `F12` are counts inside the new `F5` text that do not re-derive, and
`F13` is an inserted section breaking the antecedent of the paragraph below it,
which is the configuration audit's `F12` happening again in the other record.
None of the three changes an obligation: the demos wrapper covers every file by
class, so a miscounted subset narrows nothing, and the ScribeVault file table is
otherwise exact.

Four rounds of repair in this event, four rounds that left something new behind.
The one thing that has changed is the size of what is left behind: round one of
this stage left a false premise under an eligibility ruling, and round two left
two arithmetic slips and a pronoun.

**The `roster-frozen` gate may be recorded.** Nothing open is blocking, nothing
open is major, and the three open minor findings are text corrections inside
records whose determinations re-derive.

## Scope and artifacts inspected

Intake only, second round. No evidence package, judgment, bracket or matchup
exists and none was audited.

Re-read in full: `events/trial-2-2026/event.md`, `teams.md`, `status.md`, both
intake records, `audits/configuration.md`, round one of this report, the three
templates, `schemas/roster.schema.json`, `schemas/submission-intake.schema.json`,
`schemas/audit.schema.json`, `atj/event.py`, `atj/intake.py`, `atj/cli.py`'s
template contract, `tests/test_operator_surface.py`, `tests/test_intake.py`,
`docs/0.5.0-beta-plan.md:170-205`, `CLAUDE.md`, and both pinned checkouts under
`workspaces/trial-2-2026/`, read-only, by path, from the framework root.

The repair commit is `d899bef`, on `event/trial-2-2026-intake`, touching nine
files. The full diff was read, not only the lines the findings named.

| File | Change | Checked |
|---|---|---|
| `events/trial-2-2026/submissions/team-scribe.md` | gitlink section rewritten, agent-file table added, `completed_at`, approval fields, relative checkout path | `F1`, `F2`, `F6`, `F8`, `F11`, `F15` |
| `events/trial-2-2026/submissions/team-demos.md` | wrapper-scope section added, `completed_at`, approval fields, relative checkout path | `F5`, `F2`, `F6`, `F8`, `F12`, `F13` |
| `events/trial-2-2026/status.md` | three activity rows, `last_updated`, checkbox | `F3` |
| `docs/0.5.0-beta-plan.md` | the credential-free visibility check and its result | `F9` |
| `atj/event.py` | `sync_status_checkboxes`, called from `save_status` | `F4`, `F14` |
| `atj/intake.py` | `_relative_checkout` | `F8` |
| `tests/test_operator_surface.py` | two new tests, one rewritten | `F4` |
| `tests/test_intake.py` | one new test | `F8` |
| `events/trial-2-2026/audits/intake.md` | round one of this report, committed unedited | verified |

Round one of this report was committed with no changes made to it: its front
matter still reads `result: FAIL` with `F1` at `blocking: true`, which is what
the artifacts elsewhere in the commit cite.

## Deterministic validation results

Re-run at 2026-09-21T23:36:59Z on `d899bef`:

| Command | Result |
|---|---|
| `python3 -m atj event validate events/trial-2-2026` | `PASS (0 problems, stage intake)` |
| `python3 -m atj validate reports events/trial-2-2026` | `PASS — 4 artifacts, 0 blocking, 0 major, 0 minor, 0 advisory` |
| `python3 -m atj validate publication events/trial-2-2026` | `CLEAR (4 artifacts, 0 blocking, 0 other)` |
| `python3 -m atj release-check` | `PASS`, every line including template schemas, version-skew, write contracts, signed approvals (15, frozen) and sample event |
| `python3 -m pytest tests/ -q` | `517 passed, 5 skipped, 282 subtests passed` |
| `python3 -m atj demo build` | `Rebuilt … 54 artifacts validated`, `Demo check: PASS`, and the working tree stays clean, so the committed sample matches the generator |
| `python3 -m atj event validate events/live-trial-2026` | `PASS (0 problems, stage complete)` |
| `python3 -m atj event validate events/sample-mock-2026` | `PASS (0 problems, stage complete)` |

Every result the operator reported reproduces. The two completed events were
validated because the framework changes touch code both of them run through;
neither moved.

The test count is 517 against 514 at the configuration audit's third round,
which is the three tests this commit adds and no test removed.

## Verification of each repair

### F1 — the gitlink, repaired as a decision

Re-derived, not read.

- **The corrected facts are true.** With `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM`,
  `GIT_TERMINAL_PROMPT` and `GIT_ASKPASS` neutralized and `credential.helper`
  emptied, `git ls-remote https://github.com/beekeeper-lab/claude-kit` returns
  `refs/heads/main` at `94881ec7`, and `beekeeper-lab/website` and
  `beekeeper-lab/atticus-vault` are refused under the same conditions, which is
  the control that proves no token was in play. `git fetch --depth 1 origin
  3dff46d6…` into an empty scratch repository succeeds and `git cat-file -t`
  reports `commit`.
- **Nothing still rests on the false premise.** Every occurrence of "private",
  "fetch", "SSH", "credential", "reachable" and "assumed" in the record was read
  in place. The only "private" left is the front matter's `visibility: private`.
  The gitlink paragraph now reads "The reason it is not initialized is the
  configured URL, not the repository's visibility", and the closing sentence
  "Nothing may be assumed about its content, and no judgment may cite it" is a
  consequence of the scope decision rather than of inaccessibility.
- **The error is disclosed rather than quietly overwritten.** The record says an
  earlier version was wrong and points at this audit's `F1`, which is the
  behaviour the framework asks of a repair.
- **It is stated as a decision, and it is now an official one.** "The gitlink is
  out of the eligible scope by event-director decision, not by inaccessibility",
  with three reasons: the eligible scope is the tree a plain clone produces, the
  event does not rewrite a submission's declared remote, and `claude-kit` is a
  shared `beekeeper-lab` toolkit rather than this submission's own instructions,
  so materializing it would widen what H6 tests. `event.md:23-27` gives the
  event-director the authority, and `F6`'s approval puts the event-director's
  name on the artifact that carries the decision. Round one's objection — a scope
  ruling attributed to nobody — is answered.
- **The unchanged facts still re-derive.** `.gitmodules` declares exactly one
  submodule; `git submodule status` still prints `-3dff46d6…`; `git ls-tree HEAD
  .claude/shared` still gives the same SHA as a `160000 commit` entry.

The decision is a judgment about scope, and this audit does not second-guess it.
It is internally consistent, it is the narrower of the two available readings,
and it is now recorded where a judge will read it.

### F2 — `completed_at`

`team-scribe` 23:31:02Z, `team-demos` 23:31:44Z. Both are in the past, both are
after their `started_at` of 21:53:01Z and 22:04:10Z, both precede the approval at
23:33:46Z and the commit at 23:36:21Z, and both files' mtimes are 23:33:46Z,
which is the approval write. The values are plausible and mutually consistent;
no instrument in this repository can prove a minute, and `F20` of the
configuration audit is still why.

### F3 — the ledger

Three rows added, and each says what happened:

| Row | Claim | Checked against |
|---|---|---|
| 23:16:00Z | hand repair of the body checkbox that `atj event validate` was failing on | the file mtime round one read, and round one's own account |
| 23:16:37Z | intake stage audit, FAIL, 1 major and blocking, 4 minor, 5 advisory | this report's round-one front matter, exactly |
| 23:35:29Z | intake repaired, round one, F1-F10 with F7 left open | the commit's own file list; every named output exists |

Nine rows before, twelve now, strictly ascending, none before
`started_at: 21:51:56Z`, none after this audit's clock. `last_updated` is
23:35:29Z, the newest row. The round-one repair row lists `submissions/*.md`,
`status.md`, `docs/0.5.0-beta-plan.md`, `atj/event.py`, `atj/intake.py` and
`tests/`, which is the commit's file list less this report itself.

### F4 — the framework half, and what the rewritten test now covers

`sync_status_checkboxes` (`atj/event.py:515-546`) rebuilds the gate checkboxes
from `stage_gates` and the `complete` label from `current_stage`, leaves any
label it does not recognize untouched, and returns the body unchanged when the
template supplies no labels. `save_status` calls it before schema validation.

The concern worth stating is the rewritten test. `test_a_ticked_pending_gate_is_reported`
used to build its contradiction by setting a gate to `pending` and calling
`save_status`; that route is closed, so it now writes the ticked box into the
body directly and asserts `validate_status_narrative` reports it. That is not a
weakening. The condition the old test created can no longer exist, and the one
route left to a body that contradicts its ledger — a human or a tool editing the
body directly — is exactly what the new version exercises. The two added tests
cover the sync in both directions, including the case that matters most, a
hand-ticked box being untidied back to `pending` rather than laundered into a
passed gate. `validate_status_narrative` itself is unchanged, and the other
assertions in the class (`an unticked passed gate`, `a missing checkbox`) are
untouched.

Both completed events still validate, and `atj demo build` reproduces the
committed sample byte for byte, so the new write path has not moved an artifact
anywhere else. The residual behaviour — a silent body rewrite with no notice —
is `F14`, advisory.

### F5 — wrapper scope, and the counts inside it

| Claim in the repaired text | Re-derivation | Verdict |
|---|---|---|
| Nine files match the stated phrase scan across `*.md`, `*.html`, `*.json`, `*.txt` | ran the stated phrase list, case-insensitive, over those extensions: nine files, the same nine, no more | correct |
| `find . -path '*/.claude/*' -type f` counts 66 files | 66 | correct |
| Each of the ten demos carries its own `.claude/` directory | ten `.claude/` directories, one per `NN-*/demo/` | correct |
| The scan is a floor, not an inventory | true and important — my own round-one scan used a different phrase list and returned a partly different set, which is the point the sentence makes | correct |
| The same scan over `*.py` returns ten more | returns **13**, every hit on "Top candidate" alone | wrong — `F12` |
| The pinned tree is `LICENSE`, `README.md` and ten `NN-*/demo/` directories | also `.gitignore` | incomplete — `F12` |
| ScribeVault agent-file table, nine rows | `CLAUDE.md` 1, `.github/copilot-instructions.md` 1, `.claude/local/commands/` 3 named files, `.claude/local/skills/` 3 `SKILL.md`, `prompts/` and `agents/` `.gitkeep` only, `.claude/shared/` empty, `ai/reports/` 6 — all exact | correct except the `ai/beans/` row |
| `ai/beans/` — 168 files across 56 `BEAN-*` directories | 168 files, **54** `BEAN-*` directories, plus `_bean-template.md` and `_index.md`; 56 is the entry count | wrong — `F11` |
| "That is the full set" for ScribeVault | `ai/` contains only `beans/` and `reports/`; `.claude/` contains only what the table lists; `.github/` contains only `copilot-instructions.md` | complete as an enumeration, and `F15` is why that is a fragile way to say it |

The scope change `F5` asked for is done in both records, and it is the right
change: the demos wrapper is now a class rule over the whole checkout, which is
the only rule that survives a corpus built to evade phrase lists.

### F6 — approvals

Both records carry `approval_state: approved`, `validation_state: valid`,
`approved_by: event-director` and `approved_at: 2026-09-21T23:33:46Z`, and both
validate. This is what makes `F1`'s scope ruling an approved decision.

### F8 — the checkout path, and `live-trial-2026`

`_relative_checkout` resolves the checkout against the framework root and falls
back to the absolute path only when the checkout lives outside the root, which is
possible through `intake.run(..., workspace=...)` and is the honest fallback.
`tests/test_intake.py:276-291` asserts the recorded line contains neither the
temporary root nor a leading absolute slash. Both trial-2 records now read
`workspaces/trial-2-2026/<team>`, and no `/home/` path remains anywhere in
`events/trial-2-2026/` or in the plan. Nothing else in the framework parses or
prints that row.

**Leaving `live-trial-2026` alone is correct, and I would refuse the alternative.**
That event is complete, its records are approved, and `release-check` asserts 15
signed approvals in completed events are frozen. Editing them would break that
contract to change a string whose disclosure is already permanent in the commit
history — the path cannot be un-published by rewriting the file. The right
boundary is the one taken: fix the tool, fix the live event, leave the closed
ones as the record of what happened.

### F9 — the visibility check

Reproduced verbatim from `docs/0.5.0-beta-plan.md:193-199`:

| Repository | Anonymous `git ls-remote` |
|---|---|
| `ScribeVault` | succeeds, `67969dd9…` at HEAD, which is the pin |
| `ai-security-demos` | succeeds, `dc35f696…` at HEAD, which is the pin |
| `claude-kit` | succeeds, `94881ec7…` at HEAD |
| `website` | refused — "Repository not found", authentication failed |
| `atticus-vault` | refused — same |

The plan's sentence "Until that check is cited, a visibility claim in this plan
is the operator's assertion, not a verified fact" is the repair the configuration
audit's `F17` asked for, and it generalizes rather than patching one paragraph.

### F10 — detachment

| Checkout | HEAD | Branch | Dirty |
|---|---|---|---|
| `team-scribe` | `67969dd9479c096f05d998d8c50e5ea1968e3245` | detached (`HEAD`) | 0 |
| `team-demos` | `dc35f6962130af5e5be3fe16672e3d4964850eb9` | detached (`HEAD`) | 0 |

Both still equal the pins in `teams.md`, both intake records, the `status.md`
abbreviations and the remotes.

### F7 — left open, and the reason holds

`check_templates` (`atj/cli.py:1525-1546`) requires `event_id`, `rubric`,
`framework_commit`, `visibility`, `approval_state`, `validation_state`,
`started_at` and `completed_at` of every file in `framework/templates/`, so
trimming `team-roster.md` to the three fields the framework actually writes does
fail the contract. `events/live-trial-2026/teams.md` carries the three, and that
event is frozen. The operator's account of why this is a decision rather than a
patch is accurate, and the finding stays open at advisory.

It does not hold this gate. The artifact the gate freezes is `teams.md`, it
validates against `schemas/roster.schema.json`, and its four required keys are
present and correct. What is missing is a `visibility` and an `approval_state`
on a roster, which no code reads and which the template promises and the
generator has never written.

## What round one verified, and still holds

Re-checked where the repair touched it, taken forward where it did not.

- Pins agree at full and abbreviated length across `teams.md`, `status.md`, both
  intake records, both checkouts and both remotes. Both working trees clean.
- ScribeVault: 26 test files named across nine README categories, 30 in the tree,
  all 26 present, difference exactly four. Every other factual claim in the
  record re-derived in round one and none of them was edited by this commit.
- AI Security Demos: no test file anywhere in the tree, ten demos, attack-vector
  list matches the README row for row, 19 `import anthropic` sites all inside
  function bodies.
- Both records carry the five template sections plus the two the configuration
  audit's `F4` repair added, and every field the intake schema requires.
- Versions: rubric `submission-evaluation@1.1.0`, `prepare-submission@1.1.0`,
  `judging-auditor@1.1.0`, framework `0.4.0-beta`.
- Eligibility: one immutable pin each, both repositories reachable and public by
  anonymous check, both checkouts at the pin. The one unresolved eligibility
  question in round one — the gitlink's scope — is `F1`, and it is resolved.
- The withdrawal of `beekeeper-lab/website` is findable in `event.md:59-67` and
  `docs/0.5.0-beta-plan.md:174-203`, and its privacy premise is verified.
- The configuration audit's deferrals are still visible where the evidence stage
  reads them: `F7` in `event.md:130-139`, `F11` in `event.md:157-165` and now in
  both records' wrapper sections.

## Privacy and publication

- `events/trial-2-2026/public/` holds `.gitkeep` and nothing else.
- `atj validate publication` reports CLEAR over four artifacts.
- No `/home/` path remains in any event artifact; round one's `F8` disclosure is
  gone from the current tree, though not from the history, which is why the
  framework change matters more than the file edit.
- No credential, key or third-party personal identifier appears in any artifact.
  The plan's new code block names no host beyond `github.com` and no account.

## Instruction-shaped content encountered

Same treatment as round one: described, never followed. The phrase scan this
round re-ran over the demos checkout matched nine text files and 13 Python
files, all inside `workspaces/trial-2-2026/team-demos`. The Python matches are
the string "Top candidate" in the demos' own ranking output, not payloads. The
text matches include the resume payload at
`01-resume-that-talked-back/demo/goofy-goof.md:20-27`, which directs a screening
assistant to score a candidate 100 and rank them first; it was read, counted and
not acted on. No session was rooted in either checkout, and every command ran
from the framework root.

## Findings

| Severity | Rule | Artifact | Scope | Blocking | Finding | Required repair |
|---|---|---|---|---|---|---|
| major, **repaired** | a claim in an intake record must be re-derivable | `events/trial-2-2026/submissions/team-scribe.md:139-165` | event | no | Round one's false premise is gone; the constraint is stated truthfully, the error is disclosed, and the out-of-scope ruling is an event-director decision on an approved record | None |
| minor, repaired | `completed_at` describes the record | `submissions/*.md:11` | event | no | Both set to the minute the content was completed, consistent with mtimes and the approval | None |
| minor, repaired | the ledger records the work | `events/trial-2-2026/status.md` | event | no | Three rows added, ascending, contents match the history, `last_updated` current | None |
| minor, repaired | the body may not contradict the ledger | `atj/event.py:515-546` | framework | no | `save_status` writes the gate checkboxes both ways, with two new tests; the rewritten test still covers the remaining route | None; residual `F14` |
| minor, repaired | wrapper scope | `submissions/team-demos.md:115-146` | event | no | Scope is now every file in the demos checkout, and the ScribeVault paths are enumerated | None for the scope; `F11`, `F12`, `F13` for the text |
| advisory, repaired | approval precedes the freeze | `submissions/*.md:16-21` | event | no | Both records approved by the event-director | None |
| advisory, **open** | one source for artifact shape | `framework/templates/team-roster.md:1-12` | framework | no | Template, event template and schema still disagree; the two obvious fixes each break something | Decide it: have `atj event init` write the full roster front matter for new events and leave completed ones alone |
| advisory, repaired | no operator path in a public artifact | `atj/intake.py:361-373` | framework | no | Tool repaired with a test, both records rewritten, completed events left frozen | None |
| advisory, repaired | a claim is attributed or checkable | `docs/0.5.0-beta-plan.md:188-203` | framework | no | The credential-free check and its five results are in the plan; reproduced here | None |
| advisory, repaired | the evidence base may not move | `workspaces/trial-2-2026/*` | event | no | Both checkouts detached at their pins, clean | None |
| minor, **new** | a count attributed to `find` must be what `find` returns | `submissions/team-scribe.md:126` | event | no | "168 files across 56 `BEAN-*` directories" — 168 is right, the directory count is 54, and 56 is the entry count including two loose files | Write 54 directories plus two files |
| minor, **new** | same rule, stated scan | `submissions/team-demos.md:138-140` | event | no | "the same scan over `*.py` returns ten more" — it returns 13, all on "Top candidate"; and the tree enumeration omits `.gitignore` | Correct to 13 and say what it matches; name `.gitignore` or drop the enumeration |
| minor, **new** | an inserted section may not break the antecedent below it | `submissions/team-demos.md:108-151` | event | no | "Every one of those payloads" now points at a list the same section says is mostly not payloads. Configuration `F12`'s defect in the other record | Move the section below that paragraph or name the antecedent |
| advisory, **new** | no silent change to an artifact | `atj/event.py:1118-1124` | framework | no | The checkbox sync rewrites the body with no notice and no record, so a deliberate manual edit disappears at the next ledger write | Report on stderr when the sync changes a box |
| advisory, **new** | consistent treatment of two submissions in one event | `submissions/team-scribe.md:128-130` | event | no | One record wraps by class because an allowlist is "under-inclusive by construction"; the other relies on an allowlist, and that allowlist already carries `F11` | State the reason for the difference, or apply the class rule to both |

## Advisories

1. Three of the five new findings are the repair round's own residue, and two of
   them are miscounts in text written to fix a miscount's cousin. Nothing in the
   toolchain counts anything in a record: `atj event validate`, `atj validate
   reports`, `release-check` and 517 tests all pass over "56 directories" and
   "ten more". This is configuration `F20`'s shape one field over, and worth one
   line in the framework backlog next to it.
2. The artifacts now cross-reference this report by finding number —
   `status.md`'s 23:16:00Z row cites `F3`, `team-scribe.md` cites `F1`, the plan
   cites `F1` and `F9`. Superseding in place keeps those references valid, which
   is why the IDs are stable and why a future round must not renumber.
3. This report was written by the same auditor that wrote round one. Nobody
   independent has checked either. The framework has no second auditor, and
   `framework/rubrics/README.md` says the reviewer of a repair is never the party
   that wrote it; the operator is the only party who can hold that line here.
4. `F14` and the `F4` repair together mean `validate_status_narrative` is now
   nearly unreachable in normal operation. That is the intended outcome, but it
   also means the check is no longer evidence of anything: a passing narrative
   check after a tool write says only that the tool wrote it.

## Completion gate

- [x] No blocking findings
- [x] No major findings — `F1` is major and `repaired`; nothing open exceeds minor
- [x] Calculations valid — the counted claims re-derived; two that did not are
      `F11` and `F12`, and neither changes an obligation
- [x] Evidence references resolve — every path, line reference and commit in both
      records resolves, including the gitlink SHA and both remotes
- [x] Version and identity checks pass
- [x] Privacy boundary passes — `public/` empty, publication CLEAR, no operator
      path left in the tree
- [x] Every finding recorded in `findings:` with a `scope` and a `blocking` flag
- [ ] Approved with `atj event approve <this file>`

## Outstanding work

1. Record the `roster-frozen` gate. Freeze `teams.md` at `frozen: true`, run
   `atj event gate`, and add the activity row; `last_updated` is now written by
   the tool, as of the `F4` repair.
2. Correct `F11`, `F12` and `F13` in the two intake records. They are text
   corrections inside an approved artifact, so re-approve after, and re-validate.
   None of them needs to precede the freeze, and none changes a pin, an
   eligibility determination or a wrapper obligation.
3. `F7` needs a decision, not a patch, and `F14` and `F15` are optional.
4. Carry the configuration audit's deferrals into the evidence stage: `F7`
   (ScribeVault display, audio device, network) and `F11` (the untrusted-data
   wrapper, now scoped by class for the demos and by enumeration for
   ScribeVault).
