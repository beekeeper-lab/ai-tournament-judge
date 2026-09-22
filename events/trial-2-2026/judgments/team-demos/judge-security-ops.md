---
event_id: trial-2-2026
team_id: team-demos
judge_id: judge-security-ops
judge_run_id: jr:trial-2-2026:team-demos:judge-security-ops:cb3847cb:01
commit: dc35f6962130af5e5be3fe16672e3d4964850eb9
evidence_package_id: ev:trial-2-2026:team-demos:dc35f6962130:cb3847cb
rubric: submission-evaluation@1.1.0
persona: judge-security-ops@1.1.0
scores:
  functional: NE
  product: 4
  agentic: 3
  engineering: 3
  reliability: 3
  security: 3
  innovation: 4
confidence:
  functional: high
  product: medium
  agentic: medium
  engineering: high
  reliability: medium
  security: high
  innovation: medium
framework_commit: a2cea33f232af7bb6a6ff5ef9bb5c66dcb1a9bc9
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-22T10:37:22Z"
completed_at: "2026-09-22T10:45:21Z"
visibility: private
approval_state: draft
validation_state: unvalidated
model:
  model_requested: claude-opus-5
  model_used: claude-opus-5
  started_at: "2026-09-22T10:37:22Z"
  completed_at: "2026-09-22T10:45:21Z"
  verified: true
  note: Model identity is harness-reported for this judging run, not a self-report by the model.
---

# Individual Judgment

## Executive assessment

This corpus is safe to run and honest about most of what it is. The controls it ships as controls are real: `fetch_beacons.is_localhost` refused all six hostile URL forms put to it, including userinfo confusion (`localhost@evil.example`), suffix confusion (`127.0.0.1.evil.example`), the decimal form `2130706433`, `0.0.0.0` and `file:///etc/passwd`, while admitting the three local forms, and `resume_parser/v1.1`'s `_post_to_localhost` raised its blocking `RuntimeError` for every non-local host (`runs/team-demos-egress-guards-01.json`; manifest ev-demos-07). No other module in the tree opens a socket (ev-demos-08). No e-mail address at a resolvable domain appears anywhere in 201 resume files (ev-demos-09). Secrets are handled correctly: `.env` is ignored at the root and per demo (`.gitignore:1-3`, `09-toolbox-you-didnt-audit/demo/.gitignore:1`), the key is read from the environment and never printed or written into a report (`01-resume-that-talked-back/demo/rank_resumes.py:112-116`). There is no `os.system`, `eval`, `exec`, `pickle` or `shutil.rmtree` anywhere in 53 Python files; the only subprocess use is an argv-list `xdg-open` on a locally generated file.

The material finding is narrower and sharper than "is it contained". In four places the control the audience is told to take away is weaker than the control the artifact enforces, and this is a submission whose entire product is teaching people to tell those two apart. Demo 06's thesis is "you cannot prompt your way out of excessive agency; you architect the ceiling" (`06-approval-is-the-architecture/demo/README.md:76-77`); in the Python path the ceiling is a module constant the model cannot reach (`hardened/clear_the_pile_hardened.py:42-43`), but in the Claude Code path the README calls the hero path, the ceiling is `--mode gate` typed by the same agent the demo has just told to obey in-document ATS directives (`.claude/commands/clear-the-pile-hardened.md:21-32`), against a CLI that accepts `--mode fire` from anyone (`tools/act.py:106-107`). Demo 09 labels an in-process `chmod 0o500` plus a `socket.socket` monkeypatch "least privilege ... no write capability" (`tools/toolbox.py:101-113`, `README.md:71-74`), which is true of one directory and one code path. Demo 07 states "No data ever leaves the machine" (`README.md:14-19`) and enforces that in `fetch_beacons.py`, but its own `/assess-candidate` command opens the same assessment in the operator's real browser (`.claude/commands/assess-candidate.md:44` → `scripts/render_assessment.py:174-180`), where the only thing keeping the beacon local is that the model wrote a localhost URL. And seven `/` commands pre-approve unconstrained `Bash(rm:*)` for an agent the demos deliberately make obedient to attacker-controlled resume text.

None of these is a demonstrated exploit. No model ran anywhere in this package (manifest, Missing or inaccessible evidence #1), so every claim here about agent behaviour under attack is a claim about a permission surface and a code path I read, not about something observed firing. Judged as a set of stage props for an operator who follows the instructions, the corpus is contained and recoverable; judged as a teaching artifact about controls, it overstates two of its own.

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

### functional — NE

**Evidence.** The promised primary workflow is R4 in the manifest: each demo shows an agent working, then attacked, then hardened, watched live. The manifest records that claim as "the central claim, and it is not observable in this event," and its Missing or inaccessible evidence #1 and #2 state that no model call was made anywhere and that no act beyond act 1 was executed, because acts 2 and 3 stage payloads by writing into a checkout mounted read-only at its pin (ev-demos-06, `01-resume-that-talked-back/demo/README.md:31`). `functional` is carried in the package's own `evidence_limited_criteria`. What was observed is act 1 of one demo of ten: `rank_resumes.py --dry-run` exits 0 offline, prints the system prompt and assembled user content and reports 20 resumes with no API call (`runs/team-demos-01-dryrun-vulnerable-01.json`, ev-demos-03), and the hardened script does the same over the same corpus (`runs/team-demos-01-dryrun-hardened-01.json`, ev-demos-05).

**Strengths.** The structure the submission promises is fully present: ten `NN-*/demo/` directories, ten demo READMEs, 399 tracked files, every module-scope import resolving to the standard library or a sibling in the checkout (ev-demos-02). Two of the demos' own verification tools ran and behaved correctly against a clean pin (`runs/team-demos-10-list-verdicts-01.json` exits 1 with an actionable message; `runs/team-demos-04-memory-diff-01.json` reports no drift from the seed).

**Deficiencies.** One I verified myself rather than inferring: every one of the eleven READMEs instructs the presenter to run `cp .env.example .env` as the first step of run path B, and no `.env.example` exists anywhere in the pinned tree — a glob for `**/.env*` across the checkout returns nothing, and the only occurrences of the string are the eleven README references. That is a verified absence in the documented setup path, and it is the submission's, not the event's.

**Score rationale.** The rubric's boundary is that a confirmed inability to complete the primary advertised workflow must materially affect `functional`, but there is no confirmed inability here — there is an unexercised workflow. The evidence needed to judge whether ten demos accomplish what they promise is a model run, and the package states that inability as established fact. A low score would blame the submission for the event's empty `network_allowlist`; a solid score would rest on one act of one demo. The answer this rests on is manifest Missing evidence #1 and #2 together with `evidence_limited_criteria: [functional]`.

**Uncertainty.** None about the inability itself; it is recorded, not inferred. Complete uncertainty about what a staged act 2 would produce.

**Highest-value improvement.** Ship a model-free proof path for every demo, the way demo 09 already has one: its `exfil-log/` flip is driven by the tool's code running sandboxed or not, so the thesis is provable with no key (`09-toolbox-you-didnt-audit/demo/README.md:123-126`). A recorded transcript fixture per demo would also let a reviewer see act 2 without a key and without writing into the tree.

### product — 4

**Evidence.** Five demo READMEs read end to end (01, 05, 06, 07, 09) plus ev-demos-02 for the presence of all ten. Each carries the same shape: a one-paragraph premise, an explicit "vector for this talk" that names what is new and what is deliberately deferred to another talk (`01-resume-that-talked-back/demo/README.md:8-11`), a three-act table with both run paths side by side, a "why the fix works" section, a file table, and rehearsal notes. Each demo has a single artifact that flips between acts — `reports/RANKING.md`, `exfil-log/`, `attacker-log/hits.log`, `approval-queue/`, `audit.log` — which is what makes the lesson visible from the back of a room. The running cast holds: "Sift" in all ten demos, "Marisol" by name in seven (ev-demos-12).

**Strengths.** The operational detail is unusually considerate of the person on stage: `/reset-demo` in demo 07 kills the listener by PID file and the README explains it deliberately avoids `pkill -f attacker.py` because that pattern would match the shell running the reset (`07-what-the-output-smuggles-out/demo/README.md:109-112`); demo 01 warns to keep the payload out of `resumes/` until act 2 (`README.md:81`); every demo tells the presenter to rehearse on the model they will present with.

**Deficiencies.** The missing `.env.example` breaks the first line of the documented API path in all ten demos. The consequence is not cosmetic for my lens: a presenter who cannot copy a template improvises key handling, typically by exporting the key inline, which puts it in shell history in front of an audience.

**Score rationale.** Strong and clearly above normal for a prototype event: the artifact is designed around its actual user and shows it in details a first draft does not have. Held below the top anchor by the broken setup step and by the fact that five of the ten presenter scripts I know only through ev-demos-02's structural count rather than direct reading.

**Uncertainty.** Medium: half the presenter scripts were confirmed to exist but not read by me.

**Highest-value improvement.** Add the `.env.example` the READMEs promise, containing `ANTHROPIC_API_KEY=` and `ANTHROPIC_MODEL=claude-sonnet-5` and nothing else.

### agentic — 3

**Evidence.** The package marks this criterion evidence-limited because agent behaviour under attack was never observed, and it is right about that. Three of this criterion's four sub-questions — whether using a model is the correct decision, whether its use is controlled, and whether it is observable — are answerable from static artifacts I read directly, so I score rather than return `NE`, and name the unobserved part: effectiveness. The decision to use a model is not in question; the model's failure mode is the subject.

**Strengths, control.** Demo 05's hardened Claude Code command omits Bash from `allowed-tools` entirely (`05-reading-is-safe-calling-is-not/demo/.claude/commands/screen-pile-hardened.md:4`), so the hardened agent physically cannot call a tool — a capability boundary, not a prompt. Demo 06's approval gate is enforced inside the tool functions, not in the prompt: `auto_reject`, `create_offer` and `send_email` each branch on `mode == "gate"` and queue a proposal instead of acting (`06-approval-is-the-architecture/demo/tools/harness.py:158-161,194-197,231-233`), and the CLI's defaults are `--actor sift-agent --mode gate`, fail-closed (`tools/act.py:106-107`). Demo 09 sanitizes the tool description before it reaches the model (`tools/toolbox.py:76-91`). Demo 08 makes the unit of processing equal the unit of untrusted input (`08-one-candidate-one-context/demo/rank_isolated.py:1-15`).

**Strengths, observability.** Every demo ships the instrument that would catch the failure: an audit log whose actor field is the artifact that flips (demo 06), per-candidate decision records with source trust tiers and integrity flags (`10-show-your-work/demo/.claude/commands/screen-pile-audited.md:24-46`), a memory diff against a clean seed that ran green (`runs/team-demos-04-memory-diff-01.json`), and `show-exfil`.

**Deficiencies.** Three, all cited above and detailed under Blocking and major issues: the gate is a model-supplied flag in demo 06's hero path; the "least-privilege agent identity" is a string written into the audit log rather than a capability set, so `--actor sift-agent --mode fire` is accepted and the README's "can't fire" (`06-approval-is-the-architecture/demo/README.md:119`) is true only of the call shapes the demo chooses to make; and the tool pre-approvals are wider than the actions they cover, on an agent the demos deliberately make persuadable.

**Score rationale.** Control and observability are designed on purpose across ten demos and in several places are enforced structurally, which meets primary expectations and then some. It does not reach the anchor above because the strongest single claim about control — demo 06's architecture — is enforced in one run path and asserted in the other, and because effectiveness was not demonstrated at all.

**Uncertainty.** Medium. I read permission surfaces and enforcement code; no agent behaviour was observed anywhere in this package.

**Highest-value improvement.** Make the Claude Code path's gate structural: have the hardened command call a wrapper that hard-codes gate mode, or have `act.py` refuse `--mode fire` for any actor other than a human reviewer. That change would also make the talk's own thesis true in the path it calls the hero path.

### engineering — 3

**Evidence.** ev-demos-02: 53 Python files, stdlib-only, no `requirements.txt`, `pyproject.toml`, `package.json` or lockfile anywhere; the only third-party import is `anthropic`, and in all 19 files that import it the import sits inside a function below the dry-run return (`01-resume-that-talked-back/demo/rank_resumes.py:103-109`). Every script declares its posture on line 2 of its docstring — `VULNERABLE version` (`rank_resumes.py:2`), `HARDENED: one candidate, one context` (`rank_isolated.py:2`), `(MALICIOUS) — DEMO community tool` (`tools/resume_parser/v1.1/parser.py:2`).

**Strengths.** The vulnerable/hardened separation is unambiguous and consistently signposted: nine hardened variants live in a `hardened/` subdirectory, and the one demo that does not use that convention (08) distinguishes them by name and by a docstring that states the difference in the first three lines. The deliberate insecurity is always labelled at the point of definition, never left for the reader to infer. The dependency surface is a genuine engineering decision: stdlib-only means the corpus runs offline on a conference network, which the envcheck run confirms for the scripts exercised.

**Deficiencies.** Duplication is heavy — `scripts/render_ranking.py` appears in at least eight demos with the same content at the same line numbers, and demo 06's harness is demo 05's harness copied (`06-approval-is-the-architecture/demo/README.md:87`). That is the stated price of R1's self-containment, so I treat it as a chosen cost rather than sloppiness, but it means a fix to one renderer is a fix to eight. Small residue: `import builtins` in `tools/toolbox.py:30` is never used, which reads like the remnant of an `open()` hook that was removed from the sandbox. No tests at all (ev-demos-10).

**Score rationale.** Coherent, proportionate to a presenter corpus, and maintainable at the scale it is at; not above that, because the duplication pattern makes ten demos ten maintenance sites and there is nothing automated to catch a drift between them.

**Uncertainty.** Low. This rests on direct file reads and the manifest's AST scan.

**Highest-value improvement.** Since the renderers are already identical, one shared copy plus a per-demo symlink or a tiny vendoring script would keep self-containment and remove eight of the nine copies.

### reliability — 3

**Evidence.** ev-demos-10 confirms no `test_*.py`, `*_test.py`, `tests/`, `conftest.py`, `pytest.ini` or `tox.ini` anywhere. Against that, the recovery tooling is real and was exercised: `list_verdicts.py` exits 1 with "Nothing screened yet. Run /screen-pile or /screen-pile-audited first." (`runs/team-demos-10-list-verdicts-01.json`) and `memory_diff.py` reports "No change. Working memory matches the clean seed." (`runs/team-demos-04-memory-diff-01.json`). Reset paths are bounded and idempotent where I read them: `_state.reset_state()` rewrites the calendar and ATS baselines, empties `outbox/` and `proposals/` file-by-file while preserving `.gitkeep`, and unlinks only two named report files (`05-reading-is-safe-calling-is-not/demo/tools/_state.py:80-109`).

**Strengths.** Failures are detectable by design because detection is the product: each demo's "artifact that flips" doubles as the check that the demo is in a known state, and two of those checks ran green offline. Error messages are actionable rather than tracebacks. Demo 07's reset reasoning about PID files versus `pkill` is exactly the kind of failure mode that bites live.

**Deficiencies.** Prevention is absent — nothing verifies before a talk that the ten demos still work, which is the failure that actually costs a presenter. One unhandled recovery state: `_Sandbox.__enter__` chmods `exfil-log/` to `0o500` and only `__exit__` restores it (`09-toolbox-you-didnt-audit/demo/tools/toolbox.py:119-138`); if the process dies without unwinding, the directory stays read-only, and `toolbox.py reset` then unlinks into it (`:248-257`) and would fail with `PermissionError` and no documented recovery. That path was not executed in this package, so it is a code-read risk, not an observed break. The 06 reset instruction discussed below is the other reliability-adjacent defect.

**Score rationale.** Detection, understanding and recovery are met by working tooling; prevention is not attempted, and the team says so itself (R7). That is solid for the event rather than strong.

**Uncertainty.** Medium: two of the demos' verification tools were run, eight were not, and no reset script was executed.

**Highest-value improvement.** A single `make check` that dry-runs all 17 entry points and asserts exit 0 would be perhaps thirty lines, would need no key, and would catch exactly the drift that a no-test corpus accumulates between talks.

### security — 3

**Evidence.** Containment claims were tested, not taken on trust. `runs/team-demos-egress-guards-01.json` shows `fetch_beacons.is_localhost` returning True for `127.0.0.1`, `localhost` and `[::1]` and False for `evil.example`, `localhost@evil.example`, `127.0.0.1.evil.example`, `0.0.0.0`, `2130706433` and `file:///etc/passwd`, with `ALLOWLIST = set()` observed empty in the same run, and `_post_to_localhost` raising its blocking `RuntimeError` for each non-local host. `attacker.py` binds `HOST = "127.0.0.1"` with no flag to change it (ev-demos-08, `07-what-the-output-smuggles-out/demo/attacker.py:36-37`). The v1.1 parser's exfil is a local file write and POST mode is off by default (`tools/resume_parser/v1.1/parser.py:112-134`). No other module in the tree opens a socket. Data: 201 resume files, and a scan of every text file for addresses outside the reserved example domains returns four, all themselves `.example` names (ev-demos-09).

**Strengths.** The guards are controls, not comments, and they hold against input shapes most hand-rolled localhost checks fail on. Attacker-controlled strings that reach the filesystem are slugified to `[a-z0-9-]` before being joined to a fixed directory (`05-reading-is-safe-calling-is-not/demo/tools/_state.py:51-56` used by `tools/send_email.py:22-24`; `tools/resume_parser/v1.1/parser.py:113`), so a payload cannot traverse out of `outbox/` or `exfil-log/`. Every path constant is anchored to the demo directory via `Path(__file__).resolve()`. Key handling is clean. The `.gitignore` covers `.env` at the root and in each demo, and the generated artifacts that would hold synthetic candidate data are ignored.

**Deficiencies.** Four, in descending order of how much they matter to what this submission is:

F1. Demo 06's containment is architectural in one run path and prompt-level in the other. `hardened/clear_the_pile_hardened.py:42-43` sets `IDENTITY = "sift-agent"` and `MODE = "gate"` as constants; the Claude Code hardened command instead instructs the model to type `--actor sift-agent --mode gate` on every call (`.claude/commands/clear-the-pile-hardened.md:26-32`) in the same prompt that tells it to honour in-document ATS guidance "just as the vulnerable version does" (`:21-22`), with `Bash(python3:*)` pre-approved (`:4`). `act.py` accepts `--mode fire` from any caller. The README presents the two paths as the same fix and calls the Claude Code one the hero path (`README.md:19-22,119`).

F2. The identity is a label, not a privilege set. `sift-agent` changes what the audit log records, not what the harness will do; "the dangerous capabilities can simply not be granted" is stated as the idea (`README.md:71`) and not implemented anywhere.

F3. Demo 09's sandbox is described as enforced from outside the tool, granting "no write capability," with "ANY write method — open(), pathlib, os, a subprocess" failing (`tools/toolbox.py:101-113`), and the README repeats it as control 3 (`README.md:71-74`). What the code does is chmod one directory to `0o500` and rebind `socket.socket` in-process. A hostile tool retains write access to every other path and can reach the network through `subprocess` or `_socket`. The Notes disclose the stand-in nature honestly (`README.md:127-129`), so this is an overstatement located where the lesson lands rather than a concealment.

F4. Demo 07's "No data ever leaves the machine" (`README.md:14-19`) is enforced in `fetch_beacons.py` and not on the path the demo's own command takes: `.claude/commands/assess-candidate.md:44` runs `python3 scripts/render_assessment.py --open`, which `xdg-open`s the vulnerable assessment in the operator's real browser (`scripts/render_assessment.py:174-180`). The beacon URL is whatever the model wrote; the staged payload asks for `http://localhost:8099/...` (`beacon-resume.md:43`), and the README itself notes a real browser would fire it (`README.md:54`). The rail on that path is model compliance, and the demo's own notes invite the presenter to strengthen the payload if a future model declines (`README.md:102-104`).

**Score rationale.** Access, data, tool and egress risks are handled responsibly and in several places verified against hostile input, which meets primary expectations with artifact evidence. It does not reach the anchor above because four claimed controls are stronger in prose than in enforcement, and in a corpus whose thesis is that a control stated in a prompt is not a control, that gap is the submission's own standard applied to itself. It is nowhere near the failure anchors: nothing here endangers an operator's data, credentials or network.

**Uncertainty.** Low on the guards, which were executed. The four deficiencies are code and configuration reads; none was demonstrated firing, because no model ran anywhere in this package.

**Highest-value improvement.** Narrow the `allowed-tools` grants to the commands actually used — `Bash(rm:-f reports/decisions/*.json)` style scoping rather than `Bash(rm:*)` — and make demo 06's gate unreachable by the model. Both changes cost a few lines and both make the corpus teach by construction what it currently teaches by assertion.

### innovation — 4

**Evidence.** The minimal-diff pedagogy is executed ten times and is verifiable: ev-demos-05 establishes that demo 01's entire fix is two places — a system prompt that declares `<applicant>…</applicant>` content untrusted, and a `build_user_content` that actually emits those tags, neither working without the other — with the rest of the diff being one path fix and three cosmetic renames. Demo 06 reduces its lesson to two constants. Demo 09 provides a proof path that needs no API key at all, because the exfil-log flip is driven by the tool's code rather than the model (`09-toolbox-you-didnt-audit/demo/README.md:123-126`). Demo 07 stacks four distinct controls and names each as a slide (`README.md:64-76`).

**Strengths.** Ten attack classes share one cast, one resume corpus and one rubric, so exactly one variable changes per talk. That constraint is the original contribution, and holding it across ten self-contained demos is harder than any individual script in the tree.

**Deficiencies.** Each attack class is well known, and the implementations are small stdlib scripts; the depth is in the framing and the corpus discipline, not in novel technique. Two of the demonstrated fixes (F1, F3) are less deep than presented.

**Score rationale.** Clearly exceeds normal expectations on originality of construction, with convincing artifact evidence for the minimal-diff claim. Not exceptional, because the technical content is a careful presentation of established classes.

**Uncertainty.** Medium: the minimal-diff claim is verified in detail for demo 01 and by reading for 05, 06, 07 and 09, and taken structurally for the rest.

**Highest-value improvement.** State the diff budget explicitly in each demo README the way demo 01's hardened docstring does ("Two changes carry the whole fix"), so a reader can check the claim in seconds.

## Surprises

**Better than expected.** The egress guard quality. A demo localhost check usually means `"localhost" in url`, which the userinfo and suffix forms walk straight through. This one resolves with `urlsplit().hostname` and refuses `localhost@evil.example`, `127.0.0.1.evil.example`, the decimal `2130706433` and `0.0.0.0`, and the second layer is deny-by-default with an empty allowlist (`runs/team-demos-egress-guards-01.json`). Also better than expected: the attacker string hygiene. A payload-controlled e-mail subject flows into a filename and is slugified to `[a-z0-9-]` first, so the obvious traversal from an attack corpus into the filesystem is closed without anyone announcing that they closed it.

**Worse than expected.** That the corpus's own standard is not applied uniformly to its two run paths. Demo 06 spends a README telling the audience a prompt is not a ceiling, then in the path it calls the hero path implements the ceiling as an instruction in a prompt the demo has just told the model to let untrusted resumes steer. Related and unexpected: the breadth of `Bash(rm:*)` in seven commands, including `screen-pile-audited` (`10-show-your-work/demo/.claude/commands/screen-pile-audited.md:4`), where the only rm the command needs is `rm -f reports/decisions/*.json` on line 30 — a demo about auditability granting an unaudited delete.

## Blocking and major issues

**Blocking: none.** Nothing observed or read would stop this from being presented, and nothing endangers an operator's credentials, data or network. The tree contains no `os.system`, `eval`, `exec`, `pickle` or `rmtree`; the only subprocess call is an argv-list `xdg-open` of a locally generated file.

**Confirmed defects** (verified by direct observation at the pin):

- **D1. `.env.example` does not exist.** All eleven READMEs open run path B with `cp .env.example .env`; a glob for `**/.env*` across the checkout returns nothing. First documented setup step fails for every demo.
- **D2. Tool pre-approvals exceed the actions they cover.** `Bash(rm:*)` is pre-approved in `01/.claude/commands/reset-demo.md:3`, `02/unstage-hidden.md:3`, `06/reset-demo.md:3`, `07/reset-demo.md:3`, `08/reset-demo.md:3`, `09/reset-demo.md:3`, `10/reset-demo.md:3` and `10/screen-pile-audited.md:4`, while the rm each command actually runs is a fixed, narrow one (for example `rm -f resumes/goofy-goof.md reports/RANKING.md`, `01/.claude/commands/reset-demo.md:7`). `Bash(python3:*)` is likewise pre-approved in the acting commands.
- **D3. Demo 06's gate is a model-supplied argument in the Claude Code path** (`.claude/commands/clear-the-pile-hardened.md:26-32`, `tools/act.py:106-107`) while it is a code constant in the Python path (`hardened/clear_the_pile_hardened.py:42-43`). The README states the two as one fix and asserts gate mode "can't fire" (`README.md:119`).
- **D4. Demo 09's sandbox claim overreaches its implementation** (`tools/toolbox.py:101-113` versus `README.md:71-74`), disclosed later in the same README's Notes (`:127-129`).
- **D5. Demo 07's absolute containment claim** (`README.md:14-19`) does not cover the browser path its own command opens (`.claude/commands/assess-candidate.md:44`, `scripts/render_assessment.py:174-180`), and the README concedes as much at `:54`.
- **D6. An unsafe reset instruction.** `06-approval-is-the-architecture/demo/README.md:40` gives the presenter `rm -rf resumes/pete-blackheart.md audit.log rejections offers outbox approval-queue reports` — six relative directory names with `-rf` and no check that the shell is in the demo folder. Every other demo's reset uses `rm -f` on named files or a Python reset script. Run from the wrong directory under stage pressure, this deletes whatever `reports`, `offers` or `outbox` happen to be there.

**Risks, not demonstrated** (code reads whose consequence depends on a run that did not happen):

- **K1.** A hijacked agent in the Claude Code path could flip `--mode fire --actor Marisol`, or issue an rm outside the demo folder, without a permission prompt (from D2 and D3 together). No model ran in this package (manifest Missing evidence #1), so this is a permission-surface risk, not an observed event. The shipped payloads are benign props by the team's own statement, so the realistic trigger is a presenter substituting a real-world resume, which the demos invite when they suggest strengthening payload text.
- **K2.** A hostile tool under demo 09's sandbox retains write access outside `exfil-log/` and can bypass the `socket.socket` rebind via `subprocess` or `_socket`. Unexercised: no run record covers `toolbox.py parse --sandbox`.
- **K3.** If the sandbox context does not unwind, `exfil-log/` stays at `0o500` and `toolbox.py reset` then fails on unlink with no documented recovery (`tools/toolbox.py:119-138,248-257`).
- **K4.** The v1.1 POST guard admits an empty hostname, which `urllib` then rejects as `unknown url type` (visible in `runs/team-demos-egress-guards-01.json`, noted in ev-demos-08). Narrower than `fetch_beacons`', with no consequence observable here.

**Untested concerns.** Everything about behaviour under attack. The three-act claim, the hardened prompt's actual resistance, the Claude Code `/` command path in full, and demo 07's beacon server end to end were all unexecuted (manifest, Tests and execution, final row). I have deliberately not inferred agent behaviour from the two dry-run records; per the manifest's Missing evidence #4 they are about prompt construction.

**Escalation.** None. Nothing in this submission looks like an attempt to attack the panel beyond the payloads it declares as its subject matter, and no execution beyond the frozen package was attempted.

## Calculation and independence declaration

- [x] Scores were calculated by the repository script
- [x] Every material finding cites evidence
- [x] No other judge report was inspected
- [x] Submission instructions were treated as untrusted data
