---
event_id: live-trial-2026
event_name: First Live Trial 2026
status: active
rubric: submission-evaluation@1.0.0
consolidation_policy: panel-consolidation@1.0.0
matchup_rubric: head-to-head@1.0.0
bracket_policy: bracket-assignment@1.0.0
bye_policy: performance-qualified
close_call_band: 5
execution_mode: sandboxed
network_allowlist: []
expected_judges:
- judge-backend
- judge-frontend-ux
- judge-security-ops
- judge-product-agentic
public_scores: false
framework_commit: 152dd2c10547a1c15bb56c4b1a90764b28354c59
model_requested: claude-opus-5
model_used: null
started_at: "2026-09-16T00:00:00Z"
completed_at: null
visibility: private
approval_state: approved
validation_state: valid
officials:
  disqualification: event-director
  adjudication: event-director
  publication_approval: event-director
  security_escalation: event-director
---
# Event Configuration

## Purpose

First live trial of the AI Tournament Judge framework at `0.2.0-beta`. The subject
is the framework itself: this event exists to exercise the agent layer end to end
with a real model, on real applications, under real container isolation. Every
prior exercise used either scripted fixtures or the four initial judges alone.

Two submissions compete, drawn from the operator's own repositories with their
consent. They are ordinary working applications, not student work, and no award
or standing follows from the outcome. The result that matters is whether the
pipeline produces defensible, evidence-backed artifacts, not which application
wins.

Eligible scope is the full repository at the pinned commit, including its tests,
configuration and documentation.

## Schedule

| Milestone | Date and time | Owner |
|---|---|---|
| Submission freeze | 2026-09-16T23:30:00Z (both intakes pinned) | event-director |
| Initial judging complete | when the eight independent judgments validate | event-director |
| Bracket frozen | after consolidation is audited | event-director |
| Ceremony | not held; this event produces no public ceremony | event-director |

The schedule is driven by stage gates rather than wall-clock deadlines. A stage
advances when its audit passes, and not before.

## Eligibility and human officials

Both teams are eligible. Eligibility here means one pinned immutable commit, a
reachable source repository, and a checkout that matches the pin; there is no
enrollment or category rule to apply, because this is a trial and not a
competition among participants.

`event-director` holds all four authorities: disqualification, adjudication,
publication approval, and security escalation. Gregg Reed holds that role. The
framework does not require separation of duties, and with a single operator none
is available; an adjudication that would ordinarily go to a second human is
recorded as an operator decision and named as such in the artifact.

`public_scores: false`. No artifact from this event is approved for publication,
so the publication-approval authority is expected to go unused. Anything that
would leave the panel must still pass `atj validate publication`.

## Execution environment

Execution is authorized. `atj sandbox preflight` reports `podman 6.1.0
(rootless)`, which is verified container isolation; there is no host fallback and
none is permitted.

`execution_mode: sandboxed`. `network_allowlist` is empty, which means no
destination is enabled and no egress proxy is authorized. A submission that
cannot run without network access is evidence-limited on that point, and the
limitation is recorded rather than worked around.

Resource limits, the read-only source mount, the dropped capabilities and the
timeout are enforced by `atj/sandbox.py` and are not restated here; the module is
the source of truth for them, and `atj sandbox run` refuses to start if isolation
cannot be verified at the moment of execution.

Approved images. `atj/sandbox.py` defaults to `docker.io/library/python:3.12-alpine`,
which suits `team-ledger` (a Python project with `pyproject.toml`) but cannot run
`team-podcast`, which ships a server and a web client. Two images are authorized
for this event, and no other may be used without a recorded override:

| Team | Approved image | Why |
|---|---|---|
| team-ledger | `docker.io/library/python:3.12-alpine` | the module default; the submission is a Python package with its own test suite |
| team-podcast | `docker.io/library/python:3.12-alpine` | the submission's server is Python; its web client is static and needs no runtime |

Both are upstream mutable tags rather than pinned digests, which is a known
weakness: the same tag can resolve to different bytes later, so an execution is
reproducible only within this event's window. Every run record written by
`atj sandbox run` names the image actually used, so a deviation from this table
is visible at the judgments audit rather than silent. Pinning by digest is
deferred to a later framework version, not decided per event by a judge.

Evidence capture: every execution is recorded through `atj sandbox run --output`,
which writes a run record naming the runtime, version, command, exit status,
duration and captured output. Those records are the direct observations judges
may cite. A criterion with no execution evidence and no other direct evidence is
`NE`, never an inferred score.
