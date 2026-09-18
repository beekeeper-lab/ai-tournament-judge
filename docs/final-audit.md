---
document: final-audit
framework_version: 0.2.0-beta
audit_rounds: 4
last_round: 2026-09-16
visibility: private
result: PASS WITH ADVISORIES
---

# Final Audit

Four independent audits were run against this release: a baseline audit of
v0.1.0-alpha, two audits of the canonical data model and tooling, and two full
release audits. Each was given the repository and the requirements, never the
expected conclusion. Every round found real defects. This records what they found,
what was repaired, and what remains.

Full reproductions for the baseline round are in `docs/release-readiness-audit.md`.

## Round results

| Round | Scope | Result | Findings |
|---|---|---|---|
| 0 | Baseline of v0.1.0-alpha | FAIL | 17 defects, 12 release blockers |
| 1 | Canonical data model and versioning | FAIL | 3 blocking, 6 major, 10 minor |
| 2 | Data model and deterministic tooling | FAIL | 1 blocking, 8 major, 11 minor |
| 3 | Full release | FAIL | 5 blocking, 6 major, 8 minor |
| 4 | Full release, re-verification | FAIL | 3 blocking, 8 major, 12 minor |
| 5 | This record | PASS WITH ADVISORIES | see below |

Every finding from rounds 0–4 is closed, each with a named regression test in
`tests/test_audit_regressions.py`, `tests/test_final_audit_regressions.py` or
`tests/test_release_audit_regressions.py`. Those three files exist because every
one of those defects had already passed the suite of its day.

## What the audits kept finding

Three patterns recurred, and they are the honest summary of this release's risk:

**A generated number is not the number that ships.** `atj score` was always
deterministic. Twice, that turned out to be beside the point: the total an agent
*wrote into Markdown* was never compared back to the judgments, and an
adjudication's decided score had no code path at all. Determinism upstream of a
transcription step guarantees nothing.

**A control that reports is not a control that blocks.** Staleness was computed
and displayed while `event advance` proceeded anyway. `bracket verify` printed a
note and exited zero. A gate required an audit artifact but accepted one from a
different event and a different stage. Each of these looked implemented.

**A gate matches what you thought of.** The score gate caught `73.3/100` and
missed "finished on 73.3 out of 100". The foreign-team gate matched `team-quill`
and missed "Quill". Both published an official total with every check reporting
CLEAR. The repair added pattern coverage *and* a check against the event's own
known totals, because the pattern list will always be incomplete.

## Blocking and major findings, and their repairs

| Finding | Repair |
|---|---|
| A clean checkout failed its own validation block: Git tracks no empty directory | The generator writes a keepfile into every event subdirectory; a test asserts each is tracked |
| A summary's official total was never compared to its judgments | Validation reloads the judgments, reapplies approved adjudications, re-runs consolidation, and fails on any mismatch |
| No code path applied an adjudication's `score_override` | Adjudications are a first-class scoring input, applied automatically inside an event |
| One adjudication file could move any team's total | A resolution must be approved, resolved, criterion-scoped, matched to that team, carry no match id, and schema- and version-validate; duplicates are a conflict |
| Team dossiers rendered into `public/`, and only `.md` was scanned | Dossiers render to the team-facing directory; HTML in both tiers is gated |
| The team-facing gate had no score, PII or other-team check | Another team's total blocks, its findings are major, personal data blocks, and display names are matched as well as ids |
| `scores_published: true` overrode the event official | It is a claim, not an authorization, in both the validator and the renderer |
| Winner advancement did not exist | `atj bracket advance`, refusing an unresolved matchup, an undecided source match, or a report that disagrees with the bracket |
| The winner was parsed out of prose | Read from a structured `advances_team` field, validated against the entrants |
| Stage gates were self-certified booleans | Passing requires an audit for this event and this stage, plus the stage's actual work |
| `--force-reason ""` advanced a stage silently | An override needs a real reason and a named approver, and records what it bypassed |
| Staleness never blocked advancement | `can_advance` blocks on any stale unit |
| Judge independence was asserted and never observed | Reports stage outside `events/` until the panel completes; near-duplicate wording is flagged |
| The wheel shipped no framework data, built from a committed stale tree | Data is staged and shipped, `build/` is untracked and cleared, CI installs and runs the wheel |
| `atj event init` from a wheel wrote into site-packages | The event destination is the working directory, and writing inside a package is refused |
| A YAML alias bomb took 69 seconds | Anchors and aliases are refused outright |
| The status ledger was written non-atomically | Temp file, backup, atomic replace |
| The close-call band could be narrowed | The rubric's band is a floor; an event may widen it, never narrow it |

## Verified in this round

```
python3 -m pytest tests/ -q                     319 passed, 51 subtests
python3 -m atj release-check                    PASS
python3 -m atj demo check                       PASS
python3 -m atj event validate <sample>          PASS, 0 problems
python3 -m atj validate reports <sample>        PASS WITH ADVISORIES, 53 artifacts
python3 -m atj bracket verify --reproduce       PASS (reproduced from seed)
python3 -m atj bracket verify --event-dir       PASS (constraints re-derived)
python3 -m atj event unit <sample> list         21 units, 0 stale
python3 tools/check_placeholders.py             PASS
clean export of HEAD                            full block passes
built wheel, fresh venv, run from /tmp          release-check PASS
```

Attacks replayed and blocked: a tampered official total; a judgment edited after
consolidation; a forged adjudication for another team; an unscoped adjudication;
duplicate resolutions; an official total published in prose; another team's score
and findings in a dossier; personal data in any artifact; an artifact
self-authorizing score publication; a private report placed in `public/`; a
credential in rendered HTML; advancing a loser named by prose; advancing a later
round first; a matchup report disagreeing with the bracket; a tampered bye
assignment; a stage gate with an audit from another event; an empty
`--force-reason`; a YAML anchor bomb; a `!!python/object/apply` tag; markup
injection into the ceremony page.

The agent layer was exercised against a live Opus 5 panel; see
`docs/agent-verification.md`. All four judges refused all thirteen injection
attempts in the fixture and produced four different score vectors from identical
evidence.

## Result

**PASS WITH ADVISORIES**, for a supervised mock event. Not for a real
award-deciding event until the advisories below are closed and the framework has
been calibrated against sample projects with the event's own officials.

## Advisories

These are open, and stated rather than closed:

1. **The independence detector is a similarity heuristic.** Six-word shingles at
   80% overlap. Verbatim copying is caught; systematic paraphrase is not.
   Identical score vectors across judges are not examined.
2. **`bracket verify` without a roster checks structure only.** It says so, and
   exits 0. `--event-dir` or `--reproduce` re-derives the constraints. An
   operator who reads the label will not be misled; one who reads only the exit
   code could be.
3. **The score gate is pattern-based plus a known-totals check.** A total
   expressed in a form neither covers, for an event with no finalized summaries
   to compare against, could pass.
4. **Execution has never run against a live container runtime.** Podman is absent
   and the Docker daemon does not respond on the release host. The sandbox
   builder and its refusal path are unit-tested; the successful path is not
   exercised end to end.
5. **A network allowlist needs an egress proxy this repository does not provide.**
   Configuring one without a proxy is refused, which is correct and means the
   allowlist path is untested end to end.
6. **Several controls end in a human and cannot be verified further.** The
   framework refuses to pass a gate without a matching audit, to advance a winner
   without a confirmed result or a recorded decision, or to publish without a
   named approver. It cannot check that the audit was thorough, that the approver
   read what they approved, or that an override was justified. No command
   currently summarises `status.overrides` for review.
7. **The sample event's judge scores are scripted.** That is deliberate, so the
   pipeline is reproducible in CI without a model call, and every artifact says
   so. The fixture demonstrates the pipeline, not model behaviour.
8. **AI judgment is not deterministic.** Nothing here claims otherwise.
9. **`sandbox preflight` does not warn on a rootful runtime.** A container escape
   under rootful Docker is host root. It reports the mode; it does not judge it.
10. **Hooks are guard rails, not a security boundary**, and Claude Code ignores
    `permissions.allow` from project settings until the workspace is trusted.

## What a human must do before this decides anything real

- Run a full dry event against sample projects and review every artifact.
- Confirm each stage audit was performed, not merely recorded.
- Review every `foreign-team` advisory in every dossier.
- Read every artifact approved for publication before approving it.
- Provide a container runtime, or accept that executable evidence is unavailable
  and that affected criteria will be `NE`.
- Decide whether the independence controls are sufficient for the stakes.
