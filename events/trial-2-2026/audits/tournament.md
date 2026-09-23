---
event_id: trial-2-2026
audit_scope: tournament stage, round one — the two mu-final-01 pass reports, the atj matchup result and its private report, the draft public summary, the release-check fix 36cd3d5, and the H4 edit in docs/0.5.0-beta-plan.md
audit_id: tournament
team_id: null
match_id: mu:trial-2-2026:final:01
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.1.0
persona: judging-auditor@1.1.0
framework_commit: 36cd3d5ae05923f66de797b26a5f7d7eca701dd9
model_requested: claude-opus-5
model_used: claude-opus-5-5[1m]
started_at: "2026-09-23T18:05:00Z"
completed_at: "2026-09-23T18:27:09Z"
visibility: private
approval_state: draft
validation_state: unvalidated
result: PASS WITH ADVISORIES
findings:
- id: F1
  severity: major
  scope: event
  blocking: false
  summary: the draft public summary says every runnable part of AI Security Demos "ran as its documentation describes"; the approved manifest records that the dry run used an invocation the submission does not document, and list_verdicts' exit 1 is documented nowhere
  artifact: scratchpad draft public/mu-final-01.md (not yet under events/trial-2-2026/public/)
  repair: restate as what the manifest supports, e.g. that the offline parts that could run behaved as described, through an event-chosen invocation, and that the headline acts needing a model were not observed. Re-check before a human approves it
  state: open
- id: F2
  severity: major
  scope: framework
  blocking: false
  summary: 36cd3d5 makes check_no_duplicate_weights blind to every float-typed weight copy and to a weight at the end of a sentence; it exempts by number shape, not by provenance
  artifact: atj/cli.py:1760-1765; tests/test_canonical_model.py:79-98
  repair: exempt atj matchup output by provenance (the criterion_margins and criteria blocks of a matchup result, or events/*/matchups/*.json), restore the old number match elsewhere, and add a test that a float weight dict in a .py still fails. Record in docs/0.5.0-beta-plan.md if deferred
  state: open
- id: F3
  severity: minor
  scope: event
  blocking: false
  summary: mu-final-01.md says both passes applied consolidation F1 and consolidation N6; pass A never cites consolidation F1 and pass B never cites N6
  artifact: matchups/mu-final-01.md:61-66 (the paragraph beginning "Both passes applied")
  repair: say which pass cited which correction. Pass A cites consolidation F2 and N6, judgments F1, F19, F4 and F18. Pass B cites judgments F1, consolidation F1, consolidation F2 and judgments F4
  state: open
- id: F4
  severity: minor
  scope: event
  blocking: false
  summary: mu-final-01.md says head-to-head.md "forbids selecting on" totals; the rubric says "Do not merely select", the paraphrase consolidation F28 already flagged
  artifact: matchups/mu-final-01.md:59
  repair: quote head-to-head.md:12
  state: open
- id: F5
  severity: minor
  scope: event
  blocking: false
  summary: three pass A citations do not carry their claims (ev-demos-02 for a shared README template, judge-security-ops.md:151-161 for Bash(rm:*), judge-security-ops.md:135-139 for a dead recovery feature). No comparison value depends on them
  artifact: matchup-passes/mu-final-01-pass-a-first.md:79,82,83
  repair: record the corrected citations as an erratum in matchups/mu-final-01.md. The template ships no amendment mechanism for a pass, so do not hand-edit the pass file or its values
  state: open
- id: F6
  severity: minor
  scope: event
  blocking: false
  summary: pass B says all five team-demos offline executions "exited as documented, including list_verdicts.py's documented exit 1"; the exit 1 exists only in code, and the dry runs used an undocumented invocation the pass itself cites
  artifact: matchup-passes/mu-final-01-pass-b-first.md:81
  repair: erratum in matchups/mu-final-01.md, as for F5
  state: open
- id: F7
  severity: minor
  scope: event
  blocking: false
  summary: status.md records no row and no unit for the two passes, the atj matchup resolution or 36cd3d5; last_updated is still 14:52:55Z
  artifact: status.md
  repair: add activity-log rows for the passes, the resolution and the framework fix, record the match as a ledger unit as bracket audit F12 did for the draw, and derive last_updated from the last row
  state: open
- id: F8
  severity: minor
  scope: event
  blocking: false
  summary: both passes requested "opus" and ran claude-opus-5-5[1m]; event.md:16 requests claude-opus-5 and the panel ran claude-opus-5. mu-final-01.md records the fact but no one authorized it
  artifact: matchup-passes/*.md front matter; event.md:16
  repair: record in status.md, or in an override if the event-director treats model_requested as binding, that the matchup model was inherited from the orchestrating session and why that is acceptable. Both passes used the same model, so order balancing is intact
  state: open
- id: F9
  severity: minor
  scope: framework
  blocking: false
  summary: the publication gate blocks a 40-hex framework_commit as a private identifier, although the public template requires the field and ids.py:157 accepts 7-64 hex. The sample event never hits this because it uses "uncommitted"
  artifact: atj/publication.py:88; framework/templates/public-matchup-summary.md:6; atj/ids.py:157
  repair: exempt the framework_commit front-matter value, or make the template specify the abbreviated form. Defer to a W entry. The draft's 7-character 43e7e50 is an acceptable workaround for this event
  state: open
- id: F10
  severity: minor
  scope: framework
  blocking: false
  summary: atj validate publication reports CLEAR on an approved public artifact that carries abbreviated submission commits, a repository URL, the affiliation group and integer matchup margins
  artifact: atj/publication.py:84-108
  repair: framework scope. Record it against H4, whose kill condition is a raw score or private detail reaching a public artifact while validation passes. The draft contains none of these
  state: open
- id: F11
  severity: minor
  scope: event
  blocking: false
  summary: the draft public summary's "Both teams did well" overstates two facts. "Ten presenter guides on one consistent template" rests on one judge's generalization from demo 01 (a second judge read five of ten). "Standard library only" ignores the documented API path, which needs the anthropic SDK
  artifact: scratchpad draft public/mu-final-01.md
  repair: e.g. "presenter guides with a shared structure" and "no third-party dependency on its offline paths"
  state: open
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
  summary: pass A says judgments F19 withdraws the .env.example defect and F18 "adds the placeholder filter"; F19 accepts the rewritten product rationales and F18 records that no repair was made
  artifact: matchup-passes/mu-final-01-pass-a-first.md:70
  repair: note in the F5 erratum. It has no effect on any value
  state: open
- id: F14
  severity: advisory
  scope: event
  blocking: false
  summary: the pass timestamps, the concurrent launch, the claim that neither judge saw the other or matchups/, and the transcript extraction are unverifiable by this audit
  artifact: matchup-passes/*.md started_at/completed_at; matchups/mu-final-01.md:42-46,134-145
  repair: none possible from the repository. Record them as orchestrator-attested, not audited
  state: accepted
- id: F15
  severity: advisory
  scope: event
  blocking: false
  summary: the draft public summary discloses per-criterion comparison outcomes ("no meaningful difference in reliability or innovation"). It is not numeric and not blocked, so disclosing it is the approver's decision
  artifact: scratchpad draft public/mu-final-01.md
  repair: approver decides
  state: open
- id: F16
  severity: advisory
  scope: framework
  blocking: false
  summary: the H4 observation line was rewritten mid-event with no amendment note. The substance is a correction and the kill condition is unchanged, so the test is not weakened
  artifact: docs/0.5.0-beta-plan.md:112-114
  repair: add a dated amendment note naming commit 77fcc6a and the disclosure override as the reason
  state: open
- id: F17
  severity: advisory
  scope: framework
  blocking: false
  summary: check_no_duplicate_weights cannot see a Markdown table although its docstring names one, and both matchup templates put a Weight column in every report
  artifact: atj/cli.py:1751-1765; framework/templates/matchup-pass-report.md:59; framework/templates/matchup-report.md:43
  repair: framework window. Either drop the Weight column from the templates or document the column as a rendered read of the rubric
  state: open
---

# Judging Audit — tournament stage, first pass

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

The old pattern flagged `"product": 15.0` in `mu-final-01.json` because `(\d+)`
matched the `15`. The added `(?![.\d])` fixes that. Backtracking cannot defeat
it, because `1` followed by `5` also fails the lookahead. It also stops the
check from matching any weight written as a float, or at the end of a sentence.
I compiled both patterns against the live rubric:

| Input | Old | New |
|---|---|---|
| `{"product": 15.0}` (the matchup margin) | flagged | clear |
| `WEIGHTS = {"functional": 25.0, "product": 15.0}` | flagged | **clear** |
| `functional = 25.0` | flagged | **clear** |
| `product: 15.` in prose | flagged | **clear** |
| `"product": 15` | flagged | flagged |
| `\| product \| 15 \|` | clear | clear (F17) |

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
