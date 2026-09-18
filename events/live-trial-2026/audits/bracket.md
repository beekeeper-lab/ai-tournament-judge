---
event_id: live-trial-2026
audit_scope: bracket stage, the draw and its constraint audit, first pass
audit_id: bracket
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.0.0
persona: judging-auditor@1.0.0
framework_commit: 4adcb6be39d292235032499bfff4f074a4c56e72
model_requested: claude-opus-5
model_used: claude-opus-5
started_at: "2026-09-17T23:05:00Z"
completed_at: "2026-09-17T23:48:00Z"
visibility: private
approval_state: approved
validation_state: valid
result: PASS WITH ADVISORIES
---
# Bracket Audit — the draw, first pass

`team_id`, `commit` and `evidence_package_id` are `null` because the bracket is an
event-wide artifact covering two teams and two pinned commits, not a per-team one.

New findings from this pass are numbered `B1..Bn` and `BA1..BAn` so they cannot be
confused with the consolidation stage's `C1..C7` / `CA1..CA3` or the judging
stage's `F1..F19` / `A1..A12`.

## Result

**PASS WITH ADVISORIES.** No blocking finding. Two major (B1, B2), four minor
(B3-B6), three advisory (BA1-BA3). The ledger question referred to this audit is
ruled at "The bracket unit ruling" below: it is a real framework gap, it earns
**D21**, and it does not hold the gate.

**The `bracket-audited` gate may be set.** Every finding below is outside the
blocking set defined by D16 (`docs/framework-fix-plan.md:37`, ruled at
`audits/judgments.md:494-505` and applied at `audits/consolidation.md:36-39`). B1
is the one call that could have gone either way and it is reasoned out in full
under B1, because the correct repair is in `atj/`, and the two repairs available
*inside the event* are both themselves blocking offences.

The six things this gate exists to protect were re-derived here, not accepted:

- **The draw reproduces byte for byte from its recorded seed.** A fresh
  `atj bracket build --event-dir events/live-trial-2026 --seed live-trial-2026`
  differs from the committed `bracket.json` on **one line**, `framework_commit`
  (B2). `rounds`, `constraint_audit`, `input_digest`, `bye_teams`,
  `unsatisfied_hard_constraints` and every scalar are identical.
- **Every hard constraint holds when re-derived from the roster by hand**, not
  read out of the file's own audit block.
- **No score reached any seeding, ordering or placement decision.** Proved two
  ways: by the code path, and by rebuilding the draw under five score
  permutations including the unofficial provisional 58.25. All five produce an
  identical `rounds` **and** an identical `constraint_audit`.
- **The roster is untouched since it was frozen.** `teams.md` has not been
  modified since `6321a18`, the freeze commit itself.
- **No judgment or consolidated report was touched.**
  `git log --stat 92c6687..HEAD -- events/live-trial-2026/judgments/` is **empty**.
- **Nothing is in public output.** `events/live-trial-2026/public/` holds one
  file, `.gitkeep`, one byte, and it is the only tracked path under it.

## Scope and artifacts inspected

| Artifact | Read as | Result |
|---|---|---|
| `events/live-trial-2026/bracket.json` | untrusted evidence, re-derived in full | reproduces; schema clean; B2 |
| `events/live-trial-2026/bracket.md` | untrusted evidence | never rendered; B3 |
| `events/live-trial-2026/teams.md` | roster v1, frozen | unchanged since `6321a18`; entrants match exactly |
| `events/live-trial-2026/event.md` | event configuration | `bye_policy: performance-qualified` at `:9`; B1 |
| `events/live-trial-2026/status.md` | ledger | B4, B5, B6; bracket unit ruling |
| `events/live-trial-2026/summaries/team-ledger.json` and `.md` | score source the bracket could read | `finalized: true`, `display_total: 76.3` |
| `events/live-trial-2026/summaries/team-podcast.json` and `.md` | score source the bracket could read | `finalized: false`, `display_total: null` — the safety property that matters |
| `framework/rubrics/bracket-assignment.md` | policy | front matter matches what the draw applied |
| `atj/bracket.py`, `atj/event.py`, `atj/versions.py`, `atj/cli.py` | the code that made the decisions | read to prove the score short-circuit |

## Deterministic validation results

| Command | Result |
|---|---|
| `python3 -m atj bracket build --event-dir events/live-trial-2026 --seed live-trial-2026` | rebuilt; diff against the committed file is one line, `framework_commit` |
| `python3 -m atj bracket verify events/live-trial-2026/bracket.json --event-dir events/live-trial-2026` | **PASS (constraints re-derived from the roster)** |
| `python3 -m atj bracket verify events/live-trial-2026/bracket.json --reproduce <roster.json>` | **PASS (reproduced from seed)** |
| `atj.schema.validate("bracket", ...)` | 0 problems |
| `python3 -m atj validate reports events/live-trial-2026` | PASS — 20 artifacts, 0 blocking, 0 major, 0 minor, 0 advisory |
| `python3 -m atj event status events/live-trial-2026` | stage `bracket`, gate `bracket-audited = pending`, 6 units complete, 0 stale |
| `python3 -m atj event unit events/live-trial-2026 list` | 6 unit(s), 0 stale |
| `python3 -m atj event validate events/live-trial-2026` | **FAIL, 1 problem** — see B1 |
| `python3 -m pytest tests/ -q` | 355 passed, 51 subtests passed |
| `python3 -m atj release-check` | PASS, all nine sections |

`atj validate publication` cannot be run against `bracket.json`: it returns
`missing YAML front matter`. That is BA2, not a finding against this event —
nothing from this bracket is approved for publication and `event.md:57` records
that no ceremony is held.

## Reproducibility — the check this audit exists for

The activity log at `status.md:169` claims the draw was rebuilt from the same
seed and was byte-identical. That claim was re-derived rather than accepted.

Rebuilt into a scratch file and diffed against the committed artifact:

```
53c53
<   "framework_commit": "uncommitted",
---
>   "framework_commit": "4adcb6be39d292235032499bfff4f074a4c56e72",
```

That is the entire difference. `framework_commit` is not seed-derived: it is read
from the working tree by `atj/versions.py:144-164`, which returns `uncommitted`
whenever `git status --porcelain` is non-empty, precisely so that an artifact
cannot claim provenance from a commit that does not contain the code that made
it. The tree was dirty when the bracket was drawn and is clean now, so the two
runs disagree on that field alone. The **draw** reproduces exactly. That is B2,
and it is provenance, not reproducibility.

`input_digest` was also re-derived independently of `atj bracket`, by
reconstructing the part list that `atj/bracket.py:901-913` hashes:

```
['live-trial-2026', 'performance-qualified',
 'team-ledger|south-campus|none|76.300000|',
 'team-podcast|north-campus|none||']
  -> 5bd7a2f7e711e721
```

which is the recorded value. Note the third element: the digest **is**
score-sensitive even though the draw is not. That is BA1.

## Constraint satisfaction, re-derived from the roster

Derived from `teams.md` alone, without reading `bracket.json`'s audit block:

| Hard constraint | Re-derived independently | File says |
|---|---|---|
| Every eligible team appears exactly once | 2 eligible teams; first-round entrants are `{team-ledger, team-podcast}`; 2 placed, 0 repeated, 0 omitted | satisfied |
| Bye count and match count match the bracket size | `bracket_size(2) = 1 << ceil(log2 2) = 2`; `bye_count = 2 - 2 = 0`; slots `= 2 // 2 = 1`; matches `= 1`; rounds `= log2 2 = 1` | satisfied |
| Bye policy applied consistently | 0 byes is the only consistent application of any policy when the team count is an exact power of two | satisfied |
| Previous champion and runner-up in opposite halves | both teams carry `Previous result = none`; no finalist exists to separate | not-applicable |
| No avoidable same-affiliation or previous-finalist first-round match | `north-campus` and `south-campus` are distinct, one team each; every possible pairing is conflict-free, so the pairing used is conflict-free and nothing was forced | satisfied |
| (soft) Affiliation separation maximized | no group holds two or more teams | not-applicable |

The round is correctly named `final` rather than `preliminary`:
`atj/bracket.py:137-145` names round 1 `preliminary` only when byes exist, and
`final` when the round has two participants. The match id
`mu:live-trial-2026:final:01` is what `atj/ids.py:128-133` produces for
`(live-trial-2026, final, 1)`. `policy: bracket-assignment@1.0.0` is what
`canon.load_bracket_policy()` resolves to. `roster_version: 1` matches
`teams.md`. `team_count: 2` is inside the policy's `min_teams: 2` /
`max_teams: 32` range.

## No score was used — the critical check

team-podcast has no official total and must never acquire one
(`audits/consolidation.md`, Carry into the bracket and matchup stages). The
declared bye policy, `performance-qualified`, is the one policy in
`framework/rubrics/bracket-assignment.md` that reads a total. It did not read one
here, and the short-circuit is genuine rather than incidental.

**By code path.** `atj/bracket.py:160-161`:

```python
    if count == 0:
        return [], shuffled
```

That return precedes every policy branch. The `performance-qualified` branch at
`:168-177`, which is the only place a `.score` is sorted on, is unreachable at
`count == 0`, as is the `ValidationError` at `:170-173` that would have refused
the draw for a missing score. The audit function short-circuits the same way:
`atj/bracket.py:596-597` returns `SATISFIED` on `if not bye_teams:` before its
own `performance-qualified` score comparison at `:595`. Nothing downstream of
`choose_byes` touches `.score` — `pair_play_in`, `arrange_units`, `_total_cost`
and the presentation-order coin flip at `:718-720` take affiliation, previous
result and the seeded RNG only.

**By experiment.** The draw was rebuilt five times with the score input mutated,
holding the seed, policy and roster fixed:

| Score input | `rounds` == committed | `constraint_audit` == committed | `input_digest` |
|---|---|---|---|
| as built (`team-ledger` 76.3, `team-podcast` none) | yes | yes | `5bd7a2f7e711e721` |
| both scores stripped from the roster entirely | yes | yes | `6bd74108c46c9275` |
| both scores present, `None` | yes | yes | `6bd74108c46c9275` |
| inverted: `team-podcast` 99, `team-ledger` 1 | yes | yes | `dc3f55fc98edddb6` |
| the unofficial provisional: `team-podcast` 58.25, `team-ledger` 76.3 | yes | yes | `4c416e414638cdc7` |

An inverted score ordering that leaves both the draw and the constraint audit
bit-identical is the strongest available evidence that no ordering decision read
a score. Only the digest moves, which is BA1.

**The provisional 58.25 was never reachable.** The bracket reads scores through
`atj/event.py:192-212`, which attaches a score only when the summary's front
matter has **both** `finalized` truthy and `display_total` non-null.
`summaries/team-podcast.md` front matter records `total: null`,
`display_total: null`, `finalized: false`, so no score is attached; the roster
dict the bracket received for team-podcast has no `score` key at all, which I
confirmed by loading the event and printing it. 58.25 lives only in
`summaries/team-podcast.json:provisional_total` and in prose, and nothing in
`atj/event.py` or `atj/bracket.py` reads `provisional_total` or the `.json` at
all. The consolidation stage's instruction — 58.25 is not a score, not a ranking
input and not a bye seed — held.

## Roster integrity

`git log --follow -- events/live-trial-2026/teams.md` returns four commits, the
newest `6321a18` ("roster frozen…"), whose only change to the file is
`frozen: false` → `frozen: true`. The roster has not been edited since the moment
it was frozen, and `roster_version` has stayed at `1` since the file was created
from the template. The bracket's entrants, `{team-ledger, team-podcast}`, are
exactly the set of rows with `Eligible = yes` and no withdrawal, and the
`affiliation_group` and `previous_result` values the draw used match the table
cell for cell.

## Ledger accuracy and the bracket unit ruling

**The refusal reproduces.** `atj event unit events/live-trial-2026 record --id
bracket:main --stage bracket --output bracket.json` exits with
`cannot derive an input digest for 'bracket:main'. Known units:
consolidation:team-ledger, consolidation:team-podcast, evidence:team-ledger,
evidence:team-podcast, judging:team-ledger, judging:team-podcast`
(`atj/cli.py:259`). It wrote nothing: the working tree is unchanged after the
attempt. `derive_digests` (`atj/event.py:586-620`) iterates
`event.eligible_teams` and emits only `evidence:`, `judging:` and
`consolidation:` keys, so there is no code path by which an event-wide unit can
exist.

**The ruling: worth a D-number, D21, Tier 3, not blocking.** The reasoning is
narrower than "the bracket is untracked", because the bracket is not untracked.
It carries its own `input_digest` produced by `roster_digest`
(`atj/bracket.py:901-913`), which is *stronger* than what the ledger would have
given it: the ledger's `unit_digest` hashes file contents, whereas
`roster_digest` hashes the semantic inputs — every team's id, affiliation,
previous result, score and band, plus the seed and the policy — and
`atj bracket verify --event-dir` re-derives it from the roster on demand. Both
exist and both were checked in this audit.

What is actually lost is one thing: `stale_units` (`atj/event.py:623-630`) and
therefore `can_advance`'s drift check (`atj/event.py:429-434`) are blind to the
bracket. A post-draw roster edit would silently leave a stale bracket, and
nothing in `atj event status` would say so. In **this** event the exposure is
near zero — `roster-frozen` is `passed`, `teams.md` is provably unmodified since
the freeze commit, and I re-derived that rather than trusting the gate. The
`status.md:95-97` intake precedent is the same shape and was accepted at the
intake gate, so accepting it again is consistent rather than a new concession.

The fix is not a new digest scheme. It is to make `derive_digests` emit
`bracket:main` from `bracket.json`'s own `input_digest` when the file exists, so
the ledger reuses the stronger digest that already exists instead of inventing a
weaker one.

**The activity-log row.** `status.md:169` was checked clause by clause against
`bracket.json`:

| Claim in the row | Verdict |
|---|---|
| seed `live-trial-2026` | true (`bracket.json:76`) |
| roster version 1 | true |
| input digest `5bd7a2f7e711e721` | true, and re-derived by hand above |
| single-elimination, 2 entrants, 1 final, 0 byes | true |
| "All five hard constraints satisfied" | **false as written** — four are `satisfied`, the fifth is `not-applicable`. B4 |
| affiliation separation not-applicable with one team per group | true |
| rebuilt from the same seed and byte-identical | true of the draw; `framework_commit` differs on a clean tree. B2 |
| `atj bracket verify` re-derived the constraints from the roster: PASS | true, reproduced |
| the policy never reads a total because two teams is an exact power of two and produces no byes | true, and the strongest claim in the row. Proved above two ways |

No output field of `bracket.json` is misdescribed by the row, and no claim in it
overstates what the tool did. One count is wrong (B4) and the ledger's
`last_updated` is older than the row (B5).

## Boundaries

`events/live-trial-2026/public/` contains exactly one file, `.gitkeep`, one byte,
and `git ls-files` shows it is the only tracked path under that directory. No
bracket fact, no team total, no host path and no seed has left the panel.

`git log --stat 92c6687..HEAD -- events/live-trial-2026/judgments/` produces **no
output**. No judgment was touched during consolidation or during the bracket
stage. `summaries/` changed at `bdf369d`, `1ece869` and `aa564f0`, all of which
are consolidation-stage commits already ruled on at `audits/consolidation.md`;
nothing in the bracket commit `4adcb6b` touches a summary.

## Findings

| Severity | Rule | Artifact | scope | blocking | Finding | Required repair |
|---|---|---|---|---|---|---|
| major (B1) | `CLAUDE.md`, Working rules — the applicable audit must complete before a stage advances; D16 scope ruling (`docs/framework-fix-plan.md:37`) | `atj/event.py:356-364`, surfacing against `events/live-trial-2026/teams.md` | **framework** | **false** | `atj event validate` returns **FAIL**: `roster: performance-qualified byes need a consolidated score for every eligible team; missing for ['team-podcast']`. The check fires on `bye_policy == performance-qualified` and `stage >= bracket` alone. It never asks whether a bye exists. With `team_count == bracket_size` the policy is structurally incapable of consuming a score — `atj/bracket.py:160-161` returns before the branch that would read one — so the validator demands an input the draw provably cannot use. The event artifacts are correct; the validator is over-broad. Reasoned as non-blocking below | Fix in `atj/`: gate the check on `bracket.bracket_size(len(eligible)) > len(eligible)`. Propose **D20**. Do **not** repair this inside the event |
| major (B2) | `atj/versions.py:144-149` — "an artifact must not claim provenance from a commit that does not contain the code that made it" | `events/live-trial-2026/bracket.json:53` | event | false | `framework_commit: "uncommitted"`. The bracket is the only official artifact in this event that cannot be tied to a framework state: both summaries carry `d11a97060965b1f68797ff42f6391ae08dede3c2`, `event.md` carries `152dd2c10547a1c15bb56c4b1a90764b28354c59`, and every prior audit carries a real commit. The value is honest — the tree was dirty at draw time — but a reader cannot establish which code produced the draw from the artifact alone. **The draw itself is unaffected and reproduces.** | Re-run `atj bracket build --event-dir events/live-trial-2026 --seed live-trial-2026 --output events/live-trial-2026/bracket.json` from the clean tree and commit the one-line change; the field is computed before the file is written, so it resolves to `4adcb6be3929…`, the commit that introduced the draw. Nothing else in the file changes |
| minor (B3) | `CLAUDE.md`, Source of truth — "There is exactly one editable copy of each"; `atj/event.py:46` lists `bracket.md` in `REQUIRED_FILES`; `atj/demo_writer.py:1417` renders it from `render.bracket_tables` | `events/live-trial-2026/bracket.md:1-11` | event | false | The file is the untouched template stub. It declares `status: not-built` and `random_seed: null` while `bracket.json` records a built bracket drawn from seed `live-trial-2026`, and its body still instructs the reader to build it from `framework/templates/bracket-report.md`. The event therefore holds a reviewed Markdown artifact that contradicts the authoritative JSON on two facts. No code reads its front matter and `STAGE_REQUIREMENTS["bracket"]` needs only `bracket.json`, so the gate is unaffected and `release-check`'s single-source check does not catch it | Render it from `render.bracket_tables(bracket.json)` as the demo generator does, and set `status`, `random_seed` and `bye_policy` from the JSON — or delete the two front-matter fields that duplicate the JSON and leave one pointer to it |
| minor (B4) | The activity log's own accuracy convention, established by evidence F11, judging F11 and consolidation C5 | `events/live-trial-2026/status.md:169` | event | false | "All five hard constraints satisfied." Four of the five hard entries in `constraint_audit` are `satisfied`; "Previous champion and runner-up in opposite halves" is `not-applicable`, because neither team has a previous result. The row already uses `not-applicable` correctly for the soft affiliation constraint one clause later, so this is a transcription slip and not a claim that an unmet constraint was met | "Four hard constraints satisfied, the previous-finalist constraint not-applicable" |
| minor (B5, consolidation C6 and judging F10 recurred) | `schemas/status.schema.json` requires `last_updated`; every `atj event` writer sets it from `versions.now()` | `events/live-trial-2026/status.md:4` | event | false | `last_updated: "2026-09-17T22:15:17Z"` predates the bracket activity row at `2026-09-17T22:50:00Z` by 35 minutes. Third occurrence of one mechanism: a row hand-added above a machine-written field. C6's stated repair — "the gate command must be the last write to the ledger" — was recorded and then not applied to this stage | Add this audit's row, then run `atj event gate`, then confirm `last_updated` exceeds the newest row. Mechanically self-closing if the gate command is genuinely last |
| minor (B6, consolidation C5 partly unrepaired) | The stage-gates checklist is the human-readable face of `stage_gates` in the same file's front matter | `events/live-trial-2026/status.md:80-81` vs `:11-12` | event | false | `- [ ] All initial judgments audited` and `- [ ] All consolidated reports audited` are both unticked while the front matter records `judgments-audited: passed` and `consolidation-audited: passed`. C5 asked for the judging box to be ticked; neither was, and the consolidation gate has since passed and added a second stale box. `atj event gate` writes front matter only, so the boxes are hand-maintained. No code reads them | Tick both boxes in the same commit that ticks `Bracket frozen and audited` |

## Advisories

**BA1 — the bracket's `input_digest` is score-sensitive although its draw is
not.** `roster_digest` (`atj/bracket.py:901-913`) includes each team's score in
the hashed part list, so `5bd7a2f7e711e721` is a function of team-ledger's
`display_total: 76.3`. Two consequences, neither a defect in this event. First,
the staleness key is the **rounded display** value, 76.3, not the official total
76.25, so a change confined to the second decimal would not move the digest.
Second, if team-podcast's `reliability` `NE` were ever re-adjudicated to a score
and its summary finalized, the digest would change and any staleness check built
on it would call the bracket stale — even though I have demonstrated above that
the draw is bit-identical under every score permutation, so a redraw would be a
guaranteed no-op. Framework scope. If D20 is taken up, the same change should
consider excluding `score` from the digest whenever `bracket_size == team_count`.

**BA2 — a bracket cannot be run through the publication gate.**
`atj validate publication events/live-trial-2026/bracket.json` returns
`missing YAML front matter`; the gate is built for Markdown artifacts with front
matter, and the bracket is JSON. `CLAUDE.md` requires
`atj validate publication` before anything leaves the panel, and
`atj ceremony` reads "the bracket's structural facts" directly
(`atj/cli.py:789-793`), so bracket facts can reach a public view through a path
the publication gate cannot inspect. Zero exposure here: `public_scores: false`,
`event.md:57` records that no ceremony is held, and `public/` is empty. Raise it
before any event that does hold a ceremony.

**BA3 — carry-forwards, and what changed.** A2 (run records embed host paths)
and A9 (`ev-podcast-12` cited but unlisted in the adjudication) are unchanged;
neither is touched by the bracket stage. A10 is still a no-op — `status.md.bak`
is matched by `.gitignore:27` and is untracked, so it is an ignored path under
D16 and not a finding. A5 does **not** recur here in its usual form, because
`bracket.json` carries no `approval_state` or `validation_state` at all; the
schema does not define them and `atj validate reports` passes 20 artifacts
without them. CA1 (the D12 citation resolving only on an unmerged branch) is
untouched by this stage. One new observation, not a finding: the bracket commit
`4adcb6b` is the first event commit whose artifact records
`framework_commit: uncommitted`, which is what B2 is, and it is worth checking
that field on the next artifact rather than discovering it at audit again.

## Proposed framework defects

**D20 — `atj/event.py:356-364` fails an event for a missing score the declared
bye policy cannot consume.** `validate_roster` requires a consolidated total for
every eligible team whenever `bye_policy == performance-qualified` and the stage
has reached `bracket`, without checking whether the draw produces any bye. When
the team count is an exact power of two, `bye_count` is zero and
`atj/bracket.py:160-161` returns before the score is ever read, so the validator
demands an input that provably cannot affect the result. The live consequence is
that this event is permanently `FAIL` under `atj event validate` with a correct
bracket, a correct roster and a correctly withheld total, and the only two
repairs available inside the event — fabricating a total for team-podcast, or
changing `event.md`'s `bye_policy` mid-event — are both themselves forbidden.
Gate the check on `bracket.bracket_size(len(eligible)) > len(eligible)`.
**Tier 1** — it produces a false FAIL on a correct event today.

**D21 — `atj event unit` has no representation for an event-wide unit, so the
bracket stage cannot be recorded in the ledger.** `derive_digests`
(`atj/event.py:586-620`) iterates `event.eligible_teams` and emits only
`evidence:`, `judging:` and `consolidation:` keys, so `record --id bracket:main`
is refused at `atj/cli.py:259`. The cost is not lost provenance — `bracket.json`
carries a stronger, semantic `input_digest` of its own — it is that `stale_units`
and `can_advance`'s drift check cannot see the bracket, so a post-draw roster
edit would leave a stale bracket with nothing to report it. Emit `bracket:main`
from `bracket.json`'s existing `input_digest` rather than inventing a second
digest. Same shape as the intake gap `status.md:95-97` already documents.
**Tier 3** — no incorrect output, and the roster it depends on is frozen and
verified unmodified.

## Why this passes

Measured against the D16 ruling as it was narrowed for this stage, a bracket-stage
finding blocks only if it is a team placed more than once or not at all, a bye
policy applied inconsistently, a constraint violated, a bracket that does not
reproduce from its recorded seed, an unauthorised use of a score, or private data
in public output.

- **A team placed more than once or not at all.** Two eligible teams, two placed,
  re-derived from `teams.md` without reading the file's audit block. None.
- **A bye policy applied inconsistently.** Zero byes is the only consistent
  application when the team count is a power of two, and the policy's score-reading
  branch is unreachable at that bye count. None.
- **A constraint violated.** All six constraints re-derived by hand above; four
  hard satisfied, one hard not-applicable on a fact I checked in the roster, one
  soft not-applicable. `unsatisfied_hard_constraints` is empty and
  `feasible: true`. None.
- **A bracket that does not reproduce.** It reproduces. The rebuild differs on one
  provenance field that is read from git rather than derived from the seed, and
  `atj bracket verify --reproduce` returns PASS (reproduced from seed). None.
- **An unauthorised use of a score.** The strongest check in this audit, and the
  clearest negative. Proved by code path and by five mutated rebuilds that leave
  the draw and the constraint audit bit-identical. The provisional 58.25 is not
  reachable by any code path the bracket uses. None.
- **Private data in public output.** `public/` holds `.gitkeep`, one byte. None.

**B1 is the one call that could have gone the other way, so here is the reasoning
in full.** A failing `atj event validate` is normally enough to hold a gate, and I
considered it under "a bye policy applied inconsistently". It does not fit. The
bye policy was applied consistently: it produced zero byes, which is the only
outcome a two-team roster permits, and `_check_bye_policy` returns `SATISFIED` on
the no-byes branch by design rather than by accident. The inconsistency is
entirely inside `atj/event.py`, which asks for a score without asking whether a
bye exists — a framework artifact, explicitly non-blocking under the scope rule.
The decisive consideration is what a blocking verdict would demand: the only two
repairs available inside `events/live-trial-2026/` are to give team-podcast a
total, which is the exact offence this stage's audit exists to prevent and which
`audits/consolidation.md` forbids by name, or to change `event.md`'s `bye_policy`
mid-event, which `CLAUDE.md` forbids for an active event after judging begins. A
rule whose only in-scope repairs are both blocking offences is not a rule that can
be satisfied, which is itself the evidence that the defect is in the framework and
not in the event. Recorded as D20, repaired in `atj/`, gate not held.

B2 is the closest thing to a provenance failure in this stage and it is ruled
non-blocking on a narrow ground: the missing fact is *which framework commit*, not
*whether the draw is reproducible*. The draw was reproduced during this audit from
the recorded seed against the frozen roster, at a `HEAD` where `pytest` reports 355
passed and `release-check` passes all nine sections, so the code that produced it
is known to be sound at the only commit that matters. The repair is one command and
one line.

## Completion gate

**PASS WITH ADVISORIES.** The `bracket-audited` gate **may be set**.

Recommended order. B5 is only self-closing if the gate command is the last write
to the ledger, so:

1. Fix B2 — re-run the build from the clean tree and commit the `framework_commit`
   line.
2. Fix B3 — render `bracket.md`, or strip its two duplicate front-matter fields.
3. Fix B4 and B6 — correct the constraint count in the `22:50:00Z` row, tick the
   judging and consolidation boxes, tick the bracket box.
4. Add this audit's activity-log row.
5. Then, and last:

```
python3 -m atj event gate events/live-trial-2026 bracket-audited passed \
  --audit audits/bracket.md
```

6. Confirm `last_updated` now exceeds the newest activity row (B5).

**Carry into the tournament stage.** The bracket holds one match,
`mu:live-trial-2026:final:01`, `team-ledger` against `team-podcast`, no bye and no
prior round. team-podcast still has no official total and must not acquire one
through the matchup: `framework/rubrics/head-to-head.md` compares criteria
directly and forbids selecting on initial totals, and the bracket has now
demonstrated that the pipeline can seat a team with no total without ever reading
one. `reliability`'s comparison value is the matchup panel's finding to make on
the common evidence, as `status.md:157` records — if it returns `0`, the effective
tie-break for this pairing falls to `functional` then `product`. The presentation
order inside the match is a seeded coin flip (`atj/bracket.py:718-720`) and
carries no signal; the matchup must still be judged in both orders.

**Carry into the framework backlog.** D20 (Tier 1) and D21 (Tier 3) above,
alongside D18 and D19. BA1 and BA2 are open advisories. A2, A5 and A9 remain
open from earlier stages.
