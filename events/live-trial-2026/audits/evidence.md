---
event_id: live-trial-2026
audit_scope: evidence stage
audit_id: evidence
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.0.0
persona: judging-auditor@1.0.0
framework_commit: 152dd2c10547a1c15bb56c4b1a90764b28354c59
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-17T18:05:00Z"
completed_at: "2026-09-17T18:35:00Z"
visibility: private
approval_state: approved
validation_state: valid
result: FAIL
---
# Judging Audit — evidence stage

## Result

**FAIL** until the four major findings are resolved.

Nothing here is a safety failure and nothing is fabricated. Every one of the 22
run records shows genuine container isolation, every sampled observation I
followed into its run record was there and was stated accurately, and the two
packages are the most carefully hedged evidence this event has produced. The
stage fails on four things that are cheap to fix and that judging cannot
proceed without: an image recipe that does not build the image the evidence was
produced on, an `evidence_limited_criteria` list that is empty where it should
name one criterion, a ledger with no `evidence:` unit to bind either manifest,
and a requirements table in the team-ledger package whose evidence citations
point at the wrong observations in nine of sixteen rows.

I did not re-read any judgment, bracket or publication artifact. None exists.

## Scope and artifacts inspected

- `events/live-trial-2026/event.md`, `teams.md`, `status.md`
- `events/live-trial-2026/submissions/team-podcast.md`, `submissions/team-ledger.md`
- `events/live-trial-2026/evidence/team-podcast/manifest.md` (19 evidence IDs,
  10 requirement rows)
- `events/live-trial-2026/evidence/team-ledger/manifest.md` (19 evidence IDs,
  16 requirement rows)
- `events/live-trial-2026/evidence/Containerfile.podcast`, `Containerfile.ledger`
- All 22 run records in `events/live-trial-2026/runs/` — 11 per team. The task
  brief says 23; the directory holds 22 records plus `.gitkeep`.
- `events/live-trial-2026/audits/configuration.md`, `audits/intake.md` — F1-F5
  and A1-A10 checked for closure
- `framework/rubrics/submission-evaluation.md`, `framework/personas.md`,
  `framework/templates/audit-report.md`, `framework/templates/evidence-manifest.md`,
  `framework/policies/evidence-and-citation.md`, `schemas/evidence-manifest.schema.json`
- `atj/sandbox.py` (`DEFAULT_LIMITS`, `evidence_limitation`,
  `EXECUTION_DEPENDENT_CRITERIA`), `atj/event.py` (`derive_digests`,
  `check_staleness`), `atj/ids.py` (`evidence_package_id`)
- Both checkouts under `workspaces/live-trial-2026/`, for provenance and for
  re-deriving sampled claims
- `podman images`; `git log` for the framework commit and both Containerfiles

## Deterministic validation results

Re-run rather than taken on trust. All four agree with the operator's report.

| Command | Result |
|---|---|
| `python3 -m atj event validate events/live-trial-2026` | PASS, 0 problems, stage evidence |
| `python3 -m atj validate reports events/live-trial-2026` | PASS, 6 artifacts, 0 blocking / 0 major / 0 minor / 0 advisory |
| `python3 -m atj release-check` | PASS — single-source PASS, version-skew PASS, sample event PASS |
| `python3 -m atj personas` | PASS, 15 agents |
| `python3 -m atj sandbox preflight` | AVAILABLE — podman 6.1.0 (rootless) |
| `python3 -m atj event status events/live-trial-2026` | stage evidence, gate `evidence-validated` pending, **units: none recorded** |
| `python3 -m atj event unit events/live-trial-2026 list` | 0 unit(s), 0 stale |

The validators cannot reach F2, F3 or F4. `atj validate reports` checks that an
`[[evidence:ID]]` target exists, not that it contains the claim made of it; it
has no view on whether `evidence_limited_criteria` is correct; and a missing
unit is an absence, not an invalid artifact. That gap is the reason this audit
exists.

## Provenance

Verified and correct:

- `git -C workspaces/live-trial-2026/team-podcast rev-parse HEAD` →
  `f3fdd342465fa6bc2a52d226a8613b082ad329e0`, matching `teams.md`, the intake
  record and the manifest. Working tree clean.
- `git -C workspaces/live-trial-2026/team-ledger rev-parse HEAD` →
  `9d21b7707f204ef60f5a1cee612f1d4db0a4a575`, likewise. Working tree clean.
- `framework_commit: 152dd2c10547a1c15bb56c4b1a90764b28354c59` resolves to a
  real object in this repository ("Add `atj intake`, the missing front door",
  2026-09-16) and is identical in `event.md`, both manifests and both prior
  audits.
- `podman images` confirms every ID in `event.md`: `ledger:2` =
  `7780b2b9e6e1`, `podcast:3` = `c3670644bc7b`. The superseded `podcast:2` =
  `5ff34ae63320` matches the ID the podcast manifest records for it.
- All 22 run records name an approved image. Ledger: 11 of 11 on `ledger:2`.
  Podcast: 7 on `podcast:3`, 4 on `podcast:2`.

Not correct: F1 (the ledger image recipe) and F6 (three `podcast:2` runs still
carrying current evidence). On the specific question asked — `e2e-attempt-01`
is properly kept and properly labelled as the record of the original blocked
attempt, and it is not cited as current evidence for anything. But it is not the
only `podcast:2` record in play. `server-boot-01` (ev-podcast-02),
`media-progress-01` (ev-podcast-03) and `runsh-attempt-01` (ev-podcast-11) also
ran on `:2` and are all cited as live evidence, and `ev-podcast-03` is the sole
support for req-02 and req-04. See F6.

## Execution integrity

Clean. Every one of the 22 records carries, in its own `command` field:
`--network none`, `--read-only`, `--tmpfs /tmp:rw,noexec,nosuid,size=64m`,
`--cap-drop ALL`, `--security-opt no-new-privileges`, `--user 65534:65534`, and
a `--volume …:/submission:ro,Z` mount pointing at that team's own workspace and
no other. No record contains `--network=host`, `--privileged`, `--userns=host`,
`--cap-add`, or a writable submission mount. `runtime: podman`,
`runtime_version: 6.1.0`, and `timed_out: false` throughout. Nothing ran on the
host; the two run records that show a read-only filesystem error
(`runsh-attempt-01`, `e2e-02`) are the sandbox policy working, and both are
described as environmental rather than as submission defects, correctly.

I verified more than the six sampled claims per team the brief asked for.

team-podcast, verified against the cited JSON:

1. ev-podcast-01 — no ffmpeg/ffprobe, Chromium 152.0.7977.82, fastapi 0.141.1,
   pydantic 2.13.5, uvicorn 0.53.0, playwright importable. Exact.
2. ev-podcast-02 — `/healthz` → `200 {"ok":true,"episodes":0}`, `/api/library`
   → `200` empty list, `/` and `/sw.js` → `200`. Exact.
3. ev-podcast-03 — `206` with `Content-Range: bytes 100000-199999/5000000` and
   100000 streamed bytes; suffix `bytes 4999500-4999999/5000000`; open-ended
   4999900 bytes; `416` with `bytes */5000000`; stale `PUT` rejected and the
   stored 42.5 unchanged; newer `PUT` applied to 1195.0 with `completed: 1`;
   unknown-episode `GET` returns a zero row and `PUT` raises. All present.
4. ev-podcast-04 — `E2E_EXIT:1`, Playwright `TimeoutError` on
   `wait_for_selector(".ep")` at `tests/e2e.py:56`, every static asset `200`
   in the server log. Exact.
5. ev-podcast-12 — `/usr/bin/ffmpeg`, `/usr/bin/ffprobe`, ffmpeg 7.1.5,
   `tmpfs 64M … 0 used`. Exact.
6. ev-podcast-15 — `{"transcode":{"done":1,"skip":0,"failed":0},"indexed":1,…}`,
   `duration_sec: 578.896009`, `size_bytes: 4884617`, stage 5 `[FAIL] seek to
   600s landed — 578.9s`, four stage-6 `[PASS]` lines, stage 7 timeout at
   `e2e.py:206`. Exact, including the `tail -34` in the command that the
   manifest itself discloses truncated stages 1-4.
7. ev-podcast-16 — stage 1 four PASS and `[FAIL] episodes carry blog release
   dates — 0 of 2 dated`, stage 2 pass, stage 3 `Timeout 90000ms exceeded`.
   Exact.
8. ev-podcast-17 — download at `t+1s`, OPFS `1.m4a` 4884617 bytes, IndexedDB
   `state: "done"`, `usage` 132322 → 5015459 with `fileSystem: 4884929`, empty
   `ALL_CONSOLE_LINES` and `ALL_PAGE_ERRORS`. Exact.
9. ev-podcast-05 — I re-derived this one from the checkout rather than the run
   record, because the manifest says it is file inspection: 56 `.m4a` files,
   2.2 GB, and `grep -c "check(" tests/e2e.py` → 43. All three confirmed.
10. ev-podcast-11 and ev-podcast-13 — `Errno 30 … '/submission/.venv'` and
    `OSError: [Errno 30] … '/submission/data'` with
    `net::ERR_CONNECTION_REFUSED`. Exact.

team-ledger, verified against the cited JSON:

1. ev-ledger-02 — `3 rows -> 3 new, 0 merged, 0 already known [UNVERIFIED (no
   control totals)]`, with `status` and `validate` following. Exact.
2. ev-ledger-03 — `[critical] D0  2 AMAZON charges on citi-costco-4021 … ($15.68)`
   and the $20.68 / -$5.00 pair. Exact.
3. ev-ledger-04 / 05 — four rejections, `REJECTED` one-liners for two of them, a
   Python `Traceback` with `ValueError` for the other two, `0 new … 1 already
   known` on re-ingest. Exact, and the error-contract finding is real.
4. ev-ledger-06 — `REFERENCE | COMMITTED | 1.0`, `AMOUNT_DATE_UNIQUE |
   COMMITTED | 0.95`, one `UNMATCHED`, then `D0 … ($165.79)` and `[warning] D1
   1 of 3 merchant-feed charges … ($99.99)`. Exact.
5. ev-ledger-07 — all four `analyze` subcommands, `wrote 3 markdown reports`,
   D0/D1 reproduced verbatim in `findings.md`, `NO_STATEMENT`, `interest
   attributable to disputed principal: $0.29`, mode `600`. Exact. The 22.49%
   APR is not in the run record; it is in
   `workspaces/live-trial-2026/team-ledger/config/accounts.example.yaml:14`
   (`apr_bp: 2249`), which I checked. See A2.
6. ev-ledger-08 — 3 rows parsed, then `control totals: REJECTED … payments:
   parsed $0.00 vs stated -$500.00 (off by $500.00)`. Exact.
7. ev-ledger-09 — exactly 4 rows classified payment/refund/purchase/interest,
   `1.2X` and `$232.43` hazards present, `control totals: PASSED`. Exact.
8. ev-ledger-11 — `vault dir perm: 700`, `600 /tmp/data/raw/…-good.csv`. Exact.
9. ev-ledger-12 — `35 passed in 0.07s`, exit 0, `ledger:2`, timestamped
   2026-09-16T23:56:26Z, before preparation began. Exact, and it closes intake
   F2.
10. ev-ledger-01 — the help surface matches. The count does not: the manifest
    says "all 9 subcommand `--help` screens" and then lists ten subcommands,
    and `envcheck-02` shows argparse offering ten. Folded into F7.

## Evidence sufficiency per rubric criterion

This is the question the brief most wanted tested, so here is the test I
applied and then the result for all fourteen criterion-team pairs.

`atj/sandbox.py` gives an automatic answer in exactly one case: when isolation
is unavailable, `evidence_limitation()` returns
`EXECUTION_DEPENDENT_CRITERIA = ("functional", "reliability")`. Isolation was
available here, so nothing is automatic and `sandboxed-partial` carries no
default list. The only other rule in force is the rubric's own —
"`NE` means not enough evidence" — and the citation policy's "Use `NE` when
required evidence is unavailable. Do not manufacture certainty."

The test I used: **can a judge produce the full criterion response the rubric
demands — score, what worked, what was deficient, reasoning from cited
evidence, confidence — without the decisive question being one the package
itself declines to answer?** A criterion that is thinly evidenced but
answerable is scored with low confidence, not `NE`. A criterion whose score
would swing across the whole anchor scale depending on a question the package
explicitly leaves open is `NE`.

**team-podcast — `reliability` must be listed. Nothing else.**

`reliability` asks whether failures can be prevented, detected, understood and
recovered from. For this submission that question is carried almost entirely by
`tests/e2e.py`, 43 checks across 11 stages, and the package cannot say whether
it passes. The furthest any run reached is stage 7 of 11, and in that run the
per-check results for stages 1-4 were destroyed by a `tail -34` in the
operator's own command. A second run stalled at stage 3. The package records
two behaviors — the stage-7 resume stall and the two-episode download stall —
and in its own words does not resolve either: "inconclusive whether that is
single-vs-two-episode flakiness or a real defect, not re-tested further", and
ev-podcast-19 is labelled an evaluator inference at medium confidence,
"reasoning only — not independently re-executed". F5 below adds a third
candidate explanation the package does not consider. On top of that the
submission's own pass claim is internally contradictory and unresolvable
without a complete run (34/34 vs 42/42 vs 43 call sites, ev-podcast-05).

A judge asked to score `reliability` therefore chooses between "the suite works
and both stalls are fixture artifacts" (3-4) and "the app stalls on download
and on resume-after-reload" (1-2) with nothing in the package that separates
them. That is the definition of not enough evidence. It is not a criticism of
the preparation, which is honest about every one of these gaps — it is a
mismatch between prose that says "inconclusive" five times and a front-matter
field that says `[]`, and the field is what the judging skill reads.

The genuine partial evidence that exists for `reliability` — correct `400`,
`416` and stale-write handling in ev-podcast-03, clean startup and shutdown —
does not change this, because none of it speaks to the two open questions.

`functional` is the closest call and I am **not** requiring it. Four of the six
workflows req-01 advertises are directly observed: transcode, index and serve
(ev-podcast-14, -15), byte-range seeking (ev-podcast-03), resume tracking
(ev-podcast-03, e2e stage 6), and download into OPFS (ev-podcast-17). Two are
not: offline playback from the OPFS blob, which the manifest concedes was never
confirmed, and iPhone home-screen install, which no container can exercise. A
judge can place this on the scale with confidence reduced, and the rubric's
"confirmed inability to complete the primary advertised workflow" clause is not
triggered because nothing was confirmed to fail. Both gaps are already named in
Missing or inaccessible evidence, which is where they belong.

The other five: `product` — the UI was rendered, ordered, filtered, downloaded
from and seeked in a real browser (ev-podcast-15, -16, -17), and the service
worker registered; scoreable. `agentic` — a full read of every server and web
module found no model, API key or AI SDK anywhere (ev-podcast-07), which is a
conclusive negative, not an evidence gap; a judge can score it, and anchor 0
("not demonstrated") exists for exactly this. `engineering` — every module read
(ev-podcast-07). `security` — same read plus the D11 tailnet decision and the
Cloudflare disclosure (ev-podcast-08), with the limits of a source-only review
stated. `innovation` — the OPFS/Worker/byte-range/service-worker design was
both read and exercised.

**team-ledger — none.**

All ten declared primary workflows were driven through the CLI in the sandbox
with correct, checked output. The one real gap is R11: the CLI-level PDF path
`fin ingest x.pdf` was never invoked, because the approved image has no
PDF-authoring tool. But what is untested there is the
`subprocess.run(["pdftotext","-layout",…])` shim and the `.pdf` suffix check.
The substance behind it — the line grammar against all four documented hazards,
and the control-total gate rejecting a statement whose arithmetic does not
close — was exercised directly against synthetic layout text (ev-ledger-08,
-09), and `pdftotext` was confirmed present in the image. The manifest already
marks R11 "Direct observation, partial" and explains precisely what confidence
is limited. That is the correct handling, and it does not rise to `NE` on
`functional`.

`agentic` was the pair I expected to fail and it does not, narrowly. The whole
agentic surface is four `.claude/skills/*.md` files driving `fin`, and the
package concedes the agent loop cannot be run offline. Three of the criterion's
four sub-questions are still answerable from artifacts: appropriateness and
control are visible in the architecture, and the CLI's own help text states the
split; observability is visible in what `fin` prints. Only effectiveness is
unobservable. The package also contributes a substantive negative finding here
— the `fin-ingest` skill's description of tier-0 matching is contradicted by
the implementation. A judge has enough to score with low confidence.

`reliability` is strong (35 tests passing offline, four rejection paths,
idempotent re-ingest, invariant validation, plus a real error-contract defect).
`security` is strong (0700 vault, 0600 dispute CSV, the pre-commit PAN scanner,
no secret consumption). `product`, `engineering` and `innovation` all rest on
observed CLI behavior and a full source read.

One caveat that is not an `NE` but must reach the judges: every functional
observation for team-ledger used synthetic inputs constructed by the preparer.
The manifest says so plainly. Two requirement rows overstate their coverage
anyway — see F7.

## Fairness and symmetry

Even-handed, and the reasoning is recorded. Both amendments do the same thing
for the same stated reason: install a system binary the submission's own
documentation names as a prerequisite, so that a failure caused by the image is
not read as a failure of the team. `poppler-utils` for team-ledger closes
intake A9 in exactly the terms A9 set. `ffmpeg` for team-podcast is justified in
`event.md` on explicitly identical reasoning, and the status ledger row at
2026-09-17T00:10:14Z names the omission as "an operator error that
disadvantaged this team relative to team-ledger". Naming your own error in the
ledger is the right instinct, and the remedy went further than the disclosure —
the evidence was re-run and the package rewritten, taking `tests/e2e.py` from
stage 1 to stage 7.

Three asymmetries remain, none of them favoritism:

1. The remedy was not complete. Three `podcast:2` runs were never re-run on
   `:3` (F6), while team-ledger has no equivalent split — all 11 of its records
   are on one image.
2. Provenance quality differs. `Containerfile.podcast` was updated when the
   podcast image changed; `Containerfile.ledger` was not when the ledger image
   changed (F1).
3. The operator amended the image twice to remove environmental disadvantage
   but left the 64 MB tmpfs in place, and that cap falls on only one team — a
   2.2 GB media library cannot be tested inside it. This is defensible, and
   ev-podcast-18 defends it well: the cap is the framework's, applied
   identically, and `atj sandbox run` does not expose an override. But the
   distinction between "fix a missing declared prerequisite" and "do not move a
   framework-wide resource limit mid-event" is currently only implicit. See A4.

## Privacy and boundaries

Passes. `events/live-trial-2026/public/` contains only `.gitkeep`. Every
artifact in scope declares `visibility: private`. No operator name, email
address or personal identifier appears anywhere in either manifest or any run
record. `public_scores: false` is unchanged. The working tree is clean and the
stray `status.md.bak` is gone.

No cross-contamination: no team-ledger material appears in the team-podcast
package or its run records, and none of the reverse. Each run record mounts
only its own team's workspace. The one cross-reference is the podcast
manifest naming team-ledger's `poppler-utils` precedent when it explains the
ffmpeg amendment — fairness documentation, not the other team's evidence, and
it carries no finding or result about team-ledger. See A6.

Two things to carry to publication: every run record embeds the absolute host
path `/home/gregg/Nextcloud/workspace/Software_Dev_Tournament/workspaces/…`,
and configuration A7's note about the operator's name in `event.md` still
stands. Neither may reach `public/` without `atj validate publication`.

## Neutrality

Holds. Neither manifest states or implies a score, recommends a score, or tells
a judge what a criterion is worth. Both separate direct observation, artifact
evidence, team claim and evaluator inference, and both do it in the classes
`framework/policies/evidence-and-citation.md` defines.

The podcast package's "candidate finding" framing survives scrutiny.
ev-podcast-19 is explicitly labelled `evaluator inference`, confidence
`medium`, "reasoning only — not independently re-executed", and the Missing
section calls both candidate findings inconclusive and says neither was chased
further. The stage-5 seek `[FAIL]` is argued down to a fixture artifact rather
than a defect, but the argument shows its work — 578.9s landed against
578.896009s actual duration — and the raw `[FAIL]` line is quoted intact, so a
judge who disagrees has everything needed to disagree. That is interpretation
offered transparently, not a conclusion imposed.

One uneven note, A3: ev-ledger-05 calls its finding "a real judgment-relevant
reliability/engineering gap, not a hypothetical one". That names two rubric
criteria and pre-weighs the finding for the judge. The observation itself is
accurate and well-evidenced. The editorializing is the podcast package's
framing done in reverse, and the podcast framing is the better one.

## Carryover from the configuration and intake audits

| Prior item | State |
|---|---|
| config F4 — name the approved images | Closed. Both images named with IDs. |
| config F5 — ledger timestamp accuracy | Reopened in a new form. See F8. |
| intake F1 — httpx/pytest/plain uvicorn in the podcast image | Closed. `Containerfile.podcast` now installs `uvicorn[standard]` and neither `httpx` nor `pytest`. |
| intake F2 — no run record for the 35-test run | Closed. `runs/team-ledger-pytest-01.json` exists, on `ledger:2`, 35 passed. |
| intake F3 — amendment needs time and authorizing official | Partly closed. Times are logged; no official is named on either amendment row. See F8. |
| intake F4 — record image IDs | Closed for the current images; superseded `podcast:2` is recorded in the manifest but not in `event.md`. See F6. |
| intake F5 — line-anchor drift, `.agentic` described as 5 lines | Not closed, and repeated in the evidence package. See F9. |
| intake A2 — intake records draft/unvalidated | Closed. Both are approved/valid. |
| intake A5 — re-run preflight at the evidence stage | Closed. Both manifests record `AVAILABLE — podman 6.1.0 (rootless)` before any run, and I re-confirmed it. |
| intake A6 — justify any timeout above the default | Not closed. See A1. |
| intake A8 — stale chromium conditional | Closed. Superseded by real run records. |
| intake A9 — no `pdftotext`, PDF ingest is `NE` unless the image changes | Closed in the image, not in the recipe. See F1. |
| intake A10 — `tests/e2e.py` is not a pytest suite | Closed. Every attempt starts the server first and runs the script against it. |
| config/intake A4 — agent-directed files in both checkouts | Closed. Both packages searched independently and treated the files as data. |
| config/intake A7 — operator name must not reach `public/` | Still open by design, still correct. Carried forward. |

## Findings

| Severity | Rule | Artifact | Finding | Required repair |
|---|---|---|---|---|
| major (F1) | `events/live-trial-2026/event.md`: "The Containerfiles are committed under `events/live-trial-2026/evidence/`"; intake audit A9's repair named this file | `events/live-trial-2026/evidence/Containerfile.ledger` | The committed recipe does not build the approved image. `event.md` lists `ledger:2` (`7780b2b9e6e1`) as containing poppler-utils, and the binary is genuinely there at run time (`/usr/bin/pdftotext` in `runs/team-ledger-envcheck-01.json` and in `pytest-01`'s stdout), but the Containerfile installs only `pyyaml`, `duckdb` and `pytest` and has never contained poppler-utils in any commit — `git log` on that path shows one commit, `6321a18`, predating the amendment. Rebuilding from this recipe produces an image in which team-ledger's PDF adapter cannot run, which is the exact condition intake A9 said would force `NE`. The intake audit accepted the image amendment partly because the Containerfiles were the inspectable record of what goes into the images; for team-ledger that record is now wrong. | Add the `poppler-utils` install layer to `Containerfile.ledger`. Rebuild and confirm the ID still resolves to `7780b2b9e6e1`, or record the new ID in `event.md` and re-run any affected evidence. Log the correction in `status.md`. |
| major (F2) | `framework/rubrics/submission-evaluation.md`: "`NE` means not enough evidence"; `framework/policies/evidence-and-citation.md`: "Do not manufacture certainty" | `events/live-trial-2026/evidence/team-podcast/manifest.md`, front matter | `evidence_limited_criteria: []` is not supportable for `reliability`. The submission's reliability story is `tests/e2e.py`, and no run of it completed: the best reached stage 7 of 11 with stages 1-4's per-check output destroyed by the operator's own `tail -34`, and another stalled at stage 3. The package records two behaviors and declines to classify either — "inconclusive whether that is single-vs-two-episode flakiness or a real defect, not re-tested further", and ev-podcast-19 at medium confidence, "reasoning only". F5 adds a third unexamined explanation. The submission's own pass claim is self-contradictory and unresolvable without a complete run. A score of 1 and a score of 4 are both consistent with this package, which is what `NE` is for. The prose says "inconclusive" repeatedly; the field that the judging skill actually reads says nothing. | Set `evidence_limited_criteria: [reliability]` in the team-podcast manifest and state the basis in Missing or inaccessible evidence: the suite never completed, and the two observed stalls are unclassified. Do not add `functional` — see the sufficiency section. Leave the team-ledger list empty. |
| major (F3) | `CLAUDE.md`: "update `status.md` after verified work"; `atj/event.py` docstring: "an edited judgment or evidence manifest changes the digest, and the unit goes stale" | `events/live-trial-2026/status.md`, front matter `units: []` | Neither evidence package is bound to the ledger. `atj event status` reports "units: none recorded" and `atj event unit … list` reports "0 unit(s), 0 stale", while `atj/event.py:derive_digests` computes `evidence:team-podcast` = `8ef5c7965cda164f` and `evidence:team-ledger` = `b7acf0d1666295f5` from what is on disk right now. With no recorded `input_digest`, `check_staleness` has nothing to compare against: a manifest edited after this gate passes will not be detected, and the judging stage's inputs are not pinned to what was audited. The prose Team progress table records package IDs, but `atj` does not read prose. | Before recording the gate, run `python3 -m atj event unit events/live-trial-2026 record --id evidence:team-podcast --stage evidence --output evidence/team-podcast/manifest.md --audit-result <this audit's result>` and the same for `evidence:team-ledger`. Confirm `atj event unit … list` then shows 2 units, 0 stale. |
| major (F4) | `framework/policies/evidence-and-citation.md`: "Every material conclusion must be traceable to the pinned evidence package"; `framework/templates/evidence-manifest.md` Validation: "Artifact references resolve" | `events/live-trial-2026/evidence/team-ledger/manifest.md`, Requirements and team claims | Nine of sixteen requirement rows cite at least one evidence ID that does not contain the claimed observation. R2 (`fin ingest-amazon`) cites ev-ledger-04, which is the CSV ingest-rejection observation; Amazon ingest is ev-ledger-06. R3 (tiered matcher) cites ev-ledger-04 and ev-ledger-05; matching is ev-ledger-06. R4 (D0) cites ev-ledger-04; D0 is ev-ledger-03 and ev-ledger-06. R6 (`render`) and R7 (`analyze`) cite ev-ledger-06; both are ev-ledger-07. R8 cites ev-ledger-06 alongside the correct ev-ledger-07. R9 (`fin sql`) cites ev-ledger-04; the `sql` invocation is in ev-ledger-06's run record. R10 (`fin status`) cites ev-ledger-01 and ev-ledger-03; `status` appears in ev-ledger-02 and ev-ledger-04. R13 (the tier-0 documentation contradiction) cites ev-ledger-05; that finding rests on ev-ledger-06 and ev-ledger-16. The right observation exists in the same document in every case, so nothing is unsupported — but a judge following a citation lands on the wrong run record, and this is the table feeding the 25-point `functional` criterion. `atj validate reports` cannot catch it: the IDs exist, so the reference resolves. The manifest is marked `approved`/`valid` with "Artifact references resolve" ticked. | Repoint each of the nine rows at the observation that contains the behavior. Re-tick the Validation box only after walking every `[[evidence:…]]` target and confirming it contains the claim made of it. The team-podcast table was checked the same way and is correct throughout. |
| minor (F5) | `framework/policies/evidence-and-citation.md`: evidence classes and confidence must reflect what was actually observed | `events/live-trial-2026/runs/team-podcast-e2e-full-01.json`, `team-podcast-e2e-02.json`; team-podcast manifest ev-podcast-16, -17 | Two sandbox containers ran concurrently during the measurement behind an unresolved finding. `e2e-full-01` ran 00:15:30-00:17:26 and `e2e-02` ran 00:16:15-00:19:19 — a 71-second overlap on a host where each container is capped at `--cpus 1.0`, and the 90-second `wait_for_function` that produced ev-podcast-16's download stall falls inside it. The contrasting one-second download in ev-podcast-17 ran alone at 00:19:27. The manifest offers exactly two explanations for the difference, "single-vs-two-episode flakiness or a real defect", and never mentions that the slow run shared the host with a second Chromium and uvicorn while the fast one did not. Timing-sensitive evidence should not be gathered concurrently. | Record the overlap in ev-podcast-16, or re-run `e2e-full-01` in isolation and let the result stand or fall on its own. Either way this strengthens rather than weakens F2. |
| minor (F6) | `events/live-trial-2026/event.md`, approved-images table: "a deviation from this table is visible at the judgments audit" | `events/live-trial-2026/event.md`; team-podcast manifest ev-podcast-02, -03, -11 | Three run records still carrying current evidence ran on the superseded image. `server-boot-01`, `media-progress-01` and `runsh-attempt-01` all used `podcast:2` (`5ff34ae63320`), which `event.md` no longer lists as approved for this team, and `Containerfile.podcast` was overwritten in `3dd629c`, so `:2`'s recipe is no longer in the repository. ev-podcast-03 is the only evidence for req-02 and req-04. The results are almost certainly unaffected — `:3` is `:2` plus ffmpeg — but "almost certainly" is not recorded anywhere, and the Tests table does not mark those three rows as superseded-image results the way `e2e-attempt-01` is marked. Separately, the runtime facts in ev-podcast-01 (fastapi 0.141.1, pydantic 2.13.5, uvicorn 0.53.0, Chromium 152.0.7977.82) were observed on `:2` only; `env-probe-02` checked ffmpeg and tmpfs on `:3` and nothing else, and `Containerfile.podcast` pins no versions, so nothing establishes that `:3` carries the runtime the manifest attributes to it. | List both `podcast:2` (`5ff34ae63320`) and `podcast:3` (`c3670644bc7b`) in `event.md` with the scope and date of each, or re-run the three on `:3`. Re-probe the Python and Chromium versions on `:3` and record them. Mark the three Tests rows with the image they used, as the `e2e-attempt-01` row already is. |
| minor (F7) | `framework/policies/evidence-and-citation.md`: evidence class must match what was demonstrated; the manifest's own precedent at R11 ("Direct observation, partial") | `events/live-trial-2026/evidence/team-ledger/manifest.md`, R3, R6, ev-ledger-01 | Three rows claim more coverage than the runs show. R3 names a tiered matcher including subset-sum and is marked "Direct observation"; `src/fin/match/engine.py:9` declares `tier 3 SUBSET_SUM` and `subset_sum_edges` at line 173, and the run exercised only REFERENCE, AMOUNT_DATE_UNIQUE and UNMATCHED. R6 names five report kinds and is marked "Direct observation"; `runs/team-ledger-analyze-render-dispute-01.json` shows "wrote 3 markdown reports" — no reconciliation report and no per-statement report, because that scenario had neither a merchant feed nor an ingested statement. ev-ledger-01 says "all 9 subcommand `--help` screens" and then lists ten subcommands; argparse in `envcheck-02` shows ten. The manifest gets this exactly right at R11, so the convention exists and these three rows depart from it. | Mark R3 and R6 "Direct observation, partial" and name what was not exercised. Correct the subcommand count to ten. |
| minor (F8) | intake audit F3's required repair: "for the amendment name the time and the authorizing official"; configuration audit F5: a ledger row may not misstate when work happened | `events/live-trial-2026/status.md`, Activity log | The ledger is incomplete and out of order. Neither amendment row names an authorizing official — not the approved-images row at 2026-09-16T23:49:05Z, which intake F3 asked for explicitly, nor the ffmpeg row at 2026-09-17T00:10:14Z, which repeats the omission for a second amendment to the same gated section. The log is also not chronological: the rows stamped 00:15:00 and 00:20:00 sit above four rows stamped 00:10:14. And the 00:20:00 row describes the five-run `podcast:2` package as a completed deliverable with "`atj validate reports` PASS, 0 blocking" and no superseded marker, while the marker sits on a different row further down. A reader reconstructing the sequence from this ledger gets the wrong order and may treat a superseded package as current. | Name the authorizing official on both amendment rows. Restamp or reorder the log so rows ascend. Mark the 00:20:00 row superseded, as the 00:10:14 first-pass row already is. |
| minor (F9) | intake audit F5, unclosed and now propagated | `events/live-trial-2026/evidence/team-podcast/manifest.md`, ev-podcast-09 | The evidence package repeats an error the intake audit already found. ev-podcast-09 describes `.agentic/project.yaml` as "five inert metadata lines" and cites it as "(full file, 5 lines)"; `wc -l` gives 6 and the file has six keys — `schema_version`, `project_id`, `slug`, `kind`, `created_at`, `created_on`. Intake F5 flagged precisely this ("described as five lines and is six"). The substantive finding — the file is inert metadata with no instruction to an agent — is correct and I re-verified it. | Correct to six lines and six keys. Re-check the other line anchors intake F5 listed before judging begins, since judges will quote them. |

## Advisories

**A1 — run timeouts above the module default are still unjustified, closing
nothing on intake A6.** `atj/sandbox.py:52` sets `timeout_seconds: 120`. Five
runs exceed it: `team-podcast-e2e-02`, `-03` and `-04` at 780 seconds, six and a
half times the default; `e2e-full-01` at 400; `team-ledger-pytest-01` at 300.
The podcast Tests table lists a timeout for its 60s, 90s, 120s and 400s rows and
omits it for exactly the three 780s rows; the ledger table says only "capped
CPU/memory/pids/time". Nothing was harmed and every applied limit is in its run
record, which is why this is an advisory and not a finding. Intake A6 asked for
a sentence of justification in the evidence package. Add it — a browser
automation suite legitimately needs longer than a CLI, and saying so costs one
line.

**A2 — two podcast observations assert detail the run record does not
contain.** ev-podcast-03 says a malformed `Range` header "is rejected with
`400`"; the record captured only `"exception": "HTTPException: malformed Range
header"`. The claim is true — `server/app.py:164` and `:168` raise
`HTTPException(400, "malformed Range header")` — but it is a source read
standing in an observation row without the source cited for that specific
point. ev-podcast-02 says `/sw.js` is served "with correct headers"; the record
captured a status code and a body prefix, no headers. The ledger package has the
same shape at ev-ledger-07, where the 22.49% APR comes from
`config/accounts.example.yaml:14` rather than the run. Cite the source line
beside the run record when an observation leans on both.

**A3 — the two packages editorialize unevenly.** ev-ledger-05 calls its finding
"a real judgment-relevant reliability/engineering gap, not a hypothetical one",
naming two rubric criteria and pre-weighing the finding. The observation is
accurate and valuable; the framing is not the manifest's job. The podcast
package does the same job better — "recorded as inconclusive rather than a
confirmed defect" — and is the model to follow. No score is stated anywhere in
either package, so this is a matter of degree, not a boundary breach.

**A4 — record why one environmental gap was closed and another was not.** The
operator amended the approved image twice to remove disadvantages caused by a
missing declared prerequisite, and declined to move the 64 MB tmpfs that blocks
full-library testing for one team only. Both decisions are right, for different
reasons: a missing README prerequisite is an operator error to fix, while a
framework-wide resource cap applied identically to everyone is not something to
move mid-event for one team. ev-podcast-18 makes the second half of that
argument well. Put the distinction in `event.md` so the panel does not have to
infer it.

**A5 — privacy passes now; two items to carry to publication.** All 22 run
records embed the absolute host path
`/home/gregg/Nextcloud/workspace/Software_Dev_Tournament/workspaces/…` and the
`65534:65534` uid map, and configuration A7's note about the operator's name in
`event.md` still stands. Both are correct in private artifacts. Run `atj
validate publication` on anything that would leave the panel.

**A6 — the podcast manifest names the other team.** Scope and provenance cites
the `poppler-utils` precedent to justify ffmpeg. That is fairness
documentation, contains no finding or result about team-ledger, and the ledger
package carries no podcast material at all. Keep it out of any team-facing
dossier, where a team has no reason to read about another team's image.

**A7 — `evidence_package_id` cannot be checked at audit time.**
`atj/ids.py:98-104` promises the ID changes whenever recorded evidence changes,
"which is what marks downstream judgments stale". Neither this event's IDs nor
the committed sample event's IDs equal a digest of the manifest file, so the
digest input is not reproducible from the artifact and the guarantee cannot be
verified by an auditor. This is a framework observation, outside this stage's
scope, and it is the reason F3 matters: with the ID unverifiable, the
`evidence:` units are the only working staleness detection this event has.

## Completion gate

- [ ] No blocking findings — none raised
- [ ] No major findings — F1, F2, F3 and F4 are open
- [x] Calculations valid — no official arithmetic exists at the evidence stage;
      no score, weight or total was computed, and nothing in either package
      presents one. The arithmetic I did check reconciles: $20.68 − $5.00 =
      $15.68 in D0, $0.29 interest against `apr_bp: 2249`, 578.896009s duration
      against the 578.9s clamp, 4884617 transcoded bytes matching the OPFS file
      byte for byte, and 56 source files / 2.2 GB against a 64 MB tmpfs
- [ ] Evidence references resolve — every `runs/*.json` path cited by either
      manifest exists, and every sampled observation I followed was present and
      accurately stated. But nine of sixteen team-ledger requirement rows point
      at the wrong observation (F4), and three claim coverage the runs do not
      show (F7)
- [x] Version and identity checks pass — both checkouts match their pinned
      commits, `framework_commit` resolves and is consistent across every
      artifact, `rubric: submission-evaluation@1.0.0` and `persona:
      prepare-submission@1.1.0` match `framework/personas.md`,
      `atj personas` PASS on all 15 components, `atj release-check` PASS
- [x] Privacy boundary passes — `public/` holds only `.gitkeep`, every artifact
      is `visibility: private`, no personal identifier appears in any evidence
      artifact, and neither team's material appears in the other's package

**FAIL.** Repairs required, in order:

1. Add `poppler-utils` to `Containerfile.ledger` and reconcile the image ID (F1).
2. Set `evidence_limited_criteria: [reliability]` in the team-podcast manifest
   and state the basis (F2).
3. Repoint the nine misdirected evidence citations in the team-ledger
   requirements table (F4), and mark R3 and R6 partial (F7).
4. Record both `evidence:` units in the ledger, then re-run
   `atj event unit … list` and confirm 2 units, 0 stale (F3).
5. Close the minors: note the concurrent runs (F5), account for the three
   `podcast:2` records (F6), complete and reorder the activity log (F8), fix
   the five-versus-six line count (F9).
6. Re-audit, then record the gate with `atj event gate`.

Nothing here requires re-running a submission except by choice: F5 and F6 can be
closed by recording what happened instead of re-executing, though re-running
`e2e-full-01` alone would settle a question the package currently leaves open.
