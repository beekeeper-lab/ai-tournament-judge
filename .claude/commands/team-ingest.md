---
description: Safely ingest one team and prepare its evidence package.
argument-hint: <event-directory> <team-id> <source>
---

Use the `prepare-submission` skill for `$ARGUMENTS`. Materialize and pin the submission with `python3 -m atj intake`, complete the intake record it writes, apply the execution-safety policy, generate the evidence manifest, validate it, and update status. Stop on missing authorization or unsafe execution requirements.
