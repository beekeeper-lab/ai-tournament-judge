---
event_id: EVENT-ID
roster_version: 1
frozen: false
rubric: submission-evaluation@1.0.0
framework_commit: FRAMEWORK-COMMIT
started_at: YYYY-MM-DDTHH:MM:SSZ
completed_at: YYYY-MM-DDTHH:MM:SSZ
visibility: private
approval_state: draft
validation_state: unvalidated
---

# Team Roster

| Team ID | Display name | Affiliation group | Previous result | Submission status | Eligible | Repository | Commit |
|---|---|---|---|---|---|---|---|
| team-example | Example Team | example-school | none | pending | yes | path/or/url | |

Use stable lowercase team IDs. `affiliation_group` is used only for bracket separation, never scoring.

`Repository` and `Commit` are filled in at intake. The commit must be an immutable hash, never a branch name: from the evidence stage onward `atj event validate` requires both.
