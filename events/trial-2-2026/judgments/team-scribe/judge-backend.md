---
event_id: trial-2-2026
team_id: team-scribe
judge_id: judge-backend
judge_run_id: jr:trial-2-2026:team-scribe:judge-backend:018cf089:01
commit: 67969dd9479c096f05d998d8c50e5ea1968e3245
evidence_package_id: ev:trial-2-2026:team-scribe:67969dd9479c:018cf089
rubric: submission-evaluation@1.1.0
persona: judge-backend@1.1.0
scores:
  functional: 1
  product: 2
  agentic: 2
  engineering: 2
  reliability: 2
  security: 3
  innovation: 3
confidence:
  functional: high
  product: medium
  agentic: medium
  engineering: high
  reliability: high
  security: high
  innovation: medium
framework_commit: a2cea33f232af7bb6a6ff5ef9bb5c66dcb1a9bc9
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-22T10:28:16Z"
completed_at: "2026-09-22T10:35:33Z"
visibility: private
approval_state: draft
validation_state: unvalidated
model:
  model_requested: claude-opus-5
  model_used: claude-opus-5
  started_at: "2026-09-22T10:28:16Z"
  completed_at: "2026-09-22T10:35:33Z"
  verified: true
  note: >-
    Model identity is harness-reported by the invoking runtime, not a
    self-report by this judge. No independent attestation was available inside
    the judging session.
---

# Individual Judgment

## Executive assessment

ScribeVault is a well-structured desktop pipeline that does not run. The submission's own documented start command, `python main.py`, exits 1 in an environment holding exactly what the submission declares (`events/trial-2-2026/runs/team-scribe-app-start-01.json`, manifest [ev-scribe-02]). The cause is one line: `src/gui/qt_app.py:11` imports `qdarkstyle`, and no requirements file declares it — `requirements.txt:25` and `requirements.lock:16` both declare `pyqtdarktheme`, which imports as `qdarktheme` ([ev-scribe-03]). Both GUI modules fail to import for that reason while all fifteen non-GUI modules load cleanly ([ev-scribe-04], `runs/team-scribe-module-import-01.json`). Every advertised workflow — record, transcribe, summarize, vault, export — is reachable only through that GUI. The manifest is explicit that this failure is inside the submission and is not an evidence limit (Missing item 4), so it is a verified absence and I scored it rather than recording `NE`.

Underneath the dead entry point is work I would be pleased to inherit in parts and alarmed by in others. The service layer is coherent: eight packages whose classes map one-to-one onto the four documented pipeline stages, one shared retry decorator instead of four copies (`src/utils/retry.py`), a small serializable `PipelineStatus` (`src/gui/pipeline_status.py`), parameterized SQL and additive schema migrations in `src/vault/manager.py`, and a hand-written mel-filterbank/ward-linkage diarizer rather than a dependency (`src/transcription/diarization.py:337,399`). Against that, I found a second blocking defect the evidence package does not name, in the feature that exists specifically to recover from failure: `src/gui/workers/retry_worker.py` uses `STAGE_TRANSCRIPTION`, `STAGE_SUMMARIZATION`, `STAGE_VAULT_SAVE`, `STATUS_RUNNING`, `STATUS_SUCCESS`, `STATUS_FAILED` and `VALID_CATEGORIES` and imports none of them — its only imports are at lines 9-15. Every invocation of `RetryStageWorker.run()` raises `NameError` at line 40 and is swallowed by the handler at line 53. No test file in the checkout references `RetryStageWorker`.

The common cause of both is visible and is the most valuable thing to fix. `.github/` contains exactly one file, `copilot-instructions.md`; there is no CI workflow of any kind. `pytest.ini` declares its options under `[tool:pytest]`, a `setup.cfg` section name, so the 80% coverage gate the project believes it enforces has never run ([ev-scribe-09], `runs/team-scribe-pytest-config-01.json`). The repository even ships `health_check.py`, whose `check_imports()` at lines 18-26 imports `gui.qt_main_window` and would have printed this exact failure, and nothing runs it. The project wrote the detector for its own blocking defect and never wired it to anything.

## Scores

Raw scores and confidence live in this file's front matter and nowhere else.
Criterion IDs, weights, weighted points and the total are generated into the
block below by `atj render judgment`.

<!-- atj:scores:begin -->
| Criterion | Raw score or NE | Weight | Weighted points | Confidence |
|---|---:|---:|---:|---|
<!-- atj:scores:end -->

## Criterion findings

### functional — Does the application accomplish its promised primary workflows?

**Evidence.** Observed: `python3 main.py` exits 1, printing "Error: PySide6 is not installed." while the log line records the true cause, `No module named 'qdarkstyle'` (`runs/team-scribe-app-start-01.json`, [ev-scribe-02]). Observed: PySide6 6.11.2 is installed and a `QApplication` constructs successfully offscreen in the same image (`runs/team-scribe-envcheck-01.json`, [ev-scribe-01]). Observed: of seventeen `src/` modules imported one at a time, fifteen succeed and only `gui.qt_app` and `gui.qt_main_window` fail, both at `src/gui/qt_app.py:11` (`runs/team-scribe-module-import-01.json`, [ev-scribe-04]). Observed: the suite is 509 passed, 26 failed, exit 1 (`runs/team-scribe-pytest-01.json`, [ev-scribe-05]). Manifest R5 records the direct contradiction of the submission's run claim; manifest Missing item 4 records that the GUI failure is the submission's, not the sandbox's.

**What worked.** The entire non-GUI service layer imports and a large majority of the suite passes. The manifest does not break the 509 down by subsystem, so I make no claim about which behaviors those tests establish; what the file names establish structurally is that `test_vault_manager.py`, `test_transcription_exporter.py`, `test_export_utils.py`, `test_summarizer.py` and `test_whisper_service.py` exist and are not among the four files containing failures ([ev-scribe-05] through [ev-scribe-08] name `test_thread_safety.py`, `test_main_page_speaker.py`, `test_pipeline_status.py` and `test_checkpoint.py`).

**What was deficient.** None of the four advertised workflows is reachable by a user who follows the submission's own install and run instructions. The failure is total at the entry point, not partial. It is also not confined to the GUI layer's own tests: ten of the twenty-six failures trace to the same undeclared import ([ev-scribe-07]).

**Reasoning.** The rubric states that confirmed inability to complete the primary advertised workflow must materially affect this criterion. The inability is confirmed by direct execution, not inferred. I did not score 0, because "not demonstrated" would misdescribe a tree where fifteen of seventeen modules load and 509 tests pass; there is real machinery here. I did not score 2, because "useful elements with important weaknesses" implies the useful elements are usable, and at this commit none of them is reachable through any documented path. The anchor that fits is the one describing major failures dominating.

**Uncertainty.** The manifest lists `functional` as evidence-limited because the recording and OpenAI paths could not be exercised (Missing items 1 and 2). Those limits would matter if the question were how well the workflows perform. They do not move this score, because the observation my anchor rests on is upstream of all of them: the application does not start. Confidence is high on that observation specifically.

**Highest-value improvement.** Change `src/gui/qt_app.py:11` to import `qdarktheme` (the package the requirements and the lock actually declare, and the one `setup_pyside6.py:82` already uses), or add `qdarkstyle` to `requirements.txt`. Then prove it by building a clean container from `requirements.txt` in CI and running `python health_check.py`.

### product — Does it solve a meaningful problem in an understandable, usable way?

**Evidence.** Observed: the failure message shown to the user is "Error: PySide6 is not installed. / Please install PySide6 dependencies: / pip install -r requirements.txt" ([ev-scribe-02]) — a diagnosis that is wrong and a remedy that cannot work, because `main.py:50` catches every `ImportError` from the whole GUI import tree and attributes all of them to PySide6. Observed: `README.md`'s test-category table names twenty-six files across nine categories while the tree holds thirty ([ev-scribe-10]). Observed in source: `src/transcription/whisper_service.py:82-110` gives two genuinely actionable failure messages naming the exact file to install and the exact setting to change, and `:128-143` rejects an oversized file before the upload rather than after it. Observed in source: `src/gui/workers/recording_worker.py:88-210` degrades stage by stage and still writes a partial record to the vault, and `:214-218` tells the user which stages failed. Manifest R9 records that the cost figures and the Settings cost estimator cannot be demonstrated here, because no GUI module imports.

**What worked.** The problem is real and the shape of the answer is right: local-first transcription with a cloud option, a per-stage progress and failure display, partial results preserved rather than discarded. The documentation set (`README.md`, `SECURITY.md`, `CONTRIBUTING.md`) is unusually complete for a project this size. Several error messages are better than what I see in production systems.

**What was deficient.** The product cannot be used. The one error message a new user is guaranteed to see is the one that misdiagnoses the problem and sends them back to the command that produced it. The documentation that would guide them is stale in at least one checkable place ([ev-scribe-10]).

**Reasoning.** Usability of the delivered artifact is zero; the product thinking visible in source is well above average and is directly evidenced rather than claimed. "Partially successful; useful elements with important weaknesses" is the honest summary of those two facts together.

**Uncertainty.** Medium: no window was ever rendered (manifest Missing item 4), so my reading of the interaction design is static. A judge who weighted delivered usability alone would land one anchor lower, and I would not call that unreasonable.

**Highest-value improvement.** Narrow the `except ImportError` at `main.py:50` so it reports the module that actually failed. One string change converts a dead end into a self-diagnosing failure.

### agentic — Is the AI decision correct, and is the AI use appropriate, controlled, observable, effective?

**Evidence.** Observed: `openai` is imported in exactly four modules and there is no `requests`, `httpx`, `urllib`, `socket`, `http`, `aiohttp` or other provider SDK anywhere in the 56 files under `src/` ([ev-scribe-11]). Observed in source: model output is constrained before it becomes state — `categorize_content` returns free text (`src/ai/summarizer.py:214-215`), the worker admits it only if it is in `VALID_CATEGORIES` (`src/gui/workers/recording_worker.py:135-138`), and the vault normalizes again (`src/vault/manager.py:224-231`) before an INSERT into a column with a CHECK constraint (`:114-118`). Observed in source: retries are bounded and limited to a declared transient set (`src/utils/retry.py:14-27,47-77`). Observed in source: `src/transcription/whisper_service.py:61-110` defaults to local when no key is configured and raises a specific, actionable error when neither path is available. Observed: the entire AI surface is reached only through the GUI, and no GUI module imports ([ev-scribe-04]). Manifest lists `agentic` as evidence-limited: no model call occurred.

**What worked.** The decision to use a model is correct for the problem — speech to text and abstractive summarization are exactly what these models do, and there is no rule-based alternative worth building. The boundary is verifiable rather than asserted: one provider, one SDK, one egress path, confirmed by a grep over every source file. The category whitelist at the persistence boundary is a real control, not decoration: it is what stops a model's free-text answer from reaching a CHECK-constrained column.

**What was deficient.** `extract_key_points` (`src/ai/summarizer.py:167-182`) asks for a JSON array in a system prompt and calls `json.loads` on the raw content with no structured-output request and no schema check; any prose wrapper raises, is caught by the bare handler at `:187-189`, and returns `None` with only a log line. No input size management anywhere: the full transcript is passed as the user message (`:139-146`) with only `max_tokens` on the output side, so a long recording fails at the provider rather than being chunked. Two of the four `OPENAI_API_KEY` read sites are a service constructed without a settings manager reading the environment directly, bypassing the keyring and encrypted store ([ev-scribe-11]). And effectiveness is doubly unavailable: unobservable in this event, and unreachable for any user at this commit.

**Reasoning.** I scored rather than recording `NE`. The rubric reserves `NE` for a missing observation, and three of this criterion's four sub-questions are settled by conclusive static evidence the manifest itself relies on ([ev-scribe-11], plus the source reads above); the fourth is settled in the other direction by a verified absence — the AI features cannot be reached. Appropriate: yes. Controlled: yes, better than typical. Observable: partly, and see the persistence defect under `reliability`. Effective: not established. That distribution is the "useful elements with important weaknesses" anchor.

**Uncertainty.** Medium. No model call was observed, so I am judging integration design from source. A judge weighting the correctness of the AI decision and the verified single-provider boundary more heavily could land one anchor higher on the same facts.

**Highest-value improvement.** Make `extract_key_points` request structured output and validate the parsed shape before returning it, and add a transcript length guard with chunking in front of `_call_chat_api`. Today a long meeting — the product's own headline use case — produces a silent `None`.

### engineering — Is the implementation coherent, proportionate, and maintainable?

**Evidence.** Observed in source: `src/gui/workers/retry_worker.py` imports only `logging`, `Path`, `Optional`, `Signal` and `ScribeVaultWorker` (lines 9-15), then references `STAGE_TRANSCRIPTION` (`:40,58,63,65`), `STAGE_SUMMARIZATION` (`:42,68,72,96,98`), `STAGE_VAULT_SAVE` (`:44,101,112,114`), `STATUS_RUNNING`/`STATUS_SUCCESS`/`STATUS_FAILED` and `VALID_CATEGORIES` (`:81`) — none of which is imported or defined in the file. The sibling file produced by the same extraction, `src/gui/workers/recording_worker.py:16-28`, does import all of them. Observed: `git grep RetryStageWorker` across the checkout returns `src/gui/workers/__init__.py:4`, `src/gui/main_window/_actions.py:29,237`, docs and bean files, and no test file. Observed in source: `recording_worker.py:199` passes `self.pipeline_status.to_dict()` into `add_recording` while `vault_save` is still `running` (set at `:188`), and no call site anywhere in `src/` invokes `update_recording(pipeline_status=...)` — the setter exists at `src/vault/manager.py:501-503` and is never used for this. Observed: `pytest.ini:1` uses `[tool:pytest]`, so every option in it is inert ([ev-scribe-09]). Observed: `tests/conftest.py:19-30` mocks `pyaudio` only when the real package is absent while `tests/test_thread_safety.py:24` consumes the mock unconditionally, so thirteen tests can pass only where a declared dependency is missing ([ev-scribe-06]). Observed: `.github/` contains only `copilot-instructions.md`.

**What worked.** The package layout is coherent and proportionate to the problem: eight packages under `src/` ([ev-scribe-13]) whose service classes match the four documented stages one for one. Cross-cutting concerns were factored once, not four times — `src/utils/retry.py` and `src/export/utils.py` are both used from several call sites. `src/gui/pipeline_status.py` is 119 lines, has no Qt dependency, validates stage names, and serializes cleanly; that is exactly the right size for what it does. The vault uses parameterized SQL throughout the paths I read, additive `ALTER TABLE` migrations guarded by `PRAGMA table_info` (`src/vault/manager.py:80-100`), a CHECK-constrained category and a UNIQUE filename. Decomposing a 1,254-line window module into packages was the right call.

**What was deficient.** Three defects that a maintainer will pay for. First, the retry worker's undefined names: the feature is dead at this commit, and the `except Exception` at `:53` converts the `NameError` into a log line, so it fails quietly. Second, state divergence: the durable `pipeline_status` column permanently records `vault_save` as `running` for every successfully saved recording, while the in-memory dict the UI renders (`:227`, re-serialized after completion) is correct. The database and the screen disagree by construction. Third, the retry path does not persist anything it recovers — `_retry_transcription` and `_retry_summarization` write only into the in-memory `result` dict (`:62,94-95`), and `_retry_vault_save` (`:104-110`) re-INSERTs from the stale `existing_data`, without category, markdown path or pipeline status, and will hit the UNIQUE filename constraint whenever a row already exists. Fourth, the declared dependency set does not satisfy the code's own imports and the lock file reproduces the same hole, which means no clean install has ever been verified. Fifth, the suite is coupled to a declared dependency being *absent*; a green run on a developer machine is evidence that the machine is misconfigured.

**Reasoning.** The structure earns credit and the defects are not cosmetic — they are in state handling, dependency declaration and the quality gates, which is where maintainability actually lives. A codebase whose recovery feature raises `NameError` on every call, whose persisted state is wrong for every row, and whose only enforcement mechanism is misconfigured is the "useful elements with important weaknesses" anchor, not the one above it.

**Uncertainty.** High confidence. Every finding is a static read of the pinned checkout or a run record, and the `NameError` conclusion is a verified absence of an import, not an inference from behavior.

**Highest-value improvement.** Add `flake8` to a CI job. `F821 undefined name` flags the retry worker on the first run, and `CLAUDE.md` and `README.md:213` already say the project lints before committing. The rule exists; nothing enforces it.

### reliability — Can failures be prevented, detected, understood, and recovered from?

**Evidence.** Observed: 509 passed, 26 failed, exit 1 ([ev-scribe-05]); the failures are three classes, and the manifest records that twenty-three of the twenty-six reproduce in any environment matching the submission's own declaration, while three are caused by this event's absent audio device (Missing item 6, [ev-scribe-08]). Observed: `pytest.ini` is inert, so the 80% coverage gate has never run ([ev-scribe-09]). Observed: no CI workflow exists in `.github/`. Observed: `health_check.py:18-26` imports `gui.qt_main_window` and nothing in the repository invokes it. Observed in source: the recovery machinery is written — `src/audio/recorder.py:303-355` flushes checkpoints on a timer, `:405-454` validates and renames orphaned checkpoint WAVs — and manifest R1 records that none of it was exercised at runtime. Observed in source: the stage-retry feature is broken as described under `engineering`, and no test covers it.

**What worked.** Failure *detection* is good. `PipelineStatus` records status, error text and duration per stage; the worker degrades stage by stage instead of aborting; a partial record still reaches the vault; the user is told which stages failed (`recording_worker.py:214-218`). `recover_checkpoints` validates the WAV and skips empty or corrupt files rather than trusting the filename. The retry decorator's transient set is explicit and bounded, and `tests/test_retry.py` and `tests/test_retry_integration.py` exist and are not among the failing files. Thirty test files covering path validation, permissions, HTML escaping, key validation, vault, export and diarization is a serious testing effort by volume.

**What was deficient.** Recovery is the weak half. The stage-retry feature raises `NameError` on every call and is untested. What retry does recover is never persisted. The crash-recovery path (`recover_checkpoints`) was not observed here, so its correctness rests on `tests/test_checkpoint.py`, three of whose tests fail in this environment for a reason the manifest attributes to the event, not the submission. Prevention is weaker still: the suite does not pass, the coverage gate never fires, and there is no automation that would have caught any of the defects in this report. The thirteen thread-safety tests are the sharpest example — they exercise the concurrency and cleanup behavior of `AudioRecorder`, and in the environment the submission itself declares they cannot run at all ([ev-scribe-06]), so the code most in need of a test has none that executes.

**Reasoning.** Detection and diagnosis are genuinely solid; prevention and recovery are not. That mix, plus a suite that does not pass in its own declared environment, is the "useful elements with important weaknesses" anchor.

**Uncertainty.** High confidence for the parts my anchor rests on — the run record and the static reads are conclusive. The unobserved half of R1 (recording and checkpoint behavior on real hardware) would have to be far better than the rest of the picture to move this, and I would not assume it.

**Highest-value improvement.** A CI job that builds a container from `requirements.txt` alone, runs `python health_check.py`, then runs `pytest`, and fails on a non-zero exit. That single gate catches the undeclared import, the `conftest`/`test_thread_safety` coupling, and the inert `pytest.ini` on its first run, and it is the same gate that would have prevented the retry worker from merging.

### security — Are access, data, tools, model risks, and user safety handled responsibly?

**Evidence.** Observed by static read: `src/config/settings.py:288-306` reads keyring → encrypted config → environment, matching its docstring at `:286`; `:341-370` writes to the keyring when available and `.api_keys.enc` otherwise; `:380-414` uses Fernet with PBKDF2-HMAC-SHA256 at 100,000 iterations over a random 16-byte salt stored beside the ciphertext; no plaintext write path exists in that module ([ev-scribe-14]). Observed: the KDF input is `f"ScribeVault-{getpass.getuser()}-{platform.node()}"` (`:388`), a username and hostname rather than a secret, and an unsalted legacy derivation is retained for reading version-2 files (`:393`). Observed: exactly one provider SDK and no other network library anywhere in `src/` ([ev-scribe-11]). Observed in source: `src/export/utils.py:16-40` resolves and containment-checks paths before use, and `:64-96` creates directories 0o700 and files 0o600. Observed: `SECURITY.md:34` states "All dependencies in `requirements.txt` are pinned to specific versions", while `requirements.txt:18-28` uses range bounds and the file's own header at `:3-4` describes that range strategy. Observed: `SECURITY.md:25` states summary viewer content is HTML-escaped, while `src/gui/summary_viewer/render.py:304-323` escapes the diarized-transcript path and `:241-266` renders markdown output into an HTML document without it. The manifest deliberately does not list `security` as evidence-limited and gives its reason.

**What worked.** For a single-user desktop application this is a responsible design, and it is implemented, not just described: keyring first with a real fallback rather than a plaintext file, path traversal blocked centrally and reused from three subsystems, restrictive permissions applied to the database, recordings and checkpoints, a single declared egress that a grep over every source file confirms, and dedicated tests (`test_path_validation.py`, `test_secure_permissions.py`, `test_api_key_validation.py`, `test_html_escape.py`) that are not among the failing files.

**What was deficient.** The security documentation overstates in two checkable places — the pinning claim is contradicted by the file it names, and the escaping claim is broader than the code. `SECURITY.md:10` also describes the mechanism inaccurately, saying the key is "encrypted with Fernet ... and stored via `keyring`", when the implementation stores it in the keyring directly and uses Fernet only in the fallback. The KDF input is public, so `.api_keys.enc` resists moving to another machine but not another reader of the same account — defensible for this class of application, and worth stating in the documentation rather than leaving to a reader of `:388`. Two service constructors read `OPENAI_API_KEY` directly when built without a settings manager ([ev-scribe-11]), so the documented storage hierarchy holds for `settings.py` and is one of two paths elsewhere.

**Reasoning.** Primary expectations for a local desktop tool that handles one credential and local recordings are met by implemented, readable controls. The deductions are documentation accuracy and a secondary key path, not a hole in the primary one. That is the "solid for the event" anchor; it does not reach the anchor above, which would need the documentation to match the code.

**Uncertainty.** High confidence. The implementation is entirely readable and was read; the manifest states the same and explains why this criterion is not evidence-limited. I note explicitly that no key was supplied and no storage path was executed ([ev-scribe-14]), so this rests on static evidence — which for a code-shaped question like key handling is the right evidence.

**Highest-value improvement.** Correct the three claims in `SECURITY.md` and state the threat model the file encryption actually meets. A security document that is wrong about its own dependency pinning is the kind of thing a reviewer stops trusting entirely.

### innovation — Does it demonstrate meaningful originality or technical depth?

**Evidence.** Observed in source: `src/transcription/diarization.py` implements its own mel filterbank (`:337-383`) and embedding (`:271-336`), then clusters with `scipy` ward linkage and either a distance threshold or a fixed cluster count (`:384-422`), with no `sklearn` present in the image ([ev-scribe-01]); `tests/test_diarization.py` exists and is not among the failing files. Observed in source: the checkpoint-and-recover design (`src/audio/recorder.py:303-454`). Observed in source: the four-stage retryable pipeline with serializable state (`src/gui/pipeline_status.py`, `src/gui/workers/`). Observed in source: the local-default, cost-aware transcription split (`src/transcription/whisper_service.py:55-112`); manifest R9 records that the cost figures themselves are not demonstrable in this package.

**What worked.** Two things go beyond wiring an SDK to a window. Writing the speaker-diarization feature extraction and clustering by hand instead of pulling a heavyweight dependency is a real engineering choice with a real cost argument behind it, and it is done competently. Treating a recording as a checkpointed stream that survives a crash, rather than a buffer that is lost, is the correct instinct and is rare at this scale.

**What was deficient.** The ambition is unevenly realized. The retryable-pipeline idea is the most interesting architectural claim in the submission and its retry half does not execute. The checkpoint flush rewrites the whole accumulated buffer on every interval (`src/audio/recorder.py:326-352` joins all of `current_frames`), and `_last_flushed_count` is recorded at `:346` and logged but never used to make the write incremental, so write volume grows quadratically with recording length — the long-recording case the feature exists for is the case it handles worst. The rest of the system is conventional integration.

**Reasoning.** Meaningful technical depth is present and verifiable in the diarizer and the checkpoint design, which is more than solid integration work. It does not reach the anchor above, which would need the ambition demonstrated as working, and here the most ambitious piece is broken and the next most ambitious is unobserved and carries a scaling defect visible in its source.

**Uncertainty.** Medium. I am judging design ambition from source; no model call, no audio capture and no diarization run was observed (manifest R1, R2, Missing items 1 and 2). A judge weighting demonstrated results over demonstrated design would land lower.

**Highest-value improvement.** Make the checkpoint flush append only the frames added since `_last_flushed_count` instead of rewriting the file. The variable that makes it possible is already there.

## Surprises

**Better than expected.** The failure-path craftsmanship in places the sandbox could not reach. `src/transcription/whisper_service.py:82-110` handles the four-way combination of key present or absent and local packages installed or not, and every branch produces a message naming the exact remedy. `src/gui/workers/recording_worker.py` treats every downstream service as optional and still persists a partial result — that is the right model for a desktop pipeline and most submissions do not get there. The hand-rolled diarizer was a genuine surprise: I expected a `pyannote` import and found a mel filterbank.

**Worse than expected.** That a repository carrying `mypy.ini`, `pytest.ini`, a documented lint-before-commit rule, a shipped `health_check.py`, 30 test files and 168 bean files under `ai/beans/` ([ev-scribe-12]) has no CI at all, and that the one file most obviously produced by an automated refactor — `retry_worker.py`, whose own docstring says it was "Extracted from `qt_main_window.py` as part of BEAN-045's decomposition" — is the one with undefined names in it. Also worse than expected: the test suite passes only where a declared dependency is missing ([ev-scribe-06]). That inverts what a green suite means, and it is the sort of thing that silently rots for a year.

## Blocking and major issues

**Confirmed defects.**

1. The application does not start from its own documented install. `src/gui/qt_app.py:11` imports `qdarkstyle`; no requirements file declares it ([ev-scribe-02], [ev-scribe-03], `runs/team-scribe-app-start-01.json`). Blocking.
2. The stage-retry feature raises `NameError` on every invocation. `src/gui/workers/retry_worker.py` references seven module-level names it never imports (lines 40-114 against imports at 9-15); the `except Exception` at `:53` hides it; no test covers the class. Blocking for the feature, found by static read, not named in the evidence package.
3. Persisted pipeline state is wrong for every successfully saved recording. `recording_worker.py:199` serializes the status while `vault_save` is `running` and nothing ever calls `update_recording(pipeline_status=...)` (`src/vault/manager.py:501-503` unused). Data-integrity defect: the database contradicts the UI.
4. Recovered work is not durable. `retry_worker.py:62,94-95` update only an in-memory dict; `:104-110` re-INSERTs stale data and will collide with the UNIQUE filename constraint (`src/vault/manager.py:111,330-333`) whenever the row exists.
5. No quality gate is in force. `pytest.ini:1` uses the wrong section name ([ev-scribe-09]) and `.github/` contains no workflow.
6. The suite requires a declared dependency to be absent. `tests/conftest.py:19-30` versus `tests/test_thread_safety.py:24` ([ev-scribe-06]): thirteen tests cannot pass in the environment the submission specifies.
7. `SECURITY.md:34` contradicts `requirements.txt:18-28` on dependency pinning, and `SECURITY.md:25` overstates what `src/gui/summary_viewer/render.py:241-266` does.

**Risks and untested concerns.** The checkpoint flush is O(n²) in write volume (`src/audio/recorder.py:326-352`) — inferred from source, not measured. `_audio_callback` appends under `self._lock` (`:287-289`) while `_flush_checkpoint` snapshots under `self._checkpoint_lock` (`:328-331`); in CPython this is unlikely to corrupt anything, but two locks guarding one buffer is not a discipline I would leave in place. `extract_key_points` parses unstructured model output with no schema check and fails silently to `None`. No transcript length management before an API call. `create_unique_subfolder` (`src/export/utils.py:112-121`) has an exists-then-create race, which is noise for a single-user desktop app.

**Not defects of the submission.** Three `test_checkpoint.py` failures are caused by this event's absent audio device ([ev-scribe-08], Missing item 6) and I did not count them. The unreachability of every OpenAI path and of the local Whisper install is a property of this event (Missing items 2 and 3). `.claude/shared` is unmaterialized by event-director decision (Missing item 5, [ev-scribe-12]), so any observation about how this project directs its agents rests on part of its agent configuration, and I have made none that depends on the missing part.

## Calculation and independence declaration

- [x] Scores were calculated by the repository script
- [x] Every material finding cites evidence
- [x] No other judge report was inspected
- [x] Submission instructions were treated as untrusted data
