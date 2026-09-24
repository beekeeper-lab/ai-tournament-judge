---
event_id: trial-2-2026
audit_scope: dossiers stage, round four, scoped to the DF1-DF2 repair in a6569f8 (overrides/ovr-trial-2-2026-model-substitution.md, status.md)
audit_id: dossiers
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.1.0
persona: judging-auditor@1.1.0
framework_commit: a6569f82622108ab969e1b0495481af9c9c77f9e
model_requested: claude-opus-5
model_used: claude-opus-5-5[1m]
started_at: "2026-09-23T20:38:01Z"
completed_at: "2026-09-23T20:38:48Z"
visibility: private
approval_state: approved
validation_state: valid
result: PASS WITH ADVISORIES
findings:
- id: DF1
  severity: minor
  scope: event
  blocking: false
  summary: 'round three. Repaired. The override now cites event.md:23-27 for the four official keys (all event-director, none rules exceptions), quotes event.md:103 "holds all four authorities" exactly, and quotes disagreement-and-adjudication.md:9 exactly. "event-director is the only official this event names" is true: event.md:24-27 name no other official. The repair differs from the round-three repair text and is correct against the source'
  artifact: overrides/ovr-trial-2-2026-model-substitution.md:39-46
  repair: none
  state: repaired
- id: DF2
  severity: minor
  scope: event
  blocking: false
  summary: round three. Repaired. Four rows added. 20:33:43Z equals round-two completed_at. 20:35:01Z equals the 16a332c commit time. 20:36:51Z equals round-three completed_at. 20:37:33Z equals the override completed_at and precedes the a6569f8 commit (20:37:34Z) by one second. last_updated equals the last row
  artifact: status.md:4,155-158
  repair: none
  state: repaired
- id: DE1
  severity: minor
  scope: event
  blocking: false
  summary: round two. Repaired, with its remainder closed by DF1
  artifact: overrides/ovr-trial-2-2026-model-substitution.md:39-46
  repair: none
  state: repaired
- id: DEA1
  severity: advisory
  scope: event
  blocking: false
  summary: round two. Still open. The override is draft, so tournament F8 is open, and status.md still reads "F8 closed" at 20:18:32Z
  artifact: status.md
  repair: after atj event approve on the override, add a status.md row with that time recording F8 closed
  state: open
- id: DEA2
  severity: advisory
  scope: event
  blocking: false
  summary: round two. Repaired. completed_at moved to 20:37:33Z with the DF1 edit. framework_commit left at c0a55df, and the status.md row at 20:37:33Z says so
  artifact: overrides/ovr-trial-2-2026-model-substitution.md:11,15
  repair: none
  state: repaired
- id: DEA3
  severity: advisory
  scope: event
  blocking: false
  summary: round two. Accepted. Round-one DO6 miscounted seven run records. There are six and the repair is right
  artifact: audits/dossiers.md round one DO6; dossiers/team-demos.md:15-20
  repair: none
  state: accepted
- id: DOA2
  severity: advisory
  scope: event
  blocking: false
  summary: round one. Still open. The repository cannot show that a human approved the public summary or will approve the override
  artifact: public/mu-final-01.md; overrides/ovr-trial-2-2026-model-substitution.md
  repair: Gregg runs, or confirms in person, each approval
  state: open
- id: DOA8
  severity: advisory
  scope: framework
  blocking: false
  summary: round one. Still deferred. docs/0.5.0-beta-plan.md has no errata W-item yet
  artifact: atj/event.py:936-953,966-974
  repair: add the W-item in the framework window
  state: deferred
- id: DGA1
  severity: advisory
  scope: event
  blocking: false
  summary: round four, new, outside the a6569f8 scope. The round-one repair row at 20:30:25Z precedes its commit ef6d656 (20:31:18Z) by 53 seconds. A row may record when the work finished rather than the commit, so this is noted only
  artifact: status.md:154
  repair: none required
  state: open
approved_by: event-director
approved_at: "2026-09-24T00:14:24Z"
approval_note: Approval delegated by the event-director in session, 2026-09-23; run by the orchestrator
---

# Dossiers Audit, round four

Scoped to `git show a6569f8 -- events/trial-2-2026/overrides/ events/trial-2-2026/status.md`.
New findings use `DG1..DGn`.

## Result

**PASS WITH ADVISORIES.** No blocking, major or minor finding. DF1, DF2, DE1 and
DEA2 are repaired. DEA1 and DOA2 wait on the event-director. DOA8 is deferred.
DGA1 is new, advisory and outside scope.

## Scope and artifacts inspected

- The override diff in `a6569f8`: `completed_at` 20:18:07Z to 20:37:33Z, and the
  Authority paragraph. No other line changed.
- `event.md:23-27`, `event.md:103`, `framework/policies/disagreement-and-adjudication.md:9`.
- The four new `status.md` rows and `last_updated`, against
  `git log --format='%h %cI'` and the round-two and round-three front matter.
- `git diff a6569f8 HEAD` is empty and the working tree is clean.

No record, unit, approve, gate or advance command was run.

## Deterministic validation results

| Command | Result |
|---|---|
| `atj event status events/trial-2-2026` | stage dossiers, `dossiers-approved` pending, units 2 complete, none stale |
| `atj validate reports events/trial-2-2026` | PASS WITH ADVISORIES, 33 artifacts, 1 advisory `foreign-team` |
| `atj validate publication events/trial-2-2026` | CLEAR, 33 artifacts, 0 blocking |
| `atj validate publication --event-dir events/trial-2-2026 events/trial-2-2026/dossiers/` | CLEAR, 2 artifacts, 0 blocking |

## Word-for-word check

| Override says | Source |
|---|---|
| "A human event official owns disqualification, rules exceptions, and unresolved final ties." | `disagreement-and-adjudication.md:9`, exact |
| `event.md:23-27` names `event-director` for all four official keys, none rules exceptions | `:23` `officials:`, `:24-27` disqualification, adjudication, publication_approval, security_escalation, each `event-director`. True |
| `event.md:103` "holds all four authorities" | `:103` "`event-director` holds all four authorities and Gregg Reed holds that role." Exact |
| `event-director` is the only official this event names | no other official in `event.md`. True |

## Ledger check

| Row | Source | Match |
|---|---|---|
| 20:33:43Z round two, `8200b4e..ef6d656` | round-two `completed_at` 20:33:43Z, `audit_scope` 8200b4e..ef6d656 | yes |
| 20:35:01Z repair, `16a332c` | `16a332c` 2026-09-23T16:35:01-04:00 | yes |
| 20:36:51Z round three, `16a332c` | round-three `completed_at` 20:36:51Z, scope 16a332c | yes |
| 20:37:33Z repair, round three | override `completed_at` 20:37:33Z, `a6569f8` 16:37:34-04:00 | yes |
| `last_updated` 20:37:33Z | last row | yes |

## Findings

| ID | Severity | Scope | Blocking | State |
|---|---|---|---|---|
| DF1, DF2, DE1 | minor | event | no | repaired |
| DEA2 | advisory | event | no | repaired |
| DEA1, DOA2 | advisory | event | no | open, event-director |
| DEA3 | advisory | event | no | accepted |
| DOA8 | advisory | framework | no | deferred |
| DGA1 | advisory | event | no | open, no repair required |

Round-one DO1-DO11 and DOA1, DOA3-DOA7, DOA9, DOA10 keep the states in the
retained round-two front matter below.

## Recommended commands, in order

1. Validate (orchestrator):

```bash
python3 -m atj validate reports events/trial-2-2026
python3 -m atj validate publication --event-dir events/trial-2-2026 events/trial-2-2026/dossiers/
```

2. Approvals, **event-director only** (`DOA2`):

```bash
python3 -m atj event approve events/trial-2-2026/audits/dossiers.md --official event-director
python3 -m atj event approve events/trial-2-2026/overrides/ovr-trial-2-2026-model-substitution.md --official event-director
python3 -m atj event approve events/trial-2-2026/dossiers/team-demos.md events/trial-2-2026/dossiers/team-scribe.md --official event-director
```

3. Units (orchestrator):

```bash
python3 -m atj event unit events/trial-2-2026 record --id dossier:team-demos --stage dossiers --output dossiers/team-demos.md --audit-result "PASS WITH ADVISORIES"
python3 -m atj event unit events/trial-2-2026 record --id dossier:team-scribe --stage dossiers --output dossiers/team-scribe.md --audit-result "PASS WITH ADVISORIES"
```

4. Add `status.md` rows for this audit, the approvals, F8 closed (`DEA1`) and the Dossier column (orchestrator).
5. Gate, **event-director only**, then status:

```bash
python3 -m atj event gate events/trial-2-2026 dossiers-approved passed --audit events/trial-2-2026/audits/dossiers.md
python3 -m atj event status events/trial-2-2026
```

## Completion gate

- [x] No blocking findings
- [x] No major findings
- [x] Calculations valid
- [x] Evidence references resolve
- [x] Version and identity checks pass
- [x] Privacy boundary passes
- [x] Every finding recorded in `findings:` with a `scope` and a `blocking` flag
- [ ] Approved with `atj event approve <this file>`

---

# Superseded, retained

## Round-three front matter, retained verbatim

```yaml
event_id: trial-2-2026
audit_scope: dossiers stage, round three, scoped to the DE1 repair in 16a332c (overrides/ovr-trial-2-2026-model-substitution.md)
audit_id: dossiers
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.1.0
persona: judging-auditor@1.1.0
framework_commit: 16a332cc4e2393a48bd7a0d0cc00f32edb2113a3
model_requested: claude-opus-5
model_used: claude-opus-5-5[1m]
started_at: "2026-09-23T20:35:46Z"
completed_at: "2026-09-23T20:36:51Z"
visibility: private
approval_state: draft
validation_state: unvalidated
result: PASS WITH ADVISORIES
findings:
- id: DF1
  severity: minor
  scope: event
  blocking: false
  summary: 'round three, new. The repaired sentence attributes to event.md:103-105 two things those lines do not say. (a) "all four named authorities, none of which is rules exceptions": event.md:103 says "holds all four authorities" and names none. The names are at event.md:23-27 (disqualification, adjudication, publication_approval, security_escalation). (b) "no other official is available": event.md:104-105 says "with a single operator none is available", where "none" is separation of duties, not an official. The paragraph also now concedes rules exceptions is not among the four and does not state why the event-director may still decide it. The DE1 repair text itself carried error (b)'
  artifact: 'overrides/ovr-trial-2-2026-model-substitution.md:41-43'
  repair: 'replace the event.md sentence with: "`event.md:23-27` names four authorities, none of them rules exceptions. `event.md:103-105` records that `event-director` holds all four, that Gregg Reed holds that role, and that with a single operator no separation of duties is available. This record treats the event-director, as the only human official, as the owner under `:9`." Edit while the record is draft, then re-audit the diff'
  state: open
- id: DF2
  severity: minor
  scope: event
  blocking: false
  summary: 'round three, new. status.md has no row for the round-two audit (20:31:46Z-20:33:43Z) or the DE1 repair in 16a332c (20:35:01Z). The last row and last_updated are 20:30:25Z'
  artifact: 'status.md:4 and the activity log tail'
  repair: 'add rows for the round-two audit, the DE1 repair (16a332c) and this round, times from git log and this front matter, then set last_updated to the last row'
  state: open
- id: DE1
  severity: minor
  scope: event
  blocking: false
  summary: 'round two. Repaired in part. "every authority" is gone and the record stays draft. The new wording has its own errors, recorded as DF1'
  artifact: 'overrides/ovr-trial-2-2026-model-substitution.md:41-43'
  repair: 'see DF1'
  state: repaired
- id: DEA1
  severity: advisory
  scope: event
  blocking: false
  summary: 'round two. Still open. The override is draft, so tournament F8 is open again, and status.md still reads "F8 closed" at 20:18:32Z'
  artifact: 'status.md'
  repair: 'after atj event approve on the override, add a status.md row with that time recording F8 closed'
  state: open
- id: DEA2
  severity: advisory
  scope: event
  blocking: false
  summary: 'round two. Still open. 16a332c changed the body again, and started_at, completed_at (20:18:07Z) and framework_commit (c0a55df) are unchanged'
  artifact: 'overrides/ovr-trial-2-2026-model-substitution.md:11,14-15'
  repair: 'optional. Restamp completed_at from date -u with the DF1 edit, or record in status.md that the times are the original authoring times'
  state: open
- id: DEA3
  severity: advisory
  scope: event
  blocking: false
  summary: 'round two. Accepted. Round-one DO6 miscounted seven run records. There are six and the repair is right'
  artifact: 'audits/dossiers.md round one DO6; dossiers/team-demos.md:15-20'
  repair: 'none'
  state: accepted
- id: DOA2
  severity: advisory
  scope: event
  blocking: false
  summary: 'round one. Still open. The repository cannot show that a human approved the public summary or will approve the override'
  artifact: 'public/mu-final-01.md; overrides/ovr-trial-2-2026-model-substitution.md'
  repair: 'Gregg runs, or confirms in person, each approval'
  state: open
- id: DOA8
  severity: advisory
  scope: framework
  blocking: false
  summary: 'round one. Still deferred. docs/0.5.0-beta-plan.md has no errata W-item yet'
  artifact: 'atj/event.py:936-953,966-974'
  repair: 'add the W-item in the framework window'
  state: deferred
```

# Dossiers Audit, round three (superseded, retained)

Scoped to the DE1 repair in `16a332c`, `git show 16a332c -- events/trial-2-2026/overrides/`.
New findings use `DF1..DFn`.

## Result

**PASS WITH ADVISORIES.** No blocking or major finding. Two new minor findings
(`DF1`, `DF2`), neither blocking. Fix `DF1` before the override is approved,
because approval freezes a sentence that misattributes its source.

## Scope and artifacts inspected

- The override diff in `16a332c`: one hunk, lines 41-43, +3/-2 in the Authority paragraph.
  No other line of the override changed, including front matter.
  `git diff 16a332c HEAD` on `overrides/` is empty.
- `event.md:23-27` and `event.md:101-106`, compared word for word with the new
  sentence (`DF1`).
- The `status.md` front matter and activity log tail (`DF2`).

No record, unit, approve, gate or advance command was run.

## Deterministic validation results

| Command | Result |
|---|---|
| `atj event status events/trial-2-2026` | stage dossiers, `dossiers-approved` pending, units 2 complete, none stale |
| `atj validate reports events/trial-2-2026` | PASS WITH ADVISORIES, 33 artifacts, 1 advisory `foreign-team` |
| `atj validate publication events/trial-2-2026` | CLEAR, 33 artifacts, 0 blocking |

## Word-for-word check

| Override says `event.md:103-105` records | Source |
|---|---|
| "holds all four named authorities" | `:103` "holds all four authorities". The names are at `:23-27` |
| "none of which is rules exceptions" | true of `:23-27`. Not in `:103-105` |
| "with a single operator no other official is available" | `:104-105` "with a single operator none is available", where "none" means separation of duties |

## Findings

| ID | Severity | Scope | Blocking | Artifact | One line |
|---|---|---|---|---|---|
| DF1 | minor | event | no | override `:41-43` | the sentence cites `:103-105` for facts found at `:23-27`, or found nowhere |
| DF2 | minor | event | no | `status.md` | no rows for the round-two audit or `16a332c` |
| DE1 | minor | event | no | override `:41-43` | repaired in part, remainder is DF1 |
| DEA1, DEA2, DOA2 | advisory | event | no | see front matter | open |
| DEA3 | advisory | event | no | round-one DO6 | accepted |
| DOA8 | advisory | framework | no | `atj/event.py` | deferred |

Round-one DO1-DO11 and DOA1, DOA3-DOA7, DOA9, DOA10 keep the states in the
retained round-two front matter below.

## Recommended commands, in order

1. Repair `DF1` and `DF2` (orchestrator). Check with
   `git diff -- events/trial-2-2026/overrides/ events/trial-2-2026/status.md`,
   then run a round-four audit scoped to that diff.
2. Validate (orchestrator):

```bash
python3 -m atj validate reports events/trial-2-2026
python3 -m atj validate publication --event-dir events/trial-2-2026 events/trial-2-2026/dossiers/
```

3. Approvals, **event-director only** (`DOA2`):

```bash
python3 -m atj event approve events/trial-2-2026/audits/dossiers.md --official event-director
python3 -m atj event approve events/trial-2-2026/overrides/ovr-trial-2-2026-model-substitution.md --official event-director
python3 -m atj event approve events/trial-2-2026/dossiers/team-demos.md events/trial-2-2026/dossiers/team-scribe.md --official event-director
```

4. Units (orchestrator):

```bash
python3 -m atj event unit events/trial-2-2026 record --id dossier:team-demos --stage dossiers --output dossiers/team-demos.md --audit-result "PASS WITH ADVISORIES"
python3 -m atj event unit events/trial-2-2026 record --id dossier:team-scribe --stage dossiers --output dossiers/team-scribe.md --audit-result "PASS WITH ADVISORIES"
```

5. Add `status.md` rows for the approvals, F8 closed (`DEA1`) and the Dossier column.
6. Gate, **event-director only**, then status:

```bash
python3 -m atj event gate events/trial-2-2026 dossiers-approved passed --audit events/trial-2-2026/audits/dossiers.md
python3 -m atj event status events/trial-2-2026
```

## Completion gate

- [x] No blocking findings
- [x] No major findings
- [x] Calculations valid
- [x] Evidence references resolve
- [x] Version and identity checks pass
- [x] Privacy boundary passes
- [x] Every finding recorded in `findings:` with a `scope` and a `blocking` flag
- [ ] Approved with `atj event approve <this file>`


## Round-two front matter, retained verbatim

```yaml
event_id: trial-2-2026
audit_scope: dossiers stage, round two, scoped to the round-one repair diff 8200b4e..ef6d656 (dossiers/team-demos.md, dossiers/team-scribe.md, overrides/ovr-trial-2-2026-model-substitution.md, status.md, tests/test_tier1_regressions.py)
audit_id: dossiers
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.1.0
persona: judging-auditor@1.1.0
framework_commit: ef6d65625d52db4b871acf1c538e97047d571c5f
model_requested: claude-opus-5
model_used: claude-opus-5-5[1m]
started_at: "2026-09-23T20:31:46Z"
completed_at: "2026-09-23T20:33:43Z"
visibility: private
approval_state: draft
validation_state: unvalidated
result: PASS WITH ADVISORIES
findings:
- id: DE1
  severity: minor
  scope: event
  blocking: false
  summary: 'round two, new. The override''s Authority paragraph says event.md:103 records that event-director "holds every authority in this event". event.md:103 says "holds all four authorities", and the four keys at event.md:23-27 (disqualification, adjudication, publication_approval, security_escalation) do not include rules exceptions, which is what round-one DO10 said. The citation to disagreement-and-adjudication.md:9 is exact'
  artifact: 'overrides/ovr-trial-2-2026-model-substitution.md:41-43'
  repair: 'replace the event.md sentence with: "`event.md:103-105` records that `event-director` holds all four named authorities and that, with a single operator, no other official is available." Edit while the record is still draft, then approve'
  state: open
- id: DEA1
  severity: advisory
  scope: event
  blocking: false
  summary: 'round two, new. Returning the override to draft reopens tournament F8 until it is approved again. The status.md row at 20:18:32Z still reads "F8 closed", and the repair row at 20:30:25Z says the record went back to draft without saying F8 is open again'
  artifact: 'status.md:151,154'
  repair: 'after atj event approve on the override, add a status.md row with that time recording F8 closed'
  state: open
- id: DEA2
  severity: advisory
  scope: event
  blocking: false
  summary: 'round two, new. The override body changed in ef6d656, but started_at and completed_at still read 20:18:07Z and framework_commit still reads c0a55df, so the front matter describes the first version'
  artifact: 'overrides/ovr-trial-2-2026-model-substitution.md:11,14-15'
  repair: 'optional. Either restamp completed_at from date -u with the DE1 edit or record in status.md that the times are the original authoring times'
  state: open
- id: DEA3
  severity: advisory
  scope: event
  blocking: false
  summary: 'round two, new. Round-one DO6 said team-demos cites seven run records. It cites six distinct files, and all six exist in runs/. The repair declared exactly those six, so the repair is right and the round-one count was wrong'
  artifact: 'audits/dossiers.md round one DO6; dossiers/team-demos.md:15-20'
  repair: 'none'
  state: accepted
- id: DO1
  severity: major
  scope: event
  blocking: false
  summary: 'round one. Repaired. dossiers/team-demos.md:109-110 now names three judges. Checked against judge-backend.md:51,107, judge-frontend-ux.md:164,166 and judge-product-agentic.md:256. judge-security-ops.md:169 says only "two constants"'
  artifact: 'dossiers/team-demos.md:107-110'
  repair: 'done'
  state: repaired
- id: DO2
  severity: minor
  scope: event
  blocking: false
  summary: 'round one. Repaired by an erratum row. status.md:153 records three judges (backend, frontend-ux, product-agentic), not four. summaries/team-demos.md:425-427 is the correct range. The summary is unedited'
  artifact: 'status.md:153'
  repair: 'done. Carry to the final audit'
  state: repaired
- id: DO3
  severity: minor
  scope: event
  blocking: false
  summary: 'round one. Repaired by the same row. Two judges is correct: judge-backend.md:95 and judge-product-agentic.md:106 both name main.py:50 as highest-value improvement. frontend-ux and security-ops chose other improvements. summaries/team-scribe.md:203-205 is the correct range'
  artifact: 'status.md:153'
  repair: 'done'
  state: repaired
- id: DO4
  severity: minor
  scope: event
  blocking: false
  summary: 'round one. Repaired by the same row. Three judges is correct: judge-backend.md:129, judge-frontend-ux.md:114,128,158, judge-product-agentic.md:142 (per-stage persisted pipeline state). security-ops does not credit PipelineStatus. summaries/team-scribe.md:160-166 is the correct range'
  artifact: 'status.md:153'
  repair: 'done'
  state: repaired
- id: DO5
  severity: minor
  scope: event
  blocking: false
  summary: "round one. Repaired. All four judges found it: judge-backend.md:124,190, judge-frontend-ux.md:154, judge-product-agentic.md:430-432, judge-security-ops.md:205. Each also says it is narrower than demo 07's guard"
  artifact: 'dossiers/team-demos.md:214-216'
  repair: 'done'
  state: repaired
- id: DO6
  severity: minor
  scope: event
  blocking: false
  summary: 'round one. Repaired. team-scribe declares judgments/team-scribe/ and all three run records it cites. team-demos declares all six run records it cites (DEA3)'
  artifact: 'dossiers/team-demos.md:9-21; dossiers/team-scribe.md:9-18'
  repair: 'done'
  state: repaired
- id: DO7
  severity: minor
  scope: event
  blocking: false
  summary: "round one. Repaired. The sentence no longer gives the opponent's scoring state"
  artifact: 'dossiers/team-scribe.md:350-351'
  repair: 'done'
  state: repaired
- id: DO8
  severity: minor
  scope: event
  blocking: false
  summary: 'round one. Repaired. runs/team-scribe-envcheck-01.json stdout shows "import OK PySide6 6.11.2" and "QApplication constructed offscreen", exit 0'
  artifact: 'dossiers/team-scribe.md:160-161'
  repair: 'done'
  state: repaired
- id: DO9
  severity: minor
  scope: event
  blocking: false
  summary: 'round one. Repaired. Six rows were added. Each time matches git log for ffcf150, ac513ed, c0a55df, 483cff7 and 8200b4e. The repair row (20:30:25Z) comes before ef6d656 (20:31:18Z). last_updated equals the last row. T5, F15 and R5 are recorded closed. The Dossier column waits for approval, which is correct'
  artifact: 'status.md:4,148-154'
  repair: 'done'
  state: repaired
- id: DO10
  severity: minor
  scope: event
  blocking: false
  summary: 'round one. Repaired except for one overstatement. Category is rules exception, disagreement-and-adjudication.md:9 is quoted exactly, F8 is named as the reason, and the record is back in draft. The event.md:103 paraphrase overstates its source (DE1)'
  artifact: 'overrides/ovr-trial-2-2026-model-substitution.md:35,38-43'
  repair: 'see DE1'
  state: repaired
- id: DO11
  severity: minor
  scope: framework
  blocking: false
  summary: 'round one. Repaired. test_a_draft_public_artifact_with_another_blocker_is_refused sets evidence_package_id on a draft public artifact and asserts exit 1, private-field and an unchanged file. The test passes'
  artifact: 'tests/test_tier1_regressions.py:634-651'
  repair: 'done'
  state: repaired
- id: DOA1
  severity: advisory
  scope: event
  blocking: false
  summary: "round one. Recorded. status.md:148 says each writer stamped the times from date -u, by the writers' own reports, and says this is not independently verified"
  artifact: 'status.md:148'
  repair: 'done'
  state: accepted
- id: DOA2
  severity: advisory
  scope: event
  blocking: false
  summary: "round one. Open. The repository cannot show that a human approved either artifact. status.md:150 now says the orchestrator ran the public approval on the event-director's answer. The override approval was withdrawn to draft"
  artifact: 'public/mu-final-01.md; overrides/ovr-trial-2-2026-model-substitution.md'
  repair: 'Gregg runs, or confirms in person, each approval'
  state: open
- id: DOA3
  severity: advisory
  scope: event
  blocking: false
  summary: 'round one. Accepted, and recorded at status.md:150'
  artifact: 'status.md:150'
  repair: 'done'
  state: accepted
- id: DOA4
  severity: advisory
  scope: event
  blocking: false
  summary: 'round one. Accepted. Both dossiers still say there is no official total, and neither combines the means'
  artifact: 'dossiers/team-demos.md:53; dossiers/team-scribe.md:43'
  repair: 'keep through later edits'
  state: accepted
- id: DOA5
  severity: advisory
  scope: event
  blocking: false
  summary: 'round one. Repaired. The display name is used at dossiers/team-scribe.md:337-340. The foreign-team advisory remains and is match-public'
  artifact: 'dossiers/team-scribe.md:337-340'
  repair: 'done'
  state: repaired
- id: DOA6
  severity: advisory
  scope: event
  blocking: false
  summary: 'round one. Repaired. The wording now reads "were run independently, as the event records"'
  artifact: 'dossiers/team-demos.md:299-301'
  repair: 'done'
  state: repaired
- id: DOA7
  severity: advisory
  scope: event
  blocking: false
  summary: 'round one. Not taken, as status.md:154 says. The attributions it lists are narrower than the record but none is false'
  artifact: 'dossiers/team-scribe.md; dossiers/team-demos.md'
  repair: 'none'
  state: accepted
- id: DOA8
  severity: advisory
  scope: framework
  blocking: false
  summary: 'round one. Still deferred. docs/0.5.0-beta-plan.md has no errata W-item yet'
  artifact: 'atj/event.py:936-953,966-974'
  repair: 'add the W-item in the framework window'
  state: deferred
- id: DOA9
  severity: advisory
  scope: event
  blocking: false
  summary: 'round one. Repaired. model_requested is opus at matchup-passes/*.md:15 and matchups/mu-final-01.md:15, as the override now says'
  artifact: 'overrides/ovr-trial-2-2026-model-substitution.md:34'
  repair: 'done'
  state: repaired
- id: DOA10
  severity: advisory
  scope: framework
  blocking: false
  summary: 'round one. Accepted'
  artifact: 'commit ac513ed'
  repair: 'name it in the PR body'
  state: accepted
```

# Dossiers Audit, round two (superseded, retained)

This round is scoped to `8200b4e..ef6d656`. I read every changed line and checked
each round-one finding against `judgments/`, `runs/`, the policy and `event.md`,
not against the repair's own wording. New findings use `DE1..DEn` and new
advisories use `DEA1..DEAn`.

## Result

**PASS WITH ADVISORIES.** There are no blocking or major findings, one new minor
finding (`DE1`) and three new advisories.

The round-one major `DO1` and every round-one minor are repaired. The judge counts
in the errata row at `status.md:153` match the judgments, and its summary line
ranges are exact. Every ledger time matches `git log`. The event status shows no
stale unit. `DE1` is an overstated paraphrase in a draft record. Fix it before the
override is approved.

## Scope and artifacts inspected

- The full diff `8200b4e..ef6d656` (5 files, +55/-20).
- `judgments/team-demos/*.md` for demo 06 and the empty-hostname guard, and
  `judgments/team-scribe/*.md` for `main.py:50`, `PipelineStatus` and the retry
  decorator.
- `summaries/team-demos.md:423-428` and `summaries/team-scribe.md:158-167,201-206`.
- `runs/team-scribe-envcheck-01.json` stdout, plus a list of `runs/` for both teams
  compared with each dossier's citations.
- `framework/policies/disagreement-and-adjudication.md:9`, `event.md:23-27,95-107`,
  and `model_requested` in `matchup-passes/*.md` and `matchups/mu-final-01.md`.
- `git log` times for `ffcf150`, `ac513ed`, `c0a55df`, `483cff7`, `8200b4e` and
  `ef6d656`.

No record, unit, approve, gate or advance command was run.

## Deterministic validation results

| Command | Result |
|---|---|
| `atj validate publication … dossiers/team-demos.md` | CLEAR, 0 blocking |
| `atj validate publication … dossiers/team-scribe.md` | CLEAR, 0 blocking, 1 advisory `foreign-team` (match-public) |
| `atj validate publication … public/mu-final-01.md` | CLEAR, 0 blocking |
| `atj validate reports events/trial-2-2026` | PASS WITH ADVISORIES, 33 artifacts, 1 advisory |
| `atj event status events/trial-2-2026` | stage dossiers, `dossiers-approved` pending, units 2 complete, none stale |
| `python3 -m pytest tests/ -q` | 520 passed, 5 skipped (the new negative test passes) |
| `python3 -m atj release-check` | PASS |

## Findings

| ID | Severity | Scope | Blocking | Artifact | One line |
|---|---|---|---|---|---|
| DE1 | minor | event | no | override `:41-43` | "every authority" overstates event.md:103, which says "all four authorities" |
| DEA1 | advisory | event | no | `status.md:151,154` | F8 is open again until the override is re-approved |
| DEA2 | advisory | event | no | override front matter | times and framework_commit describe the first version |
| DEA3 | advisory | event | no | round-one DO6 | round one counted seven runs. There are six, and the repair is right |

The round-one states are in front matter. 16 are repaired, 7 accepted, 1 deferred
(`DOA8`) and 1 open (`DOA2`, which needs Gregg).

## Recommended commands, in order

1. Repair `DE1` in the draft override, then check it with
   `git diff -- events/trial-2-2026/overrides/`.

```bash
python3 -m atj validate publication --event-dir events/trial-2-2026 events/trial-2-2026/dossiers/
python3 -m atj event approve events/trial-2-2026/audits/dossiers.md --official event-director
python3 -m atj event approve events/trial-2-2026/overrides/ovr-trial-2-2026-model-substitution.md --official event-director
python3 -m atj event approve events/trial-2-2026/dossiers/team-demos.md events/trial-2-2026/dossiers/team-scribe.md --official event-director
python3 -m atj event unit events/trial-2-2026 record --id dossier:team-demos --stage dossiers --output dossiers/team-demos.md --audit-result "PASS WITH ADVISORIES"
python3 -m atj event unit events/trial-2-2026 record --id dossier:team-scribe --stage dossiers --output dossiers/team-scribe.md --audit-result "PASS WITH ADVISORIES"
```

2. Add `status.md` rows for the approvals, F8 closed (`DEA1`) and the Dossier
   column. Then run:

```bash
python3 -m atj event gate events/trial-2-2026 dossiers-approved passed --audit events/trial-2-2026/audits/dossiers.md
python3 -m atj event status events/trial-2-2026
```

The event-director runs every approval in person (`DOA2`).

## Completion gate

- [x] No blocking findings
- [x] No major findings
- [x] Calculations valid
- [x] Evidence references resolve
- [x] Version and identity checks pass
- [x] Privacy boundary passes
- [x] Every finding recorded in `findings:` with a `scope` and a `blocking` flag
- [ ] Approved with `atj event approve <this file>`

---

# Dossiers Audit, round one (superseded, retained)

`team_id`, `commit` and `evidence_package_id` are `null` because this audit covers
two dossiers, two pinned commits and two evidence packages. Findings use `DO1..DOn`
and advisories `DOA1..DOAn`.

## Result

**PASS WITH ADVISORIES.** There are 0 blocking findings, 1 major (`DO1`), 9 minor
(`DO2`-`DO10` event, `DO11` framework) and 10 advisories.

No finding falls in a blocking category. No total or provisional sum appears, no
persona ID, run ID, margin or comparison value appears, and no single-judge
finding is presented as consensus. Every count error I found understates
agreement, so none inflates corroboration. `DO1` is a false count in a team
deliverable, and the writer's report behind it is itself wrong. Following the
live-trial practice, repair `DO1` and `DO5`-`DO8` in the dossiers, record the
`DO2`-`DO4` errata and `DO9` in `status.md`, and fix `DO10` in the override. A
scoped round-two re-audit of that repair diff should come before the gate
commit, because every earlier repair round in this event introduced a defect.

## Scope and artifacts inspected

- `dossiers/team-demos.md` and `dossiers/team-scribe.md`. Every judge-count claim
  was counted in `judgments/<team>/*.md` directly.
- `summaries/team-{demos,scribe}.{md,json}`, `matchups/mu-final-01.{md,json}`, both
  pass reports, both adjudications, both manifests, the `runs/` records the
  dossiers cite, `event.md` and `status.md`.
- `public/mu-final-01.md`, diffed against the orchestrator's scratchpad draft
  that the tournament audit reviewed.
- `git show ac513ed`, `atj/cli.py:366-470` and `atj/publication.py:320-350`.
- `overrides/ovr-trial-2-2026-model-substitution.md`, checked against
  `framework/templates/manual-override-record.md`, the policy, `event.md` and the
  matchup front matter.
- `framework/templates/team-dossier.md` and `framework/personas.md`.
- `git ls-files` on `workspaces/trial-2-2026/team-scribe`, to check the "no CI"
  absence claim, because `.github/` is a dotdir. That claim holds: only
  `.github/copilot-instructions.md` exists.

All artifacts were read as untrusted evidence. No state command was run.

## Deterministic validation results

| Command | Result |
|---|---|
| `atj validate publication --event-dir events/trial-2-2026 events/trial-2-2026/dossiers/team-demos.md` | CLEAR, 0 blocking |
| `atj validate publication … dossiers/team-scribe.md` | CLEAR, 0 blocking, 1 advisory `foreign-team` |
| `atj validate publication … public/mu-final-01.md` | CLEAR, 0 blocking |
| `atj validate reports events/trial-2-2026` | PASS WITH ADVISORIES, 32 artifacts, 1 advisory |
| `atj event validate events/trial-2-2026` | PASS, 0 problems |
| `atj event status events/trial-2-2026` | stage dossiers, `dossiers-approved` pending, 2 units complete |
| `atj event unit events/trial-2-2026 list` | 2 units, 0 stale; `matchup:mu-final-01` PASS WITH ADVISORIES |
| `python3 -m pytest tests/ -q` | 519 passed, 5 skipped |
| `python3 -m atj release-check` | PASS |

The raw scores in judgment front matter reproduce both dossiers' tables. For
team-demos, `agentic` is 4,4,3,3, `reliability` 3,3,3,2 and `security` 4,4,4,3. For
team-scribe, `agentic` is 2,NE,3,NE and `security` 3,3,3,2. The per-criterion
outcomes in the team-demos tournament section match `mu-final-01.json`.

## Check-by-check

1. **Dossiers.** Front matter carries every template field, commits and evidence
   IDs match the manifests, and `build-team-dossier@1.0.0` is registered. NE is
   explained correctly in both. `.env*` blindness is framed as a tool limit, never
   as a fact about the submission (team-demos :117-121, :318-321). The errors are
   `DO1` and `DO5`-`DO8`. The other claims I counted are correct, including every
   "all four", "three judges" and single-judge label in team-scribe.
2. **Reported summary errors.** Two of the three reports are confirmed (`DO3`,
   `DO4`). The third is confirmed as an error, but the writer's count is wrong
   too: the answer is three, not four and not two (`DO2`, `DO1`).
3. **Public summary.** It matches the audited draft, and T5 and F15 are closed
   (`DOA3`). Whether a human approved it cannot be seen from the repository
   (`DOA2`).
4. **ac513ed.** It cannot let an otherwise-invalid artifact through, because only
   the two `approval` findings are dropped and the write clears both. The
   negative test is missing (`DO11`).
5. **Override.** Its facts check out: `model_used` in five artifacts, eight
   judgments on `claude-opus-5`, `event.md` unchanged, no model in the public
   artifact, and no dossier body that mentions the substitution. Its authority
   is misfiled (`DO10`) and one detail is missing (`DOA9`).
6. **Ledger.** The R5 re-record is done and consistent (digest `0ddde002acd441b6`,
   0 stale). The prose is behind four commits (`DO9`). No dossier unit exists yet.
   That is correct, because approval rewrites the dossier and its digest.

## Findings

| ID | Severity | Scope | Blocking | Artifact | One line |
|---|---|---|---|---|---|
| DO1 | major | event | no | `dossiers/team-demos.md:101-104` | demo 06 constant prompt named by three judges, not two |
| DO2 | minor | event | no | `summaries/team-demos.md:425-427` | "all four" is three; the writer's "two" is also wrong |
| DO3 | minor | event | no | `summaries/team-scribe.md:203-205` | main.py:50 top improvement is two judges, not three |
| DO4 | minor | event | no | `summaries/team-scribe.md:160-166` | PipelineStatus credited by three, not four |
| DO5 | minor | event | no | `dossiers/team-demos.md:208-211` | empty-hostname guard found by all four, labelled single-judge |
| DO6 | minor | event | no | both dossiers' `source_reports` | judgments and runs undeclared or inconsistent |
| DO7 | minor | event | no | `dossiers/team-scribe.md:348-349` | reveals the opponent has no official total |
| DO8 | minor | event | no | `dossiers/team-scribe.md:158-159` | PySide6 claim cites the wrong run record |
| DO9 | minor | event | no | `status.md` | four commits unrecorded; F8 and public summary still shown open |
| DO10 | minor | event | no | override `:38,40-44` | authority and category misfiled; a rules exception |
| DO11 | minor | framework | no | `tests/test_tier1_regressions.py:614-632` | approve fix lacks a negative test |

Repairs are in each finding's `repair` field in front matter, each derived from
the judgment, run or policy text it cites.

## Advisories

See `DOA1`-`DOA10` in front matter.

## Recommended commands, in order, after the repairs and a round-two pass

```bash
python3 -m atj validate publication --event-dir events/trial-2-2026 events/trial-2-2026/dossiers/
python3 -m atj event approve events/trial-2-2026/audits/dossiers.md --official event-director
python3 -m atj event approve events/trial-2-2026/overrides/ovr-trial-2-2026-model-substitution.md --official event-director
python3 -m atj event approve events/trial-2-2026/dossiers/team-demos.md events/trial-2-2026/dossiers/team-scribe.md --official event-director
python3 -m atj event unit events/trial-2-2026 record --id dossier:team-demos --stage dossiers --output dossiers/team-demos.md --audit-result "PASS WITH ADVISORIES"
python3 -m atj event unit events/trial-2-2026 record --id dossier:team-scribe --stage dossiers --output dossiers/team-scribe.md --audit-result "PASS WITH ADVISORIES"
python3 -m atj event gate events/trial-2-2026 dossiers-approved passed --audit events/trial-2-2026/audits/dossiers.md
python3 -m atj event status events/trial-2-2026
```

Only the event-director runs the approvals, in person (`DOA2`). If a round-two
report supersedes this one, pass that report to `--audit` and `--audit-result`.

## Completion gate

- [x] No blocking findings
- [ ] No major findings (`DO1`)
- [x] Calculations valid
- [ ] Evidence references resolve (`DO6`, `DO8`)
- [x] Version and identity checks pass
- [x] Privacy boundary passes (`DO7` is team-facing and minor)
- [x] Every finding recorded in `findings:` with a `scope` and a `blocking` flag
- [ ] Approved with `atj event approve <this file>`
