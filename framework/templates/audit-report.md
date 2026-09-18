---
event_id: EVENT-ID
audit_scope: SCOPE
audit_id: AUDIT-ID
team_id: null
match_id: null
commit: IMMUTABLE-COMMIT
evidence_package_id: EVIDENCE-ID
rubric: submission-evaluation@1.1.0
persona: judging-auditor@VERSION
framework_commit: FRAMEWORK-COMMIT
model_requested: MODEL-REQUESTED
model_used: MODEL-USED
started_at: YYYY-MM-DDTHH:MM:SSZ
completed_at: YYYY-MM-DDTHH:MM:SSZ
visibility: private
approval_state: draft
validation_state: unvalidated
result: FAIL
findings: []
---

# Judging Audit

## Result

**FAIL** until all blocking findings are resolved.

## Scope and artifacts inspected

## Deterministic validation results

## Findings

| Severity | Rule | Artifact | Scope | Blocking | Finding | Required repair |
|---|---|---|---|---|---|---|

Record the same findings in the `findings:` front matter, one entry each:

```yaml
findings:
  - id: F1
    severity: major
    scope: event          # `event` or `framework`
    blocking: true        # does this hold the stage gate?
    summary: one line
    artifact: judgments/team-x/judge-backend.md
    repair: what must change
    state: open           # open | repaired | accepted | deferred
```

**`scope` and `blocking` decide the gate; `result` does not.** A finding is
`scope: event` when it is against this event's own artifacts, and `framework`
when it is against the framework, the tooling, the documentation, or any path
outside `events/<event>/`. Set `blocking: true` only for a finding that must
hold this stage: missing evidence, arithmetic that does not reproduce, a version
mismatch, severe disagreement, unsafe execution, private data in public output,
an unauthorised score move, or an edited judgment.

Do **not** set `blocking: true` for a finding against a framework document, an
uncommitted or ignored path, activity-log prose where the underlying history is
correct, or a field no code reads. Record it, scope it `framework`, and let the
gate open. A verdict of FAIL can be true and still not be about the stage being
gated — `atj event gate` will open the gate and write why into the ledger.

Leaving `findings:` out entirely keeps the old behaviour: the verdict alone
decides, and a FAIL holds the gate.

## Advisories

## Completion gate

- [ ] No blocking findings
- [ ] No major findings
- [ ] Calculations valid
- [ ] Evidence references resolve
- [ ] Version and identity checks pass
- [ ] Privacy boundary passes
- [ ] Every finding recorded in `findings:` with a `scope` and a `blocking` flag
- [ ] Approved with `atj event approve <this file>`

Final result must be PASS, PASS WITH ADVISORIES, or FAIL.

This artifact ships `approval_state: draft`, and `atj event gate` refuses a draft
as authorization. That is deliberate — a freshly written audit has not been
reviewed. Move it with `atj event approve <this file>`, which validates the
artifact first and records the approving official; do not hand-edit the field.
