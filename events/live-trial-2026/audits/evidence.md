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
framework_commit: 4ac09bab19637c6f39d19107245f95854f9a987f
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-17T18:57:00Z"
completed_at: "2026-09-17T19:10:00Z"
visibility: private
approval_state: approved
validation_state: valid
result: PASS WITH ADVISORIES
---
# Judging Audit — evidence stage (third pass)

This replaces the second-pass report of 2026-09-17. Finding codes F1-F12 and
A1-A9 are carried with their dispositions so the history stays traceable. New
findings are coded F13 onward and A10 onward.

## Result

**PASS WITH ADVISORIES.** No blocking finding. No major finding. Five minor
findings, none of which changes a conclusion in either package.

The two majors the second pass raised are genuinely fixed, and I verified both
against ground truth rather than against the operator's account.

- **F10.** I re-ran `ev-ledger-20`'s grep myself against the pinned checkout at
  `9d21b770` and every claim in it holds, including the file count. All sixteen
  team-ledger requirement rows now cite evidence that contains the claim made of
  it. I also walked the ten team-podcast requirement rows, which the second pass
  did not.
- **F11.** `playwright 1.63.0` is in `runs/team-podcast-server-boot-02.json`,
  read via `importlib.metadata`, and `env-probe-03`'s failed probe is recorded
  accurately. `1.56.0` survives nowhere in an evidence artifact.

What is left is five text defects, four of them residuals of repairs that were
done partially:

- **F13** — the two Missing-evidence bullets the F10 repair was told to recite
  still point at `ev-ledger-10` for a scan of `src/fin/` that `ev-ledger-10`
  does not perform, and that `ev-ledger-20` explicitly says it does not perform.
- **F14** — `ev-podcast-21` fixed `playwright` and left `starlette 1.6.0` in the
  same sentence, still attributed to a `:2` measurement `env-probe-01` never
  took.
- **F15** — `req-03` in the podcast manifest says the two-episode download stall
  was "not re-tested further". `ev-podcast-20`, added two commits ago, is that
  re-test.
- **F16** — the activity log's stamps still contradict the provenance note the
  F8 repair itself wrote, in three places.
- **F17** — `Containerfile.ledger`, written by the F1 repair, cites a source
  path that does not exist at the pinned commit.

Nothing here is a safety failure, nothing reached `public/`, no cross-team
material appears in either package, no arithmetic exists yet to be wrong, and
the framework change in this repair touches no calculation.

## Scope and artifacts inspected

- The second-pass report at this path, as the specification for this pass.
- `git diff 44e5f87..4ac09ba` — every changed line; `git diff --stat
  152dd2c1..HEAD -- framework/ schemas/ atj/ VERSION`; `git log --pretty=%cI`
  for the four commits the activity log stamps against.
- `events/live-trial-2026/event.md`, `status.md`, `teams.md`, `.gitignore`
- `evidence/team-ledger/manifest.md` — all 16 requirement rows, all 20 evidence
  IDs, the Missing-evidence section and the Validation box.
- `evidence/team-podcast/manifest.md` — all 10 requirement rows, all 21 evidence
  IDs, the Tests table and the Validation box.
- `evidence/Containerfile.ledger`, `evidence/Containerfile.podcast`
- All 27 run records in `events/live-trial-2026/runs/`, by field, for every
  numeric claim either manifest makes of them.
- The pinned checkouts `workspaces/live-trial-2026/team-ledger` (`9d21b770`) and
  `team-podcast` (`f3fdd342`), both confirmed clean and at the pinned commit
  with `git rev-parse HEAD`.
- `podman history --no-trunc` for `ledger:2`, `podcast:2`, `podcast:3`.
- `atj/cli.py:cmd_render_judgment` and `tests/test_end_to_end.py` (A9).
- `framework/templates/audit-report.md`,
  `framework/policies/evidence-and-citation.md`,
  `framework/personas.md`, `framework/rubrics/submission-evaluation.md`.

I re-derived, rather than accepted, every claim the operator made about this
repair. I did not re-read any judgment, bracket or publication artifact; none
exists.

## Deterministic validation results

Re-run, not taken on trust.

| Command | Result |
|---|---|
| `python3 -m atj event validate events/live-trial-2026` | PASS, 0 problems, stage evidence |
| `python3 -m atj validate reports events/live-trial-2026` | PASS — 7 artifacts, 0 blocking / 0 major / 0 minor / 0 advisory |
| `python3 -m atj release-check` | PASS — schemas, personas, templates, claude components, single-source, version-skew, sample event all PASS |
| `python3 -m atj event unit events/live-trial-2026 list` | 2 unit(s), **0 stale** — `evidence:team-podcast` and `evidence:team-ledger`, both `complete`, both `not-audited` |
| `python3 -m atj event status events/live-trial-2026` | stage evidence, `units: {'complete': 2}`, gate `evidence-validated` pending |
| `python3 -m atj sandbox preflight` | AVAILABLE — podman 6.1.0 (rootless) |
| `python3 -m pytest tests/ -q` | **352 passed**, 51 subtests passed (351 before this repair; the new test is A9's) |

The unit digests changed again with this repair (`66e12da633537315` for
team-podcast, `0eda544caa9c3654` for team-ledger) and `0 stale` confirms they
bind the manifests as they stand now, not the ones the second pass failed.

The validators still cannot reach F13, F14 or F15. `atj validate reports`
resolves `[[evidence:ID]]` targets; it has no view on whether the target
contains the claim, on a plain-text evidence ID in prose, or on a sentence that
was true when written and is not now. That gap is why a text-level walk is
still the only control over these.

## F10 — the `ev-ledger-20` grep, re-run independently

I ran the scan myself against `workspaces/live-trial-2026/team-ledger` at
`9d21b7707f204ef60f5a1cee612f1d4db0a4a575` (confirmed by `git rev-parse HEAD`,
working tree clean). Every claim in `ev-ledger-20` holds:

| ev-ledger-20 claim | My result |
|---|---|
| 22 `.py` files in `src/fin/` | `find src/fin -name '*.py' \| wc -l` → **22** |
| zero import of `requests`, `httpx`, `urllib`, `http`, `socket`, `aiohttp`, `boto3`, `openai`, `anthropic`, `google`, `cohere`, `litellm`, `langchain` | zero matches. The complete import inventory of the package is `argparse`, `collections`, `csv`, `dataclasses`, `datetime`, `decimal`, `duckdb`, `hashlib`, `itertools`, `json`, `os`, `pathlib`, `re`, `shutil`, `statistics`, `subprocess`, `sys`, `typing`, `yaml`, `__future__` — stdlib plus `duckdb` and `pyyaml`, both in the approved image |
| zero call site matching `requests.`, `httpx.`, `urlopen`, `socket.`, `api_key`/`API_KEY`, or a model-vendor name | zero, with one exception, which is the one the row itself declares |
| the single match is a docstring at `src/fin/cli.py:3` | confirmed: `Every skill in `.claude/skills/` drives this CLI rather than reading files and` — the pattern hits on the literal `.claude` in a path, inside the module docstring. Not a call |
| only `subprocess` use is `citi_pdf.py:26,198`, invoking `pdftotext` | confirmed. Line 26 is `import subprocess`; line 198 is `subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, check=True)` |
| only environment read is `os.environ.get("FIN_DATA_DIR")` at `store.py:53` | confirmed, and it is the only `os.environ`/`getenv` occurrence in the package |

I also checked the one vector the row does not name: DuckDB can reach the
network through `INSTALL httpfs` / `ATTACH` / an `http://` path handed to
`read_csv_auto`. There is no such call in `src/fin/`. The row's conclusion is
sound, and the scan is reproducible by anyone with the checkout.

`ev-ledger-20`'s Reproduction column says "grep reproducible against the pinned
checkout; no execution involved, no run record". That is the same treatment
`ev-ledger-10` has carried since the first pass and is correct for a static
read — the template's Reproduction column is "the record it came from", and for
a source scan the pinned commit is that record.

## All sixteen team-ledger requirement rows, walked again

Third walk. Two prior passes each found errors the previous pass missed, so I
re-checked every row against the observation it cites and, where the
observation cites a run record, against the record.

| Row | Cites | Verdict |
|---|---|---|
| R1 | ev-ledger-02, -08, -04 | **Fixed.** -02 is the clean load reporting `UNVERIFIED (no control totals)`, -08 is control-total verification rejecting an unbalanced statement, -04 is the no-partial-import half. Each clause of the claim now has an observation that contains it |
| R2 | ev-ledger-06 | Correct |
| R3 | ev-ledger-06, -15 | Correct as to the tiers it names. One undercount, carried as A12 |
| R4 | ev-ledger-03, -06 | Correct — D0 is in both, with the $15.68 = $20.68 − $5.00 arithmetic in -03 |
| R5 | ev-ledger-03, -06, -04 | **Fixed.** -04 now carries idempotence ("a second identical ingest ... `0 new, 1 already known`"), which -03 alone did not |
| R6 | ev-ledger-07 | Correct, partial, both unwritten report kinds named |
| R7 | ev-ledger-07 | Correct |
| R8 | ev-ledger-07, -17 | Correct |
| R9 | ev-ledger-06 | Correct — `=== sql: matches ===` and its result are in `runs/team-ledger-amazon-match-detect-01.json` |
| R10 | ev-ledger-02, -04 | Correct |
| R11 | ev-ledger-08, -09 | Correct, unchanged |
| R12 | ev-ledger-20, -18, -10 | **Fixed, and correctly split.** -20 carries the `src/fin/` half, which I re-ran; -18 carries the four skill files as the whole agentic surface; -10 carries the injection scan. The row now names which observation carries which half |
| R13 | ev-ledger-06, -16 | Correct — I confirmed `external_ref` is a literal CSV column in `adapters/amazon.py`, not derived from `order_id` |
| R14 | ev-ledger-11, -07 | **Fixed**, and the row now states the limit of "every command execution" (three written artifacts checked, not an exhaustive enumeration) rather than leaving it absolute |
| R15 | none | Correct — labelled a team claim |
| R16 | ev-ledger-20 | **Fixed.** The observation half now has an ID, and it is the right one |

Sixteen of sixteen. The requirements table is clean.

Source references I sampled and confirmed at the pinned commit:
`match/engine.py:9` is the `tier 3 SUBSET_SUM` docstring line and
`subset_sum_edges` is at line 173 (R3); `config/accounts.example.yaml:14` is
`apr_bp: 2249`, i.e. 22.49% (ev-ledger-07); `citi_csv.py:54,70` are the two bare
`ValueError` raises ev-ledger-05 describes; the four skill files are 98/84/85/71
lines and `hooks/pre-commit` is 42 lines (ev-ledger-18, -19).

## All ten team-podcast requirement rows, walked

Only the first pass checked this table, before two of the current evidence rows
existed.

| Row | Cites | Verdict |
|---|---|---|
| req-01 | ev-podcast-03, -15, -17, -10 | Correct, and correctly separates the demonstrated pipeline from the unexecutable iPhone claims |
| req-02 | ev-podcast-03 | Correct — `206`, `Content-Range`, `416`, suffix and open-ended ranges are all in that observation |
| req-03 | ev-podcast-17, -16 | **One stale clause. See F15.** "not re-tested further" is no longer true |
| req-04 | ev-podcast-03 | Correct — last-write-wins, stale rejection and the newer-wins case are all in the observation |
| req-05 | ev-podcast-07 | Correct, and correctly hedged as a source read, not a penetration test |
| req-06 | ev-podcast-07 | Correct. I re-ran this one: the only `fetch()` targets in `web/` are `/api/library`, `/api/progress/${id}` and `/api/rescan`; `/api/media/${id}` appears as a worker URL (`storage.js:65`) and an `audio.src` (`player.js:93`). All same-origin. No `openai`, `anthropic`, `api_key` or absolute URL anywhere in `server/` or `web/` |
| req-07 | ev-podcast-05 | Correct and verified at source: `README.md:7` says "34/34", `README.md:285` and `DECISIONS.md:9` say "42/42", and `grep -c 'check('` on `tests/e2e.py` is **43** |
| req-08 | ev-podcast-05 | Correct and verified: `README.md:10` says "33 files · 11.7 h · 1,360 MB"; the checkout has 56 `.m4a` files and `du -sh source` is 2.2G; `releases.json` holds 41 `releases` + 15 `unresolved` = 56 |
| req-09 | ev-podcast-10 | Correct — team claim, unexecutable in any container |
| req-10 | ev-podcast-09 | Correct and verified: `.agentic/project.yaml` is 6 lines and 6 keys, all inert metadata |

Nine of ten clean; `req-03` is F15.

## Numeric claims spot-checked against their cited records

One fabricated version got through two passes, so I treated every number as
suspect. Each of these I read out of the cited record or the checkout:

| Claim | Where it is claimed | Ground truth |
|---|---|---|
| `playwright 1.63.0` | ev-podcast-21 | `server-boot-02` stdout line 2, produced by `python3 -c "import importlib.metadata as m; print(m.version('playwright'))"` in the record's own `command`. **Confirmed** |
| `env-probe-03`'s playwright probe failed | ev-podcast-21 | `stderr`: `AttributeError: module 'playwright' has no attribute '__version__'`. **Confirmed** |
| Chromium 152.0.7977.82, Python 3.12.14, Debian 13 trixie, fastapi 0.141.1, pydantic 2.13.5, uvicorn 0.53.0, starlette 1.6.0, `/usr/bin/ffmpeg`, `/usr/bin/ffprobe` on `:3` | ev-podcast-21 | All nine in `env-probe-03` stdout. **Confirmed as values on `:3`.** The attribution of `starlette` to a `:2` measurement is F14 |
| `:2` and `:3` differ only by `ffmpeg` in the apt layer | ev-podcast-21, event.md | `podman history --no-trunc`: pip layers byte-identical (`pip install --no-cache-dir fastapi pydantic "uvicorn[standard]" "playwright>=1.50"`); apt layers differ by the single token `ffmpeg`; base layer `ec7d6c95cd36` shared. Top IDs `5ff34ae63320` and `c3670644bc7b` match `event.md`. **Confirmed** |
| ffmpeg 7.1.5 | ev-podcast-12 | `env-probe-02`: `ffmpeg version 7.1.5-0+deb13u1`. **Confirmed** |
| 4,884,617 and 6,690,229 output bytes, 6.9s and 10.4s, 12 MB in a 64 MB tmpfs, 18% | ev-podcast-20 | `e2e-full-02` stdout, verbatim, including `MEDIA_DIR_SIZE: 12M` and `18% /tmp`. Sum is 11,574,846 B = 11.0 MiB, consistent with both. **Confirmed** |
| 24.5s | ev-podcast-20, Tests table | `e2e-full-02` `duration_seconds: 24.474`. **Confirmed**, with a reading caveat at A13 |
| `duration_sec 578.896009`, `size_bytes 4884617`, seek-to-600s landing at 578.9s | ev-podcast-15 | All in `e2e-04` stdout, including all four stage-6 `[PASS]` lines. **Confirmed** |
| download completes in 1s; OPFS `1.m4a` 4,884,617 B; `fileSystem: 4884929`; usage ~132 KB → ~5.0 MB; zero console/page errors | ev-podcast-17 | `download-diag-01` stdout: `DOWNLOAD_COMPLETED_AT 1 s`, `usage: 132322` → `usage: 5015459`, `fileSystem: 4884929`, `ALL_CONSOLE_LINES:` and `ALL_PAGE_ERRORS:` both empty. **Confirmed** |
| 71-second overlap of `e2e-full-01` with `e2e-02` | ev-podcast-16 | 00:15:30-00:17:26 against 00:16:15-00:19:19. Overlap is 00:16:15-00:17:26 = 71s. **Confirmed** |
| "~26% transcode ratio the team documents" | ev-podcast-18 | `README.md:10` (source 1,360 MB) against `README.md:43` (transcoded output ~354 MB) = 26.0%. Implicit but real, and the observed ratio matches: 4,884,617/18,631,917 = 26.2%. **Confirmed** |
| 35 passed, exit 0, 0.07s | ev-ledger-12 | `team-ledger-pytest-01`. **Confirmed** |
| `7780b2b9e6e1` is the top layer of `ledger:2` and the committed recipe is its two `RUN` layers in order | F1's closure, `event.md` | `podman history` for `ledger:2`: top layer `7780b2b9e6e1…` is the pip layer, below it `7e1b52138efd…` is the poppler-utils apt layer, below that the stock `python:3.12-slim` base. Matches `Containerfile.ledger` character for character. **Confirmed independently for a second time** |

Every number checked reconciles. The 22 run records I did not re-read in full
were re-read for `runtime`, `runtime_version`, `timed_out`, `limits` and
`command`.

## Execution integrity, re-checked across all 27 run records

Every record carries, in its own `command`, `--network none`, `--read-only`,
`--tmpfs /tmp:rw,noexec,nosuid,size=64m`, `--cap-drop ALL`, `--security-opt
no-new-privileges`, `--user 65534:65534`, `--pids-limit 256`, `--memory 1g`,
`--cpus 1.0`, and exactly one `:ro,Z` mount of that team's own checkout. None
contains `--privileged`, `--network=host`, `--userns=host` or `--cap-add`.
`runtime: podman`, `runtime_version: 6.1.0`, `timed_out: false`, and
`output_truncated: false` throughout. Every record is cited by the manifest that
claims it, and no record is cited by the other team's manifest.

`atj sandbox preflight` reports AVAILABLE. No submission code ran on the host.

## Both manifests: score, contamination, privacy

Neither manifest states, recommends or implies a score. The four occurrences of
the word in the podcast manifest are: ev-podcast-09's injection scan ("no text
directing an evaluating agent to ... alter a score"), and the two
evidence-sufficiency sentences the second pass quoted. The ledger manifest
contains none. Neither package assigns, weights or totals anything.

No cross-team contamination. The only mention of one team in the other's
package is the podcast manifest's single reference to the `poppler-utils`
precedent when it explains the `ffmpeg` amendment — the fairness disclosure
carried at A6. The ledger manifest mentions the podcast team nowhere.

`public/` holds only `.gitkeep`. Every artifact in scope is `visibility:
private`. No operator name, email or personal identifier appears in either
manifest or in any of the 27 run records. The records embed the absolute host
path `/home/gregg/Nextcloud/workspace/...`, which is correct in a private
artifact and is carried at A5. `atj validate publication` must still be run on
anything that leaves the panel.

## F12 — the committed backup, verified gone

`git ls-files` matches no `.bak` path. The file is absent from the working tree
and from `git show HEAD --stat`. `.gitignore` gained `*.bak` with a comment
naming `atj/event.py:745` as the writer, which is the right closure: the tool
recreates the file on every ledger update, so removing it once would not have
held. `git log -- events/live-trial-2026/status.md.bak` still lists the commits
that touched it, which is correct — history is not rewritten to hide a
non-sensitive file, and the blob holds nothing `status.md` did not.

## F8 residual — three stamps still wrong

The log ascends: 18:35:00, 18:35:15, 18:36:28, 18:41:56 ×4, 18:50:00, 19:05:00
×4. Ordering is fixed. The stamps themselves are not, measured against the
provenance note this repair wrote. Detail is in F16; in summary:

- the four new repair rows are stamped 8 minutes **after** the commit that
  contains them, which is the exact defect F8 named;
- the F6-repair row carries the first, not the last, of the four run records it
  describes;
- the two `00:15:00Z` team-ledger rows are still uncovered by the note.

The rows the repair did fix are right: `18:41:56Z` is the true UTC committer
time of `44e5f87` (`2026-09-17T14:41:56-04:00`), and `18:35:00Z` is the
first-pass audit's own `completed_at`, which I read out of
`git show a82ea17:events/live-trial-2026/audits/evidence.md`. `18:36:28Z`
matches `e2e-full-02`'s `completed_at` exactly. `18:50:00Z` matches the
second-pass report's `completed_at`.

## A9 — the approved-judgment guard, assessed

**The guard is right, and `--force` is the correct escape hatch.**

Placement is the part that matters and it is correct. The refusal sits *after*
the `if rendered == body: unchanged; continue` branch, so a re-render that
produces no change still succeeds on an approved judgment. Only a re-render that
would actually alter the official numbers is refused. That is the narrow rule:
it blocks silent mutation without blocking idempotency checks, CI re-runs or
validation sweeps over approved artifacts.

`--force` beats the alternative. Without it, the only way to re-render an
approved judgment would be to flip `approval_state` back to `draft`, render, and
re-approve — which launders the approval through a state change that looks
routine in a diff. An explicit `--force` is greppable in shell history, obvious
in a review, and the error text tells the operator to record the reason in the
event ledger.

The error message is unusually good: it states the refusal, the reason it
matters ("how a panel comes to cite a total no one approved"), and both ways
forward. The test is real — it asserts exit 1, asserts the file was *not*
written (`assertNotIn("| functional |", ...)`), then asserts `--force` succeeds
and reproduces the original block. The existing test was updated with a comment
explaining why it now needs `--force`, rather than being weakened.

Two limitations, both carried as A10, neither an evidence-stage matter: the
refusal raises mid-loop, so a multi-path invocation can leave earlier files
already written; and a forced write leaves no machine-readable trace, including
in `--json`.

**No arithmetic changed.** `git diff --stat 44e5f87..4ac09ba -- atj/ schemas/
framework/ VERSION` is 12 added lines in `atj/cli.py` and nothing else.
`atj/scoring.py` and `atj/render.py` are untouched. Across the whole span the
evidence packages are exposed to — `git diff --stat 152dd2c1..HEAD --
framework/ schemas/ atj/ VERSION` — the delta is 61 added lines in `atj/cli.py`
and nothing else; `framework/rubrics/`, `framework/personas.md`, `schemas/` and
`VERSION` are byte-identical. `release-check` version-skew and sample event both
PASS, which is what exercises the byte-for-byte reproduction claim.

## Repairs checked for weakening an accurate finding

I compared `git diff 44e5f87..4ac09ba` line by line against the second pass's
text. Nothing accurate was removed or softened.

- `ev-podcast-21` gained the failed-probe disclosure and the explicit statement
  that no `:2`-versus-`:3` playwright comparison exists. Strictly more
  conservative than what it replaced.
- The five ledger requirement rows gained citations; none lost one. R14 gained a
  scope limit it did not previously state. R12 gained a split between three
  observations where it previously collapsed everything into one.
- `ev-ledger-20` is additive. It removes nothing and it declares its own
  boundary against `ev-ledger-10`.
- `event.md`'s A8 paragraph replaced "with identical results" with a per-run
  statement that is accurate for each of the four and then says "No observation
  was found to differ between the two images" — which is the true, weaker claim.
  Correct.
- `status.md`'s provenance note is longer and more specific than the one it
  replaced, and it admits the original error rather than quietly fixing it. The
  note is now more honest than the stamps beneath it, which is F16.
- The `tests/test_end_to_end.py` change adds `--force` to one existing test with
  a comment saying why, and adds a new test for the refusal. It does not relax
  an assertion.

## Findings

| Severity | Rule | Artifact | Finding | Required repair |
|---|---|---|---|---|
| minor (F13) | `framework/policies/evidence-and-citation.md`: "Every material conclusion must be traceable to the pinned evidence package"; the F10 repair's own required repair, "cite that from R12 and from the two Missing-evidence bullets" | `events/live-trial-2026/evidence/team-ledger/manifest.md:140,154` | The F10 repair recited the requirements table and stopped there. Both Missing-evidence bullets still attribute the `src/fin/` scan to `ev-ledger-10`: line 140, "this preparation's own grep, ev-ledger-10, and the intake's ... found no `os.environ` read in `src/fin/` other than `FIN_DATA_DIR`", and line 154, "no code path in `src/fin/` calls any model API (confirmed by grep, ev-ledger-10 and intake)". `ev-ledger-10` is a scan of `.claude/skills/*/SKILL.md` and `hooks/pre-commit` for injection phrasing; it does not read `src/fin/`. `ev-ledger-20`'s own last clause says so explicitly, so the manifest now contradicts itself in two places. The claims themselves are sound — I re-ran the grep — and the right observation exists in the package, so this is a wrong pointer, not an unsupported claim. `atj validate reports` cannot see it because both mentions are plain text, not `[[evidence:…]]` links | Change both bullets to cite `ev-ledger-20`, or `ev-ledger-20` and `ev-ledger-10` where both scans are meant |
| minor (F14) | `framework/policies/evidence-and-citation.md`: evidence classes and confidence must reflect what was actually observed | `events/live-trial-2026/evidence/team-podcast/manifest.md`, ev-podcast-21 | The row opens "`podcast:3` carries exactly the runtime `ev-podcast-01` recorded on the superseded `:2`:" and the list that follows includes `starlette 1.6.0`. `ev-podcast-01` recorded no starlette version: `runs/team-podcast-env-probe-01.json`'s `PKGS` block is `fastapi 0.141.1`, `pydantic 2.13.5`, `uvicorn 0.53.0`, `playwright ok`, and `ev-podcast-01`'s own observation text lists the same four. This is F11's defect, in F11's sentence, for a different package — the repair corrected playwright and left starlette. The value is true of `:3` (`env-probe-03` measures it), so nothing downstream is wrong; what is false is the attribution to a `:2` measurement that was never taken. `Python 3.12.14` and `Debian 13 (trixie)` in the same list are fine: `env-probe-01` reports the Python version directly and its Chromium banner reads "built on Debian GNU/Linux 13 (trixie)" | Move `starlette 1.6.0` out of the "`ev-podcast-01` recorded" list and state it as measured on `:3` only, in the same way the row now handles playwright. The four values `ev-podcast-01` actually recorded are Chromium, fastapi, pydantic and uvicorn |
| minor (F15) | `framework/policies/evidence-and-citation.md`: "Every material conclusion must be traceable to the pinned evidence package"; `framework/templates/evidence-manifest.md`: the Evidence status column states what the package holds | `events/live-trial-2026/evidence/team-podcast/manifest.md`, req-03 | req-03 reads "inconclusive whether that is single-vs-two-episode flakiness or a real defect, **not re-tested further**". It was re-tested: `ev-podcast-20` is the same two-episode scenario run in isolation, added in `44e5f87` in response to F5, and it produced a third distinct outcome (Chromium `Target crashed` at stage 3 instead of the 90s stall). The row was written before that run existed and the F5 repair did not revisit it. A judge reading the requirements table — the first thing a judge reads — is told no isolated repeat exists, on the requirement that feeds `reliability`, the one criterion this manifest marks evidence-limited. The package is self-correcting one hop away (`ev-podcast-16` cross-references `ev-podcast-20`, and `ev-podcast-20` states all three outcomes), and the row's conclusion of "inconclusive" is if anything better supported now, which is why this is minor rather than major | Replace "not re-tested further" with a reference to `ev-podcast-20`: the isolated repeat did not reproduce the stall and failed differently again, so three executions have produced three outcomes |
| minor (F16) | `CLAUDE.md`, Source of truth: "Event state … `events/<event>/status.md`"; the provenance note this repair added to that file | `events/live-trial-2026/status.md`, activity log | The note now states the rule exactly, and three sets of stamps beneath it break it. **(a)** The four rows for the F10/F11/F12/F8 repairs are stamped `2026-09-17T19:05:00Z`. The note says a document-change row carries the commit time of the commit that recorded it; that commit is `4ac09ba` at `2026-09-17T14:56:46-04:00` = `18:56:46Z`, and the file's own `last_updated` is `18:56:31Z`. Four rows are stamped after the commit that contains them and after the ledger's own last-updated time — which is verbatim the defect F8(a) raised, reintroduced by the edit that wrote the rule against it. **(b)** The F6-repair row is stamped `18:35:15Z`. The note says the `completed_at` of the **last** run record the row describes; the four records it names complete at 18:35:15, 18:35:26, 18:35:34 and 18:35:52, so the correct stamp is `18:35:52Z`. **(c)** The two `2026-09-17T00:15:00Z` team-ledger rows remain uncovered: they are evidence-stage rows, so "rows predating the evidence stage" does not reach them, the last ledger run completed at `00:04:39Z`, and no commit or audit is at that time. Their stamp is in fact the ledger manifest's own `completed_at` — a fourth provenance kind the note does not name. Separately, the F6-repair row still says "identical results" for four runs of which `server-boot-02` is a superset and `env-probe-03` a wider probe, the wording A8 had corrected in `event.md` | Restamp the four repair rows to `18:56:46Z` (or to whatever commit ultimately records them). Restamp the F6-repair row to `18:35:52Z`. Add a fourth clause to the note covering rows that describe an evidence package, which carry that manifest's `completed_at`. Match the F6-repair row's wording to the corrected `event.md` paragraph |
| minor (F17) | `framework/policies/evidence-and-citation.md`: "Cite repository-relative paths and line or symbol when practical"; the ledger manifest's Validation box, "every source path cited exists at the pinned commit" | `events/live-trial-2026/evidence/Containerfile.ledger` | The header comment, added by the F1 repair in `44e5f87`, reads "poppler-utils supplies pdftotext, which `src/fin/ingest/pdf.py` shells out to." No such path exists at `9d21b770`. There is no `src/fin/ingest/` package — `ingest.py` is a module — and the caller is `src/fin/adapters/citi_pdf.py:198`. The second pass verified this file against `podman history` and did not read the comment. The recipe itself is correct and the manifest and `ev-ledger-20` both cite the real path, so nothing depends on this; it is a wrong source reference in an evidence-package artifact | Change the comment to `src/fin/adapters/citi_pdf.py` |

## Disposition of every prior finding

| Code | Disposition | Basis |
|---|---|---|
| F1 | **Closed** | Re-verified independently for a second time. `podman history` for `ledger:2` shows the pip layer `7780b2b9e6e1…` over the poppler-utils apt layer `7e1b52138efd…` over stock `python:3.12-slim`, matching `Containerfile.ledger` exactly. Reconciliation without rebuild remains the right closure. One wrong path in the file's comment is F17 |
| F2 | **Closed** | `evidence_limited_criteria: [reliability]`, basis written into Missing evidence, all three outcomes named. `ev-podcast-20` labels the resource-cap explanation an inference with no measurement behind it and does not overclaim |
| F3 | **Closed** | `atj event unit … list` shows 2 units, **0 stale**, with digests `66e12da633537315` and `0eda544caa9c3654` binding the current manifests. Both still `not-audited` and must be re-recorded with this audit's result |
| F4 | **Closed** | All nine originally misdirected rows repointed and re-verified in this pass's sixteen-row walk |
| F5 | **Closed** | `ev-podcast-16` records the 71-second overlap; I re-derived it from both run windows. `ev-podcast-20` is the isolated repeat. One consequence of adding it was missed in req-03, which is F15 |
| F6 | **Closed** | All four `podcast:2` runs repeated on `:3`; `podcast:2` listed in `event.md` with its scope. `event.md`'s "identical results" replaced per A8; the same wording survives in one `status.md` row, folded into F16 |
| F7 | **Closed** | R3 and R6 marked partial with the unexercised items named. One undercount in R3 is A12, not a reopening |
| F8 | **Closed as to ordering and attribution; three stamps still wrong, carried as F16** | The log ascends, both image amendments name the event-director (which closed intake F3), and the provenance note now states four rules instead of one false one. But the four new rows postdate their own commit, the F6-repair row takes the first rather than the last run record, and the two `00:15:00Z` rows remain outside the note. Fourth appearance of the rule from configuration F5 |
| F9 | **Closed** | `.agentic/project.yaml` is 6 lines, 6 keys. Re-verified |
| F10 | **Closed as to all sixteen requirement rows; the two Missing-evidence bullets are not, carried as F13** | `ev-ledger-20` exists and I re-ran its grep in full against `9d21b770`, including the 22-file count. R1, R5, R12, R14 and R16 are all correctly recited and I verified each against the observation behind it. The Validation box's "Artifact references resolve" tick is now earned for the requirements table |
| F11 | **Closed** | `playwright 1.63.0` is in `server-boot-02`, read via `importlib.metadata`; `env-probe-03`'s `AttributeError` is recorded verbatim; the row states plainly that no `:2`-versus-`:3` playwright comparison exists. `1.56.0` appears nowhere in either manifest. The same defect for `starlette` in the same sentence is F14 |
| F12 | **Closed** | `git ls-files` matches no `.bak`; the file is absent from the tree and from `HEAD`; `*.bak` is gitignored with a comment naming `atj/event.py:745` as the writer, which is the closure that holds against a tool that recreates it |
| A1 | **Closed** | Timeout paragraph present and accurate against the `limits.timeout_seconds` in each record |
| A2 | **Closed** | `ev-podcast-02` carries the real captured headers from `server-boot-02`, which I read out of the record; `ev-podcast-03` separates the record's `HTTPException` from the `400` read at `server/app.py:164,168` |
| A3 | **Closed** | `ev-ledger-05` states the observation without naming rubric criteria or pre-weighing itself |
| A4 | **Closed** | `event.md` records why a missing declared prerequisite was fixed by amending the image while the 64 MB tmpfs cap was not |
| A5 | **Carried forward** | All 27 run records embed the absolute host path and the `65534:65534` uid map. Fine in private artifacts. Run `atj validate publication` on anything leaving the panel |
| A6 | **Carried forward** | The podcast manifest's single reference to the `poppler-utils` precedent is the only cross-team mention in either package. Fairness documentation, no finding about the other team. Keep it out of a team-facing dossier |
| A7 | **Carried forward** | `evidence_package_id` still cannot be reproduced from the artifact by an auditor; the `evidence:` units remain this event's only working staleness detection. Framework observation, outside this stage |
| A8 | **Closed** | `event.md` now states per run what was reproduced, what was extended, and that `env-probe-03` is a wider probe rather than a repeat, then draws the weaker true conclusion. Accurate against all four records |
| A9 | **Closed, with two notes carried as A10** | The guard refuses only a re-render that would change an approved judgment's numbers, has a real test that asserts the file is not written, and `--force` is the right escape hatch. See the assessment section |
| configuration/intake A7 | **Carried forward** | The operator's name in `event.md` must not reach `public/`. Still open by design, still correct |

## Advisories

**A10 — the new `render judgment` guard is not atomic, and a forced write leaves
no trace.** `cmd_render_judgment` iterates over every path, and every file, and
writes as it goes. The refusal `raise AtjError(...)` fires inside that loop, so
`atj render judgment events/X/judgments/` over a directory where the third file
is approved leaves the first two already rewritten and exits 1 naming only the
third. A pre-pass that collects every refusal before writing anything would make
the command all-or-nothing. Separately, `--force` produces no machine-readable
record: the `--json` output lists `rendered` and `unchanged` and does not say
which writes were forced, so the "record why in the event ledger" instruction in
the error text is the only control. A `forced` list in the JSON, or a required
`--force-reason`, would close that. Framework note for the judging audit, not an
evidence-stage finding.

**A11 — a blank line splits the activity log into two Markdown tables.** In
`status.md` there is an empty line between the `18:41:56Z` F6/F8/F9 row and the
`18:50:00Z` re-audit row. Everything below it is a second table with no header,
so it renders as a paragraph of pipe-delimited text rather than as rows of the
log. Cosmetic, and worth fixing while F16 is being fixed.

**A12 — R3's tier count is one short.** `src/fin/match/engine.py`'s own docstring
defines five tiers, 0 through 4: `REFERENCE`, `AMOUNT_DATE_UNIQUE`, an
ambiguous tier 2 that commits nothing, `SUBSET_SUM`, and `UNMATCHED`. R3 says
"three of the four tiers were exercised" and names only `SUBSET_SUM` as
unexercised. The tier-2 ambiguity path — more than one candidate, commit nothing
— is also unexercised and unnamed. The requirement's own wording comes from the
intake's four-tier description, so the row is faithful to its source, but the
disclosure of what was not exercised is incomplete by one path. Naming it would
cost a clause.

**A13 — "24.5s into the run" is the container's duration, not the suite's.**
`e2e-full-02`'s `duration_seconds` is 24.474, and 17.3s of that is the two
transcodes (6.9s + 10.4s) that ran before `tests/e2e.py` started. The renderer
crashed roughly 7 seconds into the suite, not 24. Both `ev-podcast-20` and the
Tests table say 24.5s, which is true of the run record and misleading about the
suite. It matters a little for the resource-cap inference: a crash 7 seconds in
reads differently from one 24 seconds in.

## Completion gate

- [x] **No blocking findings** — none raised. Execution integrity is clean
      across all 27 records, checked flag by flag; `atj sandbox preflight`
      reports AVAILABLE; nothing ran on the host
- [x] **No major findings** — F10 and F11, the second pass's two majors, are
      both closed against ground truth I re-derived. The five open findings are
      minor: three wrong or stale citations in prose, three activity-log stamps,
      and one wrong path in a Containerfile comment. None changes a conclusion,
      an evidence class, a confidence rating or an `execution_status`
- [x] **Calculations valid** — no official arithmetic exists at the evidence
      stage and neither package presents a score. Every arithmetic claim I
      re-derived reconciles: 4,884,617 + 6,690,229 = 11,574,846 B against
      "12 MB combined" and the 18% of a 64 MB tmpfs `df` reports; 24.474s
      against "24.5s"; 71 seconds of overlap against both run windows; 26.0%
      transcode ratio from `README.md:10` and `:43` against the 26.2% observed;
      $15.68 = $20.68 − $5.00 in `ev-ledger-03`; `apr_bp: 2249` = 22.49%;
      41 + 15 = 56 releases against 56 files on disk
- [x] **Evidence references resolve** — every `runs/*.json` path cited by either
      manifest exists; all sixteen team-ledger requirement rows and nine of ten
      team-podcast rows cite an observation that contains the claim, verified
      row by row in this pass; every `[[evidence:…]]` target resolves and
      `atj validate reports` passes with zero problems. The three text defects
      (F13's two plain-text pointers, F14's attribution, F15's stale clause) are
      recorded as minor because the supporting evidence exists in the package in
      every case
- [x] **Version and identity checks pass** — `framework_commit: 152dd2c1` is
      consistent across both manifests and resolves; the only framework change
      since it is 61 additive lines in `atj/cli.py`, with rubrics, personas,
      schemas, `scoring.py`, `render.py` and `VERSION` byte-identical;
      `persona: prepare-submission@1.1.0` and `rubric:
      submission-evaluation@1.0.0` match `framework/personas.md`; both checkouts
      are clean at their pinned commits; `atj release-check` PASS including
      version-skew and sample event
- [x] **Privacy boundary passes** — `public/` holds only `.gitkeep`, every
      artifact is `visibility: private`, no personal identifier appears in any
      evidence artifact or run record, and neither team's material appears in
      the other's package beyond the disclosed A6 precedent

**PASS WITH ADVISORIES.**

The evidence stage may advance. Order of operations, because three of the five
findings touch the manifests and will mark the units stale:

1. Repair **F13**, **F14** and **F15** — three sentences across the two
   manifests. These change both input digests.
2. Repair **F16**, **A11** and **F17** — `status.md` and
   `Containerfile.ledger`. Neither is a unit output, so neither affects a
   digest.
3. Re-record both units:
   `python3 -m atj event unit events/live-trial-2026 record --id evidence:team-ledger --stage evidence --output evidence/team-ledger/manifest.md --audit-result "PASS WITH ADVISORIES"`
   and the same for `evidence:team-podcast` with
   `--output evidence/team-podcast/manifest.md`.
4. `python3 -m atj event gate events/live-trial-2026 evidence-validated passed --audit audits/evidence.md`.

No re-audit is required for these five. Each names the exact text to change and
the exact ground truth to change it to, and none of them touches an evidence
class, a confidence rating, an `execution_status`, or any number a judge will
score against. If a repair does anything beyond what is listed here, it needs a
fourth pass.

Nothing here requires re-running a submission.
