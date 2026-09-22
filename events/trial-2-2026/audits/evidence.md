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
framework_commit: 104194afbef1f73184c9f9a63ba9ab83fb8087f0
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-22T01:00:05Z"
completed_at: "2026-09-22T01:08:54Z"
visibility: private
approval_state: approved
validation_state: valid
result: PASS WITH ADVISORIES
audit_rounds: 3
findings:
- id: F1
  severity: major
  scope: event
  blocking: false
  summary: 'Round 1 — `ev-scribe-11` said `OPENAI_API_KEY` "is read at three sites" and omitted `src/ai/summarizer.py:54`. Round 2 repaired it and re-derived correctly: the observation now names four sites (`settings.py:303,332`, `whisper_service.py:96`, `summarizer.py:54`), keeps `whisper_service.py:449` as a report rather than a read, and answers the question R7 needed answered — `whisper_service.py:92-96` and `summarizer.py:50-54` are one fallback pattern written twice, each asking `settings_manager.get_openai_api_key()` first and reading the environment only when no settings manager was supplied, so a caller that constructs either service without one bypasses the keyring and the encrypted store. Verified against the pin: `git grep OPENAI_API_KEY` returns exactly those five `src/` occurrences, and the two constructors read as described. Round 3: the row was edited again for F27 and the four sites are unchanged.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:122
  repair: Done. No further work.
  state: repaired
- id: F2
  severity: major
  scope: event
  blocking: false
  summary: 'Round 1 — `ev-demos-05` said the hardened ranker "differs only in its system prompt". Round 2 repaired it from the diff: the observation now names two changes, quotes the submission''s own docstring ("Two changes carry the whole fix", `hardened/rank_resumes_hardened.py:5`), cites the system prompt and `build_user_content` at `:67-70`, states that neither works without the other, and gives the mechanical proof from the two run records. Verified: `diff rank_resumes.py hardened/rank_resumes_hardened.py` shows exactly those two substantive hunks, and the captures hold 20 `=== Applicant file:` headers against 20 `<applicant file=` tags. Round 3 repaired the residual F26; F28 is still half-open.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:92
  repair: Done. No further work.
  state: repaired
- id: F3
  severity: major
  scope: event
  blocking: false
  summary: 'Round 1 — `evidence_limited_criteria: [functional]` for team-scribe contradicted the manifest''s own Missing-evidence section and differed from team-demos for the identical no-model-call cause. Round 2 added `agentic`, so both manifests now record `[functional, agentic]`, and argued rather than conceded the rest: `security` is deliberately not listed because the key-handling implementation is entirely readable and was read. That argument holds. `atj/reports.py:274-296` is what consumes this field — it requires an `NE` criterion''s confidence to be `high` when the criterion is listed and `low` when it is not — and a `security` `NE` would in fact rest on evidence a judge can find at `settings.py:288-414`. The symmetry event.md:127-128 demands is satisfied: the two manifests now carry the same list for the same cause. Round 3 re-dumped the field as a block sequence through `atj event approve`; the two values are unchanged.'
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
  summary: Round 1 — two demos line ranges did not contain what was attributed to them. Round 2 repaired both and propagated the change to every place the same lines are cited. `ev-demos-03` is now `:103-106`, `ev-demos-04` is now `:33-43` with "the sentence at `:37-39`" for the quoted passage, and `ev-demos-02`, the key-file row and the dry-run decision bullet all moved to `:103-109`. All four re-derived against the pin, and round 3 re-confirmed `:33-43` as the whole vulnerable `SYSTEM` literal.
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:90,91
  repair: Done. No further work.
  state: repaired
- id: F10
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1 named two places and round 2 repaired one. Round 3 repaired the second: the Tests-and-execution row now reads "`is_localhost` and `_post_to_localhost` against nine URL forms, six of them hostile", which agrees with `ev-demos-07`''s "nine URL forms of which six are hostile". Verified: `grep -rn "nine hostile"` over `events/trial-2-2026/evidence/` now returns nothing, and the only two occurrences of the count in the manifest are those two rows, which agree. The underlying run record still shows three `True` and six `False`.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:113
  repair: Done. No further work.
  state: repaired
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
  summary: 'Round 1 — `ev-scribe-06` and `ev-scribe-08` both listed R1 in `Supports` while the R1 row said neither establishes nor refutes the recording behaviour. Round 2 rewrote the R1 row to say what each does establish: the capture path is reached and its error contract holds (`recorder.py:130` raises inside real PyAudio, `:165` wraps it as `AudioException`), and `AudioRecorder`''s thread-safety and cleanup behaviour is untested in the declared environment. Both halves verified at the pin, and the row still closes "Neither establishes recording, checkpoint flushing or `recover_checkpoints()`", so the refusal is preserved. The factual slip inside the new text was F21, now repaired; two wording residues are F32 and F33.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:102
  repair: Done. No further work.
  state: repaired
- id: F13
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 1 required three timestamps moved and round 2 moved two. Round 3 moved the third: the preparation ledger row is now `2026-09-22T00:14:30Z`, which sits after the last run record (`completed_at` maximum over the 11 records is `2026-09-22T00:07:26Z`) and before commit `355f458` (`2026-09-21T20:15:17-04:00` = `00:15:17Z`), and is consistent with both manifests'' `prepared_at` of `00:14:00Z`. The ledger''s new ordering defect is F29, which is a different fault in a different row.'
  artifact: events/trial-2-2026/status.md:70
  repair: Done. No further work.
  state: repaired
- id: F14
  severity: advisory
  scope: framework
  blocking: false
  summary: '`atj/reports.py:41` maps `runs/` to the `model-run` schema and template, and report validation globs only `*.md`. The 11 JSON sandbox execution records that every observation in this stage rests on are therefore validated by nothing — `atj validate reports` returns 7 artifacts and none of the 7 is a run record. Left open deliberately by both repair rounds: registering a sandbox-run schema is a framework change and this stage declined to make one mid-event. That is the right call under the rule against changing framework shape during an active event, and it is recorded here so the next framework window inherits it rather than the event.'
  artifact: atj/reports.py:41
  repair: Framework work, out of scope for this stage. Either register a sandbox-run schema for `runs/*.json` or record in the directory map that `runs/` holds two artifact kinds and only one is checked.
  state: open
- id: F15
  severity: advisory
  scope: event
  blocking: false
  summary: 'Round 1 — a gitignored `status.md.bak` carrying `current_stage: intake` sat in the event directory. Round 2 deleted it. Verified again this round: `git status --porcelain --ignored events/trial-2-2026/` returns nothing at all.'
  artifact: events/trial-2-2026/status.md.bak
  repair: Done. No further work.
  state: repaired
- id: F16
  severity: advisory
  scope: event
  blocking: false
  summary: Round 1 — `execution_record` was unset on both manifests. Round 2 sets it to `runs/team-scribe-*.json` and `runs/team-demos-*.json`. The schema types the field as `["string", "null"]`, so a glob is valid, and both globs resolve to the five and six records their manifests cite. Round 3's front-matter round-trip preserved both values.
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:15
  repair: Done. No further work.
  state: repaired
- id: F17
  severity: advisory
  scope: event
  blocking: false
  summary: 'Round 1 — both manifests were `approval_state: draft`. Round 2 set both to `approved` by hand; round 3 reverted them to draft and re-approved them with the tool. Both now carry `approval_state: approved`, `validation_state: valid`, `approved_by: event-director`, `approved_at: 2026-09-22T00:58:41Z` and an `approval_note` naming the round-two findings closed. The condition is met and the mechanism is now the tool''s; see F24.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:18
  repair: Done. No further work.
  state: repaired
- id: F18
  severity: advisory
  scope: event
  blocking: false
  summary: 'Round 1 — `audits/configuration.md` F7 was still `state: deferred` although the manifests discharge it. Round 2 moved it to `state: repaired` with a repair line pointing at the scribe manifest''s Scope and provenance section. Correct, and the pointer names a section rather than line numbers, which survives edits. Round 3 added the missing amendment trace, F25; the stamp inside that trace is F31.'
  artifact: events/trial-2-2026/audits/configuration.md:73-78
  repair: Done. No further work.
  state: repaired
- id: F19
  severity: advisory
  scope: event
  blocking: false
  summary: 'Round 1 — the scribe image adds apt packages that event.md:126-128 says must be named there with a reason. Round 2 argued rather than conceded, in a new Scope bullet: nothing is added, because an OS-level prerequisite of a declared Python package is not an addition. The argument holds. `requirements.txt:18` declares `PySide6` and `:19` declares `pyaudio`; without `portaudio19-dev`, `gcc` and `python3-dev` the declared `pyaudio` cannot build, and without the GL/xcb/glib set the declared `PySide6` cannot link. An image that omitted them would carry less than the submission declares, not more. Round 3 corrected two of the three supporting facts; the third is the open half of F22.'
  artifact: events/trial-2-2026/evidence/Containerfile.scribe:22-29
  repair: Done as an argument, and the argument is accepted. One supporting fact is still open under F22.
  state: repaired
- id: F20
  severity: minor
  scope: event
  blocking: false
  summary: Round 2 — three stamps postdated the commit that carried them. Round 3 repaired all three and used the tool for the one the tool owns. `approved_at` on both manifests is now `2026-09-22T00:58:41Z`, written by `atj event approve` from `versions.now()`; `status.md` `last_updated` is `00:59:00Z` and the final ledger row is `00:59:00Z`. Commit `104194a` is `2026-09-21T20:59:35-04:00` = `00:59:35Z`, so all three now precede the commit that carries them, and none is in the future against the clock this round read at `01:05:25Z`. The round-one repair row moved from `00:55:00Z` to `00:40:00Z` and the preparation row to `00:14:30Z`; both now precede their commits, but the first created the ordering fault F29, and the same invented `00:55:00Z` reappeared in a new place as F31.
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:22
  repair: Done. No further work.
  state: repaired
- id: F21
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 2 — the R1 row attributed all thirteen `test_thread_safety.py` failures to `AudioRecorder`. Round 3 repaired the count and named the exception: the row now reads "twelve of the thirteen" and adds "the thirteenth, `TestNoDeadlocks::test_settings_no_deadlock` at `tests/test_thread_safety.py:311`, tests `SettingsManager` and fails only because it shares the module''s `setUp`". Re-derived at the pin: the file holds four classes and sixteen tests (`TestAudioRecorderThreadSafety` 4, `TestAudioRecorderCleanup` 7, `TestSettingsManagerThreadSafety` 3, `TestNoDeadlocks` 2); `runs/team-scribe-pytest-01.json` lists exactly thirteen FAILED entries from the file, twelve of them `AudioRecorder` tests, and `test_settings_no_deadlock` is the thirteenth, failing at `tests/test_thread_safety.py:281` with `AttributeError: type object ''PyAudio'' has no attribute ''reset_mock''`. `def test_settings_no_deadlock` is at line 311 as cited. The twelve/thirteen split is correct; two wording residues in the new clause are F32 and F33.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:102
  repair: Done. The residues are tracked separately.
  state: repaired
- id: F22
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 2 found three defects in the image bullet and round 3 repaired two. The count is now "the 27 `apt` packages", which reproduces: the `RUN` package list at `Containerfile.scribe:23-28` holds 3 + 5 + 6 + 5 + 4 + 4 = 27 names. The comment citation moved to `:12-18`, which is correct — `:12` is "System packages, each tied to a declared requirement:" and `:18` is the last continuation line — and the bullet now discloses that the comment abbreviates `libxcb-*` and omits `libice6` and `libxkbcommon-x11-0`. What is not repaired is the second citation: the bullet says those two packages are installed by "the `RUN` at `:19-29`". The `RUN` begins at `:22`; `:19-20` is the display-and-audio comment about `QT_QPA_PLATFORM`, `:21` is the `FROM`, and the install runs `:22-28` with `:29` the `rm -rf` continuation. Round two named `:22-28` explicitly and the repair kept the wrong range while relabelling it. Secondary: the bullet still opens "Each is tied to the requirement it serves" and then discloses two that are not, so the sentence now contradicts itself in the same clause.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:57-61
  repair: Cite `:22-28` (or `:22-29`) for the install, and change "Each is tied to the requirement it serves" to something the next clause does not contradict — "the comment groups them by the requirement they serve" carries the argument without the overclaim.
  state: open
- id: F23
  severity: minor
  scope: event
  blocking: false
  summary: 'Round 2 — R9 said the two captures used "the same 20-resume corpus … with the payload text untouched on both sides", implying an injection payload in both. Round 3 repaired it and took the stronger form round two suggested: R9 now reads "and no injected payload in either capture, since act 2 was never staged — which is the point, because the difference the demo teaches is visible in the framing alone". Verified: `ev-demos-06` establishes that `goofy-goof.md` is not staged into `resumes/` at the pin, both scripts resolve `RESUMES_DIR` to the same `demo/resumes` directory, and the new R9 text now agrees with Missing-evidence item 4 rather than pulling against it. The one thing not done is the citation, F34.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:84
  repair: Done. The missing citation is F34.
  state: repaired
- id: F24
  severity: advisory
  scope: event
  blocking: false
  summary: 'Round 2 — the F17 approvals were hand-written, so `atj/cli.py:434-443`, which validates each artifact and refuses to approve one carrying a blocking or major finding, never ran. Round 3 discharged it: both manifests were reverted to draft and re-approved with `atj event approve` at stamp `2026-09-22T00:58:41Z`. Three independent signs that the tool wrote it. The field order is now the tool''s — `approve` pops the three fields on a revert and re-appends them after every existing key, so both manifests now read `approval_state`, `validation_state`, `approved_by`, `approved_at`, `approval_note`, which is the exact order on `submissions/team-scribe.md` and `audits/intake.md` and the opposite of the hand-edited order round two found. The stamp is unrounded, which `versions.now()` produces and a hand edit did not. And `evidence_limited_criteria` changed from the hand-written flow style `[functional, agentic]` to a block sequence with no change of value, which is a YAML round-trip through the tool and nothing else. The refuse-on-major check therefore ran on both artifacts and passed; `atj validate reports` independently returns 0 blocking and 0 major over 7 artifacts.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:20-24
  repair: Done. No further work.
  state: repaired
- id: F25
  severity: advisory
  scope: event
  blocking: false
  summary: 'Round 2 — `audits/configuration.md` was amended after approval with nothing recording it. Round 3 added `amended_after_approval` to the F7 finding entry, naming what changed and that no other finding''s approved text moved. The trace now exists and is machine-readable: `schemas/audit.schema.json` sets `additionalProperties: true` on both the document and each finding item, so the new key validates, and `atj validate reports` returns 0 findings over 7 artifacts with it in place. The alternative branch, re-approval, was not taken, which is allowed — round two offered either. The timestamp inside the note is wrong and is F31.'
  artifact: events/trial-2-2026/audits/configuration.md:77
  repair: Done. The stamp inside the note is F31.
  state: repaired
- id: F26
  severity: advisory
  scope: event
  blocking: false
  summary: 'Round 2 — `ev-demos-05` called `DEMO_DIR` cosmetic and omitted the removed `import glob`. Round 3 repaired both: the row now reads "one path fix and three cosmetic changes: `DEMO_DIR` becomes `Path(__file__).resolve().parent.parent` so the hardened script, living one directory down, still reads the same `resumes/` corpus, and the docstring, report title and error text name the hardened script instead of the vulnerable one. The unused `import glob` is dropped." Every clause re-derived at the pin. `hardened/rank_resumes_hardened.py:27` is `DEMO_DIR = Path(__file__).resolve().parent.parent   # hardened/ -> demo/` against `rank_resumes.py:27` `Path(__file__).resolve().parent`, and the hardened file sits in `demo/hardened/`, so both resolve `RESUMES_DIR` to `demo/resumes` — which is what makes the two captures comparable. `import glob` is at `rank_resumes.py:23` and absent from the hardened file, and it is genuinely unused there: `load_resumes` uses `Path.glob`, not the module. The remaining diff hunks are exactly the docstring, the report title and the SDK error string.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:94
  repair: Done. No further work.
  state: repaired
- id: F27
  severity: advisory
  scope: event
  blocking: false
  summary: 'Round 2 — `ev-scribe-11` folded `settings.py:332` into "the documented keyring-first chain". Round 3 separates them: "Two of the four are in `settings.py`: `:303` is the documented keyring-first chain, and `:332` is `get_api_key_storage_method`, which reports which source a key would come from rather than fetching one." Verified at the pin: `:303` is `env_key = os.getenv("OPENAI_API_KEY")` inside `get_openai_api_key`, the third branch after keyring and the encrypted config; `get_api_key_storage_method` is defined at `:315` and `:332` is its own `os.getenv` inside a function whose four return values are the strings `keyring`, `encrypted_config`, `environment` and `none`. The class distinction R7 needs is now on the page.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:128
  repair: Done. No further work.
  state: repaired
- id: F28
  severity: advisory
  scope: event
  blocking: false
  summary: 'Round 2 named two places, `manifest.md:92,119`, and round 3 repaired the prose in one of them. `ev-demos-05`''s narrative now cites the hardened system prompt as `hardened/rank_resumes_hardened.py:33-48`, against `:33-43` in the vulnerable script, and both ranges re-derive exactly: the hardened `SYSTEM` triple-quoted literal opens at `:33` and closes at `:48`, the vulnerable one at `:33` and `:43`. What did not move is either citation cell. The evidence column of the same row still reads `01-resume-that-talked-back/demo/hardened/rank_resumes_hardened.py:33-44,67-70`, and the key-file row at `:121` still reads the same `:33-44,67-70`. The row is now internally inconsistent — its prose and its own citation cell give two different ranges for one literal — which is worse for a judge than the single wrong range round two found.'
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:94,121
  repair: Change `:33-44` to `:33-48` in the evidence column of `ev-demos-05` and in the key-file row, so all three references to the hardened `SYSTEM` literal agree.
  state: open
- id: F29
  severity: minor
  scope: event
  blocking: false
  summary: 'Introduced by the F13 and F20 repairs. The activity ledger is in ascending time order for all twenty-two rows except the two this round rewrote: the round-one audit is stamped `2026-09-22T00:41:00Z` and the row immediately below it, "Evidence repaired, round one", is stamped `00:40:00Z`. The repair now records as finishing a minute before the audit that demanded it. Both commits are real and both are `2026-09-21T20:41:29-04:00` = `00:41:29Z` (`4a3ef5a` the audit, `79455e6` the repair), so a value between `00:41:00Z` and `00:41:29Z` is the only one that satisfies both the commit constraint round two set and the causal order. This is the same fault configuration audit F21 repaired on this file ("activity-log ordering"), recurring in the rows a later repair touched.'
  artifact: events/trial-2-2026/status.md:72
  repair: Move the "Evidence repaired, round one" row to a time after `00:41:00Z` and before commit `79455e6` at `00:41:29Z`.
  state: open
- id: F30
  severity: minor
  scope: event
  blocking: false
  summary: 'Introduced by this round''s new ledger row. "Evidence re-audited, round two; report superseded in place" is stamped `2026-09-22T00:41:29Z`, which is the commit time of `79455e6`, the artifact that audit read. The audit''s own front matter at that revision records `started_at: 2026-09-22T00:42:00Z` and `completed_at: 2026-09-22T00:56:33Z`, so the ledger now says the audit finished thirty-one seconds before it started and fifteen minutes before its own report claims it completed. The row was stamped from the commit it audited rather than from the work.'
  artifact: events/trial-2-2026/status.md:73
  repair: Set the row to the audit's `completed_at`, `2026-09-22T00:56:33Z`, or to any time between that and commit `104194a` at `00:59:35Z`.
  state: open
- id: F31
  severity: minor
  scope: event
  blocking: false
  summary: Introduced by the F25 repair, and the fifth recurrence of the invented-timestamp class on this event. The new `amended_after_approval` note on `audits/configuration.md` F7 opens `'2026-09-22T00:55:00Z — F7 moved from deferred to repaired by evidence audit F18'`. That amendment landed in commit `79455e6` at `00:41:29Z`, so the note records the amendment as happening thirteen and a half minutes after the commit that made it. `00:55:00Z` is one of the three invented stamps round two raised as F20; this round corrected it in `status.md` and reused the same value in the field whose only purpose is to record when the amendment happened.
  artifact: events/trial-2-2026/audits/configuration.md:77
  repair: Set the note's stamp to a time no later than commit `79455e6` at `2026-09-22T00:41:29Z`, consistent with the round-one repair row in `status.md` once F29 is fixed.
  state: open
- id: F32
  severity: advisory
  scope: event
  blocking: false
  summary: Introduced by the F21 repair. The R1 row now reads "twelve of the thirteen tests written against it cannot run there", where "it" is `AudioRecorder`. Only twelve tests are written against `AudioRecorder`; the sentence still attributes the whole set of thirteen to it, and by saying twelve of thirteen cannot run it now also implies one `AudioRecorder` test does run, when all thirteen fail. The parenthetical that follows supplies the correct facts and a careful reader recovers them, which is why this is advisory rather than a repeat of F21.
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:102
  repair: '"because the twelve tests written against it, and one `SettingsManager` test that shares their fixture, cannot run there" — or drop "written against it" and describe the thirteen as the failures in the thread-safety file.'
  state: open
- id: F33
  severity: advisory
  scope: event
  blocking: false
  summary: 'Introduced by the F21 repair. The new clause says `test_settings_no_deadlock` "fails only because it shares the module''s `setUp`". There is no module-level `setUp` in `tests/test_thread_safety.py`: the `setUp` it shares is `TestNoDeadlocks.setUp` at `:280-281`, shared with `test_recorder_no_deadlock` and with nothing else. What is module-level is the `mock_pyaudio = sys.modules[''pyaudio'']` binding at `:24` that the three class `setUp`s at `:34`, `:122` and `:281` all call `.reset_mock()` on, which is what `ev-scribe-06` cites correctly. The cause is right and the possessive is wrong.'
  artifact: events/trial-2-2026/evidence/team-scribe/manifest.md:102
  repair: Say it shares `TestNoDeadlocks`'s `setUp`, or that it fails on the module-level `pyaudio` mock its class's `setUp` resets.
  state: open
- id: F34
  severity: advisory
  scope: event
  blocking: false
  summary: Introduced by the F23 repair. R9's new clause asserts "no injected payload in either capture, since act 2 was never staged". That is true and this audit re-derived it, but R9 cites only `[[evidence:ev-demos-04]]` and `[[evidence:ev-demos-05]]`, and neither establishes it. The observation that does is `ev-demos-06`, which round two's repair line named and the repair did not add. Every other factual clause in both requirements tables carries the observation that supports it; this one does not. Adding the citation also needs `R9` added to `ev-demos-06`'s `Supports` cell, or the two-way symmetry this stage maintains breaks.
  artifact: events/trial-2-2026/evidence/team-demos/manifest.md:84
  repair: Cite `[[evidence:ev-demos-06]]` in R9 and add `R9` to `ev-demos-06`'s `Supports` cell, keeping both directions in step.
  state: open
approved_by: event-director
approved_at: "2026-09-22T01:10:39Z"
approval_note: Evidence audit round three accepted; the gate is recorded on it.
---

# Judging Audit

## Result

**PASS WITH ADVISORIES.** Round three, scoped to the repair round.

Ten findings were put to this round. Eight are repaired and two are half-repaired
for the second time: F22 and F28 each named two places, each got one, and each is
the same half-repair shape round two recorded for F10 and F13 — which this round
did close. F24 is discharged, and discharged properly: the approvals are the
tool's, not an assertion that they are. F14 stays open in framework scope by the
repair round's declared choice.

Six new findings, F29 to F34, all introduced by this round; three minor, three
advisory, none blocking. Four of the six are in sentences or fields the repair
itself wrote.

The `evidence-validated` gate may be set on this report.

## Scope and artifacts inspected

Evidence stage of `trial-2-2026` at `104194af` on branch
`event/trial-2-2026-evidence`. This round is scoped: rounds one and two verified
the two packages end to end and round two returned PASS WITH ADVISORIES. Nothing
round two confirmed was re-derived. What was audited is `git diff 79455e6..HEAD
-- events/`, which is five files — both manifests, `status.md`,
`audits/configuration.md` and this report — and whether the repair broke anything
it touched.

Re-derived this round, at the two pinned checkouts and against the committed run
records: the 27 apt package names in `Containerfile.scribe:23-28` and the comment
block at `:12-18`; the class and test inventory of
`tests/test_thread_safety.py` and the thirteen FAILED entries in
`runs/team-scribe-pytest-01.json`, including the traceback for
`test_settings_no_deadlock`; `settings.py:296-336`, covering both `:303` and
`:332` and the `def` boundaries around them; the full diff of `rank_resumes.py`
against `hardened/rank_resumes_hardened.py`, the two `SYSTEM` literals with their
opening and closing lines, `DEMO_DIR` on both sides and the dropped `import
glob`; both `evidence_package_id` digests, recomputed under the rule that
reproduces the four superseded ones; the amendment note added to
`audits/configuration.md` and the schema that admits it; and every timestamp in
`status.md` against the authored time of the commit that carries it.

Also re-checked, because the repair touched the rows: citation symmetry in both
directions across all 27 observations in both manifests, by extracting every
`[[evidence:…]]` in the requirements tables and every `Supports` cell and
comparing the two sets per observation.

Nothing was executed from either checkout. Every count came from `git grep`,
`cat -n`, a read of the committed run records, or `git log`.

## Deterministic validation results

| Check | Result |
|---|---|
| `atj event validate events/trial-2-2026` | PASS, 0 problems, stage evidence |
| `atj validate reports events/trial-2-2026` | PASS, 7 artifacts, 0 blocking, 0 major, 0 minor, 0 advisory |
| `atj validate publication events/trial-2-2026` | CLEAR, 7 artifacts, 0 blocking |
| `atj release-check` | PASS, all checks including single-source and signed approvals |
| `atj event status events/trial-2-2026` | stage evidence, gate `evidence-validated` pending |
| `git status --porcelain --ignored events/trial-2-2026/` | empty |
| Citation symmetry, both manifests | 27 observations, 0 mismatches, 0 dangling, 0 unresolved |
| `evidence_package_id` recomputation | both reproduce; see below |

None of the six new findings is visible to any of these checks. That is the third
time this stage has demonstrated it.

## What the repair got right, re-derived

**Both recomputed package ids are correct under the rule that reproduced the
previous four.** The digest is `sha256` of the manifest text after the closing
front-matter delimiter, taken raw with no stripping, truncated to eight
characters. Under that one rule and no other variant, `63f56c93` and `1c0b2b5e`
reproduce at `355f458`, `ba263edf` and `a19ab6dc` at `79455e6`, and `32470f92`
and `a9a56723` at `104194a`. The ids changed because the manifest bodies changed,
which is what marks downstream judgments stale, and `status.md`'s team table
carries the new pair.

**The approval is the tool's.** Three independent signatures, set out in F24:
field order matching every other approved artifact on this event and inverted
from what round two found, an unrounded `versions.now()` stamp, and a flow-style
YAML list re-dumped as a block sequence with no change of value. The
refuse-on-major branch at `atj/cli.py:434-443` therefore ran, and it had 0
blocking and 0 major to refuse on.

**Both manifests are approved, valid and private.** `approval_state: approved`,
`validation_state: valid`, `visibility: private` on both, `approved_at`
`2026-09-22T00:58:41Z` on both, and `atj validate publication` CLEAR over 7
artifacts with `public/` holding only `.gitkeep`.

**`status.md` still matches disk.** `current_stage: evidence`,
`evidence-validated: pending`, `gate_evidence` naming only the two passed gates,
the body checkboxes agreeing with the front matter, both new package ids in the
team table, both teams `sandboxed-partial, approved`, and a working tree with
nothing untracked or ignored anywhere in the event directory. The two new ledger
rows describe what the commit actually contains. Their times are F29 and F30 and
the underlying history is correct, which is why neither blocks.

**The 27 is right and the counterfactual behind F19 is unchanged.** The `RUN`
package list holds 3 + 5 + 6 + 5 + 4 + 4 = 27 names across `Containerfile.scribe`
lines 23 to 28. `libice6` and `libxkbcommon-x11-0` are genuinely absent from the
comment and genuinely prerequisites — `libsm6` needs `libICE`, the xcb set needs
`libxkbcommon-x11` — so disclosing them strengthens the bullet rather than
weakening the argument it carries.

**The twelve/thirteen split is exactly right.** Sixteen tests in four classes,
thirteen failures, twelve of them `AudioRecorder` tests, and the thirteenth
failing in `setUp` at `tests/test_thread_safety.py:281` with `AttributeError: type
object 'PyAudio' has no attribute 'reset_mock'`, which is the same cause as the
other twelve and not a fault in the test's own body. `def test_settings_no_deadlock`
is at `:311` as cited.

**The evidence-class corrections hold.** `settings.py:332` is now described as a
reporting function and it is one: `get_api_key_storage_method` at `:315` returns a
string naming a source and retrieves no key. `DEMO_DIR` is now described as a
path fix and it is one: `.parent.parent` from `demo/hardened/` is `demo/`, which
is why both scripts read the same twenty resumes. The egress row and the
observation it belongs with now give the same count.

**R9 no longer pulls against Missing-evidence item 4.** The new clause says there
is no injected payload in either capture, which is what `ev-demos-06` establishes
and what item 4 warns a judge about. Round two's concern is resolved; only the
citation is missing, F34.

## Findings

Ten findings were in scope. F10, F13, F20, F21, F23, F24, F25, F26 and F27 are
repaired and carry `state: repaired` with what was checked. F22 and F28 are open
below with their remaining half. F14 remains open, framework scope, by declared
choice.

| Severity | Rule | Artifact | Scope | Blocking | Finding | Required repair |
|---|---|---|---|---|---|---|
| minor | evidence-and-citation.md, cite line or symbol | `evidence/team-scribe/manifest.md:57-61` | event | no | F22 — 27 and `:12-18` are now right; the install is still cited `:19-29` where the `RUN` is `:22-28`, and "Each is tied to the requirement it serves" still precedes the disclosure that two are not | Cite `:22-28`, and soften the clause the next one contradicts |
| advisory | atj/reports.py:41 directory map | `atj/reports.py:41` | framework | no | F14 — `runs/*.json` is validated by nothing; left open deliberately as a framework change this stage will not make mid-event | Framework window, not this stage |
| advisory | evidence-and-citation.md, cite line or symbol | `evidence/team-demos/manifest.md:94,121` | event | no | F28 — the prose now says `:33-48`; the same row's citation cell and the key-file row still say `:33-44`, so the row disagrees with itself | Change both cells to `:33-48` |
| minor | status ledger ordering | `status.md:72` | event | no | F29 — the round-one repair row is stamped `00:40:00Z`, a minute before the `00:41:00Z` audit that demanded it; the ledger's only out-of-order pair | Move it between `00:41:00Z` and commit `79455e6` at `00:41:29Z` |
| minor | evidence-manifest.md, timestamps must be observed | `status.md:73` | event | no | F30 — the round-two audit row is stamped `00:41:29Z`, the commit time of what it audited, which is before that report's own `started_at` of `00:42:00Z` | Use the report's `completed_at`, `00:56:33Z` |
| minor | evidence-manifest.md, timestamps must be observed | `audits/configuration.md:77` | event | no | F31 — the new amendment note records the amendment at `00:55:00Z`; it was committed at `00:41:29Z`. Fifth recurrence, this time inside the field whose purpose is to record when | Stamp it no later than `00:41:29Z` |
| advisory | evidence-and-citation.md, direct observation must be true | `evidence/team-scribe/manifest.md:102` | event | no | F32 — "twelve of the thirteen tests written against it" still assigns all thirteen to `AudioRecorder` and implies one of them runs | Reword the clause; the parenthetical is correct |
| advisory | evidence-and-citation.md, cite line or symbol | `evidence/team-scribe/manifest.md:102` | event | no | F33 — "shares the module's `setUp`"; there is no module-level `setUp`, it is `TestNoDeadlocks.setUp` at `:280-281` | Name the class's `setUp`, or the module-level mock it resets |
| advisory | evidence-and-citation.md, cite what establishes the claim | `evidence/team-demos/manifest.md:84` | event | no | F34 — R9's new payload-absence clause rests on `ev-demos-06` and cites only `ev-demos-04` and `ev-demos-05` | Cite `ev-demos-06` in R9 and add `R9` to its `Supports` cell |

## Advisories

Three observations that are not findings.

**The half-repair pattern survived being named.** Round two recorded it as a
report-shape lesson and put both locations of F10 and F13 into the `artifact`
field. Those two closed. F22 and F28 were written the same way — `manifest.md:47-58`
and `manifest.md:92,119` — and each got one location again. The difference this
time is that F28's half-repair made the artifact worse than it found it: a single
table row now states `:33-48` in its prose and `:33-44` in its own citation cell.
A judge diffing a row against itself is a new failure mode that neither round one
nor round two produced.

**Nine of the ten repairs were re-derived and one was not.** F21, F22's count,
F26, F27 and F28's prose all required going back to the pinned source, and every
one of them is right at the level round two asked for. The exceptions are
mechanical: a range copied forward without re-reading the file (F22), two
citation cells not searched for (F28), and three timestamps written from the
narrative rather than from a commit or a clock (F29, F30, F31). The repair round
re-derived facts about the submissions and did not re-derive facts about its own
history.

**The timestamp class is now five for five and every recurrence is in a
different field.** Configuration F19 was the auditor's own stamps, intake was an
ordering repair, evidence F13 was the manifests and the ledger, F20 was the
approval stamps the F13 repair wrote, and F29/F30/F31 are the rows and the note
the F13 and F20 repairs wrote. The one instance that is now correct beyond
argument is the one the tool wrote: `approved_at: 2026-09-22T00:58:41Z`, from
`versions.now()`. Everything still wrong is hand-written. Nothing downstream
reads any of these fields, which is why none of the five is blocking, but the
judgments stage should take every stamp from a command or a commit and write none
from memory.

## Completion gate

- [x] No blocking findings — none on this stage across three rounds
- [x] No major findings — none open; F1, F2 and F3 remain `repaired` and this round's edits did not disturb them
- [x] Calculations valid — 27 apt packages reproduce from `Containerfile.scribe:23-28`; 16 tests in 4 classes and 13 failures reproduce from the file and `runs/team-scribe-pytest-01.json`; both new `evidence_package_id` digests reproduce under the same rule as the four superseded ones; the `00:07:26Z` / `00:14:30Z` / `00:15:17Z` ordering behind F13 reproduces from the run records and `git log`
- [x] Evidence references resolve — 27 observations across both manifests, `Supports` and requirement citations agree in both directions, nothing dangling and nothing unresolved
- [x] Version and identity checks pass — rubric `submission-evaluation@1.1.0`, persona `prepare-submission@1.1.0` on both manifests, `judging-auditor@1.1.0` here, `framework_commit: 3f484d5` unchanged on both manifests, both package ids well-formed and matching their own bodies
- [x] Privacy boundary passes — both manifests `visibility: private`, `public/` holds only `.gitkeep`, `atj validate publication` CLEAR over 7 artifacts
- [x] Every finding recorded in `findings:` with a `scope` and a `blocking` flag
- [ ] Approved with `atj event approve <this file>`

## Repairs required to clear this audit

None. No finding on this stage is blocking, and the `evidence-validated` gate may
be set on this report.

Nine findings are open: F14 in framework scope, and eight event-scope ones, five
minor and three advisory. Two of them, F22 and F28, are the unrepaired halves of
round-two findings and both are one-line citation edits. F28 is the one worth
doing before judging begins, because it is the only open finding that leaves an
artifact self-contradicting on the page a judge reads. F29, F30 and F31 are three
timestamps and no downstream reader.

If a fourth repair round happens it needs a fourth audit, on the same evidence as
before: every round on this stage has introduced defects, and this one introduced
six while closing eight.
