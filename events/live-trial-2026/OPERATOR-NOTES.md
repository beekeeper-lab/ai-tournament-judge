# Operator notes — live-trial-2026

Working notes for whoever runs the next stage. Not an official artifact: no
score, no finding, nothing here is evidence. `status.md` is the ledger.

## Where this stands

Stage `initial-judging`. team-ledger's panel is complete (4 of 4 judgments,
consolidated 76.3, all criteria aligned). team-podcast has none of its four yet.
The `judgments-audited` gate needs both teams' panels plus a passing audit.

## Running the four judges for team-podcast

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
2. **The schema needs a `model` block the template does not show.** Add it after
   the judges return, from each file's own front matter, or validation fails
   blocking on all four.
3. **Judges have no clock.** Their timestamps are invented. Replace
   `started_at`/`completed_at` with the real bounds of the run.

Then: stage under `workspaces/live-trial-2026/staging/team-podcast/`, promote all
four at once, `atj render judgment` on the directory, `atj validate reports`,
`atj score`, record the `judging:team-podcast` unit.

## Then

Audit the judging stage for both teams, gate `judgments-audited`, write both
consolidated panel reports with `panel-consolidator` into `summaries/`, gate
`consolidation-audited`, build the bracket (2 teams, `min_teams: 2`, different
affiliation groups, one matchup, no byes), judge that matchup in both
presentation orders, then dossiers, publication validation and the final audit.

## Framework defects this event has found

These belong in the final event report. None was repaired mid-event except where
noted, because the rubric, personas and policies are frozen once judging starts.

1. **Judge personas cannot write their own artifact** (above). Needs a new
   persona version with a staging-scoped `Write`.
2. **`schemas/judgment.schema.json` and `framework/templates/individual-judgment.md`
   disagree** about the `model` block. One of them is wrong.
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
