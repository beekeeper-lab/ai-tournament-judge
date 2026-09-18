---
event_id: sample-mock-2026
policy: bracket-assignment@1.0.0
rubric: submission-evaluation@1.1.0
persona: judging-auditor@1.1.0
framework_commit: uncommitted
roster_version: 1
team_count: 4
bracket_size: 4
bye_count: 0
bye_policy: performance-qualified
random_seed: sample-mock-2026-draw
input_digest: a4e6804ddfc43d34
feasible: true
model_requested: not-applicable
model_used: not-applicable
started_at: "2026-05-18T09:00:00Z"
completed_at: "2026-05-18T17:30:00Z"
visibility: private
approval_state: approved
validation_state: valid
approved_by: head judging official
approved_at: "2026-05-18T17:30:00Z"
---

# Bracket Report — Sample Mock Event 2026

Assignment is a reproducible constraint process, not another judgment of team
quality. Four teams, four slots, no byes.

## Frozen inputs

| Team | Consolidated score | Affiliation group | Previous result |
|---|---:|---|---|
| team-lumen | 73.3 | north-academy | champion |
| team-quill | 72.3 | south-institute | runner-up |
| team-harbor | 53.3 | north-academy | none |
| team-verdant | 59.8 | east-college | none |

## Assignment result

<!-- atj:bracket:begin -->
| Slot | Entrant A | Entrant B | Entry | Notes |
|---:|---|---|---|---|
| 1 | team-harbor | team-quill | semifinal | |
| 2 | team-verdant | team-lumen | semifinal | |

| Constraint | Kind | Status | Detail |
|---|---|---|---|
| Every eligible team appears exactly once | hard | satisfied | 4 of 4 teams placed |
| Bye count and match count match the bracket size | hard | satisfied | 0 byes, 2 first-round matches, 2 first-round slots |
| Bye policy 'performance-qualified' applied consistently | hard | satisfied | no byes: the team count is an exact power of two |
| Previous champion and runner-up in opposite halves | hard | satisfied | team-lumen in slot 1, team-quill in slot 0; earliest meeting is round 2 of 2 |
| No avoidable same-affiliation or previous-finalist first-round match | hard | satisfied | a conflict-free play-in pairing was available and used |
| Affiliation separation maximized | soft | maximized | north-academy (2 teams): earliest meeting round 2 |

Reproduce with: `python3 -m atj bracket build --event-dir <event-dir> --seed sample-mock-2026-draw` (roster version 1, input digest `a4e6804ddfc43d34`).
<!-- atj:bracket:end -->

## Why this draw was forced

Two hard constraints act at once on a four-team bracket. `team-lumen` and
`team-harbor` share `north-academy`, so they cannot meet in the first round.
`team-lumen` and `team-quill` are the previous champion and runner-up, so they
cannot share a half. With two first-round matches only one arrangement satisfies
both, and the seed selects presentation order within it rather than the pairing.

## Reproduction

```
python3 -m atj bracket build --event-dir events/sample-mock-2026 --seed sample-mock-2026-draw \
  --output events/sample-mock-2026/bracket.json
python3 -m atj bracket verify events/sample-mock-2026/bracket.json --event-dir events/sample-mock-2026
```

- [x] Every eligible team appears once
- [x] Bye count is correct
- [x] Previous finalists are separated when feasible
- [x] Affiliation separation is maximized
- [x] Exceptions are documented (none required)
