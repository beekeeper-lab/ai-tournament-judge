# Design document

The versioned design document for the AI Tournament Judge framework. It explains
the principles, architecture, data model, CLI, event history, and what is done
and left, with diagrams. The HTML is the review surface. This file holds the
durable decisions and the version index.

**Current version:** 1.0, [`design-doc-v1.0.html`](design-doc-v1.0.html)

Canonical numbers (weights, thresholds, band, tie-break, byes, component
versions) are deliberately absent from both files. Read them from the files named
in `CLAUDE.md` "Source of truth".

## Version history

| Doc version | Date | Framework | Repo commit | File | Change |
|---|---|---|---|---|---|
| 1.0 | 2026-09-24 | 0.4.0-beta | 95ae008 | `design-doc-v1.0.html` | First versioned design document, after `trial-2-2026` completed |

A new version adds `design-doc-vX.Y.html` beside the old one and a row here. Old
files are not edited.

## Durable decisions

Coded `DD` to avoid collision with the `D` codes in `docs/implementation-detail.md`,
`docs/framework-fix-plan.md` and `docs/0.5.0-beta-plan.md`.

| Code | Decision | Source |
|---|---|---|
| DD1 | The rubric Markdown is the only editable source of official numbers; a second copy fails the build | implementation-detail D1 |
| DD2 | Identifiers are derived from content, never assigned | implementation-detail D2 |
| DD3 | Version mismatch is fatal; retired versions are recorded append-only | implementation-detail D3, fix-plan D28 |
| DD4 | The close-call band is a floor: widen, never narrow | implementation-detail D4 |
| DD5 | Bracket placement is a seeded search; infeasible is a reported outcome | implementation-detail D5 |
| DD6 | Verification re-derives from inputs, never trusts the file's own audit | implementation-detail D6 |
| DD7 | The publication gate fails closed; the ceremony reads only `public/` | implementation-detail D7 |
| DD8 | Execution is isolated or unavailable; no host fallback; allowlist needs the egress proxy | implementation-detail D8, CHANGELOG 0.4.0-beta |
| DD9 | Injection resistance is claimed only for mechanical properties | implementation-detail D9 |
| DD10 | The sample event's scores are scripted and say so | implementation-detail D10 |
| DD11 | Hooks are guard rails and fail open | implementation-detail D11 |
| DD12 | Written official numbers are re-derived and compared | implementation-detail D12 |
| DD13 | A gate needs an approved in-scope audit and the stage's work | implementation-detail D13 |
| DD14 | A winner advances only from a confirmed result or an approved adjudication | implementation-detail D14 |
| DD15 | Components reading untrusted content return documents; the orchestrator writes | `framework/personas.md` |
| DD16 | Evidence stays frozen once judging begins, even to rescue an `NE` | `CLAUDE.md` |
| DD17 | Hypotheses are recorded in `event.md` before judging; nothing planted enters an official event | 0.5.0-beta-plan D2 |
| DD18 | Calibration runs before any award-deciding use | 0.5.0-beta-plan D1, `docs/final-audit.md` |

## State at this version

Framework `0.4.0-beta` at main `95ae008`. Three events are complete:
`sample-mock-2026` (scripted fixture), `live-trial-2026` (first real trial, 31
defects, all fixed) and `trial-2-2026` (second real trial, completed 2026-09-24,
every stage audit `PASS WITH ADVISORIES` after three to six rounds). The
`0.5.0-beta` plan is still `proposed`. Of its hypotheses only H6 is answered;
H4 is partial, and H1, H2, H3 and H5 have not run because no calibration exists
and trial-2 had two teams. Open work is W1 to W30 in `docs/0.5.0-beta-plan.md`,
the trial-2 carried items (evidence F14, intake F7, configuration F10, F20, F23),
the `live-trial-2026` disclosure decision, and a decision on whether trial-2
counts as the 0.5.0-beta event. The resume sequence is section 19 of the HTML.
