---
event_id: sample-mock-2026
current_stage: complete
last_updated: "2026-05-18T17:30:00Z"
blocked: false
blocked_reason: null
stage_gates:
  bracket-audited: passed
  configuration-audited: passed
  consolidation-audited: passed
  dossiers-approved: passed
  evidence-validated: passed
  final-audit-passed: passed
  judgments-audited: passed
  roster-frozen: passed
  tournament-audited: passed
gate_evidence:
  configuration-audited: audits/consolidation-panel.md
  roster-frozen: audits/consolidation-panel.md
  evidence-validated: audits/consolidation-panel.md
  judgments-audited: audits/consolidation-panel.md
  consolidation-audited: audits/consolidation-team-lumen-02.md
  bracket-audited: audits/bracket.md
  tournament-audited: audits/tournament.md
  dossiers-approved: audits/final-event.md
  final-audit-passed: audits/final-event.md
units:
- unit_id: evidence:team-lumen
  stage: evidence
  state: complete
  input_digest: fe1084534ecacef9
  outputs:
  - evidence/team-lumen/manifest.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: judging:team-lumen
  stage: initial-judging
  state: complete
  input_digest: 06d43f0bdb465217
  outputs:
  - judgments/team-lumen/judge-backend.md
  - judgments/team-lumen/judge-frontend-ux.md
  - judgments/team-lumen/judge-security-ops.md
  - judgments/team-lumen/judge-product-agentic.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: consolidation:team-lumen
  stage: consolidation
  state: complete
  input_digest: f1e22a013593857a
  outputs:
  - summaries/team-lumen.md
  audit_result: PASS WITH ADVISORIES
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: dossier:team-lumen
  stage: dossiers
  state: complete
  input_digest: 0054972513c31e44
  outputs:
  - dossiers/team-lumen.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: evidence:team-quill
  stage: evidence
  state: complete
  input_digest: 7d435963d0ee20e8
  outputs:
  - evidence/team-quill/manifest.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: judging:team-quill
  stage: initial-judging
  state: complete
  input_digest: 36a08d16b6dbb33f
  outputs:
  - judgments/team-quill/judge-backend.md
  - judgments/team-quill/judge-frontend-ux.md
  - judgments/team-quill/judge-security-ops.md
  - judgments/team-quill/judge-product-agentic.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: consolidation:team-quill
  stage: consolidation
  state: complete
  input_digest: cf2197c5c98e8394
  outputs:
  - summaries/team-quill.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: dossier:team-quill
  stage: dossiers
  state: complete
  input_digest: e41bf6a5f6854d54
  outputs:
  - dossiers/team-quill.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: evidence:team-harbor
  stage: evidence
  state: complete
  input_digest: 8a52c219d87885a9
  outputs:
  - evidence/team-harbor/manifest.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: judging:team-harbor
  stage: initial-judging
  state: complete
  input_digest: 1486d9d108d64e7f
  outputs:
  - judgments/team-harbor/judge-backend.md
  - judgments/team-harbor/judge-frontend-ux.md
  - judgments/team-harbor/judge-security-ops.md
  - judgments/team-harbor/judge-product-agentic.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: consolidation:team-harbor
  stage: consolidation
  state: complete
  input_digest: faf9097d66a51e3f
  outputs:
  - summaries/team-harbor.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: dossier:team-harbor
  stage: dossiers
  state: complete
  input_digest: 2e449c9dadc830d5
  outputs:
  - dossiers/team-harbor.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: evidence:team-verdant
  stage: evidence
  state: complete
  input_digest: 28f8b3538d250eeb
  outputs:
  - evidence/team-verdant/manifest.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: judging:team-verdant
  stage: initial-judging
  state: complete
  input_digest: c3eb5a7d18fa45ee
  outputs:
  - judgments/team-verdant/judge-backend.md
  - judgments/team-verdant/judge-frontend-ux.md
  - judgments/team-verdant/judge-security-ops.md
  - judgments/team-verdant/judge-product-agentic.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: consolidation:team-verdant
  stage: consolidation
  state: complete
  input_digest: ffc8a2959d4afea8
  outputs:
  - summaries/team-verdant.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: dossier:team-verdant
  stage: dossiers
  state: complete
  input_digest: 7e0ca6d0d51980d3
  outputs:
  - dossiers/team-verdant.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: bracket:draw
  stage: bracket
  state: complete
  input_digest: e62d5d119f909354
  outputs:
  - bracket.md
  - bracket.json
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: matchup:semifinal-1
  stage: tournament
  state: complete
  input_digest: 2494e263586474a1
  outputs:
  - matchups/semifinal-1.md
  - public/semifinal-1.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: matchup:semifinal-2
  stage: tournament
  state: complete
  input_digest: db8f752424cc6ff4
  outputs:
  - matchups/semifinal-2.md
  - public/semifinal-2.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: matchup:final
  stage: tournament
  state: complete
  input_digest: ed4cd6c5026ae58d
  outputs:
  - matchups/final.md
  - public/final.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: final:audit
  stage: final-audit
  state: complete
  input_digest: 0671b8d491c243e9
  outputs:
  - audits/final-event.md
  - public/event-summary.md
  audit_result: PASS WITH ADVISORIES
  completed_at: "2026-05-18T17:30:00Z"
---

# Event Status — Sample Mock Event 2026

Complete. This ledger is what `atj event status` reads to decide the next safe
action, and what recovery uses after an interruption.

## Stage gates

- [x] Configuration audited
- [x] Roster frozen
- [x] All eligible evidence packages validated
- [x] All initial judgments audited
- [x] All consolidated reports audited
- [x] Bracket frozen and audited
- [x] Tournament complete
- [x] All team dossiers approved
- [x] Final event audit passed
- [x] Event marked complete

## Team progress

| Team ID | Intake | Evidence | Four judgments | Consolidated | Audited | Dossier |
|---|---|---|---|---|---|---|
| team-lumen | done | done | done | done | PASS after adjudication | done |
| team-quill | done | done | done | done | PASS | done |
| team-harbor | done | done | done | done | PASS | done |
| team-verdant | done | done | done | done | PASS | done |

## Blockers and adjudications

| ID | Scope | Description | Owner | Status | Resolution artifact |
|---|---|---|---|---|---|
| adj:sample-mock-2026:team-lumen-security:01 | criterion | Unresolved `NE` on security blocked the official total | head judging official | resolved | adjudications/adj-sample-mock-2026-team-lumen-security-01.md |
| adj:sample-mock-2026:team-harbor-innovation:01 | criterion | Severe disagreement and a possible outlier on innovation | head judging official | resolved | adjudications/adj-sample-mock-2026-team-harbor-innovation-01.md |
| adj:sample-mock-2026:semifinal-2-close-call:01 | matchup | Combined margin inside the close-call band; no winner returned | head judging official | resolved | adjudications/adj-sample-mock-2026-semifinal-2-close-call-01.md |

## Activity log

| Timestamp | Action | Input identity | Output | Audit result |
|---|---|---|---|---|
| 2026-05-18T09:00:00Z | intake and evidence | four synthetic commits | evidence/*/manifest.md | PASS |
| 2026-05-18T09:00:00Z | initial judging | four evidence packages | judgments/**/*.md | PASS |
| 2026-05-18T09:00:00Z | consolidation (first pass) | team-lumen panel | summaries/team-lumen.md | **FAIL** |
| 2026-05-18T09:00:00Z | adjudication | team-lumen security NE | adjudications/*.md | resolved |
| 2026-05-18T09:00:00Z | consolidation (repaired) | team-lumen panel | summaries/team-lumen.md | PASS |
| 2026-05-18T09:00:00Z | bracket draw | seed `sample-mock-2026-draw` | bracket.md | PASS |
| 2026-05-18T09:00:00Z | tournament | three matchups, both orders | matchups/*.md | PASS WITH ADVISORIES |
| 2026-05-18T17:30:00Z | dossiers and publication | approved private records | dossiers/*.md, public/*.md | PASS |
| 2026-05-18T17:30:00Z | final event audit | complete record | audits/final-event.md | PASS WITH ADVISORIES |
