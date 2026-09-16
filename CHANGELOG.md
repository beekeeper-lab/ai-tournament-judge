# Changelog

Versions follow `MAJOR.MINOR.PATCH` with a release-stage suffix. Rubrics and
policies carry their own independent versions; see `framework/rubrics/`.

## 0.2.0-beta — 2026-09-16

First release capable of running a complete supervised mock event. The
v0.1.0-alpha scaffold described this system; this release implements it.

### Added

- `atj`, one command line covering event lifecycle, scoring, head-to-head
  resolution, bracket assignment, artifact validation, publication gating,
  sandbox preflight, the sample event, and the release check.
- Canonical data model. `framework/rubrics/submission-evaluation.md` is the only
  editable source of criterion IDs, names, weights, scale and version; a
  tree-wide check fails the build if a second copy appears.
- `framework/personas.md`, a component registry pinning every agent and skill to
  a version and a content digest. An edited component fails validation until its
  version is incremented.
- 14 JSON schemas covering event configuration, roster, team intake, evidence
  manifests, judgments, consolidated reports, adjudications, brackets, matchups,
  dossiers, public reports, model-run records and the status ledger.
- Head-to-head calculator with reversal normalization, per-criterion and total
  margins, presentation-order disagreement detection, close-call handling and a
  mechanical tie-break. It returns no winner when policy requires human review.
- Event state machine with legal transitions, audit gates, staleness detection
  and resume from the first incomplete unit.
- Publication boundary enforcement: visibility by location, recursive private-
  field bans, credential scanning, private-identifier scanning, deliberation
  detection and a required named human approver.
- `atj/sandbox.py`: isolated submission execution with no network, read-only
  mounts, dropped capabilities, resource limits and clean teardown. No host
  fallback; unavailable isolation yields `NE` on affected criteria.
- Prompt-injection fixture and 20 tests covering the mechanical resistance layer.
- Five project-local hooks, verified firing in Claude Code 2.1.273.
- Five new templates: adjudication, calibration, model-run, manual override and
  release readiness. All 17 templates now carry full identity metadata.
- `events/sample-mock-2026`, a committed synthetic event of 53 artifacts, and a
  20-team bracket fixture.
- Static ceremony HTML and printable team dossiers, generated only from approved
  public artifacts.
- CI workflow, packaging, and `atj release-check`.

### Fixed

From the baseline audit of v0.1.0-alpha:

- Official weights were duplicated in `calculate_scores.py` and the rubric
  version was pinned a third time in `judgment.schema.json`.
- Previous-finalist bracket separation was broken at every size except a 32-slot
  bracket; up to 21 of 40 seeds placed the champion and runner-up in the same
  half.
- Play-in pairing was greedy with no lookahead and produced avoidable
  same-affiliation first-round matches.
- An unrecognised bye policy was accepted whenever the bye count was zero.
- The publication boundary was unenforced: a public artifact carrying a
  credential, judge deliberation, an unapproved score and `visibility: private`
  validated clean.
- The configuration validator never parsed YAML and accepted an invalid
  `event_id`, an invalid bye policy and a wrong-typed judge list.
- Report validation accepted an empty report and an out-of-range score.
- The shipped JSON schemas were never loaded by any code.
- Weight validation checked only the sum, so a wrong split totalling 100 passed.
- A one-judge panel and four copies of the same judge both produced clean totals.

From the independent Stage 1 audits:

- The close-call band could be narrowed from a matchup input file, converting
  results requiring human review into automatic advancements. The guard was
  inverted. The rubric band is now a floor.
- A previous-finalist pair that also shared an affiliation group lost its hard
  separation penalty.
- The bye-policy list and default were a third editable copy.
- Rubric version literals in 18 templates were never resolved against the canon.
- The public field ban was top-level only; a nested mapping published scores, a
  judge run id and the official total.
- A `teams:` list in front matter silently replaced the reviewed roster table.
- The bye-policy constraint asserted satisfaction instead of checking it, and
  bracket verification trusted the audit block inside the file it was verifying.
- A 284-byte YAML alias bomb took 69 seconds to parse.
- The publication gate reported CLEAR when it could not determine an artifact's
  location.
- A severe disagreement or possible outlier produced a clean official total
  despite both policies requiring adjudication.

### Changed

- The five v0.1.0-alpha scripts are retired to compatibility shims over `atj`.
  They will be removed in 0.3.
- `panel-consolidation.md` and `head-to-head.md` now declare their thresholds and
  tie-break order in front matter, so the policy document and the code cannot
  drift.
- Templates no longer carry weight columns; official numbers are generated.

### Known limitations

- LLM judgment is not deterministic and this release does not claim otherwise.
  Calculation, validation, rendering, state transitions and seeded bracket
  assignment are.
- Judge scores in the sample event are scripted fixture inputs, not model output,
  so the pipeline is reproducible without an LLM call.
- Submission execution requires Podman or a reachable Docker daemon. Where
  neither is available, executable evidence is unavailable and affected criteria
  must be scored `NE`.
- Hooks are guard rails, not a security boundary. Claude Code also ignores
  `permissions.allow` from project settings until the workspace is trusted.

## 0.1.0-alpha

Architectural scaffold: rubrics, policies, templates, agent and skill
definitions, five scripts and eleven tests.
