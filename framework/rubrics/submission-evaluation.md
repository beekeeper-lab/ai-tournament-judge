---
rubric_id: submission-evaluation
version: 1.0.0
scale_min: 0
scale_max: 5
total_weight: 100
---

# Submission Evaluation Rubric

All four judges use these criteria and weights.

| ID | Criterion | Weight | Central question |
|---|---|---:|---|
| functional | Functional correctness and completeness | 25 | Does the application accomplish its promised primary workflows? |
| product | Product value and usability | 15 | Does it solve a meaningful problem in an understandable, usable way? |
| agentic | Agentic and AI system design | 15 | Is AI appropriate, controlled, observable, and effective? |
| engineering | Engineering and maintainability | 15 | Is the implementation coherent, proportionate, and maintainable? |
| reliability | Reliability, testing, and observability | 10 | Can failures be prevented, detected, understood, and recovered from? |
| security | Security, privacy, and responsible AI | 10 | Are access, data, tools, model risks, and user safety handled responsibly? |
| innovation | Innovation and technical ambition | 10 | Does it demonstrate meaningful originality or technical depth? |

## Score anchors

| Score | Meaning |
|---:|---|
| 0 | Not demonstrated, unusable, or contradicted by evidence |
| 1 | Seriously deficient; major failures dominate |
| 2 | Partially successful; useful elements with important weaknesses |
| 3 | Solid for the event; primary expectations are met |
| 4 | Strong; clearly exceeds normal expectations with convincing evidence |
| 5 | Exceptional; unusually complete, effective, and well-supported |

`NE` means not enough evidence and is not a numeric zero. An official total cannot be finalized while a criterion is `NE`.

## Calculation

`criterion_points = score / 5 * criterion_weight`

The overall score is the sum of criterion points and ranges from 0 to 100. Use `scripts/calculate_scores.py`; reports may display at most one decimal place.

## Required criterion response

For each criterion provide the raw score, weighted points, evidence references, what worked, what was deficient, reasoning connecting evidence to score, confidence, and highest-value improvement. Separate observation from inference. A team claim is not proof without supporting behavior or artifacts.

## Interpretation boundaries

- Judge what was submitted at the pinned commit, not what the team might add later.
- Do not reward model names, framework choice, agent count, or code volume by themselves.
- Do not penalize an appropriate prototype merely for lacking unrelated production infrastructure.
- Confirmed inability to complete the primary advertised workflow must materially affect `functional` and any dependent criteria.
- Suspected rule violations or malicious behavior are flagged for human review; judges do not disqualify teams.
