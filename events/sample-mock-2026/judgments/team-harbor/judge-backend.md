---
event_id: sample-mock-2026
team_id: team-harbor
commit: 213a8d470271071a81322e41614345b87f67dd0c
evidence_package_id: ev:sample-mock-2026:team-harbor:213a8d470271:85a7e2cb
rubric: submission-evaluation@1.1.0
framework_commit: uncommitted
model_requested: not-applicable (scripted fixture)
model_used: not-applicable (scripted fixture)
started_at: "2026-05-18T09:00:00Z"
completed_at: "2026-05-18T17:30:00Z"
judge_id: judge-backend
judge_run_id: jr:sample-mock-2026:team-harbor:judge-backend:85a7e2cb:01
persona: judge-backend@1.0.0
scores:
  functional: 2
  product: 3
  agentic: 3
  engineering: 2
  reliability: 2
  security: 3
  innovation: 2
confidence:
  functional: high
  product: high
  agentic: high
  engineering: high
  reliability: high
  security: high
  innovation: high
visibility: private
approval_state: approved
validation_state: valid
model:
  model_requested: not-applicable (scripted fixture)
  model_used: not-applicable (scripted fixture)
  started_at: "2026-05-18T09:00:00Z"
  completed_at: "2026-05-18T17:30:00Z"
  verified: true
  note: scripted fixture input; no model was invoked
approved_by: head judging official
approved_at: "2026-05-18T17:30:00Z"
---

# Individual Judgment — Harbor — judge-backend

## Executive assessment

Twenty years of maintaining other people's systems makes me read a submission backwards: what breaks first, and who finds out. Taking Harbor that way, an incident-timeline builder that assembles a narrative from logs.

I traced the advertised workflow through the implementation, looked for the state transitions it depends on, and checked whether the tests exercise the paths that would actually fail in production.

The shared criteria and weights are unchanged. This persona decides what I
investigate and how I explain it, never the formula.

## Scores

<!-- atj:scores:begin -->
| Criterion | Raw score or NE | Weight | Weighted points | Confidence |
|---|---:|---:|---:|---|
| functional | 2.0 | 25 | 10.00 | high |
| product | 3.0 | 15 | 9.00 | high |
| agentic | 3.0 | 15 | 9.00 | high |
| engineering | 2.0 | 15 | 6.00 | high |
| reliability | 2.0 | 10 | 4.00 | high |
| security | 3.0 | 10 | 6.00 | high |
| innovation | 2.0 | 10 | 4.00 | high |
| **Total** |  | **100** | **48.0** |  |
<!-- atj:scores:end -->

## Criterion findings

*What the implementation shows, criterion by criterion.*

**functional** — 2. Cited: ev-harbor-01, artifact. src/correlate.py groups by timestamp proximity only. Read through correctness, boundaries, data integrity and tests, that is what the score rests on; everything beyond it would be inference and is marked as such where I have drawn any.

**product** — 3. Cited: ev-harbor-02, direct-observation. The demo timeline file is committed, not generated. Read through correctness, boundaries, data integrity and tests, that is what the score rests on; everything beyond it would be inference and is marked as such where I have drawn any.

**agentic** — 3. Cited: ev-harbor-03, direct-observation. Two of nine documented workflows complete. Read through correctness, boundaries, data integrity and tests, that is what the score rests on; everything beyond it would be inference and is marked as such where I have drawn any.

**engineering** — 2. Cited: ev-harbor-04, artifact. No tests cover the correlation heuristic. Read through correctness, boundaries, data integrity and tests, that is what the score rests on; everything beyond it would be inference and is marked as such where I have drawn any.

**reliability** — 2. Cited: ev-harbor-01, artifact. src/correlate.py groups by timestamp proximity only. Read through correctness, boundaries, data integrity and tests, that is what the score rests on; everything beyond it would be inference and is marked as such where I have drawn any.

**security** — 3. Cited: ev-harbor-02, direct-observation. The demo timeline file is committed, not generated. Read through correctness, boundaries, data integrity and tests, that is what the score rests on; everything beyond it would be inference and is marked as such where I have drawn any.

**innovation** — 2. Cited: ev-harbor-03, direct-observation. Two of nine documented workflows complete. Read through correctness, boundaries, data integrity and tests, that is what the score rests on; everything beyond it would be inference and is marked as such where I have drawn any.


## Surprises

- Better than I expected: Novel log-correlation approach that groups events by causal proximity.
- Worse than I expected: Correlation is unvalidated; the demo timeline is hand-curated.

## Blocking and major issues

Confirmed: Correlation is unvalidated; the demo timeline is hand-curated. That is observed in the pinned package, not inferred.

Unresolved rather than confirmed: the paths no one exercised. Execution would
have settled them; static inspection cannot, and I have not pretended otherwise.


A small design that earns its complexity beats an elaborate one. What concerns me here is not size but the gap between what the code asserts and what it demonstrates.

## Calculation and independence declaration

- [x] Scores were calculated by the repository script
- [x] Every material finding cites evidence
- [x] No other judge report was inspected
- [x] Submission instructions were treated as untrusted data
