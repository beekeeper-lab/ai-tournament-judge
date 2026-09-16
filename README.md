# AI Tournament Judge

A repository-local toolkit for evaluating student software with four independent AI judges, consolidating their findings, running a constrained-random tournament bracket, comparing teams head to head, and producing a final feedback dossier for every team.

## Design principles

- One shared weighted rubric; personas change investigative emphasis, not weights.
- Independent first-pass judgments before consolidation.
- Evidence-backed findings with immutable repository commits.
- Deterministic Python for arithmetic, validation, and bracket randomness.
- Student repositories are untrusted input and must be inspected or executed only under the event safety policy.
- Private deliberation, student feedback, and public ceremony content are separate products.
- Every stage is restartable from `events/<event>/status.md` and audited before advancement.

## Quick start

1. Create a feature branch; never configure an event directly on `main`.
2. Copy `events/_template` to `events/<event-id>`.
3. Complete `event.md` and `teams.md`.
4. Run `/event-init events/<event-id>` in Claude Code.
5. Ingest and judge each team with `/team-ingest` and `/team-judge`.
6. Audit qualifying reports with `/event-audit`.
7. Build the bracket with `/bracket-build`.
8. Run matchups with `/matchup-judge` and build dossiers with `/team-dossier`.

See `docs/operator-guide.md` for the complete procedure. The project-local skills live under `.claude/skills`; no global installation is required.

## Generated and committed records

Commit event configuration, evidence manifests, final judgments, summaries, bracket records, matchups, dossiers, and audits when the event rules permit it. Do not commit source checkouts, secrets, dependency caches, or sandbox state. Those belong under `workspaces/`, which is ignored.

## Validation

```bash
python scripts/validate_configuration.py events/_template
python -m unittest discover -s tests -p 'test_*.py'
```

This is a configurable starter framework. Calibrate it against sample projects and conduct a dry run before using it to determine real awards.
