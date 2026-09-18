---
event_id: live-trial-2026
match_id: mu:live-trial-2026:final:01
round_id: final
team_a: team-ledger
team_b: team-podcast
commit_a: 9d21b7707f204ef60f5a1cee612f1d4db0a4a575
commit_b: f3fdd342465fa6bc2a52d226a8613b082ad329e0
evidence_package_a: ev:live-trial-2026:team-ledger:9d21b7707f20:b859a240
evidence_package_b: ev:live-trial-2026:team-podcast:f3fdd342465f:d06f90cc
rubric: head-to-head@1.0.0
source_rubric: submission-evaluation@1.0.0
persona: matchup-judge@1.0.0
presentation_order: a-first
framework_commit: 1e761e639141d099f975cd6b4e3efaa296e6602f
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: 2026-09-17T23:20:00Z
completed_at: 2026-09-17T23:20:00Z
close_call_band: 5
passes:
  a_first:
    presented_first: team-ledger
    comparisons:
      functional: 1
      product: 0
      agentic: 1
      engineering: 1
      reliability: 0
      security: 1
      innovation: 0
  b_first:
    presented_first: team-podcast
    comparisons: {}
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

This is the `a-first` pass only. The `b_first` block is empty because this pass was
run without sight of the opposite-order pass, as required by
`framework/rubrics/head-to-head.md` ("Do not expose one pass to the other").
Margins, the combined margin, the winner and the outcome are for `atj matchup` to
resolve; nothing numeric is computed here.

## Eligibility and common evidence

Both submissions are pinned, both evidence packages are `approval_state: approved`
and `validation_state: valid`, both carry `execution_status: sandboxed-partial`, and
both were prepared by `prepare-submission@1.1.0` at framework commit
`152dd2c10547a1c15bb56c4b1a90764b28354c59` under `submission-evaluation@1.0.0`.
Both checkouts were read directly at their pinned commits for this comparison; the
consolidated reports were used as an index into evidence, not as a substitute for
it.

**Initial totals were not used and must not be.** `head-to-head.md` states "Do not
merely select the team with the higher initial total." team-ledger is finalized at
76.3; team-podcast has no official total because `reliability` is an accepted `NE`
(`adj:live-trial-2026:team-podcast:01`), and its provisional sum of the six scored
criteria is unofficial and unpublishable. The two figures are not commensurable and
were not compared. The seven criteria below are compared directly on common
evidence.

**Evidence asymmetry created by the event, stated once and applied throughout.**
team-ledger's test suite ran to completion (35 passed, exit 0, offline,
`ev-ledger-12`). team-podcast's suite never completed a run: the first approved
image lacked `ffmpeg`/`ffprobe` (`ev-podcast-01`, `ev-podcast-04`), and after the
operator closed that gap the binding constraint became the framework's own 64 MB
`/tmp` tmpfs and podman's default 64 MB `/dev/shm` under `--memory 1g --cpus 1.0`
(`ev-podcast-12`, `ev-podcast-18`, `ev-podcast-20`), which cannot hold the 56-file,
2.2 GB source library regardless of image contents. Three executions produced three
outcomes and none was classified (`ev-podcast-15`, `ev-podcast-16`,
`ev-podcast-20`). Every traced failure points away from the submission: the server
had already logged `GET /api/media/1 200 OK` before both stage-3 failures. Nothing
in this report converts that gap into a quality difference between the teams. Where
coverage differences are cited, the environmental component is named and discounted.

**Different kinds of software.** team-ledger is a local-first personal-finance CLI;
team-podcast is a self-hosted audio PWA. Each is compared on how well it meets its
own promises against the shared criteria. A CLI is exhaustively exercisable inside
an offline container and an iPhone PWA is not; that is a property of the event's
instrument, not of either team's engineering, and it is discounted below.

## Order-balanced results

| Criterion | Weight | A-first value | B-first normalized value | Combined evidence finding |
|---|---:|---:|---:|---|
| functional | 25 | 1 | pending | A's promised chain observed complete end to end (`ev-ledger-02`, `-04`, `-06`, `-07`, `-08`, `-09`); B's executed portions exact to the byte but roughly half the advertised surface unobserved for environmental reasons, and B carries a source-established destruction of its only non-regenerable data invited by its own documentation (`W1`, verified at `server/config.py:24-25`, `server/db.py:94-103`) |
| product | 15 | 0 | pending | Both solve a sharply framed problem with argued defaults; A's strength is generated-report design (`ev-ledger-07`), B's is state-aware feedback and empty states (`ev-podcast-20` stage 1, `ev-podcast-17`). Each carries comparable user-facing defects on different surfaces |
| agentic | 15 | 1 | pending | A ships a designed, structurally enforced agentic control surface (`ev-ledger-18`, `ev-ledger-20`); B has a verified, appropriate absence of any AI (`ev-podcast-07`, `ev-podcast-09`). A has evidence on three of the criterion's four sub-questions, B on one, by absence. Held below decisive by A's unobserved effectiveness, absent action logging, two false skill statements, and the panel's logged rubric gap D12 |
| engineering | 15 | 1 | pending | Both proportionate and well reasoned. A's durable-state design is structurally correct (content-derived ids, atomic per-table replace, asserted invariants — `src/fin/store.py:109-143`); B's identity model is structurally wrong for the use it is put to (`W2`) and its destructive path fires on a documented routine action (`W1`). Narrow; B's `DECISIONS.md` deviation table is the single best maintenance artifact in either submission |
| reliability | 10 | 0 | pending | Not comparable on this evidence. B's criterion is an adjudicated, accepted `NE` for framework and operator reasons (`adj:live-trial-2026:team-podcast:01`); the defined value for "substantially equal **or** insufficient comparative evidence" applies |
| security | 10 | 1 | pending | A's privacy enforcement is demonstrated by execution on materially higher-stakes data (`ev-ledger-11`, `ev-ledger-07`, `ev-ledger-19`, `ev-ledger-20`); B's only access control lives outside the artifact and is contradicted by the artifact's own startup banner (`run.sh:60-61`). Held below decisive by A's unconstrained `fin sql` surface (`src/fin/cli.py:217-223`) |
| innovation | 10 | 0 | pending | Different kinds of ambition, both evidenced and both proportionate. A's originality is in problem framing and was observed operating (`ev-ledger-03`); B's is platform-constraint depth with one observed payoff (`ev-podcast-17`). Preferring one kind over the other is preference, not evidence |

## Margin and outcome

- First-pass margin: not computed here — `atj matchup` derives it from the
  comparison values below and the source-rubric weights.
- Second-pass normalized margin: not available to this pass.
- Combined margin: not computed here.
- Close-call threshold: `close_call_band: 5`, read from
  `framework/rubrics/head-to-head.md` front matter.
- Winner or adjudication status: not named. Qualitative read: **this pass finds
  team-ledger ahead**, on four meaningful advantages and no decisive advantage, with
  two criteria substantially equal and one not comparable. No advantage in this pass
  is decisive, so the result is narrower than the criterion count alone suggests, and
  the tool should be expected to resolve it near rather than far from the close-call
  band.

## Comparison values

```json
{"functional": 1, "product": 0, "agentic": 1, "engineering": 1, "reliability": 0, "security": 1, "innovation": 0}
```

Positive favours Team A (team-ledger); negative favours Team B (team-podcast).

## Decisive evidence

No criterion reached `2` or `-2`. The four nonzero values are meaningful advantages.
Their supporting evidence, by criterion:

### functional — value 1

Team A. Nine of the ten advertised subcommands ran to correct completion in
sandboxed records (`ev-ledger-01`, `ev-ledger-02`, `ev-ledger-04`, `ev-ledger-06`,
`ev-ledger-07`). The all-or-nothing claim is structural, not incidental:
`check_control_totals` is called before any write (`src/fin/ingest.py:144`), and the
gate rejected a synthetic statement for a genuine $500.00 discrepancy while citing
it (`ev-ledger-08`). Four malformed inputs were refused with every table left at
zero rows, then an identical re-ingest reported `0 new, 0 merged, 1 already known`
(`ev-ledger-04`). `fin validate` reported all three invariants holding after mutating
runs (`ev-ledger-03`, `ev-ledger-06`).

Team B. Everything executed was exact: byte-range serving correct across six request
shapes with exact streamed byte counts including a suffix range and a past-EOF `416`
carrying `Content-Range: bytes */5000000` (`ev-podcast-03`); a real 18,631,917-byte
source transcoded to 4,884,617 bytes and indexed with `duration_sec: 578.896009`
(`ev-podcast-15`); progress apply/stale-reject/newer-accept (`ev-podcast-03`); an
OPFS download byte-identical in one second with IndexedDB and
`navigator.storage.estimate()` agreeing and zero console output (`ev-podcast-17`);
library render, ordering, filename-derived title and hide-played default in a live
browser (`ev-podcast-20` stage 1). Nothing was confirmed to fail for a reason inside
the submission, and the two in-stage failures that did appear are not defects: the
stage-5 "seek to 600s landed — 578.9s" matches the fixture's own duration to the
tenth of a second, the signature of a correct clamp against a test hardcoding a
longer episode (`ev-podcast-15`), and the stage-1 "0 of 2 dated" is fully explained
by both fixture files sitting in `releases.json`'s own `unresolved` block
(`ev-podcast-16`).

What separates them, after discounting coverage. Coverage alone is not a fair
discriminator here: A's surface is a CLI that an offline container can drive
exhaustively, B's includes a blob-URL playback path and an iPhone install that no
container sandbox can reach at all (`ev-podcast-10`), plus stages blocked by the
framework's own tmpfs cap (`ev-podcast-18`). What survives that correction is a
difference in demonstrated data integrity. A's durable-state properties —
no-partial-import, idempotence, post-mutation invariant assertion — were exercised
and held. B carries a coupled source-established defect on the only user data in the
system that cannot be regenerated: `index_library()` calls `prune_missing()` on every
startup and rescan (`server/app.py:64`), `prune_missing` issues a bare
`DELETE FROM episodes` when handed an empty record list (`server/db.py:94-103`),
`progress` cascades (`server/db.py:25`) with `PRAGMA foreign_keys = ON`
(`server/db.py:37`) — and `server/config.py:24-25` labels both `MEDIA_DIR` and
`DB_PATH` "Derived data. Safe to delete; a rescan rebuilds both." A rescan does not
rebuild progress. I verified this chain directly in the checkout, including that the
"safe to delete" comment covers `DB_PATH` and not only `MEDIA_DIR`. Compounding it,
episode identity is a scan-order rowid used as a durable cross-device key — OPFS
files are named `${episodeId}.m4a` (`web/js/opfs-worker.js:24`, read back at
`web/js/storage.js:92,103`) and IndexedDB progress is keyed the same way
(`web/js/idb.js:19-22`) — while `filename` is already `NOT NULL UNIQUE`
(`server/db.py:13`) and would serve (`W2`).

Why this is meaningful and not decisive. A's own list is not clean: the tier-0
documentation names `order_id` where the code keys on `external_ref`, so a feed
matching the documented column list silently degrades to tier-1 matching on the
headline path (`ev-ledger-16`, `ev-ledger-06`, manifest R13); the advertised
reclassification loop is a no-op (`PD7`); tier 3 cannot produce a committed match as
documented (`PR6`); `_infer_year` silently assigned an out-of-cycle `2026-12-20` in
the team's own hazard fixture (`PD6`, `ev-ledger-08`). And B's defects are
established by source read, not observed failing. The advantage is one step of
demonstrated completeness plus one class of durable-state risk, not a gap in kind.

### agentic — value 1

Team A. Four `SKILL.md` files totalling 338 lines constitute a real agentic control
surface, read as data in preparation and independently by all four judges
(`ev-ledger-18`). They carry mutual negative routing ("Do NOT use to load data
(fin-ingest)"), an instruction to present candidates and ask rather than pick on
ambiguity, an instruction to prefer the exact tool over reasoning ("a query is
exact, cheap, and reproducible; mental arithmetic over a thousand rows is none of
those"), a human-in-the-loop with a termination condition for the one fuzzy task
(the model proposes a merchant rule, the user approves, the rule is frozen into
deterministic config and the model is out of the loop), and concrete user-safety
boundaries: never describe a charge as fraudulent, never file anything, state plainly
that deadline arithmetic is not legal advice, never tell a user an expired
billing-error window extinguishes the claim. The model/code split is enforced by
construction rather than by policy: `ev-ledger-20` records zero import or call site
for any network, HTTP or LLM surface across all 22 files in `src/fin/`, the only
`subprocess` use being local `pdftotext`, so parsing and money cannot silently become
model output.

Team B. `ev-podcast-07` and `ev-podcast-09` establish a complete, verified absence:
no model, API key, AI SDK or third-party fetch target in any server module or client
script; the only `fetch()` targets are same-origin `/api/library`,
`/api/progress/{id}`, `/api/rescan`, `/api/media/{id}`; `.agentic/project.yaml` is
six inert metadata lines. Every sandbox run executed with `--network none` and the
app worked. That is the correct engineering decision for a local media player, and
the adjacent judgment is genuinely good: `D21` refuses to fuzzy-match episodes to
blog posts after duration matching produced two confident false pairs 0.4 s apart,
choosing an exact-filename join that fails loudly into an `unresolved` list with
typed reasons (`scripts/sync-releases.py:95-102`, `releases.json:259-261,289-291`).

What separates them. The criterion asks whether AI is appropriate, controlled,
observable and effective. A has evidence bearing on three of those four. B has
evidence bearing on appropriateness, and by absence; there is no system to assess for
control, observability or effectiveness. That is an evidence-backed difference in
what the criterion measures, not a preference for AI content, and it does not reward
model names, framework choice or agent count, which the source rubric forbids.

Why this is meaningful and not decisive, and a caution. A's effectiveness is entirely
unobserved and unobservable under the event's no-network constraint — an event
limit, not the team's doing. There is no action-level observability at all: nothing
records which command an agent chose, with what arguments, before a ledger mutation
(`PR8`). Two of the skill statements are false against the implementation — the
tier-0 `order_id` attribution (`ev-ledger-16`) and the reclassification instruction
that cannot take effect (`PD7`) — so an agent following the text would mislead a
user on the headline path. And the one tool the analyze skill steers the model
toward, `fin sql`, is an unconstrained execution engine (`PR1`). Separately, the
panel logged framework defect **D12**: the rubric does not state how `agentic` is
scored when a submission has no AI surface, and all four judges asked for that rule.
Part of the gap here is therefore a rubric gap rather than a quality gap, which is an
independent reason to hold this at `1` rather than `2`. None of this should be read
as counting B's decision not to use AI against it.

### engineering — value 1

Team A. Module boundaries follow the domain with no layering inversions; integer
cents throughout; ids are content-derived so idempotence is a property of the id
scheme rather than a check (`src/fin/store.py:123-143`, `src/fin/ingest.py:12-16`);
writes are tmp-then-`replace` with deterministic sort order so the ledger is
reproducible and git-diffable (`src/fin/store.py:109-121`); derived tables are
rewritten wholesale so a stale run cannot leave phantom findings
(`src/fin/store.py:47-49`); the adapter protocol requires each adapter to declare its
`CreditSign` rather than infer it, which is the design principle behind the observed
refusal behaviour (`ev-ledger-13`, `ev-ledger-04`). Comments state the rejected
alternative and the failure mode it avoids, at the point of the decision — three
judges independently named this the strongest maintainability signal in the
submission.

Team B. Four server modules and five client modules with one responsibility each; no
build step where none is needed; OPFS writes confined to the one context where
`createSyncAccessHandle()` exists; comments explaining the non-obvious constraint at
the point of the choice. `DECISIONS.md` carries 22 decisions with rationale and an
8-row table of deviations from the original plan with reasons — the single best
maintenance artifact in either submission, and I record that plainly.

What separates them. The difference is durable-state design. A's is structurally
correct and its one gap requires a crash to manifest: `ingest_card_file` performs
three independent whole-table writes after the all-or-nothing gate
(`src/fin/ingest.py:160,224-225`), each individually atomic but not atomic as a set,
and `src/fin/validate.py:45` checks only the opposite orphan direction, so that torn
state would pass validation clean (`PR2`). B's is wrong for the use it is put to and
its failure fires on an ordinary documented action, not on a crash: `W1` above, plus
`W2`'s scan-order rowid as a durable cross-device key when a stable natural key
already exists and the team wrote the correct rule down at `DECISIONS.md:138` — for
the component it did not build. Alongside those: one module-level SQLite connection
with `check_same_thread=False` shared across the sync threadpool with a non-atomic
read-then-write in `put_progress` (`server/app.py:25`, `server/db.py:33-39,153-167`),
correct at one writer and nowhere recorded as a hard constraint; and no unit test
anywhere, including under the range parser the team deliberately hand-wrote because
a framework difference "would be miserable to debug on a phone" (`W7`).

Why this is meaningful and not decisive. The margin is narrow and I do not want it
read as larger than it is. Both submissions are proportionate, both document their
reasoning better than this event usually sees, and A has its own documentation
overreach — `validate.py`'s docstring claims a bucket-partition check the code does
not perform, and `store.py` says invariants are asserted "after every mutation" while
only a successful non-dry-run ingest revalidates (`PD5`). B's decision record is
better than A's; A's data model is better than B's. The edge is the data model,
because it is the thing a maintainer cannot fix cheaply later.

### security — value 1

Team A. The privacy controls are enforced in code and verified by execution, not
asserted: vault root `0700` and archived raw source `0600` (`ev-ledger-11`), dispute
CSV `0600` confirmed by `stat` in the run (`ev-ledger-07`), and `render.write`
chmods every generated report (`src/fin/render.py:43-46`). Data minimisation is a
raising guard at config load, not discipline: a full card number and a `pan`-class
field name are both refused, with two tests behind it inside the 35 that passed.
`hooks/pre-commit` is a real shipped control that blocks ledger data, `.env`, real
config, Luhn-valid PANs and live token patterns (`ev-ledger-19`). There is no
network, HTTP or model surface anywhere in the deterministic core (`ev-ledger-20`),
and the responsible-AI content is concrete and user-protective rather than
boilerplate. The data at stake is a complete personal financial history.

Team B. Four judges independently looked for an exploitable defect and none found
one. `ffmpeg`/`ffprobe` are invoked as argument lists with absolute paths and no
shell, so a filename cannot become a command; the media path is resolved from a
database row populated only from basenames of a local glob, so there is no traversal
surface (`server/media.py:114`, `server/app.py:143-149`); every interpolated episode
string is escaped (`web/js/app.js:161-170,237-240`); the service worker refuses to
intercept `/api/` and audio (`web/sw.js:39-57`); no credentials anywhere, `.env`,
`certs/` and `data/` gitignored; no telemetry, analytics or third-party egress
(`ev-podcast-07`). The team wrote its threat model down including the parts that cost
it something.

What separates them. A's positive controls were demonstrated by execution; B's were
verified by source read only, and B's entire access-control model lives outside the
artifact — `tailscale serve` plus a firewalld rule, neither present in the repository
and neither ever observed. Worse, the artifact contradicts its own perimeter
statement: I verified in the checkout that `run.sh:60` prints
`==> HTTP on http://127.0.0.1:8000` and `run.sh:61` execs uvicorn with
`--host 0.0.0.0` (the `--https` branch does the same on 8443 at `run.sh:55-57`). The
application listens on every interface and tells the operator it does not. Alongside
that, `POST /api/rescan` is unauthenticated and cross-site triggerable with no
preflight, fanning out to eight concurrent ffmpeg processes with no guard against two
rescans sharing a `.part` path (`server/app.py:93-97`, `server/media.py:55,80-89`),
and `gen-cert.sh:44-49` mints a 3650-day root CA that `README.md:141` walks the user
through trusting on a personal phone.

Why this is meaningful and not decisive. A carries the single widest open risk in
either submission: `fin sql` opens a default `duckdb.connect()` and executes the
query string verbatim with no read-only mode, no statement-kind check and no
`enable_external_access = false` (`src/fin/cli.py:217-223`, verified directly), while
the analyze skill steers a model toward it and the descriptor text the model reasons
over arrives from files the user did not author. Two judges rate it the
highest-consequence item in the submission and both state explicitly that they
attempted no exploit; two others read the same code and rate it low impact. No
adversarial testing was performed against either submission by anyone. A's edge is
enforcement that was executed and observed, against a perimeter that exists only in
prose and is falsified by one line of the submission's own start script — not an
absence of risk on A's side.

## Conflicting evidence

- **`fin sql` severity is genuinely contested inside team-ledger's own panel.** Two
  judges call it the top risk in the submission, tracing a path from
  attacker-influenced descriptor text through a model-composed query to filesystem
  and network access from a process the product advertises as offline; two read the
  same code and call it low impact on the ground that arbitrary SQL is the advertised
  feature and the only reachable data is the user's own. Both sides state they
  attempted no exploit. This is a threat-model disagreement on an agreed code
  reading, and it is the main thing holding `security` at `1` rather than higher.
- **`W1`'s classification is contested inside team-podcast's own panel.** Two judges
  class the prune/cascade path a confirmed defect; one classes it a risk because it
  was established by source read and never executed. I record it as
  confirmed-by-source-read with its execution status stated, which is what all three
  descriptions support, and I verified the chain in the checkout myself.
- **team-podcast's `agentic` split (2/3/3/3) is interpretive, not factual.** All four
  judges verified the same complete absence of AI and disagreed only about which
  rubric anchor applies when the subject of a criterion is absent by a correct and
  documented decision. The panel logged this as framework defect **D12** and declined
  to treat the mean as a settlement. My comparison value reflects that the criterion's
  questions are answerable for A and largely have no subject for B, not that B's
  decision was wrong.
- **A correction the panel carried, applied here.** `ev-podcast-05`'s figure of 43
  `check()` call sites is wrong; the 43rd match is the function definition at
  `tests/e2e.py:33`. The suite has 42 checks, so team-podcast's "42/42" claim at
  `README.md:285` and `DECISIONS.md:9` is consistent with its source and only
  `README.md:7`'s "34/34" is stale. The documentation-drift finding is therefore half
  the size the evidence package recorded, and it is weighted at the corrected size in
  `product` above.
- **A second package correction, applied here.** `tests/e2e.py` prints stage headers
  numbered 1 through 13 plus an "11b", not 11 stages. "Stage 7 of 11" overstates the
  coverage reached; the best run reached stage 7 of 13. This makes team-podcast's
  unexecuted surface larger than the manifest states — and since that surface is
  unexecuted for framework and operator reasons, it is discounted rather than charged
  to the team.

## Tie-break or adjudication

Not invoked by this pass. Recorded for whoever resolves the matchup:

`tie_break_order` in `framework/rubrics/head-to-head.md` front matter is
`[functional, reliability, product]`. This pass returns a nonzero value on
`functional`, so step 1 is not exhausted here. Should the combined result land inside
the close-call band, note that `reliability` at `0` contributes no margin and no
tie-break signal, which the adjudication `adj:live-trial-2026:team-podcast:01`
anticipated: with `reliability` at `0` the effective tie-break order becomes
`functional`, then `product` — and `product` is also `0` in this pass, which would
push resolution to step 4 (fewest confirmed critical security or data risks) or step
5 (neutral human decision). On step 4, the candidate items are team-ledger's `fin sql`
execution surface (`PR1`, contested severity, no exploit attempted) and
team-podcast's progress-destroying prune path (`W1`, source-established, never
executed) together with the `0.0.0.0` bind contradicting the documented perimeter
(`run.sh:61`). None of the three is confirmed by execution, so step 4 would not
resolve cleanly on this evidence either.

`reliability` is recorded as `0` as my own finding on the common evidence, for the
reason the value is defined: there is insufficient comparative evidence to establish
a difference. team-podcast's package cannot support any score on that criterion, and
scoring team-ledger's completed suite as a comparative advantage would convert an
evidence asymmetry the event created into a quality difference between the teams.
This is explicitly **not** a deficiency charged to team-podcast. For the record, the
common evidence on both sides is also mixed in the same direction on its merits:
team-ledger's 35-test property suite leaves `src/fin/dispute.py` — the module
computing a legal clock and a dollar figure — with zero tests and only its
`NO_STATEMENT` branch ever executed, no test imports `fin.cli`, the `AMBIGUOUS`
branch the product's governing rule rests on is covered by nothing, and
`cmd_ingest` returns 0 after `_revalidate` reports invariant problems to stderr;
team-podcast has zero unit tests but ships `/healthz` with a live episode count,
`Restart=on-failure` with a transcode-aware `TimeoutStartSec` and three documented
restart preconditions each with a verification command, `storage.reconcile()`
distinguishing an interrupted write from an OS eviction, and a dirty-flag drain
through `flushQueue()`, against a download path with no `worker.onerror`, no
`onmessageerror` and no timeout (`web/js/storage.js:13-31,49-76`, verified directly).
Neither side is clearly ahead even before the `NE` is taken into account.

## Audit

- [x] Both passes were independent — this pass was run without sight of the
      opposite-order pass and sought none; nothing under
      `events/live-trial-2026/matchups/` was read.
- [x] Presentation order was reversed — this is the `a-first` pass of the required
      pair; `order_balancing: required` is satisfied by the pair, not by this
      document, and the `b_first` block is left empty for `atj matchup` to fill.
- [x] Every nonzero comparison cites evidence — all four nonzero values cite evidence
      ids from the two packages and, where a claim is load-bearing, the file and line
      verified directly in the pinned checkout.
- [x] No prohibited team metadata influenced judgment — school, previous placement,
      bracket path, popularity, team identity, presentation order and ceremony
      convenience were not considered. Initial totals were not used; the finalized
      76.3 and the unofficial provisional 58.25 were not compared, and the
      `reliability` `NE` was treated as a limit of the evidence package and the
      event's execution constraints, never as a deficiency of team-podcast.
