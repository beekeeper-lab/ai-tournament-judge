---
event_id: trial-2-2026
team_id: team-demos
commit: dc35f6962130af5e5be3fe16672e3d4964850eb9
evidence_package_id: ev:trial-2-2026:team-demos:dc35f6962130:cb3847cb
rubric: submission-evaluation@1.1.0
persona: build-team-dossier@1.0.0
framework_commit: 566166b
source_reports:
- summaries/team-demos.md
- summaries/team-demos.json
- judgments/team-demos/
- adjudications/adj-trial-2-2026-team-demos-functional.md
- evidence/team-demos/manifest.md
- runs/team-demos-envcheck-01.json
- runs/team-demos-01-dryrun-vulnerable-01.json
- runs/team-demos-01-dryrun-hardened-01.json
- runs/team-demos-04-memory-diff-01.json
- runs/team-demos-10-list-verdicts-01.json
- runs/team-demos-egress-guards-01.json
- matchups/mu-final-01.md
model_requested: claude-opus-5
model_used: claude-opus-5-5[1m]
started_at: "2026-09-23T19:58:08Z"
completed_at: "2026-09-23T20:01:27Z"
visibility: team
approval_state: approved
validation_state: valid
approved_by: event-director
approved_at: "2026-09-24T00:14:24Z"
approval_note: Approval delegated by the event-director in session, 2026-09-23; run by the orchestrator
---

# Team Dossier — AI Security Demos

## Your project at a glance

AI Security Demos is a presenter's kit: ten talks, each staging one attack on an
LLM screening agent ("Sift") and then showing the minimal change that stops it.
Four judges evaluated it independently, at commit `dc35f696`, against one shared
evidence package (`ev:trial-2-2026:team-demos:dc35f6962130:cb3847cb`) under
`submission-evaluation@1.1.0`.

**You won the final.** Your matchup against the other finalist was confirmed in
both presentation orders, with no adjudication and no tie-break. See
[Tournament journey](#tournament-journey).

**There is no official panel total, and that is not a mark against you.** This
event's sandbox had no network route and no provider SDK, so no model call was
possible anywhere (`runs/team-demos-envcheck-01.json`). That means the heart of
every demo — an agent being hijacked, then resisting — could not be observed.
Two judges recorded `functional` as `NE` (not evaluable) for that reason, two
scored it from what did run, and the event director reviewed the split and
accepted `NE` rather than supply a number for something nobody saw
(`adjudications/adj-trial-2-2026-team-demos-functional.md`). The rubric allows no
official total while any criterion is `NE`. The limitation belongs to the event,
and every judge said so.

What the judges could observe, they could observe well, largely because of a
choice you made: every presenter tool is standard-library Python with no
dependency manifest, and the one third-party import sits below each script's
dry-run early return. That is why so much of the corpus was judgeable offline.

### What this result does not cover

- Agent behaviour under attack, in any demo. Nothing in this dossier says an
  attack lands or a hardening holds against a live model.
- Acts 2 and 3. Staging them writes into the checkout, which was mounted
  read-only at your pinned commit (manifest, "Missing or inaccessible evidence").
- The Claude Code run path. It could not be exercised at all.

## What you did especially well

Items here were reached by all four judges unless a single judge is named.

- **Your egress guards are real controls and they held under execution.** The
  event put nine URL forms through `fetch_beacons.is_localhost`, six of them
  hostile, including userinfo confusion (a `localhost` prefix before an `@`
  and a hostile host), suffix confusion (`127.0.0.1.evil.example`) and the decimal form `2130706433`. Every
  non-local form was refused, and the allowlist was observed empty in the same
  run (`runs/team-demos-egress-guards-01.json`). Several judges noted these are
  exactly the cases a hand-rolled host check usually lets through.
- **Nothing in the tree reaches the network by surprise.** The attacker listener
  is hard-bound to loopback with no override, the malicious parser's POST mode is
  off by default and writes a local file instead, and no other module opens a
  socket. This rests on the evidence package's tree-wide read (`ev-demos-08`),
  which all four judges cited.
- **Your sample data is clean.** Across 201 resume files, the only addresses
  outside reserved example domains are themselves `.example` names
  (`ev-demos-09`).
- **The taught fix is a real data/instruction boundary.** In demo 01 the hardened
  system prompt declares `<applicant>` content untrusted, and
  `build_user_content` is what emits those tags, so neither half works without the
  other. The two dry-run captures show it mechanically: 20 plain headers against
  20 fenced tags (`ev-demos-05`, `runs/team-demos-01-dryrun-hardened-01.json`).
- **Your presenter documentation is uniform and written by someone who has
  presented.** Every demo README carries the same shape — premise, both run
  paths, a three-act table, why the fix works, a files table naming the artifact
  that flips, and notes where a presenter would get caught out. The frontend
  and UX reviewer confirmed the three-act section is present in all ten.
- **Recovery and clean-baseline checks are designed in, and they ran.** Stage,
  unstage and reset exist for every demo, and two state tools ran offline and
  gave meaningful results: `list_verdicts.py` exited 1 with an actionable empty
  state, `memory_diff.py` confirmed the clean seed (`ev-demos-11`).
- **Demo 10 derives integrity flags from source trust rather than trusting the
  record being audited** (`10-show-your-work/demo/scripts/explain.py:85-110`).
  Two judges, the backend reviewer and the product and agentic reviewer, read the
  code and singled it out; the backend reviewer called it the kind of thing that
  usually appears only after someone has been burned.
- **Demo 06 holds the prompt constant across the vulnerable and hardened runs**,
  so only identity and mode change and the lesson cannot be mistaken for prompt
  tuning. Named by three judges: the backend reviewer, the frontend and UX
  reviewer, and the product and agentic reviewer.
- **Demo 05 expresses least privilege where it binds**: the hardened command drops
  `Bash` from `allowed-tools` while its vulnerable twin keeps it. Named by two
  judges, the backend reviewer and the security reviewer.

Three further strengths were each seen by one judge:

- The frontend and UX reviewer found model-authored text is HTML-escaped before
  markdown rendering in the file a presenter opens in a browser
  (`render_ranking.py:21-26`).
- The security reviewer found attacker-controlled strings are slugified before
  being joined to an output directory, so a payload cannot traverse out of it
  (`_state.py:51-56`, `parser.py:113`).
- The security reviewer found `.env` ignored at the root and per demo, the key
  read from the environment and never printed, and no `os.system`, `eval`,
  `exec`, `pickle` or `shutil.rmtree` in any of the 53 Python files. This is a
  statement about what was read. The judging environment does not open `.env*`
  files, so no judge inspected their contents.

## Criterion feedback

Scores are the panel means from `summaries/team-demos.json`, produced by
`atj score`. Judge scores are listed without names; the criterion sections say
who found what.

| Criterion | Judge scores | Panel |
|---|---|---|
| Functional correctness and completeness | 3, 3, NE, NE | **NE**, accepted by the event director |
| Product value and usability | 4, 4, 4, 4 | 4.00 |
| Agentic and AI system design | 4, 4, 3, 3 | 3.50 |
| Engineering and maintainability | 3, 3, 3, 3 | 3.00 |
| Reliability, testing, and observability | 3, 3, 3, 2 | 2.75 |
| Security, privacy, and responsible AI | 4, 4, 4, 3 | 3.75 |
| Innovation and technical ambition | 4, 4, 4, 4 | 4.00 |

### Functional correctness and completeness — NE

**What was shown.** Act 1 of demo 01 ran correctly in both variants: each exited
0 with no network, printed the full system prompt and assembled content over 20
resumes, and stated that no API call was made
(`runs/team-demos-01-dryrun-vulnerable-01.json`, `…-hardened-01.json`). The two
state tools behaved correctly.

**Why it is NE.** The headline workflow needs a model. The backend reviewer and
the product and agentic reviewer scored 3 on what ran; the frontend and UX
reviewer and the security reviewer recorded `NE` because a dry run is not the
promised behaviour. The event director accepted `NE`. Both positions are
reasonable readings of the same evidence.

**Next step.** All four judges named the same documentation gap: every README
gives `uv run --with anthropic python <script> --dry-run`, which fetches a package
from PyPI before printing a prompt that makes no call. Plain
`python3 <script> --dry-run` produces the same output with no install and no
network. Document it beside the `uv` line.

### Product value and usability — 4.00

**Strengths.** A complete presenter's kit with rehearsal-aware detail: honest
notes on cost, on which folder commands run from, and on what to do if a future
model shrugs off an injection.

**Limitations.** The offline invocation above. The frontend and UX reviewer found
error and empty-state strings name only Claude Code commands even for a
Python-path user (`render_ranking.py:240`, `render_assessment.py:169-170`,
`list_verdicts.py:20,40`), and no troubleshooting, minimum Python version or
degraded-mode guidance in the top README. The backend reviewer flagged that one
README says the resumes were "sourced from real resumes, then scrubbed" while the
top README says they "trace to no real individual"; the evidence package could
verify the data's shape but not its provenance.

**Next step.** The frontend and UX reviewer's suggestion: make every error string
name both paths. It is a three-file edit that helps exactly the user who is
already stuck.

### Agentic and AI system design — 3.50

**Strengths.** Controls are readable without a model: the demo 01 boundary,
demo 06's approval queue with human attribution, demo 04's provenance on memory
writes, demo 08's per-candidate context isolation, demo 10's trust-tier integrity
check.

**Limitations.** Effectiveness against a live model is unobserved, which is why no
judge went above 4. Two judges, the security reviewer and the product and agentic
reviewer, independently found that demo 06's gate is a code constant in the
Python path but a model-typed argument (`--actor sift-agent --mode gate`) in the
Claude Code path, which the README calls the hero path. The product and agentic
reviewer found `GATED_ACTIONS` is referenced nowhere, so gating depends on each
tool function remembering its own branch. The backend reviewer noted demo 04's
hardened classifier is a regex phrase list, which is payload filtering, the
approach the series argues against.

**Next step.** Make demo 06's gate structural on the Claude Code path: a wrapper
that hard-codes gate mode, or a CLI that refuses `--mode fire` from anyone but a
human reviewer. Both judges who found the gap proposed this.

### Engineering and maintainability — 3.00

**Strengths.** Uniform layout, stdlib-only, consistent path handling, docstrings
that state their own limits, and a stated reason for duplicating code so each
folder runs standalone. The backend reviewer called that tradeoff the right one.

**Limitations.** Duplication with nothing to catch drift: the renderer, the resume
corpus and demo 06's harness are copied across demos. Three judges treated this
as a defect; the backend reviewer treated it as a correct tradeoff with a stated
cost. All four judges found that the demo 09 POST guard accepts an empty
hostname where demo 07's guard for the same concern does not (no egress path was
shown, since `urllib` rejects that form). Single-judge findings, each from the
backend reviewer: demo 06's
approval queue derives its id from a file count, so archiving one file can make
the next proposal overwrite a pending approval (`harness.py:74-77`); and demo 10's
audit read path guards `json.loads` in one function and not another. The frontend
and UX reviewer found the renderer silently drops rationale cards when the model's
markdown does not match its regex, and that demo 02's hidden-content check is a
substring heuristic the README presents as its signature control.

**Next step.** Keep the per-demo copies, and add one repository-level check that
they are still identical where they are meant to be (the product and agentic
reviewer's suggestion).

### Reliability, testing, and observability — 2.75

**Strengths.** Recovery and state inspection, the reliability surface that matters
for a stateful stage prop, are designed and were verified.

**Limitations.** There is no automated test of any kind in the tree, which you
state yourselves and the evidence package confirmed (`ev-demos-10`). This is
scored as a verified absence, not as missing evidence. Two judges, the frontend
and UX reviewer and the product and agentic reviewer, noted the most brittle pieces are pure functions that would be easy to test, and that
the event had to write its own probe to check the localhost guard your README
promises.

**Next step.** All four judges proposed a version of the same thing: one
model-free check, stdlib only, that runs every `--dry-run`, every reset and every
inspection script and asserts exit code plus a marker string. It would have
caught the offline-invocation gap, and it is the cheapest item in this dossier.

### Security, privacy, and responsible AI — 3.75

**Strengths.** Guards exercised against hostile input and deny-by-default; a clean
data scan; the safety rail separated from the taught control in `fetch_beacons.py`
so the demo cannot accidentally teach that the lesson is what keeps the room
safe.

**Limitations.** Two judges, the frontend and UX reviewer and the security
reviewer, found `Bash(rm:*)` pre-approved in seventeen command files across all
ten demos, broader than the fixed deletes those commands perform. The security
reviewer and the product and agentic reviewer both found demo 09's docstring and
README describe the tool sandbox as enforced from outside with "no write
capability", while the code is an in-process permission change and socket patch;
the file does disclose its stand-in nature later. The remaining items are each
one judge's:

- The security reviewer: demo 07's "no data ever leaves the machine" does not
  cover the `--open` browser path its own command uses, which the README concedes
  at `:54`.
- The security reviewer: demo 06's reset line uses `rm -rf` over six relative
  names with no check of the working directory, where every other demo uses
  `rm -f` on named files or a reset script.
- The backend reviewer: the Claude Code path deliberately hijacks an agent holding
  `Write` and `Bash(python3:*)` on the presenter's own machine, and no README
  tells the presenter to isolate that session.

**Next step.** Scope the `rm` grants to the exact commands each file runs, as
demo 05's reset already avoids them, and add a short "how to run this safely"
section for the Claude Code path.

### Innovation and technical ambition — 4.00

**Strengths.** Ten attack classes bound to one scenario and cast, with each demo
refusing to re-teach the previous one; the fix located at a boundary and proven
by construction; demo 09's version bump whose extraction code is unchanged so
nobody notices; demo 02's render-and-diff reveal.

**Limitations.** None of the attack classes is new, and you do not claim they
are. The frontend and UX reviewer and the product and agentic reviewer found the
running-cast claim partial: "Sift" appears in all ten demos, "Marisol" in seven
(`ev-demos-12`); the security reviewer counted the same and considered the claim
held.

**Next step.** Each judge suggested a way to make your best ideas checkable
rather than only printable: a schema and validator for demo 10's decision records,
generalizing its trust-tier check across the series, committing a rendered
`REVEAL.html`, and stating each demo's diff budget in its README.

## Tournament journey

The bracket had two teams and no byes, so your journey was one match: the final.

**Final — you won.** `atj matchup` resolved the result from two order-balanced
passes, one presenting you first and one presenting you second, judged by
evaluators who were run independently, as the event records, and did not compute
the margin.
Both passes picked AI Security Demos. Every criterion was order-consistent, and
the result was well outside the close-call band, so it confirmed with no
adjudication and no tie-break. Initial panel scores were not used to pick a
winner.

Both passes favoured you on `product`, `engineering` and `security`, and on
`functional`. On `agentic` one pass favoured you and the other had the teams
level. `reliability` and `innovation` were level in both.

Be clear-eyed about why. The largest difference was that your opponent's
documented start-up path did not reach a working application in this event's
sandbox, while your kit was read and partly executed without a comparable
blocker. On `functional`, both passes said your advantage rested more on that
failure than on your own demonstrated success, because your headline workflow was
never observed. The win reflects a kit that works offline and is well documented,
not a measured result of your demos under attack.

## Blocking issues

None. No judge recorded a blocking defect, a rule violation, or any behaviour
aimed at the panel. The embedded instructions in your payloads, including the
demo 01 resume that tells a screener to award a perfect score, were read as data
and followed by no one.

One earlier finding was withdrawn during the audit and you should not act on it.
Two judges first recorded that no `.env.example` exists in the tree; ten do, one
per demo. The judging tools hide `.env*` paths, which caused the error. Neither
judge's score depended on it.

## Recommended improvement plan

1. **Immediate repair.** Add the offline invocation (`python3 <script>
   --dry-run`) to every README beside the `uv` line, and make each error string
   name both run paths. Together these are one short pass over the READMEs and
   three scripts.
2. **Highest-value next iteration.** Ship a model-free check that doubles as your
   test suite: every dry run, reset and inspection script, asserting exit code
   and one marker string, plus unit tests on the localhost guards. In the same
   pass, make demo 06's gate structural on the Claude Code path and narrow the
   `rm` grants.
3. **Longer-term opportunity.** Make the demos provable without a key. The
   frontend and UX reviewer suggested committing golden transcripts of the
   vulnerable and hardened outputs, and a transcript of demo 06's approval queue
   from proposal to human decline, which needs no model. That would let any
   future evaluator see the flip you built the corpus to show.

## Evidence appendix

Paths resolve against your checkout at commit
`dc35f6962130af5e5be3fe16672e3d4964850eb9`. Run records live in
`events/trial-2-2026/runs/`.

| Evidence | What it shows | Run record |
|---|---|---|
| `ev-demos-01` | No network route and no provider SDK in the sandbox; no model call possible | `team-demos-envcheck-01.json` |
| `ev-demos-02` | Ten demos, 53 Python files, no dependency manifest, all module-scope imports stdlib or sibling | static scan |
| `ev-demos-03` | Vulnerable dry run exits 0 offline and prints the full prompt | `team-demos-01-dryrun-vulnerable-01.json` |
| `ev-demos-05` | Hardened variant: untrusted-data declaration plus `<applicant>` fencing | `team-demos-01-dryrun-hardened-01.json` |
| `ev-demos-06` | Act 2 needs a write into a read-only pin, so it could not run | none |
| `ev-demos-07` | Nine URL forms against the egress guards; every non-local form refused | `team-demos-egress-guards-01.json` |
| `ev-demos-08` | Every network call site read; none unexpected | static read |
| `ev-demos-09` | 201 resumes, no address at a resolvable domain | static scan |
| `ev-demos-10` | No test files anywhere in the tree | static scan |
| `ev-demos-11` | `list_verdicts.py` exit 1 with an actionable message; `memory_diff.py` clean seed | `team-demos-10-list-verdicts-01.json`, `team-demos-04-memory-diff-01.json` |
| `ev-demos-12` | "Sift" in ten demos, "Marisol" in seven | static scan |
| Adjudication | `functional` accepted as `NE` by the event director | `adjudications/adj-trial-2-2026-team-demos-functional.md` |
