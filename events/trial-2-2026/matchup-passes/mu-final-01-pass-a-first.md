---
event_id: trial-2-2026
match_id: mu:trial-2-2026:final:01
round_id: final
team_a: team-demos
team_b: team-scribe
commit_a: dc35f6962130af5e5be3fe16672e3d4964850eb9
commit_b: 67969dd9479c096f05d998d8c50e5ea1968e3245
evidence_package_a: ev:trial-2-2026:team-demos:dc35f6962130:cb3847cb
evidence_package_b: ev:trial-2-2026:team-scribe:67969dd9479c:018cf089
rubric: head-to-head@1.1.0
source_rubric: submission-evaluation@1.1.0
persona: matchup-judge@1.1.0
framework_commit: 43e7e50ca414393333faa0d5e1d470a7a8df5a9c
model_requested: opus
model_used: claude-opus-5-5[1m]
started_at: "2026-09-23T17:23:53Z"
completed_at: "2026-09-23T17:26:10Z"
close_call_band: 5
presentation_order: a-first
passes:
  a_first:
    presented_first: team-demos
    comparisons:
      functional: 1
      product: 2
      agentic: 0
      engineering: 1
      reliability: 0
      security: 1
      innovation: 0
  b_first:
    presented_first: team-scribe
    comparisons: {}
combined_margin: null
order_disagreement: false
outcome: null
winner: null
adjudication_id: null
visibility: private
approval_state: approved
validation_state: valid
approved_by: event-director
approved_at: "2026-09-24T12:13:32Z"
approval_note: Approved by the event-director in session 2026-09-24 ('yes to all'); closes final audit FA7
---

# Matchup Pass Report

One pass of an order-balanced comparison, in one presentation order, written
without sight of the other pass. Fill the `comparisons` block that matches
`presentation_order` and leave the other one empty: the schema requires exactly
one populated block, because an entry in both would mean a single judge produced
both passes and order balancing bought nothing.

`combined_margin`, `winner` and `outcome` stay null here. They belong to
`atj matchup`, which reads both passes and resolves them. Nothing in this
artifact is an official result, and `atj validate publication` refuses it: a pass
report is panel-private and never a disclosure source.

## Eligibility and common evidence

Both teams are eligible, and both are pinned to immutable commits (`events/trial-2-2026/teams.md:11-12`). Both evidence packages are `approval_state: approved` and `validation_state: valid`, approved by the event-director at 2026-09-22T01:10:29Z (`evidence/team-demos/manifest.md:20-23`, `evidence/team-scribe/manifest.md:20-23`). Both packages are `execution_status: sandboxed-partial`. Both list `functional` and `agentic` as `evidence_limited_criteria`, for the same no-model-call cause, and the event treats that alike for both teams (`evidence/team-scribe/manifest.md:79-89`).

The common evidence base is:
- the two manifests;
- the eleven run records under `events/trial-2-2026/runs/`;
- the four judgments per team;
- the two consolidated summaries, used as an index only;
- `adj-trial-2-2026-team-demos-functional.md` and `adj-trial-2-2026-team-scribe-agentic.md`, each of which accepts an `NE` without a score;
- `audits/consolidation.md` and `audits/judgments.md`.

Where an audit corrected a summary claim, this pass follows the audit and the source. Consolidation F2 and N6 correct how often the v1.1 POST guard raises: three of five forms, with the schemeless form rejected by `urllib`. Judgments F1 and F19 withdraw the team-demos `.env.example` defect. Judgments F4 and F18 correct the team-scribe `install.py` attribution and add the placeholder filter.

No team total, provisional sum or partial total was compared or used.

## Order-balanced results

| Criterion | Weight | Value in this pass | Evidence |
|---|---:|---:|---|
| functional | 25 | 1 | **team-scribe:** its documented start command fails from its own declared install. `runs/team-scribe-app-start-01.json` records `exit_status: 1` and `No module named 'qdarkstyle'`. The cause is `src/gui/qt_app.py:11` against `requirements.txt:25` (`ev-scribe-02`, `ev-scribe-03`). The manifest states this cause lies inside the submission and is not an evidence limit (`evidence/team-scribe/manifest.md:168-171`). No advertised workflow is reachable (`judgments/team-scribe/judge-backend.md:75-77`). **team-demos:** every part that could execute behaved as documented. Both act-1 dry runs exited 0 (`runs/team-demos-01-dryrun-vulnerable-01.json`, `runs/team-demos-01-dryrun-hardened-01.json`). Both state tools behaved correctly (`runs/team-demos-10-list-verdicts-01.json`, `runs/team-demos-04-memory-diff-01.json`), and the structure claims were confirmed (`ev-demos-02`, `ev-demos-10`). **Why only +1:** the team-demos headline workflow (acts 2 and 3 under a model) was never observed. `adj:trial-2-2026:team-demos:01` accepted that `NE`, so the advantage rests on a confirmed failure on one side against a partial, unexercised success on the other. |
| product | 15 | 2 | **team-scribe:** the product cannot be used as delivered. Its only guaranteed user message misdiagnoses the fault and prescribes a remedy that cannot work: `main.py:50` against the PySide6 install confirmed in `runs/team-scribe-envcheck-01.json` (`ev-scribe-01`, `ev-scribe-02`). The judge calls usability of the delivered artifact zero (`judgments/team-scribe/judge-backend.md:89-91`). **team-demos:** the presenter kit was verified directly. There are ten presenter READMEs on one template (`ev-demos-02`; `judgments/team-demos/judge-backend.md:91-97`). The pin was verified clean by the demos' own tools (`ev-demos-11`). Reset paths are documented per demo (`judgments/team-demos/judge-security-ops.md:89-95`). Its surviving weaknesses are documentation-level: the offline-hostile `uv` invocation (PD1, `ev-demos-01`) and cross-path error strings (PD13). None of them blocks use. A product unusable from its own install against a verified usable kit is material and bears on the outcome. |
| agentic | 15 | 0 | Effectiveness is unobserved on both sides (`evidence/team-demos/manifest.md:130-135`, `evidence/team-scribe/manifest.md:160-164`). team-scribe `agentic` is an `NE` accepted by adjudication (`adj-trial-2-2026-team-scribe-agentic.md:26-36`). team-demos has more readable control design (`ev-demos-05`; `judgments/team-demos/judge-backend.md:105-111`). team-scribe has real controls of its own: a category whitelist at the persistence boundary and bounded retries (`judgments/team-scribe/judge-backend.md:99-101`). With half the criterion unobserved for both teams and one side adjudicated unscorable, the recorded evidence does not establish a meaningful difference. |
| engineering | 15 | 1 | **team-scribe:** several defects sit in state handling and dependency declaration. The undeclared import is `ev-scribe-03`. The conftest mock is inverted against a declared dependency (`ev-scribe-06`). `pytest.ini` is inert (`ev-scribe-09`). `retry_worker.py` raises `NameError` on every call and persisted pipeline state is wrong for every row (`judgments/team-scribe/judge-backend.md:113-119`). The audit verified these static reads against the pin, although they carry no evidence id (`audits/judgments.md` F12). **team-demos:** its defects are localized and not observed failing. They are the empty-host guard, the `_next_qid` file-count id, unguarded JSON reads (`judgments/team-demos/judge-backend.md:123-129`) and stated duplication. Its stdlib-only construction is confirmed by `ev-demos-02`. **Why only +1:** team-scribe is a larger and more ambitious system (`ev-scribe-13`), so the gap is meaningful but not decisive. |
| reliability | 10 | 0 | The two teams are strong in opposite places. **team-demos** has no automated tests of any kind (`ev-demos-10`), but its detection and recovery tooling was executed and worked (`runs/team-demos-10-list-verdicts-01.json`, `runs/team-demos-04-memory-diff-01.json`). **team-scribe** has 509 passing offline tests (`runs/team-scribe-pytest-01.json`, `ev-scribe-05`). Against that, 23 failures reproduce in its declared environment, the coverage gate is inert (`ev-scribe-09`), there is no CI, and its recovery feature is dead (`judgments/team-scribe/judge-security-ops.md:135-139`). Graceful logging degradation was observed in `runs/team-scribe-app-start-01.json`. One side has no prevention and the other has broken prevention. The evidence does not establish that either is meaningfully better. |
| security | 10 | 1 | **team-demos:** its containment controls were executed against hostile input and held. `runs/team-demos-egress-guards-01.json` shows every non-local form refused by `is_localhost`, and the v1.1 guard raising for three of five forms with the schemeless form rejected by `urllib` (`ev-demos-07`, as corrected by consolidation F2 and N6). The attacker endpoint is loopback-bound (`ev-demos-08`) and the data is clean under a whole-tree scan (`ev-demos-09`). **team-scribe:** its key storage is well built but was read only statically (`ev-scribe-14`). The only reachable key path at the pin feeds a plaintext `.env` (`judgments/team-scribe/judge-security-ops.md:153`, re-attributed by judgments F4 and qualified by F18). Three `SECURITY.md` claims are contradicted by the code (`judgments/team-scribe/judge-backend.md:141-145`). **Why only +1:** team-demos has its own gaps between stated and enforced controls. These are demo 06's model-supplied gate, the broad `Bash(rm:*)` grants (`judgments/team-demos/judge-security-ops.md:151-161`), and no isolation guidance for the hijack path (`judgments/team-demos/judge-backend.md:156`). |
| innovation | 10 | 0 | Each team's merit is of a different kind, and neither was observed working at runtime. **team-demos** offers pedagogical assembly and minimal-diff construction (`ev-demos-05`; `judgments/team-demos/judge-backend.md:168-174`), but no attack class or defence in it is new. **team-scribe** offers hand-built DSP depth in a mel-filterbank and ward-linkage diarizer, plus checkpointed recording (`judgments/team-scribe/judge-backend.md:155-161`). Its most ambitious piece, the retry half, does not execute, and its checkpoint flush is quadratic. The evidence does not establish a meaningful difference in originality or depth. |

## Margin and outcome

- Presentation order judged: a-first (team-demos presented first)
- Populated pass block: `passes.a_first`
- Margin: resolved by `atj matchup`, not stated here
- Close-call threshold: `close_call_band: 5`, from `framework/rubrics/head-to-head.md` front matter

## Decisive evidence

The only ±2 value is `product`. `runs/team-scribe-app-start-01.json` (`exit_status: 1`) and `ev-scribe-02` establish that a team-scribe user who follows the submission's own install and run instructions reaches no workflow. The same user sees an error that points to the wrong cause and repeats the failing remedy. The manifest assigns that cause to the submission rather than the event (`evidence/team-scribe/manifest.md:168-171`). The team-demos presenter surface was read and partly executed without a comparable blocker (`ev-demos-02`, `ev-demos-11`).

## Conflicting evidence

- **functional:** team-demos `functional` is an adjudicated `NE` (`adj:trial-2-2026:team-demos:01`), and its panel split 3/3/NE/NE. A reader could argue that an `NE` cannot be compared with an observed failure, which would give 0. This pass gives +1 because team-scribe's failure is confirmed and inside the submission, while team-demos' executable portion succeeded. The +1 is not +2 because the team-demos central workflow is unknown.
- **agentic:** team-demos was scored by all four of its judges, all of whom rejected `NE`. team-scribe was split 2/3/NE/NE and adjudicated `NE`. The difference in scorability reflects how much design is readable, not demonstrated effect, so it was not converted into an advantage.
- **security:** the team-demos security-ops judgment (`judgments/team-demos/judge-security-ops.md:147`) says `_post_to_localhost` raises for each non-local host. The run record and consolidation N6 show three of five. This pass relies on the corrected count, and the conclusion holds on it.
- **Double counting:** the team-scribe launch failure bears on `functional`, `product` and `engineering`. Each value above cites the part of the evidence specific to its criterion: workflow reachability, user-facing usability and dependency declaration respectively.

## Tie-break or adjudication

If a tie-break were needed, `framework/rubrics/head-to-head.md` `tie_break_order` would turn first on `functional`, where this pass records +1 for team-demos. The comparison there rests on a confirmed entry-point failure against an adjudicated `NE`. It would turn next on `reliability`, which is 0 in this pass. No tie-break is applied here. It is applied once, over both passes, by `atj matchup`.

## Audit

- [x] This pass was judged without sight of the other pass
- [x] Only the block matching `presentation_order` carries comparisons
- [x] Every nonzero comparison cites evidence
- [x] No prohibited team metadata influenced judgment
- [x] No official number was computed in this artifact
