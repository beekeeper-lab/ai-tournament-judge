---
name: run-judging-event
description: Orchestrates a restartable judging event by selecting the next permitted skill from the event status and audit gates.
---

# Run Judging Event

Run `python3 -m atj event status <event>` first. It reads the ledger, re-derives what is real on disk, and names the narrowest next action. Confirm the current branch is not `main` before changing event artifacts.

Use event status as a state machine:

`configuration -> intake -> evidence -> initial-judging -> consolidation -> bracket -> tournament -> dossiers -> final-audit -> complete`

At each invocation, take the action `atj event status` reports and call the narrow skill that owns it. A unit recorded complete whose output is missing, or whose input digest changed, is surfaced as repair or rerun work rather than skipped. Do not redo a completed audited unit whose inputs are unchanged. Do not skip failed audits. Record timestamps, artifact paths, rubric versions, source commits, and blockers in status.

Advance stages only with `python3 -m atj event advance <event>`, which refuses while the stage gate is pending or failed. A human override requires `--force-reason` and is recorded in the ledger.

Pause for human direction when authorization is missing, safety requirements cannot be met, a policy conflict exists, adjudication is required, or completing the next action would publish or externally mutate data.
