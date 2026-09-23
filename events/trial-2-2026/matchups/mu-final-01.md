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
completed_at: "2026-09-23T17:26:17Z"
close_call_band: 5.0
presentation_order: both
passes:
  a_first:
    presented_first: team-demos
    comparisons: {agentic: 0, engineering: 1, functional: 1, innovation: 0, product: 2, reliability: 0, security: 1}
  b_first:
    presented_first: team-scribe
    comparisons: {agentic: -1, engineering: -1, functional: -2, innovation: 0, product: -2, reliability: 0, security: -1}
combined_margin: 50.0
order_disagreement: false
outcome: confirmed
winner: team-demos
adjudication_id: null
visibility: private
approval_state: draft
validation_state: unvalidated
---

# Matchup Report

Resolved by `atj matchup` from the two order-balanced passes. Every number here is
read from `matchups/mu-final-01.json`; none was computed by hand. The judges' own
reports are in `events/trial-2-2026/matchup-passes/`. Each was a fresh
`matchup-judge@1.1.0` context launched concurrently with the other, neither saw the
other's output, and neither computed a margin. `started_at` and `completed_at` are
the first and last entries of the two agents' own transcripts.
These facts, and the mechanical extraction of each pass from its transcript, rest
on the orchestrator's record. The transcripts are session files outside the
evidence package, so `audits/tournament.md` F14 could not verify them.

`model_used` is `claude-opus-5-5[1m]`, which is not the `claude-opus-5` that wrote
the eight panel judgments. The matchup judges compared on those judgments as
evidence; they did not re-score them.

## Eligibility and common evidence

Both teams are eligible and pinned (`teams.md:11-12`), and both packages are
`approved` and `valid`, `execution_status: sandboxed-partial`, with `functional` and
`agentic` listed as `evidence_limited_criteria` on both for the same event-imposed
cause: no model call was possible in this event. Neither team has an official
total. `adj:trial-2-2026:team-scribe:01` accepted `agentic` as `NE` and
`adj:trial-2-2026:team-demos:01` accepted `functional` as `NE`. Both passes recorded
that they did not use or compare any total. `head-to-head.md` says "Do not merely
select the team with the higher initial total", and neither pass consulted one.

The passes applied overlapping audit corrections to the panel summaries, each
citing its own set. Both use the three-of-five count for the v1.1 POST guard:
pass A cites consolidation F2 and N6, pass B cites F2. Pass B cites consolidation
F1 (the team-scribe `.env` contradiction is a single-judge finding) and pass A
does not. Both apply judgments F1 (the team-demos `.env.example` defect is
withdrawn) and judgments F4 (the team-scribe installer attribution). Pass A also
cites F18 and F19.

## Order-balanced results

| Criterion | Weight | A-first value | B-first normalized | Combined margin | Order |
|---|---:|---:|---:|---:|---|
| functional | 25 | +1 | +2 | +18.75 | consistent |
| product | 15 | +2 | +2 | +15.00 | consistent |
| agentic | 15 | +0 | +1 | +3.75 | consistent |
| engineering | 15 | +1 | +1 | +7.50 | consistent |
| reliability | 10 | +0 | +0 | +0.00 | consistent |
| security | 10 | +1 | +1 | +5.00 | consistent |
| innovation | 10 | +0 | +0 | +0.00 | consistent |

Positive favours **team-demos**. The B-first pass was negated by `atj matchup` from
its `presented_first` field (`atj/matchup.py:42-70`), not by either judge.

## Margin and outcome

- A-first pass margin: **+40.00**, picked **team-demos**
- B-first pass margin, normalized: **+60.00**, picked **team-demos**
- Combined margin: **+50.00** on a -100..+100 scale
- Close-call band: +/-5.0
- Order disagreement: false
- Outcome: **confirmed**, winner **team-demos**

`adjudication_reasons` is empty. The result confirms automatically.

## Decisive evidence

Both passes gave `product` a decisive +2 on the same record:
`runs/team-scribe-app-start-01.json` exits 1 on `No module named 'qdarkstyle'`
(`src/gui/qt_app.py:11` against `requirements.txt:25`), which the manifest assigns to
the submission rather than the event (`evidence/team-scribe/manifest.md:168-171`).
A user following team-scribe's own install and run instructions reaches no
workflow, against a team-demos presenter kit that was read and partly executed
without a comparable blocker.

The B-first pass also gave `functional` a decisive value on the same run record and
`submission-evaluation.md:106`. The A-first pass held it at +1 because the team-demos
headline workflow was never observed.

## Conflicting evidence

- **One run record drives three criteria.** The team-scribe start failure bears on
  `functional`, `product` and `engineering`. Pass A addressed this directly and cites
  a different part of the evidence for each: workflow reachability, the misleading
  user-facing message, and the undeclared dependency. Pass B does not discuss it.
  Both passes carry positive values on all three.
- **`functional` compares an observed failure with an accepted `NE`.** team-demos'
  functional evidence is act 1 of one demo, plus two state tools. Both passes named
  this and both said the advantage rests more on team-scribe's confirmed failure than
  on team-demos' demonstrated success. Pass B said a reading that weighted the
  unobserved acts more heavily "could reasonably land at -1", which is the A-first
  value in its orientation.
- **`agentic`** split 0 against +1 in magnitude, not direction. Pass B credited the
  executed data/instruction boundary in the two dry-run captures. Pass A judged that
  unobserved effectiveness on both sides left no meaningful difference.
- **`reliability`** is 0 in both passes for the same stated reason: team-scribe has 509
  passing tests but a red suite, an inert coverage gate and no CI, and team-demos has
  no tests but working detection and recovery tools.

## Tie-break or adjudication

Not reached. `tie_break_order` is `[functional, reliability, product]`, and the combined
margin is far outside the close-call band.

## Errata

Found by `audits/tournament.md` and checked against the sources. The pass reports
are left as their judges returned them. No comparison value rests on any of these.

- **F5, pass A.** `ev-demos-02` establishes ten demo READMEs, not that they share
  one template. The `Bash(rm:*)` grants are at `judgments/team-demos/judge-security-ops.md:49,165,185,194`,
  not `:151-161`. `judgments/team-scribe/judge-security-ops.md:135-139` calls the
  recovery path unobserved, not dead. The `NameError` is in the retry worker
  (`judgments/team-scribe/judge-backend.md:113-119`).
- **F6, pass B.** `list_verdicts.py`'s exit 1 is behaviour in the code
  (`10-show-your-work/demo/scripts/list_verdicts.py:20-21` at the pin), not
  documented behaviour: the demo README (`10-show-your-work/demo/README.md:93`)
  describes only what the script prints on success. The two dry runs used
  `python3 <script> --dry-run`, which the submission does not document
  (`evidence/team-demos/manifest.md:53-55`). "Exited as documented" therefore holds
  for neither the invocation nor the `list_verdicts.py` exit, and not for
  `memory_diff.py`, whose "No change" text is in the script only (`memory_diff.py:45`).
  It holds for the dry-run output, which the root README documents as printing the
  exact prompt. The egress guard probe was the event's own script, not a documented
  command (`evidence/team-demos/manifest.md:113`).
- **F13, pass A.** Pass A's description of what judgments F18 and F19 did does not
  match `audits/judgments.md`. Read that audit, not the pass, for their effect.

## Audit

- [x] Both passes independent. They were separate contexts launched together, and
  neither was given the other's output or anything under `matchups/`
- [x] Presentation order reversed. `a-first` presented team-demos first, `b-first`
  presented team-scribe first
- [x] Normalization performed by the tool, not by a judge
- [x] Every nonzero comparison cites evidence. See the pass reports
- [x] No arithmetic performed by hand. Every figure is read from `mu-final-01.json`
- [x] Comparison values verified against each judge's own output before resolution.
  Both were extracted mechanically from the agent transcripts and both matched exactly
- [x] No total, provisional or official, used or stated
