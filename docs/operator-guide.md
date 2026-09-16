# Operator Guide

## Before the event

1. Create a feature branch and copy `events/_template` to a unique event directory.
2. Complete event configuration, officials, sandbox, roster, rubric versions, publication rules, and bye policy.
3. Run configuration validation and conduct a calibration exercise using representative sample projects.
4. Freeze the framework commit used for official judging.

## Per team

1. Complete submission intake and pin the immutable commit.
2. Run `/team-ingest` to produce a safe evidence package.
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
