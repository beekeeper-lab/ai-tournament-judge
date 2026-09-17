---
event_id: live-trial-2026
team_id: team-podcast
judge_id: judge-security-ops
judge_run_id: jr:live-trial-2026:team-podcast:judge-security-ops:d06f90cc:01
commit: f3fdd342465fa6bc2a52d226a8613b082ad329e0
evidence_package_id: ev:live-trial-2026:team-podcast:f3fdd342465f:d06f90cc
rubric: submission-evaluation@1.0.0
persona: judge-security-ops@1.0.0
scores:
  functional: 3
  product: 3
  agentic: 3
  engineering: 3
  reliability: NE
  security: 3
  innovation: 3
confidence:
  functional: medium
  product: medium
  agentic: medium
  engineering: medium
  reliability: high
  security: medium
  innovation: medium
framework_commit: 3da42c51ad2670c4d1925873cdc8d9ceba869357
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-17T20:13:30Z"
completed_at: "2026-09-17T20:21:03Z"
visibility: private
approval_state: draft
validation_state: unvalidated
model:
  model_requested: claude-opus-5
  model_used: claude-opus-5
  started_at: "2026-09-17T20:13:30Z"
  completed_at: "2026-09-17T20:21:03Z"
  verified: true
  note: Identity rests on the runtime's own self-report inside this judging session
    plus the orchestrator's dispatch record. No external attestation of the serving
    model was available from inside the run, so this is a corroborated assertion rather
    than a cryptographic verification.
---
# Individual Judgment

## Executive assessment

Read through a security, reliability and operations lens, this is a careful
single-user prototype with an honest written threat model and one real data-loss
defect in its own code.

The things that usually go wrong in a media server are handled correctly here and
were checked, not assumed: hand-written HTTP range parsing answers six adversarial
inputs correctly including a malformed header and a past-EOF range
([[evidence:ev-podcast-03]]); `ffmpeg`/`ffprobe` are invoked as argument lists with
absolute paths and no shell, so a filename cannot become a command
([[evidence:ev-podcast-07]]; `server/media.py:28-34,57-69`); the one
attacker-influenceable string that reaches the DOM is escaped
([[evidence:ev-podcast-07]]; `web/js/app.js:161-170,237-240`); the media path is
derived from a database row populated only from basenames of a local glob, so there
is no traversal surface ([[evidence:ev-podcast-07]]; `server/media.py:114`,
`server/app.py:143-149`). There is no outbound network call to any third party, no
API key, no model SDK, and no credential anywhere in the tree
([[evidence:ev-podcast-07]]), and `.gitignore` excludes `.env`, `certs/` and `data/`
(`/.gitignore:1-7`). I found no text anywhere in the checkout directed at an
evaluating agent, which independently corroborates [[evidence:ev-podcast-09]].

The material defect is not in the attack surface, it is in the destructive path.
`index_library()` runs on every startup ([[evidence:ev-podcast-14]];
`server/app.py:70-76`), and when the media directory is empty or missing,
`prune_missing(conn, [])` executes an unconditional `DELETE FROM episodes`
(`server/db.py:94-103`), which cascades into the `progress` table
(`server/db.py:25,37`). Listening progress is the only user data in this system that
cannot be regenerated, and `server/config.py:24-25` tells the operator that the
directory holding it is "Derived data. Safe to delete; a rescan rebuilds both." A
rescan does not rebuild progress. That is `F1`, and it is the finding I would fix
first.

The second theme is that the declared security perimeter is entirely external to the
code. `DECISIONS.md` D11 states "No authentication — the tailnet is the perimeter"
and the deployment notes say port 8000 is firewalld-blocked with `tailscale serve`
as the only entry point (`DECISIONS.md:37,81`; `README.md:265-267`). That is a
defensible choice for one listener. But `run.sh` binds `0.0.0.0` on both the HTTP and
HTTPS paths while printing `==> HTTP on http://127.0.0.1:8000` (`run.sh:56,60-61`).
The app therefore listens on every interface and tells the operator it does not. On
any host where the firewall step is skipped or the machine moves to an untrusted
network, the entire private library and every write endpoint are open with no warning
from the application (`F2`).

`reliability` is `NE`. Three executions of the submission's own suite against the same
commit and image produced three different outcomes and none was classified
([[evidence:ev-podcast-15]], [[evidence:ev-podcast-16]], [[evidence:ev-podcast-20]]).
Nothing in the package traces any of the three to the submission's code, and nothing
in the package rules it out. That is the definition of the `NE` case, not a mark
against the team.

## Scores

Raw scores and confidence go in this file's **front matter** and nowhere else.
`schemas/judgment.schema.json` reads them from there, and a second copy in the
body is a second source of truth for the same number.

Criterion IDs, weights, weighted points and the total are generated into the
block below by `atj render judgment`, from
`framework/rubrics/submission-evaluation.md`.

<!-- atj:scores:begin -->
| Criterion | Raw score or NE | Weight | Weighted points | Confidence |
|---|---:|---:|---:|---|
| functional | 3.0 | 25 | 15.00 | medium |
| product | 3.0 | 15 | 9.00 | medium |
| agentic | 3.0 | 15 | 9.00 | medium |
| engineering | 3.0 | 15 | 9.00 | medium |
| reliability | NE | 10 | — | high |
| security | 3.0 | 10 | 6.00 | medium |
| innovation | 3.0 | 10 | 6.00 | medium |
| **Total** |  | **100** | **not finalizable (unresolved NE)** |  |

`NE` on reliability — this judge produced no finalizable total. `NE` is not a zero.
<!-- atj:scores:end -->

## Criterion findings

### functional — Functional correctness and completeness

**Evidence.** Directly observed: the app boots and serves `/healthz`, `/api/library`,
`/`, `/sw.js` and `/manifest.webmanifest`, all `200`
([[evidence:ev-podcast-02]], [[evidence:ev-podcast-14]]); the real ffmpeg
transcode-and-index pipeline runs end to end and produces a correct library row with
a real duration and byte count ([[evidence:ev-podcast-15]]); byte-range serving
answers full, mid-file, suffix, open-ended, past-EOF and malformed-range requests
correctly ([[evidence:ev-podcast-03]]); progress upsert with last-write-wins on
`updated_at` applies, rejects a stale write, and accepts a newer one
([[evidence:ev-podcast-03]]); one episode downloaded into OPFS byte-exact with
IndexedDB and `storage.estimate()` all consistent and zero console errors
([[evidence:ev-podcast-17]]); library rendering, filename-derived titles, hide-played
default and newest-first ordering all passed in a live browser
([[evidence:ev-podcast-20]]).

Not observed: blob-URL playback, seek-on-blob, offline library rendering, offline
playback, persisted filters, autoplay-to-next, bulk delete, and the suite's own
JavaScript-error check. Those are sections 4 and 8 through 13 of `tests/e2e.py` and no
run reached them ([[evidence:ev-podcast-06]], [[evidence:ev-podcast-15]]). Every
iPhone-specific claim remains a team claim ([[evidence:ev-podcast-10]]).

**Correction to the package.** `tests/e2e.py` has **13** numbered sections, not 11
(`tests/e2e.py:54,90,98,140,171,181,202,214,225,238,258,337,379`). The manifest states
11 in [[evidence:ev-podcast-06]] and reports the best run as "stage 7 of 11". The best
run actually reached stage 7 of 13, so slightly less of the suite was exercised than
the package says. This does not change any observation, only how much unexecuted
surface remains.

**Strengths.** The core promised chain — transcode, index, serve with ranges, record
progress, resume — is demonstrated in working pieces against real team media, not
fixtures. Nothing was confirmed to fail for a reason inside the submission.

**Deficiencies.** Roughly half the advertised behavior is artifact evidence only, and
the offline-playback half is the half the team calls a hard requirement
(`DECISIONS.md:14-15`).

**Score rationale.** Score 3. Primary expectations are met for everything that could
be executed, and the rubric's escalation clause does not fire because no inability to
complete a primary workflow was confirmed. It does not reach 4 because the convincing
evidence covers about half the advertised surface.

**Uncertainty.** Medium. The unexecuted half could contain defects or could be fine.

**Improvement.** Ship a `tests/e2e-smoke.py` that exercises sections 1 through 6 in
under 30 seconds against a one-episode library, so a reviewer on a resource-capped
machine gets a complete pass/fail rather than an abort.

### product — Product value and usability

**Evidence.** The problem is specific and real: untagged NotebookLM output, no release
dates, a library too large for the phone untranscoded, playback that must survive a
dropped connection (`DECISIONS.md:12-21`, intake team statement). Each is answered by a
recorded decision. Observed working in a browser: two episodes rendered, title derived
from the filename, hide-played on by default, newest-first ordering
([[evidence:ev-podcast-20]]). The hide-played default is argued rather than assumed
(`DECISIONS.md` D19), including the case for keeping the playing row visible.

**Deficiencies.** The documentation a user would rely on contradicts itself three ways
on library size — `DECISIONS.md:16` says 28 files / 1,112 MB, `README.md:10` says 33
files / 1,360 MB, the checkout holds 56 files / 2.2 GB ([[evidence:ev-podcast-05]]) —
and two ways on test results (`README.md:7` "34/34", `README.md:285` and
`DECISIONS.md:9` "42/42", against 43 `check()` sites; [[evidence:ev-podcast-05]]).
For a project whose stated source of truth is `DECISIONS.md` (`DECISIONS.md:3-5`),
stale numbers in that file cost the reader trust in everything else it says.

**Score rationale.** Score 3. Solid, understandable product with sensible defaults and
a clear scope boundary (`DECISIONS.md` D14), held back from 4 by the unexecuted UX half
and by documentation that misstates the current state of its own library.

**Uncertainty.** Medium. This is not my primary lens, and most of the interaction
surface was never driven.

**Improvement.** Generate the counts in `README.md` and `DECISIONS.md` from the library
rather than typing them, or drop them. A number that goes stale silently is worse than
no number.

### agentic — Agentic and AI system design

**Evidence.** There is no AI or LLM in the running application. I read every server
module and every client script and found no third-party fetch target, no model
reference, no API key and no AI SDK, which corroborates
[[evidence:ev-podcast-07]] and the intake's independent read. The only same-origin
fetch targets are `/api/library`, `/api/progress/{id}`, `/api/rescan` and
`/api/media/{id}`. The AI connection is that the source audio was produced by Google
NotebookLM before this app existed (`DECISIONS.md:12-18`), and that
`.agentic/project.yaml` is six lines of inert project metadata
([[evidence:ev-podcast-09]], confirmed by direct read).

**Strengths, from this lens.** The absence is the correct answer for a local media
server, and it is a *controlled* absence: no key material to leak, no egress to
monitor, no prompt surface to inject, no model output rendered to the user. That is a
real, verifiable property, not a gap. The team also drew the boundary explicitly
rather than leaving it ambiguous.

**Deficiencies.** There is no agentic design to evaluate on its merits, so nothing here
can demonstrate appropriateness, observability or effectiveness of an AI system beyond
the decision not to have one.

**Score rationale.** Score 3. Scoring 0 would require reading "no AI" as "not
demonstrated", which would penalize a team for correctly declining to bolt a model
onto a podcast player and would conflict with the rubric's instruction not to reward
model names or agent count. Scoring above 3 would require an AI system that exceeds
expectations, and there is none. A panel member who argues this criterion is not
applicable to this submission is making a reasonable argument, and I would not resist
it in consolidation.

**Uncertainty.** Medium, and it is uncertainty about how to apply the criterion, not
about the facts. The facts are well supported.

**Improvement.** None worth making. Adding AI to this application would add risk
surface without solving a problem the team has.

### engineering — Engineering and maintainability

**Evidence.** The implementation is small, coherent and proportionate: four server
modules, five client modules, no build step, no framework where none is needed
(`DECISIONS.md` P1). Comments explain the non-obvious choices at the point of the
choice (`server/app.py:137-142`, `web/js/opfs-worker.js:1-11`,
`server/media.py:65-67`). `DECISIONS.md` records 22 decisions and 8 deviations from the
original plan with rationale, which is well above what this event normally produces.
Schema evolution is handled deliberately and minimally (`server/db.py:48-58`,
`DECISIONS.md` P8).

**Deficiencies, this lens.**
- `F1` The destructive path described in the executive summary is an engineering
  defect as much as an ops one: `prune_missing` treats "no media files visible right
  now" as "the library is gone", and the cascade turns that into permanent loss of the
  only non-derived data (`server/app.py:64,70-76`; `server/db.py:25,37,94-103`).
- `R4` Episode identity is the SQLite rowid assigned in filename-sort order at scan
  time (`server/media.py:105-127`, `server/db.py:11-22`). Renaming a source file
  changes its identity, and this library contains 15 renamed or superseded takes
  ([[evidence:ev-podcast-16]], `releases.json` "unresolved"). The team already knows
  this is wrong: `DECISIONS.md:137-138` states "Episode identity must be the slug, not
  the scan-order row id" — but only for the proposed public component, not for the
  submitted one.
- `R2` One `sqlite3` connection with `check_same_thread=False` is shared globally
  (`server/db.py:33-39`) across FastAPI's sync threadpool. WAL mode and Python's
  serialized sqlite3 make this survivable for one user; it is not a defect at this
  scope, but it is the first thing that would break under a second listener.
- The documentation inconsistencies under `product` are also a maintainability signal.

**Score rationale.** Score 3. The code reads well and the decision record is genuinely
strong, but a data-destroying default path plus an unstable primary key in a schema
that already has a stable natural key (`filename`, which carries a `UNIQUE`
constraint at `server/db.py:13`) keeps this at solid rather than strong.

**Uncertainty.** Medium. The code was read in full; the judgment about how often the
empty-media-directory path fires in practice is inference.

**Improvement.** Key `progress` on `filename` rather than the rowid, or at minimum
refuse to prune when `records` is empty. Both are a few lines.

### reliability — Reliability, testing, and observability

**Score: NE.**

**What the package does establish.** Some reliability properties have direct or
artifact evidence and should not be lost behind the `NE`:
- `/healthz` reports liveness plus episode count ([[evidence:ev-podcast-02]];
  `server/app.py:210-213`).
- The systemd unit sets `Restart=on-failure`, `RestartSec=5` and a transcode-aware
  `TimeoutStartSec` (`deploy/podcast-listener.service:27-31`), and `README.md:239-251`
  lists the three conditions that must hold for restart-after-reboot to actually work,
  with the commands to verify each. That is better operational thinking than this
  event usually sees.
- Client-side recovery exists and is deliberate: `reconcile()` reclassifies interrupted
  downloads and OS-evicted files on every startup (`web/js/storage.js:117-128`), and
  dirty progress rows drain through `flushQueue()` when connectivity returns
  (`web/js/player.js:71-75`). The server half of that queue was observed working:
  section 6 passed all four of its checks, including "progress synced to server (not
  dirty)" ([[evidence:ev-podcast-15]]).
- Logging is uvicorn access logs plus a startup index line, collected by journald
  ([[evidence:ev-podcast-02]] run record; `deploy/podcast-listener.service:16`).
  Proportionate for this scope; no structured logging or metrics, which I do not count
  against a prototype.

**Why that is still not enough to score.** The submission's own reliability claim is
its test suite, and no execution of it has completed. Three runs against the same
commit and the same image produced three different outcomes:
- stage 7 stall after `page.reload()` ([[evidence:ev-podcast-15]]);
- stage 3 download-complete wait timing out after 90s, during a 71-second overlap with
  another container on a `--cpus 1.0` host ([[evidence:ev-podcast-16]]);
- stage 3 Chromium `Target crashed` in isolation, about 7 seconds into the suite
  ([[evidence:ev-podcast-20]]).

None is classified. [[evidence:ev-podcast-19]] is reasoning, not re-execution, and the
crash has no memory measurement behind it ([[evidence:ev-podcast-20]]). I read the
stage-7 evidence directly and find [[evidence:ev-podcast-19]] persuasive — the run
record shows the single episode marked `completed: True` before the reload
([[evidence:ev-podcast-15]] run record), `hidePlayed` defaults to `"1"` and the
visibility filter is `!hidePlayed || !isFinished(e.id) || playing?.id === e.id`
(`web/js/app.js:16-19,105-128`), so after a reload with nothing playing the only row
is correctly hidden and `.ep` can never appear. Persuasive is not confirmed; no run
inspected the post-reload DOM.

Two additional facts stop me from resolving this from the source instead. First, the
team's own pass claim is internally inconsistent and cannot be reconciled with the
code (34 vs 42 vs 43 `check()` sites; [[evidence:ev-podcast-05]]), so I cannot fall
back on it. Second, `F4`: the download path the two failing runs die in has no
failure detection of its own. `web/js/storage.js:13-31` registers only
`worker.onmessage` — there is no `onerror`, no `onmessageerror`, and no timeout on the
promise at `web/js/storage.js:49-76`. If the worker dies without posting a message,
which is exactly what a crashed renderer looks like, the promise never settles, the
row stays `downloading`, the button stays disabled, and the only recovery is a reload
(after which `reconcile()` does clean up correctly). So a hung download in this app is
indistinguishable from a slow one, to the test suite and to the user. That is a real
observability gap in the exact place the evidence is inconclusive — and it is also a
candidate explanation for the 90s timeout, which pulls in the opposite direction from
the host-contention reading.

On this package I could defend a low score by pointing at zero completed runs of the
one safety net, or a high score by pointing at the ops artifacts and the fact that
every failure has a plausible environmental cause. That is what `NE` is for. Per the
rubric, `NE` is not a numeric zero and it blocks an official total until the panel
resolves it.

**Uncertainty.** High confidence in the `NE` determination itself; the ambiguity is
thoroughly documented in the package and I reproduced the reasoning from the run
records rather than accepting it.

**What would settle it.** One run of the unmodified suite to completion, in isolation,
with a library of at least three episodes so the hide-played interaction cannot
mask the list, and with the container memory raised enough that a Chromium renderer
crash can be excluded or measured. If the suite completes, `reliability` becomes
scoreable from evidence in a single run.

**Improvement.** Independent of the event: add `worker.onerror` and a timeout to
`web/js/storage.js` so a dead worker becomes a reported error instead of a permanent
"downloading" state.

### security — Security, privacy, and responsible AI

**Evidence, positive.** Beyond the items in the executive assessment: the range parser
rejects a malformed `Range` header and returns `416` with a correct `Content-Range` for
a past-EOF request, verified by execution rather than by reading
([[evidence:ev-podcast-03]]). `PUT`/media access for an unknown episode raises rather
than creating state ([[evidence:ev-podcast-03]]; `server/app.py:110-111,143-145`). No
secret material is committed — I grepped the tree for key, token, password and PEM
headers and the only hits are prose inside an HTML planning document. The team wrote
its threat model down, including the parts that cost it something: `DECISIONS.md` P6
accepts permanent publication of machine names in Certificate Transparency logs
knowingly, and P7 explains why the self-signed CA path is retained but unused. Privacy
posture is clean: no telemetry, no PII, no analytics, no third-party egress
([[evidence:ev-podcast-07]]). The publicly-reachable draft audio disclosed in
`DECISIONS.md:139-145` belongs to a proposed, unbuilt Cloudflare component and has no
counterpart in this checkout ([[evidence:ev-podcast-08]]); I do not score it against
this submission, and I note that disclosing it at all is to the team's credit.

**Deficiencies and risks.**
- `F2` **Bind address contradicts the documented perimeter.** `run.sh:61` execs
  uvicorn with `--host 0.0.0.0` on port 8000 after printing
  `==> HTTP on http://127.0.0.1:8000` at `run.sh:60`; the `--https` branch does the
  same on 8443 (`run.sh:55-57`). The only access control in the system is a host
  firewall rule and `tailscale serve`, both documented in prose and neither present in
  the repository (`DECISIONS.md:81`, `README.md:265-267`). Consequence on a host where
  that external step is missing or the machine changes networks: unauthenticated read
  of the entire private library over `/api/media/{id}`, unauthenticated writes to every
  listener's resume position, and unauthenticated `/api/rescan`. This is a credible
  risk, not a demonstrated exploit — every sandbox run bound `127.0.0.1`
  ([[evidence:ev-podcast-02]] run record), so nothing in the package tests the exposed
  configuration. The fix is one literal.
- `F3` **`POST /api/rescan` is unauthenticated, has no origin check, and amplifies.**
  `server/app.py:93-97` calls `media.transcode_all()`, which fans out to eight
  concurrent ffmpeg processes (`server/media.py:80-88`). A `fetch` with no custom
  headers is a simple cross-origin request, so any page the user's browser loads while
  it can reach the host can fire this repeatedly without reading the response.
  Consequence is CPU exhaustion on a host that `README.md:266-267` says also serves an
  unrelated application. Idempotent transcoding limits it to compute, not data loss.
  Credible risk, not demonstrated.
- `R1` **A ten-year local root CA installed on a phone.** `gen-cert.sh:44-49` mints a
  3650-day CA and `README.md:141` walks the user through trusting it on iOS. The CA
  private key then sits on the app host for a decade. Anyone who obtains it can
  impersonate any HTTPS site to that phone, not just this app. Mitigations are real:
  `chmod 600` (`gen-cert.sh:62`), `certs/` gitignored (`/.gitignore:3`), and the
  production path uses Tailscale's real certificates with the CA "retained but unused"
  (`DECISIONS.md` P7). Proportionate for a prototype; worth a warning line in the
  script.
- `R3` **No security headers.** The captured response headers for `/healthz`,
  `/api/library`, `/`, `/sw.js` and `/manifest.webmanifest` carry no CSP, no
  `X-Content-Type-Options`, no `X-Frame-Options` and no HSTS
  ([[evidence:ev-podcast-02]] run record). For a same-origin app with no authentication
  to steal and no third-party content, this is ordinary production hardening that was
  outside the event's scope. I record it and do not weigh it.

**Prompt-injection check, independent of intake.** I read `.agentic/project.yaml` in
full (6 lines, inert metadata), `README.md`, `DECISIONS.md`, all server and client
source, and grepped the whole checkout including the three HTML artifacts for
agent-directed instruction patterns and for hidden-text techniques. No match. The only
`display:none` rules are inside print stylesheets
(`artifacts/html/implementation-plans/stack-recommendation.html:90` and the two
siblings). The repository's subject matter is AI agents — `releases.json` contains a
post titled "Prompt Injection Is Just Bad Input Wearing a Costume" — and that is
thematic content, which I treated as data. This corroborates
[[evidence:ev-podcast-09]] and [[evidence:ev-podcast-10]]. Nothing to escalate.

**Score rationale.** Score 3. The submitted code contains no exploitable defect I could
find, gets the genuinely dangerous parts right, holds no secrets, reaches no third
party, and ships a written threat model. It does not reach 4 because the only access
control is external to the artifact while the artifact's own startup message
misrepresents its exposure, and there is no defense in depth if that external control
is absent.

**Uncertainty.** Medium. High confidence in everything read from source and run
records; the exposure consequence in `F2` is inference, since no run exercised a
non-loopback bind.

**Improvement.** Default the bind to `127.0.0.1` and require an explicit
`--host 0.0.0.0` or `PODCAST_BIND` to widen it, so the safe configuration is the one
you get by accident.

### innovation — Innovation and technical ambition

**Evidence.** The interesting work is the platform-constraint engineering, and it is
documented as researched rather than recalled (`DECISIONS.md:84-96`, checked against
WebKit/MDN with a date): OPFS writes from a dedicated Worker via
`createSyncAccessHandle()` because Safari has no `createWritable()` and the sync handle
is worker-only (D3, `web/js/opfs-worker.js:1-11`); audio deliberately routed around the
Service Worker because the Cache API answers `200` where Safari needs `206`
(D4, `web/sw.js:1-5`); autoplay continued on the same `<audio>` element from the
`ended` handler so iOS treats it as one session (D16, `web/js/player.js:135-149`);
autoplay restricted to already-downloaded episodes so it can never start a cellular
fetch with the screen locked (D15, `web/js/app.js:298-311`). These are constraint-driven
choices with stated failure modes, not decoration.

**Deficiencies.** The techniques are known ones applied well, not new ones. And the
most ambitious paths — blob-URL playback, offline playback, autoplay continuation —
were never executed in this package ([[evidence:ev-podcast-06]]), so their ambition
currently rests on the team's account plus a source read.

**Score rationale.** Score 3. Real technical depth in a narrow area, honestly scoped,
but unexecuted where it is most novel.

**Uncertainty.** Medium.

**Improvement.** Get sections 4 and 8 through 11 of the suite to run somewhere and
publish the output. The novel claims are the ones with no independent evidence behind
them.

## Surprises

**Better than expected.**
- The hand-written range handler. Rolling your own `206` logic is usually where a
  prototype breaks, and this one answered six adversarial cases correctly including
  suffix ranges and malformed headers ([[evidence:ev-podcast-03]]).
- Operational honesty. `README.md:239-251` lists the three independent conditions that
  must all hold for restart-after-reboot to work, with a verification command for each.
  Most submissions at this stage claim "runs under systemd" and stop.
- The team marks its own unverified claims as unverified, including two on the device
  they own ([[evidence:ev-podcast-10]]). That is rarer than it should be.

**Worse than expected.**
- `F1`. A comment in `server/config.py:24-25` labels the directory holding the only
  irreplaceable user data as safe to delete, and the startup path makes that label
  actively dangerous.
- `F6`. Three different library sizes and two different test-pass counts across two
  documents that each claim authority. In a file that opens by declaring itself the
  source of truth (`DECISIONS.md:3-5`), that is a bigger credibility cost than the
  individual numbers are worth.
- `F4`. The download path has no way to tell a hung worker from a slow one, which is
  precisely where two of the three inconclusive runs died.

## Blocking and major issues

**Confirmed defects (established by inspection of the pinned code; no execution
exercised these paths, so classed as artifact evidence plus inference, not
demonstrated exploits).**

- `F1` **Silent, unrecoverable loss of listening progress.** Startup always calls
  `index_library()` (`server/app.py:70-76`, [[evidence:ev-podcast-14]]). If
  `MEDIA_DIR` is empty or absent — a failed mount, a cleared cache, a transcode that
  produced nothing, or the operator following `server/config.py:24-25` — then
  `scan_library` returns no records (`server/media.py:105-127`) and
  `prune_missing(conn, [])` runs `DELETE FROM episodes` (`server/db.py:94-103`), which
  cascades to `progress` (`server/db.py:25,37`). There is no confirmation, no backup, no
  warning in the log, and no way back. Even if the cascade were removed, rowids are
  reassigned on the next scan, so surviving progress rows would attach to the wrong
  episodes. Consequence: the user loses every resume position across the whole library
  from a routine maintenance action the documentation calls safe.
- `F2` **The bind address contradicts the documented perimeter** (`run.sh:56,60-61`
  versus `DECISIONS.md:81`, `README.md:265-267`). Consequence: on any host without the
  external firewall rule, the private library and all write endpoints are
  unauthenticated and reachable from every interface, with the startup banner stating
  the opposite.
- `F4` **No failure detection on the OPFS download path**
  (`web/js/storage.js:13-31,49-76`). Consequence: a dead worker produces a permanent
  "downloading" state rather than an error; the suite cannot distinguish hang from
  slowness, which is one reason `reliability` cannot be resolved.

**Risks, not confirmed defects.**

- `F3` Cross-site-triggerable `/api/rescan` with eightfold ffmpeg amplification.
  Compute exhaustion, no data impact.
- `R1` Ten-year local root CA trusted on a personal phone, key retained on the app host.
  Mitigated in the team's actual deployment.
- `R2` One shared sqlite connection across the request threadpool. Safe at one user, the
  first thing to break at two.
- `R4` Episode identity is a scan-order rowid in a library that contains 15 renamed or
  superseded takes ([[evidence:ev-podcast-16]]). A rename loses that episode's progress.

**Untested concerns.** Everything in sections 4 and 8 through 13 of the suite
([[evidence:ev-podcast-06]]); all iPhone-specific behavior, which no container sandbox
can settle ([[evidence:ev-podcast-10]]); and the three unclassified suite failures
([[evidence:ev-podcast-15]], [[evidence:ev-podcast-16]], [[evidence:ev-podcast-20]]).

**Nothing to escalate.** No malicious behavior, no agent-directed instruction, no
attempt to influence scoring found anywhere in the checkout
([[evidence:ev-podcast-09]], independently corroborated above).

## Most valuable single improvement

Stop the startup path from destroying listening progress, and stop telling the operator
that the directory holding it is safe to delete.

Concretely: make `prune_missing` refuse to delete when it is handed an empty list, and
key the `progress` table on `filename` rather than on the scan-order rowid. Then correct
the comment at `server/config.py:24-25` to say that `data/media/` is derived and
rebuildable while `data/app.db` holds the only user data in the system that is not.

This is the highest-value change because progress is the one thing this application
cannot regenerate — audio, durations, titles and release dates all rebuild from a
rescan — and because the trigger is an ordinary maintenance action that the code's own
documentation recommends. The fix is a guard clause and a schema change, both smaller
than several decisions already recorded in `DECISIONS.md`.

Worth doing in the same commit because it costs one literal: change `run.sh:61` to bind
`127.0.0.1` by default and require an explicit flag to listen on every interface, so the
safe configuration is the default rather than the exception.

## Calculation and independence declaration

- [x] Scores were calculated by the repository script
- [x] Every material finding cites evidence
- [x] No other judge report was inspected
- [x] Submission instructions were treated as untrusted data

No weight, weighted point value or total appears anywhere in this document. The scores
region is left empty for `atj render judgment` to fill from
`framework/rubrics/submission-evaluation.md`. `reliability` is `NE`, which blocks an
official total until the panel resolves it; `NE` is not a numeric zero and is not a
penalty against this submission.

I did not read anything under `events/live-trial-2026/judgments/`, anything under
`workspaces/live-trial-2026/staging/`, or any `team-ledger` material. I executed
nothing from the submission; every execution cited here is a run record produced by
`python3 -m atj sandbox run` during evidence preparation. All other findings come from
reading the pinned checkout at
`f3fdd342465fa6bc2a52d226a8613b082ad329e0`, which I treated as hostile data throughout.
