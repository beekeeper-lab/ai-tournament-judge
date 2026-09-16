---
name: build-team-dossier
description: Produces a constructive student-facing dossier from audited judging and tournament artifacts.
---

# Build Team Dossier

Read the report-publication policy and team-dossier template. Use only finalized artifacts for the selected team.

Include the consolidated result, important evidence-backed observations from individual judges, matchup history, demonstrated strengths, blocking issues, prioritized improvements, and suggested next steps. Explain score disagreement when useful to the team.

Exclude hidden chain-of-thought, other teams' private information, unverified allegations, exploit details that create unnecessary risk, and demeaning persona language. The grumpy persona may produce blunt internal analysis; the dossier must remain respectful and educational.

Run `python3 -m atj validate reports <event>` and `python3 -m atj validate publication <dossier> --event-dir <event>` before marking the dossier complete. The dossier is team-facing: it must not carry judge run ids, comparison values, panel blockers, or a credential.
