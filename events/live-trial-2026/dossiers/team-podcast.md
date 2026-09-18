---
event_id: live-trial-2026
team_id: team-podcast
commit: f3fdd342465fa6bc2a52d226a8613b082ad329e0
evidence_package_id: ev:live-trial-2026:team-podcast:f3fdd342465f:d06f90cc
rubric: submission-evaluation@1.0.0
persona: build-team-dossier@1.0.0
framework_commit: 96e3f32
source_reports:
- summaries/team-podcast.md
- summaries/team-podcast.json
- adjudications/team-podcast-reliability-ne.md
- matchups/mu-final-01.md
- matchup-passes/mu-final-01-pass-a-first.md
- evidence/team-podcast/manifest.md
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-18T00:00:00Z"
completed_at: "2026-09-18T00:00:00Z"
total: null
finalized: false
visibility: team
approval_state: draft
validation_state: unvalidated
---
# Team Dossier — Podcast Listener (team-podcast)

## Your project at a glance

A self-hosted listener for a private audio library: a small Python server that
indexes and transcodes local `.m4a` files, serves them with correct byte-range
responses so `<audio>` seeking works, and a no-framework progressive web app
that downloads episodes into OPFS for offline listening on an iPhone and keeps
listening progress in sync. Four modules on the server, five on the client, no
build step. Judged at commit `f3fdd342465fa6bc2a52d226a8613b082ad329e0`.

**Read this first: you finished `live-trial-2026` without an official total, and
that is the event's doing, not yours.**

One of the seven rubric criteria — `reliability` — could not be scored. All four
judges independently returned `NE` ("not enough evidence"), and the rubric is
explicit that `NE` is not a zero and that no official total can be finalized
while a criterion carries it. An adjudication was opened specifically to ask
whether that `NE` could be cleared. It was decided by the event director, and it
**accepted** the `NE` and recorded the reason in these terms: this is the
framework's and the operator's failure, not the team's.

Here is what happened, plainly. Your own end-to-end suite was executed three
times in this event, against the same commit and the same container image, and
produced three different outcomes — a stall part-way through, a download wait
that timed out during a measured 71-second overlap with another container, and a
browser crash. None of the three could be classified. Every failure the panel
was able to trace points **away from your code**: in both of the stage-3
failures the server had already logged `GET /api/media/1 200 OK` before anything
went wrong, so your server had done its job. The environment it ran in could
not: the event's sandbox gave every submission a 64 MB `/tmp`, which cannot hold
your 2.2 GB library, and a 64 MB `/dev/shm` with no `--shm-size` override, which
is well under what a Chromium renderer needs.

Three of the four judges, working independently, said the same thing: one
re-run of the suite with `--shm-size` raised against a small library would very
likely have made `reliability` scorable, and that run was an **operator action,
not work you owed**. The event declined to do it, because re-running evidence
after judging had begun would have invalidated all four judgments that cite this
evidence package. That was a defensible call about event integrity, and it cost
you a total. It is not a statement about your engineering, and nothing in this
dossier should be read as one.

There is no provisional, unofficial or partial figure in this document, because
no such figure is a result. Nothing was scored zero, nothing was penalised, and
no adverse inference was drawn from the criterion that could not be scored.

## What you did especially well

- **Your byte-range implementation is correct on exactly the cases hand-written
  range code usually gets wrong.** Full-file, mid-file, open-ended, suffix form
  (`bytes=-500`), past-EOF returning `416` with `Content-Range: bytes */5000000`,
  and a malformed header rejected with `400` — six request shapes, verified with
  exact streamed byte counts, on two different images (`ev-podcast-03`). All
  four judges named this independently, and it was the strength most consistently
  credited across the panel. You chose to hand-write this path (P2) because a
  framework difference "would be miserable to debug on a phone", and the code you
  wrote holds up.
- **The OPFS download path is clean and fast.** An instrumented single-episode
  probe completed the download in one second, wrote a file byte-identical to the
  transcoded output at 4,884,617 bytes, recorded `state: "done"` in IndexedDB
  with a matching byte count, moved `storage.estimate()` from roughly 132 KB to
  roughly 5.0 MB, and produced zero console messages and zero page errors for the
  whole session (`ev-podcast-17`). This is the single cleanest observation in
  your evidence package, and it decisively rules out any reading in which "the
  download is broken".
- **Your decision record is the strongest artifact in the checkout.** 22
  decisions with rationale, plus an 8-row table recording where the
  implementation deviated from the original plan and why — including the ffmpeg
  `-f ipod` flag needed because the temporary file ends in `.part`. One judge
  called it the single most useful maintenance artifact in either submission in
  this event. The judges checked the code against the stated reasons at every
  point they looked, and it matched every time. This is a maintenance artifact,
  not marketing, and it is rare at this level.
- **The real pipeline works end to end on real audio.** An 18,631,917-byte
  source transcoded to 4,884,617 bytes, indexed with
  `duration_sec: 578.896009` and a title correctly derived from the filename
  (`ev-podcast-15`).
- **Progress persistence behaves exactly as you claimed.** Last-write-wins
  applies, a stale write is rejected without clobbering, a newer write is
  accepted (`ev-podcast-03`), and the server half passed all four of its checks
  in a live run (`ev-podcast-15`).
- **Platform-constraint research that is documented, dated and load-tested
  against the actual platform docs.** OPFS written from a dedicated worker
  because Safari has no `createWritable()` and `createSyncAccessHandle()` is
  worker-only (D3); audio routed around the service worker because the Cache API
  answers `200` where `<audio>` needs `206` (D4); autoplay continued on the same
  element from the `ended` handler because iOS treats a new element as a fresh,
  blockable session (D16); completeness tracked in IndexedDB because OPFS has no
  rename (P5). This is real depth.
- **The refusal to fuzzy-match.** After duration matching produced two confident
  false pairs 0.4 s apart, you chose an exact-filename join that fails loudly
  into an `unresolved` list with typed reasons (D21). One judge called it the
  best judgment call in the submission.
- **Operational honesty.** `README.md:239-251` lists the three independent
  conditions that must hold for restart-after-reboot, with a verification
  command for each, and you mark two of your own iPhone claims unverified on the
  device you actually own. Judges notice that.
- **Security handled at the point of risk.** `ffmpeg`/`ffprobe` invoked as
  argument lists with absolute paths and no shell, so a filename cannot become a
  command; the media path resolved from a database row populated only from
  basenames of a local glob, so there is no traversal surface; every interpolated
  episode string escaped; the service worker declining to intercept `/api/` and
  audio; no credentials anywhere (`ev-podcast-07`). Two judges separately swept
  the tree for injected instructions, including hidden-text techniques, and found
  none.

## Corrections to the record

Two things in the evidence package were wrong, and both are corrected here in
your favour. These corrections are binding on every artifact downstream of this
one.

**Your "42/42" claim was right. The package that checked it was wrong.** The
evidence package counted 43 `check()` call sites in `tests/e2e.py` using
`grep -c "check("` and concluded that neither of your documented figures matched
the source. The real count is **42**. The 43rd match is the function definition
`def check(` at `tests/e2e.py:33`. Counting call sites stage by stage gives 42,
and `grep -c "^\s*check("` gives 42. Your claim at `README.md:285` and
`DECISIONS.md:9` is therefore **consistent with your own source**. One judge
caught this independently during their own read and recorded the correction;
three carried the package's figure forward, and one of those escalated it to a
confirmed problem it never was. That escalation does not stand.

The documentation drift finding survives, but it is half the size the package
recorded and it is now one line, not a pattern: **only `README.md:7`'s "34/34" is
genuinely stale** against a 42-check suite. Fix that one number and this finding
disappears entirely.

**Your suite is 13 stages, not 11.** The evidence package described
`tests/e2e.py` as an 11-stage suite and reported the best run as reaching
"stage 7 of 11". The suite is actually 13 stages. This changes nothing that was
observed; it means the unexecuted portion is larger than the package stated. It
is a correction to the package, not a finding against you. Separately, the
library-size figures in `README.md:10` (33 files / 1,360 MB) and
`DECISIONS.md:16` (28 files / 1,112 MB) are stale against the 56 files / 2.2 GB
actually in the checkout, and that one is real.

## Criterion feedback

The panel's per-criterion means on the rubric's 0-5 scale are below. They are
per-criterion figures only. They are not combined into an overall result for this
event, and no overall result exists.

| Criterion | Panel mean | Agreement |
|---|---|---|
| Functional correctness and completeness | 3.00 / 5 | unanimous |
| Product value and usability | 3.75 / 5 | aligned (4/4/4/3) |
| Agentic and AI system design | 2.75 / 5 | aligned numerically; genuinely split on interpretation |
| Engineering and maintainability | 3.75 / 5 | aligned (4/4/4/3) |
| Reliability, testing, and observability | `NE` | unanimous — not scorable in this event |
| Security, privacy, and responsible AI | 3.00 / 5 | unanimous |
| Innovation and technical ambition | 3.25 / 5 | aligned (3/4/3/3) |

### Functional correctness and completeness

**Strengths.** Everything that was executed produced exact, correct output:
server boot and PWA asset serving, byte-range across six shapes, real transcode
and indexing of real audio, progress put/get/stale/newer, and library render,
ordering, title-from-filename and hide-played-by-default observed in a live
browser (`ev-podcast-02`, `-03`, `-14`, `-15`, `-17`, `-20`).

**Limitations.** Roughly half of the advertised product was never executed by
anyone — including offline playback, which `DECISIONS.md:15` calls a hard
requirement and which the whole architecture exists to satisfy. All four judges
landed on 3 for the same reason: the executed half is exact and the unexecuted
half is large. Two apparent failures in the run logs are not defects and were
read the same way by every judge who addressed them. The stage-5 `[FAIL]` ("seek
to 600s landed — 578.9s") is your code correctly clamping to the end of a
578.9-second fixture against a test that hardcodes 600 s. The stage-1 "0 of 2
dated" failure is fully explained by both fixture files sitting in
`releases.json`'s own `unresolved` block.

**Next step.** Make the suite runnable in a small environment (see the
improvement plan) so the unexecuted half can be demonstrated rather than
described. Nothing here suggests it does not work; it was simply never seen.

### Product value and usability

**Strengths.** Design judgment that is visible in the code and matches its
written reasons: hide-played-by-default with the currently playing row exempted
(D19); autoplay restricted to already-downloaded episodes so it cannot start a
cellular fetch on a locked screen (D15); three distinct empty states that each
name the control that fixes them; a status line covering loading, offline, error
and success; and a header that surfaces `storage.estimate()` usage, quota and
persistence — instrumenting the one question you could not answer off-device.

**Limitations.** Most of the interaction surface was never driven, and the stale
documentation figures cost a reader trust in a file that opens by declaring
itself the source of truth. One judge weighted those two things more heavily and
held at 3; the other three placed it above solid. That is a weighting
difference on an identical factual record, not a dispute about what is true.

**Next step.** Accessibility is the cheapest real gain here: `#status` is a plain
`<p>` with no `role="status"` and no `aria-live`, so every message the app
produces is silent to a screen reader; row and transport controls are named only
by emoji or box-drawing glyphs; and the currently-playing row is distinguished by
border colour alone.

### Agentic and AI system design

**This is a gap in the rubric, not a mark against your engineering.** The facts
are not in dispute and were verified independently by all four judges: there is
no model, no API key, no AI SDK and no third-party fetch target anywhere in the
server modules or the client scripts; the only `fetch()` targets are same-origin;
`.agentic/project.yaml` is six inert metadata lines; and every sandbox run
executed with `--network none` and the app worked. Your application correctly
contains no AI at all, you documented why, and the absence is verified rather
than asserted.

The rubric does not say how to score that. The criterion asks whether AI is
"appropriate, controlled, observable, and effective". A verified, appropriate,
documented absence answers the first two and leaves the last two with no subject.
Three judges applied the "primary expectations met" anchor and scored 3. One
applied the "partial" anchor and scored 2, on the reasoning that the subject of
the criterion is absent. **All four explicitly asked for a rule on how to score a
submission that correctly declines to use AI, and none of them could supply
one.** One wrote that a judge reading this criterion as requiring a demonstrated
AI system could score it much lower and that this reading is available from the
same anchors — which is exactly why the framework, not the team, owns this
problem.

The gap is recorded against the framework as defect D12 and referred to the event
director. The 2.75 mean is arithmetic the consolidation policy requires; it is
not a panel finding that your submission is deficient on this axis. Do not add
AI to this application to chase this criterion. The scoping decision was correct.

### Engineering and maintainability

**Strengths.** Four server modules and five client modules with one
responsibility each; no build step where none is needed (P1); comments that
explain the non-obvious constraint at the point of the choice; and the decision
and deviation records described above. Three judges recorded high confidence
here and it is the best-supported criterion in the whole evaluation.

**Limitations.** Four defects, all found by reading your source rather than by
anything failing at runtime: the prune/cascade data-loss path, episode identity
carried as a scan-order rowid, one module-level SQLite connection shared across
the sync threadpool, and no unit tests anywhere. The first two are in the
blocking-issues section below. On the third, `put_progress` does a non-atomic
read-then-write on a connection opened with `check_same_thread=False` and shared
across the pool; that is correct at one writer, which is D7's stated premise, but
the premise is not written down anywhere as a hard constraint. One judge held at
3 weighting the data-loss path and the unstable key; the other three treated the
same findings as what keeps this off the top band rather than what pulls it below
strong.

**Next step.** Write the one-writer assumption down next to the connection, and
add unit tests under the two pieces of logic you deliberately hand-wrote because
they are risky — the range parser (`server/app.py:132-205`) and the
last-write-wins comparison (`server/db.py:153-167`). Right now the only test of
your range code in existence is the one the event wrote.

### Reliability, testing, and observability

**Not scored, and not scorable in this event. This is the event's constraint,
not a judgment about your work.** The full explanation is in the opening section;
in short, three executions of your suite produced three unclassified outcomes,
every traced failure points away from your code, and the one re-run that would
have settled it was an operator action the event declined to take. Each judge
reached `NE` independently and each gave the same structural reason: on this
evidence a low score and a high score are both defensible, which is the exact
condition `NE` exists for.

**What should not be lost behind the `NE`.** The panel recorded these as real
and working, and they deserve stating: `/healthz` reports liveness plus episode
count; your systemd unit sets `Restart=on-failure`, `RestartSec=5` and a
transcode-aware `TimeoutStartSec`; `README.md:239-251` lists the three
conditions that must hold for restart-after-reboot with a verification command
for each; `storage.reconcile()` reclassifies both interrupted downloads and
OS-evicted files at startup, which are the two failures that actually happen on
a phone; dirty progress rows drain through `flushQueue()` when connectivity
returns, and the server half of that was observed passing all four of its
checks; and your suite derives expected counts from the live `/api/library`
payload instead of hardcoding them, which is better practice than most suites at
this level.

**What blocked the score.** Your reliability story rests on a single end-to-end
suite, and no execution of it has ever completed here, so your own pass claim
could not be checked against anything. That is not a criticism of the suite's
content — it is a statement about what this event was able to run.

**Next step.** Improvement 3 in the plan below makes this criterion scorable next
time, by making the suite report what it did reach instead of aborting. It does
not change anything about `live-trial-2026`.

### Security, privacy, and responsible AI

**Strengths.** All four judges scored 3 on a shared reading: they could not find
an exploitable defect in the submitted code. The specifics are listed under "What
you did especially well". No telemetry, no analytics, no third-party egress, and
`.env`, `certs/` and `data/` correctly gitignored.

**Limitations.** The entire access-control model lives outside the artifact —
`tailscale serve` plus a firewall rule, documented as prose that this evaluation
never observed, with no defence in depth behind a single escaping function, no
security headers and no CSP on any captured response. Nothing was
penetration-tested by anyone, on either side of the final. The sharpest specific
gap: `run.sh:60-61` prints `==> HTTP on http://127.0.0.1:8000` and then execs
uvicorn with `--host 0.0.0.0`. The application listens on every interface and
tells the operator it does not. The `--https` branch does the same on 8443.

**Next step.** Default the bind to `127.0.0.1` and require an explicit flag to
widen it, so the safe configuration is the one you get by accident. Also worth a
look: `/api/rescan` is unauthenticated and cross-site triggerable, and it fans
out across `ThreadPoolExecutor(max_workers=8)`, so a single cross-origin `POST`
costs eight transcodes on a host your README says also serves something else. No
data impact, and this was recorded as a credible risk rather than a confirmed
defect because nobody tested it.

### Innovation and technical ambition

**Strengths.** Unanimous agreement that the depth is real, and that it is
platform-constraint engineering rather than novelty for its own sake — the D3 /
D4 / D16 / P5 chain described above, researched against WebKit and MDN with
dates rather than recalled. One judge scored 4, weighting that chain plus the one
directly observed payoff: the OPFS write producing a byte-identical file with a
matching storage estimate.

**Limitations.** Three judges held at 3 because these are known techniques
applied well rather than new ground, and because the paths with the highest
ceiling — background audio under screen lock, lock-screen MediaSession controls,
offline playback — are precisely the ones with no execution evidence. That is an
evidence gap created by what could be run, and every judge named it as such.

**Next step.** Capture evidence on the device you own. A short screen recording
of a locked-screen playback session and a real `storage.estimate()` reading from
the phone would convert three team claims into observations.

## What could not be observed

This list is not a list of things that failed. It is a list of things nobody
was able to watch, and it is stated so you know where your evidence is thin
rather than where your app is.

- **Stages 4 and 8 through 13 of `tests/e2e.py` never ran in this event**
  (`ev-podcast-06`): blob-URL playback, offline library render, offline playback,
  filter persistence across reload, autoplay into the next downloaded episode,
  single and bulk delete, and the suite's own JavaScript-error sweep. Offline
  playback is the requirement you yourself call hard.
- **Every iPhone-specific claim.** Install to home screen, background audio under
  screen lock, lock-screen MediaSession controls, and real iOS quota and
  `persist()` behaviour rest on your own account and cannot be settled by any
  container (`ev-podcast-10`). You already mark two of them unverified.
- **Behaviour at real library size.** The 56-file, 2.2 GB library was never
  exercised, because the sandbox `/tmp` is a 64 MB tmpfs. Every observation about
  ordering, rendering, download and filtering rests on a one- or two-episode
  fixture. One judge noted explicitly that this gap is a property of the test
  fixture, not of your app.
- **Nothing adversarial was attempted.** No penetration testing; the tailnet
  perimeter, the firewall rule and `tailscale serve` were never observed.
- **No complete download-listen-offline cycle** was performed by a person, and
  no screenshot or rendered-UI artifact exists.

## Tournament journey

`live-trial-2026` had two entrants and a single match, so your only matchup was
the final.

- **The final.** You met team-ledger, and the panel's resolved outcome was that
  they advanced. Both presentation orders were judged independently, by judges
  who could not see each other's work, and both picked the same side, so the
  outcome confirmed automatically with no adjudication.
- **The combined margin was +35.00 on a -100..+100 scale**, against a close-call
  band of +/-5.0. It is a clear result and it is reported here without spin.
- **No criterion reached a decisive value in either pass.** The outcome rests on
  four meaningful comparative advantages that both orders agreed on —
  `functional`, `agentic`, `engineering` and `security` — plus `innovation`,
  where the two orders differed in magnitude but not direction. `product` came
  out as substantially equal in both orders: each submission has one strong
  surface and one rough one, and neither advantage was material.
- **Both matchup judges independently refused to treat your unscored
  `reliability` as a deficiency.** It was assessed at comparison value `0`,
  "substantially equal or insufficient comparative evidence", in both orders, and
  it contributed nothing to the margin either way. Both passes also recorded, in
  their own words, that the evidence asymmetry between the two submissions was
  created by the event and not by the teams — one suite ran to completion and
  yours never did, for the same 64 MB tmpfs, 64 MB `/dev/shm`, no `--shm-size`
  reasons described above — and both declined to convert that asymmetry into a
  quality difference. Initial totals were not used, are not comparable, and the
  head-to-head rubric forbids selecting on them.
- **Both judges predicted the margin would land near the close-call band.** It
  did not. Neither judge computed the margin — the tool did, from their
  comparison values — which is the reason arithmetic stays in the tool.

## Blocking issues

Two confirmed, high-impact defects. Both were established by reading your source
at the pinned commit. Neither was observed failing at runtime — and more
generally, **your submission was never observed failing for any reason inside
its own code.**

**B1 — Deleting `data/media/` destroys every listener's progress, and your own
documentation says that directory is safe to delete.** `index_library()` calls
`prune_missing()` on every startup and on every rescan
(`server/app.py:64,70-76`). Handed an empty scan, that function issues a bare
`DELETE FROM episodes` (`server/db.py:94-103`). `progress` cascades
(`server/db.py:25`) with `PRAGMA foreign_keys = ON` (`server/db.py:37`). And
`README.md:53` plus `server/config.py:24-25` tell the operator that directory is
safe to remove "because a rescan rebuilds both". A rescan does not rebuild
progress. Audio, durations, titles and release dates all rebuild; listening
position is the one thing in this system that cannot be regenerated, and today a
documented, recommended cleanup wipes it with no prompt, no backup and no log
line naming what was lost. Two judges classed this a confirmed defect and one
classed it a risk because it was never executed; it is recorded here with that
provenance stated. Two of the four independently named fixing it the single most
valuable change you could make.

**B2 — Episode identity is a scan-order rowid used as a durable cross-device
key.** OPFS files are named `${episodeId}.m4a` (`web/js/opfs-worker.js:24`, read
back at `web/js/storage.js:92,103`) and IndexedDB progress is keyed the same way
(`web/js/idb.js:19-22`), while `id` is a plain `INTEGER PRIMARY KEY`
(`server/db.py:12`) reassigned in filename-sort order on every re-index
(`server/media.py:114`). A phone holding downloaded audio and a re-indexed server
can therefore disagree about which episode is which, and neither side can detect
it. `filename` is already `NOT NULL UNIQUE` (`server/db.py:13`) and would serve
as the key. Two details make this urgent rather than theoretical: your library
already contains 15 renamed or superseded takes, and `DECISIONS.md:138` states
the correct identity rule — you wrote the rule down and applied it to the
component you did not end up building.

## Recommended improvement plan

1. **Immediate repair — stop an indexing pass from destroying listening history,
   and stop telling the operator to trigger it (B1).** Make `prune_missing` a
   no-op when it is handed an empty record list, rather than issuing
   `DELETE FROM episodes` (`server/db.py:94-103`). Then correct `README.md:53`
   and `server/config.py:24-25` so they say `data/media/` is derived and
   rebuildable while `data/app.db` holds the only data that is not. This is a
   few lines and it removes the one way this application can lose something a
   user cannot get back.

2. **Highest-value next iteration — give an episode a stable identity, and make
   your suite tell you what it found (B2, plus the two honesty gaps).**
   - Key `progress` and the OPFS filename on `filename` instead of the
     scan-order rowid.
   - Make `tests/e2e.py` fail soft and report live: wrap each numbered stage in
     its own `try`/`except` that records a `FAIL` and continues; print the
     `N/M checks passed` summary from a `finally` block so it always appears;
     attach buffered console and `pageerror` output to the failing stage instead
     of holding it all until stage 13; and add a fixture mode that generates two
     short synthetic episodes so the whole suite runs inside a 64 MB `/tmp`.
     Each of the three aborted runs in this event would have produced a
     stage-by-stage verdict instead of a traceback. **This does not change
     anything about `live-trial-2026` — the `NE` stands for this event
     regardless — but it is what makes `reliability` scorable in the next one,
     and it would have settled the check-count question on its own.**
   - Make `downloadAll()` count successes and failures and report both.
     `setStatus(… "all downloaded")` currently runs unconditionally after the
     loop, including when `startDownload()` caught failures
     (`web/js/app.js:258-267`). A wrong-state message in the completion path of a
     primary workflow is worse than no message.
   - Add `worker.onerror` and `onmessageerror` plus a timeout to
     `web/js/storage.js:13-31,49-76`. A worker that dies without posting — which
     is what a crashed renderer looks like — currently leaves the row
     permanently `downloading`, and a hung download is indistinguishable from a
     slow one to both the user and the test suite.
   - Add unit tests under the range parser and the last-write-wins comparison.

3. **Longer-term opportunity — decouple rendering from playback, and close the
   remaining signal gaps.** Every `timeupdate` currently drives
   `refreshState().then(render)`, which clears and rebuilds the entire episode
   list and the transport bar while issuing two IndexedDB `getAll()` calls — at
   roughly four ticks a second, on a 56-row list, during the activity the app
   exists for. It discards keyboard focus and fights a seek-slider drag. A narrow
   `renderTime()` that writes the two time labels and the slider value, with
   `render()` reserved for library and download-state changes, fixes three
   problems with one wiring change. Alongside it: surface `transcode.failed` from
   `/api/rescan` in the UI instead of showing only `Indexed N episodes`, so a
   failed transcode is visible to the only person who would fix it; prune the
   client's IndexedDB `episodes` store so server-side deletions stop leaving
   permanent ghost rows; disable the Rescan button while a rescan is running; and
   give "Download all" a cancel and an aggregate progress indicator, along with a
   visible statement of the constraint you already recorded yourself — there is
   no Background Fetch API, so the app must stay foregrounded while downloading.

**Explicitly not on this list: "get the end-to-end suite to complete."** Three of
the four judges said independently that this was an operator action for this
event, not work you owed. Improvement 3's fixture mode is worth doing because it
makes the suite better, not because the suite is at fault for what happened here.

## Evidence appendix

Everything below is traceable to your submitted commit and to the pinned
evidence package that all four judges worked from.

| Evidence ID | Class | Observation |
|---|---|---|
| ev-podcast-02 | direct observation | Server boots; `/healthz`, `/api/library`, `/`, `/sw.js`, `/manifest.webmanifest` all `200` with correct content types and `service-worker-allowed: /`; no security headers on any response. |
| ev-podcast-03 | direct observation | Byte-range serving correct across six request shapes with exact byte counts; progress put/get/stale/newer/unknown all behave as specified. Verified on both images. |
| ev-podcast-05 | direct observation | Documentation figures against the checkout: 33 files / 1,360 MB and 28 files / 1,112 MB against 56 files / 2.2 GB. Its 43-`check()` figure is corrected to 42 by this dossier. |
| ev-podcast-06 | artifact | Full read of `tests/e2e.py`; the scope of the unexecuted behaviour. Its "11 stages" is corrected to 13 by this dossier. |
| ev-podcast-07 | artifact | Complete read of all four server modules and all client scripts: same-origin `fetch()` targets only; no model, API key, AI SDK or third-party HTTP client. |
| ev-podcast-09 | inference (negative) | `.agentic/project.yaml` is six inert metadata lines; no text anywhere in the checkout directs an evaluating agent. Independently re-derived by three judges, including a check for hidden-text techniques. |
| ev-podcast-10 | team claim | PWA install, screen-locked background audio, lock-screen MediaSession controls and real iOS quota. No container can settle these. |
| ev-podcast-12 | direct observation | Approved image carries ffmpeg/ffprobe 7.1.5; `/tmp` is a 64 MB tmpfs at container start. |
| ev-podcast-14 | direct observation | Startup indexing scans only what already exists in `MEDIA_DIR`; `POST /api/rescan` is the action that populates the library. |
| ev-podcast-15 | direct observation | One 18,631,917-byte source transcoded to 4,884,617 bytes and indexed with `duration_sec: 578.896009`; the suite reached stage 7 of 13; stage 5's recorded "failure" is a correct clamp-to-end; stage 6 passed all four checks; stage 7 stalled after `page.reload()`. |
| ev-podcast-16 | direct observation | Two-episode run: stage 1 4/5, stage 2 pass, stage 3 download wait timed out after 90 s during a measured 71-second overlap with another container at `--cpus 1.0`. The stage-1 date failure is fully explained by both fixture files sitting in `releases.json`'s `unresolved` block. |
| ev-podcast-17 | direct observation | Instrumented single-episode probe: download complete in 1 s, OPFS file byte-identical at 4,884,617 bytes, IndexedDB `state: "done"`, `storage.estimate()` consistent, zero console messages or page errors. |
| ev-podcast-18 | direct observation | `/tmp` is a 64 MB tmpfs in every run, with no override available; the 56-file, 2.2 GB library cannot fit. The cap is the framework's and was applied identically to every submission. |
| ev-podcast-19 | inference | Candidate explanation for the stage-7 stall: `hidePlayed` defaults on and the one completed episode is correctly hidden after reload, leaving zero `.ep` elements. Reasoning only; never confirmed against the post-reload DOM. |
| ev-podcast-20 | direct observation | Isolated repeat: did not reproduce the stall and failed differently and sooner — a Chromium `Target crashed` at stage 3, about 7 s in, after 17.3 s of transcoding. Three executions, three outcomes, none classified, no memory measurement taken. |
| ev-podcast-21 | direct observation | Image history confirms the two images differ only by the ffmpeg layer, so no observation depends on an image difference. |
| req-10 | confirmed | No prompt-injection or agent-directed instruction anywhere in the checkout. Independently corroborated by two judges. |
| adj:live-trial-2026:team-podcast:01 | adjudication | `reliability` is not resolvable from the pinned package; the `NE` stands, confirmed and not cleared; no score was overridden; the cause is the evidence package and the event's execution constraints, not the submission. |

A closing note. The evidence limits described throughout this dossier are the
event's, and the two confirmed defects are both quiet data-integrity problems in
code that nobody ever saw fail — which is a different and better position than
having a workflow break in front of a judge. Fix B1 first, then B2, then make
your suite report what it reaches. The engineering judgment on display in your
decision record is the part that is hardest to teach, and you already have it.
