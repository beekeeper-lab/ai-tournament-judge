---
event_id: trial-2-2026
override_id: ovr-trial-2-2026-publication-disclosure
scope: event
team_id: null
match_id: null
commit: null
evidence_package_id: null
rubric: submission-evaluation@1.1.0
persona: build-bracket@1.0.0
framework_commit: c728437466d0940734bee600765af298eebb062d
model_requested: not-applicable
model_used: not-applicable
started_at: "2026-09-23T11:03:00Z"
completed_at: "2026-09-23T11:26:00Z"
visibility: private
approval_state: draft
validation_state: unvalidated
authorized_by: event-director
---

# Manual Override Record

`audits/consolidation.md` F34 carried an undecided disclosure question into this
stage: both panel reports enumerate weaknesses in the submission repositories at
exact file and line, and `event.md` held `public/` closed until the
event-director settled it. This record is that decision.

`persona` is `build-bracket@1.0.0` because that is the skill that was running
when this was written, not because a bracket skill produces publication
decisions. No persona in `framework/personas.md` produces a human decision
record taken outside a stage's own skill, which `audits/bracket.md` N14 raises
and `W16` in `docs/0.5.0-beta-plan.md` now carries.

`audits/bracket.md` F3 is why it is a record rather than prose. The decision was
first written into `event.md` as a subsection, where nothing validates it and no
`authorized_by` field carries who made it. The same commit recorded the bracket
exception correctly, one artifact over, and did not apply the same standard
here.

## What was overridden

| Field | Value |
|---|---|
| Artifact | `events/trial-2-2026/event.md` — Publication |
| Framework result | No framework result. `event.md:26` reserves publication approval to `event-director` and the framework declines to decide; `public/` stays closed and `atj validate publication` has not run on any artifact |
| Override result | Public artifacts are approved for this event, with the panel reports' file-and-line weakness citations intact and unredacted. `public_scores` stays `false` and is not changed by this decision |
| Category | publication |

## Authority

`events/trial-2-2026/event.md:26` — `officials.publication_approval:
event-director`. `event.md:103` — `event-director` holds all four authorities
and Gregg Reed holds that role.
`framework/templates/manual-override-record.md:34-35` lists publication approval
among the decisions reserved to humans.

The event has one operator and no separation of duties
(`event.md:103-107`, `R3` in `docs/0.5.0-beta-plan.md`). The official approving
disclosure is the owner of both repositories being disclosed about. That is a
known limit of this event and, for this particular decision, it is also why the
decision is easy: there is no third party to consult.

## Reason

**The private-source condition is not met.** `event.md:180-186` guards against
committing an artifact that names a private-source submission into a public
repository. Checked on 2026-09-23 with `gh repo view ... --json visibility`:
`beekeeper-lab/ScribeVault` is `PUBLIC`, `beekeeper-lab/ai-security-demos` is
`PUBLIC`, and `beekeeper-lab/ai-tournament-judge` is `PUBLIC`. That guard was
written for `live-trial-2026`, whose two submissions are private, and the
question stays open there. It does not reach this event.

**What is actually disclosed.** The panel reports cite weaknesses at exact file
and line in both repositories — on `team-scribe`, an unescaped
markdown-to-`setHtml` render path (`summaries/team-scribe.md:230,344`) and four
`OPENAI_API_KEY` read sites (`:241`); on `team-demos`, its own citations at the
same resolution, among them
`09-toolbox-you-didnt-audit/demo/tools/toolbox.py:47-51` and
`10-show-your-work/demo/scripts/explain.py:85-110`. A reader mostly learns
where to look rather than what the code says, though not always: `summaries/team-scribe.md:243` quotes the fallback
KDF input literal verbatim. Every cited line is already readable by anyone at
the pinned commit, in a public repository, without the report.

**`team-demos` needs no different treatment, but not because its weaknesses
are its subject matter.** They are not. The repository demonstrates attacks
against LLM agents and ships hardened counter-examples, and part of what the
panel found is that some of the hardened examples are not hardened.
`summaries/team-demos.md` PD4 records `Bash(rm:*)` pre-approved in seventeen
command files, the seventeenth being
`10-show-your-work/demo/.claude/commands/screen-pile-audited.md:4`, the
capstone's audited screener, which needs one fixed `rm` on line 30. PD5 records
demo 06's approval gate as a constant in one run path and a model-supplied
argument in the other, against a CLI that accepts `--mode fire` from any caller,
with the README presenting the weaker path as the hero path. PD3 records the
v1.1 POST guard admitting an empty hostname. Those are real defects in the fix,
disclosed here first, and a reader of the public artifact learns something the
repository does not currently teach.

It is approved anyway, on the same ground as `team-scribe`: the repository is
public, the operator owns it, every cited line is readable at the pin without
the report, and there is no third party whose disclosure window is being closed.
The honest description is that this discloses a defect to its owner's own
readers, not that it discloses nothing.

**Redaction was rejected, and not only on those grounds.** Redacting the
citations in public artifacts would put a manual step in front of
`atj validate publication`, which has no control for it. The gate would then not
be what caught a leak, and `H4` in `docs/0.5.0-beta-plan.md` — whether the
publication boundary holds under a real approval — would be tested against
artifacts drained of the content that makes the test real.

**Not approved.** Numeric scores. `public_scores: false` is unchanged in
`event.md:14`. Neither team carries an official total in any case
(`adj:trial-2-2026:team-scribe:01`, `adj:trial-2-2026:team-demos:01`). Whether
that flag moves is a separate event-director decision at the matchup stage.

A participant could be shown this reason as written. Nothing here is private.

## Downstream effects

| Affected artifact | Effect | Re-run required |
|---|---|---|
| `events/trial-2-2026/event.md` | Publication section cites this record instead of carrying the decision | no |
| `events/trial-2-2026/public/` | May now receive artifacts. Still empty; nothing has passed the gate | no |
| Public matchup summary, not yet written | Permitted, with citations intact. `atj validate publication` must still pass and name an approving official | not yet written |
| Team dossiers, not yet written | Same | not yet written |
| `summaries/*.md`, `judgments/*.md` | None. Both stay `visibility: private`; this decision does not publish them | no |

No score, winner, placement or evidence reference is changed by this override,
so nothing is marked stale.

## Disclosure

| Audience | What is disclosed | Approved by |
|---|---|---|
| Panel and event record | This record in full | event-director |
| Both teams | The decision and its reason as written | event-director |
| Public artifacts | Weakness class, severity and exact file and line, unredacted. No numeric score | event-director |

## Validation

- [x] Human official identified by role — `authorized_by: event-director`, the
      role `event.md:26` grants publication approval to
- [x] Authority cited — `event.md:26`, `event.md:103`, and
      `framework/templates/manual-override-record.md:34-35`
- [x] Original artifact preserved unmodified — recorded rather than ticked
      past. Nothing was overridden: the framework produced no result here, it
      reserved the decision and this record supplies it. The artifact named
      under "What was overridden" is `event.md` Publication, and that section
      *was* rewritten in the same commit, to point here instead of carrying the
      decision. What is preserved is what matters: `public_scores: false` is
      untouched, and no judgment, summary or evidence reference moved
- [x] Downstream artifacts marked stale — none are stale. The table above says
      so artifact by artifact; two of the five do not exist yet
- [x] Disclosure decided — that is what this record is, and the table above
      states it by audience
