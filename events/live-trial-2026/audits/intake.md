---
event_id: live-trial-2026
audit_scope: intake stage
audit_id: intake
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.0.0
persona: judging-auditor@1.0.0
framework_commit: 152dd2c10547a1c15bb56c4b1a90764b28354c59
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-16T23:44:00Z"
completed_at: "2026-09-16T23:53:00Z"
visibility: private
approval_state: approved
validation_state: valid
result: PASS WITH ADVISORIES
---
# Judging Audit — intake stage

## Result

**PASS WITH ADVISORIES**

The roster is frozen and correct, and both intake records are genuinely ready to
carry eight independent judgments. I verified the substance rather than the shape:
I re-derived a sample of the cited facts from the checkouts themselves, and both
records separate team claims from direct observations from inferences as
`framework/policies/evidence-and-citation.md` requires. The mid-event amendment
to the approved-images table is legitimate and does not need a manual override
record; my reasoning is below, and so is the one thing it must gain before the
evidence stage.

Five minor findings. None is blocking and none is major, so none holds the
`roster-frozen` gate. One of them matters more than its severity suggests: the
team-ledger sandbox run of "35 passed" left no run record, so I could not verify
it and no judge may cite it yet.

## Scope and artifacts inspected

Stage: intake. Gate this audit governs: `roster-frozen` (`atj/event.py`,
`STAGE_GATES` maps `intake` to `roster-frozen`; `STAGES` lists `intake` between
`configuration` and `evidence`). `atj event status` confirms the event is at
stage `intake` with that gate pending.

Event artifacts inspected:

- `events/live-trial-2026/teams.md`
- `events/live-trial-2026/submissions/team-podcast.md`
- `events/live-trial-2026/submissions/team-ledger.md`
- `events/live-trial-2026/event.md`, Execution environment section, as amended
- `events/live-trial-2026/evidence/Containerfile.ledger`
- `events/live-trial-2026/evidence/Containerfile.podcast`
- `events/live-trial-2026/status.md`
- `events/live-trial-2026/runs` and `events/live-trial-2026/judgments`, both empty

Canonical sources:

- `framework/policies/evidence-and-citation.md`
- `framework/policies/execution-safety.md`
- `framework/templates/manual-override-record.md`
- `framework/templates/submission-intake.md`
- `CLAUDE.md`, the prohibition on changing an active event and the
  narrow-but-never-weaken rule
- `atj/event.py`, `atj/sandbox.py`

Read-only inspection of both submission checkouts, and two container runs that
started the approved images with no submission mounted and no network, purely to
read what is installed in them. No submission code was executed by this audit.

## Deterministic validation results

```
$ python3 -m atj event validate events/live-trial-2026
Event validation: PASS (0 problems, stage intake)

$ python3 -m atj validate reports events/live-trial-2026
Report validation: PASS — 3 artifacts, 0 blocking, 0 major, 0 minor, 0 advisory

$ python3 -m atj event status events/live-trial-2026
Event live-trial-2026  stage: intake
  teams: 2 on roster, 2 eligible
  gate: roster-frozen = pending
  units: none recorded
```

`validate reports` counts 3 artifacts: the two intake records and the
configuration audit. The two Containerfiles under `evidence` are not
front-matter artifacts and are not counted; that is expected.

Checks this audit ran directly:

```
$ podman images
localhost/atj-live-trial/ledger:1    5f523f17ce3a   218 MB
localhost/atj-live-trial/podcast:1   1583b1a42534   1.03 GB

$ podman run --rm --network none localhost/atj-live-trial/podcast:1 \
      sh -c 'which chromium; chromium --version'
/usr/bin/chromium
Chromium 152.0.7977.82 built on Debian GNU/Linux 13 (trixie)

$ podman run --rm --network none localhost/atj-live-trial/ledger:1 \
      sh -c 'which pdftotext || echo ABSENT; ...import duckdb, yaml, pytest...'
pdftotext: ABSENT
deps ok
```

## Roster

`events/live-trial-2026/teams.md` is `frozen: true` at `roster_version: 1`. Two
teams, both `Eligible: yes`, both `Submission status: received`, affiliation
groups `north-campus` and `south-campus`, which are distinct. Each row carries a
40-character commit that matches the pinned commit in the corresponding intake
record and the checkout on disk, as verified in the configuration audit and
unchanged since. The roster is correct and ready to freeze the bracket against
later.

## Intake records — substance

`framework/policies/evidence-and-citation.md` requires reports to distinguish
direct observation, artifact evidence, team claim and inference, and to cite path
and line or symbol where practical. Both records do this explicitly and
consistently rather than as a formality.

team-ledger labels its classes in the text: "Direct observation:" opens four
separate passages; the LLM rule-proposal workflow is marked "a team claim about a
human-in-the-loop workflow, not something this checkout can independently
demonstrate"; the 1Password conclusion is marked "an inference, not a
demonstrated fact"; and the environment variable names it could not read are
recorded as "**undetermined**" rather than guessed. That last one is the strongest
evidence that the record is honest: the repository's own `.claude/settings.json`
does carry a `Read` deny rule for `.env` paths under the submission workspace
directory, exactly as the record cites, so the record hit a control, recorded the
gap, and did not work around it.

team-podcast does the same in its own idiom: "Inferred from the FastAPI routes
in..." opens the workflow list; the README's deployment status line is marked "the
team's own account of on-device testing, not something this intake observed"; an
entire limitation bullet is devoted to "All 'Confirmed'/'Verified' claims are team
claims, not observations made here"; and the configuration variable list is marked
as drawn from the README "not a direct read of the file" because the same deny
rule blocked it.

I re-derived a sample of the load-bearing facts from the checkouts. Every one
held:

| Claim in the record | Where I checked | Result |
|---|---|---|
| team-ledger: 31 `test_` functions in `tests/test_properties.py`, 400 lines | the file | 31 and 400 exactly |
| team-ledger: deps `pyyaml>=6.0`, `duckdb>=1.0`, dev `pytest>=8.0`; `fin = "fin.cli:main"`; `testpaths`/`pythonpath` set | `pyproject.toml` | all four exactly as cited |
| team-ledger: the only environment read under `src/fin` is `FIN_DATA_DIR` | grep across `src/fin` | one hit, `src/fin/store.py:53` |
| team-ledger: the pinned commit credits a model co-author | the commit message | present as described |
| team-podcast: `tests/e2e.py` hardcodes `/usr/bin/chromium` | the file | present, at line 28 rather than the cited 26 |
| team-podcast: 43 `check(...)` call sites | the file | 43 exactly |
| team-podcast: README says 33 files / 1,360 MB but the checkout holds 56 | README line 6, and a file count | README says 33; the checkout holds 56 |
| team-podcast: internal inconsistency, 34/34 versus 42/42 | README lines 7 and 285 | both present, as quoted |
| team-podcast: `tests/requirements.txt` pins `playwright>=1.50` | the file | exact |

The README discrepancy team-podcast found is real and is the kind of thing the
intake stage exists to surface: the submission's own status line understates its
content by 23 episodes, and the record correctly frames that as a stale team
claim rather than as a defect.

Both records also report a deliberate injection search across the whole checkout
and state that nothing was found and nothing was followed. That is the correct
posture toward the agent-directed files in both submissions and it matches the
scan I ran during the configuration audit. See advisory A4.

Conclusion: both records are ready to be judged against. A1 from the
configuration audit is resolved.

## The approved-images amendment

**Was amending a gated configuration mid-event legitimate here? Yes.**

`CLAUDE.md` prohibits changing "an active event's rubric version, weights,
personas, bracket policy, or evidence after judging begins". The approved-images
table is none of those five things, and judging has not begun:
`events/live-trial-2026/judgments` is empty and no judgment artifact exists
anywhere in the event. The prohibition does not reach this change by its own
terms. `CLAUDE.md` also allows event configuration to "narrow behavior but not
weaken safety, evidence, or privacy rules", and this change narrows: it removes a
default image that could produce no execution evidence at all and names two
specific images instead. The isolation parameters are untouched; every run still
gets no network, a read-only source mount, dropped capabilities and the module's
limits, because the image is the base filesystem and not the sandbox policy.

It is also symmetric. Each team got an image built from its own submission's
declared dependencies, so neither team gains an advantage from the change, and
the alternative — keeping the module default — would have forced `NE` on every
execution-dependent criterion for both teams. That is a materially worse evidence
outcome, so the amendment improves the event rather than bending it.

**Is the justification in `event.md` adequate? Substantially yes, with one
inaccuracy.** The section states what was wrong with the default, why Debian slim
rather than alpine, why chromium is baked in, that the tags are mutable, that the
Containerfiles are recorded, that every run record names the image, and — the
part that matters most — that building the images executed third-party package
installs at build time inside podman and that no submission code has run on the
host. Disclosing the build-time execution unprompted is the right instinct. The
inaccuracy is F1 below: the table's claim that each image was built from its
submission's declared dependencies "and nothing else" is false for team-podcast.

**Is building images from a submission's declared dependencies consistent with
`framework/policies/execution-safety.md`? Yes, with the risk named.** The policy
governs executing the submission and requires isolation, no host secrets, no
network by default, limits, and recorded output. None of that is touched. The new
surface the amendment introduces is that an untrusted submission now influences
what gets installed into the image that will judge it, and package installation
runs third-party setup code with network access at build time. That is a real
widening of the build-time surface, and it is the reason this amendment deserved
the scrutiny it is getting. It is acceptable here because the build happens in
podman rather than on the host, both dependency lists are short and consist of
mainstream published packages, the Containerfiles are recorded in the event so
the inputs are inspectable, and the policy's actual execution requirements are
unchanged. I read both Containerfiles in full: neither runs anything from the
submission checkout, neither copies the submission into the image, and neither
adds a capability, a mount or a network permission to the run-time container.

**Does this need a manual override record? No, and producing one would be
wrong.** `framework/templates/manual-override-record.md` is for the case where "a
human official has overridden a framework result", in one of the categories
reserved to humans: disqualification, unresolved final ties, rules exceptions,
security escalation, publication approval. No framework result was overridden
here — the tooling produced no result about images — and no rule was excepted,
because no rule barred the change. Filing an override for an ordinary
pre-judging configuration completion would dilute what an override means in this
event's record. What the amendment does need is a ledger row naming when it
happened and who authorized it, which is F3.

## Findings

| Severity | Rule | Artifact | Finding | Required repair |
|---|---|---|---|---|
| minor (F1) | a configuration statement must be accurate; `framework/policies/evidence-and-citation.md` bars manufacturing certainty | `events/live-trial-2026/event.md`, approved-images table, and `events/live-trial-2026/evidence/Containerfile.podcast` | The table says the two images were built "each from its submission's own declared dependencies and nothing else", and sources the team-podcast list from "runtime imports under `server/`, plus `tests/requirements.txt`". Two of the seven installed packages are not from either source. A grep across `server`, `tests`, `run.sh` and `README.md` in the team-podcast checkout returns no reference to `httpx` at all, and the submission declares no `pytest` dependency anywhere — its only test is a standalone script, not a pytest suite. The image also installs plain `uvicorn`, while `run.sh` installs `uvicorn[standard]`, which is a different dependency set and therefore a different server runtime from the one the team documents. None of this weakens isolation or favors a team, which is why it is minor, but the configuration currently asserts a provenance it does not have. | Either drop `httpx` and `pytest` from the team-podcast image, or correct the table to state that the image adds evaluator tooling the submission does not declare, naming which packages, and record that the image provides plain `uvicorn` rather than the `uvicorn[standard]` the submission installs. Note the difference wherever server behavior is judged. |
| minor (F2) | `events/live-trial-2026/event.md`: "every execution is recorded through `atj sandbox run --output`" | `events/live-trial-2026/runs`, and the provenance footer of both intake records | A sandbox execution of the team-ledger suite is reported to have produced 35 passed at exit 0 under rootless podman with no network. `events/live-trial-2026/runs` contains only a keep file, so no run record exists for it, and the event's status ledger has no row for it either. **I could not verify that run and I am recording the check as not performed, not as passed.** The numbers themselves are at least self-consistent: the record's count of 31 test functions plus the five cases of the single `parametrize` in `tests/test_properties.py` expands to exactly 35 collected tests, which reconciles the record with the reported result — but arithmetic consistency is not verification. Separately, both intake records still close with "Nothing in this submission has been executed", which is now inaccurate for team-ledger. | Re-run the suite through `atj sandbox run --output` so a run record lands in `events/live-trial-2026/runs`, or write the record for the run that already happened. Until it exists, no judge may cite "35 passed". Scope the intake footer to intake time, or note the later verification run in the status ledger so the two artifacts do not contradict each other. |
| minor (F3) | `CLAUDE.md`: update `status.md` after verified work; an amendment to a gated artifact must be traceable | `events/live-trial-2026/status.md` | The newest Activity log row is the configuration re-audit at `2026-09-16T23:41:20Z`, while `last_updated` is `2026-09-16T23:49:05Z`. Six material actions in between are unlogged: the roster freeze, the two intake narrative completions, the two image builds, the amendment of the gated Execution environment section, the advance to the intake stage, and the team-ledger sandbox run. The amendment matters most. It is disclosed inside `event.md` itself, so it is not hidden, but nothing records when it was made or which official authorized it, and that is the one control that makes a mid-event amendment to a gated artifact auditable rather than merely disclosed. | Add an Activity log row per action, and for the amendment name the time and the authorizing official. The Team progress table should also show intake as complete rather than only pinned, now that both narratives are written. |
| minor (F4) | `events/live-trial-2026/event.md`: "Every run record names the image actually used, so a deviation from this table is visible at the judgments audit" | `events/live-trial-2026/evidence/Containerfile.ledger`, `Containerfile.podcast`, and `atj/sandbox.py` | The claim is literally true but thinner than it reads. The execution record stores the image string it was handed and nothing more: `atj/sandbox.py` performs no digest resolution anywhere, even though its own module docstring says "limits, image digest, and runtime version go into the evidence record". Both approved images are mutable local tags, both Containerfiles start from the mutable `python:3.12-slim` tag, and the installs use open-ended ranges or no constraint at all, so rebuilding either tag produces a different image under the same name with no trace in any run record. A deviation to a *different* tag would be visible; a silent rebuild of the *same* tag would not. | Record the image IDs alongside the tags in the approved-images table — `5f523f17ce3a` for `localhost/atj-live-trial/ledger:1` and `1583b1a42534` for `localhost/atj-live-trial/podcast:1` — and have the evidence stage note the image ID in each run record. Do not rebuild either tag during the event; if a rebuild becomes necessary, treat it as a new tag. The `atj/sandbox.py` docstring overpromising a digest is a framework defect worth its own issue, outside this event's scope. |
| minor (F5) | `framework/policies/evidence-and-citation.md`: cite path and line or symbol | `events/live-trial-2026/submissions/team-podcast.md` | Line anchors drift by a few lines throughout, while the quoted content and symbol names are accurate. `tests/e2e.py:26` for the chromium constant is at line 28. `server/app.py:81-86` for the library route is at 84, and `server/app.py:141-199` for the byte-range media route starts at 135. The `.agentic` file is described as five lines and is six. Every citation I followed resolved to the right symbol, so nothing is unverifiable, but a judge quoting a line number from this record will cite the wrong line. The team-ledger record did not show this drift in the citations I checked. | Correct the line anchors, or drop bare line numbers in favor of symbol names where the symbol is unambiguous. |

## Advisories

**A8 — the chromium conditional in the team-podcast record is stale and must not
be read as a directive.** The record states that if no chromium binary exists at
`/usr/bin/chromium` in the sandbox, that should be recorded as
`execution_status: unavailable` for that path. I treated this as a stale
forward-looking statement rather than a defect, because it is correctly written
as a conditional and was true when written. Its condition is now false: I started
the approved team-podcast image with no network and no submission mounted, and
`which chromium` returns `/usr/bin/chromium`, Chromium 152.0.7977.82. The
evidence stage must record the actual outcome of running the script, and must not
carry the conditional forward as a finding of unavailability. This is the right
place to fix it — the evidence stage supersedes it with a run record — rather
than editing a narrative section that two independent agents produced.

**A9 — the approved team-ledger image has no `pdftotext`, so PDF ingest is `NE`
unless the image changes.** Verified by starting the image: `which pdftotext`
returns nothing. `events/live-trial-2026/evidence/Containerfile.ledger` installs
only `pyyaml`, `duckdb` and `pytest`, and the intake record correctly warns that
`src/fin/adapters/citi_pdf.py` shells out to `pdftotext`. CSV ingest and the rest
of the pipeline are unaffected. Judges must score PDF-adapter behavior `NE` with
the environment gap named, not as an application defect, unless the event adds
the `poppler` package to the image and records that as a further amendment.

**A10 — `tests/e2e.py` in the team-podcast submission is not a pytest suite.** It
is a standalone script that takes a base URL and needs a server already running;
pytest collects nothing from it. This is a fact the evidence stage must plan
around, not an intake defect, and the intake record describes the invocation
correctly. Any attempt to gather execution evidence for team-podcast has to start
the application first and then run the script against it, inside the same
sandbox, with the result captured in a run record.

**A2 — intake records are still `approval_state: draft`, `validation_state:
unvalidated`, and this is now actionable.** At the configuration audit this was
correct, because the narratives were empty. They are now complete and about to
become the frozen input to eight independent judgments. Set both to `approved`
and `valid` at the same time the `roster-frozen` gate is recorded, so that what
the judges read is not labelled a draft.

**A4 — both submissions contain agent-directed instruction files.** Unchanged,
and now corroborated from a second direction: both intake records independently
searched for injection and reported none, and each described the agent-facing
files as part of the submitted product. Judges must still open them as data, must
not let a submission-local agent configuration or commit hook take effect in
their own session, and must confine execution to the sandbox.

**A5 — preflight is a point-in-time result.** Re-run `atj sandbox preflight` at
the start of the evidence stage and record `execution_status: unavailable` with
`NE` on affected criteria if it changes.

**A6 — the run timeout can be raised from the command line** and the Execution
environment section does not say whether that is permitted. Note and justify any
run that uses a longer timeout than the module default.

**A7 — the operator's real name appears in `events/live-trial-2026/event.md`.**
Correct in a private artifact; it must not reach anything under
`events/live-trial-2026/public`. Run `atj validate publication` on anything that
would leave the panel.

## Completion gate

- [x] No blocking findings
- [x] No major findings — five minor findings, none of which holds the gate
- [x] Calculations valid — no official arithmetic exists at the intake stage. The
      one numeric reconciliation I performed, 31 test functions plus five
      parametrized cases equals the 35 collected tests reported, is consistency
      arithmetic and is labelled as such in F2, not treated as verification of
      the run
- [x] Evidence references resolve — I re-derived nine sampled claims from the two
      checkouts and all nine held; line-anchor drift in one record is recorded as
      F5, and the one claim I could not verify, the unrecorded sandbox run, is
      recorded as not performed in F2
- [x] Version and identity checks pass — both roster commits match their intake
      records; `framework_commit` and `rubric` are unchanged in both records;
      `atj validate reports` passes on all three artifacts
- [x] Privacy boundary passes — `events/live-trial-2026/public` holds only a keep
      file; every artifact inspected is `visibility: private`; neither intake
      record reproduces a secret, and both correctly recorded the environment
      variable names they were blocked from reading as undetermined rather than
      guessing. See A7.

Final result: **PASS WITH ADVISORIES**. The `roster-frozen` gate may be set. Close
F2 and F3 before the evidence stage begins, because the first depends on evidence
that does not yet exist and the second is what makes the amendment auditable.
Close F1 and F4 before any execution evidence is captured, so that the run records
describe the environment accurately. F5 is cosmetic and can be fixed whenever.
Carry A2, A4, A5, A6, A7, A8, A9 and A10 into the evidence stage.
