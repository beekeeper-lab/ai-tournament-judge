# Operator Guide

## Before the event

1. Create a feature branch and copy `events/_template` to a unique event directory.
2. Complete event configuration, officials, sandbox, roster, rubric versions, publication rules, and bye policy.
3. Run configuration validation and conduct a calibration exercise using representative sample projects.
4. Freeze the framework commit used for official judging.

## Per team

1. Run `atj intake <event> <team-id> <source>` to materialize the submission,
   pin its commit, and enroll it. The source may be a git URL, a local
   repository, a directory or a `.zip`. Checkouts land under
   `workspaces/<event>/<team-id>/` and are never committed. An archive has no
   commit, so intake pins a reproducible snapshot of what was delivered and says
   so in the record; a git source is pinned to its own history, and `--ref`
   selects the commit when HEAD is not the submission.
2. Complete the narrative sections of `submissions/<team-id>.md` from the team's
   own account, then run `/team-ingest` to produce a safe evidence package.
3. Review evidence gaps before judging.
4. Run `/team-judge` for the independent panel, consolidation, and audit.
5. Resolve required adjudication and freeze the team result.

## Tournament

1. Freeze eligibility and run `/bracket-build` once.
2. Review the recorded seed, byes, separation constraints, and exceptions.
3. Run `/matchup-judge` for each match only when both entrants are final.
4. Approve the public summary before display and advance only audited winners.

## Closeout

Generate every team dossier, run the final event audit, approve public artifacts, tag the repository commit, and preserve the event record according to the organization's retention rules.
