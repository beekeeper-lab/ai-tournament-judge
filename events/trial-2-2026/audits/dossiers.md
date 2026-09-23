---
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
---

# Dossiers Audit, round two

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
