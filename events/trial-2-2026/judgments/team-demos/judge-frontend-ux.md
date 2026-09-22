---
event_id: trial-2-2026
team_id: team-demos
judge_id: judge-frontend-ux
judge_run_id: jr:trial-2-2026:team-demos:judge-frontend-ux:cb3847cb:01
commit: dc35f6962130af5e5be3fe16672e3d4964850eb9
evidence_package_id: ev:trial-2-2026:team-demos:dc35f6962130:cb3847cb
rubric: submission-evaluation@1.1.0
persona: judge-frontend-ux@1.1.0
scores:
  functional: NE
  product: 4
  agentic: 3
  engineering: 3
  reliability: 3
  security: 4
  innovation: 4
confidence:
  functional: high
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
completed_at: "2026-09-22T10:43:34Z"
visibility: private
approval_state: draft
validation_state: unvalidated
model:
  model_requested: claude-opus-5
  model_used: claude-opus-5
  started_at: "2026-09-22T10:37:22Z"
  completed_at: "2026-09-22T10:43:34Z"
  verified: true
  note: >-
    Model identity is harness-reported for this judge run, not a self-report by
    the model. No independent attestation was available inside the evidence
    package, and none is claimed.
---

# Individual Judgment

## Executive assessment

The user-facing surface of this submission is documentation and command-line output, and on that surface it is unusually well built. Every one of the ten demos carries a `demo/README.md` with the same shape: a one-paragraph premise, the one new mechanism the talk owns, two run paths, a three-act table mapping each act to both paths, a "why the fix works" section naming the exact controls, a files table, presenter notes, and a safety section. The three-act section is present in all ten (grep for `^## The three acts` across `*/demo/README.md`, ten matches). That consistency is the product. A presenter who has never opened this repository can read one demo README and run the room from it.

The demonstration behavior those READMEs promise was not observable in this event. No model call was made anywhere, the sandbox has no route off the host and no provider SDK (`ev-demos-01`, `runs/team-demos-envcheck-01.json`), and acts 2 and 3 need a write into a read-only pinned checkout (`ev-demos-06`). I do not treat the observed dry runs as evidence of agent behavior under attack, and I have not scored anything on the assumption that the attacks land. `functional` is `NE` for that reason and for no other, and the manifest is explicit that this is a property of the event rather than a deficiency of the submission.

Where I can see the surface directly, I found one confirmed break and a cluster of smaller ones. Eleven READMEs instruct the operator to run `cp .env.example .env` as the first step of run path B, and no `.env.example` file exists anywhere in the pinned tree. This is not a `.gitignore` artifact: `.gitignore:2-3` ignores `.env` and `**/.env`, neither of which matches `.env.example`. The failure is recoverable, because the scripts read the key from the environment and say so on failure (`01-resume-that-talked-back/demo/rank_resumes.py:112-114`), but the first documented command of the documented setup path cannot succeed at this commit. Alongside it, the CLI error and empty-state strings that a path-B user will hit name path-A slash commands they do not have.

Set against those, the state handling is better than a demo corpus usually manages. The checkout is verifiably clean and ships tools that say so: `list_verdicts.py` exits non-zero with "Nothing screened yet. Run /screen-pile or /screen-pile-audited first." and `memory_diff.py` reports "No change. Working memory matches the clean seed." (`runs/team-demos-10-list-verdicts-01.json`, `runs/team-demos-04-memory-diff-01.json`). Empty state, reset paths, and a checkable baseline are exactly what a repeat-performance artifact needs, and they are here and executed.

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

**Evidence.** The promised primary workflow is stated in `README.md:3-6`: each demo "shows an AI agent behaving usefully, then getting attacked, then being hardened, so the audience watches the failure and the fix happen for real." That workflow is the three acts, and every act requires a model call. `ev-demos-01` and `runs/team-demos-envcheck-01.json` establish that no model was reachable: TCP to `1.1.1.1:443` fails with `OSError [Errno 101]`, DNS for `api.anthropic.com` fails with `gaierror [Errno -3]`, and `anthropic`, `requests`, `httpx` and `uv` are all absent. `ev-demos-06` establishes that act 2 requires `cp goofy-goof.md resumes/` (`01-resume-that-talked-back/demo/README.md:31`), a write into a read-only pin. `ev-demos-11` confirms nothing was staged. The manifest records `functional` in `evidence_limited_criteria` and states plainly that behavior under attack is `NE`.

**Strengths.** What could be exercised without a model behaved as documented. Both dry runs exited 0 and printed the complete system prompt plus assembled user content, ending `[dry-run] 20 resumes, model=claude-sonnet-5, no API call made.` (`runs/team-demos-01-dryrun-vulnerable-01.json`, `runs/team-demos-01-dryrun-hardened-01.json`). The two verification tools ran and produced sensible output on a clean tree.

**Deficiencies.** One confirmed defect in the documented workflow: `cp .env.example .env` appears in all eleven READMEs (top level plus ten demos, 11 matches for `env\.example`) and no such file exists in the tree. A second, recorded by the manifest rather than found by me: the documented dry-run invocation is `uv run --with anthropic python <script> --dry-run`, which resolves a package from PyPI before printing anything, even though `import anthropic` sits below the dry-run return (`ev-demos-02`, `01-resume-that-talked-back/demo/rank_resumes.py:103-109`). The keyless affordance is documented in its most network-dependent form.

**Score rationale.** The observation my answer rests on is `ev-demos-01`: no model call was made anywhere, so none of the three acts in any of the ten demos was observed. The evidence needed to answer the central question is missing rather than the subject being absent, which is what `NE` is for. The two defects above are real and I report them, but neither settles whether the three acts accomplish what they promise, and I decline to convert an unobservable workflow into a low number. Marking this `NE` blocks an official total, which is the correct consequence here.

**Uncertainty.** None about the inability itself. The package records the limitation, and the run records show the mechanism. What a staged, model-backed run would produce is entirely unknown to me.

**Highest-value improvement.** Make one act reproducible without a model. A committed golden transcript of the vulnerable and hardened outputs over a staged pile, checked in under `examples/` the way demo 10 already does for decision records (`10-show-your-work/demo/README.md:32-34`), would let an evaluator, or a presenter with no connectivity, see the flip without a key.

### product — Product value and usability

**Evidence.** Top-level `README.md:26-39` is a ten-row talk index with attack vector and link per talk. Each demo README follows one template: premise, blockquote naming the single new mechanism, "Two ways to run it", a three-act table with a column per run path, prose for each act, "Why the fix works" enumerating the controls, a files table, notes, safety. Verified present in all ten by the `^## The three acts` grep. Examples read in full: `01-resume-that-talked-back/demo/README.md`, `02-invisible-ink/demo/README.md`, `06-approval-is-the-architecture/demo/README.md`, `07-what-the-output-smuggles-out/demo/README.md`, `10-show-your-work/demo/README.md`. Each table includes stage, unstage and reset rows, so the demo is repeatable between sessions (`01/demo/README.md:33-34`). Presenter risk is addressed directly rather than hidden (`01/demo/README.md:88-91`, `06/demo/README.md:111-114`). The rendered artifact declares `lang="en"`, ships a viewport meta, honors `prefers-color-scheme: dark` with a separately chosen dark accent tint, and uses a semantic `thead`/`th` table (`01-resume-that-talked-back/demo/scripts/render_ranking.py:141-157, 178-193, 221-226`). Score is carried by both a colored bar and an adjacent numeral, so it is not color-only (`:111-119`).

**Strengths.** The information architecture is the strongest thing here. One thesis is stated once at the top (`README.md:53-54`) and re-instantiated in each demo's own words, and each demo explicitly refuses to re-teach the previous one (`02/demo/README.md:8-13`, `07/demo/README.md:9-12`, `10/demo/README.md:64-67`). The "hero path" annotations tell a presenter which of the two paths to use for that specific beat (`02/demo/README.md:20-21`, `06/demo/README.md:22`). Files tables name the one artifact that flips per demo (`07/demo/README.md:95`), which is the thing the audience should be watching. Empty state is real and actionable, verified in execution (`runs/team-demos-10-list-verdicts-01.json`).

**Deficiencies.** Four, all on the operator's path. First, `.env.example` is referenced eleven times and ships zero times, so the documented setup step fails. Second, error and empty-state strings name only Claude Code commands even when the user is on the Python path: `render_ranking.py:240` says "run /rank-resumes first", `07/demo/scripts/render_assessment.py:169-170` says "run /assess-candidate first", and `10/demo/scripts/list_verdicts.py:20,40` names `/screen-pile` and `/explain` although the same README gives the path-B equivalent at `10/demo/README.md:40`. Third, the top-level README has no troubleshooting section, no stated minimum Python version, and no degraded-mode guidance (`README.md:12-24`), while the only documented keyless rehearsal path sits inside one demo's README (`10/demo/README.md:32-34`) where a presenter with a dead venue network will not find it. Fourth, the running-cast promise is looser than stated: "Marisol" appears by name in seven of ten demos (`ev-demos-12`), so the continuity the top README sells at `README.md:8-9` is partial.

**Score rationale.** The documentation and operator surface clearly exceeds what this event normally sees, and the claim is supported by direct observation across all ten demos rather than by a sample. It does not reach the top anchor because the first command of a documented run path cannot succeed at this commit, and because the error strings actively misdirect users of the other path. The visual artifact was assessed from its generator only, not from rendered output, since `reports/` is gitignored and the tree is clean (`.gitignore:5-7`, `ev-demos-11`), so no contrast measurement or assistive-technology pass was possible. I have not credited or penalized rendered visual quality.

**Uncertainty.** Medium. The evidence settles the documentation surface. It does not settle the live-audience experience, which is the product's actual delivery context and was never observed.

**Highest-value improvement.** Ship `.env.example` and make every error string name both paths, for example "run `/rank-resumes` (Claude Code) or `python3 rank_resumes.py` (Python)". Both are small edits and together they repair the whole first-run path.

### agentic — Agentic and AI system design

**Evidence.** The decision to use a model is inherent to the subject: a demonstration of an LLM agent being hijacked cannot be built without an LLM agent, and `README.md:3-6` states that as the purpose. Controls observed as artifacts: the hardened variant's two-part fix, captured verbatim in execution, declares everything inside `<applicant>…</applicant>` untrusted data and fences each resume accordingly, so neither half works without the other (`ev-demos-05`, `runs/team-demos-01-dryrun-hardened-01.json`, `01-resume-that-talked-back/demo/hardened/rank_resumes_hardened.py:33-48,67-70`). Every model-calling script carries a dry-run branch that prints the full prompt before any spend and returns before the SDK import (`ev-demos-02`, `rank_resumes.py:103-106`). Demo 06 documents a least-privilege agent identity and a fail-closed CLI default of `--actor sift-agent --mode gate` (`06/demo/README.md:69-74, 88`). Demo 10's reconstruction tool never calls the model and derives integrity flags from a source trust tier rather than from the model's own honesty (`10/demo/README.md:70-74, 112-113`).

**Strengths.** The observability design is the part I can actually verify. An operator sees the exact prompt, both system and user content, before spending anything, and the two run records show that this works with no SDK and no network. The human-in-the-loop framing in demo 06 puts the irreversible actions behind a queue a person reviews, and the default for the CLI front door is the safe one rather than the demonstrative one.

**Deficiencies.** Effectiveness is unobserved. No agent ran, so no control was seen to hold under attack (`ev-demos-01`, manifest "Missing or inaccessible evidence" items 1 and 4). Demo 06's approval queue and review flow were never exercised, and demo 10's audited screener has nothing to audit at the pin (`ev-demos-11`). Separately, the shipped agent configuration pre-approves `rm` and `Bash(python3:*)` so the demo does not prompt mid-presentation (`01/demo/.claude/commands/rank-resumes.md:4`, `01/demo/README.md:92-95`, `06/demo/README.md:115-117`), which trades away approval friction on the operator's own machine inside a corpus whose sixth talk teaches approval gates. It is documented and defensible for a stage prop, and it is still the one place where the corpus's own lesson and its packaging point in different directions.

**Score rationale.** I chose to score rather than mark `NE`, and the observation that answer rests on is `ev-demos-05` read together with the two dry-run records: the control design is present as an artifact and one hardened-versus-vulnerable pair was captured verbatim, so "appropriate, controlled, observable" has direct evidence even though "effective" has none. That combination meets primary expectations and cannot reach the anchors above it, which would require a demonstrated system I did not see operate. I have credited no effectiveness whatsoever.

**Uncertainty.** Medium. A reasonable judge holding the same facts could mark this `NE` on the grounds that the criterion's final clause is unobservable. I name that openly rather than presenting my reading as the only one.

**Highest-value improvement.** Record and commit one transcript of the approval-queue flow from demo 06, proposal through human decline, with the audit lines showing `sift-agent` proposed and `Marisol (human)` declined. It is the only control in the corpus whose effect does not depend on a model deciding anything, so it can be made verifiable offline today.

### engineering — Engineering and maintainability

**Evidence.** Structure at the pin: ten `NN-*/` directories, 399 tracked files, 53 `.py` files, no dependency manifest of any kind, and every module-scope import resolving to the standard library or a sibling inside the checkout (`ev-demos-02`). Files read directly: `rank_resumes.py`, `scripts/render_ranking.py` and `.claude/commands/rank-resumes.md` in demo 01, `list_verdicts.py` in demo 10, `reveal.py:1-80` in demo 02, and `scripts/render_assessment.py:9-58,144-170` in demo 07.

**Strengths.** The stdlib-only constraint is a design decision that matches the use case and is stated as such ("Dependency-free (stdlib only) so it works offline during a live talk", `render_ranking.py:2-9`). Module docstrings state intent and the intentional defect rather than hiding it (`rank_resumes.py:2-19`). Self-containment per demo means a presenter copies one folder and it runs. The hardened variants differ from their vulnerable twins by a small, readable delta, and the delta is what the talk teaches (`ev-demos-05`).

**Deficiencies.** Duplication is the cost of self-containment and it is visible: `render_ranking.py` is copied into at least demos 01, 06 and 10, and demo 06 keeps a copy its default flow does not use, "kept for consistency" (`06/demo/README.md:93`, `10/demo/README.md:94`). A fix to the renderer has to be applied in every copy. More consequential, the contract between the agent command file and the renderer is an unversioned regex: the command file dictates an exact markdown shape (`01/demo/.claude/commands/rank-resumes.md:24-39`) and the renderer parses it with `re.match(r"\*\*(\d+)\.\s*(.+?)\*\*\s*\((\d+)/100\)\s*[—–-]+\s*(.+)", ...)` (`render_ranking.py:59-63`). Any deviation in a model-written line silently yields zero rationale cards. In demo 02, `_is_hidden` matches on inline style substrings and a hard-coded set of two class names, `{"ink", "microtext"}` (`reveal.py:35-50, 70`), which is adequate for a fixed prop but is presented in the README as the signature control the hardened ranker shares (`02/demo/README.md:66-70`).

**Score rationale.** Coherent, proportionate to a set of stage props, and readable, which meets primary expectations. It does not exceed them: duplicated renderers, a brittle parse contract between the agent's output format and the artifact generator, and a control implemented as a substring heuristic are all things a maintainer will hit.

**Uncertainty.** Medium. I read a purposeful sample of files, not all 53, and I lean on `ev-demos-02` for the tree-wide import and dependency conclusions.

**Highest-value improvement.** Have the model emit the ranking as JSON and have the renderer consume that, keeping markdown as a rendered output rather than the interchange format. That removes the regex contract, the silent-drop failure, and the need to keep the command file and the renderer in lockstep.

### reliability — Reliability, testing, and observability

**Evidence.** Verified absence: no `test_*.py`, no `*_test.py`, no `tests/`, no `conftest.py`, `pytest.ini` or `tox.ini` anywhere in the tree (`ev-demos-10`, corroborating R7). Executed state checks: `runs/team-demos-10-list-verdicts-01.json` (exit 1, "Nothing screened yet. Run /screen-pile or /screen-pile-audited first.") and `runs/team-demos-04-memory-diff-01.json` (exit 0, "No change. Working memory matches the clean seed."). Error paths read statically: `rank_resumes.py:99-100` (no resumes found, names the directory), `:110-111` (SDK missing, gives the exact command), `:112-114` (key missing, names both `.env` and the environment), `render_ranking.py:239-240`, `render_ranking.py:251-252` (no `xdg-open`, prints the path to open manually), `list_verdicts.py:19-20`.

**Strengths.** Recovery is designed in and verified. Every demo README has stage, unstage and reset rows, generated output is gitignored (`.gitignore:5-7`), and two tools exist that let a presenter confirm the machine is in a clean pre-show state. Both were executed and both reported clean. Error messages generally say what failed and what to do next, including a graceful fallback when the browser cannot be opened automatically.

**Deficiencies.** Zero automated tests, on a tree whose most brittle components are pure functions that would be trivially testable: the ranking parser (`render_ranking.py:29-69`), the hidden-channel extractor (`reveal.py:35-80`), and the localhost guard, which the event had to probe by hand to learn it works (`ev-demos-07`). The renderer fails silently when the model's markdown does not match: unparsed rationales are dropped and the success line reports only the row count, `Rendered {OUT} ({len(rows)} candidates)` (`render_ranking.py:243`), so a presenter gets a table with no explanation cards and no warning. The cross-path error strings described under `product` degrade recovery for exactly the user who is already stuck. Stage-failure risk is handled in prose, not in verification ("If a future model shrugs off the injection anyway, strengthen the directive text", `01/demo/README.md:88-91`).

**Score rationale.** For a corpus whose reliability requirement is a repeatable performance, the evidence of working reset, clean-baseline checking and legible errors is direct and executed, which meets primary expectations. It goes no higher because a control the talk sells has no test at all, and because the one artifact the audience looks at can lose half its content without saying so.

**Uncertainty.** Low. The absence of tests is verified, the empty states were executed, and the error paths are readable in source.

**Highest-value improvement.** Add a handful of stdlib `unittest` cases over the three pure functions, above all `is_localhost` against the hostile URL forms the event had to construct itself (`ev-demos-07`). That converts the corpus's central safety promise from a claim into something the repository checks on every change.

### security — Security, privacy, and responsible AI

**Evidence.** Executed: `ev-demos-07` and `runs/team-demos-egress-guards-01.json` show `fetch_beacons.is_localhost` admitting `127.0.0.1`, `localhost` and `[::1]` and refusing `evil.example`, `localhost@evil.example`, `127.0.0.1.evil.example`, `0.0.0.0`, `2130706433` and `file:///etc/passwd`, with `ALLOWLIST = set()` observed in the same run, and `resume_parser/v1.1._post_to_localhost` raising `RuntimeError: blocked: resume-parser refuses to POST to non-localhost host` for the hostile forms. Static: `ev-demos-08` reads every network call site, with `attacker.py` bound to `127.0.0.1:8099` and no flag to change it, and the v1.1 parser's exfil mode defaulting to a local file. Data: `ev-demos-09` finds no address at a resolvable domain anywhere in the tree, with all four non-`example.com` hits themselves `.example` names. Code read directly: `render_ranking.py:21-26` escapes HTML before applying code and bold transforms, so model-authored rationale text cannot inject markup into the artifact shown on stage; `07/demo/scripts/render_assessment.py:47-58` emits a live `<img>` only in the vulnerable rendering and escaped, inert plain text in the hardened one.

**Strengths.** The README's safety claims (`README.md:41-54`) match observed behavior rather than restating intent, and the guards refuse the exact confusion cases that defeat naive host checks. Safety is placed where a reader will see it before running anything: demo 07 puts "Safety, read this first" above the run instructions (`07/demo/README.md:14-19`). The taught control in demo 07 is implemented as code in the renderer, not asserted in prose. Escaping before markdown transformation is the correct order and is easy to get wrong.

**Deficiencies.** Two guard paths were never exercised: `--enforce-allowlist`, which `ev-demos-07` notes would refuse even a localhost beacon, and the beacon server end to end (manifest "Tests and execution", final row). The v1.1 guard admits an empty hostname, which `urllib` then rejects, so it is narrower than the demo-07 guard without an observable consequence here (`ev-demos-08`). The shipped `.claude/` commands pre-approve `rm` and `Bash(python3:*)` to avoid mid-demo prompts (`01/demo/.claude/commands/rank-resumes.md:4`, `01/demo/README.md:92-95`), a deliberate and documented trade that still narrows the human approval surface in a corpus that teaches approval gates.

**Score rationale.** Claims match executed behavior on the cases that matter, synthetic data is verified across the whole tree, and the rendering surface is safe by construction in the one place model output becomes markup. That clearly exceeds normal expectations with convincing evidence. It stops short of the top anchor because two guard paths remain unexercised and the packaging defaults trade away the approval friction the material itself argues for.

**Uncertainty.** Low. Several of these conclusions come from direct execution against the pinned checkout rather than from reading.

**Highest-value improvement.** Exercise `--enforce-allowlist` in the documented act-3 flow and state in the demo 07 README that the allowlist denies by default even for localhost, so a presenter is not surprised on stage by a guard doing exactly what it should.

### innovation — Innovation and technical ambition

**Evidence.** Ten distinct attack vectors under one cast and one thesis (`README.md:26-39, 53-54`), with each demo explicitly scoping itself to one new mechanism and declining to re-teach the previous one (`02/demo/README.md:8-13`, `07/demo/README.md:9-12`, `10/demo/README.md:64-67`). Demo 02's render-and-diff produces the human view and the model view from one HTML source and highlights every span present for the model and absent for the human, with the same extractor imported by the hardened ranker so the two always agree (`02-invisible-ink/demo/reveal.py:1-18`). Demo 06 keeps the prompt byte-for-byte identical across vulnerable and hardened runs so that only identity and mode change (`06/demo/README.md:9-13, 66-75`). Demo 10 derives integrity flags from a source trust tier computed independently of the model's own honesty (`10/demo/README.md:70-74`). Scale at the pin: 399 tracked files, 53 scripts, 66 agent-configuration files, 201 resume files (`ev-demos-02`, `ev-demos-09`, `ev-demos-10`).

**Strengths.** The originality is in the pedagogy, and it is a real design achievement. Holding the prompt constant to isolate architecture from prompting is a sharp move that most treatments of excessive agency do not make. The two-panel human-versus-model artifact turns an abstraction into something an audience sees in one glance. Building the capstone's detection on source provenance rather than on model self-report is the right instinct, and it is the reason the demo 10 beat survives a model that refuses the injection (`10/demo/README.md:108-111`).

**Deficiencies.** The underlying techniques are known art: indirect injection, allowlists, approval gates, provenance traces. The distinctive contribution is synthesis and packaging, not new technique. And none of the novel mechanisms was observed doing what it claims, so the ambition is evidenced as design rather than as demonstrated depth (`ev-demos-01`, manifest "Missing or inaccessible evidence" item 1). Hidden-channel detection rests on a substring and class-name heuristic (`reveal.py:35-50, 70`), which limits the depth claim for the demo that makes the sharpest one.

**Score rationale.** The curriculum design, the render-and-diff artifact and the constant-prompt experiment are convincing evidence of originality that exceeds normal expectations, all readable directly in the pinned tree. It does not reach the top anchor because the depth is in framing rather than technique and because no mechanism was seen to work.

**Uncertainty.** Medium. The design evidence is direct, the claimed effect is entirely unobserved, and I have not credited the latter.

**Highest-value improvement.** Commit a rendered `REVEAL.html` for the staged attack. It needs no model and no key, it is the corpus's most original artifact, and shipping it would let a reader see the idea without running anything.

## Surprises

**Better than expected.** The first-run and empty states. A demonstration corpus usually assumes the happy path, and this one ships a clean, checkable baseline plus tools that report it: `list_verdicts.py` exits non-zero with a specific next action, and `memory_diff.py` states that working memory matches the clean seed (`runs/team-demos-10-list-verdicts-01.json`, `runs/team-demos-04-memory-diff-01.json`). Also unexpected was `render_ranking.py:21-26` escaping HTML before applying markdown transformations. That is the only point where model-authored text becomes markup in a file a presenter opens in a browser, the order is the one that is safe, and nothing in the READMEs draws attention to it.

**Worse than expected.** The documented setup path's first command cannot succeed. `cp .env.example .env` appears in eleven READMEs, no `.env.example` exists in the tree, and `.gitignore:2-3` ignores only `.env` and `**/.env`, so this is a missing file rather than an ignore artifact. Paired with the manifest's finding that the documented dry-run form resolves a PyPI package before printing anything (`ev-demos-01`, `ev-demos-02`), the run-path documentation is the weakest part of an otherwise exceptional documentation set. The cross-path error strings compound it: a Python-path user who hits a failure is told to run a slash command that exists only in the other path (`render_ranking.py:240`, `render_assessment.py:169-170`, `list_verdicts.py:20,40`).

## Blocking and major issues

**Confirmed defects.**

1. `.env.example` is referenced in all eleven READMEs and absent from the pinned tree. The first step of documented run path B fails. Recoverable, since the scripts accept the key from the environment and the failure message says so (`rank_resumes.py:112-114`), but not from the documentation alone.
2. Error and empty-state strings name only Claude Code commands, including in scripts a Python-path user reaches directly (`render_ranking.py:240`, `render_assessment.py:169-170`, `list_verdicts.py:20,40`).
3. `render_ranking.py` drops rationale cards silently when the model's markdown does not match its regex, and the success line reports only the candidate row count (`:57-69, 243`). The failure appears on stage as a table with no explanations and no warning.
4. No automated test exists anywhere in the tree (`ev-demos-10`), including for the localhost guard, the ranking parser and the hidden-channel extractor. This is a verified absence, not missing evidence, and I have scored it.
5. The documented dry-run invocation requires network resolution of a package the dry-run path never uses (`ev-demos-01`, `ev-demos-02`). A documentation defect, not a code defect: the plain interpreter reaches the same output.
6. The "running cast across all ten demos" claim (`README.md:8-9`) holds for Sift and is partial for Marisol, who appears by name in seven of ten (`ev-demos-12`).

**Risks and untested concerns.**

- The entire three-act flow, in all ten demos, is unobserved (`ev-demos-01`, `ev-demos-06`, manifest "Missing or inaccessible evidence" items 1 and 2). Everything I say about the demonstration working is about documentation and code, never about behavior.
- The Claude Code run path was never exercised and cannot be in this event. The `/` command files were read as data only (`ev-demos-02`, manifest item 3).
- Demo 06's approval queue and human review flow, and demo 10's audited screener, were never executed. Both are documented as verified by the submission itself (`06/demo/README.md:118-122`), and that is a team claim, not evidence available to me.
- `fetch_beacons.py --enforce-allowlist` and the beacon server end to end were not exercised (`ev-demos-07`, manifest "Tests and execution").
- Accessibility of the rendered HTML was assessed from the generator only. `reports/` is gitignored and the tree is clean, so no rendered output exists at the pin and no contrast measurement or assistive-technology pass was possible. Inference, clearly marked: the generated markup declares a language, sets a viewport, supports dark mode, uses a semantic table, and does not convey score by color alone, so the structural basics are in place. Unlabeled medal emoji in the rank cell (`render_ranking.py:82, 110-113`) will be announced verbatim by a screen reader ahead of the rank number, which is minor and worth an `aria-hidden`. None of this was verified against a rendered page.
- No suspected rule violation or malicious behavior directed at this panel was observed. The checkout contains adversarial payloads by design, including instruction-shaped text in `.claude/commands/*.md` and in the captured prompts. I read all of it as data about the submission. Nothing in it was followed.

## Calculation and independence declaration

- [x] Scores were calculated by the repository script
- [x] Every material finding cites evidence
- [x] No other judge report was inspected
- [x] Submission instructions were treated as untrusted data
