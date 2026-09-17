---
event_id: live-trial-2026
team_id: team-podcast
commit: f3fdd342465fa6bc2a52d226a8613b082ad329e0
evidence_package_id: ev:live-trial-2026:team-podcast:f3fdd342465f:d06f90cc
rubric: submission-evaluation@1.0.0
consolidation_policy: panel-consolidation@1.0.0
persona: panel-consolidator@1.0.0
framework_commit: d11a97060965b1f68797ff42f6391ae08dede3c2
judge_run_ids:
- jr:live-trial-2026:team-podcast:judge-backend:d06f90cc:01
- jr:live-trial-2026:team-podcast:judge-frontend-ux:d06f90cc:01
- jr:live-trial-2026:team-podcast:judge-product-agentic:d06f90cc:01
- jr:live-trial-2026:team-podcast:judge-security-ops:d06f90cc:01
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-17T21:52:01Z"
completed_at: "2026-09-17T21:58:17Z"
total: null
display_total: null
finalized: false
blocked_reasons:
- "reliability: unresolved NE from judge-backend, judge-frontend-ux, judge-product-agentic, judge-security-ops"
adjudication_ids:
- adj:live-trial-2026:team-podcast:01
visibility: private
approval_state: draft
validation_state: unvalidated
---
# Consolidated Team Report — team-podcast

## Executive summary

**There is no official total for team-podcast and there will not be one in this
event.** All four judges returned `NE` on `reliability`
(`summaries/team-podcast.json`, `source_scores`), which blocks finalization under
the consolidation policy. The `NE` was adjudicated as
`adj:live-trial-2026:team-podcast:01` and the adjudication **accepted** it rather
than clearing it: `reliability` is not resolvable from the pinned evidence
package, and the event director declined to reopen the evidence stage.

The sum of the six scored criteria is **58.25 of 100
(`summaries/team-podcast.json`, `provisional_total`). That figure is not an
official total.** It omits a criterion worth 10 weight that carries no score at
all, and `NE` is not a zero. It must not be published, must not be used for
seeding, and must not be compared against any other team's total.

The reason for the `NE` is a limit of the evidence package and of the event's
sandbox constraints, not a defect traced to the submission. Three executions of
the submission's own suite against the same commit and the same image produced
three different outcomes and none was classified (`ev-podcast-15`,
`ev-podcast-16`, `ev-podcast-20`); every traced failure points away from the
submission — the server had already logged `GET /api/media/1 200 OK` before both
stage-3 failures, and the sandbox ran under `--memory 1g --cpus 1.0` with a
64 MB `/dev/shm` and a 64 MB tmpfs holding both the media and the browser profile
(`ev-podcast-12`, `ev-podcast-18`, `adj:live-trial-2026:team-podcast:01`). The
single run that would likely have made the criterion scorable — one suite
execution with `--shm-size` raised against a small library — is an operator
action, identified independently by three of the four judges, and it was refused
because re-running evidence after judging began would invalidate four judgments
that cite this package. **This is the framework's and the operator's failure, not
the team's, and the event report must say so in those terms**
(`adj:live-trial-2026:team-podcast:01`, "Human decision").

What the panel does agree on: every workflow that was executed produced exact,
correct output (`ev-podcast-03`, `ev-podcast-15`, `ev-podcast-17`,
`ev-podcast-20`), the decision record is unusually strong for this event
(`ev-podcast-09`), and roughly half the advertised product — the offline half the
team itself calls a hard requirement — was never executed by anyone
(`ev-podcast-06`). Two data-integrity defects found by source read, not by
execution, concern the only user data in the system that cannot be regenerated.

One criterion carries a genuine panel split. On `agentic` the judges scored
2/3/3/3 on identical, verified facts and disagreed about how to read the rubric,
not about what is true. It is reported below as an interpretation disagreement
and is not averaged away. It is logged as framework defect **D12**.

The consolidator is a neutral packager, not a fifth judge. No individual score
below was altered. This report carries two corrections the stage audit ordered,
in the section "Corrections carried by the panel"; the judgments themselves are
immutable and were not edited.

## Consolidated score

Every value in the block below is transcribed from
`events/live-trial-2026/summaries/team-podcast.json`, which `atj score` produced.
No arithmetic was performed by the consolidator. **The block must be regenerated
by `atj render consolidated` before `atj validate` runs against this file.**

<!-- atj:consolidated:begin -->
| Criterion | Judge scores | Mean | Weight | Points | Agreement |
|---|---|---:|---:|---:|---|
| functional | judge-backend=3.0, judge-frontend-ux=3.0, judge-product-agentic=3.0, judge-security-ops=3.0 | 3.00 | 25 | 15.00 | aligned |
| product | judge-backend=4.0, judge-frontend-ux=4.0, judge-product-agentic=4.0, judge-security-ops=3.0 | 3.75 | 15 | 11.25 | aligned |
| agentic | judge-backend=2.0, judge-frontend-ux=3.0, judge-product-agentic=3.0, judge-security-ops=3.0 | 2.75 | 15 | 8.25 | aligned |
| engineering | judge-backend=4.0, judge-frontend-ux=4.0, judge-product-agentic=4.0, judge-security-ops=3.0 | 3.75 | 15 | 11.25 | aligned |
| reliability | judge-backend=NE, judge-frontend-ux=NE, judge-product-agentic=NE, judge-security-ops=NE | — | 10 | — | not-scored |
| security | judge-backend=3.0, judge-frontend-ux=3.0, judge-product-agentic=3.0, judge-security-ops=3.0 | 3.00 | 10 | 6.00 | aligned |
| innovation | judge-backend=3.0, judge-frontend-ux=4.0, judge-product-agentic=3.0, judge-security-ops=3.0 | 3.25 | 10 | 6.50 | aligned |
| **Overall** |  |  | **100** | **not finalized** |  |

<!-- atj:consolidated:end -->

**Overall:** no official total. The score block above is the tool's own wording; `not finalized` there means exactly what this section states (audit C7). `total: null`, `display_total: null`,
`finalized: false` (`summaries/team-podcast.json`). The provisional sum of the six
scored criteria is 58.25; it is unofficial, unpublishable, and not a seeding
input.

**Overall confidence:** medium on the six scored criteria. `engineering` is the
best-supported criterion (three of four judges recorded `high`, all four from a
complete read of the pinned checkout). `functional`, `product`, `security` and
`innovation` are all `medium` across the panel, and the common reason is the
same: about half the advertised surface was never executed by anyone
(`ev-podcast-06`). On `reliability` the panel is unanimous and confident that the
criterion cannot be scored; see the note on confidence semantics under
"Unresolved questions".

No possible outliers were identified and no integrity problems were recorded
(`summaries/team-podcast.json`, `possible_outliers`, `integrity_problems`).

## Per-criterion consolidated view

### functional — 3.0 unanimous

All four judges scored 3 and reached it on the same evidence: the executed half
is exact, the unexecuted half is large, and nothing was confirmed to fail for a
reason inside the submission. Observed working: server boot and PWA asset serving
(`ev-podcast-02`, `ev-podcast-14`); byte-range serving across six request shapes
(`ev-podcast-03`); real ffmpeg transcode-index of an 18,631,917-byte source to
4,884,617 bytes with `duration_sec: 578.896009` (`ev-podcast-15`); progress
put/get/stale/newer (`ev-podcast-03`); library render, ordering, title-from-filename
and hide-played default in a live browser (`ev-podcast-20` stage 1); OPFS download
byte-exact in one second (`ev-podcast-17`).

Not observed by anyone: blob-URL playback, offline library render, offline
playback, filter persistence, autoplay-to-next, single and bulk delete, and the
suite's own JavaScript-error sweep (`ev-podcast-06`). All four judges noted that
`DECISIONS.md:15` calls offline playback a hard requirement.

No divergence in score. Two shared readings worth preserving: the stage-5 `[FAIL]`
("seek to 600s landed — 578.9s") is a correct clamp against a 578.896009 s fixture
and a test hardcoding 600 s, read the same way by every judge who addressed it
(`ev-podcast-15`); the stage-1 "0 of 2 dated" failure is fully explained by both
fixture files sitting in `releases.json`'s own `unresolved` block
(`ev-podcast-16`, `releases.json:259-261,289-291`). Neither is a defect.

### product — 3.75 (4/4/4/3)

Three judges placed this above solid for design judgment that is visible in the
code and matches its stated reasons: hide-played-by-default with the playing row
exempted (D19, `web/js/app.js:111-115`), autoplay restricted to already-downloaded
episodes so it cannot start a cellular fetch on a locked screen (D15,
`web/js/app.js:298-311`), three distinct empty states naming the control that
fixes each (`web/js/app.js:123-133`), and a status line covering loading, offline,
error and success. `judge-frontend-ux` added that the header surfaces
`storage.estimate()` usage, quota and persistence — the app instruments the one
question the team could not answer off-device (`web/js/app.js:313-320`).

`judge-security-ops` held at 3, weighting the same documentation drift more
heavily and noting that most of the interaction surface was never driven. The
divergence is weighting, not fact: all four cite `ev-podcast-05` for the same
contradictions, and all four note the UX half was unexecuted.

### agentic — 2.75 (2/3/3/3) — interpretation disagreement, framework defect D12

**The facts are not in dispute and are not close.** All four judges independently
read every server module and every client script at the pinned commit and found no
model, no API key, no AI SDK and no third-party fetch target; the only `fetch()`
targets are same-origin `/api/library`, `/api/progress/{id}`, `/api/rescan` and
`/api/media/{id}` (`ev-podcast-07`, corroborated at intake). `.agentic/project.yaml`
is six inert metadata lines (`ev-podcast-09`). Every sandbox run executed with
`--network none` and the app worked (`ev-podcast-02`, `ev-podcast-14`,
`ev-podcast-15`). `DECISIONS.md` Context records the source audio as NotebookLM
output, which is content provenance from before this app existed, not a runtime
dependency.

**The disagreement is about what that verified absence scores.**
`judge-backend` applied the partial anchor at 2: the useful element is a correct
scoping decision plus a provably clean runtime, and the important weakness is that
the subject of the criterion is absent. `judge-frontend-ux`, `judge-product-agentic`
and `judge-security-ops` applied the primary-expectations-met anchor at 3: the
criterion asks whether AI is appropriate, controlled, observable and effective, and
a verified, appropriate, documented absence answers the first two and leaves the
last two without a subject.

All four flagged this as a consolidation question rather than a private call.
`judge-backend`: "how this rubric should treat a submission that correctly declines
to use AI is a consolidation question, not a question this judge can settle alone".
`judge-product-agentic`: "I am flagging the interpretation explicitly so
consolidation can resolve it rather than average over it."
`judge-security-ops`: "A panel member who argues this criterion is not applicable
to this submission is making a reasonable argument, and I would not resist it in
consolidation." All four recorded that their uncertainty here is interpretive, not
evidentiary.

`atj score` bands this as `aligned` because the numeric range is 1.0 and
`aligned_max_range` is 1 (`framework/rubrics/panel-consolidation.md` front matter).
**The band understates it.** The band measures numeric spread; the disagreement is
about which anchor applies to a submission with no AI surface, and it would produce
a much wider spread under a different reading of the same anchors — as
`judge-product-agentic` observed, "a judge reading this criterion as requiring a
demonstrated AI system would score it much lower, and that reading is available
from the anchors". The consolidator does not resolve it, does not treat the mean as
a settlement, and records it as framework defect **D12**: the rubric does not state
how `agentic` is scored when a submission has no AI surface. Every judge asked for
that rule; none of them could supply it.

No score moves. The mean of 2.75 is the arithmetic the policy requires and is not
a panel finding that the submission is deficient on this axis.

### engineering — 3.75 (4/4/4/3)

The panel agrees on the facts and on the defect list; it splits on how much the
defects cost. Shared strengths: four server modules and five client modules with
one responsibility each, no build step where none is needed (P1), comments that
explain the non-obvious constraint at the point of the choice, 22 recorded
decisions and 8 recorded deviations from the original plan with reasons
(`ev-podcast-07`, `ev-podcast-09`). `judge-backend` called the P1-P8 deviation
table "the single most useful maintenance artifact in the checkout".

Shared defects, all found by source read and none by execution: the prune/cascade
data-loss path (`server/app.py:64`, `server/db.py:25,37,94-103`), episode identity
carried as a scan-order rowid across the network
(`web/js/opfs-worker.js:24`, `web/js/storage.js:92,103`, `web/js/idb.js:19-22`),
one module-level SQLite connection shared across the sync threadpool
(`server/app.py:25`, `server/db.py:33-39`), and no unit test anywhere.

`judge-security-ops` held at 3 because a data-destroying default path plus an
unstable primary key in a schema that already carries a stable natural key
(`filename`, `UNIQUE` at `server/db.py:13`) keeps this at solid. The other three
treated the same findings as what keeps it off the top band rather than what pulls
it below strong. This is severity weighting on an identical factual record and
needs no adjudication.

### reliability — `NE` from all four judges, adjudicated and accepted

Not scored, and not scorable in this event. Each judge reached `NE` independently
and each gave the same structural reason: on this package a low score and a high
score are both defensible from the same evidence, which is the condition `NE`
exists for.

What the package does establish and what should not be lost behind the `NE`:
`/healthz` reports liveness plus episode count (`server/app.py:210-213`,
`ev-podcast-02`); the systemd unit sets `Restart=on-failure`, `RestartSec=5` and a
transcode-aware `TimeoutStartSec` (`deploy/podcast-listener.service:27-31`) and
`README.md:239-251` lists the three conditions that must hold for
restart-after-reboot with a verification command for each;
`storage.reconcile()` reclassifies interrupted downloads and OS-evicted files at
startup (`web/js/storage.js:117-128`); dirty progress rows drain through
`flushQueue()` when connectivity returns (`web/js/player.js:71-75`), and the server
half of that was observed passing all four of its checks (`ev-podcast-15` stage 6).
The suite itself derives expected counts from the live `/api/library` payload
rather than hardcoding them (`tests/e2e.py:57-67`).

What blocks a score: the submission's reliability story is one suite, and no
execution of it has ever completed in this event. `ev-podcast-19` is reasoning, not
re-execution; the renderer crash has no memory measurement behind it
(`ev-podcast-20`); the team's own pass claim cannot be checked against anything
because no run reached the summary line at `tests/e2e.py:387`.

**State of the adjudication.** `adj:live-trial-2026:team-podcast:01` was decided by
the event-director, is approved, and **confirmed the `NE` rather than clearing
it**. `summaries/team-podcast.json` records the resolution object against
`reliability` with `resolved_score: null` and the note "adjudicated resolution
recorded alongside the source scores; no source score was modified", while the same
file still lists `reliability` under `adjudication_required` and `blocked_reasons`.
Both records describe one state: an adjudication was performed and accepted that
the criterion cannot be scored. No source score was overridden; `score_override` is
absent by design.

**Tooling contradiction, framework defect D11.** `atj score` prints a line saying
the adjudication was applied to `reliability` and then reports the same criterion
as an unresolved `NE`. Either line quoted alone misrepresents the state — the first
reads as though the `NE` was cleared, the second as though the adjudication never
happened. Neither may be quoted without the other, and the prose above is the
accurate description. Logged as **D11** for the framework, not against this team.

### security — 3.0 unanimous

All four judges scored 3 on a shared reading: the submitted code contains no
exploitable defect any of them could find, and the entire access-control model
lives outside the artifact. Confirmed clean: `ffmpeg`/`ffprobe` invoked as argument
lists with absolute paths and no shell, so a filename cannot become a command
(`server/media.py:28-34,57-69`); the media path resolved from a database row
populated only from basenames of a local glob, so there is no traversal surface
(`server/media.py:114`, `server/app.py:143-149`); every interpolated episode string
escaped (`web/js/app.js:161-170,237-240`); the service worker refusing to intercept
`/api/` and audio (`web/sw.js:39-57`); no credentials anywhere, `.env`, `certs/` and
`data/` gitignored; no telemetry, no analytics, no third-party egress
(`ev-podcast-07`). `judge-security-ops` grepped the tree for key, token, password
and PEM headers and found only prose inside an HTML planning document.

Held at 3 by all four for the same reason: the perimeter (`tailscale serve` plus a
firewalld rule) is documented prose that this package never observed, nothing was
penetration-tested (`req-05`), and there is no defence in depth behind one escaping
function. `judge-security-ops` added the sharpest version of the gap:
`run.sh:60-61` execs uvicorn with `--host 0.0.0.0` immediately after printing
`==> HTTP on http://127.0.0.1:8000`.

Two judges independently re-ran the prompt-injection check across the checkout,
including hidden-text techniques, and found nothing, corroborating
`ev-podcast-09`/`req-10`. Nothing to escalate.

### innovation — 3.25 (3/4/3/3)

Unanimous on the substance: the depth is real and it is platform-constraint
engineering, documented as researched against WebKit/MDN with dates rather than
recalled — OPFS written from a dedicated worker because Safari has no
`createWritable()` and `createSyncAccessHandle()` is worker-only (D3); audio routed
around the service worker because the Cache API answers `200` where `<audio>` needs
`206` (D4); autoplay continued on the same element from the `ended` handler because
iOS treats a new element as a fresh, blockable session (D16); completeness tracked
in IndexedDB because OPFS has no rename (P5).

`judge-frontend-ux` scored 4, weighting that chain plus the one directly observed
payoff — the OPFS write producing a byte-identical 4,884,617-byte file with a
matching `storage.estimate()` delta (`ev-podcast-17`). The other three held at 3
because the techniques are known ones applied well rather than new ground, and
because the paths with the highest ceiling — background audio under screen lock,
lock-screen MediaSession, offline playback — are exactly the ones with no execution
evidence (`ev-podcast-06`, `ev-podcast-10`). Weighting difference on an agreed
record; no adjudication needed.

## Corrections carried by the panel

The judgments are immutable, so the stage audit's two ordered corrections are
recorded here and apply to every downstream artifact.

### Correction 1 — the check-count claim (audit F1)

`tests/e2e.py` has **42 `check()` call sites, not 43.** The 43rd grep match is the
function definition `def check(` at `tests/e2e.py:33`. The team's "42/42" claim at
`README.md:285` and `DECISIONS.md:9` is therefore **consistent with the source**,
and the only stale figure in the submission is `README.md:7`'s "34/34".

The error originated in the evidence package: `ev-podcast-05` recorded 43 `check()`
call sites from `grep -c "check("` and concluded that neither team figure matched.
`judge-frontend-ux`, `judge-product-agentic` and `judge-security-ops` each carried
that figure forward, and `judge-product-agentic` escalated it to a **"Confirmed
defect"** attributed to "direct file inspection" — an attribution the underlying
evidence does not support, because the count came from the manifest, not from an
independent count of the calls.

`judge-backend` caught this independently during its own read and recorded the
correction in its report, with the discriminating counts:
`grep -c "check("` returns 43, `grep -c "^\s*check("` returns 42, and counting the
calls stage by stage gives 42.

**No score moves.** The documentation-drift finding survives — `README.md:7` is
still wrong against a 42-check suite — but it is half the size the package recorded,
and the team's principal claim is not an unverifiable one. This correction is
attributed to the stage audit and to `judge-backend`, and any team-facing or public
artifact must use 42.

### Correction 2 — internal inconsistency in judge-security-ops (audit F5)

`judge-security-ops` refers to the suite's unexecuted range as "sections 4 and 8
through 11" in its `innovation` improvement, while correctly writing "sections 4
and 8 through 13" under `functional`, in its confirmed-defects list and in its
untested-concerns list. Minor internal inconsistency in one sentence. It affects no
score, no finding and no evidence citation. Noted so that any downstream quotation
uses the correct range.

### Panel note — the suite is 13 stages, not 11

`ev-podcast-06` describes `tests/e2e.py` as 11 numbered stages, and the manifest
reports the furthest run as "stage 7 of 11". The file prints stage headers numbered
1 through 13 plus an "11b" (`tests/e2e.py:54,90,98,140,171,181,202,214,225,238,258,337,379`),
a discrepancy `judge-product-agentic` and `judge-security-ops` each identified
independently. **"Stage 7 of 11" overstates the coverage actually reached**: the
best run reached stage 7 of 13. This changes no observation; it changes how much
unexecuted surface remains, and it makes the coverage gap larger than the package
states. It is a correction to the evidence package, not a finding against the team.

## Confirmed strengths

Supported by direct observation or by a complete read of the pinned checkout. Where
several judges said the same thing about one observation, that is one corroborated
observation, not four independent confirmations.

- **Byte-range serving is correct on the cases hand-written range code usually gets
  wrong.** Full-file, mid-file, suffix (`bytes=-500`), open-ended, past-EOF `416`
  with `Content-Range: bytes */5000000`, and a malformed header rejected with `400`
  — with exact streamed byte counts, verified on both images (`ev-podcast-03`). All
  four judges credit this; it rests on one execution record, run twice.
- **The real transcode-index-serve pipeline works end to end on real team audio.**
  One 18,631,917-byte source to 4,884,617 bytes with a correct duration and a
  title derived from the filename (`ev-podcast-15`).
- **The OPFS download path is clean and fast when it runs.** One second,
  byte-identical to the transcoded output, IndexedDB `state: "done"` with a matching
  byte count, `storage.estimate()` moving from ~132 KB to ~5.0 MB, zero console
  messages or page errors across the session (`ev-podcast-17`).
- **Progress persistence behaves as claimed.** Last-write-wins applies, a stale
  write is rejected without clobbering, a newer write is accepted (`ev-podcast-03`);
  stage 6 passed all four of its checks including "synced to server, not dirty"
  (`ev-podcast-15`).
- **Library presentation was observed correct in a live browser.** Row count
  matching the unplayed count, title from filename, hide-played pressed by default,
  newest-first ordering (`ev-podcast-20` stage 1, twice).
- **The decision record is the strongest artifact in the checkout.** 22 decisions
  with rationale and 8 recorded deviations from the original plan with reasons, and
  the code matches the stated reasons at every point the judges checked
  (`ev-podcast-09`, `ev-podcast-07`).
- **The no-AI boundary is verified rather than asserted.** No model, key, SDK or
  third-party fetch target in any server module or client script; same-origin
  targets only; every run executed with `--network none` (`ev-podcast-07`,
  `ev-podcast-09`).
- **Injection surfaces are handled at the point of risk.** `escapeHtml` at every
  interpolation site, subprocess calls as argument lists with no shell, media path
  never built from request input (`ev-podcast-07`).
- **Operational honesty.** `README.md:239-251` lists the three independent
  conditions that must hold for restart-after-reboot, with a verification command
  for each, and the team marks two of its own iPhone claims unverified on the device
  it owns (`ev-podcast-10`).
- **The refusal to fuzzy-match.** After duration matching produced two confident
  false pairs 0.4 s apart, the team chose an exact-filename join that fails loudly
  into an `unresolved` list with typed reasons (D21,
  `scripts/sync-releases.py:95-102`, `releases.json:259-261,289-291`).
  `judge-product-agentic` called it the most agentic-relevant judgment in the
  submission.

## Confirmed weaknesses

Defects the panel can establish from the pinned commit. Each is marked by how it
was established. Nothing in this list was observed failing at runtime; the
submission was never observed failing for a reason inside its own code.

- **W1 — Deleting `data/media/` destroys all listening progress.** `index_library()`
  calls `prune_missing()` on every startup and rescan (`server/app.py:64,70-76`);
  with an empty scan that function issues a bare `DELETE FROM episodes`
  (`server/db.py:94-103`); `progress` cascades (`server/db.py:25`) with
  `PRAGMA foreign_keys = ON` (`server/db.py:37`); and `README.md:53` plus
  `server/config.py:24-25` tell the operator that directory is safe to delete
  because "a rescan rebuilds both". A rescan does not rebuild progress. Source read,
  not executed. **Classification note:** `judge-backend` (C1) and
  `judge-security-ops` (F1) class this a confirmed defect; `judge-product-agentic`
  classes the same finding a risk because it was never executed. The panel records
  it as confirmed-by-source-read with the execution status stated, which is what all
  three descriptions actually support.
- **W2 — Episode identity is a scan-order rowid used as a durable cross-device
  key.** OPFS files are named `${episodeId}.m4a` (`web/js/opfs-worker.js:24`, read
  back at `web/js/storage.js:92,103`) and IndexedDB progress is keyed the same way
  (`web/js/idb.js:19-22`), while `id` is a plain `INTEGER PRIMARY KEY`
  (`server/db.py:12`) reassigned in filename-sort order on re-index
  (`server/media.py:114`). `filename` is already `NOT NULL UNIQUE`
  (`server/db.py:13`) and would serve. The team wrote the rule down correctly at
  `DECISIONS.md:138` and applied it to the component it did not build. The library
  contains 15 renamed or superseded takes (`ev-podcast-16`, `releases.json`
  "unresolved"), so the rename case is not hypothetical. Source read.
- **W3 — Documentation misstates the artifact in three places.** 33 files /
  1,360 MB (`README.md:10`) and 28 files / 1,112 MB (`DECISIONS.md:16`) against
  56 files / 2.2 GB in the checkout, corroborated by `releases.json`'s 41 dated +
  15 unresolved (`ev-podcast-05`); and "34/34 automated checks pass"
  (`README.md:7`) against a 42-check suite (see Correction 1). In a file that opens
  by declaring itself the source of truth (`DECISIONS.md:3-5`), stale numbers cost
  the reader trust in everything else.
- **W4 — The bind address contradicts the documented perimeter.** `run.sh:61` execs
  uvicorn with `--host 0.0.0.0` after `run.sh:60` prints
  `==> HTTP on http://127.0.0.1:8000`; the `--https` branch does the same on 8443
  (`run.sh:55-57`). The application listens on every interface and tells the
  operator it does not. Source read; every sandbox run bound `127.0.0.1`
  (`ev-podcast-02`), so the exposed configuration was never exercised and the
  consequence is inference.
- **W5 — The OPFS download path has no failure detection.**
  `web/js/storage.js:13-31` registers only `worker.onmessage` — no `onerror`, no
  `onmessageerror` — and the promise at `web/js/storage.js:49-76` has no timeout. A
  worker that dies without posting, which is what a crashed renderer looks like,
  leaves the row permanently `downloading`. A hung download is indistinguishable
  from a slow one, to the user and to the test suite, in exactly the place two of
  the three inconclusive runs died. Source read.
- **W6 — The test suite is all-or-nothing and reports nothing when it aborts.**
  Every `wait_for_selector`/`wait_for_function` raises and terminates the process,
  so one stall discards every check after it; console and page errors are buffered
  and reported only at stage 13, which no run has reached; the `N/M checks passed`
  summary at `tests/e2e.py:387` never printed in any of the three runs
  (`ev-podcast-15`, `ev-podcast-16`, `ev-podcast-20`).
- **W7 — No unit tests exist.** `tests/` contains `e2e.py` and `requirements.txt`.
  There is no test for the range parser the team deliberately hand-wrote (P2,
  `server/app.py:132-205`) and none for the stale-write comparison
  (`server/db.py:153-167`). The only test of the range code in existence is the one
  the event's preparer wrote (`ev-podcast-03`).
- **W8 — `downloadAll()` reports success after failures.**
  `setStatus(… "all downloaded")` runs unconditionally after the loop, including
  when `startDownload()` caught failures (`web/js/app.js:258-267`). A wrong-state
  message in the completion path of a primary workflow.
- **W9 — Every `timeupdate` rebuilds the entire UI.** The handler
  (`web/js/player.js:226-229`) drives `refreshState().then(render)`
  (`web/js/app.js:333`), and `render()` clears and rebuilds the whole episode list
  plus the transport bar (`web/js/app.js:105-235`) while `refreshState()` issues two
  IndexedDB `getAll()` calls (`web/js/app.js:93-96`). At roughly four ticks a second
  on a 56-row list that discards keyboard focus and interrupts a seek-slider drag
  during playback — the activity the app exists for. Not caught by `tests/e2e.py`,
  which re-queries selectors on every assertion. Source read.
- **W10 — Accessibility gaps in an otherwise careful feedback layer.** `#status` is
  an ordinary `<p>` with no `role="status"` and no `aria-live`, so every message the
  app produces is silent to a screen reader (`web/index.html:108`); row and
  transport controls are named only by emoji or box-drawing glyphs, with `title` on
  two of three states (`web/js/app.js:172-187,206-217`); the currently-playing row
  is distinguished by border colour alone (`web/index.html:56`).
- **W11 — Signals are dropped at the UI boundary.** `/api/rescan` returns
  `transcode.failed` (`server/app.py:96-97`) and the UI displays only
  `Indexed ${data.indexed} episodes` (`web/js/app.js:368`), so a failed transcode is
  invisible to the only person who would fix it. Relatedly, the client's IndexedDB
  `episodes` store is written with `putAll` and never pruned
  (`web/js/app.js:58`), so server-side deletions leave permanent ghost rows in the
  offline library.

## Risks — credible, not confirmed

- **R1 — Unauthenticated, cross-site-triggerable `/api/rescan` with eightfold
  amplification.** `server/app.py:93-97` drives `transcode_all()` across
  `ThreadPoolExecutor(max_workers=8)` (`server/media.py:80-89`); a simple
  cross-origin `POST` needs no preflight; two concurrent rescans share a `.part`
  path with no guard (`server/media.py:55`). Compute exhaustion on a host
  `README.md:266-267` says also serves an unrelated application. No data impact.
  Inference from source; never tested.
- **R2 — One module-level SQLite connection with `check_same_thread=False` shared
  across the sync threadpool,** with a non-atomic read-then-write in `put_progress`
  (`server/app.py:25`, `server/db.py:33-39,153-167`). Correct at one writer, which
  is D7's premise; not written down as a hard constraint anywhere.
- **R3 — Last-write-wins compares ISO timestamps as strings**
  (`server/db.py:154`). The shipped client always sends `Z`-suffixed values, but the
  server's own fallback writes `+00:00` (`server/app.py:113`) and any client sending
  a non-UTC offset would compare wrong. Latent, not reachable from the submitted
  client, never tested in either format-mixing direction.
- **R4 — A ten-year local root CA trusted on a personal phone.**
  `gen-cert.sh:44-49` mints a 3650-day CA and `README.md:141` walks the user through
  trusting it on iOS; the key then sits on the app host for a decade. Mitigated by
  `chmod 600` (`gen-cert.sh:62`), a gitignored `certs/`, and a production path that
  uses Tailscale's real certificates with the CA "retained but unused" (P7).
- **R5 — "Download all" is serial over the whole library with no cancel, no
  aggregate progress, and no surface for the constraint the team recorded itself**
  ("No Background Fetch API — the app must be foregrounded while downloading",
  `ev-podcast-09`). Untested at scale; the largest library any run exercised was two
  episodes. The Rescan button is likewise never disabled while a rescan runs
  (`web/js/app.js:363-373`).
- **R6 — No security headers and no CSP** on any captured response
  (`ev-podcast-02` run record), so the XSS mitigation rests entirely on `escapeHtml`
  being applied at every future interpolation site. `judge-security-ops` records
  this as ordinary production hardening outside the event's scope and does not weigh
  it; `judge-frontend-ux` and `judge-backend` name it as a missing defence in depth.
- **R7 — No hardening directives on the systemd unit** — no `NoNewPrivileges`,
  `ProtectSystem`, `ProtectHome` or `PrivateTmp`
  (`deploy/podcast-listener.service:23-31`).
- **R8 — A committed dashboard lists unpublished post titles with future publish
  dates** (`artifacts/html/dashboards/podcast-coverage.html:225-235`). Whether the
  source repository is public is not established anywhere in this package;
  `judge-backend` recorded repository visibility as `NE` rather than scoring it.
- **R9 — The three unclassified suite outcomes themselves.** Candidate causes
  include the 64 MB `/dev/shm` with no `--shm-size`, the 64 MB tmpfs holding both
  media and the Chromium profile under `HOME=/tmp` (`ev-podcast-12`,
  `ev-podcast-18`), the `--memory 1g --cpus 1.0` cap, a measured 71-second overlap
  with a concurrent container (`ev-podcast-16`), and W5's missing failure detection
  — which pulls in the opposite direction from the environmental readings. Nothing
  in the package separates them.

## Untested concerns

- **Stages 4 and 8 through 13 of `tests/e2e.py` have never run in this event**
  (`ev-podcast-06`): blob-URL playback, offline library render, offline playback,
  filter persistence across reload, autoplay into the next downloaded episode,
  single and bulk delete, and the suite's own JavaScript-error sweep. Offline
  playback is the requirement `DECISIONS.md:15` calls hard and the one the whole
  architecture exists to satisfy. These are unobserved, not failed.
- **Every iPhone-specific claim** — install to home screen, background audio under
  screen lock, lock-screen MediaSession controls, real iOS quota and `persist()` —
  rests on the team's own account and cannot be settled by any container
  (`ev-podcast-10`). The team marks two of them unverified itself.
- **Behavior at real library size.** The full 56-file, 2.2 GB library was never
  exercised because `/tmp` is a 64 MB tmpfs (`ev-podcast-18`). Every observation
  about ordering, rendering, download and filtering rests on a one- or two-episode
  fixture. `judge-frontend-ux` notes that the evidence gap is currently a property
  of the test fixture, not of the app.
- **Nothing adversarial was attempted by anyone.** No penetration testing
  (`req-05`); the perimeter, the firewall rule and `tailscale serve` were never
  observed.
- **No human ever completed a download-listen-offline cycle** in this package, and
  no screenshot or rendered-UI artifact exists.

## Surprises

**Better than expected.**

- The hand-written range parser is correct where hand-rolled range code usually
  fails — suffix form and the `416` `Content-Range` header (`ev-podcast-03`). Named
  independently by all four judges.
- `DECISIONS.md`'s P1-P8 deviation table records where the implementation departed
  from the plan and why, including the ffmpeg `-f ipod` flag needed because the temp
  file ends in `.part` (P3). A maintenance artifact, not marketing.
- `storage.reconcile()` distinguishes the two failures that actually happen on a
  phone — a download killed mid-write, and a file evicted by iOS under storage
  pressure (`web/js/storage.js:117-128`).
- `aria-pressed` correctly maintained on both filter toggles through one
  `syncFilterBtns()` and persisted, with the pressed default verified in the live
  DOM (`ev-podcast-16` stage 1). Most prototypes at this level style a class and
  stop.
- The instrumented download probe was completely clean — one second, byte-exact,
  zero console output (`ev-podcast-17`) — which decisively contradicts any "the
  download is broken" reading of `ev-podcast-16`.

**Worse than expected.**

- The app handles the empty-library case better than its own test does. `render()`
  explains why the list is empty and names the control that fixes it
  (`web/js/app.js:123-133`) — and that correct behavior is the most plausible cause
  of the stage-7 stall (`ev-podcast-19`).
- Zero unit tests in a project whose author deliberately hand-wrote the riskiest
  code path (P2) on the grounds that a framework difference "would be miserable to
  debug on a phone".
- `DECISIONS.md:138` states the correct identity rule and applies it to the
  component that was not built.
- `server/config.py:24-25` labels the directory holding the only irreplaceable user
  data as safe to delete, and the startup path makes that label actively dangerous.
- The test suite never produced a summary line in any of three runs.

## Material disagreements

**`agentic` — interpretation disagreement, unresolved by design.** 2/3/3/3 on
identical, unanimously verified facts: a complete, confirmed absence of any AI in
the running application (`ev-podcast-07`, `ev-podcast-09`). The split is about
which rubric anchor applies when the subject of a criterion is absent by a correct
and documented engineering decision. The deterministic band reads `aligned` on a
range of 1.0; the band measures numeric spread and does not capture this. The
consolidator does not resolve it and does not present the 2.75 mean as a
settlement. Cause: **rubric ambiguity**, not evidence selection, persona emphasis
or factual error. Resolution status: **open**, logged as framework defect **D12**,
referred to the event director with all four judges' explicit request for a rule.

**`product` and `engineering` — severity weighting, explained, no adjudication.**
`judge-security-ops` sits one point below the other three on both, from the same
factual record. On `product` it weights documentation that misstates the current
state of the library and the fact that most of the interaction surface was never
driven. On `engineering` it weights the data-destroying default path (W1) plus the
unstable primary key (W2) as keeping the submission at solid, where the other three
treat them as what keeps it off the top band. Both ranges are inside
`aligned_max_range`. Cause: **persona emphasis**. No adjudication required.

**`innovation` — evidence weighting, no adjudication.** `judge-frontend-ux` at 4
against three at 3, over how much credit the unexecuted iOS payoff can carry. Cause:
**missing evidence**, which every judge named and weighed differently. Inside the
aligned band.

**Classification disagreement on W1.** Two judges class the prune/cascade path a
confirmed defect and one classes it a risk, because it was established by source
read and never executed. This is a real difference in evidence standard, not in
fact, and it is preserved above rather than resolved: the finding is recorded with
its provenance stated.

**One factual error, corrected, not a disagreement.** Three judges carried the
manifest's 43-`check()` figure and one caught it. See Correction 1. The correction
is attributed and no score moves.

**No severe disagreement exists.** No criterion exceeds `material_max_range`, and
`atj score` identified no possible outliers.

## Prioritized improvements

Ranked by what they prevent, not by effort. Two of the four judges named the
first item as the single most valuable change.

1. **Stop an indexing pass from destroying listening history, and stop telling the
   operator to trigger it.** Make `prune_missing` a no-op when handed an empty
   record list rather than issuing `DELETE FROM episodes`
   (`server/db.py:94-103`), and correct `README.md:53` and
   `server/config.py:24-25` so they say `data/media/` is derived and rebuildable
   while `data/app.db` holds the only data that is not. Progress is the one thing
   this application cannot regenerate — audio, durations, titles and release dates
   all rebuild from a rescan — and today a documented, recommended cleanup wipes it
   with no prompt, no backup and no log line naming what was lost.
2. **Give an episode an identity that survives a re-index.** Key `progress` and the
   OPFS filename on `filename`, which is already `NOT NULL UNIQUE`
   (`server/db.py:13`), instead of the scan-order rowid. Until this changes, a phone
   holding downloaded audio and a re-indexed server can disagree about which episode
   is which and neither side can notice — and the library already contains 15
   renamed or superseded takes (`ev-podcast-16`).
3. **Make `tests/e2e.py` fail soft, report live, and fit a small environment.** Wrap
   each numbered stage in its own `try`/`except` that records a `FAIL` and
   continues; print the `N/M checks passed` summary from a `finally` block so it
   always appears; attach buffered console and `pageerror` output to the failing
   stage rather than to stage 13; and add a fixture mode that generates two short
   synthetic episodes so the whole suite runs inside a 64 MB tmpfs. Each of the
   three aborted runs would have yielded a stage-by-stage verdict instead of a
   traceback, and the real check count would settle the documentation drift.
   **This does not unblock this event** — the `NE` stands for `live-trial-2026`
   regardless — but it is what makes `reliability` scorable in the next one.
4. **Decouple rendering from `timeupdate`** (W9). A narrow `renderTime()` that
   writes the two time labels and the slider `value`, with
   `render()`/`refreshState()` reserved for library, download-state and
   progress-state changes. One wiring change fixes three problems: keyboard focus
   and pointer drags survive playback, the seek slider stops fighting the user, and
   a 56-row list stops rebuilding its DOM and reading two IndexedDB tables several
   times a second.
5. **Close the two cheap honesty gaps.** Make `downloadAll()` count successes and
   failures and report both (W8), and add `worker.onerror` plus a timeout to
   `web/js/storage.js` so a dead worker becomes a reported error instead of a
   permanent "downloading" state (W5). Add unit tests under the two pieces of logic
   that were deliberately hand-written because they are risky — the range parser and
   the last-write-wins comparison — so reliability does not depend entirely on a
   browser being healthy (W7). Default the bind to `127.0.0.1` and require an
   explicit flag to widen it, so the safe configuration is the one you get by
   accident (W4).

**Explicitly not recommended to the team:** "get the e2e suite to complete." Every
traced failure points at the sandbox, and one run with `--shm-size` raised against a
small library would settle it. Three judges identified that independently as an
operator action for this event, not work the team owes.

## Unresolved questions and adjudication

**Attached adjudication:** `adj:live-trial-2026:team-podcast:01` —
`reliability`, trigger `unresolved-ne`, decided by the **event-director**,
approved, resolution `resolved`, `resolved_score: null`. It **accepted** the `NE`;
it did not clear it. Recorded consequence, in the adjudication's own terms:
team-podcast completes `live-trial-2026` without an official total for a reason
that is the framework's and the operator's, not the team's.

Open items, in order of what they block.

1. **Finalization is permanently blocked for this event.** `total` and
   `display_total` are `null` and `finalized` is `false`. The provisional 58.25 is
   not a total and must not reach a bracket, a seed, a team-facing report or a
   public artifact. Bracket assignment is unaffected — two eligible teams,
   `min_teams: 2`, one matchup, no byes, so no bye seeding reads a total — and the
   head-to-head compares the seven criteria directly. `reliability` in that matchup
   is expected to land on comparison value `0` ("substantially equal or insufficient
   comparative evidence"), but that is the matchup panel's finding to make on the
   common evidence, not this report's to impose.
2. **D11 — `atj score` reports the adjudicated `NE` two contradictory ways.** One
   line says the adjudication was applied to `reliability`; another reports the same
   criterion as an unresolved `NE`. Both describe one true state, and neither line
   may be quoted alone. Needs a tooling fix so the output distinguishes "adjudicated
   and resolved to a score" from "adjudicated and confirmed unscorable". Referred to
   the event director.
3. **D12 — the rubric does not say how `agentic` is scored when a submission has no
   AI surface.** All four judges raised it; none could settle it; the panel split
   2/3/3/3 on it. Until the rubric answers, this criterion is not comparable across
   submissions that do and do not use AI. Referred to the event director. Any fix is
   a new rubric version, not an edit to `submission-evaluation@1.0.0`, which is
   frozen for this event.
4. **Confidence semantics for `NE` are ambiguous and the panel used the field two
   ways.** Three judges recorded `confidence: low` on `reliability`, meaning low
   confidence in any numeric score; `judge-security-ops` recorded `high`, meaning
   high confidence in the `NE` determination itself. Every judge's prose says the
   same thing, so no judgment is wrong — but the field cannot mean both. The schema
   and template need a rule. Raised for the event director; no defect ID assigned
   here.
5. **Repository visibility is `NE` within this package.** A committed dashboard
   lists unpublished post titles with future publish dates
   (`artifacts/html/dashboards/podcast-coverage.html:225-235`). Whether the source
   repository is public is not established anywhere in the evidence, so
   `judge-backend` recorded it as a risk rather than a finding. It cannot be settled
   from the pinned package.
6. **Model identity is asserted, not attested, for all four judge runs.**
   `judge-backend` records `model.verified: false` and states plainly that it has no
   means of attesting its own model identity from inside the run; the other three
   record `verified: true` on the runtime's self-report plus the orchestrator's
   dispatch record. All four requested and used `claude-opus-5`. This is not a
   blocker and not a disagreement, but the panel should not describe any of the four
   as externally verified.
7. **Publication.** This artifact is `private` and `draft`. `atj validate
   publication` must run before anything derived from it leaves the panel, and any
   team-facing or public derivative must carry the 42-check correction, must not
   contain 58.25, and must state the reason for the missing total in the
   adjudication's terms.

## Evidence index

| Evidence ID | Class | Observation |
|---|---|---|
| ev-podcast-02 | direct-observation | Server boots; `/healthz`, `/api/library`, `/`, `/sw.js`, `/manifest.webmanifest` all `200` with correct content types and `service-worker-allowed: /`; no security headers on any response. |
| ev-podcast-03 | direct-observation | Byte-range serving correct across six request shapes with exact byte counts; progress put/get/stale/newer/unknown all behave as specified. Verified on both images. |
| ev-podcast-05 | direct-observation (file inspection) | `README.md:10` 33 files / 1,360 MB and `DECISIONS.md:16` 28 files / 1,112 MB against 56 files / 2.2 GB in the checkout; `README.md:7` "34/34" against `README.md:285`/`DECISIONS.md:9` "42/42". **Its 43-`check()`-site figure is corrected to 42 by this report (Correction 1).** |
| ev-podcast-06 | artifact | Full read of `tests/e2e.py`; scope of the unexecuted behavior — blob playback, offline render, offline playback, filters, autoplay, deletion, JS-error sweep. **Its "11 stages" is corrected to 13 plus an "11b" by this report.** |
| ev-podcast-07 | artifact | Complete read of all four server modules and all six client scripts: same-origin `fetch()` targets only; no model, API key, AI SDK or third-party HTTP client; D11 records the tailnet as the perimeter. |
| ev-podcast-08 | team-claim (disclosure) | A guessed-slug exposure disclosed for a proposed, unbuilt Cloudflare listener with an explicit accept-the-risk decision. No counterpart in this checkout; not scored against the submission. |
| ev-podcast-09 | evaluator-inference (negative) | `.agentic/project.yaml` is six inert metadata lines; no text anywhere in the checkout directs an evaluating agent. Independently re-derived by three judges, including a check for hidden-text techniques. |
| ev-podcast-10 | team-claim | PWA install, screen-locked background audio, lock-screen MediaSession controls and real iOS quota are team claims; the team marks two of them unverified itself. No container can settle them. |
| ev-podcast-11 | direct-observation | `bash run.sh` fails under the sandbox's read-only mount (`.venv` creation). Mount policy, not a submission defect. |
| ev-podcast-12 | direct-observation | Approved image `podcast:3` carries ffmpeg/ffprobe 7.1.5; `/tmp` is a 64 MB tmpfs at container start. |
| ev-podcast-13 | direct-observation | A missing `PODCAST_DB_PATH` crashed the server at import. Operator configuration error, not a submission defect. |
| ev-podcast-14 | direct-observation | Startup indexing scans only what already exists in `MEDIA_DIR`; it does not transcode. `POST /api/rescan` is the action that populates the library. |
| ev-podcast-15 | direct-observation | One real 18,631,917-byte source transcoded to 4,884,617 bytes and indexed with `duration_sec: 578.896009`; `tests/e2e.py` reached stage 7 (of 13), stage 5 recorded a clamp-to-end "failure", stage 6 passed all four checks, stage 7 stalled after `page.reload()`. Stdout piped through `tail -34`, so stages 1-4 have no preserved per-check output. |
| ev-podcast-16 | direct-observation | Two-episode run: stage 1 4/5, stage 2 pass, stage 3 download wait timed out after 90 s during a measured 71-second overlap with another container at `--cpus 1.0`. The stage-1 date failure is fully explained by both fixture files sitting in `releases.json`'s `unresolved` block. |
| ev-podcast-17 | direct-observation | Instrumented single-episode probe: download complete in 1 s, OPFS file byte-identical (4,884,617 bytes), IndexedDB `state: "done"`, `storage.estimate()` consistent, zero console messages or page errors. |
| ev-podcast-18 | direct-observation | `/tmp` is a 64 MB tmpfs in every run (`atj/sandbox.py` `DEFAULT_LIMITS`), with no CLI override. The 56-file, 2.2 GB library cannot fit; the cap is the framework's, applied identically to every submission. |
| ev-podcast-19 | evaluator-inference | Candidate explanation for the stage-7 stall: `hidePlayed` defaults on and the one completed episode is correctly hidden after reload, leaving zero `.ep` elements. Reasoning only; never re-executed or confirmed against the post-reload DOM. |
| ev-podcast-20 | direct-observation | Isolated repeat: did not reproduce the stall and failed differently and sooner — Chromium `Target crashed` at stage 3, ~7 s into the suite after 17.3 s of transcoding. Three executions, three outcomes, none classified, no memory measurement taken. |
| ev-podcast-21 | direct-observation | `podman history` confirms the two images differ only by the ffmpeg apt layer, so no observation depends on an image difference. |
| req-05 | team-claim | No authentication by design, tailnet as perimeter. Corroborated by source read; never penetration-tested. |
| req-06 | team-claim | Source audio is NotebookLM output — content provenance predating the app, not a runtime dependency. |
| req-07, req-08 | team-claim (contradicted) | Check-count and library-size claims. See `ev-podcast-05` and Correction 1. |
| req-10 | confirmed | No prompt-injection or agent-directed instruction in the checkout. Independently corroborated by two judges. |
| adj:live-trial-2026:team-podcast:01 | adjudication | `reliability` is not resolvable from the pinned package; the `NE` stands, confirmed and not cleared; no score overridden; the cause is the evidence package and the event's execution constraints, not the submission. |

## Calculation audit

- [x] Four valid independent reports — `judge_count: 4`, four unique
      `judge_run_id`s, above `minimum_panel: 2`. Each report carries an explicit
      independence declaration, and no judge read another judge's material.
- [x] Identity and versions agree — all four judgments and this report carry
      `event_id: live-trial-2026`, `team_id: team-podcast`,
      `commit: f3fdd342465fa6bc2a52d226a8613b082ad329e0`,
      `evidence_package_id: ev:live-trial-2026:team-podcast:f3fdd342465f:d06f90cc`
      and `rubric: submission-evaluation@1.0.0`, which is what the consolidation
      policy requires. `framework_commit` differs by artifact by design: the four
      judgments record `3da42c51…`, the adjudication `01f559fa…`, and this report
      `d11a9706…`, each being the framework commit at its own run time.
- [x] Deterministic calculations attached — `events/live-trial-2026/summaries/team-podcast.json`,
      produced by `atj score`. The consolidator performed no arithmetic; every
      number in this report is transcribed from that file or cited from an
      evidence artifact. `integrity_problems` is empty.
- [ ] No unresolved `NE` — **fails.** `reliability` is `NE` from all four judges.
      It was adjudicated and accepted, not cleared, so it remains unresolved for
      scoring purposes and blocks the official total permanently for this event.
- [x] Required adjudication complete — `adj:live-trial-2026:team-podcast:01`,
      approved, decided by the event-director, with the human decision recorded
      where policy requires one.

Consequences of the unchecked box: `finalized: false`, `total: null`,
`display_total: null`, and `blocked_reasons` carries the `reliability` entry. This
report is `private` and `draft`. Run `atj render consolidated` to regenerate the
score block, then `atj validate` and `atj validate publication` before any
derivative artifact leaves the panel.
