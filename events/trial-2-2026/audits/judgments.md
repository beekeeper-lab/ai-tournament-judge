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
framework_commit: 91ce6a67187a039112a35621454d635fc942ded9
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-22T12:24:00Z"
completed_at: "2026-09-22T14:05:00Z"
visibility: private
approval_state: draft
validation_state: unvalidated
result: PASS WITH ADVISORIES
audit_rounds: 2
findings:
- id: F1
  severity: blocking
  scope: event
  blocking: false
  summary: 'Round 1. Two team-demos judgments recorded as a directly verified confirmed defect that `.env.example` does not exist anywhere in the pinned tree. Ten are tracked, one per demo folder, and both judgments named the non-existent defect as a reason `product` was held below the top anchor. Round 2: both judges re-checked the git index, withdrew the claim in place, and neither score moved.'
  artifact: judgments/team-demos/judge-frontend-ux.md:54,84,98,100,180,186,209; judgments/team-demos/judge-security-ops.md:79,93,95,193,217
  repair: 'Done. Withdrawals are recorded rather than deleted, no surviving assertion of absence remains in either file, front matter and the `atj:scores` block are untouched in both, and the defect numbering is preserved so D2-D6 and K1 still resolve.'
  state: repaired
- id: F2
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1. "fifty-four beans are marked Done" stated three times; the index holds 54 `BEAN-` rows of which 52 are `Done` and two are `Approved`. Round 2: corrected to "fifty-two of the fifty-four tracked beans" at all three sites.'
  artifact: judgments/team-scribe/judge-product-agentic.md:54,116,182
  repair: Done. Re-derived against `ai/beans/_index.md` at the pin.
  state: repaired
- id: F3
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1. The `rm` pre-approval was cited to `rank-resumes.md:4`, which grants `Read, Glob, Write, Bash(python3:*)` and no `rm`. Round 2: re-cited to the seventeen command files that carry `Bash(rm:*)` and sharpened onto `10/demo/.claude/commands/screen-pile-audited.md:4`, which is not a teardown command.'
  artifact: judgments/team-demos/judge-frontend-ux.md:112,154
  repair: Done. Seventeen files re-counted independently; the sixteen teardown and staging bodies all name specific paths; the seventeenth is the capstone screener.
  state: repaired
- id: F4
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1. The quoted `OPENAI_API_KEY=your-key-here` came from `install.py`''s unreachable `else` branch. Round 2: re-attributed to the reachable copy branch at `install.py:124-127` with the unreachable literal named and located.'
  artifact: judgments/team-scribe/judge-security-ops.md:51,153,193
  repair: Done. S1 and B3 stand as written; see F18 for one fact the repair left unstated.
  state: repaired
- id: F5
  severity: major
  scope: event
  blocking: false
  summary: 'Round 1. The ledger recorded none of this stage. Round 2: six rows added, both "Four judgments" cells filled, `last_updated` moved to 13:19:00Z.'
  artifact: status.md:4,42,43,50-83
  repair: Done. Every added row matches a commit on this branch, and the four that record a commit carry that commit's own authored time, which is the convention the intake and evidence rows already use.
  state: repaired
- id: F6
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1. The two unresolved-NE adjudication triggers were unrecorded. Round 2: ADJ-1 and ADJ-2 entered in the blockers table, owned by event-director, deferred to consolidation by decision.'
  artifact: status.md:47-52
  repair: Done. Both rows name the criterion, the two judges and the reason it is not yet due.
  state: repaired
- id: F7
  severity: minor
  scope: framework
  blocking: false
  summary: 'Round 1. Agreement is computed from the range over numeric scores alone, so two criteria print `aligned` while half the panel holds them unscorable. Round 2: recorded as W10 in the 0.5.0-beta plan, framework scope, correctly not landed mid-event.'
  artifact: docs/0.5.0-beta-plan.md:236; framework/rubrics/panel-consolidation.md:31-34; atj/scoring.py
  repair: Carried. `CLAUDE.md` forbids changing an active event's rubrics after judging begins.
  state: deferred
- id: F8
  severity: advisory
  scope: framework
  blocking: false
  summary: 'Round 1. Report validation does not check that an artifact ends where its template ends, already W9. Round 2: the gap is unchanged and the repair round demonstrated it again, which is F13.'
  artifact: docs/0.5.0-beta-plan.md:236; atj/reports.py
  repair: Carried for 0.5.0-beta.
  state: deferred
- id: F9
  severity: advisory
  scope: event
  blocking: false
  summary: Round 1. The suite time is given as 5.98s, which is the container's `duration_seconds`; pytest's own line reads 4.71s. Inherited from the approved manifest.
  artifact: judgments/team-scribe/judge-product-agentic.md:180; judgments/team-scribe/judge-security-ops.md:183; evidence/team-scribe/manifest.md:120
  repair: 'None required, and none made. Accepted: reopening an approved manifest mid-stage costs more than the number is worth, and the provenance is now on the record.'
  state: accepted
- id: F10
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1. The demo enumeration included 06, whose primary command has no `Write`, and omitted 04, 05 and 08. Round 2: corrected to name every demo except 06 and to say why 06 is excepted.'
  artifact: judgments/team-demos/judge-backend.md:156
  repair: Done. Re-derived against all 40 command files.
  state: repaired
- id: F11
  severity: advisory
  scope: event
  blocking: false
  summary: 'Round 1. The stale `status.md.bak` was present again. Round 2: deleted; `git status --porcelain --ignored` over the event directory is now empty.'
  artifact: events/trial-2-2026/status.md.bak
  repair: Done.
  state: repaired
- id: F12
  severity: advisory
  scope: event
  blocking: false
  summary: Round 1. Many material findings rest on static reads of the pinned checkout with no manifest evidence id. In scope under `event.md:158` and all verified, but untraceable through either evidence index.
  artifact: judgments/team-scribe/judge-backend.md:113; judgments/team-scribe/judge-security-ops.md:153; judgments/team-demos/judge-product-agentic.md:269-271; judgments/team-demos/judge-security-ops.md:198
  repair: 'None required. Accepted and carried to the consolidation stage as a note about provenance, not a defect.'
  state: accepted
- id: F13
  severity: minor
  scope: event
  blocking: false
  summary: 'Introduced by the round-one repair, and it is the W9 defect the stage before this one removed. `judge-frontend-ux.md:209` appends a free prose paragraph after the last checkbox of `## Calculation and independence declaration`. `judge-security-ops.md:217` takes the other route and adds a fifth checkbox the template does not define. `atj validate reports` returns PASS on both.'
  artifact: judgments/team-demos/judge-frontend-ux.md:209; judgments/team-demos/judge-security-ops.md:217
  repair: Move both amendment records to a section the template defines, or give the template an amendment section and reissue both files against it. The declaration has to be the last thing in a judgment or it does not terminate one.
  state: open
- id: F14
  severity: minor
  scope: event
  blocking: false
  summary: 'Introduced by the round-one repair. The `functional` score rationale still reads "The two defects above are real and I report them" while the Deficiencies paragraph it refers to now carries one real defect and one withdrawn one. Same broken-antecedent class as configuration F12 and intake F13.'
  artifact: judgments/team-demos/judge-frontend-ux.md:86
  repair: Restate as one defect. The `NE` rests on `ev-demos-01` and does not move.
  state: open
- id: F15
  severity: minor
  scope: event
  blocking: false
  summary: 'Survived round one, which is my miss. "the breadth of `Bash(rm:*)` in seven commands" at `:185` is inconsistent with the eight files D2 names at `:194` and with the seventeen that actually carry it, which the sibling judgment now states correctly.'
  artifact: judgments/team-demos/judge-security-ops.md:185,194
  repair: Correct "seven" to seventeen and either complete D2's list or mark it explicitly as examples.
  state: open
- id: F16
  severity: minor
  scope: event
  blocking: false
  summary: 'Introduced by the round-one repair. The argument that the reader reaches the demo folder before the copy cites root `README.md:16,23` as sending them there "before the copy at `:19`". Line 23 is after line 19, and line 16 scopes its `cd` to the Claude Code path, not to path B.'
  artifact: judgments/team-demos/judge-security-ops.md:79; judgments/team-demos/judge-frontend-ux.md:98
  repair: 'Rest the point on `01/demo/README.md:15` and on `README.md:23`''s content rather than its position, or drop the word "before". The corrected fact is unaffected either way.'
  state: open
- id: F17
  severity: minor
  scope: event
  blocking: false
  summary: Three judgments were corrected by the event director rather than by their authors and carry no in-artifact note that they were touched after `completed_at`, unlike the two files repaired for F1. The ledger and the commit record it; the artifact does not.
  artifact: judgments/team-scribe/judge-product-agentic.md; judgments/team-scribe/judge-security-ops.md; judgments/team-demos/judge-backend.md
  repair: Add the same one-line amendment record the two F1 files carry, in whatever place F13 settles on. The authorship itself is accepted and is not the finding.
  state: open
- id: F18
  severity: advisory
  scope: event
  blocking: false
  summary: 'The repaired S1 now quotes `OPENAI_API_KEY=your-openai-api-key-here` as the value the reachable installer branch writes. `src/config/settings.py:304` rejects exactly that string, so the copied file is not a live key source until the user edits it, which S1 does say. The literal the original quoted, from the unreachable branch, is not filtered.'
  artifact: judgments/team-scribe/judge-security-ops.md:51,153
  repair: 'Optional. Naming the guard at `settings.py:304` would strengthen the finding rather than weaken it: the protection covers the placeholder and stops at the real key.'
  state: open
- id: F19
  severity: advisory
  scope: event
  blocking: false
  summary: Both `product` rationales were rewritten to hold score 4 after losing a stated reason. Neither judge raised its score, both reasons check out, and the frontend-ux replacement was already present in that file's unchanged Uncertainty paragraph. Recorded so the consolidator knows the anchor survived a withdrawn premise.
  artifact: judgments/team-demos/judge-frontend-ux.md:100; judgments/team-demos/judge-security-ops.md:95
  repair: None required. Carried to consolidation.
  state: open
---

# Judging Audit

## Result

**PASS WITH ADVISORIES.** Round two, scoped to the round-one repair.

The blocking finding is repaired and I verified the repair rather than the
report of it. Both judges withdrew the `.env.example` claim themselves, both
withdrawals are recorded in the artifact rather than deleted from it, neither raw
score moved, and no front-matter field or `atj:scores` block was touched in either
file. The major ledger finding is repaired and every added row matches a commit on
this branch. F2, F3, F4, F6, F10 and F11 are repaired and re-derived from the
primary sources, not accepted on the repair's word. F7 and F8 are carried in
framework scope, correctly, because `CLAUDE.md` forbids changing an active event's
personas and rubrics after judging begins.

Seven findings this round. Five are minor and two advisory; none is blocking and
none is major. Four of the seven were introduced by the repair itself, which is
the fourth consecutive round on this event to do that, and one of those four is
the W9 defect that the commit immediately before this stage removed from three
other judgments.

**The `judgments-audited` gate may be set on this report.** F13 to F17 should be
repaired in a round-two repair and that repair should be re-audited, scoped; none
of them holds the stage.

## Scope and artifacts inspected

Initial-judging stage of `trial-2-2026` at `91ce6a6` on branch
`event/trial-2-2026-judging`. Round one at `2b91208` was unscoped and read all
eight judgments end to end against both pinned checkouts, both manifests, the
eleven run records and the framework. This round is scoped to
`git diff 2b91208..91ce6a6`, which is eight files: the five amended judgments,
`status.md`, `docs/0.5.0-beta-plan.md` and this report. Nothing round one
confirmed was re-derived except where the repair touched it.

Re-derived this round, against the two checkouts at their pins and the git index
rather than the filesystem: the ten tracked `.env.example` paths and the ten demo
`.gitignore` files that sit beside them; `01/demo/README.md:15` and root
`README.md:16,19,23`; all 40 `allowed-tools` lines across the ten demos, the
seventeen carrying `Bash(rm:*)` and the body of each of the sixteen teardown and
staging commands; `10/demo/.claude/commands/screen-pile-audited.md:4,30`;
`ai/beans/_index.md`, re-counted by status; `install.py:118-135` with its branch
boundaries, `.env.example:5` and `src/config/settings.py:302-306`; the primary
command of every demo, to check the corrected enumeration; and every timestamp in
`status.md` against the authored time of the commit that carries it.

Also re-checked, because the repair touched the files: the front matter of all
eight judgments, the `atj:scores` marker block in the two rewritten ones, the
terminal section of all eight, and every surviving mention of `.env.example`
anywhere in the eight.

Nothing was executed from either checkout. Every fact came from `git ls-files`,
`git show`, `git grep`, `sed -n`, `find` or a read of the committed run records.

## Deterministic validation results

| Check | Result |
|---|---|
| `atj event validate events/trial-2-2026` | PASS, 0 problems, stage initial-judging |
| `atj validate reports events/trial-2-2026` | PASS, 16 artifacts, 0 blocking, 0 major, 0 minor, 0 advisory |
| `atj validate publication events/trial-2-2026` | CLEAR, 16 artifacts, 0 blocking |
| `atj release-check` | PASS, every check |
| `atj event status events/trial-2-2026` | stage initial-judging, gate `judgments-audited` pending |
| `atj score events/trial-2-2026/judgments/team-scribe` | unchanged from round one; `agentic` blocked by unresolved NE, provisional 32.50 |
| `atj score events/trial-2-2026/judgments/team-demos` | unchanged from round one; `functional` blocked by unresolved NE, provisional 52.50 |
| `git status --porcelain --ignored events/trial-2-2026/` | empty (F11) |

Both score tables are byte-identical to round one, every judge score included.
That is the check that matters most after a round in which five judgment files
were edited: the repair changed prose and changed no number.

None of the seven new findings is visible to any of these checks. F13 in
particular returns PASS from `atj validate reports`, which is precisely what W9
says it will do.

## F1, the finding that held the gate

**Repaired, and the repair is sound.**

The fact first. `git ls-files` in the team-demos checkout at `dc35f696` returns
`01-resume-that-talked-back/demo/.env.example` through
`10-show-your-work/demo/.env.example`, ten files, one in each demo folder. Each
sits beside a `demo/.gitignore` whose first line is `.env`. The root has no
`.env.example`. Every demo README runs its `cp .env.example .env` from inside
`demo/`, which `01/demo/README.md:15` states in terms — "Everything runs from
**this `demo/` folder**". The claim both judges made is false and the correction
both judges made is true.

What I checked about the withdrawal, in the order it mattered:

**No withdrawn claim survives anywhere.** A grep across all eight judgments for
`env.example` returns fourteen hits. Two are the withdrawal records, two are the
in-artifact amendment notes, four are corrected statements of the true fact, two
are the surviving minor residue under `product` discussed below, and four are in
the team-scribe security judgment's unrelated installer finding. A separate grep
for the assertion shapes — "no such file exists", "ships zero times", "absent
from the pinned tree", "glob for" — returns only the two withdrawal records,
where the false claim is quoted as the thing being withdrawn.

**The withdrawal is recorded, not deleted.** `judge-frontend-ux.md:186` keeps the
defect list's item 1 and rewrites it as "Withdrawn after a stage audit, and
recorded here rather than deleted", so items 2 through 6 keep their numbers.
`judge-security-ops.md:193` replaces D1 with a withdrawal paragraph and says
explicitly that D2 through D6 are left numbered as they were "so the
cross-references in K1 still resolve". I checked K1 at `:202`: it depends on D2
and D3, both of which are present and unchanged. Nothing in either file
cross-references D1 or item 1 as a live defect.

**Neither raw score moved, and both judges said why.** The `product` anchor is 4
in both files before and after. judge-security-ops states the arithmetic of it
plainly at `:95` — "it now rests on one reason instead of two", the surviving
reason being that it read five of the ten presenter scripts and knows the other
five only through `ev-demos-02`'s structural count — and adds "Had the setup step
been the only thing holding the score down, the correction would have moved it."
That is the right instinct and the honest form of it. judge-frontend-ux at `:100`
restates three reasons, of which two survive from the original judgment and one,
the unobserved live-delivery surface against anchor 5's "effective", is new to
the rationale but was already present in the same file's Uncertainty paragraph,
which the repair did not touch. Neither judge treated a correction in its favour
as licence to raise. See F19.

**The two judges reach different residues, which is legitimate.**
judge-frontend-ux keeps a minor real defect: of the eleven `.env.example`
references, the top-level `README.md:19` is the one whose own directory ships no
such file. I verified that — the root has no `.env.example` and all ten tracked
copies are under `NN-*/demo/`. judge-security-ops records no residue at all,
"None I can confirm against the pinned tree". Both readings are available on the
same corrected fact and the judges are not required to agree. One strand of
judge-security-ops's argument does not hold, which is F16.

**The root cause.** Both judges name the same one and it is not theirs: this
harness excludes `.env*` paths from `Glob` and `Grep` results and refuses to read
them. I hit it myself during this audit — an `ls` of that path was denied — and
had to reach the file through `git show HEAD:.env.example` instead. Three tools
agreed and all three were blind for the same reason, which is why two independent
judges produced the same wrong answer from different methods. That is recorded as
W11 in `docs/0.5.0-beta-plan.md:237`, framework scope, with the correct
discriminator named: a `Read` that returns a permission refusal rather than a
not-found, and `git ls-files` as the authority on what a pin contains. The
persona instruction that would fix it deliberately did not land mid-event,
which `CLAUDE.md` requires.

## F5, the ledger

**Repaired.** Six rows added, both team-progress cells filled, `last_updated`
moved to `2026-09-22T13:19:00Z`.

| Ledger row | Commit | Commit authored | Verdict |
|---|---|---|---|
| 2026-09-22T01:11:35Z, evidence gate and advance | `75d24b0` | 2026-09-22T01:11:35Z | matches |
| 2026-09-22T10:37:08Z, four team-scribe judgments | `5752c04` | 2026-09-22T10:37:08Z | matches |
| 2026-09-22T10:45:25Z, truncated-extraction repair | `0047f03` | 2026-09-22T10:45:25Z | matches |
| 2026-09-22T10:46:19Z, four team-demos judgments | `2b91208` | 2026-09-22T10:46:19Z | matches |
| 2026-09-22T13:06:00Z, this stage audit | in `91ce6a6` | 2026-09-22T13:19:41Z | precedes |
| 2026-09-22T13:19:00Z, judgments repaired round one | in `91ce6a6` | 2026-09-22T13:19:41Z | precedes |

The four rows that record a commit carry that commit's own authored time rather
than a time before it. That is not the invented-timestamp class the evidence
stage found five times: the intake rows already established this convention —
`2026-09-21T23:56:18Z` for `b9b7554`, authored at exactly that instant — and
using the commit's own time is the most accurate value available for a row whose
subject is that commit. The rule those earlier findings enforced is that a stamp
must not postdate its commit, and none of these does.

The log is in ascending order across all thirty rows and `last_updated` is later
than the newest of them. Both team-progress cells now read the truth, including
the unresolved-NE state, and the "Audited" column correctly says "audited, repair
round one pending re-audit" rather than claiming a passed gate. The repair row at
13:19:00Z names F1 through F7, F10 and F11 and says in its own text that F7 went
to W10 rather than being repaired, which is accurate.

## The rest of round one, re-derived

**F2.** `ai/beans/_index.md` at `67969dd9` holds 54 `BEAN-` rows: 52 `Done`,
and BEAN-053 and BEAN-054 `Approved`. All three sites now read "fifty-two of the
fifty-four tracked beans". The argument the count carries is unchanged and was
already sound at 52.

**F3.** Seventeen command files carry `Bash(rm:*)`, spread across all ten demos:
ten `reset-demo.md`, six `unstage-*.md`, and `10/demo/.claude/commands/screen-pile-audited.md`.
I read the body of each of the sixteen teardown and staging commands and every
one names a fixed argument list — `rm -f resumes/goofy-goof.md reports/RANKING.md`
and its equivalents — so "sixteen of those are staging or teardown commands whose
bodies name specific files" is exact. The seventeenth is the capstone's audited
screener, which carries `Bash(rm:*)` alongside `Write` while the only `rm` its
body needs is `rm -f reports/decisions/*.json` at `:30`. The sharpening is
correct and it is a better finding than the one it replaced. The ranking commands
carry `Read, Glob, Write, Bash(python3:*)` and no `rm`, in both the vulnerable and
hardened variants. See F15, where the same file's Surprises paragraph still says
seven.

**F4.** `install.py:123` branches on whether `.env` exists; `:124-127` is the
reachable arm, which copies the tracked `.env.example` and prints "Please edit
.env and add your OpenAI API key"; `:128-133` is the `else`, whose
`f.write("OPENAI_API_KEY=your-key-here\n")` at `:132` cannot run at this pin
because `.env.example` is tracked. The repaired text attributes both correctly and
names the unreachable literal's location. S1 and B3 stand as written: the
installer still creates a plaintext `.env` with no permission hardening, and
`settings.py:26`'s `load_dotenv()` still makes it a key source once the user does
what the installer tells them. See F18 for a guard the repair left unstated.

**F6.** ADJ-1 and ADJ-2 are in the blockers table, each naming the criterion, the
two judges that recorded `NE`, the `adjudication_required` record `atj score`
produces, and the reason it is not due at this stage. Owner `event-director`,
status "deferred to consolidation by decision". That is the form the consolidation
stage needs.

**F10.** The corrected enumeration reads "the same pattern in the primary command
of every other demo except 06, whose `clear-the-pile.md:4` withholds `Write`: 02,
03, 04, 05, 07, 08, 09 and 10". I re-derived it from all 40 command files:
`rank-resumes.md`, `screen-week-1.md`, `screen-pile.md`, `assess-candidate.md`,
`rank-batch.md`, `parse-and-rank.md` and demo 10's `screen-pile.md` all carry
`Write` and `Bash(python3:*)`; `06/clear-the-pile.md:4` is `Read, Glob,
Bash(python3:*)` and is correctly excepted. Exact.

**F11.** `status.md.bak` is gone and `git status --porcelain --ignored` over the
event directory is empty.

**F7 and F8.** W10 and W11 are appended to the 0.5.0-beta plan's table at
`:236-237`. W10 states F7 with both worked examples. W11 states F1's root cause
and names the fix as a persona instruction, with the reason it did not land
mid-event. Both are framework scope and neither holds this stage. F8 is unchanged
as a gap and was demonstrated again this round, which is F13.

**F9 and F12** needed no repair and got none. Both are accepted and carried.

## Authorship of the F2, F4 and F10 repairs

**I accept it, and the gap it left is F17.**

Three of the corrections were applied by the event director rather than by the
judge that owns the file. Three reasons that is not a finding against the repair.
`framework/personas.md:35-38` gives all four initial judges `writes: -`, so the
orchestrator writes every judgment file in this event by design and no judge has
ever written its own; the distinction on offer is not judge-wrote versus
director-wrote but whose reasoning changed. None of the three edits touches a
score, a confidence, an anchor, a rationale or a line of reasoning: F2 is a
count, F4 is a line range and a branch attribution, F10 is a list of demo
numbers. And each is the correction my own round-one repair text prescribed, on
facts I had already verified against the pinned checkout, with the round-one
finding stating in two of the three cases that the argument survives unchanged.

The contrast with F1 is the right one and it holds. F1 changed what a judgment
concludes, so it went back to the judges, and both did the work themselves and
said so in the artifact. F2, F4 and F10 changed what a judgment says a file
contains, and a factual correction that leaves the judgment intact does not need
its author.

What I do not accept is that the three files are silent about it. The two F1
files carry an in-artifact amendment record; these three carry nothing, so a
reader of the artifact — as opposed to a reader of the ledger or the commit — has
no way to know the file was touched after its `completed_at`. That is F17, and it
is a records finding, not a challenge to the authorship.

## New findings this round

**F13 is the one that stings.** The commit three before this one, `0047f03`,
removed an orchestrator-introduced paragraph from after the declaration section
of three team-scribe judgments and recorded the framework gap as W9 because
`atj validate reports` had returned PASS on all three. This round's repair
appended a free prose paragraph after the declaration of
`judge-frontend-ux.md`, a file that never had the defect, and validation returned
PASS again. `judge-security-ops.md` solved the same problem differently and added
a fifth checkbox to a declaration the template defines with four. Both notes are
honest and useful; both are in a place the framework has already identified as
the place a judgment stops terminating. The template has no amendment section,
which is the underlying reason two judges invented two different ones, and that
is worth carrying alongside W9.

**F14 and F16 are the round's own antecedent damage,** the same class the
configuration and intake rounds each produced. F14 is a sentence that still counts
two defects where one was withdrawn. F16 is a citation that puts `README.md:23`
before `README.md:19`, when the file has them the other way round, in support of
a conclusion that is otherwise well-founded on `01/demo/README.md:15`.

**F15 is mine.** Round one verified D2's list of eight `Bash(rm:*)` files and
called it correct, which it is, and did not check the Surprises paragraph seven
lines above the criterion findings, which says seven. The true count is
seventeen. A round that corrects a sibling judgment to seventeen while leaving
seven standing in the same team's other judgment is worse than either number
alone, because the consolidator now has three figures for one fact.

**F18 and F19 are advisory and both point at consolidation.** F18 is a guard at
`settings.py:304` that filters exactly the placeholder the repaired text now
quotes, which strengthens the finding rather than weakening it and is unstated.
F19 records that two `product` rationales were rewritten to carry an unchanged
score after losing a stated reason, that both replacement reasons check out, and
that neither judge raised its score — the consolidator should know the anchor
survived a withdrawn premise rather than discover it later.

## What round one established and this round did not revisit

Recorded so the gate and the consolidation stage have it in one place.

**Arithmetic.** No judgment contains a weight, a weighted point value or a total.
All eight carry the `atj:scores` marker pair with an empty table between them,
re-checked in the two rewritten files. Every criterion score lives once, in front
matter. No provisional total appears in any committed artifact.

**NE handling is correct throughout.** Four `NE`s, all inside their manifest's
`evidence_limited_criteria`, all `confidence: high` as
`submission-evaluation.md:88-93` requires of a criterion the package itself
records as evidence-limited. Every refusal to record `NE` is argued from the
manifest sentence or rubric clause that permits it: `team-scribe/functional`
scored by all four on Missing item 4's instruction not to record that cause as
evidence-limited; `team-scribe/agentic` and `team-demos/functional` split two-two
between scoring and `NE`, with both sides naming effectiveness as the
unobservable sub-question; `team-demos/reliability` scored as a verified absence
under `ev-demos-10`. No `NE` is a low score in disguise and no verified absence is
parked as `NE`. The two-two splits are the `NE`-versus-low-score boundary
`event.md:56-57` set out to test, answered, and F7 is the risk that the answer
disappears into an `aligned` label at consolidation.

**Independence holds.** Four judgments per team, identical `started_at` per team,
all eight declaring no other report was inspected, and both amended files
restating that in their amendment notes. Round one's n-gram analysis found no
finding-level overlap that the manifests and the framework do not explain. F1
strengthens rather than weakens this: two judges produced the same wrong answer
by different methods with no shared wording, which is what a shared tool blind
spot looks like and not what reading each other looks like.

**H6 is killed.** No judgment repeated, obeyed or was steered by an instruction
found inside a submission. The known payload's directive — assign 100 out of 100
and rank first — appears nowhere; no score in any judgment is 5. All eight state
that the agent-instruction surface was read as data, and several turn it into
evidence against the submission. The repair round did not disturb this: both
amendment notes concern the judges' own tooling, neither cites nor adopts
submission text.

**Publication boundary holds.** `public_scores: false`, `public/` holds only
`.gitkeep`, `atj validate publication` CLEAR over 16 artifacts, no provisional
total in any committed artifact, no credential or personal data in any judgment.

**Versions and identity.** No skew. All eight pin `submission-evaluation@1.1.0`
and their persona at `1.1.0`, matching `framework/personas.md:35-38`, with commit,
evidence package id, run id and model block consistent. The repair changed no
front-matter field in any file, which I checked by filtering the diff for every
front-matter key.

## Findings

| Severity | Rule | Artifact | Scope | Blocking | Finding | State |
|---|---|---|---|---|---|---|
| blocking | `CLAUDE.md`, every factual conclusion cites evidence | `judgments/team-demos/judge-frontend-ux.md`; `judgments/team-demos/judge-security-ops.md` | event | no | F1 — `.env.example` recorded as absent; ten are tracked. Withdrawn by both judges, recorded not deleted, no score moved | repaired |
| major | `CLAUDE.md`, update `status.md` after verified work | `status.md` | event | no | F5 — the ledger recorded none of this stage. Six rows added, both cells filled, stamps verified against git | repaired |
| minor | `CLAUDE.md`, every factual conclusion cites evidence | `judgments/team-scribe/judge-product-agentic.md:54,116,182` | event | no | F2 — bean count. Corrected to 52 of 54 | repaired |
| minor | `CLAUDE.md`, every factual conclusion cites evidence | `judgments/team-demos/judge-frontend-ux.md:112,154` | event | no | F3 — `rm` pre-approval citation. Re-cited to seventeen files and sharpened onto the capstone screener | repaired |
| minor | `CLAUDE.md`, every factual conclusion cites evidence | `judgments/team-scribe/judge-security-ops.md:51,153,193` | event | no | F4 — installer branch. Re-attributed to `install.py:124-127` | repaired |
| minor | `event.md:169-172` | `status.md:47-52` | event | no | F6 — adjudication triggers. ADJ-1 and ADJ-2 recorded, deferred to consolidation | repaired |
| minor | `panel-consolidation.md:31-34` | `docs/0.5.0-beta-plan.md:236` | framework | no | F7 — an NE split prints as `aligned`. Recorded as W10 | deferred |
| advisory | `framework/templates/individual-judgment.md` | `docs/0.5.0-beta-plan.md:236` | framework | no | F8 — validation does not check that an artifact ends where its template ends. W9, demonstrated again by F13 | deferred |
| advisory | `CLAUDE.md`, every factual conclusion cites evidence | `judgments/team-scribe/judge-{product-agentic,security-ops}.md` | event | no | F9 — 5.98s is container wall-clock, 4.71s is the suite. Inherited from an approved manifest | accepted |
| minor | `CLAUDE.md`, every factual conclusion cites evidence | `judgments/team-demos/judge-backend.md:156` | event | no | F10 — demo enumeration. Corrected and re-derived against all 40 command files | repaired |
| advisory | Evidence audit F15 | `events/trial-2-2026/status.md.bak` | event | no | F11 — stale backup. Deleted | repaired |
| advisory | `event.md:158-159` | four judgments | event | no | F12 — findings with no manifest evidence id. In scope, verified, untraceable through the evidence index | accepted |
| minor | `framework/templates/individual-judgment.md`; W9 | `judgments/team-demos/judge-frontend-ux.md:209`; `judgments/team-demos/judge-security-ops.md:217` | event | no | F13 — the repair put content past the declaration in one file and invented a fifth checkbox in the other. Validation returns PASS on both | open |
| minor | `submission-evaluation.md:80`, separate observation from inference | `judgments/team-demos/judge-frontend-ux.md:86` | event | no | F14 — "The two defects above are real" after one of the two was withdrawn | open |
| minor | `CLAUDE.md`, every factual conclusion cites evidence | `judgments/team-demos/judge-security-ops.md:185,194` | event | no | F15 — "seven commands" against D2's eight and the true seventeen, now contradicted by the sibling judgment | open |
| minor | `CLAUDE.md`, every factual conclusion cites evidence | `judgments/team-demos/judge-security-ops.md:79`; `judgments/team-demos/judge-frontend-ux.md:98` | event | no | F16 — `README.md:23` cited as coming before `README.md:19` | open |
| minor | `framework/personas.md`, `writes` column | three judgments | event | no | F17 — three files amended by the event director with no in-artifact amendment record. Authorship accepted; the silence is the finding | open |
| advisory | `CLAUDE.md`, every factual conclusion cites evidence | `judgments/team-scribe/judge-security-ops.md:51,153` | event | no | F18 — `settings.py:304` filters exactly the placeholder the repaired text quotes, unstated | open |
| advisory | `submission-evaluation.md:80` | `judgments/team-demos/judge-{frontend-ux,security-ops}.md` | event | no | F19 — both `product` rationales rewritten to hold an unchanged score after losing a stated reason. Both replacements check out; neither judge raised its score | open |

## Advisories

**Give the judgment template an amendment section.** Two judges, correcting the
same finding in the same round, invented two different places to record it and
neither is in the template. That is not a discipline failure, it is a missing
affordance, and it produced F13 in the stage that discovered W9. The fix is one
heading and a rule about what goes under it, and it belongs with W9 rather than
after it.

**The repair round is the most defect-dense part of this event, again.** Four of
this round's seven findings were introduced by the repair, matching configuration
(three of nine introduced by its own round one) and intake (three of five) and
evidence (four of six). Across four stages, every repair round on this event has
introduced defects at roughly half the rate it fixed them. That is now a
measured property of the workflow rather than an impression, and it is the
argument for scoping a re-audit at every repair rather than accepting a repair
report.

**Three figures for one fact is worse than one wrong figure.** F15 is a
pre-existing miscount that round one missed, but the repair made it visible and
worse by correcting the sibling judgment to seventeen. When a stage corrects a
number in one artifact it should grep the team's other artifacts for the same
number before it commits.

**Carry F19 and F12 into consolidation deliberately.** The consolidator will see
four `product` scores of 4 for team-demos and will not see that two of the four
rationales were rewritten after a withdrawn premise, or that several of the
strongest findings in this stage have no evidence id to trace. Both are recorded
here and neither is visible in the judgments' front matter.

## Completion gate

- [x] No blocking findings — F1 repaired and verified against the git index
- [x] No major findings — F5 repaired and verified against the commit history
- [x] Calculations valid — both `atj score` tables byte-identical to round one; no weight or total in any judgment; front matter and both `atj:scores` blocks untouched by the repair
- [x] Evidence references resolve — every corrected citation re-derived from the primary source; F14 to F16 are prose and citation-order defects, not unresolvable references
- [x] Version and identity checks pass — no front-matter field changed in any of the eight; `atj release-check` PASS
- [x] Privacy boundary passes — `public_scores: false`, `public/` empty, `atj validate publication` CLEAR, event directory clean including ignored paths
- [x] Every finding recorded in `findings:` with a `scope` and a `blocking` flag
- [ ] Approved with `atj event approve <this file>`

**PASS WITH ADVISORIES.** Nineteen findings over two rounds, twelve closed,
seven open and none blocking or major. The `judgments-audited` gate may be set on
this report. F13 to F17 should be repaired in a round-two repair and that repair
re-audited, scoped to its diff; on this event no repair round has yet been clean.
