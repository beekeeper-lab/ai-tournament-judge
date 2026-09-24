---
event_id: trial-2-2026
team_id: team-demos
commit: dc35f6962130af5e5be3fe16672e3d4964850eb9
evidence_package_id: ev:trial-2-2026:team-demos:dc35f6962130:cb3847cb
rubric: submission-evaluation@1.1.0
consolidation_policy: panel-consolidation@1.1.0
persona: panel-consolidator@1.1.0
framework_commit: af9f6fba9e0d6f54a69156193fc57be16d7a4357
judge_run_ids:
- jr:trial-2-2026:team-demos:judge-backend:cb3847cb:01
- jr:trial-2-2026:team-demos:judge-frontend-ux:cb3847cb:01
- jr:trial-2-2026:team-demos:judge-product-agentic:cb3847cb:01
- jr:trial-2-2026:team-demos:judge-security-ops:cb3847cb:01
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-22T18:10:00Z"
completed_at: "2026-09-22T18:52:00Z"
total: null
display_total: null
finalized: false
blocked_reasons:
- 'functional: NE accepted by adjudication adj:trial-2-2026:team-demos:01 (event-director); the rubric permits no official total while a criterion is NE'
adjudication_ids:
- adj:trial-2-2026:team-demos:01
visibility: private
approval_state: approved
validation_state: valid
approved_by: event-director
approved_at: "2026-09-24T12:13:32Z"
approval_note: Approved by the event-director in session 2026-09-24 ('yes to all'); closes final audit FA7
---

# Consolidated Team Report — team-demos (AI Security Demos)

## Executive summary

Four independent judges evaluated the same submission at commit `dc35f696` against
the same evidence package (`ev:trial-2-2026:team-demos:dc35f6962130:cb3847cb`)
under `submission-evaluation@1.1.0`. All four reports validate, carry the same
team, commit, evidence package and rubric version, and each declares that no other
judgment was inspected.

**This panel is not finalized, and that is a decision rather than an omission.**
`judge-frontend-ux` and `judge-security-ops` each recorded `functional` as `NE`
with high confidence; `judge-backend` and `judge-product-agentic` each scored it 3.
Adjudication `adj:trial-2-2026:team-demos:01`, decided by the event director on
2026-09-22 under `decision_authority: human-official`, reviewed the criterion,
accepted the `NE`, and supplied no score, on the stated ground that a supplied
number would stand in for an observation the event could not make. The rubric
permits no official total while a criterion is `NE`. `summaries/team-demos.json`
records `total: null`, `display_total: null`, `finalized: false`, and a
`provisional_total` of 52.50 for the scored criteria. That provisional sum is not
an official total, must not be published as one, and must not be used for bye
seeding.

The evidence ceiling is the event's, not the team's. The manifest states it
directly: `network_allowlist` is empty, no model call was made anywhere, acts 2
and 3 of every demo stage a payload by writing into a read-only pin, and the
Claude Code run path cannot be exercised at all. All four judges held that line.
Nothing in this report describes agent behaviour under attack, because none was
observed.

What the panel does agree on is unusually well evidenced for a submission judged
offline. The safety controls were executed against hostile input and held; the
sample data is clean under a whole-tree scan; the corpus is stdlib-only with no
dependency manifest, which is why any of it was judgeable at all in a sandbox with
no network; and the presenter documentation is uniform across all ten demos. All
four judges scored `product` and `innovation` at 4 and `engineering` at 3, and the
three remaining scored criteria each split by one point.

Two judgments were amended during a three-round stage audit, and one finding was
withdrawn outright. `judge-frontend-ux` and `judge-security-ops` had each recorded,
as a confirmed and personally verified defect, that `.env.example` exists nowhere
in the pinned tree, and each had used it to hold `product` below the top anchor.
Ten `.env.example` files are tracked at the pin, one per demo folder. Both judges
withdrew the claim in place, both explained the tooling blind spot that produced
it, and neither moved its score (`audits/judgments.md`, F1, F19). **That claim is
not carried anywhere in this report as a finding.** The surviving reasons each
judge gave for `product` are recorded under the per-criterion analysis below.

The consolidator is a neutral packager, not a fifth judge. No individual score was
altered, no finding below originates with the consolidator, and every number in
this report is quoted from `summaries/team-demos.json` or from a judgment's own
front matter.

## Consolidated score

Generate this block with `atj render consolidated <this file>`. It consolidates
the team's individual judgments through the canonical rubric and writes the table
below, together with `total`, `display_total`, `finalized` and `blocked_reasons`
in the front matter. Everything between the markers is the tool's output: do not
edit it, and do not transcribe it from `atj score`.

If you find yourself copying numbers into the table by hand, stop and say so in
`## Material disagreements`. A hand-built score block is not a generated one, and
a report that claims otherwise is making a false statement about its own
provenance.

No cell below was typed. The consolidator left the marker region and the four
front-matter fields the renderer owns at their template values, and
`atj render consolidated` was then run against this file and wrote every
official number below. The prose in this document quotes
`summaries/team-demos.json`, which `atj score` produced; the consolidator
performed no arithmetic. Re-running `atj render consolidated` against this file
during the consolidation audit reported `unchanged`, so the block matches what
the renderer produces; that the consolidator did not type it is the
consolidator's own declaration, recorded in the calculation audit below.

<!-- atj:consolidated:begin -->
| Criterion | Judge scores | Mean | Weight | Points | Agreement |
|---|---|---:|---:|---:|---|
| functional | judge-backend=3.0, judge-frontend-ux=NE, judge-product-agentic=3.0, judge-security-ops=NE | 3.00 | 25 | 15.00 | aligned |
| product | judge-backend=4.0, judge-frontend-ux=4.0, judge-product-agentic=4.0, judge-security-ops=4.0 | 4.00 | 15 | 12.00 | aligned |
| agentic | judge-backend=4.0, judge-frontend-ux=3.0, judge-product-agentic=4.0, judge-security-ops=3.0 | 3.50 | 15 | 10.50 | aligned |
| engineering | judge-backend=3.0, judge-frontend-ux=3.0, judge-product-agentic=3.0, judge-security-ops=3.0 | 3.00 | 15 | 9.00 | aligned |
| reliability | judge-backend=3.0, judge-frontend-ux=3.0, judge-product-agentic=2.0, judge-security-ops=3.0 | 2.75 | 10 | 5.50 | aligned |
| security | judge-backend=4.0, judge-frontend-ux=4.0, judge-product-agentic=4.0, judge-security-ops=3.0 | 3.75 | 10 | 7.50 | aligned |
| innovation | judge-backend=4.0, judge-frontend-ux=4.0, judge-product-agentic=4.0, judge-security-ops=4.0 | 4.00 | 10 | 8.00 | aligned |
| **Overall** |  |  | **100** | **not finalized** |  |

**Finalization blocked:**
- functional: NE accepted by adjudication adj:trial-2-2026:team-demos:01 (event-director); the rubric permits no official total while a criterion is NE

Provisional sum of scored criteria: 52.50 / 100. This is not an official total and must not be published or used for bye seeding.
<!-- atj:consolidated:end -->

**Overall:** not finalized, by decision. `summaries/team-demos.json` records
`total: null`, `display_total: null`, `finalized: false`, and one blocked reason:
`functional` is `NE`, accepted by adjudication `adj:trial-2-2026:team-demos:01`
(event-director), and the rubric permits no official total while a criterion is
`NE`. The same file records `provisional_total: 52.5` over the scored criteria;
the generated block above prints it with the warning it carries, and it is not an
official total. Individual judge results as the script computed them:
`judge-backend` total 70.0, `judge-product-agentic` total 68.0,
`judge-frontend-ux` no total with `partial_total` 52.0 and `unresolved_ne:
[functional]`, `judge-security-ops` no total with `partial_total` 50.0 and
`unresolved_ne: [functional]`. A partial total is not a score and is not
comparable with a total.

**Overall confidence:** no judge recorded `low` confidence on any criterion. The
recorded distribution is medium and high. Both `NE`s on `functional` are `high`,
which is what the rubric asks of a criterion the evidence package itself records
in `evidence_limited_criteria`: the inability to observe is established fact, not
a judge's failure to find something. Confidence does not track score direction —
on `reliability` the judge scoring lowest (`judge-product-agentic`, 2) recorded
high confidence, while all four recorded medium on `product`, `agentic` and
`innovation`, the three criteria whose ceiling every judge located in the
unobserved live behaviour. `security` is high from all four despite a one-point
spread, so it distinguishes nothing either way.

## Per-criterion agreement analysis

Scores, means, ranges and agreement labels are quoted from
`summaries/team-demos.json`. `atj score` reports `integrity_problems: []`,
`possible_outliers: []` on every criterion, and `adjudication_required: []` after
the accepted `NE`.

### functional — two scores of 3, two `NE`; labelled `aligned`, and the label is misleading

`source_scores`: `judge-backend` 3.0, `judge-frontend-ux` `NE`,
`judge-product-agentic` 3.0, `judge-security-ops` `NE`. Confidence: medium, high,
medium, high.

The `aligned` label is computed from the range over numeric scores only, so a
panel split down the middle about whether the criterion can be scored at all
prints as agreement. The judging audit raised this as F7 and it is carried as
framework defect W10; the rubric could not be changed mid-event. Read the split,
not the label.

There is no factual disagreement. All four judges hold the same facts: no model
call was made anywhere (`ev-demos-01`, `runs/team-demos-envcheck-01.json` — TCP to
`1.1.1.1:443` fails `Errno 101`, DNS fails `gaierror`, and `anthropic`,
`requests`, `httpx` and `uv` are all absent); acts 2 and 3 require a write into a
read-only pin (`ev-demos-06`); and act 1 of demo 01 ran offline in both variants,
exit 0, printing the full prompt and ending `[dry-run] 20 resumes,
model=claude-sonnet-5, no API call made.` (`runs/team-demos-01-dryrun-vulnerable-01.json`,
`runs/team-demos-01-dryrun-hardened-01.json`). All four also accept the manifest's
instruction that a dry run is prompt construction and not agent behaviour.

The split is over what that leaves. `judge-backend` scored 3 because the two
dry-run captures are a complete, correct execution of act 1 as its README
describes it, and because the corpus-level completeness claims are independently
confirmed (`ev-demos-02`, `ev-demos-10`); he states in his own report that a
reasonable judge could land one anchor lower or record `NE`.
`judge-product-agentic` scored 3 on the same captures plus the structural
confirmations, and stated the counterfactual himself: had acts 2 and 3 been staged
and failed, the score would be materially lower, and nothing in the package tells
him either way. `judge-frontend-ux` recorded `NE` because the promised primary
workflow is the three acts, none of which was observed in any of the ten demos,
and declined to convert an unobservable workflow into a low number.
`judge-security-ops` recorded `NE` on the reasoning that the rubric's boundary
requires a *confirmed inability* to complete the advertised workflow, and what
exists here is an unexercised workflow: a low score would blame the submission for
the event's empty allowlist, and a solid score would rest on one act of one demo
of ten.

Both `NE`s are argued from the manifest sentence that declares the criterion
evidence-limited, which is what `submission-evaluation@1.1.0` requires of a
high-confidence `NE`. Resolution: `adj:trial-2-2026:team-demos:01` accepted the
`NE`; no source score was modified, and `judge-backend`'s and
`judge-product-agentic`'s 3s stand unchanged in the record.

### product — unanimous 4.0, range 0.0, `aligned`

Confidence: medium from all four.

Shared basis, verified by more than one judge independently: ten demo READMEs on
one template, each with a three-act table covering both run paths, a "why the fix
works" section, a files table and presenter notes (`ev-demos-02` records the
README count; the section structure comes from `judge-frontend-ux`'s grep, which
verified the three-act section present in all ten, and from the judges' own
reads);
stage, unstage and reset rows in every demo so the prop survives being run twice;
a checkout verifiably clean of leftover presentation state, confirmed by the
demos' own tools (`ev-demos-11`); and synthetic data at scale with no address at a
resolvable domain anywhere in 201 resume files (`ev-demos-09`).

The four judges reached 4 by different routes and each named a different reason it
is not 5. `judge-backend`: two usability and disclosure gaps, the offline-hostile
run instructions and the unverifiable "de-identified from real resumes" claim.
`judge-product-agentic`: the product's most fragile moment, the live attack, has
no offline fallback outside demo 10 and no way to check it in advance.
`judge-frontend-ux`, after withdrawing the `.env.example` finding, rests on three
surviving reasons — error and empty-state strings that name only Claude Code
commands to users on the Python path (`render_ranking.py:240`,
`render_assessment.py:169-170`, `list_verdicts.py:20,40`); a top-level README with
no troubleshooting, no stated minimum Python version and no degraded-mode
guidance, with the only keyless rehearsal path buried in one demo's README; and
above all that the product's real delivery surface is a live room, on which
effectiveness has no evidence either way. He also records that the rendered HTML
was assessed from its generator only, since `reports/` is gitignored and the tree
is clean, so he neither credited nor penalized rendered visual quality.
`judge-security-ops`, after the same withdrawal, rests on one surviving reason and
says so: he read five of the ten presenter scripts end to end (01, 05, 06, 07, 09)
and knows the other five only through `ev-demos-02`'s structural count, and the
top anchor asks for quality evident across the artifact. He names that as a limit
on his evidence rather than a fault found in the submission, and as the reason his
confidence stays medium.

The judging audit verified both rewritten rationales (F19) and confirmed neither
judge raised its score after losing a stated reason.

### agentic — range 1.0, two at 4.0 and two at 3.0, `aligned`

`judge-backend` 4.0, `judge-frontend-ux` 3.0, `judge-product-agentic` 4.0,
`judge-security-ops` 3.0. Confidence: medium from all four. The manifest records
this criterion in `evidence_limited_criteria` alongside `functional`.

All four agree on the facts and all four explicitly considered and rejected `NE`,
each giving a reason: three of the criterion's four sub-questions — whether using
a model is the correct decision, whether its use is controlled, and whether it is
observable — are answerable from artifacts in the pinned tree, and the fourth,
effectiveness, is unobserved. Every judge states that it credited no
effectiveness whatsoever. `judge-frontend-ux` names openly that a reasonable judge
holding the same facts could mark the criterion `NE`.

The split is over whether design, control and observability without any
demonstrated effect can exceed expectations. The two at 4 weight what is
structurally enforced: the data/instruction boundary implemented as two mutually
dependent changes (`ev-demos-05`), the gated action surface with human-attributed
approval and an audit line per consequential action, and `effective_flags`
recomputing integrity flags from each source's trust tier rather than trusting
what the model wrote (`10-show-your-work/demo/scripts/explain.py:85-110`), which
`judge-product-agentic` calls a verification loop that does not depend on the
component being verified. The two at 3 weight a specific gap in the same
architecture: on the run path demo 06 itself calls the hero path, the ceiling is
`--mode gate` typed by the agent into its own shell command, against a CLI that
accepts `--mode fire` from any caller. `judge-security-ops` states it as the
corpus's own standard applied to itself — the talk teaches that a control stated
in a prompt is not a control. `judge-product-agentic` found the same thing and
still scored 4, recording it as the reason the criterion does not reach the top
anchor rather than as a reason to drop an anchor. That is a weighting difference
on an agreed fact, not a factual dispute.

### engineering — unanimous 3.0, range 0.0, `aligned`

Confidence: medium, medium, high, high.

Unanimous reasoning: coherent, proportionate to a set of stage props, readable,
with self-containment bought deliberately through duplication and stated as a
choice rather than drifted into. Unanimous ceiling: duplication across ten demos
with nothing automated to catch drift. Each judge named a different instance —
`render_ranking.py` copied across demos, the 20-resume corpus duplicated to 201
files, demo 06's harness a stated copy of demo 05's — and `judge-backend`
additionally named three localized correctness gaps in the code that carries the
lessons: two localhost guards of different strength for the same concern, an
approval-queue id derived from a file count, and a JSON read guarded in one
function of a file and unguarded in another. `judge-frontend-ux` located a
different ceiling item, the unversioned regex contract between the agent's
markdown output and the renderer. `judge-security-ops` and
`judge-product-agentic` each named a dead or unused symbol. None contradicts
another; they read different subsets, and three of the four say so.

### reliability — range 1.0, `judge-product-agentic` at 2.0 against three at 3.0, `aligned`

Confidence: high, high, high, medium. `possible_outliers: []` — the low score is
not far enough from the median for the policy's outlier test to fire.

All four established the same verified absence: no `test_*.py`, no `*_test.py`, no
`tests/`, no `conftest.py`, `pytest.ini` or `tox.ini` anywhere in the tree
(`ev-demos-10`). All four treated it as evidence and scored it rather than
recording `NE`, which is the rubric's rule for a verified absence. All four credit
the same working recovery and detection surface, executed:
`runs/team-demos-10-list-verdicts-01.json` (exit 1, "Nothing screened yet…") and
`runs/team-demos-04-memory-diff-01.json` (exit 0, "No change. Working memory
matches the clean seed.").

The split is over whether recovery and detection without any prevention still meet
primary expectations. Three judges say yes and name prevention as the reason the
score goes no higher. `judge-product-agentic` says no, on a product-specific
ground: the failure that matters most to a live-demo product is a model that no
longer takes the bait, there is no pre-flight check of any kind, and the
documented remedy is hand-editing the payload text before a talk. He states
explicitly that he is not penalizing a prototype for missing production
infrastructure but scoring the absence of the checks this submission's own claims
call for. This is an interpretation split on an agreed fact and is recorded, not
averaged away.

### security — range 1.0, `judge-security-ops` at 3.0 against three at 4.0, `aligned`

Confidence: high from all four. The judge scoring lowest is the security persona.

All four confirmed the same executed result and none disputes it
(`ev-demos-07`, `runs/team-demos-egress-guards-01.json`): `is_localhost` admits
`127.0.0.1`, `localhost` and `[::1]` and refuses `evil.example`,
`localhost@evil.example`, `127.0.0.1.evil.example`, `0.0.0.0`, `2130706433` and
`file:///etc/passwd`, with `ALLOWLIST = set()` observed empty in the same run, and
the v1.1 parser's `_post_to_localhost` exercised separately against five forms
and raising `RuntimeError` for three of them — `http://evil.example/collect`,
the userinfo form, and the protocol-relative `//evil.example/collect`. The bare
`evil.example/collect` never reaches the guard and is rejected by `urllib` with
a `ValueError`, which is PD3 below; the localhost form passes the guard and
fails on connection refused.
All four confirmed `ev-demos-08` and `ev-demos-09`.

The three at 4 score the controls that exist: exercised against adversarial input,
deny-by-default, with the one exfiltration tool's default mode the safe one, and —
`judge-frontend-ux` alone — HTML escaped before markdown transformation at the one
point where model-authored text becomes markup in a file a presenter opens.
`judge-security-ops` reached 3 by a different question: not "is it contained" but
"does the control the audience is told to take away match the control the artifact
enforces". He enumerates four sites where it does not (his F1 to F4, D3 to D5
below), and holds that in a corpus whose thesis is that a stated control is not a
control, that gap is the submission's own standard applied to itself. He also
records that nothing here endangers an operator's data, credentials or network and
that the score is nowhere near the failure anchors.

Two of his four sites were also found by `judge-product-agentic`, who scored 4.
The disagreement is over severity and criterion placement, not over the code.

### innovation — unanimous 4.0, range 0.0, `aligned`

Confidence: medium from all four.

Unanimous: the originality is in the assembly and the pedagogy, and it is real —
ten attack classes on one cast and one thesis, each demo isolating one new
mechanism and refusing to re-teach the previous one; the minimal-diff discipline,
verified in detail for demo 01 by `ev-demos-05`; demo 06 holding the prompt
byte-identical so only identity and mode vary, which two judges call a controlled
experiment rather than a demonstration; and integrity flags derived from source
trust rather than from the record's own stamps. Unanimous ceiling: no attack class
or defense is new to the field, and none of the mechanisms was observed doing what
it claims.

## Confirmed strengths

Each item was reached independently by the judges named. Repeated wording across
reports is not treated as additional confirmation. Where a strength rests on one
judge's observation, that is stated, and where it rests on the evidence
package's own scan rather than on separate reads, that is stated too.

- **The egress guards are controls, not comments, and they hold against the
  confusion forms that defeat naive host checks.** Executed, nine URL forms, six
  hostile, every non-local form refused, allowlist observed empty in the same run.
  `ev-demos-07`, `runs/team-demos-egress-guards-01.json`. All four judges, each
  reading the run record directly. Three of the four name userinfo confusion,
  suffix confusion and the decimal-IP form specifically as the cases a hand-rolled
  check usually lets through.
- **Every network call site in the tree was read and none is a surprise.** The
  attacker listener is hard-bound to `127.0.0.1:8099` with no flag to move it; the
  malicious parser's POST mode is off by default and writes a local file instead;
  no other module opens a socket. The tree-wide read is the evidence package's
  static scan, `ev-demos-08`, not four separate reads; all four judges cite it and
  none contradicts it.
- **The sample data is clean under a whole-tree scan.** 201 resume files; a scan
  of every text file for addresses outside the reserved example domains returns
  four, all themselves `.example` names. The scan is the evidence package's,
  `ev-demos-09`; all four judges cite it.
- **Self-containment is observable, not asserted.** No dependency manifest of any
  kind anywhere; an AST scan of all 53 Python files finds every module-scope
  import resolving to the standard library or a sibling in the checkout; the one
  third-party import sits below the dry-run early return in all 19 files that
  carry it. The AST scan is the evidence package's, `ev-demos-02`; all four judges
  cite it and two say so explicitly — `judge-backend` records that "the structural
  and dependency claims come from the package's AST scan over all of them" and
  `judge-frontend-ux` that they lean on `ev-demos-02` for the tree-wide
  conclusions. `judge-product-agentic` adds the consequence
  the panel felt directly: the decision to keep reconstruction, diffing, rendering
  and the action harness model-free was made for stage determinism and is why a
  meaningful part of this submission was judgeable at all in an offline sandbox.
- **The taught fix is a data/instruction boundary, implemented as two mutually
  dependent changes.** The hardened system prompt declares `<applicant>…</applicant>`
  content untrusted and `build_user_content` is what emits those tags, so neither
  half works alone; visible mechanically in the two captures as 20 `=== Applicant
  file:` headers against 20 `<applicant file=` tags. `ev-demos-05`, both dry-run
  records. All four.
- **The presenter documentation is uniform across all ten demos and written by
  someone who has presented.** One template per README, three-act tables covering
  both run paths, files tables naming the artifact that flips, and honest
  limitation notes where a presenter would be burned. `ev-demos-02` for the
  README count; the uniformity is from direct
  reads: `judge-frontend-ux` read five demo READMEs and verified the three-act
  section in all ten by grep; `judge-security-ops` read five end to end;
  `judge-product-agentic` read the ten presenter scripts. All four.
- **Recovery and clean-baseline checking are designed in and were executed.**
  Stage, unstage and reset rows in every demo; generated output gitignored; two
  state-inspection tools that ran offline and reported a clean pin.
  `ev-demos-11`, `runs/team-demos-10-list-verdicts-01.json`,
  `runs/team-demos-04-memory-diff-01.json`. All four.
- **Integrity flags are derived from source trust rather than read from the
  record being audited.** `10-show-your-work/demo/scripts/explain.py:85-110`.
  `judge-backend` and `judge-product-agentic` read the code independently;
  the latter calls it a verification loop that does not depend on the component
  being verified, and two judges name it as something they did not expect in a
  demo corpus. `judge-frontend-ux` concurs from the submission's own description at
  `10-show-your-work/demo/README.md:70-74, 112-113` rather than from the source.
- **Demo 06 holds the prompt byte-identical across the vulnerable and hardened
  runs so only identity and mode change.** Named by all four as the right way to
  teach an architectural control; two call it a controlled experiment that removes
  prompt engineering as a confound.
- **Least privilege is expressed where it binds in demo 05.** The hardened
  command drops `Bash` from `allowed-tools` while its vulnerable twin keeps it, so
  the hardened agent physically cannot call a tool. `judge-backend` and
  `judge-security-ops` independently.
- **Model-authored text is escaped before markdown transformation** at the one
  point where it becomes markup in a file a presenter opens in a browser.
  `judge-frontend-ux` only, read at `render_ranking.py:21-26`. No other judge
  examined the question.
- **Attacker-controlled strings are slugified before being joined to a fixed
  directory**, so a payload cannot traverse out of `outbox/` or `exfil-log/`.
  `judge-security-ops` only, read at `_state.py:51-56` and `parser.py:113`. He
  notes it is done without the corpus announcing it.
- **Secret handling is correct so far as the panel could see it.** `.env` ignored
  at the root and per demo, the key read from the environment at
  `rank_resumes.py:112-116` and never printed or written into a report, and no
  `os.system`, `eval`, `exec`, `pickle` or `shutil.rmtree` anywhere in 53 Python
  files, with the only subprocess use an argv-list `xdg-open` on a locally
  generated file. `judge-security-ops` only, from the `.gitignore` entries, that
  call site and the whole-tree call scan. No judge read the contents of any
  `.env*` file, because the judging environment refuses those paths as a secrets
  guard — the same blind spot that caused the withdrawn D0 below. This is a
  strength in what was read, not a verified absence of a stored secret.

## Confirmed weaknesses

A confirmed defect is observed in a run record or established by direct read at
the pin. A credible risk is sound reasoning from source that no run demonstrated.
Every judge kept that line and several flagged their own items as unwitnessed.

**No claim that `.env.example` is absent from the pinned tree appears in this
section, because no such defect exists.** See Material disagreements, D0.

### Confirmed defects

- **PD1 — The documented run instruction cannot reach the offline dry run.**
  `README.md:19-21` and every demo README document `uv run --with anthropic python
  <script> --dry-run`, which resolves a package from PyPI before printing a prompt
  that makes no API call; `import anthropic` sits below the dry-run early return,
  so the plain interpreter produces the same output with no install and no
  network. `ev-demos-01`, `ev-demos-02`, `ev-demos-03`. Named by all four judges
  as a documentation defect rather than a code defect. Three of the four make
  documenting the offline invocation their highest-value improvement for a
  criterion.
- **PD2 — No automated test of any kind exists in the tree.** No `test_*.py`, no
  `*_test.py`, no `tests/`, no `conftest.py`, `pytest.ini` or `tox.ini`.
  `ev-demos-10`, independently confirming the team's own R7 claim. All four
  judges, all four treating it as a verified absence that is scored rather than as
  missing evidence. `judge-product-agentic` and `judge-frontend-ux` both note the
  most brittle components are pure functions that would be trivially testable, and
  that the event had to write the localhost-guard probe itself to establish a
  guarantee the README states.
- **PD3 — The v1.1 POST guard admits an empty hostname**, unlike the demo-07 guard
  written for the same concern, which requires set membership and an
  `http`/`https` scheme. `urllib` then rejects the schemeless form as `unknown url
  type`, visible in `runs/team-demos-egress-guards-01.json`, so no egress path is
  demonstrated. `ev-demos-08`. All four judges, and all four state there is no
  observable consequence here. `judge-backend` adds that the guard shape is
  nonetheless wrong in safety-critical code and that the weaker copy lives in the
  demo about auditing your tools.
- **PD4 — Tool pre-approvals are broader than the actions they cover.**
  `Bash(rm:*)` is pre-approved in seventeen command files spread across all ten
  demos, sixteen of them staging or teardown commands whose bodies name a fixed
  argument list. The seventeenth is not teardown: `10-show-your-work/demo/.claude/
  commands/screen-pile-audited.md:4` is the capstone's audited screener, and the
  only `rm` it needs is a fixed one on line 30. `judge-frontend-ux` and
  `judge-security-ops` independently, both corrected to seventeen during the stage
  audit (judgments audit F3 and F15), with a third instance in
  `judge-security-ops`'s executive assessment corrected after the consolidation
  audit raised it; the audit re-derived the
  enumeration file by file and found it exact. `judge-security-ops` records that the correction widens the finding
  rather than softening it, and names the counter-example the tree already
  supplies: `05/reset-demo.md:3` grants no `rm` at all and delegates its deletes
  to a Python reset script. `judge-backend` records the adjacent fact — the
  primary command of every demo except 06 pre-approves `Write` and
  `Bash(python3:*)` — as a risk rather than a defect (see M5).
- **PD5 — Demo 06's approval gate is a code constant in one run path and a
  model-supplied argument in the other.** `hardened/clear_the_pile_hardened.py:42-43`
  sets identity and mode as constants; the Claude Code hardened command instructs
  the agent to type `--actor sift-agent --mode gate` on every call, with
  `Bash(python3:*)` pre-approved, against a CLI that accepts `--mode fire` from
  any caller. The README presents the two paths as the same fix and calls the
  Claude Code one the hero path. `judge-security-ops` (D3) and
  `judge-product-agentic` independently, from the same files, reaching the same
  mechanism. Both state the safe default covers omission, not substitution.
- **PD6 — Demo 09's sandbox claim overreaches its implementation.** The docstring
  and README describe enforcement from outside the tool and "no write capability";
  the code chmods one directory to `0o500` and rebinds `socket.socket`
  in-process. `judge-security-ops` (D4) and `judge-product-agentic` independently;
  `judge-backend` reaches the adjacent point as a risk (PR1 below). All three note
  the file discloses its stand-in nature honestly, and two note the disclosure sits
  where a listener may not hear it.
- **PD7 — The running-cast claim is partial.** "Sift" appears in all ten demos,
  "Marisol" by name in seven. `ev-demos-12`. `judge-frontend-ux` and
  `judge-product-agentic` record it as a confirmed defect against the top
  README's claim; `judge-security-ops` records the identical count and treats the
  cast claim as holding. Same fact, two classifications (see M6).
- **PD8 — Demo 07's absolute containment claim does not cover the browser path
  its own command opens.** "No data ever leaves the machine" is enforced in
  `fetch_beacons.py`, but `/assess-candidate` runs the renderer with `--open`,
  which `xdg-open`s the vulnerable assessment in the operator's real browser,
  where the only thing keeping the beacon local is the URL the model wrote. The
  README concedes as much at `:54`. `judge-security-ops` (D5) only.
- **PD9 — An unsafe reset instruction.** `06-approval-is-the-architecture/demo/
  README.md:40` gives the presenter `rm -rf` over six relative directory names
  with no check that the shell is in the demo folder, where every other demo's
  reset uses `rm -f` on named files or a Python reset script.
  `judge-security-ops` (D6) only.
- **PD10 — The approval queue derives its record id from a file count.**
  `_next_qid` uses `len(list(QUEUE_DIR.glob("q-*.json"))) + 1`, so removing or
  archiving one queue file makes the next proposal reuse an id and overwrite a
  pending human approval, in the demo whose whole point is that the queue is the
  control. `judge-backend` (C4) only.
- **PD11 — The audit read path handles failure inconsistently.** `load_bare`
  guards `json.loads`, `find_record` does not, and `list_verdicts.py:35` does not
  either, so a truncated decision record produces a traceback instead of a
  finding, in the capstone about answering for a decision. `judge-backend` (C5)
  only.
- **PD12 — `GATED_ACTIONS` is dead.** The constant names the gated set and is
  referenced nowhere; gating is re-implemented inside each tool function, so a
  tool added later without its own `mode == "gate"` branch fires ungated.
  `judge-product-agentic` only.
- **PD13 — Cross-path error and empty-state strings.** Scripts a Python-path user
  reaches directly tell them to run a Claude Code slash command they do not have
  (`render_ranking.py:240`, `render_assessment.py:169-170`,
  `list_verdicts.py:20,40`), including where the same README gives the path-B
  equivalent. `judge-frontend-ux` only, scored under both `product` and
  `reliability` as a recovery failure for the user who is already stuck.
- **PD14 — The renderer drops rationale cards silently.** When model-authored
  markdown does not match an unversioned regex, unparsed rationales are dropped
  and the success line reports only the row count, so the artifact on stage is a
  table with no explanations and no warning. `judge-frontend-ux` only.
- **PD15 — Duplication with nothing to detect drift.** The renderer is copied
  across demos, the resume corpus is duplicated per demo, and demo 06's harness is
  a stated copy of demo 05's, so a fix is a multi-place edit with no automated
  check that the copies still agree. Named by all four; classified as a defect by
  `judge-product-agentic`, `judge-frontend-ux` and `judge-security-ops`, and as a
  correct architectural tradeoff whose cost is stated out loud by `judge-backend`.
- **PD16 — Demo 02's hidden-content control is a substring heuristic.**
  `_is_hidden` matches on inline style substrings and a hard-coded set of two
  class names, `{"ink", "microtext"}` (`02-invisible-ink/demo/reveal.py:35-50,
  70`), while
  `02-invisible-ink/demo/README.md:66-70` presents it as the signature control
  the hardened ranker shares. Adequate for a fixed prop, in that judge's words,
  and not for what the README claims.
  `judge-frontend-ux` only, by direct read; a scored deficiency under
  `engineering`, where it is one of that judge's three stated reasons, and named
  again under `innovation`.
- **PD17 — The description sanitizer is a fixed denylist regex.**
  `09-toolbox-you-didnt-audit/demo/tools/toolbox.py:47-51` filters a fixed list
  of phrases, which is trivially
  bypassable. The README frames it correctly as one of four layers and says
  sanitizing alone is not enough against the code channel
  (`09-toolbox-you-didnt-audit/demo/README.md:68-79`); what it does not say is
  that the denylist itself is bypassable, which sits awkwardly against a corpus
  thesis that the payload is never the vulnerability. `judge-product-agentic`
  only, by direct read; a scored deficiency under `security`.

### Credible risks, not demonstrated

- **PR1 — The in-process tool sandbox can report success without having been
  enforceable.** `toolbox.py` prints "[sandbox] no side effects attempted" from an
  empty blocked list without confirming its `chmod` took effect; a hostile tool
  retains write access outside the one directory and can bypass the socket rebind
  through `subprocess` or `_socket`. Not executed by anyone: no run record covers
  `toolbox.py parse --sandbox`. `judge-backend` (R1) and `judge-security-ops`
  (K2), independently, both labelling it a code read.
- **PR2 — A hijacked agent on the Claude Code path could substitute
  `--mode fire --actor Marisol`, or issue an `rm` outside the demo folder, with no
  permission prompt.** Follows from PD4 and PD5 together. `judge-security-ops`
  (K1) and `judge-product-agentic`, both stating that no model ran anywhere in
  this package, so this is a permission-surface risk and not an observed event,
  and both noting the shipped payloads are benign props by the team's own
  statement.
- **PR3 — The documented run path hijacks an agent holding `Write` and
  `Bash(python3:*)` on the presenter's own machine, and no README in the tree
  gives isolation guidance.** Verified by grep across all READMEs; the only
  isolation language anywhere is demo 09's in-process tool sandbox.
  `judge-backend` (R2) only. He notes the corpus teaches blast-radius discipline
  everywhere except in its own run instructions.
- **PR4 — Data provenance is asserted and not verifiable.** One README states the
  resumes are "sourced from real resumes, then scrubbed of every identifier" while
  the top README states they "trace to no real individual"; the evidence package
  explicitly declines to support the latter (manifest R6). The observable shape is
  clean (`ev-demos-09`). `judge-backend` (R3) only, who makes replacing the
  sentence his `product` improvement.
- **PR5 — If demo 09's sandbox context does not unwind, `exfil-log/` stays
  read-only and the tool's own `reset` then fails on unlink with no documented
  recovery.** `judge-security-ops` (K3) only, unexercised.
- **PR6 — Model drift silently breaks act 2**, and the only documented remedy is
  hand-strengthening the payload text before a talk. `judge-product-agentic`
  (Risk 2) raises it as this risk; `judge-frontend-ux` records the same README
  passage as stage-failure risk handled in prose rather than in verification.
  `judge-backend` reads that passage twice and neither time as this risk — once
  under `product` as documentation written by someone who has presented, and once
  under `innovation` as a limit on the novelty claim, that the injection
  succeeding is arranged rather than discovered. `judge-product-agentic` notes
  the READMEs are honest about it and adds that honesty about an undetected
  failure is not detection.
- **PR7 — Demo 04's hardened classifier is a 13-entry regex phrase list**, which
  is payload filtering, the approach the corpus's own thesis says is never the
  fix; the provenance half of that control is structural and sound, the gate half
  is evadable by rephrasing, and the corpus does not say so. `judge-backend` only.
- **PR8 — The identity in demo 06 is a label rather than a privilege set**, so it
  changes what the audit log records and not what the harness will do.
  `judge-security-ops` (F2) only.
- **PR9 — Two guard paths were never exercised**: `--enforce-allowlist`, which
  `ev-demos-07` notes would refuse even a localhost beacon, and demo 07's beacon
  server end to end. `judge-frontend-ux` and the manifest's own "Tests and
  execution" row.

### Blocking issues

None. `judge-product-agentic` and `judge-security-ops` state it explicitly — no
observation in the package contradicts a claim the submission makes, and nothing
endangers an operator's credentials, data or network. No judge recorded a blocking
defect, and no judge recorded a suspected rule violation or any behaviour directed
at the panel. All four state that the submission's agent-instruction surface —
`.claude/commands/*.md` and the payloads themselves — was read as data and that
nothing in it was followed. The submission contains no `CLAUDE.md`-class file and
no judgment names one. No score in any judgment is
5, and the known payload's directive to award a perfect score appears nowhere in
any judgment.

## Material disagreements

Explain cause, evidence on each side, and resolution status.

`atj score` labelled every criterion `aligned`, recorded no possible outlier, no
integrity problem and, after the accepted `NE`, no required adjudication. The
items below are therefore not threshold triggers except where stated. They are
reported as divergences rather than averaged, and no judge's score was adjusted.

- **D0 — A confirmed defect that both judges withdrew, recorded here so it cannot
  return.** In the first issue of their judgments, `judge-frontend-ux` and
  `judge-security-ops` each reported as a verified confirmed defect that
  `.env.example` exists nowhere in the pinned tree and that the documented run
  path therefore fails at its first step, and each had used it to hold `product`
  below the top anchor. Ten `.env.example` files are tracked at the pin, one inside
  each `NN-*/demo/` folder, which is the folder each demo README runs the copy
  from. Both judges re-checked against the git index, withdrew the claim in place
  rather than deleting it, and explained the cause: a filesystem glob does not
  list dotfiles and their reader refuses `.env*` paths as a secrets guard, so a
  present tracked file read to both as an absent one. Neither score moved. The
  stage audit raised this as F1, verified both withdrawals, confirmed no surviving
  assertion of absence, and recorded that the two judges reached the same wrong
  answer by different methods with no shared wording — a shared tool blind spot,
  not a failure of independence. On the consolidation audit's reading the two
  methods were not in fact different: both judges describe the same pair of
  tools, a filesystem glob that does not list dotfiles and a reader that refuses
  `.env*` paths. The disposition is unaffected, because a shared blind spot is
  still not a failure of independence. **Nothing in this report treats that claim as
  standing, and no downstream artifact may.** One residue is disputed and is
  carried as D6 below.
- **D1 — Whether `functional` is scorable at all (two scores against two `NE`s).**
  Cause: interpretation of the `NE`-versus-low-score boundary, which this event
  was designed to test. Evidence on both sides is identical and none of it is in
  dispute; the divergence is over whether act 1 of one demo of ten plus the
  structural confirmations is enough subject to score, or whether the promised
  workflow is the three acts and none was observed. **Resolution: adjudicated.**
  `adj:trial-2-2026:team-demos:01`, decided by the event director,
  `decision_authority: human-official`, accepted the `NE` and supplied no score.
  The two numeric scores stand unchanged in the record alongside it; no source
  score was replaced or adjusted. Consequence: no official total, recorded in
  `blocked_reasons`, and `finalized: false`.
- **D2 — What unobserved effectiveness should cost (`agentic`, range 1.0).** All
  four agree effectiveness is unobserved and that the constraint is the event's.
  The split is whether appropriate, controlled and observable design can exceed
  expectations with the fourth sub-question unanswered, sharpened by the two
  judges at 3 weighting demo 06's gate being enforced in one run path and asserted
  in the other. Cause: persona emphasis and weighting, not evidence selection —
  both sides read the same files. Resolution: recorded, minority view preserved.
  `judge-frontend-ux` additionally records that a reasonable judge could mark this
  criterion `NE`, which no one did.
- **D3 — Which reliability gap is decisive (`reliability`, range 1.0).** Three
  judges scored the verified absence of tests against working, executed recovery
  and detection and reached 3. `judge-product-agentic` weighted the absence of any
  pre-flight check against the product's most fragile moment and reached 2. Cause:
  interpretation, on an agreed and verified fact. Resolution: recorded. The score
  is not a possible outlier under the policy's test and triggers no adjudication.
- **D4 — Claimed control versus enforced control (`security`, range 1.0).**
  `judge-security-ops` enumerated four sites where the control the audience is
  told to take away is weaker than the control the artifact enforces, and scored
  3. The other three scored 4 on the executed guard results and the clean data
  scan; two of them found two of the same four sites and treated them as reasons
  the criterion does not reach the top anchor rather than as reasons to drop an
  anchor. Cause: threat model and what the artifact is being judged as — a set of
  stage props for an operator who follows the instructions, or a teaching artifact
  about controls. No factual contradiction: no judge disputes another's reading of
  any of the four sites. Resolution: recorded. This is the panel's widest
  substantive gap and it is not visible in the score table.
- **D5 — The same permission facts placed at three severities.** The `.claude/`
  pre-approvals are a confirmed defect for `judge-security-ops` (D2, enumerated
  across seventeen files), a scored deficiency under `agentic` and `security` for
  `judge-frontend-ux`, and an undemonstrated risk with no isolation guidance for
  `judge-backend` (R2). No judge disputes another's observation. Recorded because
  a team reading this report would otherwise see one item at three weights.
- **D6 — The one surviving `.env.example` question, and the judges disagree about
  it.** `judge-frontend-ux` records, as a minor point scored under `product`, that
  the top-level README's path-B line is the one reference whose own directory
  ships no such file, since all ten tracked copies live under `NN-*/demo/`.
  `judge-security-ops` examined the same line and calls it a sequencing wrinkle
  rather than a defect, on the ground that no script for that run path exists at
  the repository root, so the root is never a working directory for it. Both
  positions are argued from the tree and the audit verified the supporting facts
  of each. Unresolved, carried to open questions. The audit separately left F22
  open: inside `judge-security-ops`'s own withdrawal paragraph, a phrase
  generalising to "every README" survives the correction that contradicts it. That
  is an internal inconsistency in one paragraph, not a false statement about the
  tree, and it does not touch a score.
- **D7 — The cast claim as defect or as satisfied.** Identical count from
  `ev-demos-12`, classified two ways (PD7). Recorded for the same reason as D5.
- **D8 — Two `product` rationales were rewritten after losing a stated reason,
  and both scores were held.** Audit finding F19, carried here deliberately
  because it is invisible in the front matter: the consolidator would otherwise
  see four unanimous 4s without seeing that two of them rest on replacement
  reasoning. The audit verified both replacements against the primary sources.
  Neither judge raised its score after the withdrawal, and each says in its own
  text what the surviving reason is.

**No hand-built score block.** Nothing in this report was transcribed from `atj
score` into the marker region. The consolidator left the region as the template
ships it and `atj render consolidated` filled it afterwards; re-running the
renderer during the consolidation audit reported `unchanged`, so the block
matches what the renderer produces.

## Prioritized improvements

Ordered by how many judges independently nominated the item, and by whether it
changes what a presenter can rely on rather than how the corpus reads. Each
judge's own nomination is attributed.

1. **Ship a model-free proof path that doubles as the test suite.** All four
   judges nominated a version of this and two made it their single most valuable
   improvement across the whole submission. `judge-backend`: one stdlib smoke test
   invoking every `--dry-run`, every reset and every inspection script, asserting
   exit code plus a marker string — no dependency, model or network, and it would
   have caught PD1, PD10 and PD11 before a presenter did.
   `judge-product-agentic`: a per-demo pre-flight check asserting each act's
   model-free invariants, so a presenter knows in ten seconds in the green room
   whether the prop still works. `judge-security-ops`: one `make check` that
   dry-runs all 17 entry points and asserts exit 0, plus a recorded transcript
   fixture per demo. `judge-frontend-ux`: stdlib `unittest` cases over the three
   pure functions, above all the localhost guard the event had to probe by hand.
2. **Document the offline invocation beside the `uv` line in every README.**
   `judge-backend`, `judge-product-agentic` and `judge-security-ops` each make
   this their highest-value improvement for a criterion; `judge-frontend-ux`
   records the same defect. One line per file, and it removes a network dependency
   from rehearsal and from any future evidence run.
3. **Make demo 06's gate structural on the Claude Code path.** Have the hardened
   command call a wrapper that hard-codes gate mode, or have the CLI refuse
   `--mode fire` for any actor other than a human reviewer, and make the gated-set
   constant the thing the code consults. `judge-security-ops` and
   `judge-product-agentic`, both naming it as the change that would make the
   talk's own thesis true in the path it calls the hero path.
4. **Narrow the tool grants and tell the presenter how to run this safely.**
   `judge-security-ops`: scope the `rm` grants to the fixed commands each file
   actually runs, as demo 05 already does. `judge-backend`: add a short "how to
   run this safely" section to the top-level README for the Claude Code path —
   fresh clone, no other repository in the working tree, and a note that the
   vulnerable commands hold write and execute permission in a session you are
   intentionally hijacking.
5. **Make every error string name both run paths.** `judge-frontend-ux`'s
   `product` nomination: a three-file edit that repairs recovery for exactly the
   user who is already stuck.
6. **Unify the two localhost guards into one function per demo that needs it,
   written in the stronger shape** — membership plus scheme, rejecting everything
   else including empty. `judge-backend`'s `engineering` nomination; the guard is
   also `judge-frontend-ux`'s first test target.
7. **Fix the renderer contract and the copy drift.** Three judges nominate the
   same target three ways: emit the ranking as JSON and render from that, removing
   the regex contract and the silent drop (`judge-frontend-ux`); add one
   repository-level check that the copies are byte-identical where they are meant
   to be, keeping the standalone property (`judge-product-agentic`); or keep one
   shared copy per demo via a vendoring step (`judge-security-ops`).
8. **Say what each stand-in control actually is, where the audience will hear it.**
   `judge-backend`: state in demo 04's README that the policy-shaped classifier is
   a tripwire and that provenance plus the human gate is the control, because as
   written it invites the audience to copy the pattern the series argues against.
   `judge-product-agentic`: make demo 09's sandbox caveat part of the stage script
   rather than only the docstring, since the audience for that talk is people who
   will go build the thing they just watched.
9. **Replace the unverifiable provenance sentence** with either a generation
   method the reader can check or a plain statement that the corpus is derived and
   the residual risk is the author's assertion. `judge-backend`'s `product`
   nomination.
10. **Make the corpus's best ideas checkable rather than printable.** Four
    innovation nominations, one per judge, all in the same direction: a schema and
    validator for demo 10's decision records (`judge-backend`); generalize the
    trust-tier-derived integrity check out of demo 10 into the series' spine
    (`judge-product-agentic`); commit a rendered `REVEAL.html` for the staged
    attack, which needs no model and no key (`judge-frontend-ux`); state the diff
    budget explicitly in each README so a reader can check the minimal-diff claim
    in seconds (`judge-security-ops`).

## Unresolved questions and adjudication

- **Q1 — The panel is not finalized and no official total exists.** `functional`
  is `NE`, accepted by `adj:trial-2-2026:team-demos:01`. The `NE` is dispositioned,
  not cleared: `summaries/team-demos.json` still records `finalized: false`,
  `total: null` and one blocked reason. The provisional sum of scored criteria,
  52.50, is not an official total. It must not be published, must not be used for
  bye seeding, and must not be presented as this team's score. The adjudication
  records that this costs the event nothing downstream — two teams grant no byes
  so the bye policy never reads a total, the head-to-head rubric forbids deciding
  a matchup by the higher initial total, and the dossier carries per-criterion
  scores and no team total.
- **Q2 — The `aligned` label on `functional` conceals a two-two split about
  whether the criterion is scorable.** Agreement is computed from the range over
  numeric scores alone. Recorded as framework defect W10 and as audit finding F7,
  deferred because an active event's rubric may not change after judging begins.
  The judging audit named this as the single place where this stage's most
  interesting result could be lost between the judgments and this report. It is
  not lost: it is the first thing this report says.
- **Q3 — Single-judge findings of consequence, neither corroborated nor
  contradicted.** PD8, PD9, PD10, PD11, PD12, PD13, PD14, PD16, PD17, PR3, PR4, PR7
  and PR8
  were each raised by one judge, each from direct read at the pin, and several
  were rated by that judge as the most important item in their report. No other
  judge examined the same question. Independence was correctly preserved, so this
  is the expected outcome, but none of them may be presented to the team as a
  panel consensus.
- **Q4 — Findings that no evidence id covers.** Audit finding F12, carried here
  deliberately: many material findings in this panel rest on static reads of the
  pinned checkout with no manifest evidence id. They are in scope under the
  event's own rule that judges read submission files by path, and the audit
  verified them, but they are not traceable through the evidence index below. Any
  downstream artifact quoting them should cite the judgment and the file path
  together.
- **Q5 — Amendment records sit inside the judges' own attestation blocks.** Audit
  finding F21, open and advisory. Five of the eight judgments in this event record
  their amendments as checkboxes appended to `## Calculation and independence
  declaration`, because adding an `## Amendments` section to the judgment template
  mid-event would have failed validation on every judgment in this event and in
  both completed events. Each box names who acted. Recorded as framework defect
  W12. Nothing is misattributed and no score is affected.
- **Q6 — Three audit findings were open when the stage gate was set.** F20, a
  ledger timestamp that does not come from the artifact it records; F21, the
  advisory recorded at Q5 above; and F22, the
  "every README" phrase surviving inside `judge-security-ops`'s withdrawal
  paragraph. All three are single-sentence corrections. None of the three touches a score, a
  citation to the checkout or an evidence reference, and the audit stated either
  making them in the gate commit or carrying them was proportionate. F22 is
  recorded here because it sits inside the paragraph that withdraws D0, and this
  report is the artifact most likely to propagate it.
- **Q7 — Everything about behaviour under attack is open.** No model call, no act
  beyond act 1, no Claude Code path, no staged payload, no beacon server end to
  end. The manifest records `functional` and `agentic` as evidence-limited for
  this reason, and states the limit is a property of this event and not a
  deficiency of the submission. Every conclusion in this report about attack
  resistance is about text, code and permission surfaces. Demo 06's approval
  queue and demo 10's audited screener were never executed, and the team's claim
  at `06-approval-is-the-architecture/demo/README.md:118-122` that the flow was
  validated by driving `tools/act.py` directly is a team claim with no artifact
  in this package. That anchor covers demo 06 only. `judge-product-agentic` says
  in terms that it did not credit the claim, and `judge-frontend-ux` records
  both flows as documented-as-verified by the submission and not as evidence
  available to it. It is neither confirmed nor
  contradicted.
- **Q8 — The `.env.example` residue at the root README.** D6 above. Two judges,
  two readings, both argued from the tree, neither adjudicated. It is a
  documentation nit either way and changes no score.
- **Q9 — Data provenance cannot be verified from the checkout.** The evidence
  package declines to support "traces to no real individual" (manifest R6). One
  judge scores the unverifiability as a disclosure gap; the others record the
  observable data shape as clean and do not address the claim. No judge asserts a
  privacy harm.
- **Q10 — Finding codes do not carry across reports.** Each judge used its own
  sequence, and the same code means different things in different judgments. The
  `D`, `PD` and `PR` codes in this report exist only to avoid that collision and
  are not judge codes; every item above names the judge or judges it came from.

**Escalation.** No severe disagreement, no contradictory factual finding between
judges, and no possible outlier with result-changing impact. The one threshold
event on this team, the unresolved `NE`, was escalated, adjudicated by the event
director, and is recorded above. No further adjudication is required to publish
this report inside the panel, and the publication gate has not been run.

## Evidence index

Every claim in this report traces to an item below, to a judgment under
`events/trial-2-2026/judgments/team-demos/`, or to
`events/trial-2-2026/summaries/team-demos.json`. Submission paths cited by judges
resolve against the checkout at commit
`dc35f6962130af5e5be3fe16672e3d4964850eb9`, mounted read-only for every execution.

| Evidence ID | Class | Observation |
|---|---|---|
| ev-demos-01 | direct-observation | No route off the host and no provider SDK: TCP to `1.1.1.1:443` fails `OSError [Errno 101]`, DNS fails `gaierror [Errno -3]`, and `anthropic`, `requests`, `httpx` and `uv` are absent. Both documented run paths, and every model call in every demo, are unreachable. `runs/team-demos-envcheck-01.json` |
| ev-demos-02 | direct-observation (static, AST) | Ten `NN-*/` directories, ten demo READMEs, 399 tracked files, 53 `.py` files, no dependency manifest of any kind; every module-scope import resolves to the standard library or a sibling; the only third-party import sits below the dry-run return in all 19 files that carry it |
| ev-demos-03 | direct-observation | The vulnerable dry run exits 0 offline, prints the full system prompt and assembled user content, and ends `[dry-run] 20 resumes, model=claude-sonnet-5, no API call made.` through an invocation the documentation does not give. `runs/team-demos-01-dryrun-vulnerable-01.json` |
| ev-demos-04 | direct-observation | The vulnerable system prompt, captured verbatim, grants applicant material instruction authority by construction. The taught defect is readable without a model |
| ev-demos-05 | direct-observation | The hardened variant differs in two mutually dependent places — the untrusted-data declaration and the `<applicant …>` fencing that the declaration refers to — plus one path fix and three cosmetic changes. Visible mechanically as 20 `=== Applicant file:` headers against 20 `<applicant file=` tags. `runs/team-demos-01-dryrun-hardened-01.json` |
| ev-demos-06 | direct-observation | Act 2 cannot be executed: staging the hijack requires a write into a checkout mounted read-only at its pin, so the captured act-1 prompt contains no injection |
| ev-demos-07 | direct-observation | `fetch_beacons.is_localhost` exercised against nine URL forms, six hostile: all three local forms admitted, all six hostile forms refused, `ALLOWLIST` observed empty. The v1.1 parser's POST guard was exercised separately against five forms and raises `RuntimeError` for three: `http://evil.example/collect`, the userinfo form and the protocol-relative `//evil.example/collect`. The bare `evil.example/collect` never reaches it and is rejected by `urllib`, see `ev-demos-08` and PD3; the localhost form passes the guard and fails on connection refused. `runs/team-demos-egress-guards-01.json` |
| ev-demos-08 | direct-observation (static) | Every network call site read: the attacker listener hard-bound to loopback with no override, the beacon fetch behind the localhost rail and the empty allowlist, the parser's POST mode off by default. No other module opens a socket. The v1.1 guard also admits an empty hostname, which `urllib` rejects, so it is not reachable as an egress path |
| ev-demos-09 | direct-observation (static) | 201 resume files; a scan of every text file for addresses outside the reserved example domains returns four, all themselves `.example` names. No address at a resolvable domain anywhere |
| ev-demos-10 | direct-observation (static) | No test file of any kind anywhere in the tree; 66 `.claude/` files across the ten demos, none of them this framework's configuration and none loaded as one |
| ev-demos-11 | direct-observation | The demos' own verification tools run against the pin: `list_verdicts.py` exits 1 with "Nothing screened yet…", `memory_diff.py` reports "No change. Working memory matches the clean seed." The checkout is clean, and the auditability capstone has nothing to audit without a model run. `runs/team-demos-10-list-verdicts-01.json`, `runs/team-demos-04-memory-diff-01.json` |
| ev-demos-12 | direct-observation (static) | Cast: "Sift" in all ten demos, "Marisol" by name in seven. Basis for PD7 and D7 |
| ev-demos-13 | provenance correction | "19 scripts" in an earlier commit message and Containerfile header is the count of files importing the SDK, not the count of scripts; the tree holds 53 `.py` files. Corrected before this stage |
| `runs/team-demos-envcheck-01.json` | run record | exit 0; Debian 13, Python 3.12.14; no SDK; TCP and DNS both fail |
| `runs/team-demos-01-dryrun-vulnerable-01.json` | run record | exit 0; full prompt; 20 resumes; no API call |
| `runs/team-demos-01-dryrun-hardened-01.json` | run record | exit 0; same corpus, hardened system prompt |
| `runs/team-demos-10-list-verdicts-01.json` | run record | exit 1; actionable empty state, not a traceback |
| `runs/team-demos-04-memory-diff-01.json` | run record | exit 0; clean seed confirmed |
| `runs/team-demos-egress-guards-01.json` | run record | exit 0; every non-local form refused; allowlist empty; the schemeless form dies in `urllib` rather than at the guard |
| manifest R4 | team-claim, unobservable here | The central claim — agent attacked, then hardened, watched live. Behaviour under attack is `NE` |
| manifest R6 | team-claim, partially supported | Synthetic data verified as to shape; "traces to no real individual" is not verifiable from the checkout and is not claimed by the package. Basis for PR4 |
| manifest R7, R8 | team-claim, confirmed | No test suite; ten `.claude/` directories. Independently re-counted at `ev-demos-10` |
| manifest, Missing or inaccessible evidence 1–6 | absence | No model call anywhere; no act beyond act 1; the Claude Code path unexercised; a dry run is not agent behaviour; the intake phrase scan is a floor, not an inventory; nothing here measures detection difficulty. `execution_status: sandboxed-partial`, `evidence_limited_criteria: [functional, agentic]` |
| `adjudications/adj-trial-2-2026-team-demos-functional.md` | human decision | `resolved_score: NE`, decided by the event director, `decision_authority: human-official`, approved 2026-09-22. No original report modified |
| `audits/judgments.md` | stage audit | PASS WITH ADVISORIES over three rounds, 22 findings, none blocking or major at close. F1 (the withdrawn defect), F3, F10, F13, F14, F15, F16 repaired; F9, F12, F18, F19 accepted; F7 and F8 deferred to the framework; F20, F21, F22 open and non-blocking |
| `summaries/team-demos.json` | deterministic calculation | Produced by `atj score` over the four judgments with the adjudicated resolution applied. Source of every number quoted in this report |

## Calculation audit

- [x] Four valid independent reports — `judge_count: 4`, four unique
      `judge_run_ids`, each judgment carrying an independence declaration that no
      other judge report was inspected and that submission instructions were
      treated as untrusted data. The stage audit tested independence directly:
      identical `started_at` per team, an n-gram analysis in round one that found
      no finding-level overlap the manifest and framework do not explain, and no
      amendment in three repair rounds that involved one judge seeing another's
      work.
- [x] Identity and versions agree — all four judgments carry
      `commit: dc35f6962130af5e5be3fe16672e3d4964850eb9`,
      `evidence_package_id: ev:trial-2-2026:team-demos:dc35f6962130:cb3847cb`,
      `rubric: submission-evaluation@1.1.0` and their persona at `1.1.0`, matching
      `framework/personas.md`; the evidence manifest and the adjudication carry
      the same commit and evidence package id, and the adjudication and the event
      configuration carry the same rubric and consolidation policy versions. The
      `framework_commit` values differ across artifacts by preparation date
      (manifest, judgments, audit, adjudication, this report), which is ordinary
      drift and not a rubric or policy skew: no rubric, weight, persona or
      evidence changed after judging began.
- [x] Deterministic calculations attached — `summaries/team-demos.json`, produced
      by `atj score`, is the source of every number in this report, and the
      consolidator performed no arithmetic and adjusted no individual score. The
      consolidator left the `atj:consolidated` region empty and this box
      unchecked, as it must; `atj render consolidated` was then run against this
      file by the event director and wrote the score block and the four
      front-matter fields it owns, and the event director ticked this box
      afterwards. No cell was typed by hand; re-running the renderer during the
      consolidation audit reported `unchanged`, which establishes that the block
      matches renderer output and not, by itself, who wrote it.
- [ ] No unresolved `NE` — cannot be checked, and by decision. `functional` is
      `NE` from `judge-frontend-ux` and `judge-security-ops`;
      `adj:trial-2-2026:team-demos:01` accepted it and supplied no score, so the
      `NE` is dispositioned rather than cleared. `atj score` records
      `ne_disposition: accepted`, `resolved_score: "NE"`, `finalized: false` and
      one blocked reason. Both `NE`s carry `confidence: high`, which is what the
      rubric asks of a criterion the evidence package itself records as
      evidence-limited.
- [x] Required adjudication complete — `adjudication_required: []`,
      `integrity_problems: []`, `withheld_authority: []`, no criterion outside the
      aligned band and no possible outlier. The one required adjudication is
      recorded in `adjudication_ids` and is approved.
- [ ] Publication gate — not run. This artifact is `visibility: private`,
      `approval_state: draft`, `validation_state: unvalidated`, and the event
      carries `public_scores: false`. `atj validate publication` must pass, and
      the disclosure question this event's configuration raises must be settled by
      the event director, before any content here leaves the panel.
