---
event_id: live-trial-2026
audit_scope: configuration stage
audit_id: configuration
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.0.0
persona: judging-auditor@1.0.0
framework_commit: 152dd2c10547a1c15bb56c4b1a90764b28354c59
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-16T23:39:00Z"
completed_at: "2026-09-16T23:40:00Z"
visibility: private
approval_state: approved
validation_state: valid
result: PASS WITH ADVISORIES
---
# Judging Audit — configuration stage

## Result

**PASS WITH ADVISORIES**

Second pass, after repair. The major finding that failed the first pass is fixed
and verified, and so are both minor findings. No blocking or major finding
remains. Two minor findings are recorded below; neither blocks the
`configuration-audited` gate, and both are cheap to close before the evidence
stage. Five advisories carry forward.

## Scope and artifacts inspected

Stage: configuration. Gate this audit governs: `configuration-audited`
(`atj/event.py`, stage gate map). This audit supersedes the first-pass audit of
the same scope, which returned FAIL.

Event artifacts inspected:

- `events/live-trial-2026/event.md`
- `events/live-trial-2026/teams.md`
- `events/live-trial-2026/status.md`
- `events/live-trial-2026/bracket.md`
- `events/live-trial-2026/submissions/team-podcast.md`
- `events/live-trial-2026/submissions/team-ledger.md`

Canonical sources checked against:

- `framework/rubrics/submission-evaluation.md`
- `framework/rubrics/panel-consolidation.md`
- `framework/rubrics/head-to-head.md`
- `framework/rubrics/bracket-assignment.md`
- `framework/personas.md`
- `framework/policies/execution-safety.md`
- `framework/policies/disagreement-and-adjudication.md`
- `framework/policies/report-publication.md`
- `framework/templates/event-configuration.md`
- `framework/templates/audit-report.md`
- `schemas/event.schema.json`, `schemas/common.schema.json`
- `atj/sandbox.py`, `atj/event.py`, `atj/cli.py`, `atj/reports.py`, `VERSION`

Submission checkouts inspected read-only, never executed:

- `workspaces/live-trial-2026/team-podcast`
- `workspaces/live-trial-2026/team-ledger`

## Deterministic validation results

Re-run for this pass, on the repaired artifacts:

```
$ python3 -m atj event validate events/live-trial-2026
Event validation: PASS (0 problems, stage configuration)

$ python3 -m atj validate reports events/live-trial-2026
Report validation: PASS — 3 artifacts, 0 blocking, 0 major, 0 minor, 0 advisory

$ python3 -m atj sandbox preflight
Sandbox preflight: AVAILABLE
  podman 6.1.0 (rootless)

$ python3 -m atj personas
Persona registry: PASS (15 agents)
```

Supporting deterministic checks:

```
$ python3 -m atj release-check
Release check: PASS   (single-source PASS, version-skew PASS, templates PASS)

$ python3 -m atj event status events/live-trial-2026
Event live-trial-2026  stage: configuration
  teams: 2 on roster, 2 eligible
  gate: configuration-audited = pending
  units: none recorded

$ git cat-file -t 152dd2c10547a1c15bb56c4b1a90764b28354c59
commit

$ git -C workspaces/live-trial-2026/team-podcast rev-parse HEAD
f3fdd342465fa6bc2a52d226a8613b082ad329e0

$ git -C workspaces/live-trial-2026/team-ledger rev-parse HEAD
9d21b7707f204ef60f5a1cee612f1d4db0a4a575
```

No official arithmetic exists at this stage. Nothing in this audit was
recalculated from prose.

### Repair verification

**F1 — repaired.** `events/live-trial-2026/event.md` now carries all four
sections `framework/templates/event-configuration.md` defines, with real content
rather than headings alone. Purpose states the subject, the two submissions'
provenance and consent, that no award follows, and that eligible scope is the
full repository at the pinned commit. Schedule gives a submission-freeze instant
of `2026-09-16T23:30:00Z`, which is after both recorded intakes
(`2026-09-16T23:27:41Z` and `2026-09-16T23:29:24Z`), and states that the
remaining milestones are gate-driven rather than wall-clock. Eligibility and
human officials states the eligibility rule actually applied — one pinned
immutable commit, a reachable repository, a checkout matching the pin — which is
the rule this audit independently verified under Decision 3, and it names the
human holding the single official role. Its claim of "eight independent
judgments" is consistent with two teams and the four `expected_judges`. Its
version claim, `0.2.0-beta`, matches `VERSION`. Execution environment is assessed
next.

**F2 — repaired.** `validation_state: valid` in `events/live-trial-2026/event.md`
is one of the three values in the `validation_state` enum of
`schemas/common.schema.json`.

**F3 — repaired, and the remedy I originally stated was wrong.** I recommended
recording an intake unit per team. I verified that this is not possible and not
correct. `atj/event.py`, `derive_digests` builds digests only for
`evidence:<team>`, `judging:<team>` and `consolidation:<team>`; nothing else. In
`atj/cli.py` the unit-record path looks the requested id up in exactly that
mapping and returns a usage error, "cannot derive an input digest", for any other
id. An intake unit is therefore unrepresentable, so `units: []` is the correct
state at this stage rather than an omission, and `atj event status` reporting
"units: none recorded" is the expected output. **This should not be re-flagged at
the roster-freeze or evidence gate.** `events/live-trial-2026/status.md` now
records this in the file itself, populates a Team progress row per team with the
correct pinned commits, and logs both intakes, the first-pass audit and the
repair in the Activity log. See F5 for a timestamp defect in that log.

### Decision 4 (re-examined) — is the delegated execution documentation adequate?

Yes. I checked each thing `framework/policies/execution-safety.md` requires
against what `atj/sandbox.py` actually does, rather than accepting the event's
claim that the module covers it:

| Policy requirement | Enforced in `atj/sandbox.py` |
|---|---|
| isolated disposable environment | `--rm`, container per run |
| no writable access outside the sandbox | `--read-only`, source mounted `:ro`, writes confined to a `noexec,nosuid` temporary filesystem |
| no host secrets or credentials | no host mounts beyond the read-only source, `HOME` redirected into the sandbox, unprivileged numeric user |
| network disabled by default | `--network none` unless an authorized egress proxy is supplied |
| CPU, memory, disk, process and time limits | `--cpus`, `--memory`, temporary-filesystem size cap, `--pids-limit`, run timeout, captured-output cap |
| no weakening of host protections | `--cap-drop ALL`, `no-new-privileges`, and an explicit refusal to build a command containing privileged, host-network, host-pid, host-userns, capability-add or a docker socket mount |
| record commands and preserve output | the execution record carries command, exit status, both output streams, duration, timeout and truncation flags, the applied limits, runtime, runtime version, image and timestamps |

The event's decision not to restate the limits is correct, not a gap. `CLAUDE.md`
requires exactly one editable copy of a fact and says to read a canonical number
rather than restate it; a copy of the limits in `event.md` could drift from the
module that enforces them, and `atj release-check` exists to catch precisely that
duplication. The section names the enforcing module, so the fact is locatable,
and the applied limits are written into every run record, so what was actually
enforced is recoverable per execution.

The rest of the section is accurate. `execution_mode: sandboxed` with an empty
`network_allowlist` matches preflight, which reports `podman 6.1.0 (rootless)`.
`schemas/event.schema.json` notes that `sandboxed` requires a verified container
runtime and has no host fallback; `atj sandbox run` refuses rather than degrading,
and it refuses a configured allowlist without an authorized proxy instead of
silently granting full network access, which is consistent with the section's
statement that no egress proxy is authorized. The evidence-capture claim matches
the record structure field for field, and the statement that a criterion without
direct evidence is `NE` matches `CLAUDE.md` and the execution-dependent criteria
the module names.

Two items the section does not settle are recorded as F4 and A6.

### Decisions 1, 2, 3 and 6 — unchanged and re-verified

Re-checked against the repaired `event.md`; nothing in the front matter moved
except `validation_state`.

Versions: `submission-evaluation@1.0.0`, `panel-consolidation@1.0.0`,
`head-to-head@1.0.0` and `bracket-assignment@1.0.0` each resolve to the matching
`rubric_id` or `policy_id` and `version` in `framework/rubrics/`.
`close_call_band: 5` agrees with `framework/rubrics/head-to-head.md`.
`bye_policy: performance-qualified` is listed and is the default in
`framework/rubrics/bracket-assignment.md`, and agrees with
`events/live-trial-2026/bracket.md`. The four `expected_judges` are all in the
registry as initial judges at 1.0.0, and four exceeds `minimum_panel: 2` in
`framework/rubrics/panel-consolidation.md`. `atj release-check` reports
`version-skew PASS` and `single-source PASS`.

Officials: all four authorities named, held by `event-director`, now with the
holder identified in the Eligibility and human officials section.
`framework/policies/disagreement-and-adjudication.md` requires a human official
and imposes no separation of duties, so one holder is permitted; the section
states what happens when a second human would ordinarily be needed.

Framework commit: `152dd2c10547a1c15bb56c4b1a90764b28354c59` resolves —
`git cat-file -t` returns `commit` — and is the repository tip. The same commit
is pinned in both intake records.

Submission pins: both commits are 40-character object names, and each matches its
checkout by `git rev-parse HEAD`; each checkout's `origin` equals the declared
repository URL; both working trees are clean. The same hash agrees across the
roster row, the intake front matter and the intake provenance table for each
team. Submission checkouts are gitignored, so no student code is committed here.

Bracket: `north-campus` and `south-campus` are distinct, so no group-separation
constraint applies; `min_teams: 2` permits a two-team bracket;
`events/live-trial-2026/bracket.md` is correctly `status: not-built` with
`random_seed: null`.

## Findings

| Severity | Rule | Artifact | Finding | Required repair |
|---|---|---|---|---|
| minor (F4) | `framework/templates/event-configuration.md`: "Document the approved sandbox"; `framework/policies/execution-safety.md`: use an isolated disposable environment | `events/live-trial-2026/event.md`, Execution environment | The section names the approved runtime and isolation profile but never names the approved container image. The module default is a mutable upstream tag rather than a pinned digest, and it is a language-specific base that cannot run both submissions: the team-ledger checkout is a Python project, while the team-podcast checkout is a web and server project with its own launch script. A judge will therefore choose an image per submission at the evidence stage with no recorded authorization and no comparability rule. This is minor, not major, because image choice does not weaken isolation — every run gets the same read-only, no-network, unprivileged, capability-dropped container — and the image actually used is written into each run record, so any deviation is visible at the judgments audit. | Before the evidence stage, name in the Execution environment section which images are approved, preferably by digest, and state who authorizes a per-submission image. Because the event is active, treat this as completing documentation of an existing decision, not as changing configuration after judging begins; judging has not begun. |
| minor (F5) | timestamp accuracy; `CLAUDE.md`: `status.md` records what is real | `events/live-trial-2026/status.md` | The Activity log's repair row is stamped `2026-09-16T23:52:00Z`. That is later than the file's own `last_updated: "2026-09-16T23:37:37Z"`, and later than the actual time at which this audit read the file. A ledger row cannot post-date the ledger's own last update, and no row may be future-dated. | Correct the repair row to the real time of the repair and set `last_updated` to a time at or after the newest row. |

## Advisories

**A1 — intake narrative sections are still unfilled, which is correct here.** Both
`events/live-trial-2026/submissions/team-podcast.md` and
`events/live-trial-2026/submissions/team-ledger.md` carry "Not supplied at
intake. Complete this from the team's submission before judging." under Team
statement, Primary workflows, Run instructions, AI and external services, and
Known limitations. Expected at this stage: `atj intake` materializes and pins the
submission and says in the artifact that it does not supply those sections. Not a
configuration failure. It must be resolved during the evidence stage, because Run
instructions and AI and external services feed sandboxed execution and the
evidence package, and `framework/policies/evidence-and-citation.md` requires every
score to cite evidence in that package. Run instructions are also the input F4
depends on: they determine which image each submission needs.

**A2 — intake records remain `approval_state: draft`, `validation_state:
unvalidated`.** Verified unchanged in this pass. Correct while the narrative is
incomplete; move to approved and valid when A1 is resolved, before evidence
validation.

**A4 — both submissions contain agent-directed instruction files.** The
team-podcast checkout carries an agent project configuration file; the team-ledger
checkout carries a skills directory with four skill definitions and a directory
containing a commit hook. For an agentic-software tournament these are plausibly
part of the product and legitimately in scope for judging. They are also exactly
the shape of file that can attempt to steer a judging agent. A targeted text scan
of both checkouts for common injection phrasing returned no matches; that scan is
not exhaustive and proves nothing beyond itself. Judges must open these as data,
must not let a submission-local agent configuration or commit hook take effect in
their own session, and must confine all execution to the sandbox per
`framework/policies/execution-safety.md`.

**A5 — preflight is a point-in-time result.** `AVAILABLE` was observed on this
host during this audit. Re-run `atj sandbox preflight` at the start of the
evidence stage and record `execution_status: unavailable` with `NE` on affected
criteria if it changes.

**A6 — the run timeout can be raised from the command line.** The module default
bounds a run, but `atj sandbox run` accepts a timeout override, and the Execution
environment section does not say whether raising it is permitted. Any run that
uses a longer timeout than the default should be justified in the evidence
package. The applied limits are written into the run record, so the deviation is
detectable at the judgments audit.

**A7 — the operator's real name now appears in a private artifact.** The
Eligibility and human officials section of `events/live-trial-2026/event.md`
names the human holding the official role. Correct there: the file is
`visibility: private` and `public_scores: false`.
`framework/policies/report-publication.md` bars personal data from public output,
so the name must not propagate into anything under
`events/live-trial-2026/public`. Run `atj validate publication` on anything that
would leave the panel.

A3 from the first pass is resolved: the official role holder is now identified.

## Completion gate

- [x] No blocking findings — none raised in either pass
- [x] No major findings — F1 from the first pass is repaired and verified above;
      nothing major was found in this pass
- [x] Calculations valid — no official arithmetic exists at the configuration
      stage; nothing was recalculated from prose
- [x] Evidence references resolve — every version reference resolves to its
      canonical file, the pinned framework commit is a real object, and both
      submission commits match their checkouts by `git rev-parse HEAD`
- [x] Version and identity checks pass — `atj release-check` reports
      `version-skew PASS` and `single-source PASS`; `atj personas` reports PASS
      for all 15 agents including the four `expected_judges`
- [x] Privacy boundary passes — `events/live-trial-2026/public` holds only a keep
      file; `public_scores: false`; every artifact inspected declares
      `visibility: private`; submission checkouts are gitignored. See A7 for the
      one item to watch at publication time.

Final result: **PASS WITH ADVISORIES**. The `configuration-audited` gate may be
set. Close F4 before the evidence stage, because it decides how both submissions
are executed, and close F5 at the same time the gate is recorded. Carry A1, A2,
A4, A5, A6 and A7 into the evidence stage.
