# Changelog

Versions follow `MAJOR.MINOR.PATCH` with a release-stage suffix. Rubrics and
policies carry their own independent versions; see `framework/rubrics/`.

## Unreleased

Nothing yet.

## 0.4.0-beta — 2026-09-18

Two of the release audit's open advisories closed, and the two controls the
framework asserted in prose and never checked.

### Added

- `atj sandbox proxy up|down|status`, the egress proxy an event's
  `network_allowlist` needs to mean anything. Container flags cannot filter by
  destination, so the allowlist path had been refused outright and never
  exercised (release advisory 5). The submission joins an internal network with
  no route off the host and no resolver; the proxy is the only way out and denies
  by default, with one anchored rule per allowed host and `CONNECT` limited to
  ports 80 and 443. `atj sandbox run --egress-proxy auto` refuses a proxy whose
  allowlist differs from the event's, because an allowlist is an official's
  decision and a leftover proxy would make it quietly false.
- Verified against a live runtime, not only unit-tested: an allowed host returns
  200, an allowed subdomain rule matches, a denied host gets 403 from the proxy,
  a bypass by name cannot resolve and a bypass by raw address cannot connect.
  `ATJ_LIVE_SANDBOX=1 python3 -m pytest tests/test_egress.py` runs that on an
  event host; CI stays hermetic.
- `atj validate reports` checks that every criterion is discussed and cites
  something: an evidence id, an evidence-class marker, or a code reference.
  `CLAUDE.md` requires that every score cite evidence and the judgment
  template's own checklist claims it, and nothing read either. A shape check, not
  a truth check, and `minor`: a number with no citation is a gap in the record
  rather than a wrong total. All 24 committed judgments pass it, in both
  conventions they use.

### Changed

- An event cannot be marked `complete` while a stage-gate bypass recorded by
  `--force-reason` has not been reviewed. An event may be *run* past a bypassed
  gate -- that is what the flag is for, and stopping the event dead would teach
  an operator to edit the ledger by hand -- but it may not be called complete
  while nobody has read the bypass. It is the last transition, so it costs no
  in-flight work, and it is the one place the framework can insist on a review it
  cannot perform itself.

## 0.3.0-beta — 2026-09-18

The release that ran a real event. `live-trial-2026` took two real applications
through intake, containerized execution, a four-persona panel, consolidation,
adjudication, a head-to-head and two dossiers, to `complete`, under nine audited
stage gates. The subject under test was the framework, and it found **31
defects** -- the last two found not by reading the code but by running the
documentation: `atj event validate` on a completed event, and step 7 of the
release checklist. All 31 are fixed; `docs/framework-fix-plan.md` records each
one with what was verified rather than what was intended.

Read this before running an event: a green `atj validate reports` means an
artifact is well-formed, not that it is true. On the live event it returned zero
findings at every stage on manifests containing nine misdirected citations, a
scan credited to an observation that never examined the code in question, and a
fabricated version number. The LLM audit caught all of them and was the only
thing that did. `framework/rubrics/README.md` now says so in the framework's own
voice.

### Added

- **Version supersession** (D28), the keystone. Nothing recorded a retired
  version, so any bump turned every artifact of every completed event into a
  blocking mismatch whose only in-event repair was to rewrite a frozen record.
  `framework/personas.md` gained an append-only `## Superseded versions` table;
  `framework/rubrics/archive/` holds retired contract versions, loaded by
  `canon.load_reference()`; `atj score` reads a panel's rubric from the panel, so
  a completed event is recomputed under the contract it was judged under; a
  superseded pin validates as an advisory, and a *template* pinning one fails
  `release-check`.
- `atj event overrides`, which lists every stage gate a human bypassed with
  `--force-reason`, exits non-zero while one is unreviewed, and records with
  `--review` that a person read it — never that it was justified. Six controls in
  this framework end in a human, and this is the one that could not be reviewed
  at all.
- `atj render consolidated`, `atj render judgment` and `atj validate publication`
  over a whole directory — three commands the templates and `CLAUDE.md` named
  before they existed (D3, D18, D24).
- A `matchup-pass` artifact kind (D22): schema, template, and a declared private
  `matchup-passes/` directory. A single order-balanced pass must carry exactly one
  populated block, because the other one's emptiness is the evidence of
  independence. The live event had parked both pass reports in an undeclared
  directory, where no check reached the only written record of the comparative
  evidence.
- Bidirectional citation checking (D4/T3.1). The evidence manifest's observation
  table declares which requirements each observation supports, written
  independently of the requirements table, and `atj validate reports` asserts the
  two agree. A requirement citing an observation that does not claim to support it
  is blocking.
- An accepted `NE` (D11). `score_override.resolved_score: NE` records that an
  official reviewed the criterion and the `NE` stands. The panel still cannot
  finalize, because the rubric forbids it — but it is unfinalized by decision, and
  `atj score` stops demanding the adjudication it already has.
- `decision_authority` on an adjudication (D13). `human-official` or
  `agent-substituted`; only the first may move an official total, a record that
  declares nothing is treated as the second, and the withheld resolution is
  disclosed rather than swallowed.
- `amendments` on an adjudication (D14): append-only, must read forward from the
  record's own `completed_at`, and an approved record's last amendment must name
  its author.
- `writes` in the component registry (D1/T2.2), declaring who persists each
  component's artifact, with `release-check` failing in both directions.
- Four release-audit advisories closed: identical score vectors across a panel are
  now examined, `sandbox preflight` says what a rootful or unknown privilege mode
  costs, `bracket verify --structure-only` must be asked for by name, and the
  score gate covers comma decimals, spelled-out scales and score words near
  numbers — plus any total-shaped number in a public artifact when no total has
  been finalized.
- `atj event validate` compares `status.md`'s prose to the ledger above it (D30).
  The live event finished with its final audit recorded as passed and its own body
  still showing it unchecked.
- Ledger digests for every stage (D21). The bracket, tournament, dossier and
  final-audit stages could not be recorded as units at all, and the sample event
  recorded three kinds of unit with digests nothing could re-derive — which drift
  detection silently skips.
- `release-check` gained `version archive`, `write contracts`, `packaging` and
  `template schemas`; the last one found two further defects the moment it ran.
- An in-tree build backend that stages `atj/data/` before any wheel, sdist or
  editable install, a `MANIFEST.in` that lets an sdist build its own wheel, and a
  CI step that installs the wheel into a fresh virtualenv and runs it from
  `/tmp` (D31). The staging tool existed and said to run it in the build step;
  there was no build step that did, so a released wheel reported `atj unknown`
  and could not find its own rubric.

### Changed

- `submission-evaluation` 1.0.0 -> **1.1.0**. The `agentic` central question has
  a subject whether or not the submission contains AI, and a new section says what
  to score when it does not: a correct, documented, verified decision not to use
  AI meets primary expectations, never reaches the anchors that require a
  demonstrated system, and is never scored at the bottom anchors, which describe
  failure (D12). `confidence` is defined — it describes the evidence, and for an
  `NE` it describes how firmly the evidence establishes that no observation was
  possible (D8). `head-to-head` and `panel-consolidation` follow to 1.1.0, since
  both declare `source_rubric`.
- All seven agent personas 1.0.0 -> **1.1.0**. Each definition now names the
  artifact it produces, the template it fills, and who persists it.
  `judging-auditor` holds `Write`; the six components that read untrusted
  submission content deliberately do not, and say why.
- `model.verified` has a threshold (D9): true only when the model identity came
  from outside the model's own statement. A self-report is a team claim one level
  removed.
- The stage gate reads an audit's scope and its unresolved blocking findings, not
  its verdict alone (D16). A finding against a framework document used to block a
  stage exactly as hard as a wrong score.
- `.claude/hooks/pre-advance.sh` reads a command rather than a string (D6, D23).
  It strips heredocs, requires a runner adjacent to a submission path, requires an
  advance to start a command rather than sit inside an argument, and compares
  positions in a chain so a command that records a gate before advancing defers to
  `atj event advance`. 19 behavioural cases, both directions.
- `atj event unit record` keeps the real `completed_at` (D15), the bye check gates
  on byes rather than on a policy name (D20), whole-tree scans ask git rather than
  the filesystem (D17), and `atj score`'s console output prints
  `adjudication_required` instead of contradicting the JSON beside it (D7).
- `atj event approve` writes `approval_state`, which six sites read and nothing
  could set (D25), and audit reports have a schema at last — the artifact kind
  that authorizes every stage transition was the least validated in the framework
  (D26).

### Added earlier in this cycle, before the live trial

- `atj intake`, the front door. It materializes a submission from a git URL, a
  local repository, a directory or a `.zip` into `workspaces/<event>/<team-id>/`,
  pins it to an immutable commit, writes the intake record, and adds or updates
  the roster row. Every step downstream of intake assumed a checkout and a commit
  that nothing produced; they were placed by hand.
- A reproducible snapshot commit for deliveries that carry no history. Fixed
  identity and fixed timestamps make the hash a pure function of the delivered
  tree, so an archive pins to the same commit on any machine, and the intake
  record states that the commit is the tool's and not the team's.
- Archive intake refuses path traversal, absolute paths, symbolic links,
  non-regular entries, and over-sized or over-compressed archives, before
  extracting anything. Checkouts are built beside their destination and swapped
  into place, so a refused or failed ingest leaves no partial tree and does not
  destroy the checkout already there.

#### Changed

- `prepare-submission` 1.0.0 -> 1.1.0: it now runs `atj intake` rather than
  assuming a checkout exists, and completes the narrative sections of the record
  the tool leaves open.

### Known limitations

- A network allowlist still needs an egress proxy this repository does not
  provide. Configuring one without a proxy is refused, and that path is untested
  end to end.
- The judge-independence detector is a similarity heuristic plus a score-vector
  check. Systematic paraphrase by a contaminated judge is not caught.
- Hooks are guard rails, not a security boundary. `atj validate`, the publication
  gate and the audit gates are.
- AI judgment is not deterministic, and nothing here claims otherwise. The sample
  event's judge scores are scripted so CI can reproduce the pipeline without a
  model call, and every artifact in it says so.
- No event has yet decided anything real. `docs/final-audit.md` lists what a human
  must do first.


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

From the final independent release audit:

- A clean checkout did not pass its own validation block: Git tracks no empty
  directory, so `events/sample-mock-2026/runs/` was absent and three tests failed.
- A consolidated report's official total was never compared against the judgments
  it claimed to summarise. An edited total, or a judgment edited after
  consolidation, passed every gate and then fed bye seeding.
- No code path applied an adjudication's `score_override`. The sample event's own
  headline total was unreachable from any operator command.
- Rendered team dossiers were written into `events/*/public/`, and report
  validation scanned only Markdown, so a team's own score sat ungated in the
  public tree.
- The team-facing gate scanned only secrets and deliberation markers: another
  team's score, another team's findings and personal data all passed as
  advisories and reached rendered output.
- An artifact declaring `scores_published: true` overrode the event official's
  `public_scores: false`.
- Winner advancement did not exist. Every match recorded `winner: null`, the
  final's entrants were empty on a completed event, and match identifiers in the
  bracket contradicted the matchup reports.
- Staleness detection and the unit ledger were library code no command called, so
  a judgment edited after consolidation was invisible.
- Stage gates were self-certified booleans. An event reached `complete` in
  eighteen commands with zero evidence, judgments, matchups or dossiers.
- Judge independence was asserted in prompts and observed nowhere.
- The built wheel shipped twenty Python files and none of the framework data it
  reads, so every command failed on an installed package. CI built the wheel and
  never ran it.
- `bracket verify` without a roster trusted the constraint audit inside the file
  it was verifying.
- Unescaped bracket fields allowed markup injection into the ceremony page.
- The status ledger was written non-atomically, so an interrupt destroyed the one
  file recovery depends on.
- The approved public summary's results table was silently dropped from the
  ceremony render.

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

### Added in repair

- `atj bracket advance`, which records a match winner and carries it forward, and
  refuses to advance anyone when a matchup returned no winner unless an approved
  adjudication names the advancing team.
- `atj event unit`, which writes and inspects the recovery ledger and re-derives
  each unit's input digest from the artifacts on disk.
- `atj score --adjudications`, applied automatically when the judgments directory
  sits inside an event.
- A consolidation cross-check, a judge-independence detector, personal-data
  scanning, and gating of rendered HTML in public and team-facing locations.
- `tools/stage_package_data.py`, so the wheel ships the framework data, and a CI
  step that installs and runs it.

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
- Judge independence is enforced by procedure and detected after the fact, not
  prevented by the tool surface. Judges hold read-only tools that are not
  path-restricted; the `judge-submission` skill stages reports outside `events/`
  until the panel completes, and near-duplicate wording between two judgments is
  flagged. That is a control and a detector, not a guarantee.
- Several controls end in a human. The framework refuses to pass a gate without an
  audit artifact, to advance a winner without a confirmed result or a recorded
  adjudication, or to publish without a named approver. It cannot check that the
  audit was performed carefully, that the approver read what they approved, or
  that an `--force-reason` override was justified.

## 0.1.0-alpha

Architectural scaffold: rubrics, policies, templates, agent and skill
definitions, five scripts and eleven tests.
