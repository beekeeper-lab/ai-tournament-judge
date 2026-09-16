---
name: run-judging-event
description: Orchestrates a restartable judging event by selecting the next permitted skill from the event status and audit gates.
---

# Run Judging Event

Read `events/<event>/event.md`, `teams.md`, and `status.md`. Confirm the current branch is not `main` before changing event artifacts.

Use event status as a state machine:

`configuration -> intake -> evidence -> initial-judging -> consolidation -> bracket -> tournament -> dossiers -> final-audit -> complete`

At each invocation, identify the next incomplete permitted unit of work. Call the narrow skill that owns it. Do not redo a completed audited unit unless the operator explicitly invalidates it. Do not skip failed audits. Record timestamps, artifact paths, rubric versions, source commits, and blockers in status.

Pause for human direction when authorization is missing, safety requirements cannot be met, a policy conflict exists, adjudication is required, or completing the next action would publish or externally mutate data.
