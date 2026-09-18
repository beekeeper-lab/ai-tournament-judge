# Operator notes — live-trial-2026

Working notes for whoever runs the next stage. Not an official artifact: no
score, no finding, nothing here is evidence. `status.md` is the ledger.

## Where this stands

**The event is complete.** All nine stage gates passed. team-ledger finished at
76.3 and won the final by a confirmed combined margin of +35.00. team-podcast
finished with **no official total**: `reliability` was `NE` from all four judges,
adjudicated and accepted, for reasons the record states are the framework's and
the operator's rather than the team's.

Both dossiers are approved and publication-clear. The sections below are kept as
the historical record of how the judging stage was run; they are no longer
instructions.

## How the four judges were run for team-podcast

Same shape as team-ledger. Spawn the four persona agents in one message so they
run concurrently and cannot see each other. Give each one this brief, changing
only the judge id:

- Team: `team-podcast`, commit `f3fdd342465fa6bc2a52d226a8613b082ad329e0`
- `judge_run_id: jr:live-trial-2026:team-podcast:<judge-id>:d06f90cc:01`
- `evidence_package_id: ev:live-trial-2026:team-podcast:f3fdd342465f:d06f90cc`
- `framework_commit`: current HEAD at the time they run
- Reads: the rubric, `framework/policies/evidence-and-citation.md`, the template,
  `evidence/team-podcast/manifest.md`, `submissions/team-podcast.md`, the
  `runs/team-podcast-*.json` records their criteria depend on, and the checkout
  at `workspaces/live-trial-2026/team-podcast/`.
- Forbidden: anything under `judgments/` or `workspaces/.../staging/`, and the
  other team's material.

**`reliability` is already marked evidence-limited for this team.** The evidence
audit established that three executions of the end-to-end suite produced three
different outcomes and none was classified. Tell the judges that, and tell them
they may still score it if they can defend a score from the package — but that
`NE` is the expected answer and is not a penalty against the submission.

Three gotchas that cost time on team-ledger:

1. **The judge personas cannot write.** `.claude/agents/judge-*.md` declares
   `tools: Read, Grep, Glob`. Every judge will return its document as text and
   you persist it. That is sanctioned by `judge-submission` step 4. Ask for the
   whole file in one fenced block and tell them to leave the `atj:scores` block
   empty and omit any duplicate `scores:` yaml from the body.
2. **The `model` block.** This cost team-ledger a repair round. Closed in
   `25624c7`: the template now shows it, so the judges should return it. Check
   one file before promoting all four rather than assuming either way.
3. **Judges have no clock.** Their timestamps are invented. Replace
   `started_at`/`completed_at` with the real bounds of the run.

Then: stage under `workspaces/live-trial-2026/staging/team-podcast/`, promote all
four at once, `atj render judgment` on the directory, `atj validate reports`,
`atj score`, record the `judging:team-podcast` unit.

## What came next, for the record

Audit the judging stage for both teams, gate `judgments-audited`, write both
consolidated panel reports with `panel-consolidator` into `summaries/`, gate
`consolidation-audited`, build the bracket (2 teams, `min_teams: 2`, different
affiliation groups, one matchup, no byes), judge that matchup in both
presentation orders, then dossiers, publication validation and the final audit.

## Framework defects this event has found

Tracked as D1-D26 in `docs/framework-fix-plan.md`, which is the source of truth
for what is scheduled and why. This list is the narrative record. A defect is
repaired mid-event only when the repair cannot touch the rubric, the personas or
the policies, which are frozen once judging starts.

1. **Judge personas cannot write their own artifact** (above). Needs a new
   persona version with a staging-scoped `Write`.
2. **`schemas/judgment.schema.json` and `framework/templates/individual-judgment.md`
   disagree** about the `model` block. D2, closed in `25624c7`: the template now
   shows it, and `release-check` compares every template's front matter against
   its schema's required list, which found two further instances at once.
3. **`atj render judgment` did not exist** though the template cited it by name.
   Added in `3a798ad` — it adds no arithmetic and reproduces the committed sample
   byte for byte. Guarded against rewriting approved judgments in `4ac09ba`.
4. **`atj validate reports` cannot catch a wrong citation.** It checks that an
   evidence id resolves, not that the target contains the claim. Three audit
   rounds found nine misdirected citations, a scan credited to the wrong
   observation, and a fabricated version number — all while `validate reports`
   returned 0 findings at every stage. This is the most useful result the trial
   has produced.
5. **`atj/event.py:745` writes `status.md.bak` on every ledger update.** It got
   committed twice before `*.bak` was gitignored.
6. **A project hook false-positives on document text.** `.claude/hooks/pre-advance.sh`
   blocked a `git commit` whose message body merely *named* a submission's test
   file. The guard is right to be blunt, but it inspects the whole command
   string, so writing prose about a submission can look like running one.
   D6, closed in `25624c7`: heredoc bodies are stripped and a runner must sit
   adjacent to the submission path. 12 cases pin both directions.

## Outcome

Twenty-six framework defects, every one found by running the event rather than by
reading the code. The four that matter most for the next tournament: **D4**, that
`atj validate reports` checks a citation resolves but not that its target supports the
claim; **D16**, that the stage gate has no scope filter, which cost the judging stage
three audit passes until the scope rule was given to the auditor up front and every
later stage then passed first time; **D20**, a validation rule with no permitted
in-event repair; and **D25/D26**, that nothing in `atj` can set `approval_state` and
that audit reports — the artifact kind authorizing every gate — have no schema.
