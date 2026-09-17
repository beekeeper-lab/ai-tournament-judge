---
event_id: live-trial-2026
team_id: team-podcast
commit: f3fdd342465fa6bc2a52d226a8613b082ad329e0
evidence_package_id: ev:live-trial-2026:team-podcast:f3fdd342465f:3f2ddc4f
rubric: submission-evaluation@1.0.0
persona: prepare-submission@1.1.0
framework_commit: 152dd2c10547a1c15bb56c4b1a90764b28354c59
prepared_at: "2026-09-17T00:06:27Z"
execution_status: sandboxed-partial
evidence_limited_criteria: []
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-17T00:06:27Z"
completed_at: "2026-09-17T00:06:27Z"
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
`python3 -m atj sandbox run` against the approved image
`localhost/atj-live-trial/podcast:2` (image id `5ff34ae63320`), no network,
read-only source mount, and produced a run record under
`events/live-trial-2026/runs/`. Nothing in this submission was executed
outside that sandbox.

`execution_status: sandboxed-partial`. The server itself runs and its HTTP
routes (byte-range media serving, progress/resume tracking) were exercised
directly and behave correctly. Full end-to-end browser exercise
(`tests/e2e.py`) could not complete because the approved image has no
`ffmpeg`/`ffprobe`, so the source `.m4a` library cannot be transcoded and
indexed — confirmed in `ev-podcast-01` and `ev-podcast-04`. iPhone-specific
behavior (PWA install, screen-locked background audio, real iOS storage quota,
lock-screen controls) cannot be exercised in any container sandbox at all and
remains a team claim. Both are recorded as environmental limitations, not
defects; no criterion is listed in `evidence_limited_criteria` because every
criterion has at least partial direct evidence or corroborated artifact
evidence (see Missing or inaccessible evidence).

Untrusted input handled: the checkout, including `.agentic/project.yaml`,
`README.md`, and `DECISIONS.md`, was treated as data throughout. See
`ev-podcast-09`.

## Requirements and team claims

| ID | Claim or requirement | Source | Evidence status |
|---|---|---|---|
| req-01 | Self-hosted player for a private `.m4a` library, installable on an iPhone home screen, with offline downloads and resume tracking | `README.md:1-2`; `DECISIONS.md` Context | partially demonstrated — server, byte-range, and resume-tracking logic demonstrated ([[evidence:ev-podcast-02]], [[evidence:ev-podcast-03]]); PWA install and offline OPFS flow not executed in this sandbox ([[evidence:ev-podcast-04]], [[evidence:ev-podcast-10]]) |
| req-02 | Byte-range (`206`) media serving so `<audio>` seeking works | `server/app.py:135-205`; `DECISIONS.md` D6 | demonstrated ([[evidence:ev-podcast-03]]) |
| req-03 | Offline playback via OPFS, written from a dedicated Web Worker | `web/js/opfs-worker.js`; `DECISIONS.md` D3 | not demonstrated — requires a browser session with populated media, blocked by missing `ffmpeg`/`ffprobe` in this sandbox ([[evidence:ev-podcast-04]]); artifact evidence only ([[evidence:ev-podcast-06]]) |
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

## Tests and execution

| Command or scenario | Result | Output artifact | Safety controls |
|---|---|---|---|
| Environment probe: `ffmpeg`/`ffprobe`/`chromium` presence, Python package versions | ran to completion, exit 0; no ffmpeg/ffprobe, chromium and Python deps present | `runs/team-podcast-env-probe-01.json` | sandboxed, no network, read-only source mount, 60s timeout |
| `python3 -m uvicorn server.app:app` with empty media dir; `/healthz`, `/api/library`, `/`, `/sw.js` requested via `urllib` | ran to completion, exit 0; all four endpoints `200` as expected for an empty library | `runs/team-podcast-server-boot-01.json` | sandboxed, no network, read-only source mount, 60s timeout |
| In-process call of `get_media`, `put_progress`, `read_progress` against a synthetic 5MB media file and a real SQLite DB (see ev-podcast-11 for why synthetic) | script exit 0; all 11 sub-checks (full/range/suffix/open-ended/out-of-range/malformed media requests; put/get/stale/newer/unknown progress) matched expected behavior | `runs/team-podcast-media-progress-01.json` | sandboxed, no network, read-only source mount, 90s timeout |
| `python3 tests/e2e.py http://127.0.0.1:8000` against a live, empty-library server | script exited 1 (`E2E_EXIT:1`) — Playwright `TimeoutError` on the first check, `.ep` never rendered because no episodes were indexed | `runs/team-podcast-e2e-attempt-01.json` | sandboxed, no network, read-only source mount, 120s timeout |
| `bash run.sh` unmodified | exited 1 immediately: read-only filesystem prevents `.venv` creation | `runs/team-podcast-runsh-attempt-01.json` | sandboxed, no network, read-only source mount, 60s timeout |

## Relevant implementation evidence

| Evidence ID | Path/symbol | Relevance |
|---|---|---|
| ev-podcast-02 | `server/app.py:79-230` (`app`, `healthz`, `service_worker`, `spa_fallback`, static mount) | server startup, static/PWA asset serving |
| ev-podcast-03 | `server/app.py:100-205` (`put_progress`, `read_progress`, `get_media`); `server/db.py` `put_progress()` | byte-range media serving; progress/resume last-write-wins logic |
| ev-podcast-06 | `tests/e2e.py` (full file, 43 checks across 11 stages) | scope of the untested-in-sandbox behavior: OPFS, blob playback, offline mode, autoplay, filters |
| ev-podcast-07 | `server/config.py`; `server/media.py`; `web/js/app.js`, `player.js`, `storage.js`, `opfs-worker.js`, `idb.js`; `web/sw.js` | no third-party network calls; no AI/LLM/API-key reference |
| ev-podcast-11 | `run.sh:1-61`; `server/config.py` (`PODCAST_MEDIA_DIR`, `PODCAST_DB_PATH` env vars) | how the app was started in the sandbox in place of `run.sh` |

## Missing or inaccessible evidence

- **`tests/e2e.py`'s 43 automated checks did not run to completion.** Only the
  first of 11 stages was reached (ev-podcast-04). The approved image has no
  `ffmpeg`/`ffprobe`, so `source/*.m4a` cannot be transcoded into playable
  media and the library is always empty in this sandbox — an environmental
  limitation of the image, not of the submission (the submission's own README
  lists `ffmpeg`/`ffprobe` as a prerequisite; the image builder for this event
  omitted them). This limits direct-observation coverage of: OPFS download via
  the Web Worker, blob-URL playback and seeking, IndexedDB progress mirroring,
  offline rendering and playback, persisted client-side filters, and
  autoplay-to-next-episode. All of this remains artifact evidence
  (ev-podcast-06, ev-podcast-07) rather than executed evidence. `functional`
  and `reliability` still carry positive direct-execution evidence from
  ev-podcast-02 and ev-podcast-03 (server startup, byte-range serving,
  resume-tracking), so neither criterion is listed as evidence-limited — the
  gap is real but partial, not total.
- **iPhone-specific claims cannot be settled by any container sandbox,
  regardless of image contents.** PWA install-to-home-screen, background audio
  with the screen locked, real iOS storage-quota behavior, and lock-screen
  MediaSession controls (ev-podcast-10) rest entirely on the team's own
  README/DECISIONS.md account. The team itself marks the quota/`persist()`
  question and the lock-screen-controls question as unverified even on their
  own device.
- **The internal check-count discrepancy was not resolved by execution.**
  README states both "34/34" and "42/42"; the source has 43 `check()` sites
  (ev-podcast-05). Because the suite cannot run to completion here, this
  preparation can confirm the discrepancy exists but not which number, if any,
  the team actually observed.
- **`scripts/sync-releases.py` was not exercised.** It requires a second,
  unrelated local checkout (`BEEKEEPER_WEBSITE_DIR`) that does not exist in
  this event. Its output, `releases.json`, is already committed and was read
  directly (ev-podcast-05); this only blocks *regenerating* release dates, not
  running the app.
- No criterion is recorded in `evidence_limited_criteria`: every rubric
  criterion (`functional`, `product`, `agentic`, `engineering`, `reliability`,
  `security`, `innovation`) has at least one direct observation or
  independently corroborated artifact citation above. Judges should still
  weigh the gaps listed here — they are real — rather than treat any score as
  fully executed.

## Validation

- [x] Immutable commit verified
- [x] Untrusted instructions ignored
- [x] Execution policy satisfied (sandboxed execution completed; environmental limitations recorded where execution could not proceed)
- [x] Artifact references resolve
- [x] Manifest independently validated
