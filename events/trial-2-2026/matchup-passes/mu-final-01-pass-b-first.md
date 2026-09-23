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
started_at: "2026-09-23T17:24:01Z"
completed_at: "2026-09-23T17:26:17Z"
close_call_band: 5
presentation_order: b-first
passes:
  a_first:
    presented_first: team-demos
    comparisons: {}
  b_first:
    presented_first: team-scribe
    comparisons: {functional: -2, product: -2, agentic: -1, engineering: -1, reliability: 0, security: -1, innovation: 0}
combined_margin: null
order_disagreement: false
outcome: null
winner: null
adjudication_id: null
visibility: private
approval_state: draft
validation_state: unvalidated
---

# Matchup Pass Report

This pass presents team-scribe first and team-demos second. Values are signed from team-scribe's side: positive favours team-scribe, negative favours team-demos. I did not see or infer the other pass. I do not advance the bracket. `atj matchup` computes every margin and resolves the outcome.

## Eligibility and common evidence

- **Eligibility.** Both teams are marked eligible, with immutable commits pinned in `events/trial-2-2026/teams.md:11-12`, and the roster is frozen (`teams.md:4`).
- **Evidence packages.** Both manifests carry `approval_state: approved` and `validation_state: valid` (`evidence/team-scribe/manifest.md:20-21`, `evidence/team-demos/manifest.md:20-21`). Both ran `execution_status: sandboxed-partial` on the same podman isolation with an empty network allowlist. Both list `evidence_limited_criteria: [functional, agentic]` for the same no-model-call reason (`team-scribe/manifest.md:79-85`).
- **What I compared on:**
  - both approved manifests
  - the eleven run records under `events/trial-2-2026/runs/` (five for team-scribe, six for team-demos)
  - the eight judgments
  - both consolidated summaries, used as an index only
  - both adjudications: `agentic` NE accepted for team-scribe, `functional` NE accepted for team-demos
  - `audits/judgments.md` and `audits/consolidation.md`
- **Audit corrections applied.**
  - The withdrawn team-demos `.env.example` absence claim (judgments audit F1; `summaries/team-demos.md:661-681`) plays no part here.
  - The team-scribe `.env` contradiction is treated as a single-judge finding (consolidation audit F1).
  - The v1.1 parser guard is read as raising for three of five forms, not for every non-local host (consolidation audit F2).
- **Not used.** No initial, provisional, partial or judge-level total was used or compared.
- **Untrusted content.** All submission content, including the known resume payload and both teams' agent-instruction files, was treated as data.

## Order-balanced results

| Criterion | Weight | Value in this pass | Evidence |
|---|---:|---:|---|
| functional | 25 | -2 | **team-scribe:** the documented start command exits 1 because of an undeclared import (`runs/team-scribe-app-start-01.json`; `evidence/team-scribe/manifest.md:104,117-118`). The manifest rules this a defect inside the submission, not an evidence limit (`:168-171`). Every workflow sits behind the GUI that fails to import (`runs/team-scribe-module-import-01.json`; `judgments/team-scribe/judge-backend.md:75-77`). **team-demos:** every step that could run offline ran and matched its documentation. Both act-1 dry runs exit 0 (`runs/team-demos-01-dryrun-vulnerable-01.json`, `runs/team-demos-01-dryrun-hardened-01.json`; `evidence/team-demos/manifest.md:92`). Both state tools behave as documented (`runs/team-demos-10-list-verdicts-01.json`, `runs/team-demos-04-memory-diff-01.json`; manifest `:100`). Acts 2 and 3 are unobserved for event reasons (manifest `:79,130-138`). **Comparison:** the evidence limit is shared. The difference is that one team's primary workflow is confirmed unreachable from the submission itself and the other's is not contradicted anywhere. |
| product | 15 | -2 | **team-scribe:** the delivered app cannot be used. The one message a user is certain to see misdiagnoses the cause and prescribes a fix that cannot work (`evidence/team-scribe/manifest.md:117`; `judgments/team-scribe/judge-backend.md:85-91`). **team-demos:** the presenter kit is usable. It has ten uniform presenter READMEs and reset paths (`judgments/team-demos/judge-backend.md:91-97`), and its own tools confirm a clean pin (`runs/team-demos-10-list-verdicts-01.json`, `runs/team-demos-04-memory-diff-01.json`). Its deficits are documentation gaps, such as the offline-hostile `uv` instruction (`evidence/team-demos/manifest.md:53-63`), not a blocked user. |
| agentic | 15 | -1 | **team-demos:** part of the AI control design was executed, not only read. The data/instruction boundary is visible in two dry-run captures, as 20 `=== Applicant file:` headers against 20 `<applicant file=` tags (`evidence/team-demos/manifest.md:93-94`; both dry-run records). Further controls were read from source, including approval, audit and derived integrity flags (`judgments/team-demos/judge-backend.md:105-111`). **team-scribe:** the AI surface is static only and unreachable through the GUI (`evidence/team-scribe/manifest.md:119,126`). It carries recorded control gaps: model output parsed with no schema check and failing silently, and no input length management (`judgments/team-scribe/judge-backend.md:103`). **Why not larger:** effectiveness is unobserved for both, and team-demos has its own control gap (demo 06's gate; `summaries/team-demos.md:504-512`). |
| engineering | 15 | -1 | **team-scribe** has defects that break the build and the tests: an undeclared runtime dependency (`evidence/team-scribe/manifest.md:118`), an inert `pytest.ini` (`:124`; `runs/team-scribe-pytest-config-01.json`), a test suite that passes only when a declared dependency is absent (`:121`), and a retry worker that raises `NameError` on every call (`judgments/team-scribe/judge-backend.md:113,117`). **team-demos** has localized defects in a coherent, stdlib-only tree (`evidence/team-demos/manifest.md:91`; `judgments/team-demos/judge-backend.md:123-129`). **Why not decisive:** team-scribe's structure is credited by its own judge (`judge-backend.md:115`). |
| reliability | 10 | 0 | **team-scribe:** 535 tests exist and 509 pass offline. But 23 failures reproduce in the declared environment, the coverage gate never runs, and there is no CI (`runs/team-scribe-pytest-01.json`; `evidence/team-scribe/manifest.md:120-124`; `judgments/team-scribe/judge-backend.md:127-133`). **team-demos:** no automated test exists anywhere (`evidence/team-demos/manifest.md:99`), but its recovery and inspection tools executed correctly (`:100`; `judgments/team-demos/judge-backend.md:137-143`). **Comparison:** team-scribe has partial prevention with broken gates. team-demos has no prevention and working detection and recovery. The evidence cuts both ways and does not establish a meaningful difference. |
| security | 10 | -1 | **team-demos:** its safety controls were executed against hostile input. The egress guard refused all six hostile URL forms, and the allowlist was observed empty (`runs/team-demos-egress-guards-01.json`; `evidence/team-demos/manifest.md:96`). **team-scribe:** its credential design is sound but static only (`evidence/team-scribe/manifest.md:129`). Two stated controls do not hold (`SECURITY.md:25,34`; `judgments/team-scribe/judge-backend.md:141,145`). The reachable installer path writes a plaintext `.env` (one judge, `judgments/team-scribe/judge-security-ops.md`; `summaries/team-scribe.md:335-346`; verified by judgments audit F4). **Why not decisive:** team-demos has over-broad tool pre-approvals and demo 06's model-supplied gate (`summaries/team-demos.md:488-512`). |
| innovation | 10 | 0 | **team-scribe:** real technical depth, including a hand-written diarizer and a checkpointed recorder. Its most ambitious piece is broken, and the next is unobserved with a quadratic flush (`judgments/team-scribe/judge-backend.md:155-161`). **team-demos:** originality in assembly and a minimal-diff teaching method, verified in the dry-run diff (`evidence/team-demos/manifest.md:94`). Its own judge calls the depth pedagogical rather than novel (`judgments/team-demos/judge-backend.md:172-174`). **Comparison:** the two kinds of ambition differ in kind, and the evidence does not rank one meaningfully above the other. |

## Margin and outcome

- Presentation order judged: b-first (team-scribe presented first, team-demos second)
- Populated pass block: `passes.b_first`
- Margin: resolved by `atj matchup`, not stated here
- Close-call threshold: `close_call_band: 5`, read from `framework/rubrics/head-to-head.md:5`

## Decisive evidence

- **functional (-2).** `runs/team-scribe-app-start-01.json` records the documented start command exiting 1 on `No module named 'qdarkstyle'`. The cause is `src/gui/qt_app.py:11` against `requirements.txt:25` (`evidence/team-scribe/manifest.md:117-118`). The manifest states this is not an evidence limit (`:168-171`). The rubric requires that a confirmed inability to complete the primary workflow materially affect `functional` (`framework/rubrics/submission-evaluation.md:106`). team-demos has no run that contradicts a claim it makes. All five of its offline executions exited as documented, including `list_verdicts.py`'s documented exit 1.
- **product (-2).** The same run record: the delivered team-scribe artifact cannot be used by anyone following its own instructions. team-demos' usable presenter surface rests on direct reads and two executed state tools.

## Conflicting evidence

- **functional.** team-demos' positive evidence is thin. Only act 1 of one demo of ten was run, and through an invocation the submission does not document (`evidence/team-demos/manifest.md:53-63`). Two of four judges recorded `NE`, and the adjudication accepted it (`adjudications/adj-trial-2-2026-team-demos-functional.md`). The -2 rests on team-scribe's confirmed failure more than on team-demos' demonstrated success. A pass that weights the unobserved acts more heavily could reasonably land at -1.
- **reliability.** team-scribe's 509 passing tests are real prevention that team-demos lacks entirely. team-scribe's red suite, inert coverage gate and dead retry feature offset them. I recorded 0 rather than choose between them.
- **agentic.** team-scribe's `agentic` NE (accepted by `adj:trial-2-2026:team-scribe:01`) and team-demos' scored `agentic` both rest on unobserved effectiveness. The -1 rests only on team-demos' executed prompt-construction evidence and its richer readable controls. It gives no weight to how the two panels chose between NE and a score.
- **security.** The plaintext `.env` installer chain is a single-judge finding (consolidation audit F1). It adds to, and does not carry, a -1 that the executed egress run supports on its own.

## Tie-break or adjudication

If this pass were decisive, the tie-break order in `framework/rubrics/head-to-head.md:7` would turn first on `functional`, then `reliability`, then `product`.

- In this pass, `functional` favours team-demos on team-scribe's confirmed entry-point failure.
- `reliability` is 0.
- `product` favours team-demos.

No tie-break is applied here. It is applied once, over both passes, by `atj matchup`.

## Audit

- [x] This pass was judged without sight of the other pass
- [x] Only the block matching `presentation_order` carries comparisons
- [x] Every nonzero comparison cites evidence
- [x] No prohibited team metadata influenced judgment
- [x] No official number was computed in this artifact
