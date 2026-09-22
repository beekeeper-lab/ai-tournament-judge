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
framework_commit: 79455e698d04ed2bd2db56a915e157b795ab1838
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-22T00:42:00Z"
completed_at: "2026-09-22T00:56:33Z"
visibility: private
approval_state: draft
validation_state: unvalidated
result: PASS WITH ADVISORIES
audit_rounds: 2
findings:
- id: F1
  severity: major
  scope: event
  blocking: false
  summary: 'Round 1 — `ev-scribe-11` said `OPENAI_API_KEY` "is read at three sites" and omitted `src/ai/summarizer.py:54`. Round 2 repaired it and re-derived correctly: the observation now names four sites (`settings.py:303,332`, `whisper_service.py:96`, `summarizer.py:54`), keeps `whisper_service.py:449` as a report rather than a read, and answers the question R7 needed answered — `whisper_service.py:92-96` and `summarizer.py:50-54` are one fallback pattern written twice, each asking `settings_manager.get_openai_api_key()` first and reading the environment only when no settings manager was supplied, so a caller that constructs either service without one bypasses the keyring and the encrypted store. Verified against the pin: `git grep OPENAI_API_KEY` returns exactly those five `src/` occurrences, and the two constructors read as described.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:122
  repair: Done. No further work.
  state: repaired
- id: F2
  severity: major
  scope: event
  blocking: false
  summary: 'Round 1 — `ev-demos-05` said the hardened ranker "differs only in its system prompt". Round 2 repaired it from the diff: the observation now names two changes, quotes the submission''s own docstring ("Two changes carry the whole fix", `hardened/rank_resumes_hardened.py:5`), cites the system prompt at `:33-44` and `build_user_content` at `:67-70`, states that neither works without the other, and gives the mechanical proof from the two run records. Verified: `diff rank_resumes.py hardened/rank_resumes_hardened.py` shows exactly those two substantive hunks, and the captures hold 20 `=== Applicant file:` headers against 20 `<applicant file=` tags. Two residuals at advisory: F26 and F28.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:92
  repair: Done. No further work.
  state: repaired
- id: F3
  severity: major
  scope: event
  blocking: false
  summary: 'Round 1 — `evidence_limited_criteria: [functional]` for team-scribe contradicted the manifest''s own Missing-evidence section and differed from team-demos for the identical no-model-call cause. Round 2 added `agentic`, so both manifests now record `[functional, agentic]`, and argued rather than conceded the rest: `security` is deliberately not listed because the key-handling implementation is entirely readable and was read. That argument holds. `atj/reports.py:274-296` is what consumes this field — it requires an `NE` criterion''s confidence to be `high` when the criterion is listed and `low` when it is not — and a `security` `NE` would in fact rest on evidence a judge can find at `settings.py:288-414`. The symmetry event.md:127-128 demands is satisfied: the two manifests now carry the same list for the same cause.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:16
  repair: Done. No further work.
  state: repaired
- id: F4
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1 — the scribe environment-probe row said 300s where `runs/team-scribe-envcheck-01.json` carries 600. Round 2 changed it to 600s. Re-derived: all eleven run records were re-read and all five scribe rows (600, 1800, 120, 300, 300) and the demos rows (120 throughout) now match their records.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:131
  repair: Done. No further work.
  state: repaired
- id: F5
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1 — `ev-demos-09` gave 213 and 210 where the pin holds 214 and 211, and this audit diagnosed the missing file as the repository-root `README.md`. Round 2 corrected the counts and corrected the diagnosis: the observation now reads "213 `.md` files (214 files of any type)" and "210 `.md` files (211 of any type)", which reproduces exactly. The one non-`.md` file in both sets is `02-invisible-ink/demo/resumes-html/camille-vise.html`, not the root `README.md`. Round one''s explanation was wrong and the repair round caught it.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:96
  repair: Done. No further work.
  state: repaired
- id: F6
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1 — the e-mail scan was called "exhaustive", returned three, and missed `talent@hexley.example`. Round 2 widened the scan and records four, dropped "exhaustive", and states the scope as "every text file in the tree, `.git` excluded". Re-derived independently: a regex sweep of the whole tree returns exactly four addresses outside `example.com` — `review@parser-helper.example` (9 occurrences), `talent@hexley.example` (3), `localhost@evil.example` (2), `hiring-manager@hexley.example` (1) — all four `.example`, so the conclusion is unchanged and now rests on the scan that was actually run.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:96
  repair: Done. No further work.
  state: repaired
- id: F7
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1 — 535 collected tests was attributed in two rows to `runs/team-scribe-pytest-config-01.json`, which collected 38 items from one file. Round 2 points both rows at `runs/team-scribe-pytest-01.json`, `ev-scribe-10` annotating it "(509 + 26 = 535)" and `ev-scribe-13` "(535 collected)". Verified against the record: its output ends "26 failed, 509 passed in 4.71s"; the config run''s output ends "38 passed".'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:121,124
  repair: Done. No further work.
  state: repaired
- id: F8
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1 — `ev-demos-13` said `Containerfile.demos`''s header currently says "all 19 demo scripts" when commit 355f458 had already corrected it. Round 2 puts the claim in the past tense and names the commit: the header "said the same until commit `355f458` corrected it alongside this manifest". Verified: `git show 355f458 -- Containerfile.demos` is the commit that changed it, and the file on disk now carries the corrected parenthetical citing ev-demos-13.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:100
  repair: Done. No further work.
  state: repaired
- id: F9
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1 — two demos line ranges did not contain what was attributed to them. Round 2 repaired both and propagated the change to every place the same lines are cited. `ev-demos-03` is now `:103-106`, which is `if dry:` through the `return 0`, with the quoted final line at 105. `ev-demos-04` is now `:33-43`, the whole `SYSTEM` literal, with "the sentence at `:37-39`" for the quoted passage; the key-file row follows. `ev-demos-02`, the key-file row and the dry-run decision bullet all moved from `:93-110` to `:103-109`, which is the dry-run branch through `import anthropic` at 109. All four re-derived against the pin.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:90,91
  repair: Done. No further work.
  state: repaired
- id: F10
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1 cited two places, `manifest.md:90,107`, and round 2 repaired one. `ev-demos-07` is now correct and better than the repair asked for: "nine URL forms of which six are hostile", the three local forms named, the `--enforce-allowlist` consequence marked as read from `fetch_beacons.py:88-91` and explicitly "not exercised, because no rendered assessment exists for the flag to scan". All of that verified — the run output shows three `True` and six `False`, `ALLOWLIST = set()` observed in the same run, lines 88-91 are guard 2, and `07/demo/reports/` does not exist at the pin so `render_html()` exits. What was not repaired is the Tests-and-execution row, which still reads "`is_localhost` and `_post_to_localhost` against nine hostile URLs". A judge reading the execution table gets the count the observation now disowns.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:111
  repair: Change "nine hostile URLs" in the Tests-and-execution row to "nine URL forms, six hostile", matching `ev-demos-07`.
  state: open
- id: F11
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1 — `ev-scribe-14` cited `settings.py:286`, a docstring, for what the observation labels the implemented read order. Round 2 cites "implemented at `:288-306`; the docstring at `:286` states the same order", and the key-file row moved from `:286-414` to `:288-414`. Verified: 283 is the `def`, 284-287 the docstring, and 288-306 is exactly keyring, then encrypted config, then the environment fallback. Class discipline is now correct — the implementation is the observation and the docstring is named as the team claim it was checked against.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:125
  repair: Done. No further work.
  state: repaired
- id: F12
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1 — `ev-scribe-06` and `ev-scribe-08` both listed R1 in `Supports` while the R1 row said neither establishes nor refutes the recording behaviour. Round 2 took the second option and rewrote the R1 row to say what each does establish: the capture path is reached and its error contract holds (`recorder.py:130` raises inside real PyAudio, `:165` wraps it as `AudioException`), and `AudioRecorder`''s thread-safety and cleanup behaviour is untested in the declared environment. Both halves verified at the pin, and the row still closes "Neither establishes recording, checkpoint flushing or `recover_checkpoints()`", so the refusal is preserved. One factual slip inside the new text is F21.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:96
  repair: Done, apart from F21.
  state: repaired
- id: F13
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1 required three timestamps moved: `prepared_at` and `completed_at` on both manifests, and the ledger row. Round 2 moved the manifests to `2026-09-22T00:14:00Z`, which is after the last run record (00:07:26Z) and before commit 355f458 (00:15:17Z), so the manifests are repaired. The ledger row for the preparation work still reads `2026-09-22T00:35:00Z`; only its outcome column changed, to "FAIL — see audits/evidence.md". That row still records the work twenty minutes after the commit that contains it.'
  artifact: events/trial-2-2026/status.md:70
  repair: Set the preparation row's timestamp to a time between the last run record (00:07:26Z) and commit 355f458 (00:15:17Z), consistent with the manifests' 00:14:00Z.
  state: open
- id: F14
  severity: advisory
  scope: framework
  blocking: false
  summary: '`atj/reports.py:41` maps `runs/` to the `model-run` schema and template, and report validation globs only `*.md`. The 11 JSON sandbox execution records that every observation in this stage rests on are therefore validated by nothing — `atj validate reports` returned 7 artifacts this round, one more than last round because this report was added, and none of the 7 is a run record. Left open deliberately by the repair round: registering a sandbox-run schema is a framework change and this stage declined to make one mid-event. That is the right call under the rule against changing framework shape during an active event, and it is recorded here so the next framework window inherits it rather than the event.'
  artifact: atj/reports.py:41
  repair: Framework work, out of scope for this stage. Either register a sandbox-run schema for `runs/*.json` or record in the directory map that `runs/` holds two artifact kinds and only one is checked.
  state: open
- id: F15
  severity: advisory
  scope: event
  blocking: false
  summary: 'Round 1 — a gitignored `status.md.bak` carrying `current_stage: intake` sat in the event directory. Round 2 deleted it. Verified: the file is absent and `git status --porcelain --ignored events/trial-2-2026/` returns nothing at all.'
  artifact: events/trial-2-2026/status.md.bak
  repair: Done. No further work.
  state: repaired
- id: F16
  severity: advisory
  scope: event
  blocking: false
  summary: 'Round 1 — `execution_record` was unset on both manifests. Round 2 sets it to `runs/team-scribe-*.json` and `runs/team-demos-*.json`. The schema types the field as `["string", "null"]`, so a glob is valid, and both globs resolve to the five and six records their manifests cite.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:15
  repair: Done. No further work.
  state: repaired
- id: F17
  severity: advisory
  scope: event
  blocking: false
  summary: 'Round 1 — both manifests were `approval_state: draft` where intake had approved its records before its gate. Round 2 set both to `approved` with `approved_by: event-director`, an `approved_at` and an `approval_note` naming the findings each repair round closed, which is the shape intake used. The condition is met. How it was met is F24.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:18
  repair: Done, apart from F24.
  state: repaired
- id: F18
  severity: advisory
  scope: event
  blocking: false
  summary: 'Round 1 — `audits/configuration.md` F7 was still `state: deferred` although the manifests discharge it. Round 2 moved it to `state: repaired` with a repair line pointing at the scribe manifest''s Scope and provenance section and restating the decision it records. Correct, and the pointer names a section rather than line numbers, which survives edits. The absence of any note that an approved report was amended is F25.'
  artifact: events/trial-2-2026/audits/configuration.md:73-77
  repair: Done, apart from F25.
  state: repaired
- id: F19
  severity: advisory
  scope: event
  blocking: false
  summary: 'Round 1 — the scribe image adds apt packages that event.md:126-128 says must be named there with a reason. Round 2 argued rather than conceded, in a new Scope bullet: nothing is added, because an OS-level prerequisite of a declared Python package is not an addition. The argument holds. `requirements.txt:18` declares `PySide6` and `:19` declares `pyaudio`; without `portaudio19-dev`, `gcc` and `python3-dev` the declared `pyaudio` cannot build, and without the GL/xcb/glib set the declared `PySide6` cannot link. An image that omitted them would carry less than the submission declares, not more, so event.md''s rule is satisfied without an event.md edit. Three factual defects inside the bullet that makes the argument are F22.'
  artifact: events/trial-2-2026/evidence/Containerfile.scribe:22-29
  repair: Done as an argument, and the argument is accepted. The supporting facts need F22.
  state: repaired
- id: F20
  severity: minor
  scope: event
  blocking: false
  summary: 'Fourth recurrence of the invented-timestamp class on this event, and this time introduced by the round that repaired the third. Commit `79455e6` carries `approved_at: "2026-09-22T00:52:00Z"` on both manifests, `last_updated: "2026-09-22T00:55:00Z"` in `status.md`, and a ledger row stamped `00:55:00Z`. That commit was authored and committed at `2026-09-21T20:41:29-04:00`, which is `2026-09-22T00:41:29Z`. All three postdate the commit containing them by eleven to fourteen minutes, and all three were still in the future when this audit read the system clock at `00:48:46Z`. The manifests'' own `prepared_at`/`completed_at` were repaired correctly in the same commit, so the defect was understood and then repeated in the fields the repair itself added.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:20
  repair: 'Set `approved_at` on both manifests, `last_updated`, and the final ledger row to the time the work was actually done. `atj event approve` stamps this field from `versions.now()` and would not have produced these values; see F24.'
  state: open
- id: F21
  severity: minor
  scope: event
  blocking: false
  summary: 'Introduced by the F12 repair. The rewritten R1 row says "the thread-safety and cleanup behaviour of `AudioRecorder` is untested in the declared environment, because the thirteen tests written for it cannot run there". Twelve of the thirteen were written for `AudioRecorder` — four in `TestAudioRecorderThreadSafety`, seven in `TestAudioRecorderCleanup`, and `TestNoDeadlocks::test_recorder_no_deadlock`. The thirteenth, `TestNoDeadlocks::test_settings_no_deadlock` at `tests/test_thread_safety.py:311`, constructs a `SettingsManager` and exercises lock contention on `save_settings`/`_load_settings`; it fails for the same module-level `reset_mock` reason, but it is not a test of the recorder. `ev-scribe-06` itself says only "thirteen tests in `tests/test_thread_safety.py`", which is right; the attribution to `AudioRecorder` is new in the R1 row.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:96
  repair: Say twelve of the thirteen, or drop `AudioRecorder` from the clause and describe the thirteen as the thread-safety file.
  state: open
- id: F22
  severity: minor
  scope: event
  blocking: false
  summary: 'Introduced by the F19 repair, in the bullet that carries the argument. Three defects. First, "Each is tied to the requirement it serves in `Containerfile.scribe:19-29`": the comment that ties each package to a declared requirement is at `:12-18`; `:19-20` is the display-and-audio note, `:21` is the `FROM`, and `:22-28` is the `RUN`. Round one cited `:12-18` correctly and the repair moved the citation off it. Second, "the roughly twenty `apt` packages": the `RUN` at `:22-28` installs 27. Round one said "about twenty" and the repair inherited the number without re-deriving it. Third, the comment at `:12-18` that the bullet points to does not name `libice6` or `libxkbcommon-x11-0`, so "each is tied to the requirement it serves" is not true of two of the 27, although both are genuine transitive prerequisites (`libsm6` needs `libICE`; the xcb set needs `libxkbcommon-x11`). None of this touches the argument, which is accepted under F19.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:47-58
  repair: Cite `Containerfile.scribe:12-18` for the comment and `:22-28` for the install, say 27, and either add the two missing packages to the Containerfile comment or say the comment names the classes rather than every package.
  state: open
- id: F23
  severity: minor
  scope: event
  blocking: false
  summary: 'Introduced by the F2 repair, in the demos R9 row. The rewritten evidence status describes `ev-demos-04` and `ev-demos-05` as "the same 20-resume corpus under two different instruction boundaries … with the payload text untouched on both sides". There is no payload text on either side. `ev-demos-06` establishes that `goofy-goof.md` is not staged into `resumes/` at the pin, and a scan of the 20 staged resumes for the payload''s own phrasing — "score of 100", "rank them first", "pre-approved", ATS or recruiting-system directives — returns nothing. Missing item 4 warns a judge in advance not to read the dry runs as an agent resisting an attack; this clause invites exactly that reading from the requirements table, which a judge reaches first.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:82
  repair: Say the resume corpus is byte-identical on both sides and that neither capture contains an injection payload, pointing at `ev-demos-06`.
  state: open
- id: F24
  severity: advisory
  scope: event
  blocking: false
  summary: 'The F17 repair asserted the approvals rather than performing them. `atj event approve` re-reads front matter and re-dumps it, appending `approved_by`, `approved_at` and `approval_note` after the existing keys: on `submissions/team-scribe.md`, `submissions/team-demos.md`, `audits/configuration.md` and `audits/intake.md` the three fields sit last in the front matter, after `validation_state` and after the whole `findings:` block. On both manifests they sit between `approval_state` and `validation_state`, where only a hand edit puts them, and `approved_at` is a rounded `00:52:00Z` against the tool''s `22:34:29Z`, `23:54:43Z` and `23:55:04Z`. The consequence is that `atj/cli.py:434-443`, which validates each artifact and refuses to approve one carrying a blocking or major finding, never ran. Here it would have passed — `atj validate reports` returns 0 findings over 7 artifacts — so the outcome is sound and the provenance is not.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:18-21
  repair: 'Run `python3 -m atj event approve --note "…" events/trial-2-2026/evidence/*/manifest.md` and let it write the fields and the stamp.'
  state: open
- id: F25
  severity: advisory
  scope: event
  blocking: false
  summary: '`audits/configuration.md` carries `approval_state: approved` and `approved_at: "2026-09-21T22:34:29Z"`. The F18 repair changed its F7 entry from `deferred` to `repaired` and rewrote the repair line at `2026-09-22T00:41Z`, eighteen hours of event time after that approval, and nothing in the file records that the approved text changed. The edit is correct and round one asked for it; what is missing is the trace. `atj release-check` reports "signed approvals PASS (15 in completed events, frozen)", which by construction does not cover an in-flight event, so nothing mechanical would notice.'
  artifact: events/trial-2-2026/audits/configuration.md:17
  repair: Add a line to the configuration audit recording that the F7 entry was amended at the evidence stage after approval, or re-approve it.
  state: open
- id: F26
  severity: advisory
  scope: event
  blocking: false
  summary: 'Introduced by the F2 repair. `ev-demos-05` closes "The rest of the diff is cosmetic (docstring, `DEMO_DIR`, report title, error text)". `DEMO_DIR` changes from `Path(__file__).resolve().parent` to `.parent.parent`, which is the path resolution that lets a script one directory deeper find the same `resumes/` and `criteria.md`; it is functional, and it is the reason the two runs read the same corpus. The diff also removes `import glob` at `rank_resumes.py:23`, which is unused there and is genuinely cosmetic, but is not in the list. Calling the path change cosmetic is what a judge would rely on if they wanted to know whether the two captures are comparable.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:92
  repair: Describe `DEMO_DIR` as the path fix that keeps both scripts on the same corpus, and add the removed `import glob`, or narrow the sentence to "nothing else changes what either script sends to the model".
  state: open
- id: F27
  severity: advisory
  scope: event
  blocking: false
  summary: 'Introduced by the F1 repair. `ev-scribe-11` now says "Two of the four are the documented keyring-first chain in `settings.py`". `:303` is the environment fallback inside `get_openai_api_key`, which is that chain. `:332` is inside `get_api_key_storage_method`, a reporting function that re-implements the same priority order to return the string `keyring`, `encrypted_config`, `environment` or `none`; it retrieves nothing and is not part of the chain. The distinction matters slightly for R7, which is about where keys live rather than about how the app reports where they live.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:122
  repair: 'Say one of the four is the chain at `get_openai_api_key` and one is the parallel order in `get_api_key_storage_method`.'
  state: open
- id: F28
  severity: advisory
  scope: event
  blocking: false
  summary: 'Introduced by the F2 and F9 repairs together, and visible only because they landed in the same round. `ev-demos-04` now cites the vulnerable `SYSTEM` block as `:33-43`, which is the whole literal. `ev-demos-05` and its key-file row cite the hardened system prompt as `:33-44`, but the hardened `SYSTEM` literal runs `:33-48`: `:45` is blank and `:46-48` is the JSON-shape instruction, which is identical on both sides. Everything the observation describes is inside `:33-44`, so nothing false is cited; the two sides of the comparison are simply cut at different places, and a judge diffing the cited ranges gets a whole block against a subset.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:92,119
  repair: Cite `:33-48` for the hardened block, or `:36-44` for the security rules that are the described difference.
  state: open
---

# Judging Audit

## Result

**PASS WITH ADVISORIES.** Round two.

The three blocking findings from round one are repaired and independently
re-derived, not merely edited. Fourteen of the sixteen minor and advisory
findings are repaired. F14 stays open by the repair round's declared choice and
is framework scope. F10 and F13 are half-repaired: each named two places and one
was changed. Nine new findings, F20 to F28, all introduced by the repair round;
three minor, six advisory, none blocking.

The `evidence-validated` gate may be set on this report.

## Scope and artifacts inspected

Evidence stage of `trial-2-2026` at `79455e69` on branch
`event/trial-2-2026-evidence`. Round one audited `355f4582` and failed it; the
repair is `79455e69`, and `git diff 4a3ef5a..HEAD -- events/` is four files:
both manifests, `audits/configuration.md` and `status.md`.

This round re-derived every number, line reference, quotation and timestamp the
repair touched, against the two pinned checkouts and the eleven run records
rather than against round one's own text. That mattered twice. Round one's F5
diagnosis was wrong — the file that pushes `example.com` from 213 to 214 is
`02-invisible-ink/demo/resumes-html/camille-vise.html`, not the root
`README.md` — and the repair caught it. Round one's F19 said "about twenty" apt
packages, the repair inherited "roughly twenty", and the `RUN` installs 27.

Read at the pins: `rank_resumes.py`, `hardened/rank_resumes_hardened.py` and the
diff between them, `fetch_beacons.py`, `settings.py:283-310`, `summarizer.py`,
`whisper_service.py:80-110`, `recorder.py:124-170`, `test_thread_safety.py`,
`requirements.txt`, demo 01's `resumes/` and `goofy-goof.md`. Read in the event:
both manifests, `Containerfile.scribe`, `Containerfile.demos`, all 11
`runs/*.json`, `status.md`, `audits/configuration.md`. Read in the framework:
`atj/ids.py`, `atj/cli.py` approve, `atj/reports.py` NE-confidence rule,
`atj/sandbox.py` limitation, `schemas/audit.schema.json`,
`schemas/evidence-manifest.schema.json`,
`framework/rubrics/submission-evaluation.md`, `events/trial-2-2026/event.md`.

Nothing was executed from either checkout. Every count came from `git grep`,
`find` or a read of the committed run records.

## Deterministic validation results

| Check | Result |
|---|---|
| `atj event validate events/trial-2-2026` | PASS, 0 problems, stage evidence |
| `atj validate reports events/trial-2-2026` | PASS, 7 artifacts, 0 findings |
| `atj validate publication events/trial-2-2026` | CLEAR, 7 artifacts, 0 blocking |
| `atj release-check` | PASS, all 13 checks |
| `atj event status events/trial-2-2026` | stage evidence, gate `evidence-validated` pending |
| `atj sandbox preflight` | AVAILABLE, podman 6.1.0 (rootless) |
| `pytest tests/ -q` | 517 passed, 5 skipped, 283 subtests |

Seven artifacts rather than round one's six, because this report is now one of
them. None of the nine new findings is visible to any of these checks, which is
the same point round one made and is now demonstrated twice on one stage.

## What the repair got right, re-derived

Recorded so a third round does not churn it.

**The two recomputed evidence package ids are correct, and the rule reproduces.**
`atj/ids.py:98` builds the id from event, team, twelve commit characters and an
eight-character digest, and the digest here is `sha256` of the manifest body
after the front matter. Both the superseded ids and the new ones reproduce under
that rule at their own commits: `63f56c93` and `1c0b2b5e` at `355f458`,
`ba263edf` and `a19ab6dc` at `79455e6`. The ids changed because the content
changed, which is what marks downstream judgments stale, and `status.md`'s team
table carries the new ones.

**Citation symmetry survives the repair, in both directions.** Every
`[[evidence:…]]` in both manifests resolves to an observation that exists, and
for all 27 observations the `Supports` cell and the set of requirement rows that
cite it are the same set. `ev-scribe-13` and `ev-demos-13` still carry `-` and
are cited by no requirement. The repair added prose citations of `ev-scribe-14`
and `ev-scribe-11` inside the new `evidence_limited_criteria` bullet, which sits
outside the requirements table and does not disturb the graph.

**Evidence-class discipline improved.** Three of the repairs are class
corrections rather than fact corrections: the docstring at `settings.py:286`
demoted to a team claim with the implementation at `:288-306` promoted to the
observation, the `--enforce-allowlist` consequence marked as a static read inside
an observation headed as exercised, and `Containerfile.demos`'s header moved to
the past tense with the commit that changed it named.

**Execution safety is untouched and still clean.** No run record was modified in
the repair commit. All 11 still carry `podman run`, `--network none`,
`--read-only`, `--cap-drop ALL`, `--security-opt no-new-privileges`, `--user
65534:65534`, the `/tmp` tmpfs, `--pids-limit 256`, `--memory 1g`, `--cpus 1.0`
and a `:ro,Z` mount; none is timed out or truncated; only the two approved images
appear. The one prose defect round one found in the limits table, F4, is fixed
and all nine remaining rows re-checked against their records.

**The untrusted-data wrapper is intact.** Both manifests still state that the
whole checkout was read as data, the scribe manifest still enumerates the agent
surface it covers, and both Validation sections still carry the wrapper checkbox
ticked. The demos manifest still marks R4 `NE`, still warns at Missing item 4
that a dry run is not agent behaviour, and still warns at item 6 against scoring
an evasiveness the submission never claimed. The scribe manifest still says a
judge must not treat the GUI import failure as an evidence limit. F23 is the one
place where new text pulls against one of those warnings.

**The status ledger matches disk apart from one row.** `current_stage: evidence`,
`evidence-validated: pending`, `gate_evidence` naming only the two passed gates,
both new package ids, both teams `sandboxed-partial, approved`, `public/` holding
only `.gitkeep`, and a working tree with nothing untracked or ignored inside the
event directory. The two new ledger rows record the failed audit and the repair,
and the repair row names F14 as left open, which is the honest entry. The
timestamps on those rows are F13 and F20.

**Both manifests are `approval_state: approved` with `validation_state: valid`,**
which is what F17 asked for, and `atj validate reports` independently agrees with
the validation state. How the fields were written is F24.

## The two arguments the repair made rather than conceded

Round one offered each of these a choice between conceding and justifying. The
repair justified both. Both hold.

**`security` does not belong in team-scribe's `evidence_limited_criteria`, and
`functional` and `agentic` do.** This holds, and the field is not decorative: at
`atj/reports.py:274-296` it decides what confidence a judge may attach to an `NE`
score. A criterion listed here makes an `NE` a `high`-confidence statement that
no observation was possible; a criterion not listed makes an `NE` a `low`-
confidence one resting on evidence the judge could not find. On that test,
`functional` and `agentic` are right — no model call was possible and no audio
device was provided, so the runtime behaviour behind R1, R2 and R3 is
unobservable, which is the identical cause team-demos records. `security` is
right to omit. The rubric asks whether access, data, tools, model risks and user
safety are handled responsibly, and the whole of ScribeVault's key handling is
readable and was read: the priority order at `settings.py:288-306`, the write
path at `:341-370`, the Fernet fallback at `:380-414`, the machine-string KDF
input at `:388` and the legacy unsalted path at `:393`. A judge who scored
`security` `NE` would be declining to read `settings.py`, not reporting an
absence of evidence. The asymmetry event.md:127-128 forbids is between teams,
and there is none: both manifests now carry `[functional, agentic]` for the same
stated reason.

**The scribe image's apt packages are prerequisites of declared packages, not
additions under event.md's image rule.** This holds. `requirements.txt:18`
declares `PySide6` and `:19` declares `pyaudio`. Without `portaudio19-dev`, `gcc`
and `python3-dev` the declared `pyaudio` cannot build from source on Linux;
without the GL, glib and xcb set the declared `PySide6` cannot link, offscreen
platform plugin or not. An image that omitted them would carry less than the
submission declares, not more. event.md's rule binds "anything added beyond" what
the submission declares, and a transitive system dependency of a declared package
is not beyond it, so the rule is satisfied with no event.md edit and no
loosening. The test that convinces is the counterfactual: strip those packages
and the failures you observe are the image's, not the submission's, which is the
exact confusion the rule exists to prevent. The Containerfile earns this by
tying each package to the requirement it serves at `:12-18`, which is more than
the rule asks. Three facts inside the bullet that makes the argument are wrong
and are F22; the argument is not one of them.

## Findings

| Severity | Rule | Artifact | Scope | Blocking | Finding | Required repair |
|---|---|---|---|---|---|---|
| minor | evidence-and-citation.md, cite what is there | `evidence/team-demos/manifest.md:111` | event | no | F10 — repaired in `ev-demos-07`, not in the Tests-and-execution row, which still says "against nine hostile URLs" | Say "nine URL forms, six hostile" in that row too |
| minor | evidence-manifest.md, timestamps must be observed | `status.md:70` | event | no | F13 — both manifests repaired to 00:14:00Z; the ledger's preparation row is still 00:35:00Z, twenty minutes after commit 355f458 | Move it between 00:07:26Z and 00:15:17Z |
| advisory | atj/reports.py:41 directory map | `atj/reports.py:41` | framework | no | F14 — `runs/*.json` is validated by nothing; left open deliberately as a framework change this stage will not make mid-event | Framework window, not this stage |
| minor | evidence-manifest.md, timestamps must be observed | `evidence/team-scribe/manifest.md:20` | event | no | F20 — `approved_at` 00:52:00Z on both manifests and `last_updated`/ledger 00:55:00Z postdate commit `79455e6` at 00:41:29Z and the wall clock at 00:48:46Z; fourth recurrence on this event | Stamp them from the tool, or from the time the work was done |
| minor | evidence-and-citation.md, direct observation must be true | `evidence/team-scribe/manifest.md:96` | event | no | F21 — the new R1 clause calls all thirteen `test_thread_safety.py` failures tests of `AudioRecorder`; `test_settings_no_deadlock` is a `SettingsManager` test | Say twelve of thirteen, or drop the attribution |
| minor | evidence-and-citation.md, cite line or symbol | `evidence/team-scribe/manifest.md:47-58` | event | no | F22 — the image bullet cites `:19-29` for a comment at `:12-18`, says "roughly twenty" where 27 are installed, and two of the 27 are not in that comment | Cite `:12-18` and `:22-28`, say 27, name the two |
| minor | evidence-and-citation.md, do not manufacture certainty | `evidence/team-demos/manifest.md:82` | event | no | F23 — R9's "with the payload text untouched on both sides" implies an injection payload in both captures; `ev-demos-06` establishes there is none in either | Say the corpus is identical and neither capture contains a payload |
| advisory | atj/cli.py approve is the approval mechanism | `evidence/team-scribe/manifest.md:18-21` | event | no | F24 — the approvals were hand-written; field placement and a rounded stamp differ from every other approved artifact on this event, so the refuse-on-major check never ran | Run `atj event approve` on both manifests |
| advisory | audit ledger hygiene | `audits/configuration.md:17` | event | no | F25 — an approved audit report's findings ledger was amended with no record that the approved text changed | Note the amendment, or re-approve |
| advisory | evidence-and-citation.md, cite what is there | `evidence/team-demos/manifest.md:92` | event | no | F26 — "the rest of the diff is cosmetic (docstring, `DEMO_DIR`, …)"; `DEMO_DIR` is the path fix that keeps both scripts on one corpus, and the removed `import glob` is unlisted | Narrow the sentence, or describe both |
| advisory | evidence-and-citation.md, keep classes distinct | `evidence/team-scribe/manifest.md:122` | event | no | F27 — "two of the four are the documented keyring-first chain"; `:332` is a reporting function that repeats the order, not part of the chain | Distinguish the two |
| advisory | evidence-and-citation.md, cite line or symbol | `evidence/team-demos/manifest.md:92,119` | event | no | F28 — the hardened `SYSTEM` literal runs `:33-48` and is cited `:33-44`, against `:33-43` for the whole vulnerable block | Cite `:33-48`, or `:36-44` for the rules that differ |

F1 to F9, F11, F12, F15 to F19 are repaired and carry `state: repaired` in the
front matter with what was re-derived for each. They are not in this table
because the table is what the next round has to act on.

## Advisories

Four observations that are not findings.

**The repair round is a net improvement, and the improvement is concentrated in
the three that mattered.** The blocking three were the ones a judge would have
carried into four independent judgments as settled fact: a miscount of where an
API key is read, a false mechanism for the one fix the demos corpus exists to
teach, and a front-matter field that decides what confidence an `NE` may carry.
All three are now correct, and two of them are better than the repair asked for.
F1 answers the bypass question R7 turns on instead of just adding a fourth line
number, and F6 replaces a scan with a wider scan rather than narrowing the claim
to fit the old one.

**Nine of twenty-eight findings on this stage were introduced by repairs, and
they cluster where the repair wrote new prose.** F21, F22, F23, F26, F27 and F28
are all inside sentences the repair added, and every one of them is a fact that
was not re-derived: thirteen tests assumed to be one class, a line range moved
without re-reading the file, "roughly twenty" carried over from this audit's own
round-one text, a payload assumed present because two prompts were being
compared. The pattern matches `live-trial-2026`, where nine defects came from
repairs, and this event's intake stage, where three of five round-two findings
came from the round-one repair. It is now established on this event that a
repair round needs the same re-derivation discipline as the work it repairs, and
it is cheaper to get it from the repairer than from the auditor.

**Half-repairs are the second pattern.** F10 and F13 each named two artifacts and
each got one. The `artifact` field in round one read `manifest.md:90,107` and
`manifest.md:12-13` with the ledger named only in the `repair` line. A repairer
working from the findings table alone would see the first location in each. That
is a report-shape lesson for this auditor as much as a discipline lesson for the
repairer: when a finding spans two files, the second one belongs in `artifact`,
not only in prose.

**The timestamp class is now four for four and should stop being repaired one
field at a time.** Configuration F19 was the auditor's own stamps, intake needed
an ordering repair, evidence F13 was both manifests and the ledger, and F20 is
the approval stamps the F13 repair itself wrote. Every instance has the same
shape: a round number, minutes after the commit that carries it, invented rather
than read. The fix is mechanical and already exists — `versions.now()` is what
`atj event approve` calls, and its output is never round. Nothing downstream
reads these fields, which is why none of the four is blocking, but a fourth
recurrence on one event is a process signal and the next stage should stamp from
the tool rather than from memory.

## Completion gate

- [x] No blocking findings — none; F1, F2 and F3 are repaired and re-derived
- [x] No major findings — none open; the three round-one majors are `repaired`
- [x] Calculations valid — 509 + 26 = 535 reproduces against `runs/team-scribe-pytest-01.json`; 13 + 10 + 3 = 26 reproduces from the FAILED list; 20 against 20 applicant delimiters reproduce from the two dry-run records; 214/213 and 211/210 and four `.example` addresses reproduce by `git grep` at the pin; both `evidence_package_id` digests reproduce under `atj/ids.py`
- [x] Evidence references resolve — every `[[evidence:…]]` resolves, `Supports` and requirement citations agree in both directions for all 27 observations, and every `runs/*.json` named exists
- [x] Version and identity checks pass — rubric `submission-evaluation@1.1.0`, persona `prepare-submission@1.1.0` on both manifests, `judging-auditor@1.1.0` here, framework commit `3f484d5` correct for the preparation window, both package ids well-formed and matching their own bodies
- [x] Privacy boundary passes — both manifests private, `public/` holds only `.gitkeep`, `atj validate publication` CLEAR over 7 artifacts
- [x] Every finding recorded in `findings:` with a `scope` and a `blocking` flag
- [ ] Approved with `atj event approve <this file>`

## Repairs required to clear this audit

None. No finding on this stage is blocking, and the `evidence-validated` gate may
be set on this report.

Twelve findings are open and all are minor or advisory. F14 is framework scope
and belongs to a framework window. The eleven event-scope ones are worth one
short round before judging begins, because four of them — F10, F21, F23 and F26 —
are sentences a judge will read as settled fact, and this event exists to test
how judges handle the boundary between an absent observation and a low score. F20
and F24 are cheap: run `atj event approve` on both manifests and let the tool
write the stamps it already knows how to write.

If that round happens, it needs a third audit. `atj event gate` reads the last
audit, not the first one that passed, and nine of the twenty-eight findings on
this stage were introduced by the round that repaired the previous nineteen.
