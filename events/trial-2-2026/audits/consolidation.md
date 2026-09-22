---
event_id: trial-2-2026
audit_scope: consolidation stage, both teams, rounds one through four
audit_id: consolidation
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.1.0
persona: judging-auditor@1.1.0
framework_commit: 7ac67fbecf9a034bba577e0f6639fe428053e5c0
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-22T19:05:00Z"
completed_at: "2026-09-22T23:55:00Z"
visibility: private
approval_state: approved
validation_state: valid
result: PASS WITH ADVISORIES
findings:
- id: F1
  severity: blocking
  scope: event
  blocking: false
  summary: team-scribe attributes a single-judge finding to two judges; judge-product-agentic never mentions .env
  artifact: summaries/team-scribe.md
  repair: attribute to judge-security-ops alone; delete "separately" and the second judge id. Done and verified in round two and re-checked in round four — the report reads "one judge, uncorroborated and uncontradicted", and judge-product-agentic still contains zero occurrences of .env
  state: repaired
- id: F2
  severity: major
  scope: event
  blocking: false
  summary: the ev-demos-07 row claims the v1.1 POST guard raises for every non-local host; the run record shows one hostile form it does not raise for
  artifact: summaries/team-demos.md
  repair: restate both sites as the manifest does; the schemeless form passes the guard and is rejected by urllib
  state: repaired
- id: F3
  severity: major
  scope: event
  blocking: false
  summary: the security score relationship is inverted; judge-security-ops scored lowest, not highest
  artifact: summaries/team-demos.md
  repair: highest to lowest
  state: repaired
- id: F4
  severity: major
  scope: event
  blocking: false
  summary: three confirmed strengths present one evidence-package scan cited by four judges as four independent confirmations
  artifact: summaries/team-demos.md
  repair: attribute to the evidence package and record that all four judges cited it
  state: repaired
- id: F5
  severity: major
  scope: event
  blocking: false
  summary: PR6 attributed to judge-backend, who recorded that README passage as a strength and as a limit on novelty, not as this risk
  artifact: summaries/team-demos.md
  repair: attribute to judge-product-agentic; restate or drop judge-backend
  state: repaired
- id: F6
  severity: major
  scope: event
  blocking: false
  summary: two justified minority concerns dropped, the substring-heuristic control and the denylist sanitizer
  artifact: summaries/team-demos.md
  repair: carry both, each attributed to its single judge, and add them to Q3
  state: repaired
- id: F7
  severity: major
  scope: event
  blocking: false
  summary: secret handling recorded as confirmed by direct read, when no judge could read any .env file
  artifact: summaries/team-demos.md
  repair: scope the bullet to what was read and cross-reference D0
  state: repaired
- id: F8
  severity: major
  scope: event
  blocking: false
  summary: a conclusion only judge-security-ops drew is reported as drawn by two judges from one manifest cell
  artifact: summaries/team-scribe.md
  repair: attribute the gating conclusion to judge-security-ops and name the shared source
  state: repaired
- id: F9
  severity: major
  scope: event
  blocking: false
  summary: a two-judge evidence-backed weakness dropped, the local transcription default against a base install omitting torch and openai-whisper
  artifact: summaries/team-scribe.md
  repair: add to confirmed weaknesses
  state: repaired
- id: F10
  severity: major
  scope: event
  blocking: false
  summary: the report says several judges turned the agent-instruction surface into evidence about the submission's process, then reports none of it
  artifact: summaries/team-scribe.md
  repair: carry the finding or drop the claim
  state: repaired
- id: F11
  severity: major
  scope: event
  blocking: false
  summary: D3 omits judge-frontend-ux M1, which that judge ranks above an item D3 does carry
  artifact: summaries/team-scribe.md
  repair: add M1 to D3
  state: repaired
- id: F12
  severity: minor
  scope: event
  blocking: false
  summary: present-tense prose says the score block is unrendered while the block is filled; a declaration checkbox is ticked against its own explanation
  artifact: summaries/team-demos.md
  repair: past-tense the provenance sentences to match the section that describes what happened, and reconcile the checkbox
  state: repaired
- id: F13
  severity: minor
  scope: event
  blocking: false
  summary: same false present-tense provenance claim inside the calculation audit checklist
  artifact: summaries/team-scribe.md
  repair: restate in the past tense
  state: repaired
- id: F14
  severity: minor
  scope: event
  blocking: false
  summary: Q6 counts two open judgments-audit findings; three are open, and the same report names the third elsewhere
  artifact: summaries/team-demos.md
  repair: three, and name F21
  state: repaired
- id: F15
  severity: minor
  scope: event
  blocking: false
  summary: a third uncorrected "seven" survives in the judgment while the consolidation states the correction was complete
  artifact: judgments/team-demos/judge-security-ops.md
  repair: correct the executive assessment to seventeen as an amendment, and qualify the consolidation sentence
  state: repaired
- id: F16
  severity: minor
  scope: event
  blocking: false
  summary: a CLAUDE.md-class file surface attributed to all four judges; the submission contains none and no judgment names it
  artifact: summaries/team-demos.md
  repair: drop the clause
  state: repaired
- id: F17
  severity: minor
  scope: event
  blocking: false
  summary: ev-demos-02 cited for README section structure it does not record
  artifact: summaries/team-demos.md
  repair: move the structure claims onto the grep and the judges' reads
  state: repaired
- id: F18
  severity: minor
  scope: event
  blocking: false
  summary: a three-judge independent code reading where one judge read the submission's README instead
  artifact: summaries/team-demos.md
  repair: name the two code readers and record the third as concurring from the README
  state: repaired
- id: F19
  severity: minor
  scope: event
  blocking: false
  summary: three blocking defects attributed to judge-backend, who labels two
  artifact: summaries/team-scribe.md
  repair: restate the count
  state: repaired
- id: F20
  severity: minor
  scope: event
  blocking: false
  summary: D2 mis-summarises what the three concurring judges deducted for
  artifact: summaries/team-scribe.md
  repair: list deductions per judge
  state: repaired
- id: F21
  severity: minor
  scope: event
  blocking: false
  summary: ev-scribe-13 cited for a pipeline-stage mapping the manifest does not make
  artifact: summaries/team-scribe.md
  repair: cite the judge for the mapping and the evidence id for the counts
  state: repaired
- id: F22
  severity: minor
  scope: event
  blocking: false
  summary: two conclusions stated as verified where the method was a five-path enumeration and a static grep over src only
  artifact: summaries/team-scribe.md
  repair: state the method and drop "verified the wider absence"
  state: repaired
- id: F23
  severity: minor
  scope: event
  blocking: false
  summary: the blockers table still shows ADJ-1 and ADJ-2 deferred with no resolution artifact, contradicting the same file's team-progress table
  artifact: status.md
  repair: close both rows against their adjudication records
  state: repaired
- id: F24
  severity: minor
  scope: event
  blocking: false
  summary: one out-of-order pair in the activity log, the round-three repair row before the gate row it precedes in time
  artifact: status.md
  repair: reorder
  state: repaired
- id: F25
  severity: minor
  scope: event
  blocking: false
  summary: the consolidation ledger row and last_updated are stamped twelve minutes before the artifacts they record finished
  artifact: status.md
  repair: restamp both to the artifacts' completed_at or later
  state: repaired
- id: F26
  severity: minor
  scope: framework
  blocking: false
  summary: atj score requires an adjudication rationale only for severe disagreement, so an accepted NE can carry no machine-readable reason
  artifact: atj/scoring.py
  repair: require a rationale for any resolution that disposes of an NE
  state: deferred
- id: F27
  severity: minor
  scope: framework
  blocking: false
  summary: the agreement band and outlier detection are computed from scored judges only, so a criterion half the panel could not judge is labelled aligned and outlier detection silently switches off
  artifact: atj/scoring.py
  repair: qualify the band when NE judges exist, and record that outlier detection did not run
  state: deferred
- id: F28
  severity: advisory
  scope: event
  blocking: false
  summary: the head-to-head rule is paraphrased as "forbids deciding by the higher initial total" where the rubric says "do not merely select"
  artifact: summaries/team-scribe.md
  repair: quote the rubric
  state: repaired
- id: F29
  severity: advisory
  scope: event
  blocking: false
  summary: the adjudication's disputed-claims row misstates the basis of judge-backend's agentic score; the consolidation characterises it correctly
  artifact: adjudications/adj-trial-2-2026-team-scribe-agentic.md
  repair: correct the row by amendment, or record the discrepancy
  state: repaired
- id: F30
  severity: advisory
  scope: event
  blocking: false
  summary: template operator scaffolding retained in the shipped report, the same class the judgments audit deferred as house style
  artifact: summaries/team-demos.md
  repair: none mid-event; settle the class at the framework level
  state: accepted
- id: F31
  severity: advisory
  scope: event
  blocking: false
  summary: five further single-judge items not carried by either report
  artifact: summaries/team-demos.md
  repair: carry or record as deliberately dropped
  state: repaired
- id: F32
  severity: advisory
  scope: event
  blocking: false
  summary: a source discrepancy between two judges' line ranges for one defect is resolved by omitting the line numbers rather than recording it
  artifact: summaries/team-scribe.md
  repair: record both ranges
  state: repaired
- id: F33
  severity: advisory
  scope: event
  blocking: false
  summary: D0 propagates the judgments audit's "different methods, no shared wording" where both judges describe the same two tools
  artifact: summaries/team-demos.md
  repair: qualify when repeating the prior audit's wording
  state: repaired
- id: F34
  severity: advisory
  scope: event
  blocking: false
  summary: both reports enumerate exploitable weaknesses in third-party repositories at exact file and line; the disclosure question reaches the dossier stage undecided
  artifact: summaries/team-demos.md
  repair: settle disclosure with the event director before the dossier stage
  state: accepted
- id: N1
  severity: blocking
  scope: event
  blocking: false
  summary: the repair said _last_flushed_count is never read; recorder.py:349 reads it, and the judge had written "logged but never used to make the write incremental"
  artifact: summaries/team-scribe.md
  repair: restore the judge's formulation. Done and verified in round three against the pin — recorder.py:344 joins all of current_frames, :346 sets _last_flushed_count and :349 reads it in the log call and nowhere else
  state: repaired
- id: N2
  severity: major
  scope: event
  blocking: false
  summary: the repair invented the directory src/gui/widgets/, which does not exist at the pin
  artifact: summaries/team-scribe.md
  repair: correct to src/gui/main_window/animated_button.py
  state: repaired
- id: N3
  severity: major
  scope: event
  blocking: false
  summary: the D2 rewrite turned a largely shared deduction set into three disjoint ones; all three judges deduct for the public KDF input and the two environment-read constructors
  artifact: summaries/team-scribe.md
  repair: shared deductions once, then each judge's addition
  state: repaired
- id: N4
  severity: major
  scope: event
  blocking: false
  summary: the annotation written to justify not reordering the ledger was false on both claims; audits/judgments.md carries an exact completed_at of 14:17:00Z
  artifact: status.md
  repair: restamp from the artifact and order by stamp
  state: repaired
- id: N5
  severity: major
  scope: event
  blocking: false
  summary: the repair round left no activity-log row, so the stage's re-audit had no ledger anchor
  artifact: status.md
  repair: add the row and derive last_updated from it
  state: repaired
- id: N6
  severity: major
  scope: event
  blocking: false
  summary: the F2 repair undercounted the egress guard at two raises; the run record shows three of five, including the protocol-relative form
  artifact: summaries/team-demos.md
  repair: state three of five and name the form that never reaches the guard
  state: repaired
- id: N7
  severity: major
  scope: event
  blocking: false
  summary: PD18 was added from an unverified advisory and no team-demos judgment supports it; the source records the point as unscored inference from the generator only
  artifact: summaries/team-demos.md
  repair: removed before re-audit, with Q3 corrected
  state: repaired
- id: N8
  severity: minor
  scope: event
  blocking: false
  summary: eight statements across both summaries drawn stronger than their source, or left with a broken antecedent, by isolated edits
  artifact: summaries/team-scribe.md
  repair: restore each source's scope and qualifier
  state: repaired
- id: N9
  severity: minor
  scope: event
  blocking: false
  summary: the F18 repair left the clause it replaced in place beside its replacement
  artifact: summaries/team-demos.md
  repair: delete the duplicate
  state: repaired
- id: N10
  severity: minor
  scope: event
  blocking: false
  summary: '''unchanged'' from a re-render proves the block matches renderer output, not that nobody transcribed it; the inference was asserted at three sites'
  artifact: summaries/team-demos.md
  repair: state what the check establishes
  state: repaired
- id: N11
  severity: minor
  scope: event
  blocking: false
  summary: the amendment cross-referenced a D-series defect for the empty-hostname point, which is K4 under risks
  artifact: judgments/team-demos/judge-security-ops.md
  repair: cite K4
  state: repaired
- id: N12
  severity: minor
  scope: framework
  blocking: false
  summary: consolidated reports have no amendment form either, so a panel report rewritten after its audit still carries the audited version's completed_at and framework_commit
  artifact: schemas/consolidated-report.schema.json
  repair: one amendment form for every artifact class, with W12
  state: deferred
- id: P1
  severity: major
  scope: event
  blocking: false
  summary: the D2 rewrite has all three judges deducting for the public KDF input; judge-backend calls that property defensible and names its deductions as documentation accuracy and a secondary key path. N3's own finding text carried the same error and the repair inherited it
  artifact: summaries/team-scribe.md
  repair: shared items once, then the KDF input as a deduction for two of the three with judge-backend's position stated
  state: repaired
- id: P2
  severity: major
  scope: event
  blocking: false
  summary: the escaping defect's two line ranges are recorded as verified by the judgments stage audit; audits/judgments.md contains no reference to render.py, to either range, to SECURITY.md or to escaping
  artifact: summaries/team-scribe.md
  repair: state what was checked and against what, not who checked it
  state: repaired
- id: P3
  severity: major
  scope: event
  blocking: false
  summary: product, agentic and innovation called the three criteria scored highest; security at 3.75 outranks agentic at 3.5 on the mean and is at or above it on every judge's card
  artifact: summaries/team-demos.md
  repair: drop the ranking clause; the confidence point does not need it
  state: repaired
- id: P4
  severity: minor
  scope: event
  blocking: false
  summary: the same D2 sentence has the two service constructors bypassing the keyring and the encrypted store, dropping the condition all three judges state
  artifact: summaries/team-scribe.md
  repair: carry the condition from the code and the judgments
  state: repaired
- id: P5
  severity: minor
  scope: event
  blocking: false
  summary: the PR6 addition restates judge-frontend-ux's position a second time in the same bullet, which is N9 recurring
  artifact: summaries/team-demos.md
  repair: delete the duplicate
  state: repaired
- id: P6
  severity: minor
  scope: event
  blocking: false
  summary: N10 was scoped to three sites in team-demos; the parallel calculation-audit checkbox in team-scribe still offers the re-render as evidence of who wrote the block
  artifact: summaries/team-scribe.md
  repair: apply the team-demos formulation to the fourth site
  state: repaired
- id: P7
  severity: minor
  scope: event
  blocking: false
  summary: the round-two ledger row records 5 major and 6 minor introduced; the front matter carries 6 major (N2-N7) and 5 minor (N8-N12)
  artifact: status.md
  repair: transpose
  state: repaired
- id: P8
  severity: minor
  scope: event
  blocking: false
  summary: the round-two section and its ledger row both say all twelve N findings are repaired while N12 carries state deferred
  artifact: audits/consolidation.md
  repair: eleven repaired, N12 deferred to W12
  state: repaired
- id: P9
  severity: advisory
  scope: event
  blocking: false
  summary: the round-two Result paragraph subtracts the two framework deferrals from the thirty-two event-scope findings, which contradicts the thirty-of-thirty-two the same round states below
  artifact: audits/consolidation.md
  repair: state the two counts separately
  state: repaired
- id: P10
  severity: advisory
  scope: event
  blocking: false
  summary: a wrong D3 count was replaced by "most of them" where all eight rest on static reads with no evidence id, and the fix widened the judging audit's verification from three items to eight
  artifact: summaries/team-scribe.md
  repair: all eight, and attribute the class rather than each item
  state: repaired
approved_by: event-director
approved_at: "2026-09-22T21:09:58Z"
approval_note: Four rounds; 56 findings, 51 repaired, 2 accepted, 3 deferred to 0.5.0-beta, none open.
---

# Consolidation Audit — both teams, first pass

## Result

**FAIL**, superseded in place after round two. Round one: thirty-two
event-scope findings — one blocking, ten major, fourteen minor, seven advisory —
plus two framework-scope findings, `F26` and `F27`. Round two, scoped to the
repair diff: thirty of the thirty-two repaired, the other two accepted, both
framework-scope findings deferred, and **twelve new defects the repair itself
introduced**, one of them blocking. Eleven of the twelve are repaired, `N12` is
deferred to the framework, and none has been re-audited, so the gate stays shut
and round three is the remaining work.

Round one's original text follows unchanged below. The round-two record is the
section after it.

**FAIL.** One blocking finding, ten major, fourteen minor, seven advisory.

Every number in this stage is correct. `atj score` reproduces both panels field
for field, `atj render consolidated` rewrites both score blocks to byte-identical
output, and neither report carries an official total. The stage fails on prose:
the consolidated reports state evidentiary weight the judgments do not carry.
One of those statements invents a second judge for a finding one judge made,
which is the class the judgments-stage audit rated blocking at its own F1.

Ten of the eleven blocking-or-major findings are attribution and coverage
defects of the same family — a claim credited to more judges than made it, a
shared evidence-package scan counted as independent confirmation, or a
single-judge concern dropped. The consolidation policy names both failures
directly: repeated wording is not independent confirmation, and justified
minority concerns must be preserved.

## Scope and artifacts inspected

| Artifact | What was checked |
|---|---|
| `summaries/team-demos.md`, `summaries/team-scribe.md` | every claim traced to a judgment or a cited artifact; all evidence-index rows; 44 inline citations resolved against the pinned checkouts |
| `summaries/team-demos.json`, `summaries/team-scribe.json` | diffed field for field against a fresh `atj score --json` |
| `judgments/team-{demos,scribe}/judge-*.md`, eight files | source of every attribution; independence; front-matter identity |
| `adjudications/adj-trial-2-2026-team-{demos,scribe}-*.md` | authority, citations, effect on the total |
| `evidence/team-*/manifest.md`, 11 run records | every evidence id the summaries cite |
| `audits/judgments.md` | carry-forward accuracy of the prior stage's 22 findings |
| `status.md` | ledger integrity, gate state, blocker table |
| `framework/rubrics/panel-consolidation.md`, `submission-evaluation.md`, `head-to-head.md`; `framework/personas.md`; `atj/scoring.py`, `atj/render.py` | the policies the reports are measured against |

Out of scope: the bracket, which is `status: not-built` and correctly so;
`atj bracket verify --reproduce` has nothing to verify at this stage.

## Deterministic validation results

| Command | Result |
|---|---|
| `python3 -m atj event validate events/trial-2-2026` | PASS, 0 problems, stage consolidation |
| `python3 -m atj validate reports events/trial-2-2026` | PASS, 20 artifacts, 0 blocking, 0 major, 0 minor, 0 advisory |
| `python3 -m atj validate publication events/trial-2-2026` | CLEAR, 20 artifacts, 0 blocking |
| `python3 -m atj release-check` | PASS |
| `python3 -m atj personas` | PASS, 15 agents |
| `atj score events/trial-2-2026/judgments/team-demos --json` vs the committed JSON | identical, every field |
| `atj score events/trial-2-2026/judgments/team-scribe --json` vs the committed JSON | identical, every field |
| `atj render consolidated` against both reports | `unchanged` for both; `git diff` empty, then restored |

Both panels: `total: null`, `finalized: false`, `adjudication_required: []`,
`integrity_problems: []`, `withheld_authority: []`. Provisional sums 52.50 and
32.50, labelled not-official at all eight places either report mentions them.
No judge score was replaced or adjusted; `source_scores` in both blocks match
the eight judgments' front matter.

`atj validate reports` returning zero findings over these same 20 artifacts is
the expected result and not evidence the reports are sound. It checks shape and
arithmetic. Every finding below is a statement about what a source says, which
no validator reads.

## The finding that holds the gate

`summaries/team-scribe.md:218-221`:

> `judge-product-agentic` and `judge-security-ops` separately record that
> `README.md` recommends an installer that writes a key into `.env` twelve lines
> before stating that keys are never stored there

`judgments/team-scribe/judge-product-agentic.md` contains the string `.env`
zero times. The finding exists once in the panel, at
`judgments/team-scribe/judge-security-ops.md:97`, which is where the phrase
"twelve lines later" comes from. The word "separately" asserts independent
corroboration that does not exist, on a documentation-contradiction finding that
carries into the team's dossier.

This is blocking because the consolidated report is the stage's deliverable and
the dossier stage consumes it. A reader cannot tell a two-judge finding from a
one-judge finding by looking, and the report has removed the only signal that
would let them. The judgments-stage audit rated the same class blocking.

## Arithmetic and provenance

The one thing this stage most needed to get right, it did. Both score blocks
were generated, not transcribed: re-running `atj render consolidated` against
both files reports `unchanged` and leaves an empty `git diff`. Both JSON
artifacts are byte-equivalent to a fresh `atj score --json`. The two accepted
`NE`s are recorded as dispositioned rather than cleared, `resolved_score: NE` in
both, and no source score moved.

Both reports then misdescribe that provenance in the present tense — team-demos
says the marker region "is left exactly as the template ships it", team-scribe
says the block "is left as the template ships it, unrendered" — while the blocks
are filled and the front matter is populated. team-demos describes the true
sequence correctly forty lines later. The numbers are sound and the attestation
is wrong about itself (F12, F13).

## The NE disposition

Both adjudications are well-formed, approved by the event director, and correct
on the substance: the `NE`s rest on what the frozen evidence package does not
contain, not on a judgment about the submission. Every line citation in the
team-demos adjudication resolves — `submission-evaluation.md:36`, `event.md:88-90`.
Its `head-to-head.md:12` citation resolves to real text that is slightly weaker
than the paraphrase (F28); the conclusion drawn from it is unaffected, because
no total exists to misuse.

Neither adjudication fills `score_override.rationale`, which the schema defines.
`atj/scoring.py:403` demands a rationale only when the resolution settles a
severe disagreement, so both passed. The reasoning exists in prose and in no
field a tool reads (F26).

## Agreement labelling under NE

`functional` for team-demos is 3, `NE`, 3, `NE`. `agentic` for team-scribe is 2,
`NE`, 3, `NE`. Both are labelled `aligned`. `atj/scoring.py:184` computes the
band from the scored values alone, so half a panel being unable to judge does
not reach the label, and `atj/scoring.py:193` returns no outliers below three
values, so outlier detection switched itself off on exactly the two criteria
that needed the most scrutiny. `minimum_panel: 2` is enforced against the count
of judgment files, not against valid scores per criterion.

Both consolidated reports caught this in prose and said so plainly — team-demos
heads the section "labelled `aligned`, and the label is misleading". The reports
are right and the tool is silent (F27).

## Neutrality

The consolidator did not move a score, and both reports declare it. On the
prose the record is worse. Beyond F1, three team-demos strengths present a
single evidence-package scan as four independent confirmations (F4); a risk is
credited to a judge who recorded the same passage as a strength (F5); a
conclusion one judge drew is reported as drawn by two (F8). In the other
direction, four judged concerns were dropped — two in team-demos (F6), one
two-judge weakness in team-scribe (F9), and the frontend judge's own
highest-ranked major issue omitted from the section that exists to hold it (F11).
team-scribe also claims a process finding two judges made and then never states
it (F10).

The pattern runs one way. Corroboration is inflated and single-judge concerns
thin out. That is the specific bias the neutral-packager rule exists to prevent.

## Evidence integrity

One security claim is stronger than its evidence. `summaries/team-demos.md:320`
and the `ev-demos-07` row at `:854` say the v1.1 parser guard raises "for every
non-local host". `runs/team-demos-egress-guards-01.json` shows the POST guard
exercised against five forms, raising `RuntimeError` for three; the schemeless
form `evil.example/collect` never reaches the guard and is rejected by `urllib`
with `ValueError`. The adjacent `ev-demos-08` row states this correctly, and the
report's own PD3 is about that hole. Two index rows contradict each other and
the stronger one is the security claim (F2).

Two more absences are reported as verified when the method could not establish
them. team-demos records correct secret handling "by direct read" when the
judging environment refuses `.env*` paths and no judge read one — the same
blindness the report itself carries at D0 as the cause of a withdrawn defect
(F7). team-scribe states a verified wider absence of quality gates from a
five-filename enumeration, and a verified single-provider egress surface from a
static grep scoped to `src/` (F22). Both conclusions are true at the pin; the
stated basis is narrower than the claim. This is the third stage of this event
at which tool blindness has been written down as observed fact.

## Ledger

`status.md` carries the consolidation correctly in its team-progress table and
its activity log, and contradicts itself in its blocker table, where ADJ-1 and
ADJ-2 still read "deferred to consolidation by decision" with no resolution
artifact although both were resolved and approved (F23). One activity-log pair
is out of chronological order (F24), and the consolidation row and `last_updated`
are stamped twelve minutes before the artifacts they record finished (F25). All
three are the classes the configuration and judgments audits already caught once
each; none changes what happened.

## Findings

| Severity | Rule | Artifact | Scope | Blocking | Finding | Required repair |
|---|---|---|---|---|---|---|
| blocking | neutral packager | `summaries/team-scribe.md:218-221` | event | yes | F1. "`judge-product-agentic` and `judge-security-ops` separately record" a `.env` documentation contradiction. `judge-product-agentic.md` contains `.env` zero times; the finding exists once, at `judge-security-ops.md:97` | attribute to `judge-security-ops` alone; delete "separately" and the second judge id |
| major | evidence support | `summaries/team-demos.md:320,:854` | event | no | F2. "the v1.1 parser guard raising for every non-local host". The run record shows five forms, three raised; `evil.example/collect` reaches `urllib`, not the guard. `ev-demos-08` at `:855` says so | restate both sites as the manifest does |
| major | evidence support | `summaries/team-demos.md:140` | event | no | F3. "the judge scoring highest on `security` (`judge-security-ops`, 3)". That judge scored lowest against three at 4; `:311` and `:313` say so correctly | highest to lowest |
| major | evidence synthesis | `summaries/team-demos.md:365-379` | event | no | F4. Three strengths cite one evidence-package scan and credit "All four"; three judges say in their own reports that the scan is the package's | attribute to the package; record that all four cited it |
| major | evidence support | `summaries/team-demos.md:570-576` | event | no | F5. PR6 credited to `judge-backend`, who cites that README passage as a strength under `product` and as a novelty limit under `innovation`; his risk list has no drift risk | attribute to `judge-product-agentic`; restate or drop `judge-backend` |
| major | minority concerns | `summaries/team-demos.md` | event | no | F6. `judge-frontend-ux`'s substring-heuristic control finding and `judge-product-agentic`'s denylist-sanitizer deficiency appear nowhere; both are scored deficiencies | carry both, attributed singly; add to Q3 |
| major | evidence support | `summaries/team-demos.md:420-425` | event | no | F7. "Secret handling is correct … by direct read", where the environment refuses `.env*` and `judge-frontend-ux.md:96` states no claim can be made about contents | scope to what was read; cross-reference D0 |
| major | evidence synthesis | `summaries/team-scribe.md:172-173` | event | no | F8. "both note this means the suite is fast enough to gate on". Only `judge-security-ops.md:183` draws it; `judge-product-agentic.md:180` draws a different conclusion from the same manifest cell | attribute singly; name the shared source |
| major | minority concerns | `summaries/team-scribe.md` | event | no | F9. `settings.py:31` defaulting transcription to `local` while the base install omits `torch` and `openai-whisper` — two judges, evidence-backed, uncontradicted — is absent from weaknesses, D3 and improvements | add to confirmed weaknesses |
| major | evidence support | `summaries/team-scribe.md:75-78` | event | no | F10. Claims several judges turned the agent-instruction surface into evidence about the submission's process, then reports none of it, and points at "corrected text" it does not use | carry the finding or drop the claim |
| major | minority concerns | `summaries/team-scribe.md:314-352` | event | no | F11. D3 omits `judge-frontend-ux` M1, invisible service-initialisation failure, which that judge ranks above the M3 item D3 does carry | add M1 to D3 |
| minor | provenance | `summaries/team-demos.md:97-101,:692-694,:896` | event | no | F12. Present-tense claim that the marker region is unfilled, contradicting the filled block and `:896-902`; a declaration checkbox ticked against its own explanation | past-tense both sentences; reconcile the checkbox |
| minor | provenance | `summaries/team-scribe.md:83-86,:494-495` | event | no | F13. Same false present-tense claim inside the calculation audit | restate in the past tense |
| minor | accuracy | `summaries/team-demos.md:805` | event | no | F14. Q6 says two judgments-audit findings were open; three are, and `:797` and `:873` name the third | three, and name F21 |
| minor | carry-forward | `judgments/team-demos/judge-security-ops.md:49`, `summaries/team-demos.md:468` | event | no | F15. A third uncorrected "seven" for the `Bash(rm:*)` count survives in the executive assessment while the consolidation states the correction was complete. Seventeen is exact | amend the judgment; qualify the consolidation |
| minor | evidence support | `summaries/team-demos.md:594-596` | event | no | F16. A `CLAUDE.md`-class file surface credited to all four judges; the submission contains none and no judgment names it | drop the clause |
| minor | citation | `summaries/team-demos.md:198-203,:387-391` | event | no | F17. `ev-demos-02` cited for README section structure; the manifest entry records counts only. The facts hold at the pin from other sources | move the claims onto the grep and the reads |
| minor | evidence synthesis | `summaries/team-demos.md:398-403` | event | no | F18. Three judges credited with reading the same code "independently"; `judge-frontend-ux.md:108` cites the submission's README | name the two code readers; record the third as concurring |
| minor | accuracy | `summaries/team-scribe.md:423-424` | event | no | F19. "two of judge-backend's three blocking defects"; he labels two | restate the count |
| minor | evidence support | `summaries/team-scribe.md:281-285` | event | no | F20. D2's summary of the three concurring judges' deductions matches neither `judge-frontend-ux` nor `judge-product-agentic` | list deductions per judge |
| minor | citation | `summaries/team-scribe.md:127-129` | event | no | F21. `ev-scribe-13` cited for a four-stage pipeline mapping; the manifest records counts and package names. The mapping is `judge-backend`'s inference | cite the judge for the mapping |
| minor | evidence support | `summaries/team-scribe.md:64,:194-197` | event | no | F22. A "wider absence" of quality gates verified by enumerating five filenames, and a "verified" egress surface from a static grep scoped to `src/`. Both conclusions hold; the basis is narrower | state the method; drop "verified the wider absence" |
| minor | ledger | `status.md:50-51` | event | no | F23. ADJ-1 and ADJ-2 still read "deferred to consolidation by decision", resolution artifact "—", though both were resolved and approved at 18:07:45Z and the team-progress table records the acceptance | close both rows against their adjudication records |
| minor | ledger | `status.md` activity log | event | no | F24. One out-of-order pair: the 14:22:00Z round-three repair row precedes the 14:19:58Z gate row | reorder |
| minor | ledger | `status.md:93`, `last_updated` | event | no | F25. The consolidation row and `last_updated` are 18:40:00Z; the artifacts they record carry `completed_at: 18:52:00Z` | restamp to the artifacts' completion or later |
| minor | tooling | `atj/scoring.py:403` | framework | no | F26. A rationale is required only when a resolution settles a severe disagreement, so an accepted `NE` can carry none. Both adjudications here omit `score_override.rationale`; the reasoning lives only in prose | require a rationale for any resolution disposing of an `NE` |
| minor | tooling | `atj/scoring.py:184,:193` | framework | no | F27. The agreement band is computed from scored judges only, so a criterion half the panel could not judge is labelled `aligned`; `_outliers` returns nothing below three values, disabling outlier detection on exactly those criteria. `minimum_panel` is checked against judgment files, not valid scores per criterion | qualify the band when `NE` judges exist; record that outlier detection did not run |
| advisory | citation | `summaries/team-scribe.md:237,:383` | event | no | F28. "`head-to-head.md` forbids deciding a matchup by the higher initial total"; `head-to-head.md:12` says "Do not merely select". No consequence here, but the bracket stage inherits the paraphrase | quote the rubric |
| advisory | evidence support | `adjudications/adj-trial-2-2026-team-scribe-agentic.md` | event | no | F29. The disputed-claims row says `judge-backend` scored `agentic` from the development-time agent configuration; his finding rests on `ev-scribe-11` and source reads of the runtime path. D1 of the consolidation gets it right | correct by amendment or record the discrepancy |
| advisory | house style | `summaries/team-demos.md:86-94` | event | no | F30. Template operator scaffolding retained in the shipped report; the judgments carry the equivalent, so this is the deferred W9 class | settle at the framework level, not mid-event |
| advisory | minority concerns | `summaries/team-demos.md`, `summaries/team-scribe.md` | event | no | F31. Five further single-judge items not carried: the unlabelled medal emoji, an uncredited team validation claim, the recording animation and reduced-motion gap, working-directory-relative icon paths, and the quadratic checkpoint flush that was one judge's highest-value improvement | carry or record as deliberately dropped |
| advisory | citation | `summaries/team-scribe.md:217` | event | no | F32. Two judges give different line ranges for one defect; the consolidation drops the line numbers rather than recording the discrepancy | record both ranges |
| advisory | carry-forward | `summaries/team-demos.md:619-621` | event | no | F33. D0 repeats the judgments audit's "different methods with no shared wording" where both judges describe the same two tools | qualify when repeating prior wording |
| advisory | disclosure | `summaries/team-demos.md`, `summaries/team-scribe.md` | event | no | F34. Both reports enumerate exploitable weaknesses in third-party repositories at exact file and line. `event.md:14` sets `public_scores: false` and the publication gate has not run; the question reaches the dossier stage undecided | settle disclosure with the event director before the dossier stage |

## Advisories

Beyond the advisory findings above, three observations carry no repair.

The two reports are structurally different by choice. team-demos adds a
per-criterion agreement analysis and a blocking-issues section the template does
not require; team-scribe matches `framework/templates/consolidated-team-report.md`
exactly. Both satisfy the policy's required sections. The asymmetry is worth a
decision before the dossier stage reads them, not a repair.

Both summaries ship `approval_state: draft` and `validation_state: unvalidated`.
So did live-trial-2026's through completion, so this matches practice and is not
a finding, but nothing in the framework moves a consolidated report to approved
and nothing requires it to be.

Privacy is clean on both reports. No real personal identity, no host path, no
credential, no repository identity in either summary or either adjudication.
`events/trial-2-2026/public/` holds only `.gitkeep`, and `atj validate publication`
is CLEAR over all 20 artifacts. The `/home/gregg/...` volume paths in the run
records stay inside private artifacts and are quoted into nothing.

## Completion gate

- [ ] No blocking findings
- [ ] No major findings
- [x] Calculations valid
- [ ] Evidence references resolve
- [x] Version and identity checks pass
- [x] Privacy boundary passes
- [x] Every finding recorded in `findings:` with a `scope` and a `blocking` flag
- [ ] Approved with `atj event approve <this file>`

**FAIL.** F1 is `blocking: true` and holds `consolidation-audited`. The ten major
findings do not hold the gate mechanically, and they must still be repaired and
re-audited before the dossier stage reads these reports, because every one of
them is a statement about evidentiary weight that a dossier would inherit.

## Round two — the repair audited

Scope: `git diff 5b4c0ac..4ce5cbb` over both summaries, the amended judgment, both
adjudications and `status.md`, plus the working-tree delta that removed PD18.
Arithmetic was excluded and separately re-verified: `atj score` regenerated both
JSON artifacts and they reproduce identically, and `atj render consolidated`
reports `unchanged` on both reports.

Thirty of the thirty-two round-one findings are repaired. `F26` and `F27` are
deferred to `docs/0.5.0-beta-plan.md` (W10 extended, W14 added) rather than
changing `atj/scoring.py` while a stage's artifacts are already written. `F30`
and `F34` are accepted: the template scaffolding is a framework-level question,
and disclosure is the event director's call before the dossier stage.

Twelve defects were introduced by the repair, `N1` through `N12` in the front
matter. The pattern is worth stating, because it is the same one round one
found. Three of the twelve are claims drawn stronger than their source —
`N1` deleted a judge's qualifier and produced a statement the code disproves,
`N3` turned shared deductions into disjoint ones, `N7` promoted an explicitly
unscored inference to a confirmed, directly-read, scored deficiency. `N2` and
`N6` are worse in kind: a citation to a directory that does not exist at the
pin, and a restatement of the egress evidence that undercounted the control it
was correcting. `N4` is a false annotation written to justify declining a
repair. Four are antecedents and counts broken by editing sentences in
isolation.

`N7` was caught during the round rather than by the re-audit: PD18 was added to
team-demos from an unverified advisory, and no team-demos judgment mentions a
medal, an emoji, `aria-hidden` or a screen reader. It was removed and the Q3
enumeration corrected before the re-audit reported. The removal is recorded in
the activity log; nothing else in the report depended on it.

Every `N` finding but `N12` is repaired in the working tree; `N12` is framework
scope and is deferred to `docs/0.5.0-beta-plan.md` W12, which the round-two
commit extended. None of the repairs has been verified by a subsequent audit,
and `CLAUDE.md` does not permit advancing on that basis. The gate stays
`pending` until round three checks the round-two repairs, which is the only work
this stage still owes.

## Round three — the round-two repair audited

Scope: `git diff 4ce5cbb..a8cbc9b` over both summaries, both adjudications, the
amended `judge-security-ops` judgment for team-demos, `status.md` and
`docs/0.5.0-beta-plan.md`. Arithmetic was excluded: `atj score` reproduces both
JSON artifacts identically and `atj render consolidated` reports `unchanged` on
both reports, before and after this round's repair.

Method, before reading the reports' prose so their framing could not set the
expectation: every citation the round-two commit added or moved was resolved
against the pinned checkouts at `dc35f696` and `67969dd9`, and every attributed
claim it rewrote was grepped across all four judgments for that team and the
hitting files counted. Confidence and score claims were checked against the
eight judgments' front matter rather than against either report.

Eleven of the twelve `N` repairs land and their new text is true against the
primary source. `N1` restores what `recorder.py:344-350` shows — the flush joins
all of `current_frames`, and `_last_flushed_count` is set at `:346` and read at
`:349` by the log call and nowhere else. `N2`'s corrected path
`src/gui/main_window/animated_button.py` is tracked at the pin, and the report
now separates the two icon citations from `:246`, which is the font directory
the judge's own range swept in. `N6` and the matching judgment amendment match
`runs/team-demos-egress-guards-01.json` exactly: five forms, three
`RuntimeError`s, the bare `evil.example/collect` rejected by `urllib`. `N4`'s
restamp to `14:17:00Z` is the `completed_at` of `audits/judgments.md`. `N7`'s
removal of `PD18` is complete — no `PD18`, medal, emoji or screen-reader text
survives in either report, and the `Q3` enumeration matches the sections. `N11`
cites `K4`, which is where that judgment puts the empty-hostname point.

Ten defects, `P1` through `P10` in the front matter, none blocking. Three are
major and all three are the mechanism this event keeps producing. `P1` is the
sharpest: `N3`'s own finding text asserted that all three judges deduct for the
public KDF input, the repair wrote that faithfully, and `judge-backend` calls
that property "defensible for this class of application" and names its
deductions as documentation accuracy and a secondary key path. A repair round
inherited a wrong premise from the audit that commissioned it. `P2` is invented
provenance of the kind `F1` was: the two line ranges for the escaping defect are
credited to the judgments stage audit, and `audits/judgments.md` contains no
reference to `render.py`, to either range, to `SECURITY.md` or to escaping. `P3`
is a false ranking introduced into the one sentence `F3` had already corrected
once. `P5` is `N9` recurring in a different bullet, and `P6` is `N10` applied to
one report and not the other. The remainder are counts: the ledger row transposes
the round's own major and minor totals, and two places call all twelve `N`
findings repaired while `N12` is deferred.

Coverage did not regress. The round-two commit removed one item, `PD18`, which
no judgment supported; every other bullet, weakness and minority finding either
report carried before the commit is still there.

## Round four — the round-three repair audited

Scope: the round-three repair diff over `summaries/team-demos.md`,
`summaries/team-scribe.md`, `status.md` and this file. `atj score` reproduces
both JSON artifacts identically and `atj render consolidated` reports `unchanged`
on both reports after the repair; the four repository validators pass over 21
artifacts.

All ten `P` repairs verified against the primary source. The rewritten `D2`
paragraph now matches all three judgments: the two constructors at
`whisper_service.py:92-96` and `summarizer.py:50-54` prefer the settings manager
and fall back to `OPENAI_API_KEY`, which is what the code does and what all
three judges say; the unsalted legacy derivation at `:393` is recorded by all
three; the KDF input is a deduction for two, with `judge-backend`'s own position
stated in its own terms. Both escaping ranges were re-resolved at the pin and
fall inside `markdown_to_html`, which spans `:241-278`.

Two defects were caught inside the round rather than by a later one. The first
`D2` draft said the constructors read the environment "only when none is
supplied", which is narrower than the code — the fallback also fires when the
manager returns no key. The second widened the judging audit's `F12` from the
class it recorded to each of the eight `D3` items individually; the lead-in now
attributes the class. Both were corrected before this round reported, and both
are the same compression mechanism, which is worth recording rather than hiding:
four rounds in, no repair in this stage has been written without introducing
something, and the only round that produced no surviving defect is the one that
audited its own draft before publishing it.

One timing note, recorded rather than smoothed over. The times this stage has
carried since the round-two audit are reconstructed and run ahead of this
environment's clock, so `approved_at` — the one stamp a tool wrote, `21:09:58Z` —
precedes this file's reconstructed `completed_at` of `23:55:00Z`. The ordering
inside the reconstruction is consistent and the approval is the later event in
fact. This is the `F20`/`N4` class and it is called out here because the next
stage should not read the two stamps as a sequence.

Nothing is open. Thirty of the thirty-four round-one findings are repaired, two
accepted, two deferred to the framework; eleven of the twelve round-two findings
are repaired and `N12` deferred; all ten round-three findings are repaired. No
raw score moved in any round, neither panel carries an official total, and the
`NE` dispositions are unchanged. **PASS WITH ADVISORIES** — the gate may be set.
