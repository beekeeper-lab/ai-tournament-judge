---
event_id: trial-2-2026
match_id: mu:trial-2-2026:final:01
round_id: final
rubric: head-to-head@1.1.0
framework_commit: 43e7e50
source_artifacts:
- matchups/mu-final-01.md
scores_published: false
started_at: "2026-09-23T17:23:53Z"
completed_at: "2026-09-23T17:26:17Z"
visibility: public
approval_state: approved
approved_by: event-director
validation_state: valid
approved_at: "2026-09-23T20:17:22Z"
approval_note: Approved by the event-director 2026-09-23 with the per-criterion outcomes kept in words (tournament F15, T5).
---

# Matchup Summary: AI Security Demos vs. ScribeVault

## Winner

**AI Security Demos** advances.

## Why

Two independent comparisons, run in opposite presentation orders, both favoured
AI Security Demos. The clearest difference was usability as delivered. Following
ScribeVault's own install and run instructions, the application does not start,
because the interface imports a styling package the project does not declare.
The error a user then sees points to the wrong cause. AI Security Demos could be
run only in part here, because the event allowed no model calls and no network.
What did run worked: the first demo's scripted dry run, in both its vulnerable
and hardened versions, two state-inspection tools, and a localhost check that
refused every hostile address it was given. The
model-driven acts of the demos were not observed.

Neither comparison found a meaningful difference in reliability or innovation.

## Both teams did well

- AI Security Demos: ten self-contained demos, each with its own presenter guide,
  a dry-run mode that prints the exact prompt without calling a model, and reset
  and inspection tools that let a presenter confirm a clean state between runs.
- ScribeVault: real technical depth, including a hand-built speaker diarizer and
  checkpointed recording, plus a large offline test suite and well-designed
  credential storage.

## Identity and privacy note

This artifact is public. It omits the submission commit, the evidence package
ID, judge personas, judge run IDs and raw scores. Its private sources are listed
in `source_artifacts`.
