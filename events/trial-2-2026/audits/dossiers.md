---
event_id: trial-2-2026
audit_scope: dossiers stage, round one — dossiers/team-demos.md and dossiers/team-scribe.md, the two consolidated-summary errors the dossier writers reported, public/mu-final-01.md as placed and approved, the approve fix ac513ed, overrides/ovr-trial-2-2026-model-substitution.md, and status.md (commits ffcf150..483cff7)
audit_id: dossiers
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.1.0
persona: judging-auditor@1.1.0
framework_commit: 483cff70a30f15e78fbd658b000743e3224956d6
model_requested: claude-opus-5
model_used: claude-opus-5-5[1m]
started_at: "2026-09-23T20:18:57Z"
completed_at: "2026-09-23T20:27:37Z"
visibility: private
approval_state: draft
validation_state: unvalidated
result: PASS WITH ADVISORIES
findings:
- id: DO1
  severity: major
  scope: event
  blocking: false
  summary: team-demos dossier says demo 06's constant prompt was named by two judges. Three named it (backend, frontend-ux, product-agentic). The writer's report of two is wrong, and so is the summary's four (DO2)
  artifact: dossiers/team-demos.md:101-104
  repair: 'replace "Named by two judges, the backend reviewer and the product and agentic reviewer." with "Named by three judges: the backend reviewer, the frontend and UX reviewer and the product and agentic reviewer." Sources: judgments/team-demos/judge-backend.md:51,107; judge-frontend-ux.md:164,166; judge-product-agentic.md:256. judge-security-ops.md:169 says only "reduces its lesson to two constants", which is identity and mode, not the prompt'
  state: open
- id: DO2
  severity: minor
  scope: event
  blocking: false
  summary: summaries/team-demos.md says all four judges named demo 06's byte-identical prompt. Three did. The writer's count of two is also wrong, so an erratum written from the writer's report would be a second error
  artifact: summaries/team-demos.md:425-427
  repair: do not edit the summary. Its digest feeds bracket:draw and both dossier units (atj/event.py:936-953,966-974), so an edit would stale two closed stages. Add a status.md activity row recording the erratum as "three judges (backend, frontend-ux, product-agentic), not four", citing this finding, and carry it to the final audit
  state: open
- id: DO3
  severity: minor
  scope: event
  blocking: false
  summary: summaries/team-scribe.md says three judges made narrowing main.py:50 their highest-value improvement. Two did (backend, product-agentic). The writer is right
  artifact: summaries/team-scribe.md:203-205
  repair: 'same route as DO2: a status.md erratum row, "two judges (judge-backend.md:95, judge-product-agentic.md:106). frontend-ux :96 and security-ops :103 chose other product improvements". No summary edit'
  state: open
- id: DO4
  severity: minor
  scope: event
  blocking: false
  summary: summaries/team-scribe.md says all four judges credit the failure-as-state design. Three credit PipelineStatus (backend, frontend-ux, product-agentic). security-ops credits only the retry decorator in that bullet. The writer is right
  artifact: summaries/team-scribe.md:160-166
  repair: 'same route as DO2: a status.md erratum row, "PipelineStatus credited by three (judge-backend.md:129, judge-frontend-ux.md:53,128, judge-product-agentic.md:140-142); the retry decorator by backend, product-agentic and security-ops (judge-security-ops.md:109,135,183)". No summary edit. The dossier does not repeat the claim'
  state: open
- id: DO5
  severity: minor
  scope: event
  blocking: false
  summary: team-demos dossier lists the demo 09 empty-hostname guard as a single-judge finding from the backend reviewer. All four judges found it, and the declared source summary says so
  artifact: dossiers/team-demos.md:208-211
  repair: 'move it out of the single-judge sentence. Suggested text: "All four judges found that the demo 09 POST guard accepts an empty hostname where demo 07''s guard for the same concern does not; no egress path was shown, since urllib rejects that form." Sources: summaries/team-demos.md:480-485 (PD3); judge-backend.md:124,190; judge-frontend-ux.md:154; judge-product-agentic.md:430; judge-security-ops.md:205'
  state: open
- id: DO6
  severity: minor
  scope: event
  blocking: false
  summary: source_reports are incomplete and inconsistent. team-scribe quotes judgments that are not declared ("in far better shape than the headline failure suggests" exists only at judge-product-agentic.md:180). team-demos cites seven run records and declares none. team-scribe declares two runs and cites a third indirectly (DO8)
  artifact: dossiers/team-scribe.md:9-16; dossiers/team-demos.md:9-15
  repair: add `judgments/team-scribe/` to team-scribe's source_reports. A directory path clears the persona-name pattern at atj/publication.py:78, as team-demos already shows. Declare run records the same way in both, either `runs/` in each or every cited run file in each
  state: open
- id: DO7
  severity: minor
  scope: event
  blocking: false
  summary: team-scribe's tournament section says neither judge compared a total "since neither team had one". That tells team-scribe that team-demos has no official total, which is team-demos's scoring state and is not in public/mu-final-01.md
  artifact: dossiers/team-scribe.md:348-349
  repair: 'replace with "Neither judge used or compared an overall total; the comparison is made criterion by criterion." Source: mu-final-01-pass-a-first.md:72, pass-b-first.md:57'
  state: open
- id: DO8
  severity: minor
  scope: event
  blocking: false
  summary: '"PySide6 is installed and works" cites runs/team-scribe-app-start-01.json. That record holds the misleading message and the qdarkstyle error. PySide6 being installed and constructing a QApplication is in runs/team-scribe-envcheck-01.json (ev-scribe-01)'
  artifact: dossiers/team-scribe.md:158-159
  repair: cite `ev-scribe-01` (evidence/team-scribe/manifest.md) or `runs/team-scribe-envcheck-01.json`, and declare it under DO6
  state: open
- id: DO9
  severity: minor
  scope: event
  blocking: false
  summary: status.md was not updated after verified work. It has no rows for the dossier drafts (ffcf150), the approve fix (ac513ed), the public summary's placement and approval (c0a55df), or the F8 override (483cff7). last_updated is still 18:53:28Z, row 147 still calls F8 and the public summary open, and the Team progress Dossier column reads "—"
  artifact: status.md:4,147,62-63
  repair: add one activity row per commit with its UTC time. Record that F8 is closed by the override, that T5 and F15 are closed (DOA3), that R5 is closed (unit matchup:mu-final-01 has audit_result PASS WITH ADVISORIES), and the DO2-DO4 errata. Set last_updated to the last row. Fill the Dossier column after approval
  state: open
- id: DO10
  severity: minor
  scope: event
  blocking: false
  summary: the override files a model substitution under category "other" and cites event.md's officials and an audit finding as authority. None of the four officials keys at event.md:23-27 covers it, and an audit's repair text grants no authority. Deviating from event.md's model_requested is a rules exception, and the bracket stage recorded the same defect as F4
  artifact: overrides/ovr-trial-2-2026-model-substitution.md:38,40-44
  repair: set Category to `rules exception`. Cite framework/policies/disagreement-and-adjudication.md:9 ("A human event official owns ... rules exceptions") and the event.md line that names event-director as that official. Keep tournament F8 as the reason the record exists, not as its authority. Re-approve after the edit
  state: open
- id: DO11
  severity: minor
  scope: framework
  blocking: false
  summary: ac513ed is sound. Only publication.py:336-346 emits rule "approval", and both findings are cleared by the fields approve writes. The one new test covers only the success path, so nothing proves a draft public artifact with a second blocking finding is still refused
  artifact: tests/test_tier1_regressions.py:614-632; atj/cli.py:436-440
  repair: add a negative test. Take a draft public artifact that also carries a numeric total or a private-only field, run approve, and assert exit FAILURE with the artifact unchanged. Framework window, not this stage
  state: deferred
- id: DOA1
  severity: advisory
  scope: event
  blocking: false
  summary: team-demos was written with validation_state valid and team-scribe with unvalidated, and no tool produced either value. Both dossiers carry the same completed_at to the second (20:01:27Z)
  artifact: dossiers/team-demos.md:22; dossiers/team-scribe.md:23
  repair: none by hand. atj event approve writes validation_state. Record in status.md whether the times were stamped by each writer or by the orchestrator
  state: open
- id: DOA2
  severity: advisory
  scope: event
  blocking: false
  summary: the repository cannot show that a human made either approval. public/mu-final-01.md (20:17:22Z) and the override (20:18:26Z) both read approved_by event-director, written by atj event approve in an agent session. The public approval also ran before ac513ed was committed (20:17:57Z)
  artifact: public/mu-final-01.md:13-17; overrides/ovr-trial-2-2026-model-substitution.md:17-22
  repair: Gregg confirms both decisions were his. If either was not, withdraw it with atj event approve --state withdrawn
  state: open
- id: DOA3
  severity: advisory
  scope: event
  blocking: false
  summary: public/mu-final-01.md is the audited draft. Diffed against the scratchpad draft the round-five tournament audit reviewed (mtime 18:37:34Z, before that audit), the body is identical and only the approval fields differ. T5 is closed, because atj validate publication returns CLEAR at the declared location. F15 is closed by approval_note. The pre-approval run T5 asked for could only have shown the two approval blockers, and it is recorded nowhere
  artifact: public/mu-final-01.md
  repair: record the T5 and F15 closure in status.md (DO9)
  state: accepted
- id: DOA4
  severity: advisory
  scope: event
  blocking: false
  summary: each dossier gives six per-criterion means that, multiplied by the rubric weights, reproduce the provisional sums in status.md:62-63. Neither dossier combines them. The live-trial precedent (its DOA4) accepts this
  artifact: dossiers/team-demos.md:129-137; dossiers/team-scribe.md:127-135
  repair: keep the "no official total" sentences through every later edit
  state: accepted
- id: DOA5
  severity: advisory
  scope: event
  blocking: false
  summary: team-demos's statement that the opponent's start-up path failed is match-public, because public/mu-final-01.md:29-32 says the same thing. team-scribe names its opponent by team id (the validator's foreign-team advisory) while the public summary uses the display name
  artifact: dossiers/team-demos.md:303-306; dossiers/team-scribe.md:335-337
  repair: optionally write "AI Security Demos" in team-scribe's dossier
  state: accepted
- id: DOA6
  severity: advisory
  scope: event
  blocking: false
  summary: team-demos states as fact that the matchup evaluators "could not see each other's work". The repository shows this only as orchestrator-attested (tournament F14)
  artifact: dossiers/team-demos.md:291-293
  repair: optionally write "were run independently, as the event records"
  state: open
- id: DOA7
  severity: advisory
  scope: event
  blocking: false
  summary: several attributions are accurate but narrower than the record. Error messages were also credited by the backend reviewer (judge-backend.md:85,169). The KDF was also flagged by security-ops (:159,204). frontend-ux's version of the CI job names neither health_check nor a pytest run (:122). product-agentic's contrary categorize_content finding (:114) is not mentioned. The demo 09 "no write capability" attribution to product-agentic follows summaries/team-demos.md:513-516 (PD6), but product-agentic's own text credits the docstring's disclosure
  artifact: dossiers/team-scribe.md:114-118,268,301-306,205-207; dossiers/team-demos.md:249-252
  repair: optional wording repairs in the same pass as DO1-DO8
  state: open
- id: DOA8
  severity: advisory
  scope: framework
  blocking: false
  summary: an audited consolidated summary has no errata route that does not stale the downstream ledger, because the bracket:draw and dossier digests include summaries/*.md
  artifact: atj/event.py:936-953,966-974
  repair: add a W-item to docs/0.5.0-beta-plan.md for an errata attachment outside the digested file
  state: deferred
- id: DOA9
  severity: advisory
  scope: event
  blocking: false
  summary: the override is accurate about model_used, the eight judgments, the unchanged event.md and the public artifact. It does not mention that all three matchup artifacts record model_requested `opus`, not event.md's claude-opus-5
  artifact: overrides/ovr-trial-2-2026-model-substitution.md:36; matchup-passes/*.md:15; matchups/mu-final-01.md:15
  repair: add one sentence in the DO10 edit
  state: open
- id: DOA10
  severity: advisory
  scope: framework
  blocking: false
  summary: ac513ed, a framework fix, landed on the event branch in the middle of a stage. 519 tests pass and release-check passes
  artifact: commit ac513ed
  repair: none. Name it in the PR body
  state: accepted
---

# Dossiers Audit, round one

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
