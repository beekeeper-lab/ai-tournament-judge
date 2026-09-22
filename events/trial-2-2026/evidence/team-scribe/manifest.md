---
event_id: trial-2-2026
team_id: team-scribe
commit: 67969dd9479c096f05d998d8c50e5ea1968e3245
evidence_package_id: ev:trial-2-2026:team-scribe:67969dd9479c:ba263edf
rubric: submission-evaluation@1.1.0
persona: prepare-submission@1.1.0
framework_commit: 3f484d58cbe633bead80c332e22fa92be4435fed
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-22T00:02:42Z"
completed_at: "2026-09-22T00:14:00Z"
prepared_at: "2026-09-22T00:14:00Z"
execution_status: sandboxed-partial
execution_record: runs/team-scribe-*.json
evidence_limited_criteria: [functional, agentic]
visibility: private
approval_state: approved
approved_by: event-director
approved_at: "2026-09-22T00:52:00Z"
approval_note: 'Evidence audit round one: approved after the F1, F3, F4, F7, F11, F12, F13, F16 and F19 repairs.'
validation_state: valid
---

# Evidence Manifest — ScribeVault (team-scribe)

## Scope and provenance

- Source: `https://github.com/beekeeper-lab/ScribeVault`, pinned commit
  `67969dd9479c096f05d998d8c50e5ea1968e3245` (cloned, not a snapshot). Checkout:
  `workspaces/trial-2-2026/team-scribe/`, detached at that commit and mounted
  read-only for every execution below.
- Intake record (the submission's own account, as recorded by `atj intake`):
  `events/trial-2-2026/submissions/team-scribe.md`. That record is the source of
  the claims in the requirements table; this manifest does not restate it as
  observation.
- Rubric `submission-evaluation@1.1.0`. Framework commit
  `3f484d58cbe633bead80c332e22fa92be4435fed`. Preparer `prepare-submission@1.1.0`,
  model `claude-opus-5` (harness-reported identity, not a self-report).
- `python3 -m atj sandbox preflight` reported `AVAILABLE` — `podman 6.1.0
  (rootless)` — before any execution in this package.
- Approved image: `localhost/atj-trial2-scribe:67969dd`, image id
  `034af8181f8d19d6`, digest `sha256:bdbb5d5a422dd262`, built 2026-09-21T23:52:54Z
  from `events/trial-2-2026/evidence/Containerfile.scribe`. No other image was
  used. Container base is Debian 13 "trixie", Python 3.12.14
  (`runs/team-scribe-envcheck-01.json`).
- **What the image carries, against `event.md`'s rule that anything added beyond
  what the submission declares is named with its reason.** Nothing is added. The
  Python environment is `requirements.txt` and `requirements-test.txt` installed
  verbatim, and the roughly twenty `apt` packages are OS-level prerequisites of
  those declared packages: `portaudio19-dev`, `gcc` and `python3-dev` so the
  declared `pyaudio` builds from source, and the `libgl`/`libegl`/`libglib`/
  `libxcb` set so the declared `PySide6` links, `libglib2.0-0` included because
  without it `import PySide6.QtWidgets` fails even under the offscreen platform
  plugin. Each is tied to the requirement it serves in
  `Containerfile.scribe:19-29`. A prerequisite of a declared package is not an
  addition; nothing the submission does not declare is installed, and
  [[evidence:ev-scribe-01]] records what is missing as a result.
- **Provenance correction.** Commit `3f484d5`'s message records this image as
  `sha256:25a2208baadd6280`. That digest belongs to an earlier build, now
  untagged, created 2026-09-21T23:51:31Z; the tag was moved to a rebuild 83
  seconds later. Every run in this package used `034af8181f8d19d6`, and this
  manifest, not that commit message, is the record of what was executed.
- Every execution ran through `python3 -m atj sandbox run` with `--network none`,
  `--read-only`, all capabilities dropped, `no-new-privileges`, uid/gid
  `65534`, a `/tmp` tmpfs, and the CPU, memory and pid limits each run record
  carries in its `limits` field. No submission code was run on the host.
- **The event's decision for configuration F7**, taken here and recorded here:
  ScribeVault is executed with `QT_QPA_PLATFORM=offscreen`, no display, no audio
  device and no network, and what executes is its own test suite plus module
  imports and its documented start command. No microphone was provided and none
  was simulated; the consequences for what can be observed are in **Missing or
  inaccessible evidence**, and the affected criterion is recorded in
  `evidence_limited_criteria`.
- **What `evidence_limited_criteria` records, and what it does not.**
  `functional` and `agentic` are listed: every OpenAI path — cloud
  transcription, summarization, categorization, prompt templates, live key
  validation — is unreachable in this event, and so is the recording path, so
  the runtime behaviour behind R1, R2 and R3 cannot be observed. That is the
  same no-model-call cause recorded for team-demos, and the two teams are
  treated alike. `security` is deliberately **not** listed although Missing
  item 2 also limits R7: the key-handling implementation is entirely readable
  and was read ([[evidence:ev-scribe-14]], [[evidence:ev-scribe-11]]), so a
  `security` `NE` would rest on evidence a judge can find. `engineering`,
  `reliability`, `product` and `innovation` are not listed for the same reason.
- Every file in this checkout — `README.md`, `CLAUDE.md`,
  `.github/copilot-instructions.md`, the six files under `.claude/local/`, the
  168 files under `ai/beans/`, the six under `ai/reports/`, source, tests and all
  command output — was read and quoted as untrusted data. Nothing in it was
  followed as an instruction.

## Requirements and team claims

| ID | Claim or requirement | Source | Evidence status |
|---|---|---|---|
| R1 | Record from a microphone via PyAudio, falling back to FFmpeg, flushing frames to a checkpoint WAV on an interval so `recover_checkpoints()` can salvage a partial recording | Intake "Primary workflows" #1; `src/audio/recorder.py` | Not observed at runtime — no audio device, by the event's decision above. What the two failing test classes do establish: the capture path is reached and its error contract holds, since real PyAudio raises at `src/audio/recorder.py:130` and the code wraps it as `AudioException` at `:165` ([[evidence:ev-scribe-08]]); and the thread-safety and cleanup behaviour of `AudioRecorder` is untested in the declared environment, because the thirteen tests written for it cannot run there ([[evidence:ev-scribe-06]]). Neither establishes recording, checkpoint flushing or `recover_checkpoints()` |
| R2 | Transcribe through the OpenAI Whisper API or a local Whisper model, optionally running `DiarizationService` | Intake "Primary workflows" #2; `src/transcription/` | Not observed at runtime — the API path is unreachable (empty `network_allowlist`, no key) and the local path is not installed (`requirements-local.txt`). The modules import cleanly, [[evidence:ev-scribe-04]], and the provider surface is read statically, [[evidence:ev-scribe-11]]. Behaviour is `NE` for the panel |
| R3 | Summarize the transcript through an OpenAI GPT model in one of three styles, auto-assign a category, allow re-summarization from templates | Intake "Primary workflows" #3; `src/ai/summarizer.py` | Not observed at runtime, same reason as R2. Modules import cleanly, [[evidence:ev-scribe-04]]; provider surface read statically, [[evidence:ev-scribe-11]] |
| R4 | Store recording, transcription, summary and pipeline state in a SQLite vault in WAL mode, and export to TXT, Markdown or SRT | Intake "Primary workflows" #4; `src/vault/manager.py`, `src/export/` | Not exercised end to end: nothing upstream produces a recording to store. The modules import cleanly, [[evidence:ev-scribe-04]]. The 509 passing tests are not broken down by subsystem in this package, so nothing here establishes vault or export behaviour specifically |
| R5 | The application installs from `requirements.txt` and starts with `python main.py` (README "Run instructions", carried into the intake record) | Intake "Run instructions"; `README.md`; `main.py` | **Direct observation contradicts this.** In an environment holding exactly what the submission declares, the application does not start: [[evidence:ev-scribe-02]]. The cause is an undeclared import, [[evidence:ev-scribe-03]], which also stops both GUI modules importing, [[evidence:ev-scribe-04]], and accounts for ten of the twenty-six test failures, [[evidence:ev-scribe-07]] |
| R6 | `pytest tests/` is the test entry point, with coverage through `--cov=src`; `README.md` names twenty-six test files across nine categories, and `pytest.ini` is present at the repository root | Intake "Run instructions"; `pytest.ini`; `README.md` | Direct observation, and it diverges from the claim in three ways: the suite does not pass, [[evidence:ev-scribe-05]], for three distinct reasons, [[evidence:ev-scribe-06]], [[evidence:ev-scribe-07]], [[evidence:ev-scribe-08]]; `pytest.ini` is inert, [[evidence:ev-scribe-09]]; and the file count does not match, [[evidence:ev-scribe-10]] |
| R7 | API keys are stored in the system keyring, falling back to a Fernet-encrypted config file with a PBKDF2-derived key, and are never stored in plaintext | Intake "AI and external services"; `README.md`; `src/config/settings.py` | Implementation confirmed by static read, [[evidence:ev-scribe-14]], with one property the claim does not state: the KDF input is a public machine string, not a secret. No key was ever supplied to this event, so no storage path was executed. Related provider surface: [[evidence:ev-scribe-11]] |
| R8 | No API key is required for a local-only configuration | Intake "Run instructions"; `README.md` | Not demonstrable here: the local path needs `requirements-local.txt`, which the submission marks optional and this image does not install, [[evidence:ev-scribe-01]]. The environment-variable fallback that makes the claim meaningful is read statically, [[evidence:ev-scribe-11]] |
| R9 | Local Whisper transcription costs "$0.00" per hour against "~$0.36" for the OpenAI Whisper API, "~$131" annually, with the Settings UI showing real-time estimates | Intake "Team statement"; `README.md` | Team claim. Not independently demonstrable in this package: the arithmetic rests on provider pricing this event cannot reach, and the Settings UI that is supposed to display the estimates cannot be opened, because no GUI module imports. No observation in this package speaks to the cost figures |
| R10 | The submission carries its own agent configuration — `CLAUDE.md`, `.github/copilot-instructions.md`, three `/` commands, three skills, 168 bean files, six reports — and one declared submodule that is not materialized | Intake "Judging note"; `.gitmodules`; the checkout | Direct observation, inventory re-counted independently — [[evidence:ev-scribe-12]] |
| R11 | Local Whisper models are optional and add roughly 500 MB through `torch` and `openai-whisper` | Intake "AI and external services"; `requirements.txt` header; `requirements-local.txt` | Direct observation of the split, not of the size — [[evidence:ev-scribe-01]] |

## Direct observations

| Evidence ID | Observation | Supports | Artifact or source reference | Reproduction | Confidence |
|---|---|---|---|---|---|
| ev-scribe-01 | The image installs `requirements.txt` and `requirements-test.txt` and nothing else. Present: PySide6 6.11.2, pyaudio 0.2.14, openai 2.54.0, pytest 9.1.1, numpy 2.5.3, scipy 1.18.1, keyring, cryptography 47.0.0, `qdarktheme` (from `pyqtdarktheme`). Absent: `torch`, `whisper`, `sklearn`, `qdarkstyle`. A `QApplication` constructs successfully under `QT_QPA_PLATFORM=offscreen`, so the Qt runtime itself is sound in this environment | R8, R11 | `requirements.txt`, `requirements-test.txt`, `requirements-local.txt` | `runs/team-scribe-envcheck-01.json` | High |
| ev-scribe-02 | `python3 main.py` — the submission's own documented start command — exits 1 and prints "Error: PySide6 is not installed. / Please install PySide6 dependencies: / pip install -r requirements.txt". The log line shows the actual cause: `PySide6 is not installed: No module named 'qdarkstyle'`. PySide6 *is* installed and working ([[evidence:ev-scribe-01]]). `main.py:50` catches `ImportError` and reports it as a PySide6 problem, so the user is directed to re-run the install command that cannot supply the missing module | R5 | `main.py:30-55`; `src/gui/qt_app.py:11` | `runs/team-scribe-app-start-01.json` | High |
| ev-scribe-03 | `src/gui/qt_app.py:11` imports `qdarkstyle` and calls `qdarkstyle.load_stylesheet_pyside6()` at lines 48, 54, 310 and 315. No requirements file declares `qdarkstyle`. `requirements.txt:25` and `requirements.lock:16` declare `pyqtdarktheme`, a different package that imports as `qdarktheme`, and `setup_pyside6.py:82` imports `qdarktheme`. The submission's declared install therefore cannot satisfy its own GUI import | R5 | `src/gui/qt_app.py:11,48,54,310,315`; `requirements.txt:25`; `requirements.lock:16`; `setup_pyside6.py:82` | static read at the pinned commit; the runtime consequence is `runs/team-scribe-app-start-01.json` and `runs/team-scribe-module-import-01.json` | High |
| ev-scribe-04 | Importing seventeen modules under `src/` one at a time: fifteen import cleanly (`version`, `config.settings`, `config.logging_config`, `gui.constants`, `audio.recorder`, `transcription.whisper_service`, `transcription.speaker_service`, `transcription.diarization`, `ai.summarizer`, `ai.prompt_templates`, `vault.manager`, `export.markdown_generator`, `export.transcription_exporter`, `utils.retry`, `utils.formatting`). Two fail — `gui.qt_app` and `gui.qt_main_window` — both at `src/gui/qt_app.py:11`, `ModuleNotFoundError: No module named 'qdarkstyle'`. The failure is confined to the GUI layer; every service module the pipeline is built from loads | R2, R3, R4, R5 | `src/` (56 `.py` files) | `runs/team-scribe-module-import-01.json` | High |
| ev-scribe-05 | Full suite, `python3 -m pytest tests/ -q`: **509 passed, 26 failed**, exit 1, 5.98s, offline. 535 tests collected from 30 files. The failures fall into exactly three classes, recorded separately below; no failure is unaccounted for (13 + 10 + 3 = 26) | R6 | `tests/` | `runs/team-scribe-pytest-01.json` | High |
| ev-scribe-06 | Failure class 1, thirteen tests in `tests/test_thread_safety.py`: `AttributeError: type object 'PyAudio' has no attribute 'reset_mock'`. `tests/conftest.py:19-30` installs a `MagicMock` for `pyaudio` **only if the real package cannot be imported**; `tests/test_thread_safety.py:24` then binds `sys.modules['pyaudio']` unconditionally and calls `.reset_mock()` on it. `requirements.txt:19` declares `pyaudio`, so in the environment the submission itself specifies these thirteen tests cannot pass. They pass only where a declared dependency is missing | R1, R6 | `tests/conftest.py:19-30`; `tests/test_thread_safety.py:24,34,122,281`; `requirements.txt:19` | `runs/team-scribe-pytest-01.json` | High |
| ev-scribe-07 | Failure class 2, ten tests — seven in `tests/test_main_page_speaker.py`, three in `tests/test_pipeline_status.py`. Both trace to the undeclared import in [[evidence:ev-scribe-03]]: the `test_pipeline_status` failures surface it directly (`src/gui/qt_main_window.py:30` → `src/gui/main_window/_actions.py:25` → `src/gui/workers/__init__.py:3` → `src/gui/workers/recording_worker.py:17` → `src/gui/qt_app.py:11`, `ModuleNotFoundError: No module named 'qdarkstyle'`), and the `test_main_page_speaker` failures surface it as `AttributeError: module 'gui' has no attribute 'qt_main_window'` at `tests/test_main_page_speaker.py:66`, where `unittest.mock.patch` cannot resolve a target inside a module that did not import | R5, R6 | `tests/test_pipeline_status.py:298,355,404`; `tests/test_main_page_speaker.py:66`; `src/gui/qt_app.py:11` | `runs/team-scribe-pytest-01.json` | High |
| ev-scribe-08 | Failure class 3, three tests in `tests/test_checkpoint.py`: `OSError: [Errno -9996] Invalid input device (no default output device)`, raised inside real PyAudio at `src/audio/recorder.py:130` and re-raised as `AudioException` at `:165`. These three tests drive the real capture path rather than a double, so they require a host with an input device. They are evidence-limited by this event's no-audio-device decision, and separately they are the only three failures that a machine with a microphone would likely not reproduce | R1, R6 | `tests/test_checkpoint.py:65,72,77`; `src/audio/recorder.py:130,165` | `runs/team-scribe-pytest-01.json` | High |
| ev-scribe-09 | `pytest.ini` declares its options under `[tool:pytest]`, which is the `setup.cfg` section name; a `pytest.ini` file is read under `[pytest]`. pytest names the file (`configfile: pytest.ini`) and applies nothing from it: running one test file shows dot progress rather than the `--verbose` the file requests, prints no coverage report despite `--cov=src --cov-report=term-missing`, and exits 0 where `--cov-fail-under=80` would have failed it. `testpaths`, `--strict-markers`, the five declared markers and `filterwarnings` are inert for the same reason. The 80% coverage gate the project believes it enforces has never run | R6 | `pytest.ini:1` | `runs/team-scribe-pytest-config-01.json` | High |
| ev-scribe-10 | The pinned tree holds 30 files matching `tests/test_*.py` and pytest collects 535 tests from them. `README.md`'s test-category table names twenty-six files across nine categories, so four test files are absent from the table that documents them. Neither number is a coverage claim; the count is recorded because the intake record raised the same discrepancy and it reproduces | R6 | `tests/`; `README.md` test-category table | `runs/team-scribe-pytest-01.json` (509 + 26 = 535); `find tests -name 'test_*.py'` against the pinned checkout | High |
| ev-scribe-11 | Provider and network surface across all 56 `.py` files under `src/`: `openai` is imported in exactly four modules — `src/config/settings.py`, `src/transcription/whisper_service.py`, `src/ai/summarizer.py`, `src/utils/retry.py`. There is no import of `requests`, `httpx`, `urllib`, `socket`, `http`, `aiohttp` or any non-OpenAI provider SDK anywhere in `src/`. `OPENAI_API_KEY` is read at four sites — `src/config/settings.py:303,332`, `src/transcription/whisper_service.py:96` and `src/ai/summarizer.py:54` — and reported again at `src/transcription/whisper_service.py:449`. Two of the four are the documented keyring-first chain in `settings.py`. The other two are one fallback pattern written twice: `whisper_service.py:92-96` and `summarizer.py:50-54` each ask `settings_manager.get_openai_api_key()` first and read the environment directly only when no settings manager was supplied, so a caller that constructs either service without one bypasses the keyring and the encrypted store. R7's ordering holds for `settings.py` and is one of two paths in those two service modules. The submission's declared external surface and its actual one agree: one provider, reached through one SDK | R2, R3, R7, R8 | `src/**/*.py` (56 files); `src/config/settings.py:303,332`; `src/transcription/whisper_service.py:92-96,449`; `src/ai/summarizer.py:50-54` | grep reproducible against the pinned checkout; no execution involved | High |
| ev-scribe-12 | Agent-configuration inventory, re-counted independently of the intake record and agreeing with it: `CLAUDE.md` (1), `.github/copilot-instructions.md` (1), `.claude/local/commands/` (3), `.claude/local/skills/` (3 `SKILL.md`), `.claude/local/prompts/` and `.claude/local/agents/` (empty but for `.gitkeep`), `ai/beans/` (168 files across 54 `BEAN-*` directories plus two root files), `ai/reports/` (6). `.claude/shared` is an empty directory: `.gitmodules` declares it at `git@github.com:beekeeper-lab/claude-kit.git` and `git submodule status` reports `-3dff46d6…`, uninitialized. Per the event director's recorded decision, that gitlink is outside the eligible scope, so nothing about its contents is evidence here | R10 | `CLAUDE.md`; `.github/copilot-instructions.md`; `.claude/local/**`; `ai/beans/**`; `ai/reports/**`; `.gitmodules` | `find`/`git submodule status` against the pinned checkout; no execution involved | High |
| ev-scribe-13 | Scale of the tree at the pin, for the panel's proportion judgments rather than for any requirement: 56 `.py` files under `src/`, 30 test files, 535 collected tests, and a `src/` layout of eight packages (`ai`, `audio`, `config`, `export`, `gui`, `transcription`, `utils`, `vault`) plus `assets` | - | `src/`; `tests/` | `runs/team-scribe-pytest-01.json` (535 collected); `find` against the pinned checkout | High |
| ev-scribe-14 | Key storage as implemented: `src/config/settings.py` reads in the order keyring → encrypted config → environment (implemented at `:288-306`; the docstring at `:286` states the same order), writes to the keyring when available and to `.api_keys.enc` otherwise (`:341-370`), and the fallback is Fernet with a PBKDF2-HMAC-SHA256 key at 100,000 iterations over a random 16-byte salt stored beside the ciphertext (`:380-414`). No plaintext write path exists in that module. One property the claim does not state: the KDF input is `f"ScribeVault-{getpass.getuser()}-{platform.node()}"` (`:388`), a username and hostname rather than a secret, so the fallback resists another machine, not another reader of the same file. A `_get_legacy_encryption_key()` unsalted path (`:393`) is retained for reading version-2 files | R7 | `src/config/settings.py:288-306,341-370,380-414,388,393` | static read at the pinned commit; no key was supplied and no storage path was executed | High |

## Tests and execution

| Command or scenario | Result | Output artifact | Safety controls |
|---|---|---|---|
| `python3 -c '<environment probe>'` — interpreter, platform, declared-package presence, offscreen `QApplication` | exit 0; Debian 13, Python 3.12.14; `qdarkstyle` absent, `qdarktheme` present | `runs/team-scribe-envcheck-01.json` | `--network none`, read-only mount, uid 65534, caps dropped, tmpfs `/tmp`, 600s timeout |
| `python3 -m pytest tests/ -p no:cacheprovider -q` | exit 1 — 509 passed, 26 failed, 5.98s | `runs/team-scribe-pytest-01.json` | as above, 1800s timeout |
| `python3 main.py` — the documented start command | exit 1; "Error: PySide6 is not installed."; actual cause `No module named 'qdarkstyle'` | `runs/team-scribe-app-start-01.json` | as above, 120s timeout |
| `python3 -c '<import sweep of 17 modules>'` | exit 0; 15 import, 2 fail at `src/gui/qt_app.py:11` | `runs/team-scribe-module-import-01.json` | as above, 300s timeout |
| `python3 -m pytest tests/test_api_key_validation.py -p no:cacheprovider` — whether `pytest.ini` applies | exit 0, 38 passed; no `--verbose`, no coverage report, no `--cov-fail-under` enforcement | `runs/team-scribe-pytest-config-01.json` | as above, 300s timeout |
| Recording, transcription, summarization, vault write, export, GUI interaction | **not run** — no audio device, no display interaction, no network, no API key | none | n/a |

## Relevant implementation evidence

| Evidence ID | Path/symbol | Relevance |
|---|---|---|
| ev-scribe-03 | `src/gui/qt_app.py:11` | The single undeclared import that stops the application and ten tests |
| ev-scribe-02 | `main.py:50-55` | `except ImportError` reports every import failure as a missing PySide6 and prescribes a command that cannot fix this one |
| ev-scribe-06 | `tests/conftest.py:19-30`, `tests/test_thread_safety.py:24` | A conditional mock and an unconditional consumer of it: the suite depends on a declared dependency being absent |
| ev-scribe-09 | `pytest.ini:1` | Section name from a different file format; every option in the file is inert |
| ev-scribe-14 | `src/config/settings.py:288-414` | Key handling: keyring first, Fernet fallback, machine-string KDF input |
| ev-scribe-11 | `src/transcription/whisper_service.py`, `src/ai/summarizer.py`, `src/config/settings.py`, `src/utils/retry.py` | The whole provider surface, four modules, one provider |
| ev-scribe-12 | `CLAUDE.md`, `.claude/local/**`, `ai/beans/**` | The agent-instruction surface this event's H6 is about; read as data throughout |

## Missing or inaccessible evidence

1. **The recording path was not exercised.** No audio device was provided, by
   the event's decision recorded above. Everything downstream of capture —
   checkpoint flushing, `recover_checkpoints()`, the FFmpeg fallback — is
   unobserved. It limits R1 and the runtime half of `functional`.
2. **Every OpenAI path was unreachable.** `network_allowlist` is empty and no key
   was supplied, so cloud transcription, summarization, categorization, prompt
   templates and the live key-validation path were not executed. It limits R2,
   R3, R7 and R8, and it is a property of this event, not a deficiency of the
   submission.
3. **The local Whisper path was not installed.** `requirements-local.txt` is
   optional by the submission's own statement, so the offline alternative to (2)
   is equally unobserved.
4. **No GUI was driven.** Both GUI modules fail to import, so no window, settings
   panel, cost estimate or export dialog was exercised. Here the cause is inside
   the submission ([[evidence:ev-scribe-03]]), not inside the sandbox, and a
   judge should not record that as evidence-limited.
5. **The `.claude/shared` gitlink is not materialized**, by the event director's
   decision. Nothing may be assumed or concluded about its contents, and any
   judgment about how this project directs its agents is made from part of its
   agent configuration.
6. **Three test failures are environment-caused** ([[evidence:ev-scribe-08]]).
   They should not be counted against the submission as defects; the other
   twenty-three reproduce in any environment matching the submission's own
   declaration.

## Validation

- [x] Immutable commit verified — `git rev-parse HEAD` in the checkout returns
      `67969dd9479c096f05d998d8c50e5ea1968e3245`, detached
- [x] Untrusted instructions ignored — every file and every command output in
      this package was read as data
- [x] Execution policy satisfied — `atj sandbox preflight` AVAILABLE before any
      run; every run isolated, offline and read-only; nothing executed on the host
- [x] Artifact references resolve — every `runs/*.json` named above exists in
      `events/trial-2-2026/runs/`
- [ ] Manifest independently validated — pending the evidence stage audit
