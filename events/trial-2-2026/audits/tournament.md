---
event_id: trial-2-2026
audit_scope: tournament stage, rounds one to four — the two mu-final-01 pass reports, the atj matchup result and its private report, the draft public summary, the release-check fix 36cd3d5, the H4 edit, the round-one repair aa0de72, the round-two repair c4d346e and the round-three repair 958d7df
audit_id: tournament
team_id: null
match_id: mu:trial-2-2026:final:01
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.1.0
persona: judging-auditor@1.1.0
framework_commit: 958d7df9a575ba1e8d72a279624fee802d29a6b8
model_requested: claude-opus-5
model_used: claude-opus-5-5[1m]
started_at: '2026-09-23T18:45:40Z'
completed_at: '2026-09-23T18:48:26Z'
visibility: private
approval_state: draft
validation_state: unvalidated
result: FAIL
findings:
- id: F1
  severity: major
  scope: event
  blocking: false
  summary: round three, repaired. The Why paragraph now lists what ran (demo 01's two dry runs, two state tools, the localhost check) and says the model-driven acts were not observed. Each item resolves to evidence/team-demos/manifest.md:109-113 and its run record
  artifact: scratchpad draft public/mu-final-01.md, "Why" paragraph (not yet under events/trial-2-2026/public/)
  repair: done
  state: repaired
- id: F2
  severity: major
  scope: framework
  blocking: false
  summary: round two, repaired. aa0de72 restores the integer pattern and exempts events/*/matchups/*.json by path. The test now requires integer, float and prose copies elsewhere to be caught. The exemption itself is looser than its comment claims (R3)
  artifact: atj/cli.py:1760-1794; tests/test_canonical_model.py:79-107
  repair: done
  state: repaired
- id: F3
  severity: minor
  scope: event
  blocking: false
  summary: round two, repaired. The paragraph attributes each correction to the pass that cites it, and every attribution resolves (pass A :70, pass B :54-56 and :69)
  artifact: matchups/mu-final-01.md:65-71
  repair: done
  state: repaired
- id: F4
  severity: minor
  scope: event
  blocking: false
  summary: round two, repaired. The report quotes head-to-head.md:12 exactly
  artifact: matchups/mu-final-01.md:62-63
  repair: done
  state: repaired
- id: F5
  severity: minor
  scope: event
  blocking: false
  summary: round two, repaired. Each erratum resolves. The grant citation omits the enumerated list at team-demos judge-security-ops.md:194 (R7)
  artifact: matchups/mu-final-01.md:143-147
  repair: done
  state: repaired
- id: F6
  severity: minor
  scope: event
  blocking: false
  summary: round three, repaired, with one new defect (T2). list_verdicts.py:20-21 and 10-show-your-work/demo/README.md:93 resolve at the pin and say what the erratum says. The egress-probe sentence cites manifest.md:112, which is the memory_diff row
  artifact: matchups/mu-final-01.md:148-151
  repair: done; see T2
  state: repaired
- id: F7
  severity: minor
  scope: event
  blocking: false
  summary: round two, repaired, with two new defects (R4, R5). Four rows and the unit exist. The unit digest re-derives as 1d4f5a970e3f5dc9 and covers the .md, the .json and both passes
  artifact: status.md
  repair: done
  state: repaired
- id: F8
  severity: minor
  scope: event
  blocking: false
  summary: round two, open by the orchestrator's decision. Both passes ran claude-opus-5-5[1m] against event.md:16's claude-opus-5 and nothing records a decision to accept it. The options are listed in the round-two body
  artifact: matchup-passes/*.md front matter; event.md:16
  repair: event-director decision, recorded in status.md or as an override. No re-run is required, because both orders share the model
  state: open
- id: F9
  severity: minor
  scope: framework
  blocking: false
  summary: round two, deferred as W21. Its citations resolve (publication.py:88, common.schema.json:15-18, the template's framework_commit field)
  artifact: docs/0.5.0-beta-plan.md W21
  repair: framework window
  state: deferred
- id: F10
  severity: minor
  scope: framework
  blocking: false
  summary: round two, deferred as W22 and tied to H4
  artifact: docs/0.5.0-beta-plan.md W22
  repair: framework window
  state: deferred
- id: F11
  severity: minor
  scope: event
  blocking: false
  summary: round two, repaired. "one consistent template" and "standard library only" are gone. "each with its own presenter guide" rests on ev-demos-02 and R1 (manifest.md:76,91). The new "dry run that needs no model or package install" is R2
  artifact: scratchpad draft public/mu-final-01.md
  repair: done
  state: repaired
- id: F12
  severity: advisory
  scope: event
  blocking: false
  summary: one run record drives functional, product and engineering. submission-evaluation.md:106 requires that, and the outcome stands without it
  artifact: runs/team-scribe-app-start-01.json
  repair: none required
  state: accepted
- id: F13
  severity: advisory
  scope: event
  blocking: false
  summary: round two, repaired. The erratum points to audits/judgments.md, and F18 (no repair made) and F19 (product rationales accepted) say what the erratum implies
  artifact: matchups/mu-final-01.md:152-153
  repair: done
  state: repaired
- id: F14
  severity: advisory
  scope: event
  blocking: false
  summary: the pass timestamps, the concurrent launch, independence and the transcript extraction are orchestrator-attested. mu-final-01.md:46-48 now says so
  artifact: matchups/mu-final-01.md:42-48
  repair: none possible from the repository
  state: accepted
- id: F15
  severity: advisory
  scope: event
  blocking: false
  summary: the draft discloses per-criterion outcomes in words. Not numeric and not blocked, so disclosure is the approver's decision
  artifact: scratchpad draft public/mu-final-01.md
  repair: approver decides
  state: open
- id: F16
  severity: advisory
  scope: framework
  blocking: false
  summary: round two, repaired. A dated amendment under H4 quotes the old text exactly (43e7e50:docs/0.5.0-beta-plan.md:112) and states the kill condition is unchanged. It does not name 77fcc6a, which git log supplies
  artifact: docs/0.5.0-beta-plan.md:123-126
  repair: done
  state: repaired
- id: F17
  severity: advisory
  scope: framework
  blocking: false
  summary: round two, deferred as W23
  artifact: docs/0.5.0-beta-plan.md W23
  repair: framework window
  state: deferred
- id: R1
  severity: minor
  scope: event
  blocking: false
  summary: aa0de72 was committed with release-check failing and six tests red. The cause was this audit's own round-one F2 table, which quoted weight-shaped copies that the restored pattern now catches. That is evidence the F2 repair works. This round restates them
  artifact: audits/tournament.md (round-one F2 table); commit aa0de72
  repair: restated by the auditor in its own report. Confirmed by release-check and pytest after the rewrite
  state: repaired
- id: R2
  severity: minor
  scope: event
  blocking: false
  summary: round three, repaired. The phrase is now "a dry-run mode that prints the exact prompt without calling a model". Every one of the ten demo directories holds a script with a --dry-run path, and ev-demos-03 observed it for demo 01
  artifact: scratchpad draft public/mu-final-01.md, "Both teams did well"
  repair: done
  state: repaired
- id: R3
  severity: minor
  scope: framework
  blocking: false
  summary: round three, repaired as scoped, with a residual hole (T1). _template and location-only files are now scanned, tested by two spoofs. The real mu-final-01.json in trial-2-2026 and live-trial-2026 is still exempt
  artifact: atj/cli.py:1788-1794
  repair: done; see T1
  state: repaired
- id: R4
  severity: minor
  scope: event
  blocking: false
  summary: round three, repaired. last_updated is 18:38:31Z, equal to the last activity row. The round-two row, 18:36:46Z, equals that report's completed_at. c4d346e was committed at 18:38:37Z, six seconds after its row
  artifact: status.md:4 against the final activity-log row
  repair: done
  state: repaired
- id: R5
  severity: minor
  scope: event
  blocking: false
  summary: 'round three, correct for now. The unit reads not-audited, digest d3d4bf0634d5c669, and atj event unit list reports 0 stale. One step is left: re-record the unit''s audit result after atj event approve on this report, as the bracket stage did'
  artifact: status.md units, matchup:mu-final-01
  repair: after approval, re-record matchup:mu-final-01 with --audit-result from this report
  state: open
- id: R6
  severity: advisory
  scope: event
  blocking: false
  summary: the unit's completed_at is 17:26:17Z. The mu-final-01.md content it digests was last changed around 18:29Z by the errata. This matches atj event unit's documented rule that a re-record keeps the original time, and the front matter's completed_at matches the later pass
  artifact: status.md units, matchup:mu-final-01
  repair: none required
  state: accepted
- id: R7
  severity: advisory
  scope: event
  blocking: false
  summary: round three, repaired. :194 added, and it is the enumerated seventeen-file list
  artifact: matchups/mu-final-01.md:144
  repair: done
  state: repaired
- id: T1
  severity: minor
  scope: framework
  blocking: false
  summary: '_is_matchup_result checks only that keys are present. An empty criteria dict passes all() vacuously, and top-level keys outside the result shape are not rejected. Probed: a file under events/<e>/matchups/ with the five required keys, an empty criteria dict and a separate dict holding the functional and product weights is exempt, and so is one with one well-formed criterion plus an extra official-weights dict. check_no_duplicate_weights reported nothing for either. No such file exists today'
  artifact: atj/cli.py:1750-1774; tests/test_canonical_model.py:80-117
  repair: deferred as W24 in docs/0.5.0-beta-plan.md, which states T1 accurately (round four)
  state: deferred
- id: T2
  severity: minor
  scope: event
  blocking: false
  summary: the F6 erratum says the egress guard probe was the event's own script and cites evidence/team-demos/manifest.md:112. Line 112 is the memory_diff.py row. The egress probe row is :113, which is what the round-two repair text gave
  artifact: matchups/mu-final-01.md, Errata, F6 bullet
  repair: done in 958d7df, manifest.md:113 is the egress guard probe row (round four)
  state: repaired
- id: T3
  severity: advisory
  scope: event
  blocking: false
  summary: the F6 erratum says "exited as documented" holds for the memory_diff.py output. 04-agent-that-remembered-wrong/demo/README.md:98 documents what the script does (a diff against the seed). The "No change" text is only in memory_diff.py:45. The run agrees with the documented behaviour, but its text is not documented
  artifact: matchups/mu-final-01.md, Errata, F6 bullet
  repair: done in 958d7df, see U3 for the residue (round four)
  state: repaired
- id: T4
  severity: advisory
  scope: event
  blocking: false
  summary: the draft says "a localhost check that refused every hostile address it was given". That is true of fetch_beacons.is_localhost, which refused all six non-local forms in runs/team-demos-egress-guards-01.json. The same run also exercised resume_parser v1.1's guard, which passed evil.example/collect through to urllib (ValueError, not the guard), as ev-demos-08 records. The singular wording is accurate. Read as covering the whole probe, it would not be
  artifact: scratchpad draft public/mu-final-01.md, Why paragraph
  repair: none required. The approver should know the sentence describes one of the two guards
  state: accepted
- id: T5
  severity: advisory
  scope: event
  blocking: false
  summary: atj validate publication cannot clear the draft where it is. From the scratchpad it returns BLOCKING location-unknown. It has not yet been run against the draft at a declared location
  artifact: scratchpad draft public/mu-final-01.md
  repair: run atj validate publication --event-dir events/trial-2-2026 on the artifact once it is placed under events/trial-2-2026/public/ by the sanctioned path, before a human approves it
  state: open
- id: U1
  severity: major
  scope: event
  blocking: true
  summary: the round-three repair edited matchups/mu-final-01.md (the F6 erratum) and did not re-record unit matchup:mu-final-01. status.md records digest d3d4bf0634d5c669, the file now digests to 74b6deda857714b4, atj event unit list reports 1 stale, and atj event status blocks advancement on it. The round-two repair re-recorded the unit after its errata edit (R5). This one omitted that step, so the ledger names an input the audited artifact no longer has
  artifact: events/trial-2-2026/status.md units, matchup:mu-final-01
  repair: python3 -m atj event unit events/trial-2-2026 record --id matchup:mu-final-01 --stage tournament --output matchups/mu-final-01.md --audit-result not-audited, then confirm atj event unit list reports 0 stale. After approval re-record with this report's result (R5)
  state: open
- id: U2
  severity: minor
  scope: event
  blocking: false
  summary: 'the round-three audit row in the activity log, status.md:140, has "completed_at: ''2026-09-23T18:44:08Z''" in its time column, a pasted YAML line, not a timestamp. The value equals the round-three report completed_at and precedes 958d7df (18:45:19Z), so only the form is wrong'
  artifact: events/trial-2-2026/status.md:140
  repair: the first cell of that row becomes 2026-09-23T18:44:08Z
  state: open
- id: U3
  severity: advisory
  scope: event
  blocking: false
  summary: the F6 erratum now says exited-as-documented does not hold for memory_diff.py. That is right for its "No change" text (memory_diff.py:45 only). But 04-agent-that-remembered-wrong/demo/README.md:35 documents the invocation python3 scripts/memory_diff.py and :98 describes the diff it ran, so the run matches documented invocation and behaviour. T3 asked for "consistent with the documented behaviour". The citation memory_diff.py:45 also lacks the demo path the list_verdicts citation carries
  artifact: matchups/mu-final-01.md, Errata, F6 bullet
  repair: 'optional: cite 04-agent-that-remembered-wrong/demo/scripts/memory_diff.py:45 at the pin and add that invocation and behaviour match 04-agent-that-remembered-wrong/demo/README.md:35,98'
  state: open
---

# Judging Audit — tournament stage, round four

## Result

**FAIL.** One blocking finding, `U1`. The round-three repair `958d7df` edited
`matchups/mu-final-01.md` and left the unit `matchup:mu-final-01` recorded against
the old digest. `atj event unit list` reports it stale and `atj event status`
refuses to advance over it. The citation repairs themselves are correct: `T2` and
`T3` hold against the sources, and `W24` states `T1` accurately. The repair also
introduced `U2` (a malformed activity-log timestamp) and `U3` (an advisory on the
new `memory_diff.py` wording). No comparison value, pass file or
`mu-final-01.json` changed.

`tournament-audited` may **not** be set on this report. `U1` is a one-command
repair. Re-audit after it.

## Scope and artifacts inspected

- `git diff HEAD~1..HEAD` at `958d7df`, excluding my round-three text, and the
  18:44:48Z activity-log row.
- The F6 erratum against `evidence/team-demos/manifest.md:53-55,109-114`, and the
  pinned checkout `workspaces/trial-2-2026/team-demos/` (HEAD `dc35f69`, the
  manifest's pinned commit): root `README.md:19-21`,
  `01-resume-that-talked-back/demo/README.md:21-22`,
  `10-show-your-work/demo/README.md:26,93`, `list_verdicts.py:19-21`,
  `04-agent-that-remembered-wrong/demo/README.md:35,93,98`, `memory_diff.py:44-45`.
- `W24` in `docs/0.5.0-beta-plan.md` against `atj/cli.py:1750-1774` and my `T1`.
- `status.md` rows 140-141, `last_updated`, the units block, and
  `git log --format='%h %cI'`.

## Deterministic validation results

| Check | Result |
|---|---|
| `python3 -m atj validate reports events/trial-2-2026`, at 958d7df | PASS, 28 artifacts, 0 findings |
| `python3 -m pytest tests/ -q`, at 958d7df | 518 passed, 5 skipped |
| `python3 -m atj release-check`, at 958d7df | PASS |
| `atj event unit events/trial-2-2026 list` | 2 units, **1 stale**: `matchup:mu-final-01`, recorded `d3d4bf0634d5c669`, now `74b6deda857714b4` (`U1`) |
| `atj event status events/trial-2-2026` | blocked on the pending gate and on the stale unit |
| `_is_matchup_result` on `trial-2-2026` and `live-trial-2026` `mu-final-01.json` | both exempt |

## The round-three repair against the source

| Claim | Source | Holds |
|---|---|---|
| T2: the egress guard probe row is `manifest.md:113` | line 113 is the `<egress guard probe>` row. Line 112 is `memory_diff.py` | yes |
| T3: `memory_diff.py`'s "No change" text is in the script only (`memory_diff.py:45`) | line 45 prints it. No Markdown file at the pin contains "No change" | yes (`U3` on what the sentence leaves out) |
| The root README documents the dry run printing the exact prompt | root `README.md:20-21`: "A `--dry-run` flag prints the exact prompt with no API call". Also demo 01 `README.md:21-22` | yes. The documented invocation is `uv run`, which the erratum already says was not used |
| The dry runs used an undocumented invocation (`manifest.md:53-55`) | unchanged from round three | yes |
| W24: key presence, vacuous `all()` on empty `criteria`, extra keys not rejected | `atj/cli.py:1768-1774`: subset test on the five keys and on the three per-criterion fields, nothing on extra or missing criterion ids | yes |
| W24: both real results exempt correctly | both `mu-final-01.json` return True | yes |
| W24: each repair round introduced a new defect | rounds one to three, and this round's `U1`, `U2` | yes |

## Timestamps

| Item | Value | Check |
|---|---|---|
| Round-three report `completed_at` | 18:44:08Z | equals the value in row 140, but that cell reads `completed_at: '2026-09-23T18:44:08Z'` (`U2`) |
| Round-three repair row | 18:44:48Z | after 18:44:08Z, before `958d7df` at 18:45:19Z |
| `last_updated` | 18:44:48Z | equals the last row |
| This report `started_at` | 18:45:40Z | after `958d7df` |

## New findings

- **U1, major, blocking.** Stale unit after the errata edit. See `findings:`.
- **U2, minor.** Row 140's time cell holds a YAML line.
- **U3, advisory.** The `memory_diff.py` clause is correct about the text and
  silent on the documented invocation and behaviour.

## Carried

`T1` deferred as `W24`. `T4` accepted. `T5`, `F15` are the approver's. `F8` is the
event-director's. `R5` still has its post-approval step.

## Required repairs

1. `U1`: `python3 -m atj event unit events/trial-2-2026 record --id matchup:mu-final-01 --stage tournament --output matchups/mu-final-01.md --audit-result not-audited`,
   then `atj event unit events/trial-2-2026 list` shows 0 stale.
2. `U2`: row 140's first cell becomes `2026-09-23T18:44:08Z`.
3. `U3`, optional: the wording in its finding.

Then re-audit, scoped to that diff.

**Verdict: FAIL. `U1` blocks. `tournament-audited` may not be set until `U1` is
repaired and re-audited.**

---

# Judging Audit — tournament stage, round three (superseded, retained)

## Result

**PASS WITH ADVISORIES.** No finding is blocking. The round-two repair
`c4d346e` fixes `F1`, `F6`, `R2`, `R3`, `R4` and `R7` against their sources. `R5`
is correct for now and has one step left after approval. The repair added two
minor findings, `T1` (a residual hole in the new shape check) and `T2` (an
off-by-one citation in the F6 erratum), and three advisories, `T3` to `T5`. `F8`
and `F15` stay open from earlier rounds, and neither holds the gate. No
comparison value, pass file or `mu-final-01.json` changed in `c4d346e`.

`tournament-audited` may be set once this report is approved with
`atj event approve`. Nothing in `findings:` blocks the gate.

**The public draft may go to a human approver**, on two conditions. `T5`:
`atj validate publication` must pass on it at a declared location first. The
approver must also decide `F15` (per-criterion outcomes disclosed in words). Every
factual claim in "Why" and "Both teams did well" resolved to the evidence. `T4`
explains the scope of the localhost sentence.

## Scope and artifacts inspected

- `git diff aa0de72..c4d346e`, excluding my own round-two text, and the
  18:38:31Z activity-log row.
- The draft at the orchestrator's scratchpad path, `public/mu-final-01.md`, as
  edited in place. Every sentence in "Why" and "Both teams did well" was checked
  against `evidence/team-demos/manifest.md`, `evidence/team-scribe/manifest.md`,
  `runs/team-demos-egress-guards-01.json`, both pass reports,
  `mu-final-01.json`, and the pinned checkout
  `workspaces/trial-2-2026/team-demos/` (HEAD `dc35f696…`, clean).
- The F5 and F6 errata in `matchups/mu-final-01.md` against the pinned checkout
  and `judgments/team-demos/judge-security-ops.md`.
- `_is_matchup_result` and `check_no_duplicate_weights` in `atj/cli.py`, and
  `test_a_decisive_matchup_margin_is_not_a_weight_copy`, probed with my own
  spoof files in a temporary root.
- `status.md`, `atj event unit events/trial-2-2026 list`, and
  `git log --format='%h %cI'`.

## Deterministic validation results

| Check | Result |
|---|---|
| `python3 -m atj validate reports events/trial-2-2026`, at c4d346e | PASS, 28 artifacts, 0 findings |
| `python3 -m pytest tests/ -q`, at c4d346e | 518 passed, 5 skipped |
| `python3 -m atj release-check`, at c4d346e | PASS |
| `atj event unit events/trial-2-2026 list` | 2 units, 0 stale. `matchup:mu-final-01` complete, not-audited |
| `atj validate publication --event-dir events/trial-2-2026` on the scratchpad draft | BLOCKED, `location-unknown` (`T5`) |
| `_is_matchup_result` on `trial-2-2026` and `live-trial-2026` `mu-final-01.json` | both exempt |
| Probe: the five result keys, empty `criteria`, plus a separate weight dict | **exempt, nothing reported** (`T1`) |
| Probe: one well-formed criterion plus an extra official-weights dict | **exempt, nothing reported** (`T1`) |
| The same three after this rewrite | recorded under "After the rewrite" below |

## The public draft against the sources

| Claim in the draft | Source | Holds |
|---|---|---|
| Both comparisons, opposite orders, favoured AI Security Demos | `mu-final-01.json`: both passes pick team-demos, `order_disagreement` false | yes |
| The clearest difference was usability as delivered | `product` is the only criterion both passes rated decisive, same sign (`mu-final-01.json`). Both passes' product rows rest on the start failure | yes. `functional` has the larger combined margin but was decisive in one order only |
| Following ScribeVault's instructions the app does not start, because the interface imports an undeclared styling package | ev-scribe-02, ev-scribe-03; `runs/team-scribe-app-start-01.json`; `src/gui/qt_app.py:11` against `requirements.txt:25` | yes |
| The error a user sees points to the wrong cause | ev-scribe-02, `main.py:50` | yes |
| AI Security Demos could be run only in part, no model calls and no network | manifest `:14-18`, ev-demos-01, Missing item 1 | yes |
| The first demo's dry run ran, vulnerable and hardened | manifest `:109-110`; both dry-run run records | yes |
| Two state-inspection tools ran | manifest `:111-112`; `list_verdicts` exit 1 on a clean pin, `memory_diff` exit 0 | yes. "Worked" is fair: both report the clean state they exist to report (ev-demos-11) |
| A localhost check refused every hostile address it was given | `runs/team-demos-egress-guards-01.json`: `is_localhost` False for all six non-local forms | yes, for that guard (`T4`) |
| The model-driven acts were not observed | manifest `:114`, Missing items 1-3 | yes |
| No meaningful difference in reliability or innovation | both criteria 0 in both orders | yes |
| Ten self-contained demos | ev-demos-02 (ten directories, stdlib or in-checkout imports, `anthropic` only below the dry-run return) | yes |
| Each with its own presenter guide | ten `NN-*/demo/README.md` at the pin, each laying out its acts. `judgments/team-demos/judge-backend.md:91-97` | yes, by direct read. ev-demos-02 alone establishes ten READMEs, not their content (the F5 erratum) |
| A dry-run mode that prints the exact prompt without calling a model | every one of the ten demo directories holds a `--dry-run` script at the pin. Observed for demo 01 (ev-demos-03) | yes. The sentence claims the mode exists, not that it ran ten times |
| Reset and inspection tools to confirm a clean state | `/reset-demo` commands per demo, `05` via `scripts/reset_demo.py` (`judge-security-ops.md:194`). Inspection per ev-demos-11 | yes |
| ScribeVault: hand-built speaker diarizer, checkpointed recording | `judgments/team-scribe/judge-backend.md:155-161`, source reads of `diarization.py` and `recorder.py:303-454` | yes. The "broken" piece in that passage is the retry pipeline, not the diarizer |
| A large offline test suite | ev-scribe-05: 535 collected, 509 pass offline | yes |
| Well-designed credential storage | ev-scribe-14: keyring first, Fernet with PBKDF2 and a random salt, no plaintext path | yes, with ev-scribe-14's machine-string KDF caveat. For a strengths line that caveat can stay out |

`R2` is gone. The draft no longer says the dry run needs no package install.

## Round-two findings against the source

- **F1, repaired.** See the table. The model-driven acts are now stated as
  unobserved.
- **F6, repaired, with `T2`.** `list_verdicts.py:20-21` prints "Nothing screened
  yet…" and returns 1. `10-show-your-work/demo/README.md:93` describes only the
  summary it prints. The invocation sentence cites `manifest.md:53-55` correctly.
  The egress-probe sentence cites `:112`, the `memory_diff.py` row. The probe row
  is `:113`. `T3` records a smaller over-reach in the same bullet.
- **R3, repaired as scoped, with `T1`.** A file under `_template` or a
  location-only weight dict is now scanned, and the test covers both. The shape
  check tests key presence only. `all()` over an empty `criteria` is true, and no
  top-level key is rejected, so a hand-made file that carries the five result
  keys is exempt whatever else it holds. The real results stay exempt. The per-criterion
  `weight` field inside a real result never matched the pattern. Only the
  per-pass criterion margins did.
- **R4, repaired.** `last_updated` `18:38:31Z` equals the last row. `c4d346e`
  committed at `18:38:37Z`. The round-two row `18:36:46Z` equals the round-two
  `completed_at`.
- **R5, open, correct for now.** The unit reads `not-audited`, and its digest
  `d3d4bf0634d5c669` is not stale. After approval the unit must be re-recorded
  with this report's result.
- **R7, repaired.** `:194` is the enumerated seventeen-file list.
- **F8** (model not the one `event.md:16` requests) is still open for the
  event-director. **F15** is still the approver's decision.

## New findings

- **T1, minor, framework.** The exemption's shape check can be satisfied by
  hand. See the findings entry for the two probes and the repair.
- **T2, minor, event.** `manifest.md:112` should be `:113` in the F6 erratum.
  My round-two repair text gave `:113`. The repair transcribed it wrong.
- **T3, advisory.** "Exited as documented" holds for the `memory_diff.py`
  behaviour, but its "No change" text is only in the script (`memory_diff.py:45`).
- **T4, advisory, accepted.** The localhost sentence is true of
  `fetch_beacons.is_localhost`. The same run shows `resume_parser` v1.1's guard
  passing `evil.example/collect` through to `urllib`, and ev-demos-08 records that
  gap. The draft says "a localhost check", singular, so it is accurate.
- **T5, advisory.** The publication gate has not cleared the draft. It cannot
  clear it from the scratchpad.

## After the rewrite

| Check | Result |
|---|---|
| `python3 -m atj validate reports events/trial-2-2026` | PASS, 28 artifacts, 0 findings |
| `python3 -m pytest tests/ -q` | 518 passed, 5 skipped |
| `python3 -m atj release-check` | PASS |

## Required repairs

Nothing holds the gate.

Before a human approves the public summary:

1. `T5`: place the draft by the sanctioned path and run
   `atj validate publication --event-dir events/trial-2-2026` on it.
2. `F15`: the approver decides on the per-criterion wording.

Before this branch merges, recommended:

3. `T2`: `manifest.md:112` becomes `:113` in the F6 erratum.
4. `T1`: tighten `_is_matchup_result` to the rubric's criterion ids and the
   keys `atj matchup` writes, with the two probes as tests, or record a W entry.
5. `R5`: after `atj event approve` on this report, re-record
   `matchup:mu-final-01` with its audit result.
6. `F8`: event-director decision.

Re-audit the next repair diff. Three rounds running, a repair has introduced a
defect. This round it was a transcription error in a citation.

**Verdict: PASS WITH ADVISORIES. No blocking finding. `tournament-audited` may
be set after `atj event approve` on this report.**

---

# Judging Audit — tournament stage, round two (superseded, retained)

## Result

**PASS WITH ADVISORIES.** No finding is blocking. Of the seventeen round-one
findings, eleven are repaired or accepted, three are deferred to the plan, and
four stay open: `F1` (major, uncommitted draft), `F6`, `F8` and `F15`. The
repair added seven findings. `R1` is repaired. `R2`, `R3`, `R4`, `R5` and `R7`
are open, and `R6` is accepted. No decision artifact changed a value. The pass
files are byte-unchanged since 77fcc6a, and `mu-final-01.json` is unchanged.

`tournament-audited` may be set once this report is approved. Nothing in
`findings:` blocks the gate. `F1` and `R2` must be repaired before any human
approves the public summary, whatever the gate does.

## Scope and artifacts inspected

- `git diff 36cd3d5..aa0de72` and the 18:29:57Z activity-log row, checked against
  the sources and not against my round-one repair text.
- The draft public summary at the orchestrator's scratchpad path, as edited in
  place.
- `atj/cli.py` `check_no_duplicate_weights`, probed with hand-written files.
- Every erratum citation, and the F3/F4 paragraph, against the pass files,
  `audits/judgments.md`, `framework/rubrics/head-to-head.md`, both teams'
  judgments and `evidence/team-demos/manifest.md`.
- `status.md`, `atj event unit ... list`, `atj.event.derive_digests`, and
  `git log --format='%h %cI'`.
- `docs/0.5.0-beta-plan.md` W21-W23 and the H4 amendment, against
  `atj/publication.py:84-89`, `schemas/common.schema.json:15-18`,
  `atj/ids.py:157`, both matchup templates, and `43e7e50`'s H4 text.

## Deterministic validation results

| Check | Result |
|---|---|
| `python3 -m atj validate reports events/trial-2-2026`, at aa0de72 | PASS, 28 artifacts, 0 findings |
| `python3 -m pytest tests/ -q`, at aa0de72 | 6 failed, 513 passed, 5 skipped. All six fail on the weight check reading this report (`R1`) |
| `python3 -m atj release-check`, at aa0de72 | FAIL, `single-source`, this report (`R1`) |
| The same three after this rewrite | recorded under "After the rewrite" below |
| `atj event unit events/trial-2-2026 list` | 2 units, 0 stale |
| `derive_digests` for `matchup:mu-final-01` | `1d4f5a970e3f5dc9`, equal to the recorded digest |
| Weight check probe: a matchup result under `events/e/matchups/` | exempt |
| Probe: hand-written weight dict at `events/_template/matchups/weights.json` | **exempt** (`R3`) |
| Probe: the same copy in `.yaml`, `.md`, or one directory deeper | caught |

## Round-one findings against the source

**F1.** The draft now says the dry run went through "a direct Python invocation
rather than the documented `uv` command". That half is right. The sentence
before it still reads "Every part of AI Security Demos that could run in this
event worked". The manifest's execution table (`evidence/team-demos/manifest.md:105-114`)
records six executions: an environment probe, demo 01's two act-1 dry runs,
`list_verdicts.py`, `memory_diff.py`, and an event-written egress probe. The
dry runs of demos 02-10 were not run, and the table does not record them as
unrunnable. So "could run" claims more than the event observed. The draft also
never says that acts 2 and 3, which need a model, were not observed. My
round-one repair suggested "the offline parts that could run behaved as
described", which contains the same error. The repair followed my text. The
fault is in the text.

**F2.** The integer pattern `(\d+)` is back, so float and sentence-final copies
are caught again. The exemption skips a file when its path relative to the root
has exactly four parts, `events/<x>/matchups/<name>.json`. It is narrow in depth
and suffix. The probes above show that `.yaml`, `.md` and deeper paths are still
scanned. The new test writes a margin into `events/e/matchups/mu-final-01.json`,
plus an integer JSON copy, a float JSON copy and a prose copy at the root. It
requires all three copies to be caught and none of the problems to name
`matchups`. That covers what round one asked for. The hole is `R3`. The
exemption trusts any JSON in that directory, including `events/_template/`,
which is copied into new events. The comment says the file is exempt "by what
it is", but nothing checks what it is. The matchup result also carries a
literal `weight` field per criterion. The pattern cannot see it, because the key
is `weight` and not a criterion id. That is tool output, not a new copy.

**F3.** Pass A (`:70`) cites consolidation F2 and N6, judgments F1 and F19, and
judgments F4 and F18. Pass B cites judgments F1 (`:54`), consolidation F1 (`:55`,
`:89`), consolidation F2 (`:56`) and judgments F4 (`:69`, "verified by judgments
audit F4"). Every attribution in the new paragraph matches. So does "both use
the three-of-five count".

**F4.** `head-to-head.md:12` reads "Do not merely select the team with the
higher initial total." The quote is exact.

**F5 erratum.**
- `ev-demos-02` (`manifest.md:91`) records counts and the dependency surface,
  with no template claim. Correct.
- `judgments/team-demos/judge-security-ops.md:49`, `:165` and `:185` each name
  the `Bash(rm:*)` grants. `:194` holds the enumerated list and is omitted
  (`R7`). The erratum is correct as far as it goes.
- `judgments/team-scribe/judge-security-ops.md:137` says `recover_checkpoints()`
  is "entirely unobserved". Correct.
- `judgments/team-scribe/judge-backend.md:113` names `retry_worker.py`'s
  undefined names, and `:117` says "the feature is dead ... converts the
  `NameError` into a log line". Correct.

**F6 erratum.** `manifest.md:53-55` says the dry run is "*not* the invocation
the submission documents". Correct. The rest is `F6`, still open: the exit-1
claim is uncited, the egress probe is not addressed, and "holds for the
documented output" is false for `list_verdicts.py`.

**F13 erratum.** `audits/judgments.md` F18 says "None made", and F19 says the
rationales "check out". The erratum sends the reader there. Correct.

**F14.** `mu-final-01.md:46-48` states that the independence and extraction
facts rest on the orchestrator's record. Correct.

**F7, ledger and unit.** Checked against `git log --format='%h %cI'`:

| Row | Against | Holds |
|---|---|---|
| 17:26:17Z passes judged | pass B `completed_at` 17:26:17Z. Pass A starts 17:23:53Z, pass B 17:24:01Z | yes |
| 17:28:59Z committed 77fcc6a | `77fcc6a 2026-09-23T13:28:59-04:00`. 36cd3d5 at 17:30:42Z | yes |
| 18:27:09Z round-one audit | this report's round-one `completed_at` | yes |
| 18:29:57Z repair | `aa0de72` at 18:30:04Z, after the row. The draft's mtime is 18:28Z | yes |
| `last_updated` 18:29:45Z | the last row, 18:29:57Z | **no** (`R4`) |

The unit's inputs are the report, the JSON and both passes
(`atj/event.py:977-989`). The unit lists only the report as an output, but the
digest covers all four, so drift in any of them is caught. The unit's
`audit_result` is `R5`, and its `completed_at` is `R6`. The repair row's claim
"float and prose copies tested as still caught" is true.

**F8 options.** The event-director can:
- **O1.** Accept by a dated `status.md` row. It would name `matchup-judge`'s
  `model: inherit` as the cause and note that both orders shared one model, so
  order balance holds. It would also record as a limitation that the panel and
  the matchup ran on different models. This is the cheapest option and enough if
  `model_requested` in `event.md` is read as covering the panel only.
- **O2.** Record an override under `overrides/`, the way this event handled
  disclosure. This fits if `event.md:16` is binding for every agent in the
  event. It leaves a record a later audit can cite by id.
- **O3.** Re-run both passes with `claude-opus-5` explicitly requested,
  re-resolve with `atj matchup`, and re-audit. The unit goes stale and the
  stage repeats. At a combined margin of 50 with a band of 5, the outcome is
  unlikely to move. The only gain is conformance, and the re-run adds a second
  sample to H5.
- Editing `event.md:16` is not an option. It is frozen configuration after
  judging began, per `CLAUDE.md`.

**Plan entries.** W21 is accurate. The pattern is at `atj/publication.py:88`,
the schema accepts 7-64 hex at `schemas/common.schema.json:17`, and the template
requires the field at `framework/templates/public-matchup-summary.md:6`. W22 is
accurate as to what I placed in the draft and what cleared. W23 is accurate: the
pattern needs `:` or `=`, and the templates carry a Weight column at
`matchup-pass-report.md:59` and `matchup-report.md:43`. No W entry was needed for
`F2`, because it was fixed. `R3` is not in the plan. The H4 amendment quotes the
old text exactly and leaves the **Kills it** line unchanged.

## Restated examples in this report

The requested restatement: `release-check` read the round-one F2 table as seven
weight copies. They were at lines 328 and 336-340 of the round-one text. The
table now puts the criterion and the value in separate columns, and the prose
line names the value in words. Each row still evidences the same probe result.
The reproduction line at round-one lines 213-214 never matched the pattern. No
value there equals its weight, and I scanned it with the live pattern. I left it
as written.

## After the rewrite

| Check | Result |
|---|---|
| `python3 -m atj validate reports events/trial-2-2026` | PASS, 28 artifacts, 0 findings |
| `python3 -m pytest tests/ -q` | 518 passed, 5 skipped |
| `python3 -m atj release-check` | PASS |

`R1` is repaired by this rewrite alone. No other file changed.

## Required repairs

None holds the gate. Before any human approves the public summary:

1. `F1`: "that could run" becomes what was run, plus one sentence saying the
   acts needing a model were not observed.
2. `R2`: qualify "needs no ... package install".

Before this branch merges, recommended:

3. `F6`: finish the erratum with the two citations and the egress-probe sentence.
4. `R3`: tighten the exemption, or add a W entry.
5. `R4`, `R5`: fix `last_updated`, and re-record the unit's audit result after
   approval.
6. `F8`: an event-director decision, O1 to O3.

Re-audit whatever repair diff follows. This is the second round in which a
repair introduced a defect, and the second in which my own repair text carried
one.

**Verdict: PASS WITH ADVISORIES. No blocking finding. `tournament-audited` may
be set after `atj event approve` on this report.**

---

# Judging Audit — tournament stage, round one (superseded, retained)


## Result

**PASS WITH ADVISORIES.** Seventeen findings: two major, nine minor and six
advisory. None is blocking. The match result reproduces exactly from comparisons
this audit extracted itself. Both passes cite evidence for every nonzero
comparison. No total, affiliation or presentation order was used as evidence. No
private identifier is in the draft public summary.

The gate may be set mechanically. This event's practice has been to repair and
re-audit before gating, and I recommend that here. `F1` and `F11` must be
repaired before any human approves the public summary, whatever the gate does.
`F2` is a framework defect committed on this branch and should not merge
unrecorded.

## Scope and artifacts inspected

- `git diff 43e7e50..HEAD`: 77fcc6a (two pass reports, `matchups/mu-final-01.json`
  and `.md`, and the H4 edit) and 36cd3d5 (`atj/cli.py`, `tests/test_canonical_model.py`).
- `matchup-passes/mu-final-01-pass-a-first.md` and `-pass-b-first.md`.
  I resolved every file:line, evidence-id and run-record citation behind a
  nonzero comparison, and most behind the zeros. The sources were the event's
  artifacts, and for submission lines the pinned checkouts under
  `workspaces/trial-2-2026/`. Both are at their pins, `dc35f69…` and `67969dd…`,
  with clean trees.
- `audits/judgments.md` F1, F4, F12, F18 and F19, and `audits/consolidation.md`
  F1, F2, F17, F28 and N6.
- The draft public summary at the orchestrator's scratchpad path
  `…/scratchpad/public/mu-final-01.md`, which is not committed.
- `framework/rubrics/head-to-head.md`, `framework/rubrics/submission-evaluation.md:106`,
  `.claude/agents/matchup-judge.md`, `.claude/skills/judge-matchup/SKILL.md`,
  `framework/templates/public-matchup-summary.md`, `atj/publication.py`, `atj/matchup.py`.

Out of scope: re-judging the match, and the bracket advance. Submission content
was read as data only. I read no instruction from it and followed none. The
pre-advance hook refused one of my `grep` commands because it named a submission
script beside the word `python3`. I re-ran it without executing anything.

## Deterministic validation results

| Check | Result |
|---|---|
| `python3 -m atj validate reports events/trial-2-2026` | PASS, 27 artifacts, 0 findings |
| `python3 -m pytest tests/ -q` | 518 passed, 5 skipped |
| `python3 -m atj release-check` | PASS |
| `atj matchup` on comparisons extracted by this audit from the two pass front matters | byte-identical to `matchups/mu-final-01.json` after key sort (`diff` empty, `==` true) |
| Pass front matter against pass prose tables | all fourteen values agree |
| `atj validate publication` on the draft, copied into a scratch copy of the event's `public/` | BLOCKED only on `approval_state: draft` and `approved_by: null`. With the full `framework_commit` restored, it also blocks `private-identifier` (see F9) |
| Same draft with approval fields set, plus appended short commits, a repository URL, the affiliation and "+50"/"40" margins | CLEAR (F10) |

## Reproduction

I read the input from the two pass files, not from the orchestrator's `mu-input.json`:
A-first `{functional: 1, product: 2, agentic: 0, engineering: 1, reliability: 0,
security: 1, innovation: 0}` presented_first team-demos, and B-first `{-2, -2, -1,
-1, 0, -1, 0}` presented_first team-scribe. `atj matchup --event-dir` gives
combined margin 50.0, outcome `confirmed`, winner `team-demos`, no order
disagreement. The file matches exactly. The negation of B-first sits in
`atj/matchup.py:61`, inside the cited `:42-70`. `atj/matchup.py` is unchanged
since 43e7e50.

## Citations behind nonzero comparisons

The following resolve and say what the passes claim:

- `runs/team-scribe-app-start-01.json`: exit 1, `No module named 'qdarkstyle'`,
  the misleading PySide6 message, and the log-file degradation.
- `src/gui/qt_app.py:11` (`import qdarkstyle`), `requirements.txt:25`
  (`pyqtdarktheme`) and `main.py:50` (`except ImportError`) at the pin.
- Team-scribe manifest `:79-89`, `:104`, `:116-129` and `:168-171`, and team-demos
  manifest `:20-23`, `:53-63`, `:79`, `:91-100` and `:130-138`.
- `SECURITY.md:25` (escaping) and `:34` (pinning).
- `judgments/team-scribe/judge-backend.md` `:75-77`, `:85-91`, `:99-103`,
  `:113-119`, `:127-133`, `:141-145` and `:153-161`.
- `judgments/team-scribe/judge-security-ops.md:153`.
- `judgments/team-demos/judge-backend.md` `:91-97`, `:105-111`, `:123-129`,
  `:137-143`, `:156` and `:168-174`.
- `summaries/team-demos.md:488-512` and `:661-681`, `summaries/team-scribe.md:335-346`.
- `adj-trial-2-2026-team-scribe-agentic.md:26-36`.
- `head-to-head.md:5` and `:7`, and `submission-evaluation.md:106`.
- Pass B's 20 `=== Applicant file:` headers and 20 `<applicant file=` tags are
  exact. The vulnerable dry run has 20 and 0, and the hardened one has 0 and 20.

**Pass B's egress claim holds.** "The egress guard refused all six hostile URL
forms" is exactly what `runs/team-demos-egress-guards-01.json` shows for
`fetch_beacons.is_localhost`. It returns `False` for `evil.example`,
`localhost@evil.example`, `127.0.0.1.evil.example`, `file:///etc/passwd`,
`0.0.0.0` and `2130706433`, and `True` for the three local forms, with
`ALLOWLIST = set()`. That guard is not the v1.1 POST guard. Pass B's security
cell never makes a claim about the v1.1 guard, so the six-of-six statement is
consistent with the three-of-five correction the pass lists at `:56`.

**Pass A states the three-of-five correction correctly**, including the
schemeless form rejected by `urllib`. The run record matches: `RuntimeError` for
`http://evil.example/collect`, the userinfo form and `//evil.example/collect`,
`ValueError` for `evil.example/collect`, and `URLError` for the loopback form.

**Consolidation F1 (single-judge `.env`).** Pass B labels the claim "one judge"
and says it adds to, and does not carry, the `-1`. Pass A cites only
`judge-security-ops.md:153` and claims no corroboration, so it does not repeat
the F1 error either. It also does not cite F1 (F3).

The citations that do not carry their claims are in F5, F6 and F13. None of them
is the only support for any nonzero value.

## Totals, affiliation, presentation order

Neither pass mentions an affiliation, a repository, a school, a seed or a bye.
The only mention of the bracket is pass B's statement that it does not advance
it. Both passes state that no total was used. The only scores quoted are pass A's
per-criterion panel splits (3/3/NE/NE and 2/3/NE/NE). Pass A cites them to
explain why it did not convert scorability into an advantage, which is the
opposite of selecting on them. Presentation order appears only as the structural
fields. Both passes cite `teams.md:11-12` for eligibility, and those lines also
carry the affiliation and repository URLs. Nothing from those columns appears in
either pass.

## Double counting (F12)

`submission-evaluation.md:106`: "Confirmed inability to complete the primary
advertised workflow must materially affect `functional` and any dependent
criteria." The rubric requires propagation to `product`. `engineering` rests on
the undeclared dependency, which is an engineering defect in its own right, and
also on the inert `pytest.ini`, the inverted conftest mock and the `NameError`
retry worker. None of those comes from the launch record. So the propagation is
legitimate. It does not inflate the result into a different outcome. I zeroed
`functional` and `product` in both passes and re-ran `atj matchup`: combined
margin 16.25, confirmed, team-demos. Zeroing `engineering` as well gives 8.75,
still confirmed and outside the band of 5. These are audit sensitivity runs, not
official figures. The launch record does concentrate the margin. It does not
decide it.

## mu-final-01.md

Every table value, margin, outcome and tie-break statement matches the JSON and
the passes. Front matter `started_at`/`completed_at` is the earliest and latest
of the two pass stamps. The `model_used` paragraph is accurate. "Pass B does not
discuss it" (double counting) is accurate, and so is the "-1 in its orientation"
reading of pass B's hedge. The defects are F3 and F4. The timestamps and the
independence and extraction statements in the Audit block are orchestrator
attestations (F14). The reproduction above confirms that the pass files match
the JSON. It cannot confirm that the pass files match the transcripts.

## Draft public summary

Accurate: the winner, the two-order statement, the ScribeVault launch failure,
its cause and the misleading message, the localhost guards holding against
hostile input, the absence of a difference on reliability and innovation, and
the ScribeVault strengths. The strengths are the diarizer, checkpointed
recording, the large offline suite, and credential storage that is sound by
static read (`ev-scribe-14`).

Defects: F1 and F11. The draft carries no private identifier, score, judge name
or deliberation marker. It omits the commits and IDs as its privacy note says.
Its only source is `matchups/mu-final-01.md`, which is correct for a derived
summary. Its timestamps are the transcript-sourced ones (F14).

**`framework_commit`.** This is a framework finding (F9). The template requires
the field. `ids.py:157` defines it as 7-64 hex. The gate's `\b[0-9a-f]{40}\b`
cannot tell the framework's own commit from a submission commit. The framework
commit identifies public framework code, not a team, so it is not private. The
7-character form is an acceptable workaround here, and the defect belongs in the
next framework window. F10 is the other side of the same scan. The gate blocks a
harmless 40-hex value and clears a short submission commit, a repository URL,
the affiliation and integer margins. That is direct evidence for H4.

## 36cd3d5 (F2)

The old pattern flagged the `product` criterion margin in `mu-final-01.json`,
written there as the float fifteen point zero, because `(\d+)`
matched the `15`. The added `(?![.\d])` fixes that. Backtracking cannot defeat
it, because `1` followed by `5` also fails the lookahead. It also stops the
check from matching any weight written as a float, or at the end of a sentence.
I compiled both patterns against the live rubric:

Restated in round two so the criterion and the value sit in separate columns:

| Input shape | Criterion | Value written | Old | New |
|---|---|---|---|---|
| JSON key, as in the matchup margin | product | 15.0 | flagged | clear |
| Python dict literal of floats | functional, product | 25.0, 15.0 | flagged | **clear** |
| Python assignment with `=` | functional | 25.0 | flagged | **clear** |
| prose `criterion` then `:` then value, sentence-final | product | "15." | flagged | **clear** |
| JSON key with an integer value | product | 15 | flagged | flagged |
| Markdown table row | product | 15 | clear | clear (F17) |

A float weight dict is the most likely shape for a Python copy used in
arithmetic, and alpha defect X1 was a Python dict. The fix trades a false
positive in one generated file for a false negative across the tree. The new
test asserts only the integer case and the matchup case, so nothing would catch
the regression. The exemption should key on what the file is, not on how the
number is written. The fix had to land, because release-check failed on a
tool-generated event artifact. Its shape is the defect.

## H4 edit (F16)

The old line said "`public_scores` set so that public artifacts exist". The
event instead approved publication by override and kept `public_scores: false`.
The new line separates the disclosure decision from `public_scores` and notes
that the score scan stays active. That is a correct description of how the two
controls divide, and the **Kills it** line is untouched, so the hypothesis is no
easier to survive. `docs/0.5.0-beta-plan.md:327` (D2) makes hypotheses
pre-registered. Editing one in place during the event it is being tested in
should leave a visible amendment, not only a commit message.

## Findings

| Severity | Rule | Artifact | Scope | Blocking | Finding | Required repair |
|---|---|---|---|---|---|---|
| major | public accuracy | draft `public/mu-final-01.md` "Why" | event | no | `F1`. "Every part of AI Security Demos that could run in this event ran as its documentation describes." The manifest records that the dry run uses "*not* the invocation the submission documents" (`evidence/team-demos/manifest.md:53-55`) and that the documented `uv` path is unreachable offline. `list_verdicts.py`'s exit 1 is at `:20-21` of the script and absent from `10-show-your-work/demo/README.md:93`. The egress probe is an audit harness, not a documented use. A ceremony reader would take this as the documented workflow working | Restate to what `ev-demos-03`/`ev-demos-11` support, and say that the model-driven acts were not observed. Re-check before approval |
| major | single source | `atj/cli.py:1760-1765` | framework | no | `F2`. The `(?![.\d])` exemption clears every float-typed or sentence-final weight copy (table above). The new test covers neither | Exempt `atj matchup` output by provenance. Restore the number match. Add a float-dict regression test. Or defer with a W entry |
| minor | report accuracy | `matchups/mu-final-01.md:61-66` | event | no | `F3`. "Both passes applied … consolidation F1 … consolidation F2 and N6". Pass A never names consolidation F1 (`pass-a:70` names F2, N6, judgments F1, F19, F4 and F18). Pass B never names N6 (`pass-b:53-56`) | Attribute per pass |
| minor | citation | `matchups/mu-final-01.md:59` | event | no | `F4`. "`head-to-head.md` forbids selecting on them". `head-to-head.md:12` says "Do not merely select". Consolidation F28 flagged this paraphrase and warned that the bracket stage would inherit it | Quote the rubric |
| minor | citation | `pass-a-first.md` product, security, reliability cells | event | no | `F5`. (a) "ten presenter READMEs on one template (`ev-demos-02`…)". `ev-demos-02` records counts only, as consolidation F17 found, and `judge-backend.md:91` generalizes from demo 01. (b) "`Bash(rm:*)` grants (`judge-security-ops.md:151-161`)". The grants are at `:165` and `:194`. (c) "its recovery feature is dead (`judge-security-ops.md:135-139`)". That judge never mentions `retry_worker` or `NameError`, and the support is `judge-backend.md:113-119,131`. (a) and (b) sit behind the `+2` product and the "why only +1" security qualifier. Both values stand on the other citations in their cells | Erratum in `mu-final-01.md` "Conflicting evidence"; pass files and values untouched |
| minor | claim stronger than source | `pass-b-first.md:81` | event | no | `F6`. "All five of its offline executions exited as documented, including `list_verdicts.py`'s documented exit 1." No README documents the exit status. The dry runs used the undocumented invocation pass B itself cites at `:86`. The claim sits in the functional decisive-evidence paragraph, and the `-2` rests on team-scribe's failure, which the pass says is the main support | Erratum, as F5 |
| minor | ledger | `status.md` | event | no | `F7`. No activity-log row for 17:23:53Z-17:26:17Z, the resolution or 36cd3d5. No match unit. `last_updated: 14:52:55Z` | Add the rows and the unit, and derive `last_updated` |
| minor | version and identity | pass front matter; `event.md:16` | event | no | `F8`. `model_requested: opus`, `model_used: claude-opus-5-5[1m]`, against the event's `claude-opus-5`. `matchup-judge` is `model: inherit`. `mu-final-01.md:47-49` discloses the model. Nothing records a decision to accept it | Record the decision. No re-run is required, because both orders share the model |
| minor | gate design | `atj/publication.py:88` | framework | no | `F9`. The full-hash pattern blocks the `framework_commit` the public template requires | Exempt that field or specify the short form. W entry |
| minor | gate coverage | `atj/publication.py:84-108` | framework | no | `F10`. CLEAR on short submission commits (`dc35f69`, `67969dd9479c`), `https://github.com/beekeeper-lab/ScribeVault`, `beekeeper-lab`, "+50" and "gave 40" | W entry. Cite as H4 evidence |
| minor | public accuracy | draft "Both teams did well" | event | no | `F11`. "one consistent template" is supported for five of ten guides (`judgments/team-demos/judge-security-ops.md:89,95`). "standard library only" is wrong for the documented API path (`manifest.md:55-59`) | Soften both, as in the front matter |
| advisory | double counting | `runs/team-scribe-app-start-01.json` | event | no | `F12`. Legitimate per `submission-evaluation.md:106`. Sensitivity runs give 16.25 and 8.75, both confirmed | None |
| advisory | carry-forward | `pass-a-first.md:70` | event | no | `F13`. F19 is described as a withdrawal and F18 as adding a filter. Neither matches the audit | Fold into the F5 erratum |
| advisory | unverifiable | pass timestamps; `mu-final-01.md` Audit block | event | no | `F14`. The transcripts, the concurrent launch and the non-exposure of each judge to the other are orchestrator-attested. The pass contents are consistent with independence: different value on agentic, different formatting, and pass B lacks a double-counting section | Record as attested |
| advisory | disclosure | draft "Why" | event | no | `F15`. Per-criterion outcomes disclosed in words | Approver decides |
| advisory | pre-registration | `docs/0.5.0-beta-plan.md:112-114` | framework | no | `F16`. Correct edit with no amendment note | Add a dated note |
| advisory | single source | `atj/cli.py:1751-1765`; both matchup templates | framework | no | `F17`. Markdown tables are invisible to the check, and the templates mandate a Weight column | Framework window |

## Advisories

Pass B was worth having. It disagrees with pass A on `functional` (−2 against
+1 in A's orientation) and on `agentic`, and both passes say why in their own
conflicting-evidence sections. Two passes that agreed on every value would have
told the event less about order sensitivity than these do. Pass B's own hedge
("could reasonably land at -1") names pass A's value without having seen it.

## Completion gate

- [x] No blocking findings
- [ ] No major findings: `F1` (event, uncommitted draft) and `F2` (framework)
- [x] Calculations valid: `atj matchup` reproduces `mu-final-01.json` exactly from independently extracted input
- [ ] Evidence references resolve: every nonzero value has resolving support, but `F5`, `F6` and `F13` resolve to text that does not carry the claim
- [x] Version and identity checks pass: `head-to-head@1.1.0`, `submission-evaluation@1.1.0`, `matchup-judge@1.1.0` current in `framework/personas.md:40`. Pins and package IDs match both manifests. Model deviation recorded as `F8`
- [x] Privacy boundary passes: `public/` empty, draft carries no private identifier, score or judge name. `public_scores: false` unchanged
- [x] Every finding recorded in `findings:` with a `scope` and a `blocking` flag
- [ ] Approved with `atj event approve <this file>`

## Required repairs

These are needed before the gate, by this event's practice. The gate is not held
mechanically.

1. `F1`, `F11`: rewrite the two sentences in the draft public summary. This must
   be done before any approver reads it for publication.
2. `F3`, `F4`: two sentences in `matchups/mu-final-01.md`.
3. `F5`, `F6`, `F13`: one erratum paragraph in `matchups/mu-final-01.md` with the
   corrected citations. Do not edit either pass file or any value.
4. `F7`, `F8`: ledger rows, the match unit, and a recorded decision on the model.
5. `F2`: fix it with a provenance-based exemption and a regression test, or
   record it as a W entry before this branch merges. `F9`, `F10`, `F16` and
   `F17` go to the plan.

Re-audit the repair diff. Every repair round in this event so far has introduced
new defects.

**Verdict: PASS WITH ADVISORIES. No blocking finding; `tournament-audited` may be
set.**
