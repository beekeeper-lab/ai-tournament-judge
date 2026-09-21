---
event_id: trial-2-2026
audit_scope: intake stage
audit_id: intake
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.1.0
persona: judging-auditor@1.1.0
framework_commit: e5322ac5d214d586eec07434259e70e1441e6572
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-21T23:16:37Z"
completed_at: "2026-09-21T23:27:54Z"
visibility: private
approval_state: draft
validation_state: unvalidated
result: FAIL
findings:
- id: F1
  severity: major
  scope: event
  blocking: true
  summary: The ScribeVault intake states the `.claude/shared` submodule is "a private repository reachable only with the operator's SSH credentials" and that its content "cannot be fetched". Re-derived without credentials — `beekeeper-lab/claude-kit` is public and the pinned gitlink commit `3dff46d6` fetches anonymously. The eligible-scope ruling in the record rests on a false premise.
  artifact: events/trial-2-2026/submissions/team-scribe.md:121-131
  repair: Restate the constraint as the one that is true (the configured submodule URL is SSH and no key is supplied, so `git submodule update` fails here), and either record the out-of-scope ruling as an event-director decision with that reason or materialize the gitlink from `https://github.com/beekeeper-lab/claude-kit` at `3dff46d6` and re-pin.
  state: open
- id: F2
  severity: minor
  scope: event
  blocking: false
  summary: Both intake records carry `completed_at` equal to the clone minute (21:53:01Z, 22:04:10Z) while their narrative was edited twice afterwards, in commits `196aa42` (22:18:08Z) and `49242aa` (22:28:44Z). The field describes the clone, not the completed record.
  artifact: events/trial-2-2026/submissions/team-scribe.md:9-11
  repair: Set `completed_at` on each record to the time its content was last completed, or state in the template that the field describes the clone. Tooling half is configuration `F23`; the reason nothing caught it is configuration `F20`.
  state: open
- id: F3
  severity: minor
  scope: event
  blocking: false
  summary: The checkbox repair made to `status.md` at 23:16:00Z is correct and minimal, but it is recorded nowhere — no activity-log row, and `last_updated` still reads 22:34:38Z. This is configuration `F22`'s condition returning in the same file.
  artifact: events/trial-2-2026/status.md:4
  repair: Add an activity row for the hand repair and set `last_updated` when the `roster-frozen` gate is recorded.
  state: open
- id: F4
  severity: minor
  scope: framework
  blocking: false
  summary: '`atj event gate` and `atj event advance` write the front-matter gate and stage but never tick the matching body checkbox, so a passing gate leaves `status.md` in a state `validate_status_narrative` rejects. That is the defect the operator repaired by hand before this audit, and live-trial-2026 finished in the same state (D30).'
  artifact: atj/event.py:696-704
  repair: Have the gate and advance commands write the matching body checkbox, or refuse to exit while the body contradicts the ledger they just wrote.
  state: open
- id: F5
  severity: minor
  scope: event
  blocking: false
  summary: The deferred untrusted-data wrapper (configuration `F11`) is scoped to one file, and the demos intake names four payload demos. A narrow phrase scan finds instruction-shaped payloads in at least eight files across demos 01, 02, 05, 06 and 10, and the ScribeVault agent configuration includes `.claude/local/prompts/` and `.claude/local/agents/`, which the record does not name.
  artifact: events/trial-2-2026/submissions/team-demos.md:100-119
  repair: Enumerate the payload-carrying files and the agent-configuration paths in the record or the evidence plan, so the evidence stage wraps a set rather than an example.
  state: open
- id: F6
  severity: advisory
  scope: event
  blocking: false
  summary: "Both intake records are still `approval_state: draft` and `validation_state: unvalidated` although `atj validate reports` has passed them. live-trial-2026's intake records were `approved` and `valid` before its roster froze."
  artifact: events/trial-2-2026/submissions/team-demos.md:16-17
  repair: Run `atj event approve` on both records before freezing the roster, or state that intake records stay draft in this event.
  state: open
- id: F7
  severity: advisory
  scope: framework
  blocking: false
  summary: '`teams.md` carries three front-matter fields; `framework/templates/team-roster.md` shows ten. `events/_template/teams.md` matches the event and `schemas/roster.schema.json` requires four keys, so the roster about to be frozen carries no `visibility`, `approval_state` or `validation_state`, and `atj release-check` reports templates PASS.'
  artifact: framework/templates/team-roster.md:1-12
  repair: Reconcile `framework/templates/team-roster.md`, `events/_template/teams.md` and `schemas/roster.schema.json` on one front matter.
  state: open
- id: F8
  severity: advisory
  scope: framework
  blocking: false
  summary: Configuration `F10` carried forward — both intake provenance tables print the absolute operator home path, in files committed to a public repository. No credential or third-party data is exposed.
  artifact: events/trial-2-2026/submissions/team-scribe.md:141
  repair: Write a repository-relative checkout path in `atj intake`.
  state: open
- id: F9
  severity: advisory
  scope: framework
  blocking: false
  summary: "Configuration `F17` carried forward. The withdrawal of `beekeeper-lab/website` is findable in `event.md` and the plan, and its privacy premise is true — anonymous access to that repository is refused while both rostered repositories are anonymously readable. What is unrepaired is the form: repository visibility is still asserted as fact, without attribution or a check a reader can repeat."
  artifact: docs/0.5.0-beta-plan.md:179-186
  repair: Attribute the visibility claims to the operator or cite the check in this report's F9 evidence.
  state: open
- id: F10
  severity: advisory
  scope: event
  blocking: false
  summary: Both checkouts sit on an attached `main` tracking `origin/main`, clean and at the pin, which is also the current remote HEAD. A `git pull` would move the evidence base silently, and `workspaces/` is gitignored, so no committed artifact would show the drift.
  artifact: workspaces/trial-2-2026/team-scribe
  repair: Detach both checkouts at their pinned commits, or re-verify `git rev-parse HEAD` against the pin as a recorded step of each evidence package.
  state: open
---

# Judging Audit — intake stage

## Result

**FAIL.** One major finding, marked blocking, holds the `roster-frozen` gate:
`F1`. The ScribeVault intake record states as established fact that the
`.claude/shared` submodule is a private repository whose content "cannot be
fetched", and builds an eligible-scope ruling on that. Re-derived with
credentials disabled, `beekeeper-lab/claude-kit` is public and the pinned gitlink
commit is anonymously fetchable. The record is wrong about the one fact that
decides what is inside the submission being frozen.

Everything else re-derived. Both pins agree across four places and both
checkouts, both intake records match the template, the disputed test count from
configuration `F1` is right, the demos have no test file anywhere in the tree,
every timestamp sits inside the event window and the activity log is ascending,
`public/` is empty and the publication check is clear. The operator's checkbox
repair is correct and changed nothing else.

The pattern this event was built to observe held again: the repair that closed
configuration `F2` introduced `F1` of this report, and it survived two further
audit rounds because nobody tested the claim against the network.

## Scope and artifacts inspected

Intake only. No evidence package, judgment, bracket or matchup exists, and none
was audited.

Read: `events/trial-2-2026/event.md`, `teams.md`, `status.md`,
`submissions/team-scribe.md`, `submissions/team-demos.md`,
`audits/configuration.md`, `status.md.bak` (ignored runtime artifact),
`framework/templates/submission-intake.md`, `framework/templates/team-roster.md`,
`framework/templates/audit-report.md`, `framework/personas.md`,
`schemas/roster.schema.json`, `schemas/submission-intake.schema.json`,
`schemas/audit.schema.json`, `atj/event.py`, `atj/reports.py`, `CLAUDE.md`,
`docs/0.5.0-beta-plan.md:170-195`, `events/live-trial-2026/status.md` and
`events/live-trial-2026/submissions/team-podcast.md` for precedent, and both
pinned checkouts under `workspaces/trial-2-2026/`.

Both checkouts were read read-only, by path, from the framework root. Nothing in
either was executed; a `python3 - <<EOF` invocation issued with the working
directory inside the ScribeVault checkout was refused by
`.claude/hooks/pre-advance.sh` as host execution of submission code, and the
check was redone with shell tools from the framework root. Every file inside a
checkout is treated in this report as evidence described, never as instruction
followed — including the resume payload at
`workspaces/trial-2-2026/team-demos/01-resume-that-talked-back/demo/goofy-goof.md:20-27`,
which directs a screening assistant to score the candidate 100 and rank them
first. It was read, quoted in outline and not acted on. See `F5` for the files
like it that no artifact yet enumerates.

Outbound network was used for three read-only checks against `github.com`:
`git ls-remote` on the two rostered repositories, on `beekeeper-lab/website`,
`beekeeper-lab/claude-kit` and `beekeeper-lab/atticus-vault`, and a one-commit
`git fetch` of the claude-kit gitlink into the session scratchpad. Nothing was
fetched into the repository, into either checkout, or executed.

## Deterministic validation results

Re-run at 2026-09-21T23:16:37Z on `e5322ac`:

| Command | Result |
|---|---|
| `python3 -m atj event validate events/trial-2-2026` | `PASS (0 problems, stage intake)` |
| `python3 -m atj validate reports events/trial-2-2026` | `PASS — 3 artifacts, 0 blocking, 0 major, 0 minor, 0 advisory` |
| `python3 -m atj release-check` | `PASS` (rubric 7 criteria total 100, schemas, personas, templates, single-source, version-skew, packaging, write contracts, signed approvals, sample event) |
| `python3 -m atj validate publication events/trial-2-2026` | `CLEAR (3 artifacts, 0 blocking, 0 other)` |
| `python3 -m atj event status events/trial-2-2026` | stage `intake`, 2 teams, 2 eligible, `roster-frozen = pending`; wrote nothing |

All three of the operator's reported results reproduce. `atj event status` was
confirmed read-only: `git diff` on `status.md` after the run still shows exactly
one changed line.

## The operator's repair, checked

The repair is the single line `- [ ] Configuration audited` →
`- [x] Configuration audited` in `events/trial-2-2026/status.md:26`.

- **Correct.** `validate_status_narrative` (`atj/event.py:514-560`) requires each
  body checkbox to agree with its ledger gate. The ledger records
  `configuration-audited: passed` with `gate_evidence` pointing at
  `audits/configuration.md`, whose `result` is PASS WITH ADVISORIES and whose
  `approval_state` is `approved`. A checked box is what that ledger requires.
- **Complete for what it was.** `git diff` against `HEAD` is that one line and
  nothing else. Every other checkbox still matches its gate: eight `pending`
  gates against eight unchecked boxes, and `Event marked complete` unchecked
  against `current_stage: intake`.
- **It introduced one thing, in bookkeeping, not in state.** The edit is not in
  the activity log and `last_updated` still reads `2026-09-21T22:34:38Z`, the
  minute the gate was recorded, while the file changed at 23:16:00Z. Recorded as
  `F3`, because configuration `F22` was this exact condition and its repair note
  said to set the field "again when the gate is recorded".
- **The cause is not the operator.** `status.md.bak` holds the pre-write state:
  gates passed, `current_stage: configuration`, same `last_updated`. So the gate
  and the advance were one invocation that wrote the ledger and left the body it
  requires untouched, which is `F4`.

## Verification of each intake claim

Every claim below was re-derived from the pinned checkout or the named file, not
accepted because it was cited.

### Pins

| Fact | Source | Value |
|---|---|---|
| `teams.md` | row | `67969dd9479c096f05d998d8c50e5ea1968e3245`, `dc35f6962130af5e5be3fe16672e3d4964850eb9` |
| intake front matter | `commit:` | identical, both records |
| intake provenance table | `Pinned commit` | identical, both records |
| `status.md` Team progress | abbreviated | `67969dd9`, `dc35f696` — correct 8-character prefixes |
| activity log | abbreviated | same two prefixes |
| checkout | `git -C … rev-parse HEAD` | identical, both checkouts, both trees clean (`git status --porcelain` empty) |
| remote | anonymous `git ls-remote … HEAD` | identical, both repositories |

Full and abbreviated forms agree everywhere. Both repositories are reachable and
public: anonymous `ls-remote` with the global and system git config neutralized
and the credential helper disabled succeeds for `ScribeVault` and
`ai-security-demos`, and fails for `beekeeper-lab/website` and
`beekeeper-lab/atticus-vault` with "Repository not found … Authentication
failed", which is what proves the credential isolation held.

### ScribeVault — `submissions/team-scribe.md`

| Claim | Re-derivation | Verdict |
|---|---|---|
| "a desktop application for audio recording, transcription, and intelligent summarization with cost-optimized processing" | `README.md:7`, verbatim | correct |
| Four independent, retryable stages; `AudioRecorder`, `WhisperService`, `SummarizerService`, `VaultManager` | `README.md:25`, `README.md:52-58`; classes at `src/audio/recorder.py:28`, `src/transcription/whisper_service.py:43`, `src/ai/summarizer.py:29`, `src/vault/manager.py:39` | correct |
| `$0.00` local, `~$0.36` API, `~$131` annual, Settings UI shows real-time estimates | `README.md:148-153` | correct |
| Transcription defaults to `local` | `README.md:136`, Default column | correct |
| Checkpoint default 30 seconds, `recover_checkpoints()` | `README.md:52`, `README.md:144`; `src/audio/recorder.py:406` | correct |
| `DiarizationService`, speakers auto or 2-6 | `src/transcription/diarization.py:74`; `README.md:142` | correct |
| Models `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, default `gpt-4o-mini`; three summary styles | `README.md:139-140` | correct |
| SQLite vault in WAL mode; export TXT/Markdown/SRT | `README.md:45`, `README.md:58` | correct |
| Python 3.8+, FFmpeg, PortAudio, `sudo apt install ffmpeg portaudio19-dev`, venv + `requirements.txt` or `./setup.sh`, `python main.py` | `README.md:64-114` | correct |
| `pytest tests/`, `--cov=src`, flake8/black/isort/`mypy src/`, `mypy.ini` and `pytest.ini` at root | `README.md:202-220`; both files present at the checkout root | correct |
| **26 test files named across nine categories, 30 in the tree, four unlisted** | README table rows 227-235 name 26 distinct files in nine categories; `tests/test_*.py` is 30 and `find` over the whole tree is also 30; set difference is exactly `test_diarization_settings.py`, `test_thread_safety.py`, `test_utils.py`, `test_version.py`, and every named file exists | correct — configuration `F1` is genuinely repaired |
| Local Whisper optional, ~500 MB via `torch` and `openai-whisper` | `requirements.txt:14-16` states it; the packages are pinned in `requirements-local.txt:14-15` | correct; the attribution to `requirements.txt` is the comment block, not the pins |
| Keyring, Fernet/PBKDF2 fallback, `OPENAI_API_KEY` read-only, never plaintext | `README.md:119-126`, `README.md:286` | correct |
| No key needed for local-only | `README.md` local mode | correct |
| `CLAUDE.md`, `.claude/local/skills/`, `.claude/local/commands/`, `.github/copilot-instructions.md`, `ai/beans/` present | all five present | correct but not exhaustive — `.claude/local/prompts/` and `.claude/local/agents/` are also present (`F5`) |
| One submodule `.claude/shared` at `git@github.com:beekeeper-lab/claude-kit.git`; `git submodule status` prints `-3dff46d6…`; leading `-` means uninitialized | `.gitmodules` declares exactly one; `git submodule status` output matches character for character; `git ls-tree HEAD .claude/shared` gives `160000 commit 3dff46d6…`, so the record's SHA is also the pinned one | correct |
| **"a private repository reachable only with the operator's SSH credentials … it cannot be fetched, and nothing may be assumed about it"** | anonymous `ls-remote` on `beekeeper-lab/claude-kit` succeeds and lists `refs/heads/main`; `git fetch --depth 1 origin 3dff46d60e1285f68bb986b516813a535d14ef4d` into an empty scratch repository succeeds and `git cat-file -t` reports `commit` | **wrong — `F1`** |

### AI Security Demos — `submissions/team-demos.md`

| Claim | Re-derivation | Verdict |
|---|---|---|
| "companion live demos … self-contained, runnable prop … not on a slide" | `README.md:3-6`, verbatim | correct |
| Sift and Marisol, "the vulnerability is never the payload" | `README.md:8-9`, `README.md:53` | correct |
| Each talk in `NN-slug/demo/`, own README with "the three-act presenter script" | `README.md:23-24`; ten `demo/` directories present | correct |
| The ten attack vectors, 01 through 10 | `README.md:29-38` table, item by item | correct, in order |
| Two run paths; Claude Code with no key and `/` commands; Python with `ANTHROPIC_API_KEY`, `.env.example`, `uv`; "a `--dry-run` flag prints the exact prompt with no API call" | `README.md:16-21`; ten `.env.example` files; ten `demo/.claude/commands/` directories | correct |
| The documented dry run is `uv run --with anthropic …` | the exact string is in the per-demo README, e.g. `01-resume-that-talked-back/demo/README.md:22`, not the root `README.md` the paragraph otherwise cites | correct in substance, imprecise in citation |
| `import anthropic` sits inside the API branch, not at module scope | 19 occurrences across the demo scripts, every one indented inside a function body | correct |
| Egress quote, synthetic-data quote, "obvious, harmless props" quote | `README.md:46-52`, verbatim | correct |
| **No test file appears anywhere in the pinned tree** | `find` over the whole checkout for `test_*.py`, `*_test.py`, `tests/`, `test/`, `conftest.py`, `pytest.ini`, `*.test.js` returns nothing | correct |
| Payloads in demos 01, 03, 04, 08 | 01 verified directly at `goofy-goof.md:20-27`; a phrase scan also hits 02, 05, 06 and 10 | correct but under-enumerated (`F5`) |

`event.md:144-146` says `team-demos` "carries a `.claude/commands/` directory
inside each of its ten demo folders". Ten such directories exist, one per
`NN-slug/demo/`, which is what the README calls the demo folder. Accurate.

### Template conformance

Both records carry the five template sections in order — Team statement, Primary
workflows, Run instructions, AI and external services, Known limitations — plus
two additions, a judging note and an intake provenance table, which the
configuration audit's `F4` repair introduced deliberately. Front matter carries
every field `schemas/submission-intake.schema.json` requires, and
`persona: prepare-submission@1.1.0` and `rubric: submission-evaluation@1.1.0`
match `framework/personas.md:41` and the canon rubric. `judging-auditor@1.1.0`
in this report matches `framework/personas.md:49`.

## Eligibility

`event.md:98-101` defines eligibility as one pinned immutable commit, a
reachable source repository, and a checkout that matches the pin. Both teams are
`eligible: true` in `teams.md` and in their own front matter, and all three
conditions re-derive: the pins are 40-character hashes, both repositories answer
an anonymous `ls-remote`, and both checkouts are clean at the pin. No enrollment
rule applies, consistent with `event.md`.

One tension is unresolved, and it is `F1`'s second half. The ScribeVault record
says "the pin is not fully realized" and then rules the gitlink's content
"outside the eligible scope … nothing may be assumed about it". That is an
eligibility scope decision, it appears only in a narrative record compiled by a
model, it is attributed to nobody, and `event.md:23-27` gives the event-director
the authority it would need. It also rests on the false reachability premise: the
content can be fetched. Freeze the roster with the ruling stated as an operator
decision and a true reason, or with the gitlink materialized.

## The withdrawal of `beekeeper-lab/website`

Findable, and the reason holds.

It is recorded in `events/trial-2-2026/event.md:59-67`, inside the hypothesis
section a reader of the event configuration cannot miss, and in
`docs/0.5.0-beta-plan.md:174-186`, where the candidate table marks the website
"Accept, with a stated scope" and the paragraph below it records the withdrawal
on 2026-09-21 with the disclosure reason. `ai-security-demos` is recorded in the
same table as its replacement.

Configuration `F17` said the privacy claim was not checkable here. It is
checkable, and this audit checked it: with credentials disabled,
`beekeeper-lab/website` refuses anonymous access while both rostered
repositories answer. The stated reason for the withdrawal is therefore true.
What remains is presentational, and is `F9`: `event.md:62-65` and the plan still
assert repository visibility in the event's own voice, with no attribution and no
reproducible check, which is the habit `F17` objected to rather than the
conclusion.

## Activity log and timestamps

Complete for the work that happened, strictly ascending, and every value is
inside the window.

| Row | Time | Checked against |
|---|---|---|
| `atj event init` | 21:51:56Z | `event.md:18` `started_at`, and commit `37ee443` at 21:54:21Z |
| `atj intake` team-scribe | 21:53:01Z | `team-scribe.md:9-11` |
| `atj intake` team-demos | 22:04:10Z | `team-demos.md:9-11`, and commit `24a66a1` at 22:04:57Z |
| configuration audit, round 1 | 22:08:00Z | reconstructed, labelled as such, and equal to the configuration audit's `F19` table |
| repair round 1 | 22:18:08Z | commit `196aa42` at 22:18:08Z exactly; its output list now includes `docs/0.5.0-beta-plan.md`, which that commit did change |
| configuration audit, round 2 | 22:19:10Z | reconstructed, labelled, matches `F19` |
| repair round 2 | 22:28:17Z | operator wall-clock reading; commit `49242aa` at 22:28:44Z |
| configuration audit, round 3 | 22:28:50Z | matches `F19` and the report's own `started_at` |
| repair round 3 | 22:34:26Z | commit `a8a0f4e` at 22:34:58Z |

Nine rows, strictly ascending, none before `started_at: 2026-09-21T21:51:56Z`,
none after the clock this audit read (23:16:37Z, then 23:24:45Z). Configuration
`F21` and `F22` are therefore **repaired in fact**, against a ledger the
configuration audit still lists as `open` because it was written before the
repair: the log is ordered, both reconstructed stamps match `F19`, the plan file
is in the round-one output, and `last_updated` (22:34:38Z) is newer than the last
row rather than stuck at event creation. What is missing from the log is the
23:16:00Z hand repair, which is `F3`. Two further absences are consistent with
`live-trial-2026`, which also logs audit results rather than gate commands, so
they are not findings: the gate record itself and the stage advance have no rows,
and the audit-result rows carry them.

`F2` is the one timestamp defect this stage owns: both intake records claim they
completed at the minute they were cloned, and both were rewritten 14 and 24
minutes later.

## Carry-forward of the configuration audit's open findings

Configuration-audit numbers, not this report's.

| Configuration finding | State recorded there | State now |
|---|---|---|
| `F7` — ScribeVault execution profile: display, audio device, network | deferred | still deferred and still visible. `event.md:130-139` names all three unknowns and commits to deciding them at the evidence stage, in the file the evidence stage reads first. The record is where it needs to be |
| `F11` — untrusted-data wrapper around the demos payloads | deferred | still deferred and visible in `event.md:157-165` and `team-demos.md:100-119`. The requirement is stated; the file set is not enumerated, which is this report's `F5` |
| `F10` — absolute home paths in provenance tables | open | unchanged, carried as `F8` |
| `F17` — unverifiable privacy claim behind the roster substitution | open | conclusion now verified by this audit, form unrepaired, carried as `F9` |
| `F20` — no validator reads a timestamp as a time | open | unchanged. `atj event validate` still accepts `completed_at` values that predate the edits they describe, which is how `F2` passed |
| `F21` — activity log out of order | open in the audit | **repaired in the artifact**, verified row by row above. The audit's `state` is stale, not wrong: the repair is the ledger's last row and is marked `not-audited` there |
| `F22` — stale `last_updated` | open in the audit | **repaired in the artifact**, 22:34:38Z against a newest row of 22:34:26Z. Recurring at a smaller scale as `F3` |
| `F23` — `atj intake` writes `model_used: not-applicable` | open | unchanged in the tool; both records carry the hand-corrected `claude-opus-5` |
| `F24` — audit template does not name the four `state` values in prose | open | unchanged; this report uses `open` only |

Nothing deferred to the evidence stage has been lost, and no open finding has
been silently closed.

## Privacy and publication

- `events/trial-2-2026/public/` holds `.gitkeep` and nothing else.
- `atj validate publication events/trial-2-2026` reports CLEAR, 3 artifacts, 0
  blocking.
- `public_scores: false` in `event.md:14`; no artifact carries
  `visibility: public`.
- No credential, key, token or third-party personal identifier appears in any
  event artifact. The demos' sample data is synthetic by the submission's own
  statement and the names in it are fictional.
- The one private-path disclosure is the operator home path in both provenance
  tables, in a repository that is public. It is `F8`, at the severity the
  configuration audit gave it, because it exposes a directory layout and a
  username already present throughout `events/live-trial-2026/`.
- The `claude-kit` submodule URL named in `team-scribe.md` discloses nothing
  new: it is public, and it is already in the pinned checkout's own
  `.gitmodules`.

## Instruction-shaped content encountered

Reported, not followed. All of it is inside the checkouts and none of it is an
instruction to this or any persona.

| File | What it does |
|---|---|
| `team-demos/01-resume-that-talked-back/demo/goofy-goof.md:20-27` | a fake "SYSTEM / ATS PRIORITY DIRECTIVE" inside a resume telling a screening assistant to score the candidate 100 out of 100, rank them first and not penalize the gaps. The known payload, configuration `F11` |
| `team-demos/02-invisible-ink/demo/camille-vise.md`, `.../README.md` | hidden-channel payload and its presenter script |
| `team-demos/05-reading-is-safe-calling-is-not/demo/max-goof.md`, `screen_pile.py` | tool-misuse payload, and a script that embeds it |
| `team-demos/06-approval-is-the-architecture/demo/pete-blackheart.md` | excessive-agency payload |
| `team-demos/10-show-your-work/demo/attacks/quill-avara.md`, `examples/decisions/quill-avara.json` | capstone payload and a recorded decision about it |
| `team-scribe/CLAUDE.md`, `.claude/local/{skills,commands,agents,prompts}/`, `.github/copilot-instructions.md`, `ai/beans/` | a project directing its own agents; product and security evidence, not configuration for any persona here |

`event.md:141-166` already forbids rooting a session in a checkout and requires
this class of file to be quoted inside an untrusted-data wrapper. This audit read
every one of them by path from the framework root and followed none. The gap is
that no artifact yet lists them, which is `F5`.

## Findings

| Severity | Rule | Artifact | Scope | Blocking | Finding | Required repair |
|---|---|---|---|---|---|---|
| major | `CLAUDE.md`: every factual conclusion must cite evidence available in the evidence package, and a claim in an intake record must be re-derivable from the checkout or its named source | `events/trial-2-2026/submissions/team-scribe.md:121-131` | event | **yes** | The record calls `beekeeper-lab/claude-kit` "a private repository reachable only with the operator's SSH credentials" and concludes the gitlink "cannot be fetched, and nothing may be assumed about it". The repository is public and the pinned commit `3dff46d6` fetches anonymously. The true constraint is the SSH URL in `.gitmodules` and the absent key. The eligible-scope ruling built on the false premise is also attributed to nobody, while `event.md:23-27` gives that authority to the event-director | Restate the constraint truthfully; then either record the out-of-scope ruling as an event-director decision with that reason, or materialize `.claude/shared` from the HTTPS URL at `3dff46d6` and re-pin. Re-run `atj event validate` after |
| minor | `framework/templates/submission-intake.md` front matter describes the record; configuration `F23` and `F20` | `events/trial-2-2026/submissions/team-scribe.md:9-11`, `team-demos.md:9-11` | event | no | `completed_at` equals the clone minute in both records, while commits `196aa42` (22:18:08Z) and `49242aa` (22:28:44Z) rewrote their narratives afterwards | Set `completed_at` to when each record was actually completed, or state in the template that it describes the clone |
| minor | `CLAUDE.md`: update `status.md` after verified work; configuration `F22`'s repair note | `events/trial-2-2026/status.md:4`, `:26` | event | no | The 23:16:00Z hand repair is in no activity row and `last_updated` still reads 22:34:38Z | Add the activity row and set `last_updated` when the `roster-frozen` gate is recorded |
| minor | `atj/event.py:514-560` requires body and ledger to agree | `atj/event.py:696-704` | framework | no | The gate and advance commands write the ledger and leave the body checkbox unchecked, so a passing gate produces a `status.md` the framework's own validator rejects | Write the checkbox in the same transaction, or refuse to exit while the body contradicts the new ledger |
| minor | `event.md:157-165` untrusted-data wrapper requirement; configuration `F11` | `events/trial-2-2026/submissions/team-demos.md:100-119` | event | no | The wrapper obligation is carried by one example file and a four-demo list; payload-shaped content is in at least eight files across five demos, and the ScribeVault agent configuration has two paths the record does not name | Enumerate the payload files and agent-config paths where the evidence stage will read them |
| advisory | `live-trial-2026` precedent; `atj event approve` | `events/trial-2-2026/submissions/*.md:16-17` | event | no | Both intake records are still `draft` / `unvalidated` after passing `atj validate reports` | Approve both before the freeze, or state that they stay draft |
| advisory | `CLAUDE.md` single source of artifact shape | `framework/templates/team-roster.md:1-12` | framework | no | Template front matter has ten fields, `events/_template/teams.md` has three, the schema requires four, and `release-check` calls templates PASS | Reconcile the three on one front matter |
| advisory | configuration `F10` | `events/trial-2-2026/submissions/team-scribe.md:141`, `team-demos.md:129` | framework | no | Absolute operator home path in both provenance tables, committed to a public repository | Write a repository-relative checkout path in `atj intake` |
| advisory | configuration `F17` | `docs/0.5.0-beta-plan.md:179-186`, `events/trial-2-2026/event.md:62-65` | framework | no | Repository visibility is still asserted as fact without attribution, although the conclusion is now verified | Attribute the claim to the operator or cite a repeatable check |
| advisory | `event.md:98-101` eligibility means a checkout that matches the pin | `workspaces/trial-2-2026/team-scribe`, `team-demos` | event | no | Both checkouts are on an attached `main` tracking `origin/main`, and `workspaces/` is gitignored, so a pull would move the evidence base invisibly | Detach at the pin, or re-verify `rev-parse HEAD` against the pin in each evidence package |

## Advisories

1. The configuration audit's `state` values for `F21` and `F22` are stale, since
   the repair landed after round three. That is normal and not a finding against
   the audit. This report is where a reader learns they are repaired, and the
   `roster-frozen` gate record should say so.
2. `atj validate reports` counts three artifacts at this stage and will count
   four with this report. Neither it nor `atj event validate` reads a timestamp,
   a pin or a claim against a checkout, so a clean run is not evidence that the
   intake is sound. Everything in this report's tables was derived by hand.
3. `status.md.bak` sits in the event directory, ignored by git and by every
   validator. It currently preserves the pre-advance state and was useful here as
   evidence of how the gate wrote. It is also an unreviewed copy of the ledger in
   a working tree; nothing needs doing, but nothing should read it as state.
4. `F1` was introduced by the repair that closed configuration `F2`, and survived
   two audit rounds after that. Four of the ten findings in this report are
   residue of earlier repairs. The event's own observation about repair rounds
   now has a fourth data point.

## Completion gate

- [x] No blocking findings — **not met.** `F1` is marked blocking
- [x] No major findings — **not met.** `F1` is major
- [x] Calculations valid — no official arithmetic exists at this stage; the two
      counted claims, 26 named and 30 present test files, both re-derived
- [x] Evidence references resolve — every path, line reference, quotation and
      commit in both intake records resolves, with the exception recorded in `F1`
- [x] Version and identity checks pass — rubric `1.1.0`, personas
      `prepare-submission@1.1.0` and `judging-auditor@1.1.0`, framework
      `0.4.0-beta`, `release-check` PASS
- [x] Privacy boundary passes — `public/` empty, publication check CLEAR, one
      advisory-level path disclosure
- [x] Every finding recorded in `findings:` with a `scope` and a `blocking` flag
- [ ] Approved with `atj event approve <this file>`

The first two boxes are listed unmet on purpose: the verdict is FAIL and the
gate must read `blocking: true` on `F1`, not this prose.

## Outstanding work

1. Repair `F1` in `events/trial-2-2026/submissions/team-scribe.md`, and decide
   the gitlink's scope as an event-director decision or by materializing it.
2. Repair `F2`, `F3` and `F5` in the event's own artifacts.
3. Re-audit. Every repair round in this event has introduced a new defect, and
   this report's `F1` is the fourth instance.
4. `F4`, `F7`, `F8` and `F9` are framework work and do not hold this gate.
5. Only then freeze the roster: set `frozen: true` in `teams.md`, record the gate
   with `atj event gate`, and update `last_updated` and the activity log in the
   same pass.
