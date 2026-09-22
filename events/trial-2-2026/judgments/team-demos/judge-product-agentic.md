---
event_id: trial-2-2026
team_id: team-demos
judge_id: judge-product-agentic
judge_run_id: jr:trial-2-2026:team-demos:judge-product-agentic:cb3847cb:01
commit: dc35f6962130af5e5be3fe16672e3d4964850eb9
evidence_package_id: ev:trial-2-2026:team-demos:dc35f6962130:cb3847cb
rubric: submission-evaluation@1.1.0
persona: judge-product-agentic@1.1.0
scores:
  functional: 3
  product: 4
  agentic: 4
  engineering: 3
  reliability: 2
  security: 4
  innovation: 4
confidence:
  functional: medium
  product: medium
  agentic: medium
  engineering: high
  reliability: high
  security: high
  innovation: medium
framework_commit: a2cea33f232af7bb6a6ff5ef9bb5c66dcb1a9bc9
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-22T10:37:22Z"
completed_at: "2026-09-22T10:43:36Z"
visibility: private
approval_state: draft
validation_state: unvalidated
model:
  model_requested: claude-opus-5
  model_used: claude-opus-5
  started_at: "2026-09-22T10:37:22Z"
  completed_at: "2026-09-22T10:43:36Z"
  verified: true
  note: >-
    Model identity is harness-reported by the runtime that invoked this judge, not a
    self-report by the model. No separate attestation source was available.
---

# Individual Judgment

## Executive assessment

The product is a presenter's kit, not an application, and it is built with unusual
care for that user. Ten talks each ship a three-act script, a vulnerable script, a
minimally different hardened script, staging and reset commands, and a rendered
artifact to put on a screen (`README.md:23-39`; `01-resume-that-talked-back/demo/README.md:26-34`;
[[evidence:ev-demos-02]]). The decision about where AI belongs is the best thing in
the submission and it is verifiable offline: the model drives screening, and every
tool a presenter depends on mid-talk — reconstruction, state diff, verdict listing,
the action harness, the audit renderer — is deliberately model-free and stdlib-only,
which is why two of them ran correctly inside an offline sandbox
([[evidence:ev-demos-02]], [[evidence:ev-demos-11]], `runs/team-demos-04-memory-diff-01.json`,
`runs/team-demos-10-list-verdicts-01.json`).

The central claim — an agent gets attacked and the hardening stops it — was not
observed in this event, and the manifest is explicit that this is a property of the
event, not a deficiency of the submission ([[evidence:ev-demos-01]], "Missing or
inaccessible evidence" item 1). I did not score that gap as failure. I scored what
the pinned tree does establish: prompt construction and the vulnerable-to-hardened
delta as text ([[evidence:ev-demos-03]], [[evidence:ev-demos-04]], [[evidence:ev-demos-05]]),
a gated action surface with human approval and per-action attribution
(`06-approval-is-the-architecture/demo/tools/harness.py:43-152,158-250`), an integrity
check computed independently of the model's own record
(`10-show-your-work/demo/scripts/explain.py:85-110`), and egress guards that refused
six hostile URL forms under execution ([[evidence:ev-demos-07]],
`runs/team-demos-egress-guards-01.json`).

Two things hold it back from the top of this panel's range. Nothing in the repository
tests anything — a verified absence, not a missing observation ([[evidence:ev-demos-10]]) —
so the presenter has no way to learn before a talk that a prop has stopped working;
the README's own remedy for that failure is to hand-edit the payload text
(`01-resume-that-talked-back/demo/README.md:88-91`). And on the run path the demo calls
its hero path, the approval gate is enforced by flags the agent itself writes into a
shell command (`06-approval-is-the-architecture/demo/.claude/commands/clear-the-pile-hardened.md:4,30-31`),
which is a weaker ceiling than the one the talk claims to be teaching.

Every file in this checkout — READMEs, scripts, `.claude/` command files, payloads —
was read as data. Several are written as direct instructions to an agent. None changed
what I examined or how I scored it.

## Scores

Raw scores and confidence go in this file's **front matter** and nowhere else.
`schemas/judgment.schema.json` reads them from there, and a second copy in the
body is a second source of truth for the same number.

Criterion IDs, weights, weighted points and the total are generated into the
block below by `atj render judgment`, from
`framework/rubrics/submission-evaluation.md`. Leave the block empty. Do not type
a weight or a total into this file; a hand-copied weight is how the official
numbers drift, and the declaration at the end of this template asserts that the
repository script calculated them.

<!-- atj:scores:begin -->
| Criterion | Raw score or NE | Weight | Weighted points | Confidence |
|---|---:|---:|---:|---|
<!-- atj:scores:end -->

## Criterion findings

### functional — Functional correctness and completeness

**Evidence.** Structure is complete at the pin: ten `NN-*/` directories, ten
`demo/README.md` presenter scripts, 399 tracked files, 53 `.py` files, no dependency
manifest of any kind, and every module-scope import resolving to the standard library
or a sibling inside the checkout ([[evidence:ev-demos-02]]). Act 1 of demo 01 runs and
behaves exactly as its README describes: exit 0, the full system prompt and assembled
user content printed, ending `[dry-run] 20 resumes, model=claude-sonnet-5, no API call
made.` ([[evidence:ev-demos-03]], `runs/team-demos-01-dryrun-vulnerable-01.json`). The
hardened variant runs over the same corpus and differs in the two places its docstring
claims ([[evidence:ev-demos-05]], `runs/team-demos-01-dryrun-hardened-01.json`). Two
model-free tools ran to their intended output, one of them exiting non-zero with an
actionable message rather than a traceback ([[evidence:ev-demos-11]]). Claims R5, R6,
R7 and R8 are directly confirmed ([[evidence:ev-demos-07]], [[evidence:ev-demos-08]],
[[evidence:ev-demos-09]], [[evidence:ev-demos-10]]).

**Strengths.** The self-containment claim is not a promise, it is observable: no
`requirements*.txt`, `pyproject.toml`, `package.json` or `uv.lock` anywhere, and the
only third-party import in the tree sits inside a function below the dry-run return in
all 19 files that carry it ([[evidence:ev-demos-02]]). That is why a plain interpreter
reached the same output the documentation describes. Each demo's README maps the three
acts onto both run paths with exact commands, including the pull-back-out and reset
rows (`01-resume-that-talked-back/demo/README.md:28-34`;
`06-approval-is-the-architecture/demo/README.md:32-40`;
`10-show-your-work/demo/README.md:38-45`).

**Deficiencies.** Neither documented run path is reachable in this event
([[evidence:ev-demos-01]]), and one part of that is the submission's own: the dry run
is documented only as `uv run --with anthropic python rank_resumes.py --dry-run`
(`01-resume-that-talked-back/demo/README.md:20-22`), which resolves a package from PyPI
before printing anything, even though the script needs neither the package nor the
network to produce that output ([[evidence:ev-demos-02]], [[evidence:ev-demos-03]]). A
presenter without network has no documented way to run the advertised "no API call"
path. Acts 2 and 3 were not executed because staging requires a write into a read-only
pinned checkout ([[evidence:ev-demos-06]]), and the cast claim is looser than stated:
"Sift" appears in all ten demos, "Marisol" by name in seven ([[evidence:ev-demos-12]]).

**Score rationale.** For everything observable, the submission does what it says: the
structure, the self-containment, the act-1 behaviour, the safety posture, and the two
independent counts all match the claims. The score stops short of the anchor above it
because the central workflow — the attack landing and the hardening stopping it — has
no supporting observation here, so there is no convincing evidence of exceeding
expectations. It does not fall to the anchor below because nothing observed contradicts
a claim and the inability to observe is the event's, not the submission's.

**Uncertainty.** Medium. My score rests on the observation that act 1 reproduces its
documented behaviour and the structure is complete ([[evidence:ev-demos-02]],
[[evidence:ev-demos-03]]). If acts 2 and 3 had been staged and had failed, this score
would be materially lower; nothing in this package tells me either way, and the manifest
warns explicitly against reading a dry run as agent behaviour ("Missing or inaccessible
evidence" item 4).

**Highest-value improvement.** Document the model-free invocation. `python3 <script>
--dry-run` works offline today ([[evidence:ev-demos-03]]) and no README says so; adding
that row to the two-ways-to-run table makes the advertised "prints the exact prompt with
no API call" path true without network.

### product — Product value and usability

**Evidence.** The user is a presenter and the artifact is shaped to that user's real
failure mode. Each demo's README carries staged beats with what to show and what to say
(`01-resume-that-talked-back/demo/README.md:36-48`), an explanation of why the fix works
written for a live diff (`:50-62`), and a file table that tells the presenter what every
path on screen is (`:64-81`). Demo 06 ships a deck-aligned 2x2 reference
(`06-approval-is-the-architecture/demo/README.md:78,94`). Demo 10 ships a full offline
fallback so the reconstruction beats can be rehearsed with no key and no subscription:
`python3 scripts/explain.py quill-avara --from examples` (`10-show-your-work/demo/README.md:32-34`).
The state of the checkout at the pin is clean — no leftover output from a previous
presentation is committed, verified by the demos' own tools ([[evidence:ev-demos-11]]).
Stage safety is real: 201 resume files with `example.com` addresses and `(555)` numbers,
and a scan of every text file returns four e-mail addresses, all four at `.example`
names ([[evidence:ev-demos-09]]).

**Strengths.** Three product decisions stand out. First, the reset and unstage paths are
first-class in every demo, so the prop survives being run twice in a row and a presenter
can recover mid-talk (`01-resume-that-talked-back/demo/README.md:33-34`;
`10-show-your-work/demo/README.md:44-45`). Second, the hardened variants are kept
minimally different on purpose so the fix can be diffed live and read in seconds — the
demo-01 delta is two substantive changes plus a path fix and three cosmetic ones
([[evidence:ev-demos-05]]). Third, the corpus is designed to make the ranking genuinely
interesting rather than a toy: a mixed pile where a few candidates are strong fits and
the rest are not, visible in the captured prompt (`runs/team-demos-01-dryrun-vulnerable-01.json`,
20 applicant files spanning frontend, data, DevOps, QA and UX).

**Deficiencies.** The offline story exists only for demo 10; the other nine have no
documented path that works without network ([[evidence:ev-demos-01]];
`01-resume-that-talked-back/demo/README.md:20-22`). The demo's payoff depends on a model
misbehaving on cue, and the documented mitigation when it does not is manual payload
editing right before a talk (`01-resume-that-talked-back/demo/README.md:88-91`;
`06-approval-is-the-architecture/demo/README.md:111-114`;
`10-show-your-work/demo/README.md:108-111`). The running-cast promise is uneven —
"Marisol" is absent from three demos ([[evidence:ev-demos-12]]) — which is small, but the
cast is the thread the series sells.

**Score rationale.** The problem is real and specific, the solution is understandable
and directly usable by its stated user, and the supporting detail — reset paths, safe
data, rendered artifacts, a "do not fix this prompt, it would hide the lesson" note at
`06-approval-is-the-architecture/demo/README.md:111-114` — goes well past what a demo
corpus normally carries. It does not reach the top anchor because the product's most
fragile moment, the live attack, has neither an offline fallback outside demo 10 nor any
way to check it in advance.

**Uncertainty.** Medium. My score rests on direct reading of the ten presenter scripts
and on the three executed runs that confirm the checkout's clean, ready-to-present state
([[evidence:ev-demos-02]], [[evidence:ev-demos-11]]). No demo was ever presented under
observation, so usability on stage is inference from artifacts, and a reasonable judge
could land one anchor lower on that basis.

**Highest-value improvement.** This is the improvement with the greatest user impact in
the whole submission. Ship a per-demo pre-flight check that runs with no key and no
network and asserts the acts' model-free invariants: that staging places the payload
where the README says, that `--mode gate` queues instead of firing, that `explain.py`
raises the integrity flag on an untrusted deciding rule. Every piece needed already
exists (`tools/act.py`, `scripts/explain.py`, `scripts/memory_diff.py`); none of it
asserts. A presenter could then know in ten seconds, in the green room, whether the prop
still works.

### agentic — Agentic and AI system design

**Evidence.** Where AI is used and where it is not is a deliberate, verifiable line. The
model screens; the tools that carry the talk do not. `explain.py` never calls the model
and is stated as such so the reconstruction beats stay deterministic on stage
(`10-show-your-work/demo/README.md:112-113`), and the AST scan confirms the tooling has
no third-party or model dependency at module scope ([[evidence:ev-demos-02]]). Two of
those tools executed correctly with no network and no SDK present
([[evidence:ev-demos-11]], `runs/team-demos-04-memory-diff-01.json`,
`runs/team-demos-10-list-verdicts-01.json`).

The action surface is narrow and controlled. `harness.py` exposes exactly three
consequential tools, each writing a local file and one audit line carrying an actor
field (`06-approval-is-the-architecture/demo/tools/harness.py:56-63,158-250`). In gate
mode each becomes a JSON proposal in `approval-queue/` with an id, a proposer and a
pending status (`:80-99`), and the only path from proposal to effect is a human
approving it, with the resulting action re-attributed to that human (`:129-152`). The CLI
front door fails closed: `--actor` defaults to `sift-agent` and `--mode` to `gate`
(`tools/act.py:26,106-107`). In the Python path the identity and mode are module
constants out of the model's reach (`hardened/clear_the_pile_hardened.py:42-43`, applied
at `:108-115`), against `Marisol`/`fire` in the vulnerable script
(`clear_the_pile.py:44-45`).

The observability design is the strongest single element. `effective_flags` recomputes
integrity flags from each source's trust tier rather than trusting the flags the model
wrote, so an untrusted or unreviewed deciding rule is caught even when the record is
sloppy or dishonest (`10-show-your-work/demo/scripts/explain.py:85-110`). That is a
verification loop that does not depend on the component being verified.

**Strengths.** Restraint. The corpus could have used a model for the reconstruction,
the diffing and the rendering; it uses plain Python for all three, and that choice is
what made a meaningful part of this submission judgeable at all in an offline sandbox.
The prompt being byte-identical between vulnerable and hardened in demo 06
(`06-approval-is-the-architecture/demo/README.md:12-13,66-67`) is a well-controlled
demonstration: it isolates architecture from prompt engineering so the audience cannot
attribute the fix to better wording.

**Deficiencies.** On the Claude Code path the demo calls "the hero path"
(`06-approval-is-the-architecture/demo/README.md:22`), the ceiling is made of arguments
the agent itself writes. The command file instructs the agent to emit `python3
tools/act.py ... --actor sift-agent --mode gate` under `allowed-tools: Read, Glob,
Bash(python3:*)` (`.claude/commands/clear-the-pile-hardened.md:4,30-31`). The safe
default protects against a forgotten flag, not against an agent that has been persuaded
to pass `--mode fire --actor Marisol` — and persuading the agent is precisely the threat
the series demonstrates. Nothing above the agent constrains those flags. Separately,
`GATED_ACTIONS` at `harness.py:43` names the gated set but is referenced nowhere in the
tree; the gate is re-implemented inside each tool function, so a tool added later
without its own `mode == "gate"` branch would fire ungated.

**Score rationale.** The criterion asks whether the AI decision is correct and whether
the AI use is appropriate, controlled, observable and effective. Three of those four are
settled by direct evidence: the decision is right and is verified by the model-free
tooling executing offline; the tool surface is small, named, gated, attributed and
auditable; the observability is designed not to trust the model. Effectiveness under
attack is unobserved ([[evidence:ev-demos-01]], "Missing or inaccessible evidence" items
1-3). That, plus the Claude Code gate being inside the agent's argument list, is what
keeps it off the top anchor. This is not `NE`: the design questions have answers in the
pinned tree, and a verified absence of the effectiveness observation is a limit on my
confidence, not a hole where the subject should be.

**Uncertainty.** Medium. The manifest records this criterion as evidence-limited, and my
score rests on static design reading plus two model-free executions, not on any observed
agent behaviour. The claim at `06-approval-is-the-architecture/demo/README.md:118-122`
that the three-act flow was validated by driving `tools/act.py` directly is a team claim
with no artifact in this package, and I did not credit it.

**Highest-value improvement.** Move the ceiling outside the agent's reach on the Claude
Code path. Have `act.py` read identity and mode from a config file or environment the
agent cannot write, or split the entry points so the firing variant is simply not in
`allowed-tools`, and make `GATED_ACTIONS` the thing the code consults rather than a
comment in constant form. The talk's thesis is that you architect the ceiling; the hero
path should not be the one place the ceiling is a string the model typed.

### engineering — Engineering and maintainability

**Evidence.** The implementation is proportionate to what it is. No build system, no
dependency file, stdlib only, 53 Python files in a repeating per-demo shape
([[evidence:ev-demos-02]]). The vulnerable/hardened pair is the same pattern in every
talk, and the demo-01 delta is deliberately small: two substantive changes plus a
necessary path fix (`DEMO_DIR` becoming `Path(__file__).resolve().parent.parent` so the
hardened script one directory down reads the same corpus) and three cosmetic renames
([[evidence:ev-demos-05]]). `harness.py` and `act.py` are clean, documented and small
(`06-approval-is-the-architecture/demo/tools/harness.py`,
`06-approval-is-the-architecture/demo/tools/act.py`). `toolbox.py` is candid about its
own limits: the in-process sandbox docstring says a real deployment would need OS-level
sandboxing and calls itself a legible stand-in
(`09-toolbox-you-didnt-audit/demo/tools/toolbox.py:111-113`).

**Strengths.** The code is written to be read on a projector, and that is the right
optimization for this product. Comments explain the lesson rather than the syntax
(`harness.py:12-27,41-51`). Error paths in the model-free tools produce presenter-legible
messages rather than stack traces (`runs/team-demos-10-list-verdicts-01.json`, exit 1
with "Nothing screened yet. Run /screen-pile or /screen-pile-audited first.").

**Deficiencies.** Self-containment is bought with duplication and nothing detects drift.
`render_ranking.py` exists in all ten demos as separate copies
(`01-.../demo/scripts/render_ranking.py` through `10-.../demo/scripts/render_ranking.py`),
the 20-resume corpus is duplicated per demo for 201 resume files total
([[evidence:ev-demos-09]]), and talk 06's harness is a stated copy of talk 05's
(`06-approval-is-the-architecture/demo/tools/harness.py:9-10`). A fix to the renderer or
the corpus is a ten-place edit with no test anywhere to catch a missed one
([[evidence:ev-demos-10]]). `GATED_ACTIONS` at `harness.py:43` is dead. Demo 06's README
also lists `scripts/render_ranking.py` as "not used by this demo's default flow, kept for
consistency" (`:93`), which is honest but is carried weight.

**Score rationale.** Coherent, proportionate and readable, with the duplication a
defensible consequence of a product requirement — each folder must run standalone on a
presenter's laptop. Solid meets the bar. It does not exceed it, because ten copies with
zero automated checks is a maintenance posture that works only while one person holds
the whole corpus in their head.

**Uncertainty.** High confidence. The structure, the import surface, the file counts and
the hardened-versus-vulnerable delta are all direct observations ([[evidence:ev-demos-02]],
[[evidence:ev-demos-05]], [[evidence:ev-demos-10]]), and the duplication and the dead
constant are directly citable in the checkout.

**Highest-value improvement.** Keep the per-demo copies — they serve the user — but add
one repository-level check that the copies are byte-identical where they are meant to be.
A twenty-line script comparing the ten `render_ranking.py` files and the shared corpus
would turn silent drift into a visible failure without touching the standalone property.

### reliability — Reliability, testing, and observability

**Evidence.** The repository has no automated test of any kind: no `test_*.py`, no
`*_test.py`, no `tests/`, no `conftest.py`, `pytest.ini` or `tox.ini` anywhere in the
tree ([[evidence:ev-demos-10]]). That is a verified absence, and I scored it rather than
recording it as a missing observation. What does exist for failure handling is
presenter-facing: reset and unstage rows in each demo's act table
(`01-resume-that-talked-back/demo/README.md:33-34`;
`10-show-your-work/demo/README.md:44-45`), generated output gitignored so a re-run starts
clean (`01-resume-that-talked-back/demo/README.md:75`), an append-only audit line per
consequential action (`06-approval-is-the-architecture/demo/tools/harness.py:56-63`), and
two state-verification tools that both reported a clean baseline when run
([[evidence:ev-demos-11]]). The egress guards behaved correctly under nine inputs
(`runs/team-demos-egress-guards-01.json`).

**Strengths.** The detection story that does exist is well-made. `effective_flags`
(`10-show-your-work/demo/scripts/explain.py:85-110`) catches a decision whose deciding
rule came from an untrusted or unreviewed source even when the record itself carries no
flag, which is the right shape for after-the-fact detection. `memory_diff.py` gives the
presenter a one-command answer to "is the working memory clean?" and answered it
correctly offline (`runs/team-demos-04-memory-diff-01.json`).

**Deficiencies.** The claims this corpus makes about its own safety are exactly the
claims a two-line test would defend, and the repository does not make them. The event had
to write the egress-guard probe itself to establish that `is_localhost` refuses
`localhost@evil.example` and `127.0.0.1.evil.example` ([[evidence:ev-demos-07]]) — that
test belongs in the repository, because the README states the guarantee
(`README.md:50-52`). Worse for the product: there is no pre-flight check at all, so the
failure mode that matters most — a model that no longer takes the bait — is undetectable
until it happens in front of an audience, and the documented remedy is to hand-strengthen
the payload text (`01-resume-that-talked-back/demo/README.md:88-91`;
`10-show-your-work/demo/README.md:108-111`). The READMEs are honest about this risk,
which is to their credit, but honesty about an undetected failure is not detection.

**Score rationale.** Useful elements are present and some of them ran correctly under
observation, so this is not at the failure anchors. It sits below solid because the one
thing a live-demo product most needs — a way to know before the talk that the demo still
works — does not exist, and because a corpus whose selling point is "the fix is real" has
nothing that checks the fix is still real. I am not penalizing an appropriate prototype
for missing production infrastructure; I am scoring the absence of the specific checks
this submission's own claims call for.

**Uncertainty.** High confidence. The absence of tests is directly verified
([[evidence:ev-demos-10]]) and the recovery and state tooling I credit was executed
([[evidence:ev-demos-11]]).

**Highest-value improvement.** The same pre-flight check named under `product`, made to
double as the test suite: assert the model-free invariants of each act. It closes the
reliability gap and the maintainability gap at once.

### security — Security, privacy, and responsible AI

**Evidence.** The egress claim at `README.md:50-52` was tested against nine URL forms,
six of them hostile, and held: `fetch_beacons.is_localhost` admits `127.0.0.1`,
`localhost` and `[::1]` and refuses `evil.example`, the userinfo form
`localhost@evil.example`, the suffix form `127.0.0.1.evil.example`, `0.0.0.0`, the
decimal `2130706433` and `file:///etc/passwd`; `ALLOWLIST` is empty, so the second layer
is deny-by-default; `resume_parser/v1.1._post_to_localhost` raises rather than posting for
the hostile forms ([[evidence:ev-demos-07]], `runs/team-demos-egress-guards-01.json`).
Every network call site in the tree was read statically: the attacker listener binds
`127.0.0.1` hard-coded with no flag to change it, and the malicious parser's POST mode is
off by default ([[evidence:ev-demos-08]]). The action harness writes only local files and
"sends" mail into `outbox/` (`06-approval-is-the-architecture/demo/tools/harness.py:167-250`;
`06-approval-is-the-architecture/demo/README.md:100-105`). Sample data is synthetic with
no address at a resolvable domain anywhere in the corpus ([[evidence:ev-demos-09]]).

**Strengths.** The guards are controls, not comments, and they cover the confusion forms
a careless implementation misses — userinfo, suffix and decimal-IP — which is more than
the stated claim required. The hardened screener's fix is a data/instruction boundary
rather than a payload filter: untrusted material is fenced as `<applicant file="…">` and
the system prompt declares that fence untrusted and requires attempted injections to be
scored as absent and noted ([[evidence:ev-demos-05]],
`runs/team-demos-01-dryrun-hardened-01.json`). That is the correct defense to teach, and
the corpus teaches it by construction rather than by assertion.

**Deficiencies.** Demo 09's containment is in-process monkeypatching of `socket.socket`
plus a `chmod` on the exfil directory
(`09-toolbox-you-didnt-audit/demo/tools/toolbox.py:101-138`). The docstring says plainly
that a real deployment needs OS-level isolation (`:111-113`), which is the right
disclosure, but the demo is teaching containment and a presenter's audience may not hear
the caveat. The description sanitizer is a fixed denylist regex
(`toolbox.py:47-51`); the README frames it correctly as one of four layers and says
sanitizing alone is not enough against the code channel
(`09-toolbox-you-didnt-audit/demo/README.md:68-79`), but it does not say the denylist
itself is trivially bypassable, which sits awkwardly against a series thesis that the
payload is never the vulnerability. The v1.1 guard also admits an empty hostname, which
`urllib` then rejects — narrower than its sibling guard, with no observable consequence
([[evidence:ev-demos-08]]).

**Score rationale.** Strong. The safety posture is not merely asserted; it was exercised
against hostile input and held, and the data handling is clean under a whole-tree scan.
It stops short of the top anchor because one demo's containment mechanism is a stand-in
that the demo relies on to make its point, and one guard is narrower than the guard beside
it without the corpus noting the difference.

**Uncertainty.** High confidence. Every claim above is either an executed run or a
whole-tree scan recorded in the package ([[evidence:ev-demos-07]], [[evidence:ev-demos-08]],
[[evidence:ev-demos-09]]).

**Highest-value improvement.** Make demo 09's sandbox caveat part of the stage script, not
just the docstring — one line in the README's "why the fix works" saying an in-process
patch is a teaching stand-in and naming what a real boundary is. The audience for this
talk is people who will go build the thing they just watched.

### innovation — Innovation and technical ambition

**Evidence.** Three elements carry real depth. Deriving integrity flags from source trust
tiers independently of what the model recorded
(`10-show-your-work/demo/scripts/explain.py:85-110`) answers the hard problem in agent
auditability: the trace is written by the thing being audited. Holding the prompt
byte-identical across the vulnerable and hardened runs of demo 06 and changing only
identity and mode (`06-approval-is-the-architecture/demo/README.md:12-13,66-74`;
`clear_the_pile.py:44-45` against `hardened/clear_the_pile_hardened.py:42-43`) is a
controlled experiment rather than a demonstration — it removes prompt engineering as a
confound. Demo 09 splits a supply-chain compromise into two channels, description and
code, and shows each control is separately necessary
(`09-toolbox-you-didnt-audit/demo/README.md:68-79`). Across the ten talks, each isolates
exactly one new mechanism on one running cast and one thesis ([[evidence:ev-demos-12]];
`README.md:26-39`).

**Strengths.** The ambition is curricular rather than decorative. Nothing here adds an
agent, a model or a framework for effect; the depth is in what each demo controls for.

**Deficiencies.** The attack classes are well known, the payloads are deliberately
unsubtle by the submission's own statement, and none of the defenses are new to the
field. The originality is in packaging and pedagogy. The manifest is right that measuring
evasiveness would be measuring something never claimed ("Missing or inaccessible
evidence" item 6), and I did not.

**Score rationale.** Strong. The independently derived trace check and the controlled
identical-prompt design are more than a competent assembly of known material. Not
exceptional, because the technical content is a synthesis of established practice and
because the ambition's payoff — the demos landing live — was never observed.

**Uncertainty.** Medium. I read the design artifacts directly, but an originality judgment
compares against a field I am not citing evidence for, and the model-dependent half of the
corpus was never seen working ([[evidence:ev-demos-01]]).

**Highest-value improvement.** Generalize the `effective_flags` idea out of demo 10. A
trust-tier-derived check that runs across every demo's output would turn the capstone's
best idea into the series' spine rather than its last chapter.

## Surprises

**Better than expected.**

- The guards refused the confusion forms, not just the obvious ones. `localhost@evil.example`,
  `127.0.0.1.evil.example` and the decimal `2130706433` are the three a naive
  implementation lets through, and all three were refused under execution
  ([[evidence:ev-demos-07]]).
- A submission built entirely around model calls turned out to be substantially judgeable
  with no model at all, because the decision to keep reconstruction, diffing, rendering
  and the action harness model-free was made for stage determinism
  (`10-show-your-work/demo/README.md:112-113`) and happened to survive contact with an
  offline sandbox ([[evidence:ev-demos-11]]).
- `explain.py` does not trust the record it is explaining
  (`10-show-your-work/demo/scripts/explain.py:85-110`). That is a design instinct I did
  not expect in a demo corpus.

**Worse than expected.**

- The path advertised as "no API call" needs the network
  (`01-resume-that-talked-back/demo/README.md:20-22`; [[evidence:ev-demos-01]],
  [[evidence:ev-demos-02]]), and the offline invocation that does work is undocumented.
- Zero tests ([[evidence:ev-demos-10]]) in a corpus whose whole pitch is that the failure
  and the fix are real rather than on a slide (`README.md:3-6`).
- The approval gate on the hero path is a flag the agent writes into its own shell command
  (`06-approval-is-the-architecture/demo/.claude/commands/clear-the-pile-hardened.md:4,30-31`),
  in a talk whose thesis is that you cannot prompt your way out of excessive agency.
- `GATED_ACTIONS` (`06-approval-is-the-architecture/demo/tools/harness.py:43`) is defined
  and used nowhere in the tree.

## Blocking and major issues

**Blocking.** None. No observation in this package contradicts a claim the submission
makes.

**Confirmed defects.**

1. The documented dry-run path requires network resolution of a PyPI package before
   printing, though the script needs neither the package nor the network
   ([[evidence:ev-demos-01]], [[evidence:ev-demos-02]], [[evidence:ev-demos-03]];
   `01-resume-that-talked-back/demo/README.md:20-22`).
2. No automated test of any kind exists in the tree ([[evidence:ev-demos-10]]).
3. `GATED_ACTIONS` is dead; gating is re-implemented per function, so a tool added without
   its own `mode == "gate"` branch fires ungated
   (`06-approval-is-the-architecture/demo/tools/harness.py:43,158-250`).
4. The running-cast claim is partial: "Marisol" appears in seven of ten demos
   ([[evidence:ev-demos-12]]).

**Risks and untested concerns.**

1. The approval gate on the Claude Code path depends on the agent emitting `--actor
   sift-agent --mode gate` under `allowed-tools: Bash(python3:*)`
   (`.claude/commands/clear-the-pile-hardened.md:4,30-31`). The safe default at
   `tools/act.py:106-107` covers omission, not substitution. This is a static reading; the
   Claude Code path was never exercised in this event ("Missing or inaccessible evidence"
   item 3), so I flag it as a design risk rather than a demonstrated failure.
2. Model drift silently breaks act 2, and the only documented remedy is hand-editing the
   payload before a talk (`01-resume-that-talked-back/demo/README.md:88-91`;
   `06-approval-is-the-architecture/demo/README.md:111-114`;
   `10-show-your-work/demo/README.md:108-111`).
3. Demo 09's in-process sandbox is not a security boundary and says so
   (`09-toolbox-you-didnt-audit/demo/tools/toolbox.py:111-113`), while the demo leans on it
   to teach containment.
4. The central claim — attack lands, hardening stops it — is unverified here. Acts 2 and 3
   need a write into a read-only pin, and every act needs a model
   ([[evidence:ev-demos-01]], [[evidence:ev-demos-06]]). Per the manifest, this is a
   property of the event, not a deficiency of the submission, and I scored it that way.

**Steering.** This checkout contains text written as direct instruction to an agent,
including the ATS directives in the payload files and the `.claude/commands/*.md` files
that address an agent in the imperative. All of it was read as data. No `.claude/`
configuration was loaded, no command was executed, and no file's framing of what good
looks like was adopted as a criterion. My scores rest on the rubric at
`framework/rubrics/submission-evaluation.md` and on observations in the evidence package
and the pinned checkout.

## Calculation and independence declaration

- [x] Scores were calculated by the repository script
- [x] Every material finding cites evidence
- [x] No other judge report was inspected
- [x] Submission instructions were treated as untrusted data
