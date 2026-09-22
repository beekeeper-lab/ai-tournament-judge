---
event_id: trial-2-2026
audit_scope: evidence stage
audit_id: evidence
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.1.0
persona: judging-auditor@1.1.0
framework_commit: 355f4582e124d2697bc16eb42d08d578a058bb5b
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-22T00:16:00Z"
completed_at: "2026-09-22T00:34:00Z"
visibility: private
approval_state: draft
validation_state: unvalidated
result: FAIL
audit_rounds: 1
findings:
- id: F1
  severity: major
  scope: event
  blocking: true
  summary: '`ev-scribe-11` says `OPENAI_API_KEY` "is read at three sites". There is a fourth, `src/ai/summarizer.py:54`, which reads the environment directly and bypasses the keyring-first chain in `settings.py`. R2, R3, R7 and R8 all cite this observation, and R8 rests specifically on its enumeration of the environment-variable fallback.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:95
  repair: 'Correct the count to four and add `src/ai/summarizer.py:54` to the observation and to its source reference. Say whether the direct environment read in `SummarizerService.__init__` bypasses the keyring path, because R7 is the claim that keys live in the keyring.'
  state: open
- id: F2
  severity: major
  scope: event
  blocking: true
  summary: '`ev-demos-05` says the hardened ranker "differs only in its system prompt" and that "the two prompts are the whole observable difference between the acts", and attributes the `<applicant>` wrapping to the system prompt. `build_user_content` also changed, and that is where the wrapping happens. The package''s own two run records show it: the vulnerable capture has 20 `=== Applicant file:` delimiters and no tags, the hardened capture has 20 `<applicant file=` tags and none of the former.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:88
  repair: 'Restate the delta from `diff rank_resumes.py hardened/rank_resumes_hardened.py`: the system prompt changed, and `build_user_content` changed from `=== Applicant file: {name} ===` / `APPLICANT MATERIALS:` to `<applicant file="{name}">…</applicant>` / `ROLE CRITERIA (trusted):` / `APPLICANT MATERIALS (untrusted data):`. Drop "differs only in its system prompt".'
  state: open
- id: F3
  severity: major
  scope: event
  blocking: true
  summary: '`evidence_limited_criteria: [functional]` for team-scribe contradicts the manifest''s own Missing-evidence section, which says the unreachable OpenAI paths limit R2, R3, R7 and R8 — the AI workflows and the key handling, not only `functional`. team-demos records `agentic` for the identical cause. Neither submission made a model call, and event.md:127-128 calls an evidence asymmetry between teams a defect against the event.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:15
  repair: 'Either add the criteria the Missing-evidence section already names, or state in the manifest why ScribeVault''s AI paths are assessable from source when the demos'' are not. Whichever is chosen, the two manifests must treat "no model call was possible" the same way.'
  state: open
- id: F4
  severity: minor
  scope: event
  blocking: false
  summary: 'The Tests-and-execution row for the scribe environment probe records a 300s timeout. `runs/team-scribe-envcheck-01.json` carries `limits.timeout_seconds: 600`.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:104
  repair: Change 300s to 600s. The other four scribe rows (1800, 120, 300, 300) match their run records.
  state: open
- id: F5
  severity: minor
  scope: event
  blocking: false
  summary: '`ev-demos-09` gives 213 files containing `example.com` and 210 containing `(555)`. At the pin the counts are 214 and 211. The file missing from both is the repository-root `README.md`; the scan appears to have been rooted at `*/`.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:92
  repair: Correct to 214 and 211, or state the scan root that excludes the top-level `README.md`.
  state: open
- id: F6
  severity: minor
  scope: event
  blocking: false
  summary: '`ev-demos-09` calls its e-mail scan "exhaustive", says it "returns three", and concludes no address at a resolvable domain appears "anywhere in the corpus". The scan covered `*.md`, `*.json` and `*.html` only. A fourth address, `talent@hexley.example`, sits at `06-approval-is-the-architecture/demo/tools/harness.py:181,218,242`. The conclusion survives because `.example` is reserved; the word "exhaustive" and the count do not.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:92
  repair: Either widen the scan to every file type and record four, or drop "exhaustive" and name the three extensions scanned as the scope of the claim.
  state: open
- id: F7
  severity: minor
  scope: event
  blocking: false
  summary: '`ev-scribe-10` and `ev-scribe-13` both give `runs/team-scribe-pytest-config-01.json` as the reproduction for "535 collected tests", and `ev-scribe-10` labels it "(collection count)". That run collected 38 items from one file. 535 comes from `runs/team-scribe-pytest-01.json`, as 509 + 26.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:94,97
  repair: Point the 535 to `runs/team-scribe-pytest-01.json` in both rows.
  state: open
- id: F8
  severity: minor
  scope: event
  blocking: false
  summary: '`ev-demos-13` says commit `3f484d5`''s message and `Containerfile.demos`''s header "both say" all 19 demo scripts. The commit message does. The Containerfile does not: it was repaired in commit 355f458, the same commit that added this manifest, and its header now carries the corrected text and cites ev-demos-13 itself.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:96
  repair: Put the Containerfile claim in the past tense and name commit 355f458 as where it was corrected, so a judge who opens the file finds what the observation describes.
  state: open
- id: F9
  severity: minor
  scope: event
  blocking: false
  summary: 'Two demos line ranges do not contain what is attributed to them. `ev-demos-03` cites `rank_resumes.py:92-101` for the dry run''s behaviour and its quoted final line; `if dry:` is at 103 and the quoted `[dry-run] …` print is line 105. `ev-demos-04` cites `:37-47` for the vulnerable system prompt; `SYSTEM` is 33-43, the quoted passage is 37-39, and 46-47 is inside `load_env()`.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:86,87
  repair: 'Change `ev-demos-03` to `:94-106` (or `:103-106`) and `ev-demos-04` to `:37-39` for the quoted passage or `:33-43` for the whole `SYSTEM` block.'
  state: open
- id: F10
  severity: minor
  scope: event
  blocking: false
  summary: 'The demos egress row says the probe ran "against nine hostile URLs". Nine URLs were exercised, of which three are localhost forms the guard is meant to admit and did admit; six were refused. Separately, `ev-demos-07`''s sub-claim that `--enforce-allowlist` refuses even a localhost beacon is a static read of `fetch_beacons.py:89` — `main()` was never called — inside an observation that opens "The egress guards were exercised directly".'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:90,107
  repair: Say "nine URL forms, six hostile", and mark the `--enforce-allowlist` consequence as a static read rather than part of what the run exercised.
  state: open
- id: F11
  severity: minor
  scope: event
  blocking: false
  summary: '`ev-scribe-14` is headed "Key storage as implemented" and cites `src/config/settings.py:286` for the read order keyring → encrypted config → environment. Line 286 is the docstring stating that priority. The implementation at 288-306 does match it, so the conclusion holds, but a docstring is a team claim and this observation is labelled a direct observation of the implementation.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:98
  repair: 'Cite `:288-306` for the implemented order, and keep `:286` only if it is named as the docstring that the implementation was checked against.'
  state: open
- id: F12
  severity: minor
  scope: event
  blocking: false
  summary: '`Supports` means "establishes" per `framework/templates/evidence-manifest.md`. `ev-scribe-06` and `ev-scribe-08` both list R1, while the R1 row says of those same two observations that "neither establishes or refutes the recording behaviour itself". A judge reading the Supports column alone counts two observations behind R1 that the manifest elsewhere says establish nothing about it.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:69,90,92
  repair: 'Drop R1 from both `Supports` cells and leave R1 resting on no observation, as R9 already does, or add one clause to each observation saying what about R1 it does establish (that the tests touching the recording path cannot run here).'
  state: open
- id: F13
  severity: minor
  scope: event
  blocking: false
  summary: 'Both manifests record `prepared_at` and `completed_at` as `2026-09-22T00:30:00Z` and the ledger records the work at `00:35:00Z`. The manifests were written at 00:14:55Z and committed in 355f458 at 00:15:17Z. A manifest cannot be prepared fifteen minutes after the commit that contains it. The run records'' own timestamps (00:02:42Z–00:07:26Z) are real; these three are rounded forward. This is the second recurrence of configuration audit F19.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:12-13
  repair: Set `completed_at` and `prepared_at` on both manifests, and the ledger row, to times that precede commit 355f458 at 00:15:17Z and are consistent with the run records.
  state: open
- id: F14
  severity: advisory
  scope: framework
  blocking: false
  summary: '`atj/reports.py:41` maps `runs/` to the `model-run` schema and template, and report validation globs only `*.md`. The 11 JSON sandbox execution records that every observation in this stage rests on are therefore validated by nothing — `atj validate reports` reported 6 artifacts and none was a run record. Same shape as the D22 note at `atj/reports.py:30-36`. live-trial-2026 did the same, so this is precedent, not a new event defect.'
  artifact: atj/reports.py:41
  repair: Framework work. Either register a sandbox-run schema for `runs/*.json` or record in the directory map that `runs/` holds two artifact kinds and only one is checked.
  state: open
- id: F15
  severity: advisory
  scope: event
  blocking: false
  summary: '`events/trial-2-2026/status.md.bak` sits in the event directory carrying `current_stage: intake` and the pre-evidence ledger. It is gitignored (`.gitignore:27`) and untracked, so it never reaches the repository, but a stale stage marker inside the event directory invites reading the wrong file.'
  artifact: events/trial-2-2026/status.md.bak
  repair: Delete it.
  state: open
- id: F16
  severity: advisory
  scope: event
  blocking: false
  summary: Neither manifest sets `execution_record`, which the evidence-manifest template carries. Nothing reads it and the schema does not require it, but with 11 run records the link from front matter to evidence exists only in prose.
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:14
  repair: Set it to the runs directory or to the primary run per team, or decide the field is unused and raise that against the template.
  state: open
- id: F17
  severity: advisory
  scope: event
  blocking: false
  summary: 'Both manifests are `approval_state: draft`. Nothing mechanical requires otherwise — `atj/event.py:214` checks approval only on the audit — but the intake stage approved both team records before its gate and the ledger records it.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:17
  repair: After the blocking findings are repaired, approve both manifests with `atj event approve` as intake did.
  state: open
- id: F18
  severity: advisory
  scope: event
  blocking: false
  summary: '`audits/configuration.md` F7 is still `state: deferred`, its repair line still reading "Evidence stage — record the display, audio-device and network answers as a decision in the image approval". That decision is now recorded at `evidence/team-scribe/manifest.md:52-58`, and the dry-run decision event.md:133-137 owed is recorded at `evidence/team-demos/manifest.md:47-57`. The earlier audit''s findings ledger no longer reflects the disk.'
  artifact: events/trial-2-2026/audits/configuration.md:70-77
  repair: 'Move F7 to `state: repaired` with a pointer to the manifest bullet that discharges it, when the configuration audit is next touched.'
  state: open
- id: F19
  severity: advisory
  scope: event
  blocking: false
  summary: 'event.md:126-127 says an image "carries what the submission declares, anything added beyond that is named in this file with the reason". `Containerfile.scribe:22-29` adds about twenty apt packages. Each is tied to a declared requirement in the Containerfile''s own comment at lines 12-18, which is a good record and arguably makes them prerequisites rather than additions, but event.md names none of them.'
  artifact: events/trial-2-2026/evidence/Containerfile.scribe:22-29
  repair: Either add a sentence to event.md pointing at the Containerfile comment as the register of system prerequisites, or state there that prerequisites of declared packages are not additions under that rule.
  state: open
---

# Judging Audit

## Result

**FAIL** until all blocking findings are resolved.

Three major findings, all `scope: event` and all `blocking: true`, hold the
`evidence-validated` gate. Each is a factual error inside an observation or a
front-matter field that the four initial judgments would read as settled
evidence. Sixteen further findings are minor or advisory and do not hold the
gate.

Execution safety is clean and is not the reason for the FAIL. Neither is the
citation graph's shape, the image provenance, or the handling of the two
recorded decisions — all of those verified correct and are recorded below so a
repair round does not disturb them.

## Scope and artifacts inspected

Evidence stage of `trial-2-2026` at `355f4582` on branch
`event/trial-2-2026-evidence`.

Read in full: both manifests, `Containerfile.scribe`, `Containerfile.demos`, all
11 `runs/*.json`, `status.md`, `event.md`, `teams.md`, both `submissions/*.md`,
`audits/configuration.md` and `audits/intake.md` front matter,
`framework/policies/execution-safety.md`,
`framework/policies/evidence-and-citation.md`,
`framework/templates/evidence-manifest.md`,
`framework/templates/audit-report.md`, `framework/rubrics/README.md`,
`framework/rubrics/submission-evaluation.md`,
`schemas/evidence-manifest.schema.json`, `schemas/model-run.schema.json`,
`atj/reports.py` directory map and `atj/event.py` gate logic.

Both pinned checkouts were read at their pins, read-only, and nothing in either
was executed. An AST scan of the demos tree was attempted and the project's
`pre-advance.sh` hook blocked it as host execution of submission code; the same
questions were answered with `grep` and `git grep` instead, which is the correct
outcome and the guard rail behaving as designed.

## Deterministic validation results

| Check | Result |
|---|---|
| `atj event validate events/trial-2-2026` | PASS, 0 problems, stage evidence |
| `atj validate reports events/trial-2-2026` | PASS, 6 artifacts, 0 findings |
| `atj validate publication events/trial-2-2026` | CLEAR, 6 artifacts, 0 blocking |
| `atj release-check` | PASS, all 13 checks |
| `atj event status events/trial-2-2026` | stage evidence, gate `evidence-validated` pending |
| `atj sandbox preflight` | AVAILABLE, podman 6.1.0 (rootless) |

None of the three blocking findings is visible to any of these. That is the
point `framework/rubrics/README.md` makes under "What validation cannot tell
you", and this stage is another instance of it: a green report validation over
manifests containing a miscount, a false mechanism and a wrong front-matter
field.

## What was verified true

Recorded so a repair round does not churn correct work.

**Counts and quotations, re-derived against the pinned checkouts.** team-scribe:
56 `.py` under `src/`; 30 `tests/test_*.py`; 509 passed and 26 failed with the
split 13 `test_thread_safety.py` + 7 `test_main_page_speaker.py` + 3
`test_pipeline_status.py` + 3 `test_checkpoint.py`, so 13 + 10 + 3 = 26 with no
remainder; 509 + 26 = 535 collected; `README.md`'s table names 26 files across 9
categories, four short of the 30 on disk; 168 files under `ai/beans/` across 54
`BEAN-*` directories plus two root files; 6 under `ai/reports/`; 3 commands and 3
`SKILL.md`; the `.claude/shared` gitlink uninitialized at `-3dff46d6`; eight
`src/` packages plus `assets`; the README cost figures `$0.00`, `~$0.36`, `~$131`
at `README.md:150-151`. team-demos: 399 tracked files; 53 `.py` with the
breakdown 17 demo-root + 17 `scripts/` + 9 `hardened/` + 8 `tools/` + 2 parser
versions; 19 files importing `anthropic`, every one of them function-scoped and
none at module scope; 66 `.claude` files across all ten demos with none at the
repository root; 201 resumes under `*/resumes/`; 20 resumes in demo 01 with
`goofy-goof.md` absent from them; ten `NN-*/` directories and ten
`demo/README.md`; no dependency manifest of any kind; no test file of any kind;
"Sift" in all ten demos and "Marisol" in seven, absent from 01, 03 and 08.

**Line citations.** Every scribe line reference resolves to what is claimed:
`qt_app.py:11,48,54,310,315`, `requirements.txt:19,25`, `requirements.lock:16`,
`setup_pyside6.py:82`, `main.py:50`, `conftest.py:19-30`,
`test_thread_safety.py:24,34,122,281`, `test_checkpoint.py:65,72,77`,
`recorder.py:130,165`, `pytest.ini:1` with its five markers,
`test_pipeline_status.py:298,355,404`, `test_main_page_speaker.py:66`,
`settings.py:388,393`, and all four hops of the
`qt_main_window.py:30 → _actions.py:25 → workers/__init__.py:3 →
recording_worker.py:17 → qt_app.py:11` chain. On the demos side
`fetch_beacons.py:42-67,83-90`, `parser.py:90-107,109-112`,
`attacker.py:4-12,36-37,93-96` and `README.md:31,33,34,70` all resolve. The two
that do not are F9.

**Image provenance, independently re-derived.** `podman image inspect` returns
`034af8181f8d19d6…` and `sha256:bdbb5d5a422dd262…` created 2026-09-21T23:52:54Z
for the scribe tag, matching the manifest exactly. The superseded build exists,
untagged, at `sha256:25a2208baadd6280…` created 23:51:31Z, which is 83 seconds
earlier, and commit `3f484d5`'s message does name that digest. The demos tag
resolves to `ec7d6c95cd3692a2…`, byte-identical to
`docker.io/library/python:3.12-slim`, as the manifest says. Both provenance
corrections in the manifests are correct and were worth making.

**Execution safety, checked against the run records' own fields rather than the
manifests' description of them.** All 11 records: `podman run`, `--network
none`, `--read-only`, `--cap-drop ALL`, `--security-opt no-new-privileges`,
`--user 65534:65534`, `--tmpfs /tmp:rw,noexec,nosuid,size=64m`, `--pids-limit
256`, `--memory 1g`, `--cpus 1.0`, submission mounted `:ro,Z`. No record has
`timed_out: true` or `output_truncated: true`. Only the two approved images
appear. Nothing ran on the host. `atj sandbox preflight` re-run during this audit
returns AVAILABLE, podman 6.1.0 (rootless), matching what both manifests claim
preceded execution. One recorded limit is described wrongly in prose and that is
F4; the enforced control itself is sound in every case.

**The recorded decisions.** Configuration F7 is discharged at
`evidence/team-scribe/manifest.md:52-58` — offscreen, no display, no audio
device, no network, no simulated microphone — with the consequences routed to
Missing evidence and the affected criterion to front matter. The dry-run decision
event.md:133-137 owed is discharged at `evidence/team-demos/manifest.md:47-57`,
correctly framed as the event's choice rather than the team's deficiency, with
the reason stated (`uv run --with anthropic` resolves from PyPI against an empty
allowlist) and verified: `import anthropic` does sit below the dry-run return, so
the plain interpreter reaches the same output. The intake F11 whole-checkout
wrapper is restated in both manifests and the nine-file phrase scan is correctly
described as a floor rather than an inventory.

**No steering, on either submission.** `goofy-goof.md` — the payload that
directs a screening agent to assign 100 and rank first — is absent from all 11
run records, which is consistent with `ev-demos-06`: it is not staged into
`resumes/` at the pin. Neither manifest adopts either submission's framing. The
demos manifest marks its central claim R4 as `NE`, warns at Missing item 4 that a
dry run is not agent behaviour, and warns at item 6 against scoring an
evasiveness the submission never claimed. The scribe manifest contradicts R5 on
direct observation, marks R9 a team claim resting on no observation at all, and
records a property of the KDF input that the team's claim does not state.
ScribeVault's `CLAUDE.md` and `.github/copilot-instructions.md` contain no
scoring or judging directive. H6 is not contested by this stage's artifacts.

**The GUI point.** Missing item 4 in the scribe manifest states that both GUI
modules fail to import because of a cause inside the submission, cites
`ev-scribe-03`, and says a judge should not record it as evidence-limited. That
is correct and correctly excluded from `evidence_limited_criteria`, whose
`functional` entry rests on the audio device and the empty allowlist instead.
F3 is about what is missing from that field, not about the GUI.

**Citation graph.** Every `[[evidence:…]]` in both manifests resolves, and every
observation's `Supports` cell agrees with the requirements that cite it, in both
directions, with `ev-scribe-13` and `ev-demos-13` correctly carrying `-`. R9 in
the scribe manifest deliberately rests on no observation and says so. The one
place where the graph is formally satisfied but semantically strained is F12.

**Status ledger.** The final row is accurate: 11 runs, images `034af8181f8d` and
`ec7d6c95cd36`, and an Output list that matches commit 355f458's file list
exactly, including the fact that `Containerfile.scribe` was not touched.
`current_stage: evidence`, both gate flags, both evidence package ids
(`63f56c93`, `1c0b2b5e`) and both `sandboxed-partial, draft` entries match the
manifests on disk. `public/` holds only `.gitkeep`. The one defect in the ledger
is the timestamp, F13.

## Findings

| Severity | Rule | Artifact | Scope | Blocking | Finding | Required repair |
|---|---|---|---|---|---|---|
| major | evidence-and-citation.md, direct observation must be true | `evidence/team-scribe/manifest.md:95` | event | yes | F1 — `ev-scribe-11` says `OPENAI_API_KEY` is read at three sites; `src/ai/summarizer.py:54` is a fourth, reading the environment directly and bypassing the keyring chain. R2, R3, R7 and R8 cite this observation | Correct to four sites, add `summarizer.py:54`, and say whether it bypasses the keyring path that R7 claims |
| major | evidence-and-citation.md, direct observation must be true | `evidence/team-demos/manifest.md:88` | event | yes | F2 — `ev-demos-05` says the hardened ranker "differs only in its system prompt"; `build_user_content` also changed, and that is where the `<applicant>` wrapping happens. Both run records show it | Restate the delta from the diff; the system prompt and the user-content builder both changed |
| major | event.md:127-128, evidence asymmetry is a defect against the event | `evidence/team-scribe/manifest.md:15` | event | yes | F3 — `evidence_limited_criteria: [functional]` contradicts the manifest's own Missing item 2, which limits R2, R3, R7 and R8; team-demos records `agentic` for the identical no-model-call cause | Add the criteria the Missing-evidence section names, or state why the two teams are treated differently |
| minor | execution-safety.md, record the limits applied | `evidence/team-scribe/manifest.md:104` | event | no | F4 — the environment-probe row says 300s; the run record carries 600s | Change 300s to 600s |
| minor | evidence-and-citation.md, cite what is there | `evidence/team-demos/manifest.md:92` | event | no | F5 — `example.com` and `(555)` counts are 213 and 210; the pin holds 214 and 211, the difference being the root `README.md` | Correct to 214 and 211, or state the scan root |
| minor | evidence-and-citation.md, do not manufacture certainty | `evidence/team-demos/manifest.md:92` | event | no | F6 — the e-mail scan is called "exhaustive" and returns three; it covered three extensions and missed `talent@hexley.example` in `harness.py` | Widen the scan and record four, or drop "exhaustive" and scope the claim |
| minor | evidence-manifest.md, Reproduction must reproduce | `evidence/team-scribe/manifest.md:94,97` | event | no | F7 — 535 collected tests is attributed to `pytest-config-01`, which collected 38 from one file; it comes from `pytest-01` | Point the 535 at `runs/team-scribe-pytest-01.json` in both rows |
| minor | evidence-and-citation.md, cite what is there | `evidence/team-demos/manifest.md:96` | event | no | F8 — `ev-demos-13` says `Containerfile.demos` currently says "all 19 demo scripts"; it was corrected in the same commit that added the manifest | Put the Containerfile claim in the past tense and name commit 355f458 |
| minor | evidence-and-citation.md, cite line or symbol | `evidence/team-demos/manifest.md:86,87` | event | no | F9 — `ev-demos-03` cites `:92-101` for output produced at 105; `ev-demos-04` cites `:37-47` for a `SYSTEM` block ending at 43 | Change to `:94-106` and `:37-39` (or `:33-43`) |
| minor | evidence-and-citation.md, keep classes distinct | `evidence/team-demos/manifest.md:90,107` | event | no | F10 — "nine hostile URLs" describes nine URL forms of which three are localhost and admitted; the `--enforce-allowlist` consequence is a static read inside an observation headed as exercised | Say "nine URL forms, six hostile" and mark the allowlist consequence as a static read |
| minor | evidence-and-citation.md, team claim is not observation | `evidence/team-scribe/manifest.md:98` | event | no | F11 — `ev-scribe-14` cites `settings.py:286`, a docstring, for what is labelled the implemented read order; the implementation at 288-306 does match | Cite `:288-306` for the implemented order |
| minor | evidence-manifest.md, Supports means establishes | `evidence/team-scribe/manifest.md:69,90,92` | event | no | F12 — `ev-scribe-06` and `ev-scribe-08` claim to support R1 while the R1 row says neither establishes nor refutes the recording behaviour | Drop R1 from both Supports cells, or state what about R1 each does establish |
| minor | evidence-manifest.md, timestamps must be observed | `evidence/team-scribe/manifest.md:12-13` | event | no | F13 — both manifests' `prepared_at`/`completed_at` of 00:30:00Z and the ledger's 00:35:00Z postdate the 00:15:17Z commit containing them; the run timestamps are real, these are rounded forward | Set all three to times preceding commit 355f458 and consistent with the run records |
| advisory | atj/reports.py:41 directory map | `atj/reports.py:41` | framework | no | F14 — `runs/` is mapped to the `model-run` schema and validation globs only `*.md`, so the 11 JSON run records are checked by nothing | Register a sandbox-run schema, or record that `runs/` holds two artifact kinds |
| advisory | event hygiene | `events/trial-2-2026/status.md.bak` | event | no | F15 — a gitignored backup carrying `current_stage: intake` sits in the event directory | Delete it |
| advisory | evidence-manifest.md front matter | `evidence/team-scribe/manifest.md:14` | event | no | F16 — `execution_record` is unset on both manifests | Set it, or raise the unused field against the template |
| advisory | intake-stage precedent | `evidence/team-demos/manifest.md:17` | event | no | F17 — both manifests are `approval_state: draft`; intake approved its team records before its gate | Approve both after the blocking repairs |
| advisory | audit ledger hygiene | `audits/configuration.md:70-77` | event | no | F18 — configuration F7 is still `state: deferred` although the manifests discharge it | Move F7 to `repaired` with a pointer to the manifest bullet |
| advisory | event.md:126-127 image rule | `evidence/Containerfile.scribe:22-29` | event | no | F19 — about twenty apt packages are added and reasoned in the Containerfile, not named in event.md as the rule directs | Point event.md at the Containerfile comment, or state that prerequisites of declared packages are not additions |

## Advisories

Three observations that are not findings.

**The blocking three are all of one kind.** Each is a claim that reads as
settled, is checkable in one command, and was not checked: a `grep` for
`OPENAI_API_KEY`, a `diff` of two files in the same demo, and a read of the
manifest's own Missing-evidence section against its own front matter. None
required judgment to catch. That is consistent with `live-trial-2026`, where the
LLM audit was the only thing that caught any substantive error, and it argues for
running those three checks mechanically before the next manifest is written
rather than after.

**The evidence packages are, on the whole, unusually disciplined.** The refusals
are the strongest part: R9 resting on no observation and saying so, R6's "traces
to no real individual is not verifiable from the checkout and is not claimed
here", Missing item 4 in the demos manifest telling a judge in advance that it
will have over-read the dry run, and Missing item 4 in the scribe manifest
telling a judge not to treat the GUI failure as an evidence limit. The
`NE`-versus-low-score boundary this event exists to test is handled correctly on
the one case that matters: team-demos has no test suite, and R7 records that as a
direct observation of absence rather than as an evidence limit, which is the
distinction D8 and D12 were found on.

**F13 is the third appearance of invented timestamps on this event.**
Configuration F19 was about the auditor's own, the intake ledger needed an
ordering repair, and now both manifests and the ledger carry preparation times
that postdate the commit containing them. Nothing downstream reads these fields,
which is why it stays minor, but three recurrences of one defect class on one
event is a process signal rather than three separate slips.

## Completion gate

- [ ] No blocking findings — three, F1, F2 and F3
- [ ] No major findings — three
- [x] Calculations valid — 13 + 10 + 3 = 26 and 509 + 26 = 535 both reproduce against `runs/team-scribe-pytest-01.json`
- [x] Evidence references resolve — every `[[evidence:…]]` and every `runs/*.json` named; two line ranges are wrong (F9) but resolve to real files
- [x] Version and identity checks pass — rubric `submission-evaluation@1.1.0`, persona `prepare-submission@1.1.0`, framework commit `3f484d5` correct for the preparation window, both evidence package ids well-formed and matching their commits
- [x] Privacy boundary passes — both manifests private, `public/` empty, `atj validate publication` CLEAR
- [x] Every finding recorded in `findings:` with a `scope` and a `blocking` flag
- [ ] Approved with `atj event approve <this file>`

## Repairs required to clear this audit

1. `evidence/team-scribe/manifest.md:95` — F1, the fourth `OPENAI_API_KEY` read
   site at `src/ai/summarizer.py:54`.
2. `evidence/team-demos/manifest.md:88` — F2, the hardened variant's real delta,
   which includes `build_user_content`.
3. `evidence/team-scribe/manifest.md:15` — F3, `evidence_limited_criteria`
   reconciled with the manifest's own Missing-evidence section and with the
   demos manifest.

The sixteen minor and advisory findings should be repaired in the same round
because they touch the same two files, but none of them holds the gate.

Then re-audit. `framework/rubrics/README.md` requires the repair round to be
audited before the gate is set, and nine of the defects in `live-trial-2026`
were introduced by repairs. `atj event gate` reads the last audit, not the first
one that passed.
