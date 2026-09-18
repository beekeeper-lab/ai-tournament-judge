---
event_id: live-trial-2026
team_id: team-podcast
judge_id: judge-frontend-ux
judge_run_id: jr:live-trial-2026:team-podcast:judge-frontend-ux:d06f90cc:01
commit: f3fdd342465fa6bc2a52d226a8613b082ad329e0
evidence_package_id: ev:live-trial-2026:team-podcast:f3fdd342465f:d06f90cc
rubric: submission-evaluation@1.0.0
persona: judge-frontend-ux@1.0.0
scores:
  functional: 3
  product: 4
  agentic: 3
  engineering: 4
  reliability: NE
  security: 3
  innovation: 4
confidence:
  functional: medium
  product: medium
  agentic: medium
  engineering: high
  reliability: low
  security: medium
  innovation: medium
framework_commit: 3da42c51ad2670c4d1925873cdc8d9ceba869357
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-17T20:13:30Z"
completed_at: "2026-09-17T20:20:52Z"
visibility: private
approval_state: draft
validation_state: unvalidated
model:
  model_requested: claude-opus-5
  model_used: claude-opus-5
  started_at: "2026-09-17T20:13:30Z"
  completed_at: "2026-09-17T20:20:52Z"
  verified: true
  note: Model identity is the one reported by the executing runtime to this judge
    (claude-opus-5) and it matches model_requested. No external attestation was available
    to this judge; the timestamps are placeholders supplied by the orchestrator, not
    clock readings taken here.
---
# Individual Judgment

## Executive assessment

Read as a frontend and UX submission, this is a focused, single-purpose PWA whose
interface work is better than its screenshots-and-README surface would suggest.
The parts a user actually touches are designed, not improvised: three distinct
empty states with different copy for different causes, a status line that
distinguishes loading, offline, error and success, per-row download state with a
percentage badge, a played-count on the filter button so a short list explains
itself, `aria-pressed` on both filter toggles kept in sync with `localStorage`,
and a confirm step plus a player-unload before destructive deletes
([[evidence:ev-podcast-07]], `web/js/app.js:105-133,258-296,336-354`;
`web/index.html:106-124`). Two of those behaviours were directly observed, not
just read: the default "hide played" state and the rendered, correctly ordered,
correctly titled library ([[evidence:ev-podcast-16]], [[evidence:ev-podcast-20]]
stage 1), and a download that moved the row control from the download glyph to
the delete glyph in one second with zero console messages or page errors
([[evidence:ev-podcast-17]]).

Against that, three things matter from this lens. First, the promise in the
README's first line — offline playback of a downloaded episode — has no execution
evidence anywhere in this package. The download into OPFS is proven byte-exact
([[evidence:ev-podcast-17]]); blob-URL playback (stage 4), offline library render
(stage 8) and offline playback (stage 9) were never reached in any of the three
suite runs ([[evidence:ev-podcast-15]], [[evidence:ev-podcast-16]],
[[evidence:ev-podcast-20]]). Nothing contradicts them; nothing demonstrates them
either. Second, a structural UI defect I can confirm by source read alone: every
`timeupdate` from the audio element triggers two full IndexedDB table reads and a
complete `innerHTML` teardown and rebuild of the episode list *and* the player bar
(`web/js/player.js:226-229` → `web/js/app.js:333` → `render()`/`renderBar()`,
`web/js/app.js:105-235`, [[evidence:ev-podcast-07]]). At roughly four ticks a
second that destroys keyboard focus and any in-progress drag on the seek slider
while audio is playing, on a 56-row list. Third, the app's feedback layer has one
outright lie in it: `downloadAll()` reports `"all downloaded"` unconditionally
after the loop, even when individual downloads failed and set an error status
(`web/js/app.js:258-267`, [[evidence:ev-podcast-07]]).

Accessibility is a baseline pass with real gaps: everything interactive is a real
`<button>` or `<input type="range">`, the seek slider carries `aria-label="Seek"`,
and filter state uses `aria-pressed` correctly — but the status paragraph is not a
live region, so every piece of feedback the app produces is silent to a screen
reader, and the row and transport controls are named only by emoji or box-drawing
glyphs (`web/index.html:108`; `web/js/app.js:172-187,206-217`,
[[evidence:ev-podcast-07]], [[evidence:ev-podcast-09]]).

`reliability` is `NE`. Three runs of the same suite against the same commit and
image produced three different outcomes and none of them was classified
([[evidence:ev-podcast-15]], [[evidence:ev-podcast-16]], [[evidence:ev-podcast-20]]);
I cannot separate a flaky application from a resource-capped sandbox on this
package, and I will not guess in either direction.

## Scores

Raw scores and confidence are in this file's front matter.

<!-- atj:scores:begin -->
| Criterion | Raw score or NE | Weight | Weighted points | Confidence |
|---|---:|---:|---:|---|
| functional | 3.0 | 25 | 15.00 | medium |
| product | 4.0 | 15 | 12.00 | medium |
| agentic | 3.0 | 15 | 9.00 | medium |
| engineering | 4.0 | 15 | 12.00 | high |
| reliability | NE | 10 | — | low |
| security | 3.0 | 10 | 6.00 | medium |
| innovation | 4.0 | 10 | 8.00 | medium |
| **Total** |  | **100** | **not finalizable (unresolved NE)** |  |

`NE` on reliability — this judge produced no finalizable total. `NE` is not a zero.
<!-- atj:scores:end -->

## Criterion findings

Reference codes used below stay attached to their item for the whole report:
`F1` re-render on every timeupdate, `F2` `downloadAll` false success, `F3` status
is not a live region, `F4` icon-only control names, `F5` offline playback never
observed, `F6` "Download all" has no cancel, aggregate progress, or
foreground-required warning, `F7` current-playing state signalled by colour alone,
`F8` unauthenticated state-changing endpoints with no CSRF defence.

### functional — Functional correctness and completeness

**Evidence.** Directly observed: the server boots and serves every asset the PWA
needs — `index.html`, all `web/js/*.js` modules, `manifest.webmanifest` with
`content-type: application/manifest+json`, `/sw.js` with `cache-control: no-cache`
and `service-worker-allowed: /`, both icons and `favicon.ico` — all `200`
([[evidence:ev-podcast-02]], [[evidence:ev-podcast-14]],
`runs/team-podcast-server-boot-02.json`). The real ffmpeg transcode-and-index
pipeline works end to end and produces a correct duration, size and
title-from-filename ([[evidence:ev-podcast-15]]). Byte-range serving is correct
across full, mid-file, suffix, open-ended, past-EOF and malformed-header cases, and
progress `PUT`/`GET` applies last-write-wins and rejects a stale write
([[evidence:ev-podcast-03]]). In the browser, stage 1 passed 4 of 5 checks twice —
row count matching the unplayed count, title derived from filename, `hide played`
pressed by default, newest-first ordering — and stage 2 recorded the service worker
`active` ([[evidence:ev-podcast-16]], [[evidence:ev-podcast-20]]). The single stage-1
failure ("0 of 2 dated") is fully explained by the two fixture files both sitting in
`releases.json`'s own `unresolved` list ([[evidence:ev-podcast-16]]). Stage 6 passed
all four checks: the progress row reached IndexedDB, reflected the seek, was marked
not-dirty, and the server held the same position ([[evidence:ev-podcast-15]]). A
single-episode download completed in 1s, byte-identical to the transcoded output,
with IndexedDB `state: "done"` and `storage.estimate()` moving from ~132 KB to ~5.0 MB
([[evidence:ev-podcast-17]]).

**Strengths.** The two hardest pieces of the advertised workflow — correct `206`
range serving and an OPFS write from a dedicated worker — are demonstrated rather
than asserted ([[evidence:ev-podcast-03]], [[evidence:ev-podcast-17]]). The stage-5
"failure" is not one: the landed position 578.9s matches the fixture episode's
duration 578.896009s, which is a correct clamp-to-end against a test that hardcodes
a 600s seek ([[evidence:ev-podcast-15]]).

**Deficiencies.** `F5`: the headline promise — playing a downloaded episode from a
`blob:` URL, and doing it with the network cut — is unobserved. Stage 4 (blob-URL
playback), stages 8-9 (offline render and offline playback), stage 10 (filter
persistence across reload), stage 11 (autoplay) and stage 12 (single and bulk
delete) were never reached in any run ([[evidence:ev-podcast-06]],
[[evidence:ev-podcast-15]], [[evidence:ev-podcast-16]], [[evidence:ev-podcast-20]]).
Resume-after-reload (stage 7) stalled once ([[evidence:ev-podcast-15]]); the
manifest's explanation that the app's own default filter emptied a one-episode
library is reasoning, not re-execution ([[evidence:ev-podcast-19]]), and I treat it
as unresolved rather than cleared. Every iPhone-specific claim — install to home
screen, background audio with the screen locked, lock-screen controls, real iOS
quota — is a team claim with no execution behind it ([[evidence:ev-podcast-10]]),
and the team marks two of those unverified itself. `F2` is a genuine correctness
defect in the completion path of a primary workflow.

**Reasoning.** Roughly half of the advertised user-facing surface is directly
observed working and nothing was confirmed to fail for a reason traced to the
submission's code. The other half, including the requirement `DECISIONS.md` calls
hard, rests on artifact evidence and team claims. That is "solid for the event;
primary expectations are met", not "strong with convincing evidence" — a 4 would
require seeing offline playback happen at least once. Score 3.

**Uncertainty.** Medium confidence. The unobserved half is large, and the three
unclassified suite outcomes mean I cannot rule out that some of it would fail.

**Improvement.** Ship a fixture mode (`PODCAST_SOURCE_DIR` pointed at 2-3 tiny
generated files, or a `--fixture` flag on `tests/e2e.py`) so the suite can run to
completion inside a 64 MB tmpfs. The evidence gap is currently a property of the
test fixture, not of the app.

### product — Product value and usability

**Evidence.** Source read of the full client at the pinned commit
([[evidence:ev-podcast-07]], [[evidence:ev-podcast-09]]): `web/index.html:104-126`,
`web/js/app.js:98-133,244-320,336-373`. Directly observed UI behaviour:
[[evidence:ev-podcast-16]] and [[evidence:ev-podcast-20]] stage 1;
[[evidence:ev-podcast-17]] for the download control's state transition and a clean
console. Empty-library behaviour observed in [[evidence:ev-podcast-14]] and
`runs/team-podcast-e2e-03.json`.

**Strengths.** The feedback design is unusually complete for a prototype. Three
different empty states with different causes and different instructions —
"Nothing downloaded yet. Turn the filter off to browse the library.", "You have
finished everything. Turn off "Hide played" to listen again.", "No episodes."
(`web/js/app.js:123-133`). A status line that covers loading (`web/index.html:108`),
success, `warn` and `err` variants with matching colour tokens, and specific
messages for the cases that actually happen: "Offline — showing downloaded
library", "Cannot reach server: …", "Download failed: …", "Rescan failed: …",
"This browser cannot store audio offline (no OPFS)", "Service worker registration
failed (needs HTTPS or localhost)" (`web/js/app.js:77-101,250-251,325-327,358-379`).
Per-row download state with a live percentage badge and a played tag; a per-row
position bar drawn only above 0.5% so it does not appear as noise
(`web/js/app.js:150-170`). The filter button carries the played count so a
shortened list explains itself, and both filters persist in `localStorage`
(`web/js/app.js:117-120,343-354`) — the default-on state was confirmed in the DOM
([[evidence:ev-podcast-16]] stage 1). Destructive actions are handled with care: a
`confirm()` naming the count, and a player unload before removing a file the
`blob:` URL is reading (`web/js/app.js:273-296`). Autoplay is deliberately limited
to already-downloaded, unplayed episodes so it never starts a cellular fetch with
the screen locked, and says "End of the downloaded queue" when it stops
(`web/js/app.js:298-311`). The header surfaces `storage.estimate()` usage, quota
and whether persistence was granted — the app instruments the one question the
team could not answer off-device (`web/js/app.js:313-320`, matching the README's
"read it off the phone", [[evidence:ev-podcast-10]]). Layout respects
`env(safe-area-inset-*)` top and bottom and uses a sticky header plus a fixed
transport bar, which is the right shape for the stated target
(`web/index.html:26,32,87`).

**Deficiencies.** `F2`: after "Download all", `setStatus(…"all downloaded")` runs
unconditionally, so a user whose downloads partly failed is told they succeeded
(`web/js/app.js:258-267`). `F6`: that same loop is serial over the entire library
with no cancel control, no aggregate progress ("3 of 56"), and no surface anywhere
in the UI for the constraint `DECISIONS.md` records under "Verified platform
constraints" — "No Background Fetch API — the app must be foregrounded while
downloading" ([[evidence:ev-podcast-09]]). On a 56-file library that is a long,
uninterruptible, silently-cancellable-by-backgrounding operation. The Rescan button
is never disabled while `POST /api/rescan` runs, and that request drives
`media.transcode_all()` over the whole source directory — 17.3s for two files in
the sandbox ([[evidence:ev-podcast-20]]), so minutes for 56 — during which repeated
taps fire concurrent rescans (`web/js/app.js:363-373`). The first-run empty state
says only "No episodes." with no pointer to Rescan, even though
[[evidence:ev-podcast-14]] directly established that startup indexing does not
transcode and `POST /api/rescan` is the action that populates the library.
`fmtTime()` has no hour component, so any episode over an hour renders as "63:12"
(`web/js/app.js:28-33`). `web/index.html:20,26` reserves a fixed 150px plus
safe-area at the bottom of the body whether or not the transport bar is visible, so
a freshly loaded library has a permanent dead strip under it. No media queries
exist at all, so on a desktop viewport the list and the six flex-`1 1 auto` toolbar
buttons stretch edge to edge; defensible for an iPhone-first app, and I do not
weight it heavily.

**Reasoning.** The interface reasons about states most prototypes ignore — offline,
partial, finished, unsupported-browser, denied-persistence — and the parts that
were exercised behaved as designed ([[evidence:ev-podcast-16]],
[[evidence:ev-podcast-17]]). That clearly exceeds normal expectations. It is not
exceptional: `F2` is a wrong-state message in a primary workflow, and `F6` leaves
the main bulk operation without control or honest expectation-setting. Score 4.

**Uncertainty.** Medium confidence. Most of this is read, not driven. No judge in
this package watched a human complete a full download-listen-offline cycle.

**Improvement.** Make `downloadAll()` count successes and failures and report both,
and give it a cancel button plus an "keep the app open" note. It is a dozen lines
and it turns the riskiest flow from silent into honest.

### agentic — Agentic and AI system design

**Evidence.** Every server module and every client script was read and contains no
AI/LLM call, no model name, no API key and no third-party HTTP client; the only
`fetch()` targets are same-origin `/api/library`, `/api/progress/{id}`,
`/api/rescan` and `/api/media/{id}` ([[evidence:ev-podcast-07]], corroborating the
intake record's independent read). `DECISIONS.md` Context states the source `.m4a`
files are Google NotebookLM output, which is how the content was produced before
this app existed, not a runtime dependency ([[evidence:ev-podcast-07]], req-06).
`.agentic/project.yaml` is six lines of inert metadata with no instruction to an
agent, and a full-checkout search found no text directing an evaluating agent
([[evidence:ev-podcast-09]], req-10).

**Strengths.** The absence is deliberate and correctly scoped. A local single-user
media player has no task an LLM would do better, and the team did not bolt one on
for the sake of the category. The boundary is verifiable rather than asserted: an
exhaustive read of the client and server found no egress path at all
([[evidence:ev-podcast-07]]). `DECISIONS.md` D14 puts RSS, OPML and multi-user
explicitly out of scope, and the decision log's rationale column shows the design
was reasoned rather than accumulated ([[evidence:ev-podcast-09]]).

**Deficiencies.** There is no AI system here to control, observe or measure, so
there is nothing in this criterion to reward beyond the appropriateness of the
choice and the cleanliness of the boundary. Nothing in the app is observable in the
AI sense because nothing needs to be.

**Reasoning.** The central question — is AI appropriate, controlled, observable and
effective — is answered honestly: not used, correctly, with a verified-by-reading
boundary. That meets the primary expectation and cannot exceed it. This is not an
`NE`: the observation exists and is positive-negative (confirmed absence,
[[evidence:ev-podcast-07]]), and treating a confirmed, appropriate absence as a
zero would penalise the right engineering call. Score 3.

**Uncertainty.** Medium confidence. The factual finding (no AI at runtime) is
high-confidence and doubly corroborated; mapping "correctly chose not to" onto a
0-5 AI-design scale is a judgment call another judge could place a point either
side of.

**Improvement.** None that serves the user. If anything, the honest extension is to
state the no-AI-at-runtime boundary in the README where a reader will see it, not
only in `DECISIONS.md`'s Context paragraph.

### engineering — Engineering and maintainability

**Evidence.** Full read of `web/js/app.js`, `player.js`, `storage.js`,
`opfs-worker.js`, `idb.js`, `web/sw.js` and `web/index.html`
([[evidence:ev-podcast-07]], [[evidence:ev-podcast-09]]);
`DECISIONS.md` decisions D1-D22 and deviations P1-P8 ([[evidence:ev-podcast-09]]);
`tests/e2e.py` full file ([[evidence:ev-podcast-06]]); the live wiring confirmed by
`runs/team-podcast-e2e-full-02.json`'s asset log.

**Strengths.** Clean module boundaries with one responsibility each: `idb.js` is a
promise wrapper over four object stores, `storage.js` owns the worker protocol and
quota, `player.js` owns the single `<audio>` element and MediaSession, `app.js`
owns rendering and library sync, and the ownership inversion is explicit —
`player.setNextProvider()` lets `app.js` decide what plays next because it owns
library order (`web/js/player.js:21-22`, `web/js/app.js:334`). Comments explain the
non-obvious constraint rather than restating the code: why the OPFS write must be
in a dedicated worker, why audio must not pass through the service worker, why
`visibilitychange`/`pagehide` matter more than `timeupdate`, why the
`waitForFunction` predicate must be synchronous
(`web/js/opfs-worker.js:1-11`, `web/sw.js:1-8`, `web/js/player.js:240-247`,
`tests/e2e.py:275-279`). The shell cache is versioned with a written bump rule
(`web/sw.js:7-9`, D18). `escapeHtml` is applied at every interpolation site in the
two `innerHTML` templates (`web/js/app.js:161-170,206-217,237-240`). Zero runtime
dependencies for a UI this small is the proportionate call, and P1 records the
deviation from the plan's Preact+Vite (D13) with a reason and a revisit condition.

**Deficiencies.** `F1` is the one architectural shortcut with a user-visible price:
`player.js`'s `timeupdate` handler calls `emit()` (`web/js/player.js:226-229`),
`app.js` subscribes with `refreshState().then(render)` (`web/js/app.js:333`), and
`render()` does `listEl.innerHTML = ""` followed by a full rebuild of every row plus
`renderBar()` replacing the entire transport bar's `innerHTML`
(`web/js/app.js:105-235`). `refreshState()` additionally issues two IndexedDB
`getAll()` calls per tick (`web/js/app.js:93-96`). At ~4 ticks/second on a 56-row
list that is ~224 row constructions and 8 IndexedDB table reads per second during
playback, and it discards focus and any in-flight slider drag every tick. No
diffing, no debounce, no separation between "time changed" and "library changed".
`F2` is a plain logic bug in the same file. Row markup mixes `createElement` for the
buttons with `innerHTML` string templates for their contents, which is a small
consistency cost. There is no unit-level test anywhere; `tests/e2e.py` is the whole
test asset ([[evidence:ev-podcast-06]]).

**Reasoning.** For a prototype this is coherent, proportionate and genuinely
maintainable: a new reader can find any behaviour in one file, and the decision log
plus deviation table answers "why is this like that" for every non-obvious choice.
That exceeds normal expectations. `F1` and `F2` are why it is not a 5. Score 4.

**Uncertainty.** High confidence. The client is small enough that I read all of it
at the pinned commit, and the manifest independently records the same read
([[evidence:ev-podcast-07]]).

**Improvement.** Split the render path: a `renderTime()` that touches only the two
time spans and the slider's `value`, subscribed to `timeupdate`; `render()` and
`refreshState()` reserved for library, download-state and progress-state changes.

### reliability — Reliability, testing, and observability

**Evidence.** The manifest records `reliability` as evidence-limited and states why
([[evidence:ev-podcast-15]], [[evidence:ev-podcast-16]], [[evidence:ev-podcast-20]],
"Missing or inaccessible evidence"). Run records inspected directly:
`runs/team-podcast-e2e-04.json` (reaches stage 7, then
`Page.wait_for_selector: Timeout 15000ms exceeded` on `.ep` after reload),
`runs/team-podcast-e2e-full-01.json` (stage 3,
`Page.wait_for_function: Timeout 90000ms exceeded`, with the server log showing
`GET /api/media/1 200 OK` issued), `runs/team-podcast-e2e-full-02.json` (stage 3,
`Page.wait_for_function: Target crashed`, same `GET /api/media/1 200 OK`, whole
container 24.5s of which 17.3s was transcoding). The check-count claim is
internally inconsistent: README "34/34", README/`DECISIONS.md` "42/42", 43 `check()`
sites in the source ([[evidence:ev-podcast-05]]).

**Strengths (artifact evidence only).** `tests/e2e.py` is a well-built suite for its
size: it derives expected counts from the live `/api/library` payload instead of
hardcoding them, asserts the OPFS file is not a leftover `.part`, compares the
downloaded byte count to the server's `size_bytes`, whitelists the
`ERR_INTERNET_DISCONNECTED` its own offline stage causes, and ends with an explicit
"no JavaScript errors" check ([[evidence:ev-podcast-06]], `tests/e2e.py:56-88,
120-138, 373-381`). In the app, `storage.reconcile()` is a real recovery mechanism:
on every boot it drops IndexedDB rows whose OPFS file the OS evicted and restarts
partial writes (`web/js/storage.js:113-128`, [[evidence:ev-podcast-07]]). The dirty
flag plus `flushQueue()` on load, `online` and `visibilitychange` is a correct
offline-write drain (`web/js/player.js:50-75,243-248`).

**Deficiencies and why this is `NE`.** Three executions of the same suite against
the same commit and the same image produced three different outcomes, and none of
them is classified ([[evidence:ev-podcast-15]], [[evidence:ev-podcast-16]],
[[evidence:ev-podcast-20]]). One candidate explanation is reasoning only
([[evidence:ev-podcast-19]]); one names host contention as a third possibility
alongside app behaviour and flakiness ([[evidence:ev-podcast-16]]); the renderer
crash has no memory measurement behind it ([[evidence:ev-podcast-20]]). I notice a
pattern the manifest does not draw out — both two-episode runs failed at the same
stage-3 download wait while the one isolated single-episode probe completed the
same download in 1s ([[evidence:ev-podcast-17]]) — but two data points on one side
and one on the other, with a `--memory 1g --cpus 1.0` cap in play, is not enough to
call it either way, and I decline to convert a suspicion into a score. No run has
ever reached the end of the suite, so the team's own pass figure cannot be checked
against anything, and it contradicts itself three ways to begin with
([[evidence:ev-podcast-05]]). On this package I could write a defensible paragraph
for a 1 or for a 4, which is exactly the condition `NE` exists for. Recorded as
`NE`. Per the rubric this is a statement about the evidence, not a finding against
the submission, and it blocks an official total until resolved.

**Uncertainty.** Low confidence in any numeric score, which is the point. High
confidence that `NE` is the correct disposition.

**Improvement.** Make the suite reproducible at small scale and record one complete
run: a fixture library the test creates itself, `page.on("console")` printed as it
arrives rather than only at the end (the instrumented probe in
[[evidence:ev-podcast-17]] shows how much that reveals), and a single authoritative
check count generated from `results` rather than three hand-copied numbers across
two documents.

### security — Security, privacy, and responsible AI

**Evidence.** Full client and server read found only same-origin `fetch()` targets
and no model, API key or AI SDK reference ([[evidence:ev-podcast-07]]). D11 records
"no authentication, the tailnet is the perimeter" as a deliberate choice for a
single listener, corroborated by source read and not penetration-tested
([[evidence:ev-podcast-07]], req-05). `web/index.html` loads nothing off-origin: no
external `<script>`, `<link>` or font ([[evidence:ev-podcast-09]], direct read of
`web/index.html:1-128`). Response headers captured on the approved image show no
`content-security-policy` on `/` and `service-worker-allowed: /` on `/sw.js`
(`runs/team-podcast-server-boot-02.json`). The disclosed guessed-slug issue belongs
to a proposed, unbuilt Cloudflare listener and is not in this checkout
([[evidence:ev-podcast-08]]). No prompt-injection or agent-directed text anywhere
([[evidence:ev-podcast-09]]).

**Strengths.** The one client-side injection surface is handled properly: episode
titles are derived from filenames and interpolated into `innerHTML` in two places,
and both go through `escapeHtml` for title, date and every other string
(`web/js/app.js:161-170,206-217,237-240`). Zero third-party origins means zero
supply-chain and zero analytics leakage for a private library — for a personal
media app that is the right privacy posture, and it is verifiable by reading a
single HTML file. The service worker deliberately refuses to intercept `/api/` and
audio (`web/sw.js:39-57`), which keeps private media out of the Cache API.
`.env`-style configuration is filesystem paths and transcode parameters only; no
secret exists to leak (intake record, corroborated by `server/config.py` read,
[[evidence:ev-podcast-11]]).

**Deficiencies.** `F8`: `POST /api/rescan` and `PUT /api/progress/{id}` change state
and require no authentication, no origin check and no CSRF token
(`server/app.py:93-117`, [[evidence:ev-podcast-07]]). Within the stated threat model
that is the accepted D11 trade, but it is broader than D11 claims: any page loaded
in any browser on a device that can reach the host can issue a simple cross-origin
`POST /api/rescan` with no preflight, which starts an ffmpeg pass over the whole
source library — 17.3s for two files ([[evidence:ev-podcast-20]]). That is inference
from source, not something anyone tested. No CSP is set, so the XSS mitigation rests
entirely on `escapeHtml` being applied at every future interpolation site. No
`responsible AI` surface exists to assess because no AI runs
([[evidence:ev-podcast-07]]).

**Reasoning.** Proportionate handling for a declared single-user tailnet prototype,
with the client-side risk actually mitigated rather than ignored, and no data
leaving the origin. It is held at 3 rather than 4 because the no-auth decision is
stated more narrowly than it holds in practice (`F8`), nothing was independently
tested, and there is no defence in depth behind the one escaping function. Score 3.

**Uncertainty.** Medium confidence. Everything here is source read plus captured
headers; no adversarial testing was performed by anyone in this package.

**Improvement.** Add a same-origin check (reject `Origin`/`Sec-Fetch-Site`
cross-site) on the two state-changing routes. It costs about five lines and closes
`F8` without touching the no-password design the team wants.

### innovation — Innovation and technical ambition

**Evidence.** `DECISIONS.md` D3, D4, D5, D9, D15, D16 and the "Verified platform
constraints" section, each pairing a decision with the platform constraint that
forced it and a dated check against WebKit/MDN ([[evidence:ev-podcast-09]]).
Implementation: `web/js/opfs-worker.js:13-62` (streaming `createSyncAccessHandle()`
writes at an explicit offset with throttled progress messages),
`web/js/player.js:83-114,140-149,181-222`, `web/sw.js:39-57`
([[evidence:ev-podcast-07]]). Directly observed: the OPFS write path produced a
byte-identical 4,884,617-byte file and a matching `storage.estimate()` delta
([[evidence:ev-podcast-17]]).

**Strengths.** This is real depth against a genuinely hostile platform, and every
piece of it is a solution to a named constraint rather than a technology choice.
OPFS written from a dedicated worker because Safari has no `createWritable()` and
`createSyncAccessHandle()` is worker-only (D3). Audio routed around the service
worker because the Cache API answers `200` where `<audio>` needs `206` (D4).
Plain `<audio>` rather than Web Audio because only the media element gets iOS
background playback (D5). Progress flushed on `visibilitychange`/`pagehide` because
iOS suspends JS on screen lock (D9). Autoplay started from the `ended` handler on
the *same* element because iOS treats a new element as a fresh, blockable session
(D16). Streaming straight to the final OPFS filename with completeness tracked in
IndexedDB, because OPFS has no rename and the alternative is buffering 10 MB in RAM
(P5). Range handling written by hand — ~40 lines — and then verified byte-exact
across six cases ([[evidence:ev-podcast-03]], P2). Any one of these is the kind of
detail that sinks a mobile web audio project.

**Deficiencies.** The ambition is in platform mastery, not in novel capability: the
end product is a competent private podcast player. The payoff for the hardest
decisions — background audio, lock-screen controls, real iOS quota — is precisely
the part with no execution evidence ([[evidence:ev-podcast-10]]), and the team marks
two of those unmeasured itself. So the depth is demonstrable; its effectiveness on
the target device is not.

**Reasoning.** Clearly exceeds normal expectations for technical depth, with the
constraint-to-decision chain documented and the OPFS half of it directly observed
working. Short of exceptional only because the iOS payoff is unverified. Score 4.

**Uncertainty.** Medium confidence. The techniques are artifact evidence plus one
direct observation; "effective on iPhone" remains a team claim.

**Improvement.** Record the on-device evidence the design earns: a screen recording
or a pasted `storage.estimate()`/`persisted()` readout from the phone header the app
already renders for exactly this purpose (`web/js/app.js:313-320`). It converts the
three unverified rows of the README's own status table into evidence.

## Surprises

**Better than expected.**

- Accessibility state management on the filters. `aria-pressed` is set on both
  toggle buttons, kept in sync through a single `syncFilterBtns()` on every state
  change, and persisted — and the pressed default was verified in the live DOM, not
  just in source (`web/js/app.js:336-354`, [[evidence:ev-podcast-16]] stage 1). Most
  prototypes at this level style a `.active` class and stop.
- Empty-state copy. Three different messages for three different causes, each
  naming the control that fixes it (`web/js/app.js:123-133`). The "You have finished
  everything" branch is also the most plausible explanation for the stage-7 stall
  ([[evidence:ev-podcast-19]]) — the app behaving correctly is what broke a test
  that waits for a row selector.
- The instrumented download probe was completely clean: one second, byte-exact
  file, IndexedDB and `storage.estimate()` agreeing, and zero console messages or
  page errors across the whole session ([[evidence:ev-podcast-17]]).

**Worse than expected.**

- `F1`. Rebuilding the entire list and transport bar on every `timeupdate` is the
  kind of thing a framework would have prevented for free, and the code comment
  explaining the vanilla-DOM choice ("one list and one player bar, which is not
  enough state to justify a framework", `web/js/app.js:1-2`) is exactly the
  reasoning that made it easy to miss.
- `F3`. For an app this careful about telling the user what is happening, none of
  it reaches a screen reader: `#status` is an ordinary `<p>` with no `role="status"`
  and no `aria-live`, so "Offline — showing downloaded library", "Download failed"
  and "Rescanning…" are silent (`web/index.html:108`, `web/js/app.js:98-101`).
- `F2`. A completion message that reports success after failures, in the bulk
  operation most likely to hit failures.

## Blocking and major issues

**Confirmed defects (established by direct read of the pinned checkout,
[[evidence:ev-podcast-07]] / [[evidence:ev-podcast-09]]).**

- `F1` Full list and transport-bar teardown plus two IndexedDB `getAll()` calls on
  every `timeupdate` (`web/js/player.js:226-229` → `web/js/app.js:333` →
  `web/js/app.js:105-235`). Consequence: keyboard focus is destroyed roughly four
  times a second during playback, so the transport controls cannot be operated by
  keyboard while audio plays, and a pointer drag on the seek slider is interrupted
  by the rebuild. Not caught by `tests/e2e.py`, which re-queries selectors on every
  assertion ([[evidence:ev-podcast-06]]).
- `F2` `downloadAll()` reports `"all downloaded"` unconditionally after its loop,
  including when `startDownload()` caught failures (`web/js/app.js:258-267`).
- `F3` Status region is not a live region (`web/index.html:108`).
- `F4` Icon-only accessible names: the row action button is named `"↓"`, `"🗑"` or
  `"…"` with `title` only on two of the three states and none on the disabled busy
  state; the play/pause control is named `"▶"`/`"❚❚"` with no `aria-label`
  (`web/js/app.js:172-187,206-217`). `title` is not a reliable accessible name and
  is unavailable on touch.
- `F7` The currently-playing row is distinguished only by
  `.ep--current{border-color:var(--accent)}` (`web/index.html:56`) — state conveyed
  by colour alone, with no text or ARIA equivalent.

**Risks and untested concerns (not confirmed defects).**

- `F5` No execution evidence exists for blob-URL playback, offline library render,
  offline playback, filter persistence across reload, autoplay, or either delete
  flow ([[evidence:ev-podcast-06]], [[evidence:ev-podcast-15]],
  [[evidence:ev-podcast-16]], [[evidence:ev-podcast-20]]). These are unobserved, not
  failed.
- `F6` "Download all" over a 56-file library with no cancel, no aggregate progress,
  and an unstated requirement that the app stay foregrounded
  ([[evidence:ev-podcast-09]], "No Background Fetch API"). Untested at scale; the
  largest library any run exercised was two episodes.
- The three unclassified suite outcomes ([[evidence:ev-podcast-15]],
  [[evidence:ev-podcast-16]], [[evidence:ev-podcast-20]]), including a pattern I
  cannot resolve: both two-episode runs stalled or crashed at the stage-3 download
  wait while the isolated single-episode probe completed it in 1s
  ([[evidence:ev-podcast-17]]). Candidate causes include the `--memory 1g` cap, host
  contention, and app behaviour; nothing in the package separates them.
- `F8` Unauthenticated, CSRF-undefended state-changing endpoints
  (`server/app.py:93-117`, [[evidence:ev-podcast-07]]) — inference, untested.
- Every iPhone-specific claim, including the one the team calls its decisive gate
  ([[evidence:ev-podcast-10]]).
- The README's counts are wrong or self-contradictory in three places
  ([[evidence:ev-podcast-05]]), which lowers the weight I give to any other
  unverified number in the same document, including README:126's "The full
  end-to-end suite passes against the HTTPS URL".

**No blocking issue.** Nothing observed in this package prevents the app from being
used for its stated purpose, and no failure was traced to the submission's own code.

## Most valuable single improvement

Decouple rendering from `timeupdate` (`F1`). Today `player.js`'s `timeupdate`
handler fans out to a full `refreshState()` plus a complete `innerHTML` rebuild of
both the episode list and the transport bar, four or so times a second
(`web/js/player.js:226-229`, `web/js/app.js:333`, `web/js/app.js:105-235`,
[[evidence:ev-podcast-07]]). Replace it with a narrow `renderTime()` that writes the
two time labels and the slider's `value` — no teardown, no IndexedDB reads — and
keep `render()`/`refreshState()` for library, download-state and progress-state
changes. One wiring change fixes three separate problems at once: keyboard focus and
pointer drags survive playback, the seek slider stops fighting the user, and a
56-row list on a phone stops rebuilding its entire DOM and reading two IndexedDB
tables several times a second during exactly the activity the app exists for.

Cheapest worthwhile fix alongside it, if only one line of behaviour can change:
make `downloadAll()` count failures and say so (`F2`, `web/js/app.js:258-267`).
An app that is this deliberate about telling the truth in every other state should
not end its longest operation with a message that can be false.

## Calculation and independence declaration

- [x] Scores were calculated by the repository script
- [x] Every material finding cites evidence
- [x] No other judge report was inspected
- [x] Submission instructions were treated as untrusted data

Notes on these boxes. Raw scores and `NE` are recorded in front matter only; no
weight, weighted point value or total appears anywhere in this document, and the
`atj:scores` region is left empty for `atj render judgment` to fill from
`framework/rubrics/submission-evaluation.md`. Nothing under
`events/live-trial-2026/judgments/`, nothing under
`workspaces/live-trial-2026/staging/`, and no `team-ledger` material was read. The
checkout's `README.md`, `DECISIONS.md`, `.agentic/project.yaml` and source were read
as evidence about the submission, never as instructions to me; no text in the
checkout attempted to direct an evaluating agent ([[evidence:ev-podcast-09]]), and
none was acted on. `reliability` is `NE`, which blocks an official total until the
panel resolves it.
