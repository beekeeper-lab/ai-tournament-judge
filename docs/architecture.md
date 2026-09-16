# Architecture

The framework separates judgment from mechanics.

1. **Event records** define teams, versions, status, and approvals.
2. **Evidence preparation** pins each submission and creates a safe, shared evidence package.
3. **Four independent judges** apply one rubric through different professional lenses.
4. **The panel consolidator** performs neutral synthesis while Python calculates official scores.
5. **The bracket engine** applies declared constraints and recorded randomness.
6. **The matchup judge** compares two evidence records twice in reversed order.
7. **The dossier builder** converts private records into constructive team feedback.
8. **The auditor** gates every transition.

Markdown is the reviewable source of truth. JSON schemas and Python scripts provide deterministic validation. Source checkouts remain outside committed event records under `workspaces/`.

## Trust boundaries

Submission content is untrusted. Judge and skill instructions are trusted only from this repository at the event's pinned framework commit. Private reports may flow into consolidation and dossiers; they may not flow into other initial judges or public output.
