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

Approved images. The module default `docker.io/library/python:3.12-alpine`
cannot produce execution evidence for either submission: it has no test runner,
and with `--network none` nothing can be installed at run time. Two images were
built for this event instead. They are built with network access so that the
container can run without it.

| Team | Approved image | Image ID | Contents |
|---|---|---|---|
| team-ledger | `localhost/atj-live-trial/ledger:2` | `7780b2b9e6e1` | python:3.12-slim, poppler-utils, pyyaml, duckdb, pytest |
| team-podcast | `localhost/atj-live-trial/podcast:3` | `c3670644bc7b` | python:3.12-slim, chromium, fonts-liberation, ffmpeg, fastapi, pydantic, uvicorn[standard], playwright |

Where each package comes from, stated exactly rather than loosely:

- team-ledger: `pyyaml` and `duckdb` are `pyproject.toml` dependencies; `pytest`
  is its declared dev extra. `poppler-utils` is **not** declared by the
  submission. It supplies the `pdftotext` binary that the ingest path shells out
  to, and without it PDF ingest fails for a reason that has nothing to do with
  the submission's quality. It is added deliberately and named here.
- team-podcast: `fastapi` and `pydantic` are imported by `server/`; `playwright`
  is `tests/requirements.txt`; `chromium` is the browser `tests/e2e.py` expects
  at `/usr/bin/chromium`. `ffmpeg` supplies the `ffmpeg` and `ffprobe` binaries the
  README lists as prerequisites; without them the library cannot be populated and
  `tests/e2e.py` stops at stage 1 of 11 for a reason that has nothing to do with the
  submission. Added on the same reasoning as `poppler-utils` above, after an initial
  omission produced an unfair evidence asymmetry against this team.
  `uvicorn[standard]` matches what `run.sh` installs —
  plain `uvicorn` is a different server runtime and was corrected. An earlier
  build of this image also carried `httpx` and `pytest`, neither of which appears
  anywhere in the checkout; both were removed.

Debian slim rather than alpine: duckdb publishes manylinux wheels but no musl
wheel, so alpine attempts a source build and fails.

Image IDs are recorded above because the tags are mutable and `atj/sandbox.py`
records only the image string, not a resolved digest. Both Containerfiles start
from a mutable base and use open-ended version ranges, so the tag alone would let
a silent rebuild pass unnoticed; the ID is what makes a rebuild detectable. The
Containerfiles are committed under `events/live-trial-2026/evidence/`.

An untrusted submission now influences what is installed into the image that
judges it, and package installation runs third-party setup code with network at
build time. That happens inside podman, never on the host, and never runs the
submission's own code. The dependency lists are short, mainstream, and recorded.

This table was amended after the configuration gate passed, which is permitted
only because no judging has begun. The amendment is in scope for the intake stage
audit; it does not inherit the passed configuration gate. The intake audit ruled
that it needs a ledger entry rather than a manual override record, because
nothing was overridden and no rule was excepted.

Evidence capture: every execution is recorded through `atj sandbox run --output`,
which writes a run record naming the runtime, version, command, exit status,
duration and captured output. Those records are the direct observations judges
may cite. A criterion with no execution evidence and no other direct evidence is
`NE`, never an inferred score.
