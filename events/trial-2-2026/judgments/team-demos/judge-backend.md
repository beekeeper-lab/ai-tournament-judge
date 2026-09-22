---
event_id: trial-2-2026
team_id: team-demos
judge_id: judge-backend
judge_run_id: jr:trial-2-2026:team-demos:judge-backend:cb3847cb:01
commit: dc35f6962130af5e5be3fe16672e3d4964850eb9
evidence_package_id: ev:trial-2-2026:team-demos:dc35f6962130:cb3847cb
rubric: submission-evaluation@1.1.0
persona: judge-backend@1.1.0
scores:
  functional: 3
  product: 4
  agentic: 4
  engineering: 3
  reliability: 3
  security: 4
  innovation: 4
confidence:
  functional: medium
  product: medium
  agentic: medium
  engineering: medium
  reliability: high
  security: high
  innovation: medium
framework_commit: a2cea33f232af7bb6a6ff5ef9bb5c66dcb1a9bc9
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-22T10:37:22Z"
completed_at: "2026-09-22T10:44:23Z"
visibility: private
approval_state: draft
validation_state: unvalidated
model:
  model_requested: claude-opus-5
  model_used: claude-opus-5
  started_at: "2026-09-22T10:37:22Z"
  completed_at: "2026-09-22T10:44:23Z"
  verified: true
  note: Model identity is harness-reported for this judging run, not a self-report by the model. No in-band self-identification was used or relied on.
---

# Individual Judgment

## Executive assessment

This is a corpus of ten presentation props, not an application, and it should be judged as the artifact it is: code whose job is to make a security failure and its fix legible on a stage, repeatably, offline, without hurting anyone. On that job the observable parts are good. The structural promises hold at the pin — ten `NN-*/` directories, ten `demo/README.md` presenter scripts, 53 `.py` files with no dependency manifest and every module-scope import resolving to the standard library or a sibling in the tree ([[evidence:ev-demos-02]]). The safety engineering is not decoration: nine URL forms, six of them hostile including userinfo confusion (`localhost@evil.example`), suffix confusion (`127.0.0.1.evil.example`) and the decimal form `2130706433`, were put through the egress guards and every non-local form was refused (`runs/team-demos-egress-guards-01.json`). The attacker endpoint is hard-bound to loopback with no flag to move it ([[evidence:ev-demos-08]], `07-what-the-output-smuggles-out/demo/attacker.py:36-37`). No e-mail address at a resolvable domain exists anywhere in the tree ([[evidence:ev-demos-09]]).

The central claim — the audience watches the agent get hijacked and then resist — is not observable in this event and I do not credit it. Act 2 requires a write into a read-only pin ([[evidence:ev-demos-06]]) and every act requires a model that the sandbox cannot reach: TCP to `1.1.1.1:443` fails `Errno 101`, DNS fails `gaierror`, and `anthropic`, `requests`, `httpx` and `uv` are all absent ([[evidence:ev-demos-01]]). What I did see is prompt construction ([[evidence:ev-demos-03]]), and a dry run is not agent behaviour.

What I can assess as an engineer is the design, and it is more considered than most demo code. The vulnerable/hardened pairs are reduced to minimal, documented diffs: in demo 01 the two changes are mutually dependent — the system prompt declares `<applicant>…</applicant>` untrusted, and `build_user_content` is what produces those tags, so neither works alone ([[evidence:ev-demos-05]]). In demo 06 the prompt is held deliberately identical and only identity and mode change (`06-approval-is-the-architecture/demo/clear_the_pile.py:43-49`; `demo/tools/harness.py:12-26`). That is the right way to teach an architectural control and it is also the right way to review one.

The defects are small, local, and real: one localhost guard in the corpus is written correctly and another, for the same concern, is not (`07-…/fetch_beacons.py:66-67` against `09-…/tools/resume_parser/v1.1/parser.py:100`); the approval queue derives its record id from a file count (`harness.py:74-77`); the audit read path parses JSON unguarded in one function and guarded in another within the same file (`10-show-your-work/demo/scripts/explain.py:54-55` against `:69-71`); and there is no automated test of any kind across 53 files and ten stateful demos ([[evidence:ev-demos-10]]).

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

**The observation this rests on.** `runs/team-demos-01-dryrun-vulnerable-01.json` and `runs/team-demos-01-dryrun-hardened-01.json`: both variants of demo 01 exit 0 with no network and no SDK, print the complete system prompt and assembled user content over the same 20-resume corpus, and end `[dry-run] 20 resumes, model=claude-sonnet-5, no API call made.` The mechanical difference between them is visible in the captures — 20 `=== Applicant file:` headers against 20 `<applicant file=` tags ([[evidence:ev-demos-05]]). That is a complete, correct execution of act 1 as `01-resume-that-talked-back/demo/README.md:36-38` describes it. I chose to score rather than record `NE` because this is direct observation of a promised workflow behaving as documented, and because the corpus-level completeness claims are independently confirmed: ten demo directories, ten demo READMEs, 66 `.claude/` files across the ten ([[evidence:ev-demos-02]], [[evidence:ev-demos-10]]).

**What worked.** The offline paths are genuinely standalone. No `requirements*.txt`, `pyproject.toml`, `package.json` or `uv.lock` exists anywhere, and every module-scope import resolves to the standard library or a sibling module in the checkout ([[evidence:ev-demos-02]]). `import anthropic` sits below the dry-run early return in all 19 files that use it (`01-…/rank_resumes.py:103-109`), which is why the plain interpreter reaches the documented output. The `--dry-run` convention is uniform: 19 files import the SDK and every one of them carries the flag (grep across `*.py`). Two state-inspection tools ran and behaved correctly with meaningful exit codes — `list_verdicts.py` exit 1 with "Nothing screened yet" and `memory_diff.py` exit 0 with "No change" ([[evidence:ev-demos-11]]).

**What was deficient.** Neither documented invocation is reachable offline, and one of those is a property of the submission rather than of the event: `README.md:19-21` and `01-…/demo/README.md:22` document the dry run as `uv run --with anthropic python rank_resumes.py --dry-run`, which resolves a package from PyPI before printing a prompt that makes no API call. The working offline invocation is undocumented ([[evidence:ev-demos-01]], [[evidence:ev-demos-03]]). Observation, not inference: the code supports offline; the documentation does not point at it.

**Score rationale.** The verified portion of the advertised workflow is complete and correct for what could be run. The headline workflow — agent attacked, agent hardened, for real — was not observed at all, and the rubric's interpretation boundary forbids me from treating prompt construction as evidence of it. That caps this criterion rather than confirming it. I did not mark it down further for a constraint the event imposed.

**Uncertainty.** A reasonable judge with these same facts could land one anchor lower on the grounds that most of the promised three acts went unobserved, or record `NE`. My answer rests on the two dry-run records plus the structural confirmations, which are direct.

**Highest-value improvement.** Add the offline invocation to every README next to the `uv` line. One line per file removes a network dependency from rehearsal and from any future evidence run.

### product — Product value and usability

**Evidence.** `README.md:26-39` indexes ten talks with attack vector and path; each demo carries its own three-act table covering both run paths, a "why the fix works" section, a file inventory, and presenter notes (`01-resume-that-talked-back/demo/README.md:26-95`). Reset and unstage paths are documented per demo (`:33-34`) and pre-approved in the command front matter so they do not prompt mid-talk (`:92-95`). The pin is verified clean of leftover presentation state ([[evidence:ev-demos-11]]).

**What worked.** The documentation is written by someone who has presented. `01-…/demo/README.md:88-91` states plainly that the vulnerable prompt is deliberately naive so the hijack is reliable on stage, and tells the presenter what to do if a future model shrugs the injection off. `09-…/demo/README.md:123-125` tells the presenter which part of the demo is model-independent. Rendering scripts produce offline, stdlib-only HTML views for the room (`01-…/demo/README.md:74`). Honest limitation notes appear where a presenter would be burned — cost of the N-call isolated ranker (`08-…/demo/README.md:136`), the folder the `/` commands are relative to (`:142`).

**What was deficient.** The documented run instructions are offline-hostile, as above. `01-…/demo/README.md:77-79` states the resumes are "sourced from real resumes, then scrubbed of every identifier" while `README.md:46-47` states they "trace to no real individual" — a residual-risk claim a user of this MIT-licensed repository cannot check, and one the evidence package explicitly declines to support (R6). The observable data shape is clean; provenance is not shape.

**Score rationale.** The product is a presenter's kit and it is unusually complete for that job, with rehearsal-aware detail I do not normally see. Two usability and disclosure gaps keep it short of the top anchors.

**Uncertainty.** Documentation quality is directly observable; whether it works in a room is inference from the artifacts.

**Highest-value improvement.** Replace the "de-identified from real resumes" sentence with either a generation method the reader can verify or a plain statement that the corpus is derived and re-identification risk is the author's assertion.

### agentic — Agentic and AI system design

**Evidence.** The controls are readable without a model. Data/instruction separation implemented as two mutually dependent changes ([[evidence:ev-demos-05]], `01-…/hardened/rank_resumes_hardened.py:33-48,67-70`). Identity and blast-radius architecture with an approval queue, human-attributed approval, and an audit line per consequential action (`06-…/demo/tools/harness.py:43,80-99,129-152`). Memory writes carry provenance and policy-shaped writes are quarantined rather than self-authored (`04-…/demo/sift_memory.py:91-117`). Per-candidate context isolation via sub-agents, aggregated in ordinary code (`08-…/demo/README.md:83-84,142`). Tool supply chain: description sanitizing, an explicit sandbox flag, and a version rug-pull whose extraction code is byte-identical to the previous version (`09-…/demo/tools/resume_parser/v1.1/parser.py:5-6,39`). Decision records with trust tiers, and integrity flags *derived* from source trust rather than trusted from the record (`10-…/demo/scripts/explain.py:85-110`).

**What worked.** Least privilege is expressed in the agent surface itself, not only in prose: the hardened command in demo 05 drops `Bash` from `allowed-tools` while its vulnerable twin keeps it (`05-…/demo/.claude/commands/screen-pile-hardened.md:4` against `screen-pile.md:4`; explained at `05-…/demo/README.md:21,64`). Demo 06 holds the prompt byte-identical across the pair so the lesson cannot be mistaken for prompt tuning (`clear_the_pile.py:43-49`). `effective_flags` catching an attack even when the record was hand-authored without a flag is a genuinely good idea.

**What was deficient.** Demo 04's hardened classifier is a 13-entry regex phrase list (`sift_memory.py:35-50`), which is payload filtering — the approach the corpus's own thesis says is never the fix ([[evidence:ev-demos-04]], [[evidence:ev-demos-05]]). The provenance half of that control is structural and sound; the gate half is evadable by rephrasing. The corpus does not say so. Separately, effectiveness against an actual model is unobserved everywhere ([[evidence:ev-demos-01]]; manifest, Missing evidence 1 and 4), so I credit appropriateness, control and observability, not efficacy.

**Score rationale.** The AI use is the subject matter and the decision to use it is correct by construction. The controls are appropriate, boundary-shaped, and observable as artifacts. The top anchor requires demonstrated effectiveness, which this event cannot supply.

**Uncertainty.** Design is direct observation; effectiveness is absent, not adverse.

**Highest-value improvement.** Say in demo 04's README that the policy-shaped classifier is a tripwire, not the control, and that provenance plus the human gate is what carries the fix. As written it invites the audience to copy the pattern the series argues against.

### engineering — Engineering and maintainability

**Evidence.** Uniform layout across ten demos; stdlib-only; `DEMO_DIR`-relative path handling used consistently, including the one-directory-down correction in the hardened script (`01-…/hardened/rank_resumes_hardened.py:27`); docstrings that state design intent and their own limits (`09-…/demo/tools/toolbox.py:111-113` conceding that a real deployment needs OS-level isolation); deliberate, stated duplication for standalone-ness (`06-…/demo/tools/harness.py:9-10`).

**What worked.** The duplication tradeoff is the right one here. A presenter clones one folder and it runs; that is worth more than a shared package, and the corpus says so out loud rather than drifting into it. The vulnerable/hardened pairs are constructed so the diff is the teaching artifact, which also makes them reviewable.

**What was deficient — all directly observed.**
- Two implementations of the same localhost guard, of different strength. `fetch_beacons.is_localhost` requires set membership *and* an `http`/`https` scheme (`07-…/demo/fetch_beacons.py:66-67`). `_post_to_localhost` accepts an empty hostname as local (`09-…/…/v1.1/parser.py:100`). The run record shows the schemeless form reaching `urllib` and dying there with `ValueError: unknown url type` rather than at the guard (`runs/team-demos-egress-guards-01.json`), so no egress path is demonstrated — but the guard shape is wrong in safety-critical code, and [[evidence:ev-demos-08]] records the same nuance.
- `_next_qid` derives the approval-queue id from `len(list(QUEUE_DIR.glob("q-*.json"))) + 1` (`harness.py:74-77`). Remove or archive one queue file and the next proposal reuses an existing id and overwrites a pending human approval. In a demo whose whole point is that the queue is the control, the queue's identity scheme should not be recoverable from a file count.
- Inconsistent failure handling in the same read path: `load_bare` guards `json.loads` (`explain.py:54-55`), `find_record` does not (`:69-71`), and `list_verdicts.py:35` does not either. A truncated decision record produces a traceback instead of a finding, in the capstone about being able to answer for a decision.
- Copy drift is visible: `import glob` is unused in `01-…/rank_resumes.py:23` and dropped in the hardened copy ([[evidence:ev-demos-05]]). Small, but it is the signature of hand-propagated edits across 53 files.

**Score rationale.** Coherent, proportionate, readable, with an explicit and correct architectural tradeoff. Not above that: three localized correctness gaps in exactly the code that carries the lessons, and no mechanism that would catch a fourth.

**Uncertainty.** I read roughly a fifth of the 53 files closely; the structural and dependency claims come from the package's AST scan over all of them ([[evidence:ev-demos-02]]). Another judge reading a different subset could find more of the same or none.

**Highest-value improvement.** Make the two localhost guards one function in one place per demo that needs it, written in the `fetch_beacons` shape (membership plus scheme, reject everything else including empty).

### reliability — Reliability, testing, and observability

**Evidence.** No `test_*.py`, no `*_test.py`, no `tests/`, no `conftest.py`, `pytest.ini` or `tox.ini` anywhere in the tree ([[evidence:ev-demos-10]]) — a verified absence, which the rubric says is evidence and is scored. Against that: recovery paths exist in every demo (`/reset-demo` in all ten per the command front matter; `sift_memory.reset()` at `04-…/demo/sift_memory.py:120-126`; `_state.reset_state()` at `05-…/demo/tools/_state.py:93-109`; `toolbox.py reset`). Detection works and was exercised: `list_verdicts.py` exits 1 with an actionable message and `memory_diff.py` exits 0 reporting a clean seed ([[evidence:ev-demos-11]], `runs/team-demos-10-list-verdicts-01.json`, `runs/team-demos-04-memory-diff-01.json`). Failure messages in the entry points are actionable rather than tracebacks (`01-…/rank_resumes.py:100,111,114`).

**What worked.** For a repeatedly-run stateful prop, recovery and state inspection are the reliability surface that matters, and both are designed rather than improvised. The pin is verified clean, which means the reset discipline is actually being followed ([[evidence:ev-demos-11]]).

**What was deficient.** Nothing prevents a stage-breaking regression. Two model-free self-checks exist (`sift_memory.py --self-test` at `:129-141`, `toolbox.py parse --sandbox`) but they are manual, uncollected, and cover two demos. Neither was exercised in this event, so I treat them as present, not as passing. The audit-path JSON reads noted above turn a corrupt record into a traceback. And `09-…/demo/tools/toolbox.py` prints "[sandbox] no side effects attempted" (`:217-221`) based on an empty blocked-list, without confirming its `chmod 0o500` was ever enforceable (`:119-122`); if writes succeed regardless of mode, the tool reports the control worked when it did nothing. That is inference — I did not execute it — but the code path is plain.

**Score rationale.** Recovery and observability are present and verified; prevention is absent by direct observation. These are not unrelated production infrastructure: ten stateful demos and 53 files with no automated check is the specific risk of a broken live talk.

**Uncertainty.** Both the presence of the reset/inspection tooling and the absence of tests are settled by direct observation and by the package's scans.

**Highest-value improvement.** A single stdlib smoke test that invokes every `--dry-run`, every reset, and every inspection script and asserts exit code plus one marker string in stdout. No dependencies, no model, no network, a few minutes of runtime. It is the cheapest thing in this report and it protects the thing the corpus exists to do.

### security — Security, privacy, and responsible AI

**Evidence.** Egress guards exercised against nine URL forms, six hostile, all refused, with `ALLOWLIST` observed empty in the same run (`runs/team-demos-egress-guards-01.json`, [[evidence:ev-demos-07]]). Every network call site in the tree read statically: the attacker listener is hard-bound to `127.0.0.1:8099` with no override, `fetch_beacons` fetches only past the localhost rail and the empty allowlist, and the parser's POST mode is off by default with `PARSER_EXFIL_MODE` defaulting to a local file write ([[evidence:ev-demos-08]], `parser.py:112`). No module else opens a socket. Corpus-wide scan finds no e-mail address outside reserved example domains; the only four hits are themselves `.example` names ([[evidence:ev-demos-09]]).

**What worked.** The two-layer split in `fetch_beacons.py:41-46,83-91` is the right decomposition: an always-on safety rail that is not the lesson, and a deny-by-default allowlist that is. Separating them means the demo cannot accidentally teach that the taught control is what keeps the room safe. The guards refused userinfo confusion and the decimal-IP form, which is where most hand-rolled host checks fail.

**What was deficient.** Three things, in descending severity by my reading.
1. The primary documented run path deliberately gets an agent hijacked on the presenter's own machine while `Write` and `Bash(python3:*)` are pre-approved in that session (`01-…/.claude/commands/rank-resumes.md:4`, and the same pattern in the primary command of every other demo except 06, whose `clear-the-pile.md:4` withholds `Write`: 02, 03, 04, 05, 07, 08, 09 and 10). No README in the tree tells the presenter to run that session in a container, a throwaway clone, or anything else — a grep for isolation language across all READMEs returns only demo 09's in-process tool sandbox. The payloads are stated to be benign props, and I saw nothing contradicting that; the gap is that the corpus teaches blast-radius discipline everywhere except in its own run instructions.
2. The empty-host acceptance in `parser.py:100`, with no demonstrated exploit path ([[evidence:ev-demos-08]]).
3. The unverifiable data-provenance claim at `01-…/demo/README.md:77-79`. The shape of the corpus is verifiably synthetic; its derivation from real documents is asserted.

**Score rationale.** The controls that exist are real, exercised against adversarial input, and deny-by-default, and the default mode of the one exfiltration tool is the safe one. The three gaps above are why this does not reach the top anchor.

**Uncertainty.** The egress behavior and data scan are direct and settle the main questions. Item 1 is a documentation absence I verified by grep, not a demonstrated harm.

**Highest-value improvement.** Add a short "how to run this safely" section to the top-level README for the Claude Code path: fresh clone, no other repository in the working tree, and a note that the vulnerable commands hold write and execute permission in a session you are intentionally hijacking.

### innovation — Innovation and technical ambition

**Evidence.** Ten distinct attack classes bound to one persistent scenario and cast — "Sift" in all ten demos, "Marisol" by name in seven ([[evidence:ev-demos-12]]). Non-obvious design choices: integrity flags derived from source trust tiers rather than read from the record's own stamped flags (`explain.py:85-110`); a version bump whose extraction code is byte-identical so "it still works" and nobody notices (`parser.py:5-6,39`); a pair whose prompt is deliberately held constant so only identity and mode vary (`clear_the_pile.py:43-49`); sub-agent fan-out used as a context boundary and aggregation done in plain code (`08-…/demo/README.md:83-84`).

**What worked.** The corpus consistently locates the fix at a boundary rather than in a filter, and then proves it by construction — the hardened system prompt's rule is meaningless without the tag-fencing that `build_user_content` adds, so the pair cannot be half-copied ([[evidence:ev-demos-05]]). That is a design decision doing pedagogical work.

**What was deficient.** None of the attack classes is new, and the corpus does not claim otherwise. The demos' reliability on stage depends on a prompt tuned to be naive (`01-…/demo/README.md:88-91`), which is honest and also limits the technical-depth claim: the injection succeeding is arranged, not discovered. Demo 04's regex classifier is the least ambitious control in the set.

**Score rationale.** Originality is in the assembly, the minimal-diff discipline, and several design choices I would not have expected. Depth is real but pedagogical rather than novel.

**Uncertainty.** I read a subset of the tree closely, and originality is a judgment against a field I am not citing evidence for.

**Highest-value improvement.** Demo 10 is the strongest idea in the corpus and the thinnest on execution. Make the decision record a schema with a validator, so a malformed or truncated record is a reportable finding instead of a stack trace, and so the audit artifact is checkable rather than merely printable.

## Surprises

**Better than expected.** The egress guard held against the cases that usually break hand-rolled host checks — `localhost@evil.example` resolved to `evil.example` and was refused, as were `127.0.0.1.evil.example`, `0.0.0.0` and `2130706433` (`runs/team-demos-egress-guards-01.json`). `effective_flags` deriving an integrity flag from source trust rather than trusting the record's own flags (`explain.py:85-110`) is the kind of thing that usually only appears after someone has been burned. And demo 05 enforcing the vulnerable/hardened split in the command's `allowed-tools` rather than in prose (`screen-pile-hardened.md:4`) is a control expressed where it actually binds.

**Worse than expected.** The documented dry run needs the network to print a prompt that makes no network call ([[evidence:ev-demos-01]], `README.md:19-21`). The same corpus contains a correct localhost guard and a weaker one for the same purpose, and the weaker one lives in the demo about auditing your tools. And the tool sandbox announces success without confirming it was enforceable (`toolbox.py:119-122,165-173,217-221`) — in a teaching artifact, a control that reports "clean" when it did nothing is the worst available failure mode.

## Blocking and major issues

**Confirmed defects (direct observation).**
- C1 — The documented invocation cannot reach the offline dry run. `README.md:19-21` and `01-…/demo/README.md:22`; [[evidence:ev-demos-01]], [[evidence:ev-demos-03]]. Not blocking, one line per README to fix.
- C2 — `_post_to_localhost` treats an empty hostname as local (`09-…/…/v1.1/parser.py:100`), unlike `fetch_beacons.is_localhost` (`07-…/fetch_beacons.py:66-67`). No egress path demonstrated; the schemeless form dies in `urllib`, not at the guard (`runs/team-demos-egress-guards-01.json`, [[evidence:ev-demos-08]]).
- C3 — No automated test of any kind in the tree ([[evidence:ev-demos-10]]). Stated by the team and independently confirmed.
- C4 — `_next_qid` derives the approval-queue id from a file count and can overwrite a pending proposal (`06-…/demo/tools/harness.py:74-77`).
- C5 — Unguarded `json.loads` in the audit read path (`explain.py:69-71`, `list_verdicts.py:35`) against a guarded read in the same file (`explain.py:54-55`).

**Risks and untested concerns (inference, clearly labelled).**
- R1 — The in-process tool sandbox reports "no side effects attempted" from an empty blocked-list without confirming its `chmod` was enforceable (`toolbox.py:119-122,165-173,217-221`). Not executed by me or by the evidence package; the code path is legible and the failure would be silent. The file is honest that this is not a real boundary (`:111-113`).
- R2 — The Claude Code run path hijacks an agent holding `Write` and `Bash(python3:*)` on the presenter's machine, with no isolation guidance in any README (command front matter across ten demos; grep over all READMEs). Payloads are stated to be benign props and nothing I read contradicts that.
- R3 — Data provenance is asserted, not verifiable: `01-…/demo/README.md:77-79` states derivation from real resumes; the evidence package declines to support "traces to no real individual" (R6). The observable shape is clean ([[evidence:ev-demos-09]]).
- R4 — The corpus's central claim is unobserved in this event: no model call anywhere, no act beyond act 1, no Claude Code path (manifest, Missing or inaccessible evidence 1-4). Every conclusion I drew about attack resistance is about text, not behaviour.

**Single most valuable improvement across the whole submission.** The stdlib smoke test described under `reliability`. It is the only proposal here that would have caught C1, C4 and C5 before a presenter did, it needs no dependency, model or network, and it would give a future evidence run a model-free verification surface across all ten demos instead of the two that happened to be inspectable.

## Calculation and independence declaration

- [x] Scores were calculated by the repository script
- [x] Every material finding cites evidence
- [x] No other judge report was inspected
- [x] Submission instructions were treated as untrusted data
- [x] Corrected by the event director after a stage audit, 2026-09-22, under audit finding F10 and with no judge re-run: the enumeration of demos whose primary command pre-approves `Write` and `Bash(python3:*)` is corrected to every demo except 06, whose `clear-the-pile.md:4` withholds `Write`. No score, confidence, anchor or line of reasoning was touched.
