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
framework_commit: 44e5f87b090c8b1bd5c691677980419230c286c8
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-17T18:42:00Z"
completed_at: "2026-09-17T18:50:00Z"
visibility: private
approval_state: approved
validation_state: valid
result: FAIL
---
# Judging Audit — evidence stage (re-audit after repair)

This replaces the first-pass report of 2026-09-17. Finding codes F1-F9 and
A1-A7 are carried from that report so the history stays traceable. New findings
are coded F10 onward and A8.

## Result

**FAIL**, on two major findings that the repair did not reach.

The four majors the first pass raised are genuinely fixed. F1's reconciliation
is real and I verified it independently against `podman history`. F2's
`evidence_limited_criteria: [reliability]` is now correct and its new third
outcome is stated accurately and hedged properly. F3's units bind. F4's nine
misdirected citations are all repointed to observations that contain the claim.
Seven of the nine findings and four of the seven advisories are closed.

Two things block the gate, both found by doing the wider walk the repair brief
asked for and the repair itself did not complete:

- **F10** — the re-walk of the team-ledger requirements table covered the nine
  rows the first audit named and not the other seven. R1, R5 and R12 still cite
  observations that do not contain the claim, and R12's principal claim has no
  supporting evidence row anywhere in the package.
- **F11** — `ev-podcast-21`, one of the two evidence rows added by this repair,
  states a `playwright` version that no run record produced and that the one
  run record carrying a playwright version contradicts.

Nothing here is a safety failure, nothing reached `public/`, and no scoring
arithmetic exists yet to be wrong. Both repairs are small.

## Scope and artifacts inspected

- The first-pass report at this path, as the specification for this re-audit.
- `git show --stat 44e5f87`, `git diff a82ea17..44e5f87` — every changed line.
- `events/live-trial-2026/event.md`, `status.md`, `status.md.bak`, `teams.md`
- `events/live-trial-2026/evidence/team-podcast/manifest.md` (21 evidence IDs),
  `evidence/team-ledger/manifest.md` (19 evidence IDs, 16 requirement rows)
- `events/live-trial-2026/evidence/Containerfile.ledger`, `Containerfile.podcast`
- All 27 run records in `events/live-trial-2026/runs/` — 11 ledger, 16 podcast.
  The five added by this repair were read in full.
- `podman history --no-trunc` for `ledger:2`, `podcast:2` and `podcast:3`
- `workspaces/live-trial-2026/team-podcast/.agentic/project.yaml` (F9)
- `git diff 152dd2c1..HEAD -- framework/ schemas/ atj/ VERSION` and the
  `atj render judgment` implementation added in `3a798ad`
- `framework/templates/audit-report.md`, `framework/personas.md`,
  `framework/policies/evidence-and-citation.md`,
  `framework/rubrics/submission-evaluation.md`

I did not re-read any judgment, bracket or publication artifact. None exists.
I did not re-verify the sampled observations the first pass already walked and
found exact, except where this repair changed the row.

## Deterministic validation results

Re-run, not taken on trust.

| Command | Result |
|---|---|
| `python3 -m atj event validate events/live-trial-2026` | PASS, 0 problems, stage evidence |
| `python3 -m atj validate reports events/live-trial-2026` | PASS, 7 artifacts, 0 blocking / 0 major / 0 minor / 0 advisory |
| `python3 -m atj release-check` | PASS — single-source PASS, version-skew PASS, sample event PASS |
| `python3 -m atj event unit events/live-trial-2026 list` | 2 unit(s), 0 stale — `evidence:team-podcast` and `evidence:team-ledger`, both `complete`, both `not-audited` |
| `python3 -m atj event status events/live-trial-2026` | stage evidence, `units: {'complete': 2}`, gate `evidence-validated` pending |
| `python3 -m pytest tests/ -q` | 351 passed, 51 subtests passed |

The validators still cannot reach F10 or F11. `atj validate reports` checks that
an `[[evidence:ID]]` target exists, not that it contains the claim made of it,
and it has no view on whether an observation matches its own run record. That
gap is the reason both majors survived a repair whose commit message says they
were checked.

## F1 — the `podman history` reconciliation, verified independently

The operator's claim is that `Containerfile.ledger` was reconciled against
`podman history localhost/atj-live-trial/ledger:2` rather than by rebuilding. I
checked this rather than accepting it.

`podman history --no-trunc localhost/atj-live-trial/ledger:2` shows, top down:

1. layer `7780b2b9e6e1…` — `pip install --no-cache-dir "pyyaml>=6.0" "duckdb>=1.0" "pytest>=8.0"`
2. layer `7e1b52138efd…` — `apt-get update && apt-get install -y --no-install-recommends poppler-utils  && rm -rf /var/lib/apt/lists/*`, whose `COMMENT` column is `FROM docker.io/library/python:3.12-slim`
3. everything below is the stock `python:3.12-slim` base, `PYTHON_VERSION=3.12.14`

The committed recipe is `FROM docker.io/library/python:3.12-slim`, then the
poppler-utils apt layer, then the pip layer. That is the same two `RUN`
commands, in the same order, on the same base, character for character
including the double space the `\` line continuation produces before `&& rm`.
The top layer ID is the image ID `event.md` records. The recipe now describes
the image the evidence ran on.

**"Verified against build history instead of rebuilt" is the correct closure
here, not a deferral.** A rebuild would not have proved anything about
`7780b2b9e6e1`; it would have produced a different image and left the question
of what built the old one exactly where it was. `podman history` answers that
question directly, and the operator's reason for not rebuilding — new apt and
pip resolutions, a new image ID, 11 invalidated run records — is sound. I
applied the same check to `podcast:2` and `podcast:3` and it holds there too:
the two differ only by `ffmpeg` in the apt layer, and the pip layer command is
identical.

One residual, which `event.md` already states and I am not raising as a
finding: neither recipe pins versions, so neither is byte-reproducible. The
image ID, not the recipe, is what makes a silent rebuild detectable. That is
recorded and correct.

## F4 re-walk — all sixteen team-ledger requirement rows

The repair brief asked for all sixteen, not the nine the first audit named. All
sixteen, with the evidence IDs each now cites:

| Row | Cites | Verdict |
|---|---|---|
| R1 | ev-ledger-01, -02 | **Wrong. See F10.** Neither contains "verifying control totals when present" (ev-ledger-02 is the *absent* case, `UNVERIFIED`) nor "rejecting outright rather than partially importing" (that is ev-ledger-04's "no partial import"; the control-total gate is ev-ledger-08) |
| R2 | ev-ledger-06 | Correct — Amazon ingest is in ev-ledger-06 |
| R3 | ev-ledger-06, -15 | Correct, and correctly marked "Direct observation, partial" with `SUBSET_SUM` named as unexercised |
| R4 | ev-ledger-03, -06 | Correct — D0 is in both |
| R5 | ev-ledger-01, -03 | **Undercited. See F10.** ev-ledger-03 says only "all invariants hold"; idempotence is demonstrated in ev-ledger-04, which is not cited. ev-ledger-01 is the help surface |
| R6 | ev-ledger-07 | Correct, and correctly marked partial with the two unwritten report kinds named |
| R7 | ev-ledger-07 | Correct |
| R8 | ev-ledger-07, -17 | Correct |
| R9 | ev-ledger-06 | Correct — I confirmed `=== sql: matches ===` and its three-row result are in `runs/team-ledger-amazon-match-detect-01.json` |
| R10 | ev-ledger-02, -04 | Correct — `fin status` appears in both |
| R11 | ev-ledger-08, -09 | Correct, unchanged, already the model row |
| R12 | ev-ledger-10 | **Wrong. See F10.** ev-ledger-10 is an injection-phrasing grep of `.claude/skills/*/SKILL.md` and `hooks/pre-commit`. It does not look at `src/fin/` and does not search for network, HTTP or model-API calls |
| R13 | ev-ledger-06, -16 | Correct |
| R14 | ev-ledger-11 | Acceptable. The dispute-CSV `0600` half is in ev-ledger-07 rather than ev-ledger-11; both are in the package and the row's substance holds. Folded into F10's repair as a courtesy, not a separate finding |
| R15 | none | Correct — labelled a team claim, no citation required |
| R16 | none | Labelled part team claim, part "direct observation (repeat grep)". The observation half has no evidence ID. Same root cause as R12; folded into F10 |

The nine rows the first audit named are all fixed. Three of the other seven are
not.

## F11 — an unsupported version in a new evidence row

`ev-podcast-21`, added by this repair, reads: "The approved image
`localhost/atj-live-trial/podcast:3` carries exactly the runtime
`ev-podcast-01` recorded on the superseded `:2`: Chromium 152.0.7977.82, Python
3.12.14, Debian 13 (trixie), `fastapi` 0.141.1, `pydantic` 2.13.5, `uvicorn`
0.53.0, `starlette` 1.6.0, `playwright` 1.56.0 …", class "direct observation
(execution)", confidence "high", reproduction
`runs/team-podcast-env-probe-03.json`.

Every value in that list is confirmed by that run record except the last one.
`env-probe-03`'s probe of `playwright.__version__` **failed**; its `stderr` is:

```
AttributeError: module 'playwright' has no attribute '__version__'
```

So the cited record produced no playwright version at all. The only run record
in the event that carries one is `runs/team-podcast-server-boot-02.json`, also
added by this repair, whose first two lines of stdout are `PLAYWRIGHT:` and
`1.63.0`. The string `1.56.0` appears nowhere else in the event directory or in
either checkout. `ev-podcast-01` on `:2` recorded only "playwright ok", with no
version, so there is no earlier measurement it could have been copied from —
and because `Containerfile.podcast` pins `"playwright>=1.50"`, the `:2` and `:3`
pip layers resolved independently and cannot be assumed equal anyway.

The rest of ev-podcast-21 is sound, including its `podman history` claim, which
I verified: `:2` and `:3` differ only by `ffmpeg` in the apt layer.

## Repairs checked for weakening an accurate finding

I compared the diff against the first report's text. Nothing accurate was
removed or softened into uselessness:

- `ev-ledger-05` (A3) lost the phrase "a real judgment-relevant
  reliability/engineering gap, not a hypothetical one" and gained "Recorded as
  observed; how much it matters is the panel's call." The observation itself —
  two of four rejection paths surface as a traceback — is intact and still
  stated at high confidence. Editorializing removed, finding preserved. Correct.
- `ev-podcast-02` (A2) lost "with correct headers" and gained the actual
  captured headers from `server-boot-02`. Strengthened, not weakened.
- `ev-podcast-03` (A2) now separates the run record's
  `HTTPException: malformed Range header` from the `400` status read at
  `server/app.py:164,168`. Correct.
- `ev-podcast-01` and `ev-podcast-11` gained superseded-image labels rather
  than losing content.
- `ev-podcast-16` (F5) gained the overlap disclosure verbatim and accurately:
  "this run (00:15:30-00:17:26) overlapped `runs/team-podcast-e2e-02.json`
  (00:16:15-00:19:19) by 71 seconds". Both windows match the run records.

## The five new run records

All five are genuinely sandboxed. Each carries, in its own `command` field,
`--network none`, `--read-only`, `--tmpfs /tmp:rw,noexec,nosuid,size=64m`,
`--cap-drop ALL`, `--security-opt no-new-privileges`, `--user 65534:65534`,
`--pids-limit 256`, `--memory 1g`, `--cpus 1.0`, and a single
`…/workspaces/live-trial-2026/team-podcast:/submission:ro,Z` mount and no
other. None contains `--privileged`, `--network=host`, `--userns=host` or
`--cap-add`. `runtime: podman`, `runtime_version: 6.1.0`, `timed_out: false`
throughout. Each is cited by the manifest that claims it.

The "identical results" claim, checked by comparing the records field by field:

- `runsh-attempt-02` vs `-01` — byte-identical on every field except the
  timestamps, image and command. Identical.
- `media-progress-02` vs `-01` — byte-identical on the same basis. Identical.
- `server-boot-02` vs `-01` — **not identical, and better.** The command was
  extended to capture response headers and `/manifest.webmanifest`, closing A2.
  All four original routes return the same statuses and the same body prefixes.
  Consistent and a superset, not identical. `event.md` says "with identical
  results" for all four; the manifest's own Tests row says "capturing response
  headers", which is accurate. See A8.
- `env-probe-03` — confirms on `:3`: `/usr/bin/ffmpeg`, `/usr/bin/ffprobe`,
  Chromium 152.0.7977.82, Python 3.12.14, Debian 13 trixie, fastapi 0.141.1,
  pydantic 2.13.5, uvicorn 0.53.0, starlette 1.6.0, tmpfs 64M. Every version
  `ev-podcast-01` attributed to the runtime is now measured on the approved
  image. Only playwright failed to report (F11).
- `e2e-full-02` — a real, isolated third execution. Transcode of both episodes
  succeeded (4,884,617 and 6,690,229 output bytes, 6.9s and 10.4s, 12 MB in the
  64 MB tmpfs), stage 1 ran all five checks with output preserved, stage 2
  passed, and stage 3 ended with
  `playwright._impl._errors.Error: Page.wait_for_function: Target crashed`.
  Wall clock 18:36:04 to 18:36:28, 24 seconds, consistent with the "24.5s" the
  manifest states.

`ev-podcast-20` states all of this accurately and **does not overclaim**. It
says the crash "is most readily explained by the sandbox's resource cap, but
that is an inference: no memory measurement was taken at the moment of the
crash, and no run has been observed to complete." That is the right handling
and it is what makes F2's closure sound rather than nominal.

## Both manifests still validate and still state no score

`atj validate reports` passes on 7 artifacts. Neither manifest states,
recommends or implies a score. The only occurrences of the word are the
team-podcast manifest's own reasoning about why `reliability` is
evidence-limited — "a judge could defend a low score or a high one, which is
what `NE` is for" — and "rather than treat any score as fully executed". Both
are statements about evidence sufficiency addressed to the panel, not scores.

`public/` holds only `.gitkeep`. Every artifact in scope is
`visibility: private`. No operator name, email or personal identifier appears
in either manifest or any of the 27 run records. The five new records embed the
same absolute host path the other 22 do, which remains correct in a private
artifact and is carried at A5.

## `atj render judgment`, added mid-event in `3a798ad`

**Acceptable.** I checked the whole delta, not the commit message.
`git diff 152dd2c1..HEAD -- framework/ schemas/ atj/ VERSION` is 49 added lines
in `atj/cli.py` and nothing else. `framework/rubrics/`, `framework/personas.md`
and `VERSION` are byte-identical between the commit the evidence packages pin
and HEAD. The rule in `CLAUDE.md` — do not change an active event's rubric
version, weights, personas, bracket policy or evidence after judging begins —
is not engaged: none of those changed, and judging has not begun.

The command itself adds no arithmetic. `cmd_render_judgment` reads front
matter, calls the existing `scoring.Judgment.from_metadata` and
`scoring.individual_score`, calls the existing
`render.individual_scores_table`, and replaces only the `atj:scores` generated
block. `atj/scoring.py` and `atj/render.py` are untouched. `release-check`
reports sample event PASS and 351 tests pass, which is what exercises the
byte-for-byte reproduction claim.

On the version skew: judgments will record `framework_commit: 44e5f87` or later
while the evidence packages record `152dd2c1`. That is fine and should simply
be stated in the judging audit, because the delta between those two commits is
an additive CLI subcommand with no effect on any evidence artifact, any
criterion, any weight or any total. `atj release-check` version-skew passes.

## Carryover

`configuration/intake A7` — the operator's name in `event.md` must not reach
`public/` — is still open by design and still correct. Every other prior-stage
item the first pass tracked stays as that report left it, except intake F3
(authorizing official), which the F8 repair closes: both image-amendment rows
now name the event-director.

## Findings

| Severity | Rule | Artifact | Finding | Required repair |
|---|---|---|---|---|
| major (F10) | `framework/policies/evidence-and-citation.md`: "Every material conclusion must be traceable to the pinned evidence package"; the F4 repair's own standard, "walking every `[[evidence:…]]` target and confirming it contains the claim made of it" | `events/live-trial-2026/evidence/team-ledger/manifest.md`, R1, R5, R12 (and R14, R16) | The re-walk covered the nine rows the first audit named and stopped there. R12 is the serious one: its principal claim — "the deterministic `fin` package makes no network, HTTP, or LLM API calls" — cites only ev-ledger-10, which is a grep of `.claude/skills/*/SKILL.md` and `hooks/pre-commit` for *injection phrasing*. It does not examine `src/fin/` and does not search for network or model-API calls. No evidence row anywhere in the package records that grep, although the Missing-evidence section attributes it to ev-ledger-10 twice more ("confirmed by grep, ev-ledger-10 and intake"; "this preparation's own grep, ev-ledger-10 … found no `os.environ` read in `src/fin/`"). R12 feeds `agentic` and `security`. R1 cites ev-ledger-01 (help surface) and ev-ledger-02 for a claim whose control-total clause is ev-ledger-08 and whose no-partial-import clause is ev-ledger-04. R5 cites ev-ledger-03 for three named invariants, of which idempotence is demonstrated only in ev-ledger-04. R14's dispute-CSV `0600` half sits in ev-ledger-07, not the cited ev-ledger-11; R16 asserts a direct observation with no ID. The Validation box "Artifact references resolve" is ticked on the strength of a walk that did not happen for these rows. | Add the `src/fin/` network/HTTP/model-API/`os.environ` grep as its own observation row, or extend ev-ledger-10's observation text to record it, and cite that from R12 and from the two Missing-evidence bullets. Add ev-ledger-04 and ev-ledger-08 to R1. Add ev-ledger-04 to R5. Add ev-ledger-07 to R14 and an ID to R16's observation half. Then re-tick the Validation box against all sixteen rows. |
| major (F11) | `framework/policies/evidence-and-citation.md`: evidence classes and confidence must reflect what was actually observed; `framework/templates/evidence-manifest.md`: an observation's Reproduction column is the record it came from | `events/live-trial-2026/evidence/team-podcast/manifest.md`, ev-podcast-21 | The row states `playwright` 1.56.0 on `podcast:3` as a "direct observation (execution)" at "high" confidence, reproduced by `runs/team-podcast-env-probe-03.json`. That run's playwright probe raised `AttributeError: module 'playwright' has no attribute '__version__'` and returned no version. The only run record in the event carrying a playwright version is `runs/team-podcast-server-boot-02.json`, which reports **1.63.0**. `1.56.0` appears nowhere else in the event directory or in either checkout, and `ev-podcast-01` on `:2` recorded only "playwright ok", so there is no prior measurement it restates. Because `Containerfile.podcast` pins `"playwright>=1.50"`, the `:2` and `:3` pip layers resolved separately and equality cannot be assumed either. The row's whole purpose is to assure judges that `:3`'s runtime equals the one `ev-podcast-01` recorded; one of its eight values is unmeasured and contradicted. Everything else in the row is confirmed, including the `podman history` layer-equality claim. | Replace `playwright 1.56.0` with `playwright 1.63.0` and cite `runs/team-podcast-server-boot-02.json` for it, or drop the playwright entry and record that `env-probe-03`'s version probe failed. State plainly that `ev-podcast-01` never captured a playwright version, so no `:2`-vs-`:3` comparison is available for that package. |
| minor (F12) | `CLAUDE.md`, Source of truth: "Event state … `events/<event>/status.md`" and "There is exactly one editable copy of each" | `events/live-trial-2026/status.md.bak` | The repair commit added and committed a 99-line `status.md.bak`. It is a second copy of the event ledger and it is already stale: it is identical to `status.md` except that it is missing the `evidence:team-ledger` unit block, so it records one unit where the ledger records two. The first-pass report noted "the stray `status.md.bak` is gone" as a passing observation; this reintroduces it and puts it under version control. `atj release-check` single-source passes, so nothing automated catches it, and the `.claude/hooks/` guard on event artifacts does not cover a `.bak` suffix. No private information beyond what `status.md` already holds. | `git rm events/live-trial-2026/status.md.bak`. If a backup is wanted during edits, keep it outside the event directory or add `*.bak` to `.gitignore`. |

## Disposition of the first-pass findings

| Code | Disposition | Basis |
|---|---|---|
| F1 | **Closed** | `podman history` for `ledger:2` shows exactly the two `RUN` layers the committed recipe now contains, in order, on the same base, with the top layer ID equal to `7780b2b9e6e1`. Reconciliation without rebuild is the right closure, and the reasoning is recorded in `event.md` and `status.md`. |
| F2 | **Closed** | `evidence_limited_criteria: [reliability]`, with the basis written into Missing or inaccessible evidence and naming all three outcomes. `ev-podcast-20` states the third one accurately against `e2e-full-02` and labels the resource-cap explanation an inference with no measurement behind it. It does not overclaim. |
| F3 | **Closed as to mechanism; one step outstanding** | `atj event unit … list` shows 2 units, 0 stale, and the recorded digests (`259d298fbae6db7f`, `36f69f52d934b790`) differ from the first pass's, so they bind the repaired manifests rather than the audited-and-failed ones. Both still carry `audit_result: not-audited` and must be re-recorded with this audit's result. Repairing F10 and F11 will change both digests, so re-record after the repair, not before. |
| F4 | **Closed** | All nine rows repointed and each verified against the run record behind the target. See the sixteen-row table above. The three rows that remain wrong are ones F4 did not name; they are F10. |
| F5 | **Closed** | `ev-podcast-16` now records the 71-second overlap with `e2e-02`, both windows matching the run records, and names host contention as a third candidate explanation. The isolated repeat is cross-referenced. |
| F6 | **Closed** | All four `podcast:2` runs repeated on `:3`. `runsh-attempt-02` and `media-progress-02` are byte-identical to their originals; `server-boot-02` is consistent and a deliberate superset; `env-probe-03` measures the `:3` runtime directly. `podcast:2` is listed in `event.md` with its scope and the five records that used it. The one defect in the new material is F11. |
| F7 | **Closed** | R3 and R6 are "Direct observation, partial" with `SUBSET_SUM` and the two unwritten report kinds named specifically. The subcommand count is ten in both `ev-ledger-01` and the Tests table. |
| F8 | **Partially closed** | Ordering and attribution are fixed: the log now ascends, both image-amendment rows name the event-director (closing intake F3), and the five-run `podcast:2` package is marked SUPERSEDED. Three accuracy problems remain. (a) Four rows are stamped **after the commit that contains them** — 18:45:00Z, 18:50:00Z, 18:55:00Z and 19:00:00Z, against a commit at 18:41:56Z and `last_updated: 18:41:16Z`. (b) The audit row is stamped 14:10:00Z while `audits/evidence.md` records `completed_at: 18:35:00Z` and its commit is 18:32:58Z, a 4h25m misstatement. (c) The new closing note says "Execution timestamps in this log are the completion time of the last run record the row describes"; that is false for the two team-ledger rows at 00:15:00Z (last ledger run completed 00:04:39Z) and for the six rows that describe no run record at all. This is the third appearance of the rule from configuration F5. Not blocking on its own. Repair: restamp the four future rows at or before 18:41:16Z, correct the audit row to 18:35:00Z, and narrow the closing note to the rows it actually describes. |
| F9 | **Closed** | `ev-podcast-09` says "six inert metadata lines, six keys" and "(full file, 6 lines)". `wc -l` on the file is 6 and it has six keys. |
| A1 | **Closed** | The timeout paragraph is in the podcast manifest and is accurate: three 780s runs and two 400s runs are browser-automation runs, the 300s pytest run predates the preparation. |
| A2 | **Closed** | `ev-podcast-02` carries real captured headers; `ev-podcast-03` separates the record's `HTTPException` from the `400` read at `server/app.py:164,168`; `ev-ledger-07` cites `config/accounts.example.yaml:14` for the APR and says the record carries the computed $0.29, not the rate. |
| A3 | **Closed** | `ev-ledger-05` no longer names rubric criteria or pre-weighs itself. The observation is unchanged. |
| A4 | **Closed** | `event.md` now records why a missing declared prerequisite was fixed by amending the image while the 64 MB tmpfs cap was not. |
| A5 | **Carried forward** | Still correct. All 27 run records embed the absolute host path and the `65534:65534` uid map; configuration A7's note about the operator's name in `event.md` stands. Both are fine in private artifacts. Run `atj validate publication` on anything leaving the panel. |
| A6 | **Carried forward** | The podcast manifest still cites the `poppler-utils` precedent when it explains the ffmpeg amendment. Fairness documentation, no finding about the other team. Keep it out of a team-facing dossier. |
| A7 | **Carried forward** | `evidence_package_id` still cannot be reproduced from the artifact by an auditor, so the `evidence:` units remain this event's only working staleness detection. A framework observation, outside this stage. |

## Advisories

**A8 — `event.md` says "identical results" for four repeats where one is a
superset.** `server-boot-02` was deliberately extended to capture response
headers and `/manifest.webmanifest`, which is how A2 was closed. Its results are
consistent with `server-boot-01` — same four routes, same statuses, same body
prefixes — but the run is not identical and the word invites a reader to think
it was. The manifest's own Tests row gets this right ("capturing response
headers"). Match `event.md` to the manifest.

**A9 — `atj render judgment` writes in place with no dry-run.**
`cmd_render_judgment` rewrites the judgment file whenever the rendered block
differs, and nothing checks `approval_state` first. At the judging stage that
means a re-render can silently rewrite the official scores table of an approved
judgment. The command is correct for this event and adds no arithmetic; this is
a framework note for whoever writes the judging audit, not an evidence-stage
finding.

## Completion gate

- [x] No blocking findings — none raised. Execution integrity is clean across
      all 27 run records; the five new ones were checked flag by flag
- [ ] No major findings — F10 and F11 are open
- [x] Calculations valid — no official arithmetic exists at the evidence stage
      and neither package presents a score. The arithmetic I re-checked in the
      new material reconciles: 4,884,617 + 6,690,229 output bytes against the
      "12 MB combined" and the 18% tmpfs occupancy `df` reports; 24 seconds of
      wall clock in `e2e-full-02` against the "24.5s" the manifest states; the
      71-second overlap against both run windows
- [ ] Evidence references resolve — every `runs/*.json` path cited by either
      manifest exists, all nine F4 repairs land on the right observation, and
      all five new records are cited by the manifest that claims them. But R1,
      R5 and R12 cite observations that do not contain the claim (F10), and
      ev-podcast-21 cites a record that contradicts it (F11)
- [x] Version and identity checks pass — `framework_commit: 152dd2c1` is
      consistent across both manifests and resolves; the only framework change
      since it is 49 additive lines in `atj/cli.py`, with rubric, personas and
      `VERSION` byte-identical; `persona: prepare-submission@1.1.0` and
      `rubric: submission-evaluation@1.0.0` match `framework/personas.md`;
      `atj release-check` PASS including version-skew
- [x] Privacy boundary passes — `public/` holds only `.gitkeep`, every artifact
      is `visibility: private`, no personal identifier appears in any evidence
      artifact or run record, and neither team's material appears in the
      other's package

**FAIL.** What still blocks the gate, in order:

1. **F10** — cite the `src/fin/` no-network/no-model-API grep from R12, or
   record it as an observation if it is not yet one. Fix R1 and R5, and while
   there, R14 and R16. Re-tick Validation against all sixteen rows.
2. **F11** — correct or withdraw `playwright 1.56.0` in `ev-podcast-21`.
3. **F12** — remove the committed `status.md.bak`.
4. **F8** — restamp the four future-dated activity-log rows, correct the audit
   row to `2026-09-17T18:35:00Z`, and narrow the run-record derivation note.

Then re-record both `evidence:` units — the manifest edits in steps 1 and 2 will
change both digests and mark the units stale — and re-audit before
`atj event gate`.

Nothing here requires re-running a submission. Every repair is an edit to an
artifact, and F11's correct value is already sitting in a run record this
repair produced.
