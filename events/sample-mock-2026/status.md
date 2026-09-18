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
  input_digest: f37104cb4c5e1676
  outputs:
  - evidence/team-lumen/manifest.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: judging:team-lumen
  stage: initial-judging
  state: complete
  input_digest: d75f17354c66bb62
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
  input_digest: b00512fd150f9155
  outputs:
  - summaries/team-lumen.md
  audit_result: PASS WITH ADVISORIES
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: dossier:team-lumen
  stage: dossiers
  state: complete
  input_digest: 23495d98da9b8e1b
  outputs:
  - dossiers/team-lumen.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: evidence:team-quill
  stage: evidence
  state: complete
  input_digest: 7f9c5d05a023f942
  outputs:
  - evidence/team-quill/manifest.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: judging:team-quill
  stage: initial-judging
  state: complete
  input_digest: 867c090687b9726b
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
  input_digest: 234ea44f0f2ac34d
  outputs:
  - summaries/team-quill.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: dossier:team-quill
  stage: dossiers
  state: complete
  input_digest: 6077e0e04a847c98
  outputs:
  - dossiers/team-quill.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: evidence:team-harbor
  stage: evidence
  state: complete
  input_digest: 4ac163562b16e924
  outputs:
  - evidence/team-harbor/manifest.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: judging:team-harbor
  stage: initial-judging
  state: complete
  input_digest: e6136e8f9972995a
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
  input_digest: 43417dd82487ce04
  outputs:
  - summaries/team-harbor.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: dossier:team-harbor
  stage: dossiers
  state: complete
  input_digest: 9f208c0402a3d192
  outputs:
  - dossiers/team-harbor.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: evidence:team-verdant
  stage: evidence
  state: complete
  input_digest: d29c343c3f229b5e
  outputs:
  - evidence/team-verdant/manifest.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: judging:team-verdant
  stage: initial-judging
  state: complete
  input_digest: 53bff7e8cb29a1bf
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
  input_digest: ae596da9f836a746
  outputs:
  - summaries/team-verdant.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: dossier:team-verdant
  stage: dossiers
  state: complete
  input_digest: f01a1f306d54b171
  outputs:
  - dossiers/team-verdant.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: bracket:draw
  stage: bracket
  state: complete
  input_digest: 1ac51f175c002dd7
  outputs:
  - bracket.md
  - bracket.json
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: matchup:semifinal-1
  stage: tournament
  state: complete
  input_digest: a62497dbd541f381
  outputs:
  - matchups/semifinal-1.md
  - public/semifinal-1.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: matchup:semifinal-2
  stage: tournament
  state: complete
  input_digest: 00a7dbbcbea1c0d5
  outputs:
  - matchups/semifinal-2.md
  - public/semifinal-2.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: matchup:final
  stage: tournament
  state: complete
  input_digest: 4c12884640acdc41
  outputs:
  - matchups/final.md
  - public/final.md
  audit_result: PASS
  completed_at: "2026-05-18T17:30:00Z"
- unit_id: final:audit
  stage: final-audit
  state: complete
  input_digest: 183bf5f40fbc9648
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
