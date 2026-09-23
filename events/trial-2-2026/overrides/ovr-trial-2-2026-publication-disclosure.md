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
started_at: "2026-09-23T10:47:00Z"
completed_at: "2026-09-23T11:09:00Z"
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

`audits/bracket.md` F3 is why it is a record rather than prose. The decision was
first written into `event.md` as a subsection, where nothing validates it and no
`authorized_by` field carries who made it. The same commit recorded the bracket
exception correctly, one artifact over, and did not apply the same standard
here.

## What was overridden

| Field | Value |
|---|---|
| Artifact | `events/trial-2-2026/event.md` — Publication |
| Framework result | No framework result. `event.md:25` reserves publication approval to `event-director` and the framework declines to decide; `public/` stays closed and `atj validate publication` has not run on any artifact |
| Override result | Public artifacts are approved for this event, with the panel reports' file-and-line weakness citations intact and unredacted. `public_scores` stays `false` and is not changed by this decision |
| Category | publication |

## Authority

`events/trial-2-2026/event.md:25` — `officials.publication_approval:
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
markdown-to-`setHtml` render path (`summaries/team-scribe.md:343`) and four
`OPENAI_API_KEY` read sites (`:241`); on `team-demos`, thirteen file-and-line
citations of its own. A reader mostly learns where to look rather than what the
code says, though not always: `summaries/team-scribe.md:243` quotes the fallback
KDF input literal verbatim. Every cited line is already readable by anyone at
the pinned commit, in a public repository, without the report.

**`team-demos` needs no different treatment.** It is ten demonstrations of
attacks against LLM agents. Its weaknesses are its subject matter, written to be
read and published as such, and a report naming them at line level discloses
nothing the repository does not set out to teach.

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
      role `event.md:25` grants publication approval to
- [x] Authority cited — `event.md:25`, `event.md:103`, and
      `framework/templates/manual-override-record.md:34-35`
- [x] Original artifact preserved unmodified — nothing was overridden. The
      framework produced no result here; it reserved the decision and this
      record supplies it. `public_scores: false` is untouched
- [x] Downstream artifacts marked stale — none are stale. The table above says
      so artifact by artifact; three of the five do not exist yet
- [x] Disclosure decided — that is what this record is, and the table above
      states it by audience
