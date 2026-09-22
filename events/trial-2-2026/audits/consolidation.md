---
event_id: trial-2-2026
audit_scope: consolidation stage, both teams, first pass
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
completed_at: "2026-09-22T20:02:00Z"
visibility: private
approval_state: draft
validation_state: unvalidated
result: FAIL
findings:
  - id: F1
    severity: blocking
    scope: event
    blocking: true
    summary: team-scribe attributes a single-judge finding to two judges; judge-product-agentic never mentions .env
    artifact: summaries/team-scribe.md
    repair: attribute to judge-security-ops alone; delete "separately" and the second judge id
    state: open
  - id: F2
    severity: major
    scope: event
    blocking: false
    summary: the ev-demos-07 row claims the v1.1 POST guard raises for every non-local host; the run record shows one hostile form it does not raise for
    artifact: summaries/team-demos.md
    repair: restate both sites as the manifest does; the schemeless form passes the guard and is rejected by urllib
    state: open
  - id: F3
    severity: major
    scope: event
    blocking: false
    summary: the security score relationship is inverted; judge-security-ops scored lowest, not highest
    artifact: summaries/team-demos.md
    repair: highest to lowest
    state: open
  - id: F4
    severity: major
    scope: event
    blocking: false
    summary: three confirmed strengths present one evidence-package scan cited by four judges as four independent confirmations
    artifact: summaries/team-demos.md
    repair: attribute to the evidence package and record that all four judges cited it
    state: open
  - id: F5
    severity: major
    scope: event
    blocking: false
    summary: PR6 attributed to judge-backend, who recorded that README passage as a strength and as a limit on novelty, not as this risk
    artifact: summaries/team-demos.md
    repair: attribute to judge-product-agentic; restate or drop judge-backend
    state: open
  - id: F6
    severity: major
    scope: event
    blocking: false
    summary: two justified minority concerns dropped, the substring-heuristic control and the denylist sanitizer
    artifact: summaries/team-demos.md
    repair: carry both, each attributed to its single judge, and add them to Q3
    state: open
  - id: F7
    severity: major
    scope: event
    blocking: false
    summary: secret handling recorded as confirmed by direct read, when no judge could read any .env file
    artifact: summaries/team-demos.md
    repair: scope the bullet to what was read and cross-reference D0
    state: open
  - id: F8
    severity: major
    scope: event
    blocking: false
    summary: a conclusion only judge-security-ops drew is reported as drawn by two judges from one manifest cell
    artifact: summaries/team-scribe.md
    repair: attribute the gating conclusion to judge-security-ops and name the shared source
    state: open
  - id: F9
    severity: major
    scope: event
    blocking: false
    summary: a two-judge evidence-backed weakness dropped, the local transcription default against a base install omitting torch and openai-whisper
    artifact: summaries/team-scribe.md
    repair: add to confirmed weaknesses
    state: open
  - id: F10
    severity: major
    scope: event
    blocking: false
    summary: the report says several judges turned the agent-instruction surface into evidence about the submission's process, then reports none of it
    artifact: summaries/team-scribe.md
    repair: carry the finding or drop the claim
    state: open
  - id: F11
    severity: major
    scope: event
    blocking: false
    summary: D3 omits judge-frontend-ux M1, which that judge ranks above an item D3 does carry
    artifact: summaries/team-scribe.md
    repair: add M1 to D3
    state: open
  - id: F12
    severity: minor
    scope: event
    blocking: false
    summary: present-tense prose says the score block is unrendered while the block is filled; a declaration checkbox is ticked against its own explanation
    artifact: summaries/team-demos.md
    repair: past-tense the provenance sentences to match the section that describes what happened, and reconcile the checkbox
    state: open
  - id: F13
    severity: minor
    scope: event
    blocking: false
    summary: same false present-tense provenance claim inside the calculation audit checklist
    artifact: summaries/team-scribe.md
    repair: restate in the past tense
    state: open
  - id: F14
    severity: minor
    scope: event
    blocking: false
    summary: Q6 counts two open judgments-audit findings; three are open, and the same report names the third elsewhere
    artifact: summaries/team-demos.md
    repair: three, and name F21
    state: open
  - id: F15
    severity: minor
    scope: event
    blocking: false
    summary: a third uncorrected "seven" survives in the judgment while the consolidation states the correction was complete
    artifact: judgments/team-demos/judge-security-ops.md
    repair: correct the executive assessment to seventeen as an amendment, and qualify the consolidation sentence
    state: open
  - id: F16
    severity: minor
    scope: event
    blocking: false
    summary: a CLAUDE.md-class file surface attributed to all four judges; the submission contains none and no judgment names it
    artifact: summaries/team-demos.md
    repair: drop the clause
    state: open
  - id: F17
    severity: minor
    scope: event
    blocking: false
    summary: ev-demos-02 cited for README section structure it does not record
    artifact: summaries/team-demos.md
    repair: move the structure claims onto the grep and the judges' reads
    state: open
  - id: F18
    severity: minor
    scope: event
    blocking: false
    summary: a three-judge independent code reading where one judge read the submission's README instead
    artifact: summaries/team-demos.md
    repair: name the two code readers and record the third as concurring from the README
    state: open
  - id: F19
    severity: minor
    scope: event
    blocking: false
    summary: three blocking defects attributed to judge-backend, who labels two
    artifact: summaries/team-scribe.md
    repair: restate the count
    state: open
  - id: F20
    severity: minor
    scope: event
    blocking: false
    summary: D2 mis-summarises what the three concurring judges deducted for
    artifact: summaries/team-scribe.md
    repair: list deductions per judge
    state: open
  - id: F21
    severity: minor
    scope: event
    blocking: false
    summary: ev-scribe-13 cited for a pipeline-stage mapping the manifest does not make
    artifact: summaries/team-scribe.md
    repair: cite the judge for the mapping and the evidence id for the counts
    state: open
  - id: F22
    severity: minor
    scope: event
    blocking: false
    summary: two conclusions stated as verified where the method was a five-path enumeration and a static grep over src only
    artifact: summaries/team-scribe.md
    repair: state the method and drop "verified the wider absence"
    state: open
  - id: F23
    severity: minor
    scope: event
    blocking: false
    summary: the blockers table still shows ADJ-1 and ADJ-2 deferred with no resolution artifact, contradicting the same file's team-progress table
    artifact: status.md
    repair: close both rows against their adjudication records
    state: open
  - id: F24
    severity: minor
    scope: event
    blocking: false
    summary: one out-of-order pair in the activity log, the round-three repair row before the gate row it precedes in time
    artifact: status.md
    repair: reorder
    state: open
  - id: F25
    severity: minor
    scope: event
    blocking: false
    summary: the consolidation ledger row and last_updated are stamped twelve minutes before the artifacts they record finished
    artifact: status.md
    repair: restamp both to the artifacts' completed_at or later
    state: open
  - id: F26
    severity: minor
    scope: framework
    blocking: false
    summary: atj score requires an adjudication rationale only for severe disagreement, so an accepted NE can carry no machine-readable reason
    artifact: atj/scoring.py
    repair: require a rationale for any resolution that disposes of an NE
    state: open
  - id: F27
    severity: minor
    scope: framework
    blocking: false
    summary: the agreement band and outlier detection are computed from scored judges only, so a criterion half the panel could not judge is labelled aligned and outlier detection silently switches off
    artifact: atj/scoring.py
    repair: qualify the band when NE judges exist, and record that outlier detection did not run
    state: open
  - id: F28
    severity: advisory
    scope: event
    blocking: false
    summary: the head-to-head rule is paraphrased as "forbids deciding by the higher initial total" where the rubric says "do not merely select"
    artifact: summaries/team-scribe.md
    repair: quote the rubric
    state: open
  - id: F29
    severity: advisory
    scope: event
    blocking: false
    summary: the adjudication's disputed-claims row misstates the basis of judge-backend's agentic score; the consolidation characterises it correctly
    artifact: adjudications/adj-trial-2-2026-team-scribe-agentic.md
    repair: correct the row by amendment, or record the discrepancy
    state: open
  - id: F30
    severity: advisory
    scope: event
    blocking: false
    summary: template operator scaffolding retained in the shipped report, the same class the judgments audit deferred as house style
    artifact: summaries/team-demos.md
    repair: none mid-event; settle the class at the framework level
    state: open
  - id: F31
    severity: advisory
    scope: event
    blocking: false
    summary: five further single-judge items not carried by either report
    artifact: summaries/team-demos.md
    repair: carry or record as deliberately dropped
    state: open
  - id: F32
    severity: advisory
    scope: event
    blocking: false
    summary: a source discrepancy between two judges' line ranges for one defect is resolved by omitting the line numbers rather than recording it
    artifact: summaries/team-scribe.md
    repair: record both ranges
    state: open
  - id: F33
    severity: advisory
    scope: event
    blocking: false
    summary: D0 propagates the judgments audit's "different methods, no shared wording" where both judges describe the same two tools
    artifact: summaries/team-demos.md
    repair: qualify when repeating the prior audit's wording
    state: open
  - id: F34
    severity: advisory
    scope: event
    blocking: false
    summary: both reports enumerate exploitable weaknesses in third-party repositories at exact file and line; the disclosure question reaches the dossier stage undecided
    artifact: summaries/team-demos.md
    repair: settle disclosure with the event director before the dossier stage
    state: open
---

# Consolidation Audit — both teams, first pass

## Result

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
