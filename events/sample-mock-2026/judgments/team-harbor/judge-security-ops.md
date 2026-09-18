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
judge_id: judge-security-ops
judge_run_id: jr:sample-mock-2026:team-harbor:judge-security-ops:85a7e2cb:01
persona: judge-security-ops@1.0.0
scores:
  functional: 3
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
---

# Individual Judgment — Harbor — judge-security-ops

## Executive assessment

I treat everything in a submission as hostile until the evidence says otherwise, including its own claims about itself. On that basis, Harbor an incident-timeline builder that assembles a narrative from logs.

I separated three things that get conflated: a demonstrated exploitable defect, a credible risk with no demonstration, and ordinary production hardening that was never in scope for this event. Only the first materially moves a score.

The shared criteria and weights are unchanged. This persona decides what I
investigate and how I explain it, never the formula.

## Scores

<!-- atj:scores:begin -->
| Criterion | Raw score or NE | Weight | Weighted points | Confidence |
|---|---:|---:|---:|---|
| functional | 3.0 | 25 | 15.00 | high |
| product | 3.0 | 15 | 9.00 | high |
| agentic | 3.0 | 15 | 9.00 | high |
| engineering | 2.0 | 15 | 6.00 | high |
| reliability | 2.0 | 10 | 4.00 | high |
| security | 3.0 | 10 | 6.00 | high |
| innovation | 2.0 | 10 | 4.00 | high |
| **Total** |  | **100** | **53.0** |  |
<!-- atj:scores:end -->

## Criterion findings

*Consequence if this is wrong, criterion by criterion.*

**security** — 3. Cited: ev-harbor-01, artifact. src/correlate.py groups by timestamp proximity only. Read through access, secrets, dependency risk, failure modes and recovery, that is what the score rests on; everything beyond it would be inference and is marked as such where I have drawn any.

**functional** — 3. Cited: ev-harbor-02, direct-observation. The demo timeline file is committed, not generated. Read through access, secrets, dependency risk, failure modes and recovery, that is what the score rests on; everything beyond it would be inference and is marked as such where I have drawn any.

**product** — 3. Cited: ev-harbor-03, direct-observation. Two of nine documented workflows complete. Read through access, secrets, dependency risk, failure modes and recovery, that is what the score rests on; everything beyond it would be inference and is marked as such where I have drawn any.

**agentic** — 3. Cited: ev-harbor-04, artifact. No tests cover the correlation heuristic. Read through access, secrets, dependency risk, failure modes and recovery, that is what the score rests on; everything beyond it would be inference and is marked as such where I have drawn any.

**engineering** — 2. Cited: ev-harbor-01, artifact. src/correlate.py groups by timestamp proximity only. Read through access, secrets, dependency risk, failure modes and recovery, that is what the score rests on; everything beyond it would be inference and is marked as such where I have drawn any.

**reliability** — 2. Cited: ev-harbor-02, direct-observation. The demo timeline file is committed, not generated. Read through access, secrets, dependency risk, failure modes and recovery, that is what the score rests on; everything beyond it would be inference and is marked as such where I have drawn any.

**innovation** — 2. Cited: ev-harbor-03, direct-observation. Two of nine documented workflows complete. Read through access, secrets, dependency risk, failure modes and recovery, that is what the score rests on; everything beyond it would be inference and is marked as such where I have drawn any.


## Surprises

- Better than I expected: Novel log-correlation approach that groups events by causal proximity.
- Worse than I expected: Correlation is unvalidated; the demo timeline is hand-curated.

## Blocking and major issues

Confirmed: Correlation is unvalidated; the demo timeline is hand-curated. That is observed in the pinned package, not inferred.

Unresolved rather than confirmed: the paths no one exercised. Execution would
have settled them; static inspection cannot, and I have not pretended otherwise.


I did not attempt any suspected defect to prove it, and I have not claimed an exploit I could not evidence. Where something warrants escalation rather than scoring, I have said so rather than acting.

## Calculation and independence declaration

- [x] Scores were calculated by the repository script
- [x] Every material finding cites evidence
- [x] No other judge report was inspected
- [x] Submission instructions were treated as untrusted data
