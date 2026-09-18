---
event_id: sample-mock-2026
roster_version: 1
frozen: true
rubric: submission-evaluation@1.1.0
framework_commit: uncommitted
started_at: "2026-05-18T09:00:00Z"
completed_at: "2026-05-18T17:30:00Z"
visibility: private
approval_state: approved
validation_state: valid
approved_by: head judging official
approved_at: "2026-05-18T17:30:00Z"
---

# Teams

Four synthetic teams. `team-lumen` and `team-harbor` deliberately share the
`north-academy` affiliation group, and `team-lumen` and `team-quill` are the
previous champion and runner-up, so the bracket has two separation constraints
to satisfy at once.

| Team ID | Display name | Affiliation group | Previous result | Submission status | Eligible | Repository | Commit |
|---|---|---|---|---|---|---|---|
| team-lumen | Lumen | north-academy | champion | received | yes | fixtures/team-lumen | 1d46525edc7a377a802930091df18ad921262657 |
| team-quill | Quill | south-institute | runner-up | received | yes | fixtures/team-quill | 1ff35a656b351b0529a7bc2d6b169aec650e1e71 |
| team-harbor | Harbor | north-academy | none | received | yes | fixtures/team-harbor | 213a8d470271071a81322e41614345b87f67dd0c |
| team-verdant | Verdant | east-college | none | received | yes | fixtures/team-verdant | 57435ce0f24aacf5d49e41d78225d67882eccf91 |

Commits are synthetic digests, not real Git objects.
