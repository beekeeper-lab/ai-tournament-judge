---
event_id: trial-2-2026
team_id: team-scribe
commit: 67969dd9479c096f05d998d8c50e5ea1968e3245
evidence_package_id: ev:trial-2-2026:team-scribe:67969dd9479c:018cf089
rubric: submission-evaluation@1.1.0
persona: build-team-dossier@1.0.0
framework_commit: 566166b
source_reports:
- summaries/team-scribe.md
- summaries/team-scribe.json
- judgments/team-scribe/
- adjudications/adj-trial-2-2026-team-scribe-agentic.md
- evidence/team-scribe/manifest.md
- runs/team-scribe-envcheck-01.json
- runs/team-scribe-app-start-01.json
- runs/team-scribe-pytest-01.json
- matchups/mu-final-01.md
model_requested: claude-opus-5
model_used: claude-opus-5-5[1m]
started_at: "2026-09-23T19:58:15Z"
completed_at: "2026-09-23T20:01:27Z"
visibility: team
approval_state: draft
validation_state: unvalidated
---

# Team Dossier — ScribeVault

## Your project at a glance

ScribeVault is a PySide6 desktop application that records conversations,
transcribes them locally or through a cloud provider, summarizes and categorizes
them, and keeps the results in a local vault. Four reviewers evaluated it
independently at commit `67969dd9`, against one shared evidence package
(`ev:trial-2-2026:team-scribe:67969dd9479c:018cf089`), under
`submission-evaluation@1.1.0`. Each reviewer looked through a different lens:
backend and architecture, frontend and user experience, product and AI design,
and security and operations.

**There is no overall score for this submission, and that is not a penalty.**
The `agentic` criterion is recorded as `NE` (not evaluable), and the rubric does
not allow an official total while any criterion is `NE`. The event director
reviewed that criterion and accepted the `NE` rather than supplying a number
(`adjudications/adj-trial-2-2026-team-scribe-agentic.md`). The reason is below
under the agentic criterion.

The central finding is shared by all four reviewers. The documented start
command, `python3 main.py`, exits with status 1 in an environment that holds
exactly what the submission declares, because `src/gui/qt_app.py:11` imports
`qdarkstyle`, a package no requirements file names
(`runs/team-scribe-app-start-01.json`). Every advertised workflow is entered
through that GUI, so none of them could be reached. Beneath that one failure the
reviewers found a substantial, well-organized codebase: an intact service layer,
a narrow and auditable network surface, careful credential storage and
genuinely ambitious audio work. The gap between the quality of that work and
what a user can reach today is the main message of this dossier, and the fix for
the largest part of it is one line.

### What this result does not cover

This event ran every submission without network access and without an audio
device. That limited what anyone could observe here, and none of the following
counts against you:

- No recording, checkpoint flush or crash recovery was exercised (no audio
  device, `evidence/team-scribe/manifest.md`, Missing item 1).
- No OpenAI call was possible, so transcription quality, summaries, categories
  and real cost could not be observed (Missing item 2).
- The local Whisper path was not installed (Missing item 3).
- Three of the 26 test failures come from the absent audio device, and every
  reviewer excluded them (Missing item 6).

One limitation is different. No window was ever rendered, and the manifest
records that this cause is inside the submission, not the sandbox (Missing
item 4). The reviewers therefore treated the unreachable GUI as an observed
defect rather than as missing evidence.

## What you did especially well

These strengths were reached by more than one reviewer. Where several rest on
the same evidence item, that is several readings of one observation, and it is
said so.

- **The service layer is sound.** Fifteen of seventeen probed modules import
  cleanly; only the two GUI modules fail. All four reviewers credit the
  non-GUI code, and the product reviewer called it "in far better shape than the
  headline failure suggests".
- **Your network surface is narrow and checkable.** One provider, reached
  through one SDK, imported in four modules, with no other HTTP or socket
  library anywhere under `src/` (evidence item `ev-scribe-11`). All four
  reviewers relied on this reading. It is what makes the privacy story of the
  application auditable.
- **Credential storage is implemented, not only described.** Keyring first,
  then an encrypted file using Fernet over PBKDF2-HMAC-SHA256 at 100,000
  iterations with a fresh random salt, then the environment
  (`src/config/settings.py:288-306`, `ev-scribe-14`). All four reviewers credit
  this design. The security and operations reviewer, who scored `security`
  lowest, still described the storage implementation as "above the level this
  event requires".
- **Retries are classified, not blanket.** `src/utils/retry.py` retries only
  rate limits, timeouts, connection errors and a named set of server status
  codes, with bounded backoff and a terminal error. The backend, product and
  security reviewers all credit it.
- **Your suite is large, fast and runs offline.** 535 tests collected, 509
  passing, in a read-only container with no network, as an unprivileged user
  (`runs/team-scribe-pytest-01.json`). The product reviewer read this as a
  codebase built to run without ambient state. The security reviewer added that
  it is fast enough to gate on.
- **There is real technical ambition.** All four reviewers scored `innovation`
  at 3. They point to hand-written audio feature extraction and hierarchical
  clustering for speaker diarization (`src/transcription/diarization.py`),
  checkpointed recording designed to survive a crash
  (`src/audio/recorder.py:303-454`), and cost-aware routing between local and
  cloud transcription with pricing kept in a dated config file.
- **Your error messages on the AI paths are good.** `whisper_service.py:81-88`
  and `:104-110` give the cause and two remedies, and `:127-143` refuses an
  oversized upload with the numbers and alternatives. The product and frontend
  reviewers both noticed this, which makes the one misleading message below
  stand out more.

## Criterion feedback

Scores are on the rubric's 0-5 scale, where 1 means "seriously deficient; major
failures dominate", 2 means "partially successful; useful elements with
important weaknesses" and 3 means "solid for the event; primary expectations are
met". Each value is the panel mean recorded in `summaries/team-scribe.json`.

| Criterion | Panel score | Agreement |
|---|---:|---|
| Functional correctness and completeness | 1.00 | all four at 1 |
| Product value and usability | 2.00 | all four at 2 |
| Agentic and AI system design | `NE` | two scored, two not evaluable; adjudicated `NE` |
| Engineering and maintainability | 2.00 | all four at 2 |
| Reliability, testing, and observability | 2.00 | all four at 2 |
| Security, privacy, and responsible AI | 2.75 | three at 3, one at 2 |
| Innovation and technical ambition | 3.00 | all four at 3 |

### Functional correctness and completeness — 1.00 / 5

**Limitation.** The application does not start from its own declared install.
`src/gui/qt_app.py:11` imports `qdarkstyle`, while `requirements.txt:25` and
`requirements.lock:16` declare a different package, `pyqtdarktheme`, whose
import name is `qdarktheme`. All four reviewers named this first, and it is the
whole reason this criterion sits at 1.

**Strength.** The failure is confined to the GUI layer. The code behind it
imports and most of it is tested.

**Next step.** Switch the import in `src/gui/qt_app.py` (lines 11, 48, 54, 310
and 315) to `qdarktheme`, which `setup_pyside6.py:82` already uses, or declare
`qdarkstyle`. Then prove it from a clean environment built only from
`requirements.txt`, for example with `python3 -c "import gui.qt_main_window"`.

### Product value and usability — 2.00 / 5

**Limitation.** The one message a user is certain to see points the wrong way.
`main.py:50` catches every `ImportError` from the GUI import tree and reports it
as "PySide6 is not installed", prescribing `pip install -r requirements.txt`,
which cannot supply the missing module. PySide6 is installed and works
(`runs/team-scribe-envcheck-01.json`). All four reviewers recorded this.

Three further points were each raised by one reviewer:

- The frontend and UX reviewer found that when a service fails to initialize,
  the actionable text you wrote goes to the log and never reaches the window
  (`src/gui/qt_main_window.py:105-109`), and that the README places Settings in
  a toolbar the window does not have.
- The security and operations reviewer found that `README.md:103-107`
  recommends an installer that creates a `.env` file for the key, while
  `README.md:119` says keys are not stored in `.env`.
- The product and AI reviewer found that the README carries no privacy, consent
  or retention statement, for an application that records conversations and can
  upload them.

The product reviewer also noted that transcription defaults to `local`
(`src/config/settings.py:31`) while the base install omits the packages the
local path needs, so a default first run is likely to land in the unconfigured
path. The frontend reviewer recorded the same concern as an unobserved risk and
did not score it.

**Strength.** The product and AI reviewer credited three design decisions:
summarization is an opt-in the pipeline actually honors, the cost comparison is
shown before the user chooses, and a failed stage can be retried on its own
rather than forcing a re-record. That reviewer credited them as design
evidence, since no window could be driven.

**Next step.** Narrow the handler at `main.py:50` so it reports the module that
actually failed. The backend and product reviewers both made this their
top product improvement.

### Agentic and AI system design — `NE`

**Why there is no score.** The rubric asks whether AI use is appropriate,
controlled, observable and effective. This event could make no model call and
could not open the Settings dialog, so effectiveness and in-operation
observability had no observation at all. Two reviewers (frontend and UX,
security and operations) recorded `NE` for that reason. Two (backend, product
and AI) scored the criterion from source reads of the design. No reviewer
disputed another's facts. They disagreed on which half of the criterion
matters more. The event director reviewed both positions and accepted the `NE`
without supplying a score.

**Strengths observed in source.** Using models only for speech-to-text and
summarization is the right call. The call surface is small and bounded, and a
missing key
routes to the local path with a warning instead of an error. The backend
reviewer alone traced the category whitelist from the summarizer to a
constrained database column.

**Limitations observed in source.** The backend reviewer found that
`extract_key_points` (`src/ai/summarizer.py:167-189`) parses free model output
with no schema check and fails silently to `None`, and that there is no length
management for long transcripts. The product and AI reviewer found that
`response.usage` is discarded, so spend is estimated and never measured, and
that there is no evaluation of output quality.

**Next step, and what would make this criterion scorable next time.** Both
reviewers who recorded `NE` asked independently for the same thing: make the AI
path observable without a provider. The frontend reviewer suggested a dry-run
mode that renders the cost estimate, model and settings from local config. The
security reviewer suggested logging request and response metadata and adding
fixture-backed offline tests of `summarize_text`, `extract_key_points` and
`categorize_content`. Either would let a network-less evaluation score this
criterion.

### Engineering and maintainability — 2.00 / 5

**Limitation.** Configuration and verification failures, not logic failures,
account for most of the serious defects. The lockfile pins a package the code
does not import. `pytest.ini:1` uses `[tool:pytest]`, a `setup.cfg` section
name, so pytest names the file but applies none of it, including the
`--cov-fail-under=80` gate (`ev-scribe-09`). All four reviewers recorded the
inert configuration.

The backend reviewer alone found that the stage-retry worker,
`src/gui/workers/retry_worker.py`, uses constants it never imports, so every
retry raises `NameError`, which a broad `except` then swallows. No test covers
that class. The same reviewer found that persisted pipeline status is saved
while the save stage is still marked running, so the stored state and the
screen disagree.

**Strength.** Eight packages that map onto the pipeline stages, GUI code split
into builder, action and worker mixins, and one shared retry decorator. The
decomposition is proportionate to the problem.

**Next step.** Change `pytest.ini:1` to `[pytest]`. The backend reviewer also
suggested running `flake8` in CI, which would flag the retry worker's undefined
names on the first run.

### Reliability, testing, and observability — 2.00 / 5

**Limitation.** The suite is red in the environment the submission declares:
26 failures, 23 of which reproduce in any conforming environment
(`runs/team-scribe-pytest-01.json`). All four reviewers found that thirteen
tests in `tests/test_thread_safety.py` can pass only where the declared
`pyaudio` is missing, because `tests/conftest.py:19-30` installs a mock
conditionally and `tests/test_thread_safety.py:24` uses it unconditionally.
The backend and security reviewers both noted that `health_check.py`, which
imports the GUI and would have printed the start failure, is wired to nothing,
and that there is no CI configuration.

**Strength.** The product and security reviewers both credited size-bounded
log rotation. The security and operations reviewer added that file permissions
are re-applied after every rollover and that the logger degrades to console
output rather than crashing, which was observed: the start run logged that it
could not create its log file and continued to its real error
(`runs/team-scribe-app-start-01.json`).

**Next step.** Three reviewers proposed the same single CI job: install from
`requirements.txt` in a clean environment, run `python3 health_check.py`, then
run `pytest`. It would catch the start failure, the inert configuration and the
test-mock inversion on its first run.

### Security, privacy, and responsible AI — 2.75 / 5

**Why the scores differ.** Three reviewers scored 3 and judged the
implementation: the storage design is responsible for a single-user desktop
tool. The security and operations reviewer scored 2 and judged what a user is
actually handed. None of the three higher scores contradicts the lower one. The
difference is which question each reviewer weighted.

**The lower score's reasoning, from that reviewer alone.** The Settings dialog,
which the README names as the way to enter a key, is in the GUI that cannot
start. The installer the README recommends copies `.env.example` to a plaintext
`.env` with no permission hardening (`install.py:124-127`), and
`src/config/settings.py:26` loads that file. So at this commit the reachable
key path is the plaintext one that `README.md:119` and `SECURITY.md:5` say does
not exist. The reviewer recorded this as a credible risk, not a demonstrated
exploit, since `install.py` was not run.

**Corroborated limitations.**

- All four reviewers found that two service constructors
  (`src/transcription/whisper_service.py:92-96`, `src/ai/summarizer.py:50-54`)
  read `OPENAI_API_KEY` directly when built without a settings manager, so the
  documented key ordering is one of two paths.
- The backend and security reviewers found that two claims in `SECURITY.md` do
  not hold at this commit. `SECURITY.md:34` says dependencies are pinned, while
  `requirements.txt:18-28` uses ranges. `SECURITY.md:25` says summary content is
  HTML-escaped, which is true of the transcript path and not of the markdown
  summary path in `src/gui/summary_viewer/render.py`.
- The fallback encryption key is derived from the username and hostname
  (`src/config/settings.py:388`), which protects the file against being copied
  to another machine but not against another reader on the same account. The
  product and frontend reviewers counted this against the score. The backend
  reviewer called it defensible for this class of application and asked only
  that the documentation say so.

**Strength.** The keyring and Fernet design, credited by all four reviewers.
The frontend and UX reviewer added that key entry is masked and a stored key is
never echoed back. The security and operations reviewer added that
`.gitignore` covers the key file, `.env`, the database and audio files.

**Next step.** Remove the `.env` creation from `install.py` or make it write a
0o600 file, add a way to enter a key that does not need the window, require the
settings manager in both services, and correct `SECURITY.md` so it states what
the file encryption actually protects against.

### Innovation and technical ambition — 3.00 / 5

**Strength.** Diarization built from first principles, crash-resilient
checkpointed recording, and cost-driven local and cloud routing. This is the
criterion where the panel was most positive.

**Limitation.** None of it could be demonstrated in this event. The backend
reviewer alone found that the checkpoint flush rewrites every frame on every
flush (`src/audio/recorder.py:326-352`), so its cost grows with recording
length, although `_last_flushed_count` is already tracked.

**Next step.** The security reviewer suggested offline fixture tests for
diarization and checkpoint recovery, so your two most original pieces become
demonstrable without a microphone or a provider.

## Tournament journey

ScribeVault met AI Security Demos in the event's single final matchup,
`mu:trial-2-2026:final:01`. Two independent matchup judges compared the teams,
each seeing them in the opposite order, and both chose AI Security Demos. ScribeVault
did not advance.

The decisive evidence was the start failure. A user following ScribeVault's own
install and run instructions reaches no workflow, and both judges weighted that
most heavily under product value and functional correctness. Both judges also
said the functional comparison rested more on ScribeVault's confirmed failure
than on the other team's demonstrated success.

Two criteria came out even in both orders. Reliability was even because
ScribeVault's 509 passing tests were offset by a red suite, an inert coverage
gate and no CI. Innovation was even as well. Neither judge used or compared an
overall total; the comparison is made criterion by criterion.

## Blocking issues

1. **The application does not start from its declared install.** Undeclared
   `qdarkstyle` import at `src/gui/qt_app.py:11`. Confirmed by execution
   (`runs/team-scribe-app-start-01.json`) and named first by all four
   reviewers.
2. **The start error misdiagnoses its own cause.** `main.py:50` reports a
   missing PySide6 and prescribes a command that cannot fix the problem.
   Confirmed by execution and recorded by all four reviewers.
3. **No quality gate runs.** `pytest.ini` is inert, there is no CI, and thirteen
   tests depend on a declared dependency being absent. Confirmed by execution
   (`ev-scribe-06`, `ev-scribe-09`) and recorded by all four reviewers.

## Recommended improvement plan

1. **Immediate repair.** Fix the `qdarkstyle` import and narrow the handler at
   `main.py:50` so it names the missing module. Together they are a few lines,
   and they turn a dead end into a working application or a self-explaining
   failure.
2. **Highest-value next iteration.** Add one CI job that installs from
   `requirements.txt` in a clean environment, runs `health_check.py` and
   `pytest`, with `pytest.ini` corrected to `[pytest]` and
   `tests/test_thread_safety.py` installing its own mock. In the same pass,
   make the credential path reachable without the window and bring
   `SECURITY.md` and the README in line with the code.
3. **Longer-term opportunity.** Make the AI path observable offline: record
   `response.usage` and show measured spend next to the estimate, validate
   structured model output, and add fixture-backed tests for the summarizer and
   for diarization and checkpoint recovery. That would demonstrate your
   strongest ideas and would let a future network-less evaluation score the
   `agentic` criterion.

## Evidence appendix

| What | Where |
|---|---|
| Start failure, exit 1, `No module named 'qdarkstyle'` | `runs/team-scribe-app-start-01.json` |
| Test result, 26 failed and 509 passed | `runs/team-scribe-pytest-01.json` |
| Inert `pytest.ini`, the `pyaudio` mock inversion, the module import sweep | `evidence/team-scribe/manifest.md` (`ev-scribe-04`, `ev-scribe-06`, `ev-scribe-09`) |
| Network surface across `src/` | `evidence/team-scribe/manifest.md` (`ev-scribe-11`) |
| Key storage as implemented | `evidence/team-scribe/manifest.md` (`ev-scribe-14`) |
| What this event could not observe | `evidence/team-scribe/manifest.md`, Missing items 1-6 |
| Why `agentic` is `NE` | `adjudications/adj-trial-2-2026-team-scribe-agentic.md` |
| Per-criterion panel scores | `summaries/team-scribe.json` |
| Final matchup result | `matchups/mu-final-01.md` |

Source locations in this dossier refer to your repository at commit
`67969dd9479c096f05d998d8c50e5ea1968e3245`.
