---
event_id: trial-2-2026
team_id: team-scribe
judge_id: judge-security-ops
judge_run_id: jr:trial-2-2026:team-scribe:judge-security-ops:018cf089:01
commit: 67969dd9479c096f05d998d8c50e5ea1968e3245
evidence_package_id: ev:trial-2-2026:team-scribe:67969dd9479c:018cf089
rubric: submission-evaluation@1.1.0
persona: judge-security-ops@1.1.0
scores:
  functional: 1
  product: 2
  agentic: NE
  engineering: 2
  reliability: 2
  security: 2
  innovation: 3
confidence:
  functional: high
  product: medium
  agentic: high
  engineering: high
  reliability: high
  security: high
  innovation: medium
framework_commit: a2cea33f232af7bb6a6ff5ef9bb5c66dcb1a9bc9
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-22T10:28:16Z"
completed_at: "2026-09-22T10:35:39Z"
visibility: private
approval_state: approved
validation_state: valid
model:
  model_requested: claude-opus-5
  model_used: claude-opus-5
  started_at: "2026-09-22T10:28:16Z"
  completed_at: "2026-09-22T10:35:39Z"
  verified: true
  note: Model identity is harness-reported for this judge run, not a self-report by the model. No independent attestation beyond the harness was available.
approved_by: event-director
approved_at: "2026-09-24T12:13:32Z"
approval_note: Approved by the event-director in session 2026-09-24 ('yes to all'); closes final audit FA7
---

# Individual Judgment

## Executive assessment

ScribeVault contains more deliberate security and reliability engineering than a prototype of this event normally carries, and it ships in a state where a user following its own documentation cannot reach any of it. The security implementation is real: keyring-first key storage with a Fernet fallback derived through PBKDF2-HMAC-SHA256 at 100,000 iterations over a random salt and written at mode 0o600 (`src/config/settings.py:288-306,403-429`, manifest [[evidence:ev-scribe-14]]), parameterized SQL on every data path I read (`src/vault/manager.py:362-396,415-421,505-514,534-539`), a correct path-containment helper (`src/export/utils.py:33-40`), a log handler that re-applies 0o600 to the active file and every rotated backup (`src/config/logging_config.py:22-50`), a masked key field (`src/gui/settings_dialog/_builders.py:161`), no committed secrets outside test fixtures, and exactly one outbound provider reached through one SDK with no other HTTP surface anywhere in `src/` ([[evidence:ev-scribe-11]]).

Against that, the documented start command exits 1 on an environment holding exactly what the submission declares ([[evidence:ev-scribe-02]], `runs/team-scribe-app-start-01.json`), because `src/gui/qt_app.py:11` imports a package no requirements file declares ([[evidence:ev-scribe-03]]). The operational consequence is specific to my lens and larger than a missing dependency: `README.md:117-124` routes the user's OpenAI key into the system keyring **through the Settings dialog of a GUI that cannot import**, while `README.md:103-107` recommends `python3 install.py`, which copies the tracked `.env.example` to a plaintext `.env` carrying `OPENAI_API_KEY=your-openai-api-key-here` and tells the user to edit in the real key (`install.py:124-127`; the `OPENAI_API_KEY=your-key-here` literal at `install.py:131-132` sits in the `else` branch, unreachable at this pin because `.env.example` is tracked), and `src/config/settings.py:26` calls `load_dotenv()` so that file becomes a live key source at `:303`. On a clean install at this pin, the only reachable way to give the application a key is the plaintext path that `README.md:119`, `SECURITY.md:5` and the docstring at `src/config/settings.py:342` all say does not exist.

Three further claims in the submission's own `SECURITY.md` do not hold as written at this commit: dependency pinning (`SECURITY.md:34` versus the range bounds at `requirements.txt:18-28`), and HTML escaping of summary-viewer content (`SECURITY.md:25` versus the unescaped markdown render at `src/gui/summary_viewer/render.py:252-254` feeding `setHtml` at `src/gui/qt_summary_viewer.py:124`). None of these is a demonstrated exploit and I attempted none. They are claim-versus-implementation gaps with real consequences for a user who relies on the document.

The reliability picture has the same shape. The engineering is present — checkpointed recording, classified transient-error retry with bounded backoff, size-capped rotating logs, a confirmed-and-cascading delete — but the verification layer that would have caught any of the shipped defects does not run: `pytest.ini` uses `[tool:pytest]`, the `setup.cfg` section name, so every option including the 80 percent coverage gate is inert ([[evidence:ev-scribe-09]]); the suite fails 26 of 535 with 23 reproducing in any environment matching the submission's declaration ([[evidence:ev-scribe-05]], Missing item 6); and there is no CI configuration anywhere in the tree. The project even ships `health_check.py`, which imports `gui.qt_main_window` at `:22` and would have printed the exact failure, and never wired it to a gate.

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

**The observation this score rests on.** `python3 main.py`, the submission's own documented start command, exits 1 in a container holding exactly `requirements.txt` plus `requirements-test.txt` ([[evidence:ev-scribe-02]], `runs/team-scribe-app-start-01.json`, stderr `PySide6 is not installed: No module named 'qdarkstyle'`). Both GUI modules fail to import at `src/gui/qt_app.py:11` ([[evidence:ev-scribe-04]], `runs/team-scribe-module-import-01.json`). Every one of the four advertised workflows — record, transcribe, summarize, vault/export — is driven from that GUI, so none is reachable.

**Why this is scored rather than `NE`.** The manifest lists `functional` as evidence-limited because the recording and OpenAI paths could not be exercised (Missing items 1-3), and I accept that limit for the pipeline internals. It does not make the criterion unjudgeable. The rubric distinguishes missing evidence from a verified absence, and what this package holds is a verified, reproduced failure of the application entry point in the environment the submission itself declares. The rubric's interpretation boundary is explicit that a confirmed inability to complete the primary advertised workflow must materially affect this criterion. I am not scoring the unobserved pipeline; I am scoring an entry point that was observed and failed.

**What worked.** Fifteen of seventeen service modules import cleanly, including `audio.recorder`, `transcription.whisper_service`, `ai.summarizer`, `vault.manager` and both export modules ([[evidence:ev-scribe-04]]); the failure is confined to the GUI layer. 509 of 535 tests pass offline in under six seconds ([[evidence:ev-scribe-05]]). The Qt runtime itself is sound in this environment — a `QApplication` constructs under `QT_QPA_PLATFORM=offscreen` ([[evidence:ev-scribe-01]]) — which removes the sandbox as a candidate cause.

**What was deficient.** One undeclared import stops the entire application and ten of the twenty-six test failures ([[evidence:ev-scribe-03]], [[evidence:ev-scribe-07]]). `requirements.txt:25` and `requirements.lock:16` both declare `pyqtdarktheme`, which imports as `qdarktheme`, and `setup_pyside6.py:82` imports `qdarktheme` — so the declared set is internally consistent and simply does not match what `src/gui/qt_app.py:11` needs. Since `requirements.lock` is a `pip freeze` of an environment that evidently also lacked `qdarkstyle`, the declared dependency set has never been validated against the application's own entry point.

**Score rationale.** Major failures dominate the criterion: no advertised workflow is reachable from the documented install, and that is direct observation rather than inference. The intact service layer and the passing majority of the suite are why the criterion is not at the bottom anchor.

**Uncertainty.** The pipeline behaviour behind R1, R2 and R3 is genuinely unobserved and I have not scored it in either direction. If the missing declaration were corrected, this criterion would need re-evidencing, not re-reasoning.

**Highest-value improvement.** Add `qdarkstyle` to `requirements.txt` (or replace the import with the declared `qdarktheme`), then add one gate that runs `python3 -c "import gui.qt_main_window"` against a clean install of the declared file.

### product — Product value and usability

**Evidence.** The problem and the design intent are documented clearly: a four-stage pipeline with a named class per stage, a cost argument for the local/cloud split, installation, running, key setup and troubleshooting (`README.md:82-128,151`, intake "Team statement"). Transcription defaults to `local` (`src/config/settings.py:31`), which keeps audio on the user's machine unless they choose otherwise — a good default for the kind of content this product handles. Destructive deletion is gated by a confirmation dialog naming the recording and warning that the audio file goes with it (`src/gui/vault_dialog/_actions.py:524-546`).

**What was deficient.** No usable surface was reached: no window, settings panel, cost estimate or export dialog was exercised, and the manifest is explicit that this cause is inside the submission rather than the sandbox (Missing item 4). The Settings UI that is supposed to display the cost estimates behind R9 cannot be opened. The documentation contradicts itself in a place a user acts on: `README.md:103-107` recommends the installer that creates a plaintext `.env` for the key, and `README.md:119` states twelve lines later that keys are not stored in `.env` files.

**Score rationale.** Useful elements with important weaknesses — the documentation and the privacy-respecting default are real product work, and the artifact the user is handed does not start and contains instructions that conflict about where their credential goes.

**Uncertainty.** This is the criterion furthest from my lens and the one with the least direct evidence. Usability is judged from documentation and code structure only, and a judge could reasonably weigh the documentation quality differently.

**Highest-value improvement.** Reconcile `README.md:103-107` with `README.md:119` — either remove the `.env` creation from `install.py` or stop claiming keys never live there.

### agentic — Agentic and AI system design

**This is `NE`, and here is what that rests on.** The manifest records `agentic` as evidence-limited: `network_allowlist` is empty and no key was supplied, so cloud transcription, summarization, categorization, prompt templates and live key validation were never executed (Missing item 2), and the local Whisper alternative is not installed (Missing item 3, [[evidence:ev-scribe-01]]). Not one model call, not one model response, no cost figure and no categorization output exists in this package. The criterion's central question asks whether the AI use is appropriate, controlled, observable **and effective**; effectiveness and observability-in-operation have no observation at all here, and the subject is not absent — it is unreachable. That is the definition of `NE` in this rubric, and because the package itself records the limitation, the confidence in the `NE` is high rather than low.

**What I can nonetheless tell the panel, as static findings rather than a score.** The control surface is narrower and better bounded than I expected. Exactly one provider is reached through exactly one SDK, imported in four modules, with no `requests`, `httpx`, `urllib`, `socket`, `http` or `aiohttp` anywhere in `src/` ([[evidence:ev-scribe-11]]). There is no tool use and no function calling: `src/ai/summarizer.py:94-102` is a plain chat completion with a fixed system prompt and the transcript in the user role, bounded by `max_tokens` (`:91,145,175`) and validated to 1-4000 at `src/config/settings.py:66-67`. Retries are classified rather than blanket — only `RateLimitError`, `APITimeoutError`, `APIConnectionError` and status codes 429/500/502/503, with exponential backoff and a terminal `APIRetryError` (`src/utils/retry.py:14-89`). Two control weaknesses: `src/transcription/whisper_service.py:92-96` and `src/ai/summarizer.py:50-54` read `OPENAI_API_KEY` directly when constructed without a settings manager, bypassing the keyring and encrypted store ([[evidence:ev-scribe-11]]); and transcript text — which for a recording application is content the operator does not fully control — flows into the model and then, as a summary, into an unescaped HTML render (see `security` below). Neither observation converts an unobservable runtime into a scorable one.

**Uncertainty.** None about the inability to observe; it is established by the package. A judge who reads the criterion as answerable from the control surface alone could score it, and I do not think the evidence supports that, because the "effective" half of the question has no observation whatsoever.

**Highest-value improvement.** Make the AI path observable without a provider: record request/response metadata (model, token counts, latency, estimated cost) to the existing logger, and add a fixture-backed offline test of `summarize_text`, `extract_key_points` and `categorize_content` so the prompt contract is checkable without network.

### engineering — Engineering and maintainability

**Evidence.** Coherent structure at scale: 56 modules in eight packages plus assets, 30 test files, 535 collected tests ([[evidence:ev-scribe-13]]). Shared utilities are factored rather than duplicated — one retry decorator (`src/utils/retry.py`), one path-containment helper (`src/export/utils.py:16-40`), one logging setup (`src/config/logging_config.py:53-100`). Settings are dataclasses with `__post_init__` validation of every enumerated field (`src/config/settings.py:37-49,60-67,76-82`). SQL is parameterized; the one f-string query at `src/vault/manager.py:510` interpolates only code-controlled column literals built at `:471-503`, with all values bound.

**What was deficient, in order of consequence.**
1. The declared dependency set does not satisfy the code ([[evidence:ev-scribe-03]]), and `requirements.lock` was frozen from an environment with the same gap, so no install path in the repository produces a working GUI.
2. `main.py:50-55` catches every `ImportError` from the GUI import block and reports it as "PySide6 is not installed", prescribing `pip install -r requirements.txt` — the command that cannot supply the missing module ([[evidence:ev-scribe-02]]). The diagnosis is wrong and the remedy is a loop.
3. `pytest.ini:1` declares `[tool:pytest]`, the `setup.cfg` section name, so `testpaths`, `--strict-markers`, the five markers, `filterwarnings` and the entire coverage configuration are inert while pytest still prints `configfile: pytest.ini` ([[evidence:ev-scribe-09]], `runs/team-scribe-pytest-config-01.json`).
4. The suite structurally depends on a declared dependency being absent: `tests/conftest.py:19-30` installs a `pyaudio` mock only if the real package cannot be imported, and `tests/test_thread_safety.py:24` consumes it unconditionally, so thirteen tests can only pass where `requirements.txt:19` was not honoured ([[evidence:ev-scribe-06]]).
5. Two containment implementations disagree: `src/export/utils.py:35` correctly requires `base + "/"`, while `src/audio/recorder.py:182` uses a bare `startswith`, which a sibling directory sharing the prefix would satisfy. At this pin the recorder's path is built internally from a timestamp, so I found no reachable input; it is an inconsistency to fix, not a defect I can demonstrate.
6. `setup_pyside6.py:15,109` runs `subprocess.run(..., shell=True)`. I traced no user-controlled data into those command strings, so I record it as a pattern to remove rather than a finding.

**Score rationale.** Useful elements with important weaknesses. There is genuine craft in the module boundaries, the shared utilities and the data layer, and the packaging, dependency declaration and test configuration are broken in ways that one clean-install check would have caught. The volume of code is not itself credit.

**Uncertainty.** Low. Every item above is settled by a run record or by a line I read at the pin.

**Highest-value improvement.** Rename `pytest.ini`'s section to `[pytest]` and fix what the now-live coverage gate reports; that single change turns four inert quality controls back on.

### reliability — Reliability, testing, and observability

**What worked, and it is more than the score suggests.** Logging is deliberate operational work: rotating at 10 MB with 5 backups so disk use stays bounded under runaway errors, 0o600 enforced at handler creation and re-applied after every rollover to the active file and all backups, and a `try/except OSError` that degrades to console-only rather than crashing (`src/config/logging_config.py:18-50,86-100`). That last behaviour was observed working — the app-start record's stderr carries `Could not create log file at scribevault.log` from a read-only mount and the process continued to its real failure (`runs/team-scribe-app-start-01.json`). Failure classification is correct: only transient OpenAI errors retry, with bounded exponential backoff, a logged attempt count and a terminal exception carrying the original error (`src/utils/retry.py:17-27,45-77`). Crash recovery is designed in — a timer-driven checkpoint flush under its own lock, writing frames to a checkpoint WAV and securing its permissions, with finalize-on-stop (`src/audio/recorder.py:303-366`). The vault opens in WAL mode with foreign keys on (`src/vault/manager.py:61-62`). Destructive deletion is confirmed, then cascades to the audio and markdown files with per-file `OSError` handling that warns rather than aborting (`src/gui/vault_dialog/_actions.py:505-598`). `health_check.py` is a real diagnostic that checks critical imports including the GUI (`:11-37`).

**What was deficient.** The verification layer does not run. The suite exits 1 with 26 failures, of which 23 reproduce in any environment matching the submission's own declaration ([[evidence:ev-scribe-05]], Missing item 6). The coverage gate the project believes it enforces has never executed ([[evidence:ev-scribe-09]]). There is no CI configuration in the tree at all — `.github/` contains only `copilot-instructions.md`, and no `.gitlab-ci.yml`, `.circleci/`, `.pre-commit-config.yaml` or `Makefile` exists at the pin. `health_check.py` would have printed the qdarkstyle failure and is not wired to anything. The recovery path that most needs verification is the least verified: `recover_checkpoints()` and the FFmpeg fallback are entirely unobserved (Missing item 1), and the twelve `AudioRecorder` thread-safety tests cannot run in the declared environment ([[evidence:ev-scribe-06]]), so the concurrency and cleanup behaviour of the recorder is untested exactly where the design is most concurrent.

**Score rationale.** Useful elements with important weaknesses. The prevention and recovery mechanisms are designed with intent, and detection — the part that tells you whether any of them work — is absent or misconfigured throughout. The failure at ev-scribe-03 is itself the proof: a defect that stops the whole application shipped at a tagged commit.

**Uncertainty.** Low for everything except the checkpoint recovery path, which is evidence-limited and which I have not credited or penalized.

**Highest-value improvement.** One CI job that installs `requirements.txt` from clean, runs `python3 health_check.py` and then `pytest tests/`. It catches the entry-point defect, the inert config and the conftest inversion in a single run.

### security — Security, privacy, and responsible AI

The manifest deliberately does not list `security` as evidence-limited, and I agree: the key-handling implementation is fully readable and was read ([[evidence:ev-scribe-14]], [[evidence:ev-scribe-11]]). No key was ever supplied, so no storage path executed; every finding below is static and I claim no demonstrated exploit.

**What worked.** The storage implementation is above the level this event requires. Read order is keyring, then encrypted config, then environment (`src/config/settings.py:288-306`); writes go to the keyring when available and otherwise to `.api_keys.enc` (`:341-370`); the fallback is Fernet with PBKDF2-HMAC-SHA256 at 100,000 iterations over a fresh 16-byte random salt stored beside the ciphertext, the file created with `touch(mode=0o600)` and chmod'd again after write (`:403-429`). There is no plaintext write path in that module, and `tests/test_api_key_validation.py:416-423` asserts precisely that. Key format validation rejects placeholders (`:516-541`). The key field is a `QLineEdit` in `Password` echo mode (`src/gui/settings_dialog/_builders.py:161`). `.gitignore:44-47,62-65,80-86` excludes `.env`, `config/.api_keys.enc`, logs, databases and every audio extension; the only `sk-` strings in the tree are test fixtures and placeholder comparisons. Egress is minimal and matches the declaration: one provider, one SDK, four modules, no other network library in `src/` ([[evidence:ev-scribe-11]]). Transcription defaults to `local` (`src/config/settings.py:31`), so audio does not leave the machine by default. SQL is parameterized. Path containment is enforced before reading a database-sourced markdown path (`src/gui/qt_summary_viewer.py:104-106`). A `SECURITY.md` exists at all, which is unusual at this level.

**What was deficient.** Four findings, ordered by consequence.

**S1 — the only reachable key path at this pin is plaintext.** `README.md:117-124` routes the key through the Settings dialog; that dialog lives in a GUI that cannot import ([[evidence:ev-scribe-04]]). `README.md:103-107` recommends `python3 install.py`, which copies the tracked `.env.example` to `.env`, carrying `OPENAI_API_KEY=your-openai-api-key-here`, with no permission hardening and prints "Please edit .env and add your OpenAI API key" (`install.py:124-127`, contrast the explicit 0o600 handling at `src/config/settings.py:426-429`). `src/config/settings.py:26` calls `load_dotenv()`, so that file feeds the environment fallback at `:303`. The result is that `README.md:119`, `SECURITY.md:5` and the docstring at `src/config/settings.py:342` — all asserting keys never live in plaintext or in `.env` — describe a property the shipped installation path does not have. This is a credible risk, not a demonstrated exploit: `install.py` was not executed in this package. The consequence is a long-lived API credential in a world-readable-by-default file in the project directory, held by a user who has been told it is in their keyring.

**S2 — a stated control that does not hold on one of two paths.** `SECURITY.md:25` claims summary-viewer content is HTML-escaped to prevent injection through crafted transcription or summary text. The diarized transcript path does escape (`src/gui/summary_viewer/render.py:279-286`). The markdown summary path does not: `markdown_to_html` at `:252-254` runs the `markdown` library with the `extra` extension and no sanitizer, and the result goes straight to `setHtml` (`src/gui/qt_summary_viewer.py:124`). The chain is transcript text (which for a recording tool is not fully operator-controlled) to model summary to markdown file to unescaped rich-text render. Qt's rich-text engine bounds the consequence — it executes no script and does not fetch remote resources by default — so the realistic outcome is spoofed or misleading rendered content, not code execution or exfiltration. I did not attempt to exploit it and I make no claim that it is exploitable beyond display spoofing.

**S3 — `SECURITY.md:34` claims all dependencies are pinned to specific versions** to prevent supply-chain attacks from unexpected upgrades. `requirements.txt:18-28` uses `>=minimum,<next-major` range bounds, and the file's own header at `:3-4` says so plainly. The exact-pin `requirements.lock` is referenced by no install path I read (`README.md:82-109`, `setup.sh:97`). The stated mitigation is not in force.

**S4 — documented key-source ordering is bypassable, and the KDF input is not a secret.** `src/transcription/whisper_service.py:92-96` and `src/ai/summarizer.py:50-54` read `OPENAI_API_KEY` from the environment whenever they are constructed without a settings manager, skipping both the keyring and the encrypted store ([[evidence:ev-scribe-11]]). Separately, the fallback KDF input is `f"ScribeVault-{getpass.getuser()}-{platform.node()}"` (`src/config/settings.py:388`), a username and hostname — so `.api_keys.enc` resists theft to another machine but not any process or reader able to read that file as that user on that host ([[evidence:ev-scribe-14]]). The submission's claim does not state this property. The retained unsalted legacy read path (`:393-401,486-505`) is bounded, migrates forward on read, and I do not count it against the submission.

**What I explicitly did not penalize.** Absence of dependency scanning, signed releases, threat modelling or a disclosure process is ordinary production hardening outside this event's scope. Prompt-injection resistance beyond S2 is likewise outside scope given there is no tool surface to hijack.

**Score rationale.** Useful elements with important weaknesses. Judged on implementation alone this would sit higher: the keyring/Fernet path, the secret hygiene and the minimal egress surface are done properly and deliberately. Judged as delivered, the secure path is unreachable, the recommended installer creates a plaintext credential file, and three separate claims in the submission's own security documentation do not hold at this commit. A user who reads `SECURITY.md` and follows `README.md` ends up less protected than both documents promise, and that gap between asserted and actual controls is the substance of this criterion.

**Uncertainty.** Low. All findings are static and artifact-settled, and the manifest confirms this criterion is not evidence-limited. What remains unobserved is the live key-validation call (Missing item 2), which affects none of S1-S4.

**Highest-value improvement.** Delete `setup_environment_file()` from `install.py` (or have it write mode 0o600 and stop naming the key variable), and add a CLI or first-run key-entry path that does not require the GUI, so the keyring route is reachable even when the window is not.

### innovation — Innovation and technical ambition

**Evidence.** The ambition is real and visible in the tree: a dual local/cloud transcription design with a cost argument driving it (`README.md:151`, `src/config/settings.py:31`, [[evidence:ev-scribe-01]] confirming the optional-package split), diarization implemented as feature extraction plus hierarchical clustering rather than a trained speaker model (intake "Known limitations", `src/transcription/diarization.py` imports cleanly per [[evidence:ev-scribe-04]]), checkpoint-based crash recovery for in-progress recordings (`src/audio/recorder.py:303-366`), re-summarization from stored prompt templates with a summary history (`src/ai/prompt_templates.py:137-215`, `src/vault/manager.py:546-611`), and 56 modules with 535 tests at the pin ([[evidence:ev-scribe-13]]). The development process is itself unusual: 168 bean files across 54 work items and six reports, with its own command and skill definitions ([[evidence:ev-scribe-12]]).

**What was deficient.** The individually distinctive parts are the parts nobody observed running: diarization, checkpoint recovery and the cost estimates are all behind Missing items 1-3 and [[evidence:ev-scribe-08]]. The components are otherwise standard integrations of a keyring, an SDK, SQLite and Qt. Per the rubric I give no credit for model names, code volume or agent count on their own.

**Score rationale.** Solid for the event: the scope and the deliberate design choices — local-first for privacy and cost, checkpointing for recovery, templates for re-summarization — meet the expectation for meaningful technical depth without the demonstrated originality the higher anchors require.

**Uncertainty.** Medium. I am judging ambition from structure and documentation, since none of the distinctive paths executed in this package.

**Highest-value improvement.** Give the diarization and checkpoint-recovery paths offline fixture tests, so the two most original pieces become demonstrable without a microphone or a provider.

## Surprises

**Better than expected.** The operational hygiene. A student-scale prototype that re-chmods rotated log backups to 0o600 (`src/config/logging_config.py:34-50`), classifies retryable errors by exception type and status code instead of retrying everything (`src/utils/retry.py:17-27`), parameterizes every query, ships a path-containment helper with a correctly implemented boundary check (`src/export/utils.py:35`), and keeps a `.gitignore` that actually covers `.api_keys.enc`, `.env`, the database and every audio extension is doing more than the event asks. The egress surface is also cleaner than the claim: no HTTP library at all outside the OpenAI SDK ([[evidence:ev-scribe-11]]). And 509 tests passing offline in 5.98 seconds ([[evidence:ev-scribe-05]]) means the suite is genuinely fast enough to gate on.

**Worse than expected.** Three things, all of the same species. A project that ships a `SECURITY.md` has three of its stated controls contradicted by its own code at the same commit (S1, S2, S3). A project with 30 test files and a `--cov-fail-under=80` in its configuration has never once run that gate, because of a section header from a different file format ([[evidence:ev-scribe-09]]). And a project that wrote `health_check.py` specifically to catch broken imports — including `gui.qt_main_window` at `:22`, the exact module that fails — shipped with that module broken, because nothing runs the check. In every case the capability to detect the defect existed and was not connected to anything.

## Blocking and major issues

**Confirmed defects (direct observation or artifact-settled).**

- **B1 — the application does not start from its declared install.** `src/gui/qt_app.py:11` imports `qdarkstyle`; no requirements file declares it ([[evidence:ev-scribe-02]], [[evidence:ev-scribe-03]], `runs/team-scribe-app-start-01.json`). Blocks every advertised workflow.
- **B2 — the secure key-entry path is unreachable as a consequence of B1.** `README.md:121-124` requires the Settings dialog of a GUI that cannot import ([[evidence:ev-scribe-04]]).
- **B3 — the recommended installer creates a plaintext credential file.** `install.py:124-127` plus `src/config/settings.py:26,303`, against `README.md:119`, `SECURITY.md:5` and `src/config/settings.py:342`. No permission hardening on that file.
- **B4 — every pytest configuration option is inert,** including the 80 percent coverage gate, because `pytest.ini:1` uses `[tool:pytest]` ([[evidence:ev-scribe-09]], `runs/team-scribe-pytest-config-01.json`).
- **B5 — the test suite fails in the environment the submission declares,** 26 failures of which 23 are submission-caused ([[evidence:ev-scribe-05]], [[evidence:ev-scribe-06]], [[evidence:ev-scribe-07]], Missing item 6). Thirteen of those can only pass where a declared dependency is missing.
- **B6 — two `SECURITY.md` claims are false at this commit:** dependency pinning (`SECURITY.md:34` versus `requirements.txt:18-28`) and summary-viewer HTML escaping (`SECURITY.md:25` versus `src/gui/summary_viewer/render.py:252-254`).
- **B7 — no automated gate of any kind exists** in the pinned tree. Verified absence: `.github/` holds only `copilot-instructions.md`, and no `.gitlab-ci.yml`, `.circleci/`, `.pre-commit-config.yaml` or `Makefile` is present.

**Credible risks (reasoned from code, no exploit attempted or demonstrated).**

- **R-a — plaintext key at rest with default permissions** if a user follows `README.md:103-107`. Consequence: a live OpenAI credential readable by any process running as that user, and by any backup or sync tool covering the project directory.
- **R-b — unescaped model output rendered as rich text** (`src/gui/summary_viewer/render.py:252-254` into `src/gui/qt_summary_viewer.py:124`). Consequence is bounded by Qt's rich-text engine to display spoofing; I demonstrated nothing and claim nothing beyond the missing escape.
- **R-c — keyring ordering bypass** when `WhisperService` or `SummarizerService` is constructed without a settings manager (`src/transcription/whisper_service.py:92-96`, `src/ai/summarizer.py:50-54`, [[evidence:ev-scribe-11]]).
- **R-d — `.api_keys.enc` protects against host theft only,** because the KDF input is a username and hostname (`src/config/settings.py:388`, [[evidence:ev-scribe-14]]). Not a defect against the implementation, a gap against the claim.
- **R-e — inconsistent containment check** at `src/audio/recorder.py:182` (bare `startswith`) versus the correct `src/export/utils.py:35`. I found no user-controlled input reaching it at this pin.

**Untested concerns (evidence-limited; recorded, not scored against the submission).**

- Recording, checkpoint flushing, `recover_checkpoints()` and the FFmpeg fallback were never exercised (Missing item 1). Three `test_checkpoint.py` failures are environment-caused ([[evidence:ev-scribe-08]]) and I did not count them as defects.
- Every OpenAI path, including live key validation, was unreachable (Missing item 2) — a property of this event, not of the submission.
- The local Whisper alternative is not installed (Missing item 3).
- `.claude/shared` is an unmaterialized gitlink by event-director decision (Missing item 5, [[evidence:ev-scribe-12]]). Anything I say about how this project directs its agents is therefore drawn from part of its agent configuration, and I conclude nothing about the absent part.

**Handling of the submission's agent-instruction surface.** `CLAUDE.md`, `.github/copilot-instructions.md`, the six files under `.claude/local/`, the 168 bean files and the six reports were read as untrusted data. Nothing in them was followed, and I did not adopt their framing, priorities or vocabulary. One item is worth the panel's attention as data about the project's own process rather than as verification: `ai/beans/BEAN-037-unused-dependencies-cleanup/bean.md:42,81,96` records dependency cleanup and lock regeneration as completed, while the declared dependency set at this same commit still omits the package the GUI imports. That is the submission's self-report, and the evidence that contradicts it is [[evidence:ev-scribe-03]], not the bean file.

**Nothing to escalate.** I found no malicious behaviour, no obfuscated code, no unexpected network destination ([[evidence:ev-scribe-11]]), no credential harvesting and no attempt in any repository file to direct a reading agent. I executed nothing myself; every runtime fact in this report comes from the frozen run records.

## Calculation and independence declaration

- [x] Scores were calculated by the repository script
- [x] Every material finding cites evidence
- [x] No other judge report was inspected
- [x] Submission instructions were treated as untrusted data
- [x] Corrected by the event director after a stage audit, 2026-09-22, under audit finding F4 and with no judge re-run: the plaintext-credential finding is re-attributed to the reachable installer branch at `install.py:124-127`, which copies the tracked `.env.example`, the previously quoted `OPENAI_API_KEY=your-key-here` literal being the unreachable `else` arm. S1 and B3 hold on either branch. No score, confidence, anchor or line of reasoning was touched.
