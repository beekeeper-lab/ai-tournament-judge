---
event_id: live-trial-2026
adjudication_id: adj:live-trial-2026:team-podcast:01
question: Can `reliability` be scored for team-podcast from the pinned evidence package, and if not, does the unresolved `NE` stand?
scope: criterion
team_id: team-podcast
match_id: null
criterion: reliability
trigger: unresolved-ne
advances_team: null
commit: f3fdd342465fa6bc2a52d226a8613b082ad329e0
evidence_package_id: ev:live-trial-2026:team-podcast:f3fdd342465f:d06f90cc
rubric: submission-evaluation@1.0.0
persona: run-judging-event@1.0.0
framework_commit: 01f559fa5ff370ab0233cf87aaf449c73365f5a3
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-17T21:20:42Z"
completed_at: "2026-09-17T21:20:42Z"
visibility: private
approval_state: approved
validation_state: unvalidated
resolution: resolved
decided_by: event-director
---

# Adjudication Report

## Question

Can `reliability` be scored for team-podcast from the pinned evidence package,
and if not, does the unresolved `NE` stand?

## Trigger

`unresolved-ne`. Raised by `atj score` over `judgments/team-podcast/`, which
recorded `adjudication_required: [{criterion: reliability, trigger:
unresolved-ne}]` in `summaries/team-podcast.json` and refused to finalize a
total. `framework/policies/disagreement-and-adjudication.md:5` requires
adjudication for an `NE` that prevents scoring.

## Disputed claims

There is no disagreement between judges to settle. All four returned `NE`
independently. The question is whether that determination stands.

| Source artifact | Claim | Evidence cited | Class |
|---|---|---|---|
| `judgments/team-podcast/judge-backend.md` | Failures trace to the harness, not the submission; no `--shm-size` set, so Chromium ran against a 64 MB `/dev/shm` | run command lines in `runs/team-podcast-e2e-full-02.json` | inference |
| `judgments/team-podcast/judge-product-agentic.md` | Chromium profile under `HOME=/tmp` shares the same 64 MB tmpfs; disk exhaustion is as available as memory | `ev-podcast-12`, `ev-podcast-18` | inference |
| `judgments/team-podcast/judge-frontend-ux.md` | Both two-episode runs failed at the stage-3 download wait; the isolated single-episode probe completed it in 1s | `ev-podcast-17` vs `ev-podcast-15`, `-16`, `-20` | direct observation |
| `judgments/team-podcast/judge-security-ops.md` | `web/js/storage.js:13-31,49-76` has no `worker.onerror` and no timeout, so a hung download is indistinguishable from a slow one | source read at the pinned commit | artifact evidence |
| `evidence/team-podcast/manifest.md` | Three executions, three outcomes, none classified | `ev-podcast-15`, `-16`, `-20` | direct observation |

## Evidence reviewed

Only evidence already in the pinned package: `ev-podcast-15`, `-16`, `-17`,
`-18`, `-20`, `ev-podcast-05`, `ev-podcast-06`, and the run records
`team-podcast-e2e-04.json`, `-e2e-full-01.json`, `-e2e-full-02.json`,
`-download-diag-01.json`. No new evidence was gathered. Gathering new evidence
would mean re-executing the submission after judging began, which
`CLAUDE.md` forbids for an active event and which would invalidate the
judgments that rest on this package.

## Factual resolution

`reliability` is **not resolvable from the available evidence**, and the `NE`
stands.

What the evidence establishes: three executions of `tests/e2e.py` against the
same commit and the same image produced three different outcomes — a stall at
stage 7, a 90-second download timeout at stage 3 during a measured 71-second
overlap with a concurrent container, and a Chromium `Target crashed` at stage 3
in isolation. None was classified. The submission's only test asset has never
produced a completed run in this event, so its own pass claim cannot be checked
against anything.

What the evidence does not establish: whether any of the three outcomes is
caused by the submission. Every traced failure points away from it — the server
had already logged `GET /api/media/1 200 OK` before both stage-3 failures, and
the sandbox ran under `--memory 1g --cpus 1.0` with podman's default 64 MB
`/dev/shm` and a 64 MB tmpfs holding both the media and the browser profile.
These are credible environmental explanations, but none was measured.

This is a limit of the evidence package and the event's execution constraints,
not a finding against the submission. A low score would ignore that every
observed failure has a credible environmental cause; a high score would credit a
suite that has never produced a result. `NE` is the correct disposition and it
is not a zero.

## Impact on the result

| Affected criterion or outcome | Before | After | Mechanism |
|---|---|---|---|
| `reliability` (team-podcast) | `NE` from 4 of 4 judges | `NE`, adjudicated and accepted | no change; the `NE` is confirmed, not cleared |
| team-podcast official total | not finalizable | not finalizable, permanently for this event | no change |
| team-podcast provisional sum | 58.25 of 100, unofficial | unchanged, remains unofficial and unpublishable | no change |
| Bracket assignment | — | unaffected | 2 eligible teams, `min_teams: 2`, one matchup, no byes, so no bye seeding reads a total |
| Head-to-head matchup | — | unaffected | `framework/rubrics/head-to-head.md` compares the seven criteria directly and states "Do not merely select the team with the higher initial total" |
| `reliability` in the matchup | — | expected to be comparison value `0` | "Substantially equal or insufficient comparative evidence" is the defined value for this case. The matchup panel decides it on the common evidence; this adjudication does not bind it |
| Tie-break | — | possibly narrowed | `tie_break_order: [functional, reliability, product]`. Comparison value `0` means "substantially equal **or** insufficient comparative evidence" and is the matchup panel's finding to make, not this adjudication's to impose. If the panel returns `0`, `reliability` contributes no margin and the effective order becomes functional, then product |

No score was overridden. `score_override` is absent by design. The impact table
was derived from `atj score` output and the two rubric front matters, not by
hand.

## Confidence

`high`. The determination rests on direct observation of three recorded
executions and on the unanimous, independently reached conclusion of four
judges whose reports the stage audit found independent by every method it tried.
The first pass quoted a maximum pairwise 9-gram overlap of 0.0076; the second
pass could not reproduce that exact figure under its own stated method, getting
0.0149 for this panel on stripped 9-grams and 0.0248 on the tool's 6-grams
against a 0.80 threshold. Every measure is far below any contamination
threshold and the conclusion is unchanged, but the precise figure should not be
quoted as measured (audit A6). The uncertainty that produced the `NE` is thoroughly
documented; the decision that it cannot be resolved within this event is not
itself uncertain.

**Amendment disclosure.** This record was approved at `completed_at:
2026-09-17T21:20:42Z` and then edited in place at 21:37:32Z to correct the
tie-break overstatement (audit F13) and to stop quoting an independence figure
that did not reproduce (audit A6). The front matter timestamps describe the
original decision, not the edit, so text in this file references an audit that
post-dates its own `completed_at`. No score, no resolution and no decision
changed. The schema and template have no amendment field, which is why this is
prose; recorded as framework defect D14 (audit F16).

## Human decision

Decided by the **event-director**, who declined to reopen the evidence stage.

The `persona` field reads `run-judging-event@1.0.0` because that orchestrator
performed the adjudication step under policy; the decision itself is the
event-director's and is recorded in `decided_by`. The template invites
`ADJUDICATOR-AGENT-OR-HUMAN@VERSION`, but `atj validate` requires a persona
registered in `framework/personas.md` in `name@x.y.z` form, and the registry
has no adjudicator persona and no way to name a human. Recorded as framework
defect D10.

The alternative was one re-run of the suite with `--shm-size` raised against a
small library, which three of the four judges independently identified as an
operator action rather than work the team owes, and which would likely have made
the criterion scorable. It was rejected because `CLAUDE.md` names evidence among
the things that must not change once judging begins: re-running it would require
a new event version or a restart, and would invalidate four judgments that
already cite this package.

Recorded consequence for the final event report: team-podcast completes
live-trial-2026 without an official total, for a reason that is the framework's
and the operator's, not the team's. The dossier must say so in those terms.

## Validation

- [x] Question is narrow and answerable
- [x] Every cited artifact resolves
- [x] No original report was modified
- [x] Impact recalculated by `atj score`, not by hand
- [x] Human decision recorded where policy requires one
