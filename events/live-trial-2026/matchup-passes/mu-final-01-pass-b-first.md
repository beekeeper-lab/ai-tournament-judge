---
event_id: live-trial-2026
match_id: mu:live-trial-2026:final:01
round_id: final
team_a: team-podcast
team_b: team-ledger
commit_a: f3fdd342465fa6bc2a52d226a8613b082ad329e0
commit_b: 9d21b7707f204ef60f5a1cee612f1d4db0a4a575
evidence_package_a: ev:live-trial-2026:team-podcast:f3fdd342465f:d06f90cc
evidence_package_b: ev:live-trial-2026:team-ledger:9d21b7707f20:b859a240
rubric: head-to-head@1.0.0
source_rubric: submission-evaluation@1.0.0
persona: matchup-judge@1.0.0
framework_commit: 1e761e639141d099f975cd6b4e3efaa296e6602f
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: 2026-09-17T23:20:00Z
completed_at: 2026-09-17T23:20:00Z
close_call_band: 5
presentation_order: b-first
passes:
  a_first:
    presented_first: team-podcast
    comparisons: {}
  b_first:
    presented_first: team-podcast
    comparisons: {functional: -1, product: 0, agentic: -1, engineering: -1, reliability: 0, security: -1, innovation: -1}
combined_margin: null
order_disagreement: false
outcome: adjudication-required
winner: null
adjudication_id: null
visibility: private
approval_state: draft
validation_state: unvalidated
---

# Matchup Report

## Orientation

This is one of two order-balanced passes. In this pass **team-podcast was presented
first and team-ledger second**, and the comparison values below are oriented
**positive = team-podcast, negative = team-ledger**, as directed by the event
orchestrator. The `presentation_order: b-first` field records this pass's position
in the bracket's canonical A/B orientation; it does not describe the order in which
the two submissions were read here. I did not see, seek, or infer the other pass's
work, and I do not advance the bracket. `atj matchup` computes all margins and
resolves the outcome.

## Eligibility and common evidence

Both submissions are eligible and comparable. Both were materialized by `atj intake`
from a cloned repository at an immutable commit, both evidence packages carry
`approval_state: approved` and `validation_state: valid`, both were prepared by
`prepare-submission@1.1.0` at framework commit `152dd2c10547a1c15bb56c4b1a90764b28354c59`
against `submission-evaluation@1.0.0`, and both were judged by the same four personas.

Both packages carry `execution_status: sandboxed-partial`. Every execution on both
sides ran through `python3 -m atj sandbox run` under `podman 6.1.0 (rootless)` with
`--network none`, a read-only source mount, a non-root user, and identical CPU,
memory, pid and tmpfs caps. Nothing was run on the host for either team.

**The packages differ in what was executable, and that difference was created by the
event, not by the teams.** team-ledger's own test suite ran to completion — 35 passed,
exit 0, offline, 0.07s (`ev-ledger-12`). team-podcast's never completed a run: three
executions of `tests/e2e.py` against the same commit and the same image produced three
different outcomes, none classified (`ev-podcast-15`, `ev-podcast-16`, `ev-podcast-20`).
The framework's `DEFAULT_LIMITS` set `/tmp` to a 64 MB tmpfs with no CLI override
(`ev-podcast-18`), which cannot hold the 56-file, 2.2 GB source library (`ev-podcast-05`)
and which also held the Chromium profile under `HOME=/tmp`; no podman invocation set
`--shm-size`, so Chromium ran against a 64 MB `/dev/shm` under `--memory 1g --cpus 1.0`
(`adj:live-trial-2026:team-podcast:01`). That cap is applied identically to every
submission but bites only the team whose test asset is a browser suite. Where this
comparison touches demonstrated behaviour, I separate what the sandbox prevented from
what the submission itself would have left unproven, and I say so at each point.

Two further asymmetries, both environmental and neither counted against either team:
team-podcast's iPhone-specific claims (PWA install, screen-locked background audio,
lock-screen MediaSession, real iOS quota) cannot be settled by any container
(`ev-podcast-10`); team-ledger's agent-orchestration layer cannot be exercised under a
no-network sandbox (`ev-ledger-18`, manifest "Missing evidence"), and no PDF-authoring
tool exists in its approved image, so `fin ingest <file>.pdf` was never invoked
(`runs/team-ledger-envcheck-01.json`).

Run-record volume: 16 for team-podcast, 11 for team-ledger. Volume is not quality; I
cite outcomes, not counts.

**Initial totals were not used and must not be.** `head-to-head.md` says "Do not merely
select the team with the higher initial total." team-podcast has no official total at
all — `reliability` is an `NE` from all four judges, adjudicated and **accepted** as
unscorable from the pinned package for reasons the adjudication records as the
framework's and the operator's, not the team's (`adj:live-trial-2026:team-podcast:01`).
Its provisional 58.25 is not a total. Comparing it against team-ledger's 76.3 would be
meaningless, and I did not. The seven criteria below are compared directly on common
evidence.

**Two corrections to the evidence packages carried forward.** `ev-podcast-05` recorded
43 `check()` call sites in `tests/e2e.py`; the correct count is **42** — the 43rd grep
match is the definition at `tests/e2e.py:33` (consolidated report, Correction 1). The
team's "42/42" claim at `README.md:285` and `DECISIONS.md:9` is therefore consistent
with its own source, and the only stale figure is `README.md:7`'s "34/34". I use 42.
`ev-podcast-06` describes the suite as 11 stages; the file prints headers numbered 1
through 13 plus an "11b", so "stage 7 of 11" overstates coverage — the best run reached
**stage 7 of 13**. I use 13. On the team-ledger side I discount manifest row R8, which
presents the dispute workflow as directly observed while `ev-ledger-07` shows only the
`NO_STATEMENT` branch with the deadline literally the string `unknown`
(judge-backend, Q2).

## Order-balanced results

| Criterion | Weight | A-first value | B-first normalized value | Combined evidence finding |
|---|---:|---:|---:|---|
| functional | 25 | — | -1 | team-ledger demonstrated nine of ten advertised subcommands end to end (`ev-ledger-01`, `-02`, `-04`, `-06`, `-07`) including the hard cases — control-total rejection on a genuine $500 discrepancy (`ev-ledger-08`), four rejections leaving every table at zero rows, idempotent re-ingest (`ev-ledger-04`). team-podcast has direct evidence for roughly four of its eight intake workflows; stages 4 and 8-13, including the offline playback `DECISIONS.md:15` calls a hard requirement, were never executed by anyone (`ev-podcast-06`). Part of that gap is the event's disk and shm caps (`ev-podcast-18`); part is the submission's own all-or-nothing suite and absent unit tests, which would have left the same surface unproven regardless. |
| product | 15 | — | 0 | Both solve a sharply framed problem for one named user with visible design judgment, and each has one strong layer and one rough one. No material difference established. |
| agentic | 15 | — | -1 | team-ledger ships an inspectable, constrained AI control surface that is the product's intended primary interface (`ev-ledger-18`) with the boundary enforced structurally (`ev-ledger-20`). team-podcast's AI surface is a verified, correct, documented absence (`ev-podcast-07`, `ev-podcast-09`) — appropriate, but it leaves three of the criterion's four sub-questions without a subject. team-ledger is held to one point by unobserved effectiveness (an event constraint), absent action-level observability, and three skill statements false against the implementation. |
| engineering | 15 | — | -1 | Both are coherent, proportionate and unusually well commented. team-podcast carries two source-read defects that attack the only user data it cannot regenerate — a bare `DELETE FROM episodes` cascading to `progress`, triggered by an operation its own documentation recommends (W1), and a scan-order rowid used as a durable cross-device key when a stable natural key already exists in the same schema (W2). team-ledger's defect cluster is concentrated outside the well-trodden path and none of it destroys irreplaceable data. |
| reliability | 10 | — | 0 | `reliability` is not resolvable for team-podcast from its pinned package, and I could not place it on the scale in either direction without importing that unresolved uncertainty as a finding. This is "insufficient comparative evidence", not a deficiency finding. See below. |
| security | 10 | — | -1 | team-ledger's privacy controls live inside the artifact and three were verified by execution (`ev-ledger-11`, `ev-ledger-07`) plus two passing tests behind the PAN guard. team-podcast's entire access-control model is prose outside the artifact that this package never observed, and `run.sh:61` binds `0.0.0.0` one line after printing `http://127.0.0.1:8000` (W4). Each carries one comparable unmitigated risk, both source inferences. |
| innovation | 10 | — | -1 | team-ledger evidences both legs of the criterion: an inverted design thesis carried through every layer with one directly observed payoff (D0 firing on transaction one with no history, twice), plus real parser and matcher depth. team-podcast evidences technical depth strongly and explicitly declines the originality leg. |

The A-first column is left empty; the opposite-order pass populates it and `atj matchup`
normalizes and combines.

## Margin and outcome

- First-pass margin: not computed here — `atj matchup` derives it from the comparison
  values.
- Second-pass normalized margin: not available to this pass.
- Combined margin: not computed here.
- Close-call threshold: 5, from `head-to-head.md` front matter.
- Winner or adjudication status: not named numerically by this judge. **Qualitative
  read: team-ledger is ahead on this pass**, on five criteria at meaningful-advantage
  strength with two ties, and no criterion at decisive strength in either direction.
  `atj matchup` resolves.

## Decisive evidence

No criterion reached decisive strength. The material comparative evidence, by criterion:

**functional (-1).** team-ledger: nine of ten advertised subcommands observed producing
correct output in sandboxed run records (`ev-ledger-01`, `ev-ledger-02`, `ev-ledger-04`,
`ev-ledger-06`, `ev-ledger-07`); the control-total gate rejecting a statement whose own
arithmetic does not close, citing the exact $500.00 discrepancy (`ev-ledger-08`); the
line grammar parsing all four documented layout hazards on a balanced fixture
(`ev-ledger-09`); four malformed inputs rejected with every table left at zero rows,
then `0 new, 0 merged, 1 already known` on re-ingest (`ev-ledger-04`). team-podcast:
byte-range serving correct across six request shapes with exact streamed byte counts,
verified on both images (`ev-podcast-03`); the real ffmpeg pipeline transcoding an
18,631,917-byte source to 4,884,617 bytes and indexing it with `duration_sec: 578.896009`
(`ev-podcast-15`); an OPFS download byte-identical in one second (`ev-podcast-17`);
library render, ordering, title-from-filename and hide-played default in a live browser
(`ev-podcast-20` stage 1). Everything team-podcast executed was exact, and nothing was
observed failing for a reason inside its own code. The gap is coverage: blob-URL
playback, offline library render, offline playback, filter persistence, autoplay and
both delete flows were never exercised (`ev-podcast-06`). I attribute the disk-cap and
iPhone portions of that gap to the event, not the team (`ev-podcast-18`,
`ev-podcast-10`); I do not attribute the rest, because `tests/e2e.py` aborts the process
on any wait and reports nothing when it does — the `N/M checks passed` line at
`tests/e2e.py:387` never printed in three runs — and there is no unit test anywhere to
fall back on. Against team-ledger, the credit is capped by inputs: every functional
observation is against synthetic data constructed for the preparation (manifest
"Missing evidence"), the largest ledger anywhere in its package is four rows, and it
carries a confirmed defect that silently degrades a real user's results — tier 0 keys
on `external_ref` while the skill text and README attribute it to `order_id`, so a feed
matching the documented column list falls through to tier-1 matching with no warning
(`ev-ledger-16`, `ev-ledger-06`, manifest R13). That is why this is -1 and not -2.

**agentic (-1).** team-ledger's four `.claude/skills/*/SKILL.md` files (98/84/85/71
lines, `ev-ledger-18`) carry explicit mutual routing boundaries, refusal rules aimed at
the model's known failure modes (never hand-transcribe a figure from a PDF, never retry
a rejection with a flag, never call a charge fraudulent, never tell a user an expired
billing-error window extinguishes the claim, state that deadline arithmetic is not legal
advice), one fuzzy task with human approval and a termination condition, and an
instruction to prefer the exact tool over reasoning. The allocation is enforced
structurally, not by policy: zero LLM, HTTP or network import or call site across all 22
files in `src/fin/`, the only `subprocess` use being local `pdftotext` and the only
environment read being `FIN_DATA_DIR` (`ev-ledger-20`). team-podcast's answer is a
verified absence: every server module and client script read, same-origin `fetch()`
targets only, no model, key or SDK, `.agentic/project.yaml` six inert metadata lines,
every run executed with `--network none` and the app worked (`ev-podcast-07`,
`ev-podcast-09`). **That absence is the correct engineering decision and I do not treat
it as a deficiency** — the rubric forbids rewarding model names or agent count, and
D21's refusal to fuzzy-match episodes to blog posts after duration matching produced two
confident false pairs 0.4s apart, failing loudly into a typed `unresolved` list
(`scripts/sync-releases.py:95-102`, `releases.json:259-261,289-291`), is genuine
judgment about where a model does not belong. The comparative finding is narrower: the
criterion asks whether AI is appropriate, controlled, observable and effective, and
team-ledger answers three of the four from artifacts while team-podcast answers one and
leaves three without a subject. I record that the panel logged framework defect **D12** —
the rubric does not state how `agentic` is scored when a submission has no AI surface,
and all four team-podcast judges asked for a rule none could supply. My value is a
comparison on the criterion's own question, not an endorsement of any reading of the
anchors. team-ledger is held to -1 rather than -2 by three real weaknesses: effectiveness
entirely unobserved (an event constraint, not the team's doing), no record anywhere of
which command an agent chose with what arguments before a ledger mutation (PR8), and
three statements in the instruction text that are false against the implementation — the
tier-0 `order_id` claim, the tier-3 match claim, and the reclassification claim that
`.claude/skills/fin-analyze/SKILL.md:70-75` tells the agent to perform and that
`src/fin/ingest.py:186-190` makes a no-op.

**engineering (-1).** Verified independently in the checkout: `server/db.py:25` declares
`progress.episode_id ... ON DELETE CASCADE` and `server/db.py:37` executes
`PRAGMA foreign_keys = ON`, so the bare `DELETE FROM episodes` that `prune_missing`
issues on an empty scan (`server/db.py:94-103`, called unconditionally from
`index_library()` at `server/app.py:64`) destroys every listening position — the only
state this application accumulates that a rescan cannot rebuild — while `README.md:53`
and `server/config.py:24-25` tell the operator that directory is safe to delete (W1).
Separately, OPFS files are named `${episodeId}.m4a` (`web/js/opfs-worker.js:24`, read
back at `web/js/storage.js:92,103`) and IndexedDB progress is keyed the same way
(`web/js/idb.js:19-22`) against an `INTEGER PRIMARY KEY` reassigned in filename-sort
order on re-index, while `filename` is already `NOT NULL UNIQUE` at `server/db.py:13`
and the team wrote the correct rule at `DECISIONS.md:138` about the component it did not
build (W2); the library contains 15 renamed or superseded takes, so the rename case is
not hypothetical (`ev-podcast-16`). team-ledger's comparable findings are wrong data in
a derived table (`UNMATCHED` links persisting `method="AMOUNT_DATE_UNIQUE"`, PD3,
visible in `ev-ledger-06`), a documented tier that cannot commit (PR6, verified at
`engine.py:6-10` against `:254-272`), two docstrings claiming guarantees the code does
not provide (PD5), and a torn-write window `validate.py:45` cannot see (PR2) — all real,
none destroying irreplaceable user data, against writes that are atomic tmp-then-replace
per table with content-derived ids making idempotence a property rather than a check.
team-podcast's counterweight, which keeps this at -1: 22 recorded decisions and the
P1-P8 deviation table recording where the implementation departed from the plan and why,
which judge-backend called the single most useful maintenance artifact in the checkout,
and which team-ledger matches in comment quality but not in kind.

**security (-1).** team-ledger's controls are in the artifact and were watched working:
vault root `0700` and archived raw source `0600` (`ev-ledger-11`), dispute CSV `0600`
(`ev-ledger-07`), `render.write` chmodding every generated report
(`src/fin/render.py:43-46`), a PAN guard that raises at config load and also rejects the
field names `pan`/`card_number`/`number`/`cvv`/`expiry` with two tests behind it inside
the 35 that passed, a shipped `hooks/pre-commit` blocking ledger data, `.env`, real
config, Luhn-valid PANs and live token patterns (`ev-ledger-19`), and no network, HTTP
or model surface anywhere in the deterministic core (`ev-ledger-20`). team-podcast's
submitted code is clean — `ffmpeg`/`ffprobe` invoked as argument lists with absolute
paths and no shell so a filename cannot become a command (`server/media.py:28-34,57-69`),
the media path resolved from a row populated only from basenames of a local glob so
there is no traversal surface (`server/media.py:114`, `server/app.py:143-149`),
`escapeHtml` at every interpolation site, the service worker refusing to intercept
`/api/` and audio, no credentials anywhere, no telemetry, no third-party egress
(`ev-podcast-07`) — but its entire access-control model is `tailscale serve` plus a
firewalld rule documented in prose that this package never observed (`req-05`), and
`run.sh:61` execs uvicorn with `--host 0.0.0.0` immediately after `run.sh:60` prints
`==> HTTP on http://127.0.0.1:8000`, so the application listens on every interface and
tells the operator it does not (W4). I note explicitly that team-podcast holds no
secrets, no PII and no financial data, so it has less to protect — the advantage I
record is not "more data protected" but "controls inside the artifact, observed working,
versus controls outside it that were never observed and that the artifact's own launcher
contradicts". team-ledger is held to -1 by `fin sql`, which executes arbitrary DuckDB on
a default connection with no read-only mode, no statement-kind check and no
`enable_external_access = false` (PR1), reachable from attacker-influenced descriptor
text through a model-composed query — at least as consequential as W4 and equally
undemonstrated. Neither team had anything penetration-tested; both risks are source
inferences.

**innovation (-1).** team-ledger evidences originality and depth: detectors ordered by
time-to-detection with the explicit claim that D0 fires on transaction one where the
statistical detectors could not have fired until month six of a 343-day fraud
(`detectors.py:1-17`), directly observed firing on a single transaction with no history
and no feed, twice (`ev-ledger-03`, `ev-ledger-06`); a matcher that refuses to be a
global optimizer on the stated ground that a higher match rate hides fraud
(`engine.py:12-17`, verified in the checkout), with the principle surviving into
`d1_unmatched`, which counts anything not `COMMITTED` as unexplained so an `AMBIGUOUS`
annotation cannot retire a charge; a dispute model that re-tags an expired billing-error
window rather than dropping it; and parser depth verified by execution against a
bleeding rewards column, page furniture and a three-line wrapped merchant name
(`ev-ledger-08`, `ev-ledger-09`). team-podcast's depth is real and hard-won — OPFS
written from a dedicated worker because Safari has no `createWritable()` and
`createSyncAccessHandle()` is worker-only (D3); audio routed around the service worker
because the Cache API answers `200` where `<audio>` needs `206` (D4); autoplay continued
on the same element from the `ended` handler because iOS treats a new element as a fresh
blockable session (D16); completeness tracked in IndexedDB because OPFS has no rename
(P5); a hand-written range parser verified byte-exact across six cases (`ev-podcast-03`)
— and it has one directly observed payoff in the byte-identical 4,884,617-byte OPFS write
with a matching `storage.estimate()` delta (`ev-podcast-17`). But three of its four
judges recorded, and the submission's own documentation supports, that there is no
originality claim here to reward: these are documented platform behaviours applied
correctly, with the ambition deliberately capped (D14, P1). This is a comparison on the
criterion's two named legs, not a preference between problem domains; team-ledger's
highest-ceiling mechanisms are also its least demonstrated (tier 3 never ran and cannot
commit; the dual dispute clock never produced a non-`NO_STATEMENT` state), which is why
this is -1 and not -2.

**product (0).** Each has a strong layer and a rough one, and neither advantage is
material. team-podcast's interface reasons about states most prototypes ignore: three
distinct empty states each naming the control that fixes it (`web/js/app.js:123-133`),
hide-played default with the currently-playing row exempted (D19,
`web/js/app.js:111-115`), autoplay restricted to already-downloaded episodes so it can
never start a cellular fetch on a locked screen (D15, `web/js/app.js:298-311`),
`storage.estimate()` usage/quota/persistence surfaced in the header — the app
instruments the one question the team could not answer off-device
(`web/js/app.js:313-320`) — and `aria-pressed` maintained, persisted and verified in the
live DOM (`ev-podcast-20` stage 1). Against that: `downloadAll()` reports "all
downloaded" unconditionally after failures (W8), documentation misstates the artifact in
three places (W3, `ev-podcast-05`), `#status` is not a live region so every message the
app produces is silent to a screen reader (W10), and most of the interaction surface was
never driven. team-ledger's generated markdown is the best-designed surface in either
submission — do-not-edit banner naming the regeneration command, source attribution,
sections ordered by user urgency, findings reproduced verbatim (`ev-ledger-07`) — with
honest labels throughout (`UNVERIFIED (no control totals)`, `NO_STATEMENT`,
`deadline: unknown`) and error text that names the file, the line, the rule and the
reason for refusing. Against that: two of four rejection paths dump an eleven-line
traceback on a routine user error (PD1, `ev-ledger-05`, named independently by all four
judges), three of four `analyze` modes have no empty state and `recurring` prints
nothing at all (PD8), `fin match` prints only counts on the command implementing the
product's stated thesis (PD9), subcommand help is a bare argparse dump (PD12), setup is
five manual `cp` steps with no `fin init` (PD13), and the dispute as-of date defaults to
the ledger's latest post date, so a statutory deadline is computed against the data's age
(PR3). Each side has one item that changes a user's result rather than their experience
(W8 and the "Safe to delete" label for team-podcast; PR3 and PD2 for team-ledger), and
they are comparable in kind and severity. Tie.

## Conflicting evidence

- **team-podcast's three unclassified suite outcomes pull in opposite directions.** Away
  from the submission: the server had already logged `GET /api/media/1 200 OK` before
  both stage-3 failures; no invocation set `--shm-size`, so Chromium ran against a 64 MB
  `/dev/shm`; the Chromium profile shared the 64 MB tmpfs with the media; one run
  overlapped a concurrent container by a measured 71 seconds at `--cpus 1.0`
  (`ev-podcast-12`, `ev-podcast-16`, `ev-podcast-18`). Toward the submission: W5 —
  `web/js/storage.js:13-31` registers only `worker.onmessage` with no `onerror` and no
  timeout on the promise at `:49-76`, so a dead worker is indistinguishable from a slow
  one, in exactly the place two of the three runs died. Nothing in the package separates
  them, and no memory measurement was taken at the crash.
- **`ev-podcast-17` contradicts a "the download is broken" reading of `ev-podcast-16`.**
  An instrumented single-episode probe completed the same download in one second,
  byte-identical, with IndexedDB and `storage.estimate()` agreeing and zero console
  messages. The isolated two-episode repeat (`ev-podcast-20`) did not reproduce the 90s
  stall and failed differently, so the finding remains inconclusive rather than either
  confirmed or withdrawn.
- **team-ledger, M3.** Two judges rate `fin sql` the highest-consequence item in their
  reports; two read the same code and rate it low impact. The disagreement is entirely
  about threat model, not about the code, and it is invisible in the score table because
  `security` is unanimous. I weighed PR1 as a credible, undemonstrated risk on both
  readings and did not let either reading carry the criterion alone.
- **team-ledger, M4.** Two judges cite the ledger-relative as-of date approvingly, as
  what makes a detect run reproducible; one rejects the same default for the dispute
  clock, where it silently produces a wrong statutory deadline. Both are correct about
  their own path. I treated PR3 as a real product risk on the dispute path without
  disturbing the detector-reproducibility credit.
- **Classification split on W1.** Two team-podcast judges class the prune/cascade path a
  confirmed defect; one classes it a risk because it was never executed. I record it as
  confirmed by source read with the execution status stated, which is what all three
  descriptions support, and I verified the cascade and the `PRAGMA` directly in the
  checkout rather than relying on the citation.

## Tie-break or adjudication

`tie_break_order` is `[functional, reliability, product]` from `head-to-head.md` front
matter. This pass returns `0` on `reliability`, so if the combined result reaches the
tie-break, `reliability` contributes no margin and the effective order narrows to
`functional`, then `product`. I state the consequence; `atj matchup` applies it.

**On the `reliability` zero.** I reached `0` on the common evidence, and it is my
finding, not an inheritance. team-podcast's package establishes real reliability
properties — `/healthz` reporting liveness plus episode count (`server/app.py:210-213`),
a systemd unit with `Restart=on-failure`, `RestartSec=5` and a transcode-aware
`TimeoutStartSec` (`deploy/podcast-listener.service:27-31`) alongside `README.md:239-251`
naming the three conditions that must hold for restart-after-reboot with a verification
command for each, `storage.reconcile()` reclassifying interrupted downloads and
OS-evicted files at startup (`web/js/storage.js:117-128`), dirty progress draining
through `flushQueue()` with the server half observed passing all four stage-6 checks
(`ev-podcast-15`), and a suite that derives expected counts from the live `/api/library`
payload rather than hardcoding them (`tests/e2e.py:57-67`). It also establishes real
gaps: zero unit tests, including none under the range parser the team deliberately
hand-wrote and none under the last-write-wins comparison, and a suite that forfeits every
check after the first stall. team-ledger's package establishes a passing 35-test
property suite aimed at the hazards its author feared (`ev-ledger-12`) and gaps of its
own: `dispute.py` — the module computing a legal clock and a dollar figure — has no test
and only its `NO_STATEMENT` branch ever executed (PD4); no test imports `fin.cli`, so
exit codes, the `REJECTED` contract and every rendered report are uncovered; the
`AMBIGUOUS` branch the governing rule rests on has neither a test nor a run; and
`cmd_ingest` returns 0 after `_revalidate` reports invariant problems (PR4). These push
in both directions, and for team-podcast the criterion is not placeable on the scale at
all: a low score would ignore that every observed failure has a credible environmental
cause, and a high score would credit a suite that has never produced a result. Any
nonzero value I assigned would convert that unresolved uncertainty into a comparative
finding. `0` — "substantially equal **or** insufficient comparative evidence" — is the
accurate disposition. **It is explicitly not a finding against team-podcast**, and
nothing in either package shows team-podcast's suite failing for a reason traced to its
own code.

No adjudication is requested by this pass. If the combined margin falls inside the
close-call band of 5, or if the two passes disagree, the event's declared procedure
applies.

## Audit

- [x] Both passes were independent — this pass read no matchup artifact, sought no
      knowledge of the opposite-order pass, and inferred none.
- [x] Presentation order was reversed — this pass read team-podcast first and
      team-ledger second; the orientation of the values is recorded above.
- [x] Every nonzero comparison cites evidence — by evidence id, run record, or a
      repository-relative path with a line or symbol at the pinned commit.
- [x] No prohibited team metadata influenced judgment — no school, bracket position,
      previous placement, popularity, presentation order, or initial total was
      considered. The two teams' totals were deliberately not compared, and
      team-podcast's accepted `NE` was never treated as a deficiency.
- [x] Domain difference handled — each submission was compared against its own stated
      promises on the shared criteria, not against the other's problem.
- [x] Evidence asymmetry handled — the execution difference created by the event's
      64 MB tmpfs, 64 MB `/dev/shm`, missing PDF-authoring tool and no-network policy is
      named where it applies and was not converted into a quality difference.
