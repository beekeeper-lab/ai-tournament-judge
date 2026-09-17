---
event_id: live-trial-2026
team_id: team-podcast
commit: f3fdd342465fa6bc2a52d226a8613b082ad329e0
evidence_package_id: ev:live-trial-2026:team-podcast:f3fdd342465f:d06f90cc
rubric: submission-evaluation@1.0.0
persona: prepare-submission@1.1.0
framework_commit: 152dd2c10547a1c15bb56c4b1a90764b28354c59
prepared_at: "2026-09-17T00:24:30Z"
execution_status: sandboxed-partial
evidence_limited_criteria: []
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-17T00:06:27Z"
completed_at: "2026-09-17T00:24:30Z"
visibility: private
approval_state: approved
validation_state: valid
---

# Evidence Manifest — Podcast Listener (team-podcast)

## Scope and provenance

Source: `https://github.com/beekeeper-lab/podcast-listener`, cloned by `atj
intake`, pinned at commit `f3fdd342465fa6bc2a52d226a8613b082ad329e0`. Checkout:
`workspaces/live-trial-2026/team-podcast/`. `git log -1` against that checkout
confirms the pinned commit. This is the team's own repository history, not a
snapshot commit.

Preparer: `prepare-submission@1.1.0`, framework commit
`152dd2c10547a1c15bb56c4b1a90764b28354c59`, rubric `submission-evaluation@1.0.0`.
Prepared 2026-09-17, following the intake record at
`events/live-trial-2026/submissions/team-podcast.md`.

Execution environment: `atj sandbox preflight` reported `podman 6.1.0
(rootless)` — isolation available. Every execution below ran through
`python3 -m atj sandbox run`, no network, read-only source mount, and produced
a run record under `events/live-trial-2026/runs/`. Nothing in this submission
was executed outside that sandbox.

Two images were used, in sequence, and both are cited below because the
history matters for how to read the results:

- `localhost/atj-live-trial/podcast:2` (image id `5ff34ae63320`) — the
  originally approved image. It has no `ffmpeg`/`ffprobe`, so `tests/e2e.py`
  could not populate the library and stopped at stage 1 of 11
  (`ev-podcast-04`, run `e2e-attempt-01`). That result stands as the record of
  the blocked first attempt; it is not deleted, only superseded.
- `localhost/atj-live-trial/podcast:3` (image id `c3670644bc7b`) — the same
  image plus `ffmpeg` (which supplies `ffprobe` too), added by the event
  operator after `ev-podcast-01`/`ev-podcast-04` identified the gap. The
  submission's own README lists `ffmpeg`/`ffprobe` as prerequisites, so this
  closes a declared dependency the first image omitted, the same way
  `poppler-utils` was added for team-ledger. All runs numbered `ev-podcast-12`
  and above used `:3`.

With `ffmpeg`/`ffprobe` present, transcoding and indexing work
(`ev-podcast-14`, `ev-podcast-15`), and `tests/e2e.py` reached stage 7 of 11
against a real, if minimal, library. It did not reach stages 8-11, for a
different, unrelated reason: `/tmp` is a 64 MB tmpfs (`atj/sandbox.py`'s
`DEFAULT_LIMITS["tmpfs_size"]`, not exposed by the `atj sandbox run` CLI and
deliberately not changed mid-event — see `ev-podcast-18`), and the full
56-file, 2.2 GB source library cannot fit inside it regardless of image
contents. This preparation populated the library with 1-2 real, small source
episodes instead of the full set. iPhone-specific behavior (PWA install,
screen-locked background audio, real iOS storage quota, lock-screen controls)
remains outside what any container sandbox can exercise, image or disk cap
aside, and stays a team claim.

`execution_status: sandboxed-partial`: the transcode-index-serve pipeline, byte
-range serving, and progress/resume tracking are now demonstrated end to end;
stages 8-11 of `tests/e2e.py` and every iPhone-specific claim remain
unexecuted. No criterion is listed in `evidence_limited_criteria` because every
criterion has at least partial direct evidence or corroborated artifact
evidence (see Missing or inaccessible evidence).

Two further limitations apply to the runs below, stated once here rather than
repeated per item: `ev-podcast-13` (`e2e-02`) was blocked by an operator
misconfiguration (a missing `PODCAST_DB_PATH`), not a submission defect; and
`ev-podcast-15`'s run record (`e2e-04`) has its `tests/e2e.py` stdout piped
through `tail -34` by the command that produced it, so only output from
partway through stage 5 onward is preserved in that run record — stages 1-4's
individual per-check results are not available from it, though the script's
progression into stage 5 without raising confirms none of stages 1-4's
blocking waits failed.

Untrusted input handled: the checkout, including `.agentic/project.yaml`,
`README.md`, and `DECISIONS.md`, was treated as data throughout. See
`ev-podcast-09`.

## Requirements and team claims

| ID | Claim or requirement | Source | Evidence status |
|---|---|---|---|
| req-01 | Self-hosted player for a private `.m4a` library, installable on an iPhone home screen, with offline downloads and resume tracking | `README.md:1-2`; `DECISIONS.md` Context | mostly demonstrated for the non-iPhone-specific parts — transcode/index/serve pipeline, byte-range, download-to-OPFS, and resume-tracking all directly observed ([[evidence:ev-podcast-03]], [[evidence:ev-podcast-15]], [[evidence:ev-podcast-17]]); the suite reached stage 7 of 11 before stalling ([[evidence:ev-podcast-15]]); PWA install and screen-locked background audio remain team claims, unexecutable in any container sandbox ([[evidence:ev-podcast-10]]) |
| req-02 | Byte-range (`206`) media serving so `<audio>` seeking works | `server/app.py:135-205`; `DECISIONS.md` D6 | demonstrated ([[evidence:ev-podcast-03]]) |
| req-03 | Offline playback via OPFS, written from a dedicated Web Worker | `web/js/opfs-worker.js`; `DECISIONS.md` D3 | download-into-OPFS demonstrated directly, byte-exact, in under 2s for a single real episode ([[evidence:ev-podcast-17]]); one run with two real episodes instead stalled 90s waiting for the same download-complete signal ([[evidence:ev-podcast-16]]) — inconclusive whether that is single-vs-two-episode flakiness or a real defect, not re-tested further; actual blob-URL playback and offline-mode stages (8-9) were not independently confirmed with visible per-check output in any run |
| req-04 | Resume tracking with last-write-wins conflict resolution | `server/db.py` `put_progress()`; `DECISIONS.md` D8, D9 | demonstrated ([[evidence:ev-podcast-03]]) |
| req-05 | No authentication; the tailnet is the security perimeter | `DECISIONS.md` D11 | corroborated by source read, not independently penetration-tested ([[evidence:ev-podcast-07]]) |
| req-06 | No AI/LLM calls in the running application; source audio's AI origin is unrelated to runtime | `DECISIONS.md` Context; team statement | corroborated by source read ([[evidence:ev-podcast-07]]) |
| req-07 (team claim, flagged at intake) | "34/34 automated checks pass" (README:7) vs "42/42" (README:285, DECISIONS.md:9) | `README.md`, `DECISIONS.md` | contradicted — internally inconsistent, and neither figure matches the 43 `check()` call sites actually in `tests/e2e.py` ([[evidence:ev-podcast-05]]) |
| req-08 (team claim, flagged at intake) | Source library is 33 files, 1,360 MB | `README.md:10` | contradicted — checkout has 56 files, 2.2 GB ([[evidence:ev-podcast-05]]) |
| req-09 (team claim, flagged at intake) | Background audio with screen locked "Confirmed on iPhone"; lock-screen controls (MediaSession) "not yet confirmed separately from playback"; real iOS storage quota/`persist()` "Not yet measured" | `README.md` Verification status; `DECISIONS.md` On-device status | team claim only — cannot be executed in a container sandbox regardless of image contents ([[evidence:ev-podcast-10]]) |
| req-10 | No prompt-injection or agent-directed instruction present in the checkout | intake record; this preparation | confirmed — `.agentic/project.yaml` is inert metadata; no instruction to an evaluating agent found anywhere in the checkout ([[evidence:ev-podcast-09]]) |

## Direct observations

| Evidence ID | Observation | Artifact or source reference | Reproduction | Confidence |
|---|---|---|---|---|
| ev-podcast-01 | Approved image `localhost/atj-live-trial/podcast:2` has no `ffmpeg`/`ffprobe` binary; has Chromium 152.0.7977.82 at `/usr/bin/chromium`; has `fastapi` 0.141.1, `pydantic` 2.13.5, `uvicorn` 0.53.0, and an importable `playwright` | direct observation (execution) | `runs/team-podcast-env-probe-01.json` | high |
| ev-podcast-02 | The FastAPI app boots cleanly under the system `python3 -m uvicorn server.app:app` (bypassing `run.sh`'s venv step — see ev-podcast-11) with `PODCAST_MEDIA_DIR`/`PODCAST_DB_PATH` pointed at a writable tmpfs path. With an empty media directory: `/healthz` → `200 {"ok":true,"episodes":0}`; `/api/library` → `200` with an empty episode list; `/` serves `index.html`; `/sw.js` serves the service worker with correct headers | direct observation (execution); `server/app.py:210-230` | `runs/team-podcast-server-boot-01.json` | high |
| ev-podcast-03 | Calling `server.app.get_media()` and the progress routes directly (in-process, same commit, real SQLite + a synthetic 5,000,000-byte stand-in media file — see ev-podcast-11 for why real transcoded audio is unavailable here) confirms: full-file `GET` returns `200` with correct `Content-Length`; a mid-file range (`bytes=100000-199999`) returns `206` with `Content-Range: bytes 100000-199999/5000000` and exactly 100000 streamed bytes; a suffix range (`bytes=-500`) returns the correct final 500 bytes; an open-ended range (`bytes=100-`) streams the correct 4,999,900 bytes; a range past EOF returns `416` with `Content-Range: bytes */5000000`; a malformed `Range` header is rejected with `400`. Progress: a first `PUT` (`position_sec=42.5`) is applied and read back exactly; a `PUT` with an older `updated_at` is correctly rejected as `"stale"` and does not overwrite the stored position; a subsequent `PUT` with a newer `updated_at` and `completed=true` is applied and reflected on `GET`; `GET` for an unknown episode returns a default zero-value row (by design, not a 404); `PUT`/media access for an unknown episode raises `HTTPException` ("unknown episode") | direct observation (execution); `server/app.py:100-205`; `server/db.py` `put_progress()` | `runs/team-podcast-media-progress-01.json` | high |
| ev-podcast-04 | `tests/e2e.py` launched Chromium successfully via Playwright against the running server and the app served every static asset the PWA needs (`index.html`, all `web/js/*.js` modules, `manifest.webmanifest`, both icon sizes, `favicon.ico`, `/sw.js`) with `200` responses — no Chromium- or static-asset-related failure. The suite then failed at its first check, `page.wait_for_selector(".ep", timeout=15000)`, with a Playwright `TimeoutError`, because the library was empty: no episodes could be indexed without `ffmpeg`/`ffprobe` (ev-podcast-01) to transcode `source/*.m4a` into `data/media/`. This is an environmental limitation of the approved image, not a defect in the submission — the suite requires populated media by design and the team's own README lists `ffmpeg`/`ffprobe` as a prerequisite | direct observation (execution) | `runs/team-podcast-e2e-attempt-01.json` | high |
| ev-podcast-05 | `README.md:10` states "Source: `source/` 33 files · 11.7 h · 1,360 MB"; the checkout actually has 56 `.m4a` files totaling 2.2 GB (`find source -name '*.m4a' \| wc -l` → 56; `du -sh source` → 2.2G, read directly from the checkout, not executed). `releases.json` lists 41 dated releases + 15 unresolved = 56, consistent with the checkout, not the README. Separately, `README.md:7` claims "34/34 automated checks pass" while `README.md:285` and `DECISIONS.md:9` both claim "42/42", and `tests/e2e.py` itself contains 43 `check(...)` call sites (`grep -c "check("` against the file) | direct observation (file inspection, not execution); `README.md:7,10,285`; `DECISIONS.md:9`; `tests/e2e.py` | inspection reproducible by reading the cited files | high |
| ev-podcast-06 | `tests/e2e.py` also exercises, beyond what ev-podcast-04 reached: OPFS download via a dedicated Worker, blob-URL playback, seek-on-blob, IndexedDB progress mirroring, offline library rendering, offline playback, persisted filters, autoplay-to-next-episode, and played-episode hiding (11 numbered stages, 43 checks). None of these ran; the suite never got past stage 1 in this sandbox (ev-podcast-04) | artifact evidence (source read); `tests/e2e.py` (full file) | source read | high |
| ev-podcast-07 | Every server module (`server/app.py`, `config.py`, `db.py`, `media.py`) and every client script (`web/js/app.js`, `player.js`, `storage.js`, `opfs-worker.js`, `idb.js`, `web/sw.js`) was read; the only `fetch()` targets are same-origin paths (`/api/library`, `/api/progress/{id}`, `/api/rescan`, `/api/media/{id}`). No import of an HTTP client targeting a third-party host, no model/API key/AI SDK reference in `server/` or `web/`. `DECISIONS.md` D11 records "No authentication... the tailnet is the perimeter" as a deliberate design choice for a single-listener, tailnet-only deployment | artifact evidence (source read) | source read | high |
| ev-podcast-08 | `DECISIONS.md` "Proposed — a public listener on Cloudflare" (not decided, not built) discloses that in a *separate, unbuilt* public component, a draft episode's audio would be reachable at a guessed slug, and records an explicit accept-the-risk decision. This does not describe the submitted code: this checkout has no such public route and is unauthenticated only within a private tailnet (ev-podcast-07). Reported because it is part of the submission's documentation, not because it affects this checkout's security posture | team claim (disclosure); `DECISIONS.md` "Proposed — a public listener on Cloudflare" | source read | high |
| ev-podcast-09 | `.agentic/project.yaml` contains only `schema_version`, `project_id`, `slug`, `kind`, `created_at`/`created_on` — five inert metadata lines, no instruction to an agent. A full read of `README.md`, `DECISIONS.md`, `.agentic/project.yaml`, all server and web source, and `releases.json` found no text directing an evaluating agent to change role, skip steps, alter a score, or hide findings. The only "AI"/"agent" content is the podcast library's own subject matter (episode/blog titles about AI agents) | evaluator inference (negative finding); `.agentic/project.yaml` (full file, 5 lines) | source read | high |
| ev-podcast-10 | README "Verification status" and DECISIONS.md "On-device status" claim background audio survives screen-lock ("Confirmed on iPhone, 2026-08-06"), OPFS+range+resume "Verified (Chromium)", and mark real iOS storage quota/`persist()` grant and lock-screen MediaSession controls as explicitly unverified by the team itself ("Not yet measured" / "not yet confirmed separately from playback"). None of this was executed as part of this preparation; no container sandbox can exercise physical-iOS behavior regardless of image contents | team claim (carried from intake, independently re-read here) | `README.md:205-216`; `DECISIONS.md` "On-device status" | n/a — team claim | — |
| ev-podcast-11 | `bash run.sh` fails immediately in the sandbox: `Error: [Errno 30] Read-only file system: '/submission/.venv'`, because the source mount is read-only and `run.sh` tries to create a virtualenv inside the checkout. This is expected given the sandbox's read-only mount policy, not a submission defect — the approved image already provides the packages `run.sh` would have installed (`fastapi`, `uvicorn[standard]`), so ev-podcast-02 through ev-podcast-04 instead invoke `python3 -m uvicorn` directly against those pre-installed packages, with `PODCAST_MEDIA_DIR`/`PODCAST_DB_PATH` redirected to a writable tmpfs path | direct observation (execution); `run.sh:24-34` | `runs/team-podcast-runsh-attempt-01.json` | high |
| ev-podcast-12 | Image `localhost/atj-live-trial/podcast:3` (id `c3670644bc7b`) has `/usr/bin/ffmpeg` and `/usr/bin/ffprobe` (ffmpeg 7.1.5), closing the gap identified in `ev-podcast-01`. `/tmp` is a 64 MB tmpfs (`df -h /tmp` → `64M size, 0 used, 64M avail` at container start) | direct observation (execution) | `runs/team-podcast-env-probe-02.json` | high |
| ev-podcast-13 | With `PODCAST_MEDIA_DIR` set but `PODCAST_DB_PATH` left at its default (`data/app.db`, relative to the read-only `/submission`), the server crashes at import time: `OSError: [Errno 30] Read-only file system: '/submission/data'` (`server/db.py:34`, `connect()` → `path.parent.mkdir(...)`). Uvicorn never binds the port, so Playwright's subsequent `page.goto` fails with `net::ERR_CONNECTION_REFUSED`. This is an operator configuration error in how this preparation invoked the app — `server/config.py` documents `PODCAST_DB_PATH` as a required override alongside `PODCAST_MEDIA_DIR` for any non-default data location — not a defect in the submission | direct observation (execution); `server/config.py` (`DB_PATH`); `server/db.py:33-39` | `runs/team-podcast-e2e-02.json` | high |
| ev-podcast-14 | With both `PODCAST_MEDIA_DIR` and `PODCAST_DB_PATH` pointed at a writable tmpfs path, the server boots correctly and every static/PWA asset (`index.html`, JS modules, manifest, icons, `/sw.js`) returns `200`. The library is still empty (`{"episodes":[]}`) at this point, confirming `index_library()` only scans whatever already exists in `MEDIA_DIR` at startup — it does not transcode. `POST /api/rescan` (`server/app.py:93-97`) is the documented action that drives `media.transcode_all()` and then re-indexes; this matches the submission's own `run.sh`, which calls the equivalent `python -m server.media` before starting uvicorn | direct observation (execution); `server/app.py:43-97` | `runs/team-podcast-e2e-03.json` | high |
| ev-podcast-15 | `POST /api/rescan` against one real source file (`AI_code_reviews_need_the_prompt.m4a`, 18,631,917 bytes) returned `{"transcode":{"done":1,"skip":0,"failed":0},"indexed":1,"removed":0,"dated":0}`; the resulting library entry has `duration_sec: 578.896009`, `size_bytes: 4884617`, correct title-from-filename, and a real `created_at`. The real ffmpeg pipeline works end to end. `tests/e2e.py` then reached **stage 7 of 11**: stage 5 recorded one `[FAIL]`, "seek to 600s landed — 578.9s"; stage 6 ("Progress persisted locally and pushed to server") passed all 4 of its checks (IndexedDB row present, local position reflects the seek, synced/not-dirty, server has the position); stage 7 ("Resume after reload") then stalls — `page.wait_for_selector(".ep", timeout=15000)` times out 15s after `page.reload()`, even though the same selector resolved earlier in the run. On the stage-5 `[FAIL]`: the landed position (578.9s) matches the episode's actual duration (578.896009s) to the tenth of a second — the signature of the player correctly clamping a seek to end-of-media, not of a random failure. The test hardcodes a seek to 600s; this fixture episode (9m39s) is shorter than that. The evidence supports reading this as the fixture (one short episode, forced by the sandbox's disk cap — see `ev-podcast-18`) not satisfying the test's assumption of a longer episode, rather than a defect in the seek/clamp logic. This run's stdout is piped through `tail -34` by the command that produced it, so stages 1-4's individual check results are not preserved in the run record — only that the script reached stage 5 without an unhandled exception, which requires stage 3's download-complete wait to have resolved | direct observation (execution); `tests/e2e.py` stages 5-7; `server/media.py` `transcode_all()` | `runs/team-podcast-e2e-04.json` | high |
| ev-podcast-16 | With two real transcoded episodes (`AI_code_reviews_need_the_prompt.m4a`, `Why_AI_agents_need_test_architects.m4a`; 12 MB combined output) and the full unmodified `tests/e2e.py`: stage 1 passed 4 of 5 checks (fail: "episodes carry blog release dates — 0 of 2 dated" — expected, see below); stage 2 passed; stage 3 ("Download one episode into OPFS") then hit the same `wait_for_function` used in `ev-podcast-15`'s stage 7, but here it is the *download*-complete signal, and it timed out after 90s. Chromium launched and every static asset served correctly beforehand, so this is not a browser-launch or asset-serving problem. On the stage-1 fail: both chosen files are listed under `releases.json`'s own `"unresolved"` section (`"AI_code_reviews_need_the_prompt.m4a"`: "not in the master library — an earlier take, since renamed"; `"Why_AI_agents_need_test_architects.m4a"`: "listed under 'unmapped' in audio-map.yaml — a superseded take"), i.e. the team's own release-date pipeline deliberately excludes both — the fail is fully explained by which two (arbitrary, smallest-by-size) files this preparation happened to pick, not a date-matching defect | direct observation (execution); `tests/e2e.py` stages 1-3; `releases.json` "unresolved" | `runs/team-podcast-e2e-full-01.json` | high |
| ev-podcast-17 | An instrumented single-episode script (console/pageerror captured live, not deferred) clicked the same download control used in `ev-podcast-16` and observed it complete in **1 second**: OPFS held exactly one file (`1.m4a`, 4,884,617 bytes, byte-identical to the transcoded output), IndexedDB recorded `state: "done"` with the matching byte count, `navigator.storage.estimate()` reported the usage growing from ~132 KB to ~5.0 MB (`fileSystem: 4884929`) across the download, and zero console messages or page errors were recorded throughout. This directly contradicts a "the download mechanism is broken" reading of `ev-podcast-16` and narrows that finding to something specific to the two-episode scenario (or to timing/flakiness) rather than the download path in general | direct observation (execution); `web/js/storage.js` `download()`; `web/js/opfs-worker.js` | `runs/team-podcast-download-diag-01.json` | high |
| ev-podcast-18 | `/tmp` is a 64 MB tmpfs in every run (`atj/sandbox.py` `DEFAULT_LIMITS["tmpfs_size"] = "64m"`), and the `atj sandbox run` CLI does not expose an override. The full source library is 56 files / 2.2 GB (`ev-podcast-05`); even at the ~26% transcode ratio the team documents, that would not fit. This preparation instead populated the library with one or two of the smallest real source files (transcoded output 4.9-6.7 MB each). No configuration change was made to the sandbox to work around this — the cap is the framework's, applied identically to every submission, and a full-library execution could not be demonstrated because of it, not because of anything in the submission | direct observation (execution, `df -h /tmp` in `ev-podcast-12`, `ev-podcast-15`, `ev-podcast-16`); `atj/sandbox.py` `DEFAULT_LIMITS` | `runs/team-podcast-env-probe-02.json`, `runs/team-podcast-e2e-full-01.json` | high |
| ev-podcast-19 | Candidate finding, not confirmed by a targeted follow-up: stage 7's stall (`ev-podcast-15`) is plausibly explained by the app's own documented behavior rather than a defect. `web/js/app.js` hides finished episodes by default (`hidePlayed` defaults to `"1"`; `render()`'s visibility filter is `!hidePlayed \|\| !isFinished(e.id) \|\| playing?.id === e.id`, `app.js:105-128`). Stage 6 left the library's one and only episode marked `completed: true`. On `page.reload()`, "currently playing" resets, so that episode would be the *only* one hidden by the default filter — leaving zero `.ep` elements to render, which is exactly what `wait_for_selector(".ep")` timing out looks like. This was not independently confirmed by checking the post-reload DOM or `localStorage` state directly (no further sandbox executions were run once execution was handed back to the operator), so it is recorded as an evaluator inference, not a direct observation. If correct, this is an artifact of testing a one-episode library forced by `ev-podcast-18`'s disk cap, not a defect that would appear against a realistic multi-episode library | evaluator inference; `web/js/app.js:16-19,105-128` | reasoning only — not independently re-executed | medium |

## Tests and execution

| Command or scenario | Result | Output artifact | Safety controls |
|---|---|---|---|
| Environment probe: `ffmpeg`/`ffprobe`/`chromium` presence, Python package versions | ran to completion, exit 0; no ffmpeg/ffprobe, chromium and Python deps present | `runs/team-podcast-env-probe-01.json` | sandboxed, no network, read-only source mount, 60s timeout |
| `python3 -m uvicorn server.app:app` with empty media dir; `/healthz`, `/api/library`, `/`, `/sw.js` requested via `urllib` | ran to completion, exit 0; all four endpoints `200` as expected for an empty library | `runs/team-podcast-server-boot-01.json` | sandboxed, no network, read-only source mount, 60s timeout |
| In-process call of `get_media`, `put_progress`, `read_progress` against a synthetic 5MB media file and a real SQLite DB (see ev-podcast-11 for why synthetic) | script exit 0; all 11 sub-checks (full/range/suffix/open-ended/out-of-range/malformed media requests; put/get/stale/newer/unknown progress) matched expected behavior | `runs/team-podcast-media-progress-01.json` | sandboxed, no network, read-only source mount, 90s timeout |
| `python3 tests/e2e.py http://127.0.0.1:8000` against a live, empty-library server | script exited 1 (`E2E_EXIT:1`) — Playwright `TimeoutError` on the first check, `.ep` never rendered because no episodes were indexed | `runs/team-podcast-e2e-attempt-01.json` | sandboxed, no network, read-only source mount, 120s timeout |
| `bash run.sh` unmodified | exited 1 immediately: read-only filesystem prevents `.venv` creation | `runs/team-podcast-runsh-attempt-01.json` | sandboxed, no network, read-only source mount, 60s timeout |
| Environment probe on image `:3`: `ffmpeg`/`ffprobe` presence, `/tmp` tmpfs size | ran to completion, exit 0; both binaries present, 64 MB tmpfs confirmed | `runs/team-podcast-env-probe-02.json` | sandboxed, no network, read-only source mount, 60s timeout |
| Boot with `PODCAST_MEDIA_DIR` set, `PODCAST_DB_PATH` left default | exit 0 (script level), but the server itself crashed at import (`OSError`, read-only `/submission/data`); Playwright got `ERR_CONNECTION_REFUSED` | `runs/team-podcast-e2e-02.json` | sandboxed, no network, read-only source mount — operator misconfiguration, not a submission defect |
| Boot with both `PODCAST_MEDIA_DIR` and `PODCAST_DB_PATH` set; static assets + empty-library check | ran to completion; server healthy, static/PWA assets `200`, library empty pre-rescan | `runs/team-podcast-e2e-03.json` | sandboxed, no network, read-only source mount |
| `POST /api/rescan` (1 real source file) then `tests/e2e.py http://127.0.0.1:8000` | rescan/transcode succeeded (1 done, 0 failed); e2e reached stage 7 of 11 (1 fail in stage 5, all 4 stage-6 checks pass, stalls in stage 7) | `runs/team-podcast-e2e-04.json` | sandboxed, no network, read-only source mount |
| `POST /api/rescan` (2 real source files) then unmodified `tests/e2e.py` | rescan succeeded; e2e stage 1 (4/5 pass), stage 2 (pass), stage 3 timed out after 90s waiting for download-complete | `runs/team-podcast-e2e-full-01.json` | sandboxed, no network, read-only source mount, 400s timeout |
| Instrumented single-episode download probe (console/pageerror captured live) | download completed in 1s; OPFS, IndexedDB, and `storage.estimate()` all consistent; zero console/page errors | `runs/team-podcast-download-diag-01.json` | sandboxed, no network, read-only source mount, 90s timeout |

## Relevant implementation evidence

| Evidence ID | Path/symbol | Relevance |
|---|---|---|
| ev-podcast-02 | `server/app.py:79-230` (`app`, `healthz`, `service_worker`, `spa_fallback`, static mount) | server startup, static/PWA asset serving |
| ev-podcast-03 | `server/app.py:100-205` (`put_progress`, `read_progress`, `get_media`); `server/db.py` `put_progress()` | byte-range media serving; progress/resume last-write-wins logic |
| ev-podcast-06 | `tests/e2e.py` (full file, 43 checks across 11 stages) | scope of the behavior beyond stage 7: offline mode, autoplay, filters |
| ev-podcast-07 | `server/config.py`; `server/media.py`; `web/js/app.js`, `player.js`, `storage.js`, `opfs-worker.js`, `idb.js`; `web/sw.js` | no third-party network calls; no AI/LLM/API-key reference |
| ev-podcast-11 | `run.sh:1-61`; `server/config.py` (`PODCAST_MEDIA_DIR`, `PODCAST_DB_PATH` env vars) | how the app was started in the sandbox in place of `run.sh` |
| ev-podcast-14, ev-podcast-15 | `server/app.py:43-97` (`index_library`, `rescan`); `server/media.py` `transcode_all()`/`transcode_one()` | the real ffmpeg transcode-and-index pipeline, exercised end to end |
| ev-podcast-19 | `web/js/app.js:16-19,105-128` (`hidePlayed` default, `render()` visibility filter) | candidate explanation for the stage-7 stall |

## Missing or inaccessible evidence

- **`tests/e2e.py`'s 43 automated checks did not run to completion.** The
  furthest any single run reached was stage 7 of 11 (`ev-podcast-15`). Stages
  8-11 — offline library rendering, offline playback, persisted client-side
  filters, and autoplay-to-next-episode — were never exercised. The original
  blocker (no `ffmpeg`/`ffprobe` on the first approved image) was an
  environmental limitation and has been corrected (`ev-podcast-12`); the
  current blocker is the sandbox's 64 MB `/tmp` tmpfs, which cannot hold the
  full 56-file, 2.2 GB source library regardless of image contents
  (`ev-podcast-18`) — also environmental, and specifically the framework's
  resource cap rather than anything about this submission. All of stages 8-11
  remain artifact evidence only (`ev-podcast-06`, `ev-podcast-07`).
- **Two candidate findings about the submission itself, both appropriately
  hedged.** (1) Stage 7's "Resume after reload" stall (`ev-podcast-15`) is
  plausibly explained by the app's own default "hide played episodes" filter
  interacting with a library reduced to one now-fully-played episode
  (`ev-podcast-19`) — a fixture artifact of the disk cap, not independently
  confirmed by re-execution, and not necessarily present against a realistic
  multi-episode library. (2) A two-episode download stalled 90s
  (`ev-podcast-16`) where a one-episode download completed in 1s
  (`ev-podcast-17`); only one run of each was observed, so this is recorded as
  inconclusive rather than a confirmed defect. Neither finding was chased
  further with additional sandbox executions.
- **The stage-5 seek fail is not read as a defect.** "seek to 600s landed —
  578.9s" matches the fixture episode's actual duration (578.896009s) to the
  tenth of a second, the signature of a correct clamp-to-duration, against a
  test that hardcodes an assumption of a longer episode (`ev-podcast-15`).
- **iPhone-specific claims cannot be settled by any container sandbox,
  regardless of image contents or disk cap.** PWA install-to-home-screen,
  background audio with the screen locked, real iOS storage-quota behavior,
  and lock-screen MediaSession controls (`ev-podcast-10`) rest entirely on the
  team's own README/DECISIONS.md account. The team itself marks the
  quota/`persist()` question and the lock-screen-controls question as
  unverified even on their own device.
- **The internal check-count discrepancy was not resolved by execution.**
  README states both "34/34" and "42/42"; the source has 43 `check()` sites
  (`ev-podcast-05`). No run reached the end of the suite, so this preparation
  can confirm the discrepancy exists but not which number, if any, the team
  actually observed.
- **`scripts/sync-releases.py` was not exercised.** It requires a second,
  unrelated local checkout (`BEEKEEPER_WEBSITE_DIR`) that does not exist in
  this event. Its output, `releases.json`, is already committed and was read
  directly (`ev-podcast-05`, `ev-podcast-16`); this only blocks *regenerating*
  release dates, not running the app.
- No criterion is recorded in `evidence_limited_criteria`: every rubric
  criterion (`functional`, `product`, `agentic`, `engineering`, `reliability`,
  `security`, `innovation`) has at least one direct observation or
  independently corroborated artifact citation above, and `functional` and
  `reliability` in particular now carry substantially more execution evidence
  than at the prior revision. Judges should still weigh the gaps listed here —
  they are real — rather than treat any score as fully executed.

## Validation

- [x] Immutable commit verified
- [x] Untrusted instructions ignored
- [x] Execution policy satisfied (sandboxed execution completed; environmental limitations recorded where execution could not proceed)
- [x] Artifact references resolve
- [x] Manifest independently validated
