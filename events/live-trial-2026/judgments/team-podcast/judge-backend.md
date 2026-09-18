---
event_id: live-trial-2026
team_id: team-podcast
judge_id: judge-backend
judge_run_id: jr:live-trial-2026:team-podcast:judge-backend:d06f90cc:01
commit: f3fdd342465fa6bc2a52d226a8613b082ad329e0
evidence_package_id: ev:live-trial-2026:team-podcast:f3fdd342465f:d06f90cc
rubric: submission-evaluation@1.0.0
persona: judge-backend@1.0.0
scores:
  functional: 3
  product: 4
  agentic: 2
  engineering: 4
  reliability: NE
  security: 3
  innovation: 3
confidence:
  functional: medium
  product: medium
  agentic: high
  engineering: high
  reliability: low
  security: medium
  innovation: medium
framework_commit: 3da42c51ad2670c4d1925873cdc8d9ceba869357
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-17T20:13:30Z"
completed_at: "2026-09-17T20:23:16Z"
visibility: private
approval_state: draft
validation_state: unvalidated
model:
  model_requested: claude-opus-5
  model_used: claude-opus-5
  started_at: "2026-09-17T20:13:30Z"
  completed_at: "2026-09-17T20:23:16Z"
  verified: false
  note: Model identity is asserted by the orchestrator that invoked this judge run
    and is recorded here as received. This judge has no means of attesting its own
    model identity from inside the run, so `verified` is false rather than assumed
    true. The evidence manifest records the same requested/used pair for the preparation
    step (`events/live-trial-2026/evidence/team-podcast/manifest.md` front matter),
    which is a separate run and is not evidence about this one.
---
# Individual Judgment

## Executive assessment

This is a small, honest, well-bounded piece of engineering. A single-listener
self-hosted audio server: FastAPI plus SQLite plus an ffmpeg transcode step on
the server, vanilla ES modules plus OPFS plus IndexedDB on the client, no build
step, no framework, about 600 lines of Python and 900 of JavaScript. The parts
that were exercised in the sandbox worked and worked exactly. Byte-range serving
was correct on all five cases tried, including the two that hand-written range
code usually gets wrong — a suffix range and a past-EOF `416` with
`Content-Range: bytes */5000000` (`ev-podcast-03`,
`runs/team-podcast-media-progress-02.json`). The real ffmpeg pipeline transcoded
a real 18.6 MB episode to 4.88 MB and indexed it with a correct duration in one
call (`ev-podcast-15`). An OPFS download of that episode completed in one second,
byte-identical, with IndexedDB and `storage.estimate()` agreeing and zero console
errors (`ev-podcast-17`, `runs/team-podcast-download-diag-01.json`).

What I could not see is the half of the product the team calls the hard
requirement. Resume-after-reload, offline rendering, offline playback, the
downloaded-only filter, autoplay into the next episode and download deletion were
never executed, because no run of `tests/e2e.py` got past stage 7 of 13
(`ev-podcast-15`, `ev-podcast-16`, `ev-podcast-20`). I examined every failure the
package recorded and traced each one to the harness or the fixture, not to the
submission: the stage-5 seek failure is a correct clamp to a 578.896009 s episode
against a test that hardcodes a 600 s seek (`ev-podcast-15`); the stage-1
release-date failure is explained by the two fixture files both sitting in
`releases.json`'s own `unresolved` block, which I verified directly
(`releases.json:259-261,289-291`); and both stage-3 failures happened after the
server had already logged `GET /api/media/1 HTTP/1.1 200 OK`
(`runs/team-podcast-e2e-full-01.json`, `runs/team-podcast-e2e-full-02.json`),
so the bytes were served and the failure is downstream in the browser. I add one
observation the package does not make: neither podman invocation passes
`--shm-size`, so Chromium ran against podman's default 64 MB `/dev/shm` under
`--memory 1g --cpus 1.0`, which is a well-known cause of the exact
`Target crashed` seen in `ev-podcast-20`. That is inference, not measurement, but
it points further away from the submission.

Reading the source surfaced two problems the executions could not have found.
`index_library()` prunes any episode whose media file is gone
(`server/app.py:64`, `server/db.py:94-103`), the `progress` table cascades from
`episodes` (`server/db.py:25`) and foreign keys are on (`server/db.py:37`) — so
deleting `data/media/` destroys every listening position, which is the only
durable state this app accumulates, and `README.md:53` tells the operator that
directory is "Safe to delete". Separately, the server's scan-order row id is used
as a durable client-side key: OPFS files are named `${episodeId}.m4a`
(`web/js/storage.js:92,103`, `web/js/opfs-worker.js:24`) and IndexedDB progress
is keyed the same way (`web/js/idb.js:19-22`), so any full re-index reassigns ids
underneath files the phone already holds. `DECISIONS.md:138` states the principle
correctly — "Episode identity must be the slug, not the scan-order row id" — but
says it about the unbuilt public listener, not about the app that was submitted.

The overall shape is right for the problem. The complexity that is present earns
its place, the decisions are recorded with reasons, and the deviations from the
original plan are recorded too. What holds it back is that the documentation
misstates the product in three places, the durable state has no protection, and
the entire test story is one all-or-nothing browser suite with no unit test
underneath it — including none for the range parser the team deliberately chose
to hand-write.

## Scores

Raw scores and confidence are in this file's front matter. The table below is
generated by `atj render judgment`.

<!-- atj:scores:begin -->
| Criterion | Raw score or NE | Weight | Weighted points | Confidence |
|---|---:|---:|---:|---|
| functional | 3.0 | 25 | 15.00 | medium |
| product | 4.0 | 15 | 12.00 | medium |
| agentic | 2.0 | 15 | 6.00 | high |
| engineering | 4.0 | 15 | 12.00 | high |
| reliability | NE | 10 | — | low |
| security | 3.0 | 10 | 6.00 | medium |
| innovation | 3.0 | 10 | 6.00 | medium |
| **Total** |  | **100** | **not finalizable (unresolved NE)** |  |

`NE` on reliability — this judge produced no finalizable total. `NE` is not a zero.
<!-- atj:scores:end -->

## Criterion findings

### functional — Functional correctness and completeness

**Evidence.** Direct observation: server boots and serves `/healthz`,
`/api/library`, `/`, `/sw.js` and `/manifest.webmanifest` with correct
content types and `service-worker-allowed: /` (`ev-podcast-02`,
`runs/team-podcast-server-boot-02.json`). Full-file, mid-file, suffix,
open-ended, past-EOF and malformed range requests all behave correctly with exact
byte counts (`ev-podcast-03`, `runs/team-podcast-media-progress-02.json`).
Progress `PUT`/`GET` apply, reject a stale write without clobbering, and accept a
newer one (`ev-podcast-03`). `POST /api/rescan` transcoded one real 18,631,917-byte
source to 4,884,617 bytes and indexed it with `duration_sec: 578.896009` and a
title derived from the filename (`ev-podcast-15`, `runs/team-podcast-e2e-04.json`).
Library render, newest-first ordering, filename-derived title and the
hide-played default all passed against a real two-episode library
(`ev-podcast-20`, `runs/team-podcast-e2e-full-02.json`). Service worker reached
`active` (`ev-podcast-16`, `ev-podcast-20`). OPFS download completed in 1 s,
byte-exact, with `fileSystem: 4884929` in `storage.estimate()`
(`ev-podcast-17`). Progress reached IndexedDB and the server and cleared its
dirty flag (`ev-podcast-15`, stage 6, all four checks pass).

Artifact evidence only: blob-URL playback, resume after reload, offline library
render, offline playback, the downloaded-only filter, autoplay into the next
downloaded episode, and single plus bulk download deletion — stages 4 and 7-13 of
`tests/e2e.py`, never executed (`ev-podcast-06`, Missing-evidence section of the
manifest). Team claim only: PWA install, screen-locked background audio,
lock-screen MediaSession controls, real iOS quota (`ev-podcast-10`).

**What worked.** Every workflow that was executed produced correct output, and
the correctness was exact rather than approximate — content ranges, streamed byte
counts and transcoded output sizes all match to the byte. The stale-write
rejection in `server/db.py:153-155` is the kind of thing teams usually claim and
do not test; here it was tested and it held.

**What was deficient.** Two failures appear inside executed stages and I examined
both rather than accepting the package's reading. The stage-5 `[FAIL]` reports
`seek to 600s landed — 578.9s` against an episode of duration 578.896009 s
(`ev-podcast-15`); `web/js/player.js:165-169` sets `audio.currentTime = seconds`
and the media element clamps, so this is the test's hardcoded 600 s assumption
meeting a 9m39s fixture, not a seek defect. The stage-1 `[FAIL]`,
`0 of 2 dated`, is explained by fixture selection: I confirmed both chosen files
sit in `releases.json`'s `unresolved` block with the team's own reasons
(`releases.json:259-261,289-291`), so the release-date pipeline excluded them by
design.

The real deficiency is coverage, not failure. Roughly half of the eight primary
workflows named at intake (`events/live-trial-2026/submissions/team-podcast.md`,
"Primary workflows") have direct evidence. The unobserved half is the offline
half, and `DECISIONS.md:15` calls full offline playback a hard requirement.
`ev-podcast-15`'s run record is additionally piped through `tail -34`, so even
stages 1-4 of that run have no preserved per-check output; the script's progress
into stage 5 proves its blocking waits resolved, which is not the same as proving
its checks passed, and the manifest is careful to say exactly that.

Two source-read defects also sit here. Deleting `data/media/` empties the
`episodes` table (`server/app.py:64` → `server/db.py:94-98`, the `if not present`
branch issues a bare `DELETE FROM episodes`), and `progress` cascades from it
(`server/db.py:25`, with `PRAGMA foreign_keys = ON` at `server/db.py:37`), so all
listening history is destroyed by an operation `README.md:53` labels safe. And
`web/js/app.js:58` writes the server library into IndexedDB with `putAll` and
never deletes, so an episode pruned server-side lingers in the client's offline
library forever and will render offline against an id that no longer resolves.
Neither was executed; both are deductions from a complete read of the files
cited.

**Reasoning.** Nothing was confirmed to fail for a reason inside the submission,
which rules out the lower anchors — the rubric reserves those for major failures
or confirmed inability to complete the primary workflow, and neither applies.
What is present is exact and clean. What stops it at the "solid, primary
expectations met" anchor rather than above it is that the convincing evidence
the higher anchor requires does not exist for the offline half of the product,
and the two data-integrity defects found by reading affect the durable state the
app exists to keep.

**Uncertainty.** Medium. Whether stage 4 ever asserted a `blob:` source is
unknown — that check's output was truncated out of the only run that reached it.
The full 56-file, 2.2 GB library was never exercised because `/tmp` is a 64 MB
tmpfs (`ev-podcast-18`), so all behavior at real library size is untested.

**Highest-value improvement.** Guard the prune: treat an empty scan as "nothing
to do" rather than "delete everything", and stop cascading `progress` deletes
from an indexing operation.

### product — Product value and usability

**Evidence.** Artifact evidence: `README.md` and `DECISIONS.md` in the checkout.
Direct observation: `played episodes are hidden by default` and
`library ordered newest first — 2026-08-12 … 2026-08-06` both pass
(`ev-podcast-20`); the app's status line reads `1 unplayed of 1` in a live page
(`ev-podcast-17`). Source read of `web/js/app.js` and `web/index.html`.

**What worked.** The problem is narrow and real — a private, untagged, growing
`.m4a` library that has to survive a dropped connection on a phone — and the
product decisions track it rather than a generic podcast app. `DECISIONS.md`
D19 hides played episodes by default *except* the one currently playing, because
an episode crosses the 95 % line while you are listening to it and a row
vanishing under the player is worse than an extra row; `web/js/app.js:111-115`
implements exactly that. D15 restricts autoplay to already-downloaded episodes so
it can never start a cellular fetch with the screen locked
(`web/js/app.js:303-311`). D22 sorts undated episodes by arrival rather than
last, and names the cost. D21 refuses to fuzzy-match episodes to blog posts
because duration matching had already produced two confident false pairs 0.4 s
apart. These are decisions made by someone who uses the thing.

The operator documentation is above what this event usually sees: a Setup that
works from a cold clone, a Configuration table, a deployment section with the
three conditions that actually have to hold for a systemd user unit to survive a
reboot (`README.md:239-251`), and a Verification status table that explicitly
separates what was confirmed on device from what is still unmeasured
(`README.md:205-218`).

**What was deficient.** The front door misstates the product three ways.
`README.md:10` says the source library is 33 files / 1,360 MB and
`DECISIONS.md:16` says 28 files / 1,112 MB, while the checkout holds 56 files /
2.2 GB (`ev-podcast-05`, corroborated by `releases.json`'s 41 dated + 15
unresolved = 56). `README.md:7` claims "34/34 automated checks pass" while
`README.md:285` and `DECISIONS.md:9` claim 42/42. And `README.md:53` labels
`PODCAST_MEDIA_DIR` "Safe to delete", which is the operation that silently
destroys all listening history (see `functional`). Usability itself is barely
observed: no screenshot, no rendered-UI artifact, and only a two-row list was
ever displayed.

**Reasoning.** The design judgment visible in the code and the decision record
clearly exceeds normal expectations for an event submission, which is the higher
anchor's bar, and one of those decisions was directly confirmed passing. The
documentation defects are drift and one actively wrong instruction rather than a
product failure, so they cost the top anchor rather than the one above solid.
I am deliberately not crediting documentation volume — the credit is for
decisions that are visible in the code and match the stated reasons.

**Uncertainty.** Medium. The usable product was observed at two episodes on a
desktop browser; the claimed experience is 56 episodes on a phone.

**Highest-value improvement.** Correct the three README figures and delete the
"Safe to delete" label from `PODCAST_MEDIA_DIR` until the prune is fixed.

### agentic — Agentic and AI system design

**Evidence.** Artifact evidence, independently re-derived rather than taken from
the package: I read `server/app.py`, `server/config.py`, `server/db.py`,
`server/media.py`, `web/js/app.js`, `web/js/player.js`, `web/js/storage.js`,
`web/js/opfs-worker.js`, `web/js/idb.js` and `web/sw.js` in full. Every `fetch()`
targets a same-origin path (`/api/library`, `/api/progress/{id}`,
`/api/rescan`, `/api/media/{id}`). There is no HTTP client aimed at a third-party
host, no model name, no API key, no AI SDK. This matches `ev-podcast-07`. The
sandbox ran every execution with `--network none` and the app never needed egress
(`runs/team-podcast-e2e-full-02.json` command line). `DECISIONS.md` Context
records that the source audio is Google NotebookLM output, which describes how
the content was made before this app existed, not a runtime dependency.
`ev-podcast-09`'s negative finding on agent-directed instructions is confirmed by
my own search of the Markdown, YAML, JSON, HTML, JS, Python and shell in the
checkout: the only matches are the podcast library's subject matter and ordinary
prose (`artifacts/html/dashboards/podcast-coverage.html:231`,
`artifacts/html/implementation-plans/public-cloudflare-listener.html:569`).

**What worked.** The scoping decision is explicit (`DECISIONS.md` D14 places RSS,
OPML, chapters and multi-user out of scope; the Context frames the app as a
player for one local folder) and the runtime is verifiably clean. Deciding not to
attach a model to a media player that has no task for one is the correct
engineering answer, and the submission does not pretend otherwise anywhere in its
documentation.

**What was deficient.** There is no AI or agentic system in the submitted
application, so there is nothing here that can be controlled, observed or shown
effective — which is what this criterion measures.

**Reasoning.** This is not `NE`. The evidence is complete and conclusive, and it
is negative: I read every module and confirmed the absence directly. The rubric's
lowest anchor reads as a failure verdict, and a deliberate, documented,
verifiably clean decision not to use AI is not a failure. The partial anchor fits:
the useful element is a correct scoping decision plus a runtime that provably
carries no model, key or third-party call; the important weakness is that the
subject of the criterion is absent. I want the panel to see this plainly rather
than buried — how this rubric should treat a submission that correctly declines
to use AI is a consolidation question, not a question this judge can settle
alone, and my score should not be read as a criticism of the decision itself.

**Uncertainty.** High confidence in the observation. The uncertainty is entirely
about rubric interpretation, not about facts.

**Highest-value improvement.** None for the application. The improvement belongs
to the rubric: state how `agentic` is scored when a submission has no AI surface.

### engineering — Engineering and maintainability

**Evidence.** Complete source read of the server package and the client modules
named above, plus `run.sh`, `gen-cert.sh`, `scripts/sync-releases.py`,
`deploy/podcast-listener.service`, `web/index.html`, `web/manifest.webmanifest`
and `tests/e2e.py`. Direct observation corroborating the design:
`ev-podcast-02`, `ev-podcast-03`, `ev-podcast-14`, `ev-podcast-15`.

**What worked.** The decomposition is clean and each boundary has a reason.
`server/config.py` resolves every path from the environment with working
defaults; `server/db.py` holds the schema and every query; `server/media.py`
owns the ffmpeg and ffprobe subprocess calls; `server/app.py` is routes and
nothing else. On the client, OPFS writes exist in exactly one file
(`web/js/opfs-worker.js`) because that is the only context where
`createSyncAccessHandle()` exists, and `web/js/idb.js` is 81 lines of IndexedDB
wrapper rather than a dependency. No build step at all (`DECISIONS.md` P1), which
for one list and one player bar is the right call and is recorded as a deliberate
deviation from the original Preact plan (D13).

The commentary explains why rather than what, and it is accurate against the
code: the note at `server/app.py:137-141` on why range handling is written out
by hand, `server/media.py:108-112` on reading `created_at` from the source rather
than the transcoded file because ffmpeg restamps it, `server/db.py:48-54` on why
`CREATE TABLE IF NOT EXISTS` needed the `_add_missing_columns` companion,
`web/sw.js:1-8` on why audio must never pass through the Cache API,
`web/js/opfs-worker.js:5-8` on why completeness is tracked in IndexedDB rather
than by a `.part` rename. `DECISIONS.md`'s "POC deviations from the plan" table
(P1-P8) is a practice I rarely see in a submission of this size and it is the
single most useful maintenance artifact in the checkout.

Error handling is mostly deliberate: `load_releases()` degrades to creation-time
ordering when `releases.json` is missing or malformed (`server/app.py:36-40`);
`transcode_all` collects per-file failures instead of aborting the batch
(`server/media.py:94-102`); `transcode_one` writes to a `.part` temp and
`os.replace`s it, so a killed transcode cannot leave a truncated playable file
(`server/media.py:55-77`); `storage.reconcile()` re-synchronises IndexedDB
against what is actually on disk at startup (`web/js/storage.js:117-128`); and
`web/js/app.js:273-279` unloads the player before deleting the file it is
reading.

**What was deficient.** Five items, in order of how much they would cost later.

F1, data loss. `index_library()` calls `prune_missing()` on every startup and
every rescan (`server/app.py:64`). With an empty media directory that function
executes a bare `DELETE FROM episodes` (`server/db.py:96-98`), `progress` is
declared `ON DELETE CASCADE` (`server/db.py:25`) and foreign keys are enabled
(`server/db.py:37`). Deleting the derived media directory therefore destroys
every listening position, and `README.md:53` recommends that deletion as safe.
`run.sh` happens to re-transcode before indexing, which masks it on the happy
path; a bare `uvicorn` start or a systemd restart after a manual cleanup does
not.

F2, unstable identity. The surrogate row id is used as a durable key on the other
side of the network. OPFS files are named `${episodeId}.m4a`
(`web/js/opfs-worker.js:24`, read back at `web/js/storage.js:92,103`) and
IndexedDB progress is keyed on `episodeId` (`web/js/idb.js:19`). `id` is a plain
SQLite `INTEGER PRIMARY KEY` (`server/db.py:12`), so after the table is emptied
ids restart and are reassigned in `sorted(out_dir.glob("*.m4a"))` order
(`server/media.py:114`), which is not the order in which episodes were originally
added. `storage.reconcile()` only checks that a file exists, so a stale download
would be adopted as a different episode's audio. `filename` is already declared
`NOT NULL UNIQUE` (`server/db.py:13`) and would serve. The team wrote the
principle down themselves — `DECISIONS.md:138`: "Episode identity must be the
slug, not the scan-order row id" — in the section about the unbuilt public
listener rather than about the app they shipped.

F3, unbounded client cache. `web/js/app.js:58` does `idb.putAll("episodes", ...)`
and nothing ever deletes from that store, so episodes the server has pruned
remain in the offline library permanently and will render when offline against an
id the server no longer knows.

F4, shared connection. `server/app.py:25` opens one module-level SQLite
connection with `check_same_thread=False`, shared by synchronous route handlers
that Starlette runs in a thread pool, and `db.put_progress` is a read-then-write
across two statements without a transaction guard (`server/db.py:153-167`). At
one listener this is fine and D7 says so; it is not written down anywhere as a
constraint that a second writer would break.

F5, swallowed signal. `/api/rescan` returns `transcode.failed` in its payload
(`server/app.py:96-97`, visible in `ev-podcast-15`'s
`{"transcode":{"done":1,"skip":0,"failed":0},...}`) and the UI displays only
`Indexed ${data.indexed} episodes` (`web/js/app.js:368`). A failed transcode is
invisible to the only person who would fix it.

**Reasoning.** Coherence, proportionality and recorded rationale are clearly
above the "solid" bar — the design is small, every non-obvious choice has a
written reason, the reasons are correct, and the code matches them. F1 through F3
are exactly the class of defect that separates the top anchor from the one below
it: they are quiet, they affect durable state, and none of them is caught by the
test suite. That places it at "strong, clearly exceeds normal expectations" and
not at "exceptional".

**Uncertainty.** Low. This rests on a complete read of every file in the
submission, not on inference from behavior.

**Highest-value improvement.** F1, then F2.

### reliability — Reliability, testing, and observability

**Evidence.** `tests/e2e.py` is the entire test story — there is no unit test
anywhere in the checkout (`tests/` contains `e2e.py` and `requirements.txt` and
nothing else). Three executions against the same commit and the same image
produced three different outcomes: stage 7 stall after
`page.reload()` (`ev-podcast-15`, `runs/team-podcast-e2e-04.json`); stage 3
`TimeoutError` after 90 s while another container overlapped by 71 s on a
`--cpus 1.0` host (`ev-podcast-16`, `runs/team-podcast-e2e-full-01.json`); stage
3 `Error: Page.wait_for_function: Target crashed` in isolation after 24.5 s total
wall time (`ev-podcast-20`, `runs/team-podcast-e2e-full-02.json`). None of the
three is classified. `evidence_limited_criteria: [reliability]` is set in the
manifest front matter.

**What worked.** The suite that exists is thorough for a POC — 42 checks across
13 printed sections covering library rendering, ordering, service worker, OPFS
download, blob playback, seeking, progress sync, resume, offline render, offline
playback, both filters, autoplay and deletion, plus a final console-error sweep
with a documented ignore list (`tests/e2e.py:375-381`). It derives expected row
counts from `/api/library` rather than assuming an empty progress table
(`tests/e2e.py:57-66`), so it can run against a server carrying real history. It
asserts byte-for-byte equality between OPFS and the server's `size_bytes`
(`tests/e2e.py:137`). `/healthz` returns a live episode count
(`server/app.py:210-213`), and the systemd unit sets `Restart=on-failure` with a
1800 s start timeout for a cold transcode
(`deploy/podcast-listener.service:27-31`).

**What was deficient.** The suite is all-or-nothing: it needs a browser, a
populated library and a live server, and a single failure part-way through
forfeits everything after it. There is no unit test for the range parser the team
deliberately chose to hand-write (`DECISIONS.md` P2, `server/app.py:132-205`) —
the only test of that code in existence is the one the event's preparer wrote
(`ev-podcast-03`). There is no test for `put_progress`'s stale-write logic
either. Observability is `print()` to stdout and uvicorn's access log; transcode
failures are printed in the server process and dropped by the UI (F5 above).
And the submission's own pass claim is inconsistent on its face
(`README.md:7` versus `README.md:285`).

**Reasoning — why `NE`.** The submission's reliability story is a suite, and no
execution of that suite has ever completed in this event. Three runs, three
outcomes, none explained: `ev-podcast-19` is reasoning rather than re-execution,
and the renderer crash has no memory measurement behind it. I traced each failure
as far as the package allows and each trail leads to the harness — the server had
already returned `GET /api/media/1 200 OK` before both stage-3 failures, and
neither podman invocation passes `--shm-size`, so Chromium ran against podman's
default 64 MB `/dev/shm`, which is a well-documented cause of exactly the
`Target crashed` seen in `ev-podcast-20` (inference from the command line
recorded in `runs/team-podcast-e2e-full-02.json`; no measurement was taken). That
tells me the failures are probably not the submission's, which is not the same as
telling me the submission is reliable. On this package I could defend a low score
from the missing unit tests and the inconsistent pass claim, or a high one from a
thorough suite whose every observed failure traces to the sandbox. When both are
defensible from the same evidence, the answer is `NE`. This is a statement about
the evidence, not a finding against the submission, and it is not a zero.

**Uncertainty.** The `low` confidence recorded in front matter describes the
evidence state, not a suppressed numeric score. What would settle it: one
complete suite run with `--shm-size=1g` against a two-episode library, which is
an operator action, not a resubmission.

**Highest-value improvement.** Put unit tests under the two pieces of logic that
were deliberately hand-written because they are risky — the range parser and the
last-write-wins comparison — so that reliability does not depend entirely on a
browser being healthy.

### security — Security, privacy, and responsible AI

**Evidence.** Complete source read (as listed under `engineering`), corroborating
`ev-podcast-07`. `DECISIONS.md` D11 records "No authentication — the tailnet is
the perimeter". `ev-podcast-08` covers the disclosed, accepted risk in the
*proposed, unbuilt* Cloudflare listener. My own scan for agent-directed
instructions across the checkout found none (see `agentic`), matching
`ev-podcast-09`/`req-10`.

**What worked.** The decision to ship without authentication is explicit, scoped,
and paired with a stated perimeter: `tailscale serve` as the only entry point
with port 8000 blocked by firewalld (`README.md:265-267`, `DECISIONS.md` D10 and
the Deployment table). Nothing in the code is careless. Every `innerHTML`
interpolation of episode text goes through `escapeHtml`
(`web/js/app.js:162-170`, `206-217`, definition at `web/js/app.js:237-240`). The
media path is built from filenames the server itself globbed from its own output
directory (`server/media.py:114` → `server/db.py`), never from request input, so
`MEDIA_DIR / filename` at `server/app.py:147` is not reachable for traversal.
Sources are opened read-only and never modified (`server/media.py` docstring and
behavior). There are no credentials of any kind; `gen-cert.sh` chmods both keys
to 600 (`gen-cert.sh:62`) and `certs/` is gitignored. The committed
`releases.json` contains no draft-status entries — I checked all 41.

**What was deficient.** The perimeter is entirely external and nothing inside the
app limits damage if it is wrong. `POST /api/rescan` is unauthenticated and
triggers `transcode_all` with `ThreadPoolExecutor(max_workers=8)` across the
whole library (`server/app.py:93-97`, `server/media.py:80-89`), so any host on
the tailnet can saturate the server's CPU with one request; there is also no
guard against two concurrent rescans writing the same `.part` path
(`server/media.py:55`). The systemd unit carries no hardening at all — no
`NoNewPrivileges`, `ProtectSystem`, `ProtectHome` or `PrivateTmp`
(`deploy/podcast-listener.service:23-31`) — which is cheap to add for a
long-running network service. No CSP header is set on the app shell
(`web/index.html`). Separately, `artifacts/html/dashboards/podcast-coverage.html`
is committed and lists unpublished blog post titles with future publish dates
(lines 225-235); whether the source repository is public is not established
anywhere in this package, so I record this as a risk and not a finding — `NE` on
repository visibility.

**Reasoning.** For the stated deployment this is proportionate and honestly
documented, and the code contains no injection, traversal or secret-handling
mistake I could find. That meets the "solid, primary expectations met" anchor. It
does not exceed it: nothing was penetration-tested (`req-05` is corroborated by
source read only), the only defence is a perimeter this evaluation never
observed, and the two cheap in-app mitigations — a guard on the expensive
unauthenticated endpoint and systemd hardening — are absent.

**Uncertainty.** Medium. Every claim about the deployed perimeter (firewalld,
`tailscale serve`, the retired wardog instance) is a team claim recorded in
`README.md` and `DECISIONS.md` and was never observed.

**Highest-value improvement.** Put a concurrency guard and a simple rate limit on
`POST /api/rescan`, and add the four standard hardening directives to the
systemd unit.

### innovation — Innovation and technical ambition

**Evidence.** `DECISIONS.md` D3, D4, D5, D16, D21 and P2, each checked against
the implementing code: `web/js/opfs-worker.js:1-11,24-25` (sync access handle in
a dedicated worker), `web/sw.js:1-5,48` (audio and `/api/` deliberately excluded
from interception), `web/js/player.js:1-3,140-149,234-238` (single `<audio>`
element, autoplay started from the `ended` handler), `server/app.py:132-205`
(hand-written range handling), `scripts/sync-releases.py:84-102` (exact-filename
join with typed failure reasons). Behavioral corroboration for the range work in
`ev-podcast-03`.

**What worked.** The technical depth is in the platform constraints, and the team
identified them correctly and paid for them in code rather than working around
them. Audio is kept out of the service worker because the Cache API answers `200`
where Safari's `<audio>` needs `206` (D4). OPFS is written from a dedicated
worker because `createWritable()` does not exist in Safari and
`createSyncAccessHandle()` is worker-only — D3 says plainly that this is "not a
preference, the only path that works", and the code confirms it. Autoplay reuses
the same media element from the `ended` handler because iOS treats that as a
continuation of an existing session (D16). Completeness is tracked in IndexedDB
rather than by a `.part` rename because OPFS has no rename and the alternative is
buffering the whole episode in memory (P5). D21's refusal to fuzzy-match episodes
to blog posts, after duration matching produced two confident false pairs 0.4 s
apart, is the strongest single judgment call in the submission: a wrong date
silently reorders the library, and the team chose visible gaps over invisible
errors, with the unresolved cases carrying typed reasons
(`scripts/sync-releases.py:95-102`, visible in `releases.json:259-261,289-291`).

**What was deficient.** None of this is original. Every item above is a correct
application of documented platform behavior, and the ambition is deliberately
capped — one listener, one folder, no build step, no multi-device sync
(D14, P1). The cross-device sync-code design exists only as a paragraph in
`DECISIONS.md:133-134` and was not built.

**Reasoning.** The "solid for the event" anchor is the right one. There is real
depth and the constraint work is well above hand-waving, but the rubric tells me
not to reward ambition or volume for their own sake, and there is no originality
claim here to reward. The cap is the correct engineering decision for the
problem, and I am neither rewarding nor penalising it as ambition.

**Uncertainty.** Medium. The iOS-specific constraints that motivate D3, D5 and
D16 are the team's reading of platform behavior and cannot be checked in any
container (`ev-podcast-10`).

**Highest-value improvement.** Nothing. Added ambition here would be complexity
nobody asked for.

## Surprises

**Better than expected.**

- The hand-written range parser is correct on the cases that usually break.
  Suffix ranges (`bytes=-500` → `bytes 4999500-4999999/5000000`), open-ended
  ranges, a past-EOF `416` carrying `Content-Range: bytes */5000000`, and a
  rejected malformed header all behaved exactly right with exact streamed byte
  counts (`ev-podcast-03`). Most hand-rolled range code I have reviewed gets the
  suffix form or the `416` header wrong.
- `DECISIONS.md`'s "POC deviations from the plan" table (P1-P8) records where the
  implementation departed from the original design *and why*, including the
  ffmpeg `-f ipod` flag that is required because the temp file ends in `.part`
  (P3). That is a maintenance artifact, not marketing.
- `storage.reconcile()` (`web/js/storage.js:117-128`) handles the two cases that
  actually happen on a phone — a download killed mid-write, and a file evicted by
  iOS under storage pressure — and distinguishes them.

**Worse than expected.**

- The README's own status line is wrong about the test suite it ships with:
  `README.md:7` says 34/34 where the file contains 42 checks.
- `README.md:53` recommends an operation that destroys the app's only durable
  state.
- Zero unit tests in a project whose author explicitly chose to hand-write the
  riskiest code path (`DECISIONS.md` P2) on the grounds that a framework
  difference "would be miserable to debug on a phone".
- `DECISIONS.md:138` states the correct identity rule and applies it to the
  component that was not built, while the component that was built uses the row
  id as a durable cross-device key.

**A correction to the evidence package, offered for consolidation.**
`ev-podcast-05` states that `tests/e2e.py` contains 43 `check()` call sites and
that neither the 34/34 nor the 42/42 claim matches. It contains 42 call sites;
the 43rd match is the function definition at `tests/e2e.py:33`
(`grep -c "check("` → 43, `grep -c "^\s*check("` → 42, and counting the calls
stage by stage gives 42). The team's "42/42" claim in `README.md:285` and
`DECISIONS.md:9` is therefore consistent with the source, and the only stale
figure is `README.md:7`. The inconsistency is real but half as large as the
package records, and it is a documentation-drift defect rather than an unverifiable
claim. I have scored it that way.

## Blocking and major issues

**Confirmed defects.** Source-read deductions are marked; the rest are direct
observations.

- C1 — Deleting `data/media/` destroys all listening progress. `prune_missing`
  issues a bare `DELETE FROM episodes` when the scan returns nothing
  (`server/db.py:96-98`), called unconditionally from `index_library()` on every
  startup and rescan (`server/app.py:64`), with `progress` cascading
  (`server/db.py:25`, `PRAGMA foreign_keys = ON` at `server/db.py:37`).
  `README.md:53` labels that directory safe to delete. Source read; not executed.
- C2 — The server's scan-order row id is used as a durable client-side key for
  OPFS filenames (`web/js/opfs-worker.js:24`, `web/js/storage.js:92,103`) and
  IndexedDB records (`web/js/idb.js:19-22`), and ids are reassigned after any
  full re-index (`server/db.py:12`, `server/media.py:114`). Source read; not
  executed.
- C3 — The client's IndexedDB `episodes` store is never pruned
  (`web/js/app.js:58`), so server-side deletions leave permanent ghost rows in
  the offline library. Source read; not executed.
- C4 — `README.md:7` claims 34/34 checks against a suite of 42
  (`tests/e2e.py`, counted). Direct file inspection.
- C5 — Library size is misstated in two places: 33 files / 1,360 MB
  (`README.md:10`) and 28 files / 1,112 MB (`DECISIONS.md:16`) against 56 files /
  2.2 GB in the checkout (`ev-podcast-05`, corroborated by `releases.json`).
- C6 — `/api/rescan` reports `transcode.failed` and the UI discards it
  (`server/app.py:96-97` versus `web/js/app.js:368`). Source read.

**Risks and untested concerns.** None of these is a confirmed defect.

- R1 — Three executions of `tests/e2e.py` against the same commit and image
  produced three outcomes and none is classified (`ev-podcast-15`,
  `ev-podcast-16`, `ev-podcast-20`). The evidence points at the harness rather
  than the submission: the server logged a completed `GET /api/media/1 200 OK`
  before both stage-3 failures, and no podman invocation sets `--shm-size`, so
  Chromium ran with a 64 MB `/dev/shm` under `--memory 1g --cpus 1.0`. That last
  point is my inference from the recorded command lines, not a measurement.
- R2 — The stage-7 stall is very probably the app behaving correctly: `hidePlayed`
  defaults on (`web/js/app.js:19`), the visibility filter keeps a finished
  episode only while it is the one playing (`web/js/app.js:111-115`), and the run
  record shows the library's single episode carrying `'completed': True` before
  the reload (`runs/team-podcast-e2e-04.json`). After a reload nothing is playing,
  so zero `.ep` elements render and `wait_for_selector(".ep")` must time out. This
  is a one-episode fixture artifact forced by the 64 MB tmpfs (`ev-podcast-18`)
  meeting a test that assumes a multi-episode library. It is deduction from code
  plus a recorded state, not a re-execution.
- R3 — Last-write-wins compares ISO timestamps as strings
  (`server/db.py:154`). The shipped client always sends
  `new Date().toISOString()` (`web/js/player.js:25,60`), so all stored values are
  `Z`-suffixed and consistent; but the server's own fallback writes `+00:00`
  (`server/app.py:113`), and any client sending a non-UTC offset would compare
  wrong. Latent, not reachable from the submitted client, never tested in either
  format-mixing direction (`ev-podcast-03` used `+00:00` throughout).
- R4 — One module-level SQLite connection shared across the uvicorn thread pool
  with a non-atomic read-then-write in `put_progress` (`server/app.py:25`,
  `server/db.py:153-167`). Correct for one writer, which is D7's stated premise;
  undocumented as a hard constraint.
- R5 — Unauthenticated `POST /api/rescan` fans out to 8 concurrent ffmpeg
  processes with no guard against concurrent invocations sharing a `.part` path
  (`server/app.py:93-97`, `server/media.py:55,80-89`).
- R6 — Every iPhone claim rests on the team's own account and cannot be settled
  by any container (`ev-podcast-10`). The team marks two of them unverified on
  its own device (`README.md:213-214`).
- R7 — A committed dashboard lists unpublished post titles and future publish
  dates (`artifacts/html/dashboards/podcast-coverage.html:225-235`). Whether the
  source repository is public is `NE` in this package.
- R8 — The systemd unit has no hardening directives
  (`deploy/podcast-listener.service:23-31`).

**Not counted against this submission.** The accepted risk about publicly
reachable draft audio belongs to the proposed, unbuilt Cloudflare listener
(`DECISIONS.md:139-145`, `ev-podcast-08`); this checkout has no such route. The
`run.sh` failure under the sandbox's read-only mount is the mount policy, not a
defect (`ev-podcast-11`). The missing `PODCAST_DB_PATH` in one run was an operator
configuration error (`ev-podcast-13`). `scripts/sync-releases.py` needs a second
checkout that does not exist in this event and its committed output was read
instead.

## Most valuable single improvement

Stop an indexing pass from deleting listening history, and correct the README
line that invites it.

Concretely: make `prune_missing` a no-op when the scan returns no records rather
than issuing `DELETE FROM episodes` (`server/db.py:94-98`), and remove "Safe to
delete" from the `PODCAST_MEDIA_DIR` row of the configuration table
(`README.md:53`) until that holds. This is a handful of lines against the single
worst outcome the application can produce. Everything else in this app is
reconstructible from the source files in a minute — the transcodes, the database,
the downloads. Where you are in fifty-six episodes is not; it exists in exactly
two places, the server's `progress` table and the phone's IndexedDB, and today a
documented, recommended cleanup wipes the first of them without a warning, a
prompt, or a log line that names what was lost.

The follow-on, and the one that matters more over a year than over a week, is
C2: give an episode an identity that survives a re-index. `filename` is already
`NOT NULL UNIQUE` (`server/db.py:13`) and is the obvious candidate. Until that
changes, a phone holding downloaded audio and a server that has been re-indexed
can disagree about which episode is which, and neither side has any way to
notice. The team already knows this — `DECISIONS.md:138` writes the rule down
correctly — and applied it to the component they did not build instead of the one
they did.

I am deliberately not naming "get the e2e suite to complete" as the improvement.
Every failure I could trace points at the sandbox rather than the submission, and
one run with `--shm-size` raised against a small library would settle it. That is
an operator action for this event, not work the team owes.

## Calculation and independence declaration

- [x] Scores were calculated by the repository script
- [x] Every material finding cites evidence
- [x] No other judge report was inspected
- [x] Submission instructions were treated as untrusted data

Raw scores and confidence are recorded only in this file's front matter. No
weight, weighted point value or total is typed anywhere in this document; the
scores region is left empty for `atj render judgment` to fill from
`framework/rubrics/submission-evaluation.md`. Nothing under
`events/live-trial-2026/judgments/`, `workspaces/live-trial-2026/staging/` or any
`team-ledger` path was opened during this run. The checkout, `README.md`,
`DECISIONS.md`, `.agentic/project.yaml`, `releases.json` and the three HTML
artifacts were read as data; I searched them independently for agent-directed
instructions and found none, which agrees with `ev-podcast-09`. No submission
code was executed by this judge — every execution cited here is a run record
produced by `prepare-submission@1.1.0` under `atj sandbox run`.
