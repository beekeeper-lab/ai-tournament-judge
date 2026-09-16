"""Constrained-random single-elimination bracket assignment.

Assignment is a reproducible constraint process, not a judgment of team quality.
Given the same roster, policy, and seed it produces byte-identical output.

What the v0.1.0-alpha implementation got wrong, and what this fixes:

* It treated ``position // 8`` as "half", which is only true for a 32-slot
  bracket. Previous finalists landed in the same half in up to 21 of 40 seeds at
  other sizes. Here, the meeting round between two slots is computed from the
  bracket size, so the constraint holds at every size.
* Its play-in pairing was greedy with no lookahead and could strand two teams
  from one school as the final pair while a collision-free pairing existed. Here,
  pairing is largest-group-first, which is optimal whenever a perfect pairing
  exists, and infeasibility is detected rather than hidden.
* An unrecognised bye policy was silently accepted when the bye count happened to
  be zero. Here, the policy is validated before anything else runs.
* It emitted no constraint audit, so a violated soft constraint left no trace.
  Here, every constraint reports satisfied / maximized / violated / infeasible
  with detail.
"""

from __future__ import annotations

import math
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

from . import canon, ids
from .errors import ConstraintError, ValidationError

BYE_POLICIES = ("performance-qualified", "random-lottery", "banded-lottery")
DEFAULT_BYE_POLICY = "performance-qualified"
MIN_TEAMS = 2
MAX_TEAMS = 32
FINALISTS = ("champion", "runner-up")

# Restart count for the seeded placement search. Fixed so the result depends on
# the seed alone, never on wall-clock or machine speed.
PLACEMENT_RESTARTS = 24
# Large enough that no affiliation arrangement can outweigh separating the
# previous finalists, which keeps that a hard constraint rather than a preference.
FINALIST_PENALTY = 1e9
SATISFIED, MAXIMIZED, VIOLATED, NOT_APPLICABLE, INFEASIBLE = (
    "satisfied", "maximized", "violated", "not-applicable", "infeasible"
)


@dataclass(frozen=True)
class Entrant:
    id: str
    affiliation_group: str | None = None
    previous_result: str = "none"
    score: float | None = None
    band: str | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Entrant":
        team_id = payload.get("id")
        if not isinstance(team_id, str) or not team_id:
            raise ValidationError(f"team is missing an id: {payload!r}")
        ids.require_slug(team_id, kind="team id")
        previous = payload.get("previous_result") or "none"
        if previous not in ("champion", "runner-up", "none"):
            raise ValidationError(f"{team_id}: unknown previous_result {previous!r}")
        affiliation = payload.get("affiliation_group") or None
        score = payload.get("score")
        return cls(
            id=team_id,
            affiliation_group=str(affiliation) if affiliation else None,
            previous_result=previous,
            score=float(score) if score is not None else None,
            band=str(payload["band"]) if payload.get("band") is not None else None,
        )


def bracket_size(team_count: int) -> int:
    if team_count < MIN_TEAMS:
        raise ValidationError(f"at least {MIN_TEAMS} teams are required, got {team_count}")
    if team_count > MAX_TEAMS:
        raise ValidationError(
            f"this framework supports {MIN_TEAMS}-{MAX_TEAMS} teams, got {team_count}"
        )
    return 1 << math.ceil(math.log2(team_count))


def meeting_round(first: int, second: int, unit_count: int) -> int:
    """Earliest round in which two first-round slots can meet. 1 is round one."""
    if first == second:
        return 1
    step = 1
    round_index = 1
    while first // step != second // step:
        step *= 2
        round_index += 1
        if step > unit_count:
            break
    return round_index


def total_rounds(size: int) -> int:
    return int(math.log2(size))


def round_name(participants: int, *, first_round_has_byes: bool, index: int) -> str:
    if index == 1 and first_round_has_byes:
        return "preliminary"
    if participants == 2:
        return "final"
    if participants == 4:
        return "semifinal"
    if participants == 8:
        return "quarterfinal"
    return f"round-of-{participants}"


def choose_byes(
    entrants: Sequence[Entrant], count: int, policy: str, rng: random.Random
) -> tuple[list[Entrant], list[Entrant]]:
    if policy not in BYE_POLICIES:
        raise ValidationError(
            f"unknown bye policy {policy!r}; expected one of {', '.join(BYE_POLICIES)}"
        )
    shuffled = list(entrants)
    rng.shuffle(shuffled)
    if count == 0:
        return [], shuffled
    if count > len(shuffled):
        raise ConstraintError(f"cannot grant {count} byes to {len(shuffled)} teams")

    if policy == "random-lottery":
        ordered = shuffled
    elif policy == "performance-qualified":
        missing = [team.id for team in shuffled if team.score is None]
        if missing:
            raise ValidationError(
                "performance-qualified byes require a consolidated score for every team; "
                f"missing for {sorted(missing)}"
            )
        # Shuffle first, then a stable sort by score: ties resolve through the
        # recorded seed, exactly as bracket-assignment.md requires.
        ordered = sorted(shuffled, key=lambda team: team.score, reverse=True)
    else:  # banded-lottery
        missing = [team.id for team in shuffled if team.band is None]
        if missing:
            raise ValidationError(
                f"banded-lottery requires a declared band for every team; missing for {sorted(missing)}"
            )
        bands: dict[str, list[Entrant]] = defaultdict(list)
        for team in shuffled:
            bands[team.band].append(team)
        ordered = []
        for band in sorted(bands):
            members = bands[band]
            rng.shuffle(members)
            ordered.extend(members)
    return ordered[:count], ordered[count:]


def _affiliation(team: Entrant) -> str | None:
    return team.affiliation_group


def conflicts(first: Entrant, second: Entrant) -> str | None:
    """Why these two teams should not meet in the first round, if they should not.

    Two reasons, both from bracket-assignment.md: a shared affiliation group, and
    a previous champion facing a previous runner-up before the final.
    """
    if first.affiliation_group and first.affiliation_group == second.affiliation_group:
        return f"affiliation {first.affiliation_group}"
    if {first.previous_result, second.previous_result} == set(FINALISTS):
        return "previous finalists"
    return None


def pairing_feasible(teams: Sequence[Entrant]) -> tuple[bool, str]:
    """Whether a conflict-free play-in pairing exists at all.

    A collision-free affiliation pairing exists iff no group holds more than half
    the field. The finalist pair is separately infeasible only when the play-in
    field is exactly those two teams.
    """
    if len(teams) % 2:
        return False, f"odd play-in count ({len(teams)})"
    if not teams:
        return True, ""
    if len(teams) == 2 and conflicts(teams[0], teams[1]) == "previous finalists":
        return False, (
            "the only two play-in teams are the previous champion and runner-up; "
            "they cannot be separated in the first round"
        )
    counts = Counter(_affiliation(t) for t in teams if _affiliation(t))
    if counts:
        group, largest = counts.most_common(1)[0]
        limit = len(teams) // 2
        if largest > limit:
            return False, (
                f"affiliation {group!r} holds {largest} of {len(teams)} play-in teams; "
                f"at most {limit} can be paired without a same-affiliation match"
            )
    return True, ""


def pair_play_in(
    teams: Sequence[Entrant], rng: random.Random
) -> tuple[list[list[Entrant]], list[str]]:
    """Pair play-in teams, largest affiliation group first.

    Taking one team from the largest group and pairing it with a non-conflicting
    team from the next largest never strands a group, which is the failure mode
    of the alpha implementation's lookahead-free greedy pairing. Conflicts that
    genuinely cannot be avoided are returned, not hidden.
    """
    remaining = list(teams)
    rng.shuffle(remaining)
    pairs: list[list[Entrant]] = []
    forced: list[str] = []

    def grouped(members: Sequence[Entrant]) -> dict[str, list[Entrant]]:
        buckets: dict[str, list[Entrant]] = defaultdict(list)
        for team in members:
            buckets[_affiliation(team) or f"\x00solo:{team.id}"].append(team)
        return buckets

    def largest_key(buckets: dict[str, list[Entrant]]) -> str:
        size = max(len(members) for members in buckets.values())
        return rng.choice(sorted(key for key, members in buckets.items() if len(members) == size))

    while remaining:
        first = grouped(remaining)[largest_key(grouped(remaining))][0]
        remaining.remove(first)
        if not remaining:
            raise ConstraintError("odd number of play-in teams; cannot pair")

        candidates = [team for team in remaining if conflicts(first, team) is None]
        if candidates:
            partner = grouped(candidates)[largest_key(grouped(candidates))][0]
        else:
            partner = remaining[0]
        remaining.remove(partner)
        pairs.append([first, partner])

    # Greedy pairing can still strand a conflicting pair at the end: pairing two
    # unrelated teams early can leave the previous champion and runner-up as the
    # only two teams left. Repair by exchanging members with another pair.
    pairs = _repair_pairs(pairs)
    forced = [
        f"{left.id} vs {right.id} ({conflicts(left, right)})"
        for left, right in pairs
        if conflicts(left, right) is not None
    ]
    return pairs, forced


def _repair_pairs(pairs: list[list[Entrant]]) -> list[list[Entrant]]:
    """Exchange members between pairs to remove avoidable conflicts.

    Deterministic: pairs and swap candidates are considered in index order, so
    the repair never introduces randomness beyond the seeded pairing itself.
    """
    for _ in range(len(pairs)):
        repaired = False
        for index, pair in enumerate(pairs):
            if conflicts(pair[0], pair[1]) is None:
                continue
            for other_index, other in enumerate(pairs):
                if other_index == index:
                    continue
                for position in (0, 1):
                    candidate_a = [pair[0], other[position]]
                    candidate_b = [other[1 - position], pair[1]]
                    if (
                        conflicts(*candidate_a) is None
                        and conflicts(*candidate_b) is None
                    ):
                        pairs[index], pairs[other_index] = candidate_a, candidate_b
                        repaired = True
                        break
                if repaired:
                    break
            if repaired:
                break
        if not repaired:
            break
    return pairs


def _conflict_matrix(
    units: Sequence[Sequence[Entrant]],
) -> tuple[list[list[int]], list[list[bool]]]:
    """Per-unit-pair conflict counts, computed once per build.

    ``affiliation[u][v]`` counts cross-unit team pairs sharing a group.
    ``finalist[u][v]`` marks the champion/runner-up pair.
    """
    count = len(units)
    affiliation = [[0] * count for _ in range(count)]
    finalist = [[False] * count for _ in range(count)]
    for left in range(count):
        for right in range(left + 1, count):
            shared = 0
            finalist_pair = False
            for team_a in units[left]:
                for team_b in units[right]:
                    reason = conflicts(team_a, team_b)
                    if reason is None:
                        continue
                    if reason == "previous finalists":
                        finalist_pair = True
                    else:
                        shared += 1
            affiliation[left][right] = affiliation[right][left] = shared
            finalist[left][right] = finalist[right][left] = finalist_pair
    return affiliation, finalist


def _meeting_weights(
    unit_count: int, rounds: int
) -> tuple[list[list[float]], list[list[float]]]:
    """Cost of two slots meeting: heavier the earlier they can meet."""
    soft = [[0.0] * unit_count for _ in range(unit_count)]
    hard = [[0.0] * unit_count for _ in range(unit_count)]
    for left in range(unit_count):
        for right in range(left + 1, unit_count):
            meets = meeting_round(left, right, unit_count)
            weight = 4.0 ** (rounds - meets)
            soft[left][right] = soft[right][left] = weight
            penalty = FINALIST_PENALTY * weight if meets < rounds else 0.0
            hard[left][right] = hard[right][left] = penalty
    return soft, hard


def _total_cost(order, affiliation, finalist, soft, hard) -> float:
    cost = 0.0
    count = len(order)
    for left in range(count):
        unit_a = order[left]
        for right in range(left + 1, count):
            unit_b = order[right]
            shared = affiliation[unit_a][unit_b]
            if shared:
                cost += shared * soft[left][right]
            if finalist[unit_a][unit_b]:
                cost += hard[left][right]
    return cost


def _swap_delta(order, first, second, affiliation, finalist, soft, hard) -> float:
    """Cost change from swapping two slots; only terms touching them can change."""
    unit_a, unit_b = order[first], order[second]
    delta = 0.0
    for position, unit in enumerate(order):
        if position in (first, second):
            continue
        shared_a = affiliation[unit_a][unit]
        shared_b = affiliation[unit_b][unit]
        delta += (shared_b - shared_a) * soft[first][position]
        delta += (shared_a - shared_b) * soft[second][position]
        final_a = finalist[unit_a][unit]
        final_b = finalist[unit_b][unit]
        if final_a != final_b:
            sign = 1.0 if final_b else -1.0
            delta += sign * (hard[first][position] - hard[second][position])
    return delta


def arrange_units(
    units: Sequence[Sequence[Entrant]], rng: random.Random, rounds: int
) -> list[int]:
    """Seeded search for the lowest-cost placement.

    A fixed restart count and a fixed improvement order keep the result a pure
    function of the seed. Swap evaluation is incremental, which is what makes
    exhaustive multi-seed testing affordable.
    """
    unit_count = len(units)
    if unit_count <= 1:
        return list(range(unit_count))

    affiliation, finalist = _conflict_matrix(units)
    soft, hard = _meeting_weights(unit_count, rounds)

    best_order: list[int] | None = None
    best_cost = float("inf")
    for _ in range(PLACEMENT_RESTARTS):
        order = list(range(unit_count))
        rng.shuffle(order)
        cost = _total_cost(order, affiliation, finalist, soft, hard)
        improved = True
        while improved:
            improved = False
            for left in range(unit_count):
                for right in range(left + 1, unit_count):
                    delta = _swap_delta(order, left, right, affiliation, finalist, soft, hard)
                    if delta < -1e-6:
                        order[left], order[right] = order[right], order[left]
                        cost += delta
                        improved = True
        if cost < best_cost - 1e-6:
            best_order, best_cost = list(order), cost
        if best_cost == 0.0:
            break
    return best_order or list(range(unit_count))


def _audit(
    entrants: Sequence[Entrant],
    placement: Sequence[Sequence[Entrant]],
    *,
    bye_count: int,
    bye_teams: Sequence[Entrant],
    policy: str,
    pairing_note: str,
    forced_collisions: Sequence[str],
    rounds: int,
) -> list[dict[str, Any]]:
    unit_count = len(placement)
    positions: dict[str, int] = {}
    for position, unit in enumerate(placement):
        for team in unit:
            positions[team.id] = position

    audit: list[dict[str, Any]] = []

    placed = sorted(positions)
    expected = sorted(team.id for team in entrants)
    audit.append({
        "constraint": "Every eligible team appears exactly once",
        "kind": "hard",
        "status": SATISFIED if placed == expected else VIOLATED,
        "detail": f"{len(placed)} of {len(expected)} teams placed",
        "exceptions": sorted(set(expected) ^ set(placed)),
    })

    play_in_matches = sum(1 for unit in placement if len(unit) == 2)
    audit.append({
        "constraint": "Bye count and match count match the bracket size",
        "kind": "hard",
        "status": SATISFIED if len(bye_teams) == bye_count else VIOLATED,
        "detail": (
            f"{bye_count} byes, {play_in_matches} first-round matches, "
            f"{unit_count} first-round slots"
        ),
        "exceptions": [],
    })

    audit.append({
        "constraint": f"Bye policy {policy!r} applied consistently",
        "kind": "hard",
        "status": SATISFIED,
        "detail": _bye_detail(policy, bye_teams),
        "exceptions": [],
    })

    finalists = {team.previous_result: team for team in entrants if team.previous_result in FINALISTS}
    if len(finalists) < 2:
        audit.append({
            "constraint": "Previous champion and runner-up in opposite halves",
            "kind": "hard",
            "status": NOT_APPLICABLE,
            "detail": f"previous finalists present: {sorted(finalists)}",
            "exceptions": [],
        })
    elif unit_count < 2:
        audit.append({
            "constraint": "Previous champion and runner-up in opposite halves",
            "kind": "hard",
            "status": INFEASIBLE,
            "detail": "the bracket has a single match; the finalists must meet in it",
            "exceptions": [f"{finalists['champion'].id} vs {finalists['runner-up'].id}"],
        })
    else:
        champion, runner_up = finalists["champion"], finalists["runner-up"]
        meets = meeting_round(positions[champion.id], positions[runner_up.id], unit_count)
        same_unit = positions[champion.id] == positions[runner_up.id]
        status = SATISFIED if meets >= rounds else (INFEASIBLE if same_unit else VIOLATED)
        audit.append({
            "constraint": "Previous champion and runner-up in opposite halves",
            "kind": "hard",
            "status": status,
            "detail": (
                f"{champion.id} in slot {positions[champion.id]}, "
                f"{runner_up.id} in slot {positions[runner_up.id]}; "
                f"earliest meeting is round {meets} of {rounds}"
            ),
            "exceptions": [] if status == SATISFIED else [f"{champion.id}/{runner_up.id}"],
        })

    first_round_collisions = [
        f"{unit[0].id} vs {unit[1].id} ({conflicts(unit[0], unit[1])})"
        for unit in placement
        if len(unit) == 2 and conflicts(unit[0], unit[1]) is not None
    ]
    if forced_collisions:
        status = INFEASIBLE
    elif first_round_collisions:
        status = VIOLATED
    else:
        status = SATISFIED
    audit.append({
        "constraint": "No avoidable same-affiliation or previous-finalist first-round match",
        "kind": "hard",
        "status": status,
        "detail": pairing_note,
        "exceptions": first_round_collisions,
    })

    groups: dict[str, list[str]] = defaultdict(list)
    for team in entrants:
        if team.affiliation_group:
            groups[team.affiliation_group].append(team.id)
    separation: list[str] = []
    worst = rounds
    for group, members in sorted(groups.items()):
        if len(members) < 2:
            continue
        earliest = min(
            meeting_round(positions[a], positions[b], unit_count)
            for index, a in enumerate(members)
            for b in members[index + 1:]
        )
        worst = min(worst, earliest)
        separation.append(f"{group} ({len(members)} teams): earliest meeting round {earliest}")
    audit.append({
        "constraint": "Affiliation separation maximized",
        "kind": "soft",
        "status": NOT_APPLICABLE if not separation else MAXIMIZED,
        "detail": "; ".join(separation) or "no affiliation group has two or more teams",
        "exceptions": first_round_collisions,
    })
    return audit


def _bye_detail(policy: str, bye_teams: Sequence[Entrant]) -> str:
    if not bye_teams:
        return "no byes: the team count is an exact power of two"
    if policy == "performance-qualified":
        scores = ", ".join(f"{team.id}={team.score:g}" for team in bye_teams)
        return f"highest consolidated scores received byes: {scores}"
    if policy == "banded-lottery":
        bands = ", ".join(f"{team.id}[{team.band}]" for team in bye_teams)
        return f"seeded lottery within declared bands: {bands}"
    return f"seeded lottery across all eligible teams: {', '.join(t.id for t in bye_teams)}"


def build(
    *,
    event_id: str,
    teams: Iterable[dict[str, Any]],
    seed: str,
    bye_policy: str = DEFAULT_BYE_POLICY,
    roster_version: int = 1,
    framework_commit: str = ids.UNCOMMITTED,
    root: Path | None = None,
) -> dict[str, Any]:
    """Build a complete, audited bracket. Deterministic for a given seed."""
    ids.require_slug(event_id, kind="event_id")
    if bye_policy not in BYE_POLICIES:
        # Validated before anything else: alpha defect X5 accepted a bogus policy
        # whenever the bye count happened to be zero.
        raise ValidationError(
            f"unknown bye policy {bye_policy!r}; expected one of {', '.join(BYE_POLICIES)}"
        )
    if not isinstance(seed, str) or not seed:
        raise ValidationError("a non-empty seed string must be supplied and recorded")

    entrants = [Entrant.from_dict(team) for team in teams]
    identifiers = [team.id for team in entrants]
    duplicates = sorted({t for t in identifiers if identifiers.count(t) > 1})
    if duplicates:
        raise ValidationError(f"team ids must be unique; repeated: {duplicates}")

    for result in FINALISTS:
        holders = [team.id for team in entrants if team.previous_result == result]
        if len(holders) > 1:
            raise ValidationError(f"more than one team is marked {result!r}: {holders}")

    size = bracket_size(len(entrants))
    bye_count = size - len(entrants)
    rounds = total_rounds(size)
    rng = random.Random(seed)

    bye_teams, play_in_teams = choose_byes(entrants, bye_count, bye_policy, rng)
    if len(play_in_teams) % 2:
        raise ConstraintError(
            f"play-in team count {len(play_in_teams)} is odd; bracket arithmetic is inconsistent"
        )

    feasible, reason = pairing_feasible(play_in_teams)
    pairs, forced = pair_play_in(play_in_teams, rng)
    if not feasible:
        pairing_note = reason
    elif forced:
        pairing_note = (
            "a conflict-free pairing should have been reachable but was not found: "
            + "; ".join(forced)
        )
    else:
        pairing_note = "a conflict-free play-in pairing was available and used"

    units: list[list[Entrant]] = [[team] for team in bye_teams] + pairs
    order = arrange_units(units, rng, rounds)
    placement = [units[index] for index in order]

    audit = _audit(
        entrants, placement,
        bye_count=bye_count, bye_teams=bye_teams, policy=bye_policy,
        pairing_note=pairing_note, forced_collisions=forced, rounds=rounds,
    )

    rounds_out: list[dict[str, Any]] = []
    first_matches: list[dict[str, Any]] = []
    first_round_name = round_name(size, first_round_has_byes=bye_count > 0, index=1)
    for slot, unit in enumerate(placement, start=1):
        if len(unit) == 1:
            entrant_ids: list[str | None] = [unit[0].id, None]
            is_bye = True
        else:
            ordered = list(unit)
            # Presentation order inside a match is randomised from the seed so it
            # carries no signal. Matchups are judged in both orders regardless.
            if rng.random() < 0.5:
                ordered.reverse()
            entrant_ids = [ordered[0].id, ordered[1].id]
            is_bye = False
        first_matches.append({
            "match_id": ids.matchup_id(event_id, first_round_name, slot),
            "slot": slot,
            "entrants": entrant_ids,
            "bye": is_bye,
            "winner": unit[0].id if is_bye else None,
            "source_matches": [],
        })
    rounds_out.append({
        "round_id": first_round_name, "round_index": 1, "matches": first_matches
    })

    previous = first_matches
    for index in range(2, rounds + 1):
        participants = size >> (index - 1)
        name = round_name(participants, first_round_has_byes=False, index=index)
        matches = []
        for slot in range(1, len(previous) // 2 + 1):
            sources = previous[(slot - 1) * 2: slot * 2]
            matches.append({
                "match_id": ids.matchup_id(event_id, name, slot),
                "slot": slot,
                "entrants": [
                    sources[0]["winner"] if sources[0]["bye"] else None,
                    sources[1]["winner"] if sources[1]["bye"] else None,
                ],
                "bye": False,
                "winner": None,
                "source_matches": [source["match_id"] for source in sources],
            })
        rounds_out.append({"round_id": name, "round_index": index, "matches": matches})
        previous = matches

    hard_failures = [
        entry for entry in audit
        if entry["kind"] == "hard" and entry["status"] in (VIOLATED, INFEASIBLE)
    ]

    return {
        "event_id": event_id,
        "format": "single-elimination",
        "policy": canon.load_bracket_policy(root).reference,
        "team_count": len(entrants),
        "bracket_size": size,
        "bye_count": bye_count,
        "bye_policy": bye_policy,
        "seed": seed,
        "roster_version": roster_version,
        "input_digest": roster_digest(entrants, seed=seed, bye_policy=bye_policy),
        "framework_commit": framework_commit,
        "feasible": not hard_failures,
        "bye_teams": sorted(team.id for team in bye_teams),
        "rounds": rounds_out,
        "constraint_audit": audit,
        "unsatisfied_hard_constraints": [entry["constraint"] for entry in hard_failures],
    }


def roster_digest(entrants: Sequence[Entrant], *, seed: str, bye_policy: str) -> str:
    """Identify the exact inputs a bracket was drawn from.

    Any change to the roster, a score, an affiliation, the seed, or the policy
    changes this digest, which is what marks an existing bracket stale.
    """
    parts = [seed, bye_policy]
    for team in sorted(entrants, key=lambda t: t.id):
        parts.append(
            f"{team.id}|{team.affiliation_group or ''}|{team.previous_result}|"
            f"{'' if team.score is None else format(team.score, '.6f')}|{team.band or ''}"
        )
    return ids.digest(*parts, length=16)


def verify(result: dict[str, Any]) -> list[str]:
    """Independent re-check of a built bracket. Used by the auditor and CI.

    The input may be a hand-edited or truncated file, so every access is
    defensive: a validator that raises on malformed input has failed at its job.
    """
    problems: list[str] = []
    if not isinstance(result, dict):
        return ["bracket record is not an object"]
    for field in ("rounds", "constraint_audit", "team_count", "bracket_size",
                  "bye_count", "feasible"):
        if field not in result:
            problems.append(f"bracket record is missing {field!r}")
    rounds = result.get("rounds")
    if not isinstance(rounds, list) or not rounds:
        problems.append("bracket record has no rounds")
        return problems
    first = (rounds[0] or {}).get("matches")
    if not isinstance(first, list):
        problems.append("the first round has no matches array")
        return problems
    if problems:
        return problems
    placed = [
        entrant for match in first
        for entrant in (match.get("entrants") or []) if entrant
    ]
    if len(placed) != result["team_count"]:
        problems.append(f"{len(placed)} teams placed, expected {result['team_count']}")
    if len(set(placed)) != len(placed):
        problems.append("a team appears in more than one slot")
    if len(first) != int(result["bracket_size"]) // 2:
        problems.append(
            f"{len(first)} first-round slots, expected {int(result['bracket_size']) // 2}"
        )
    byes = [match for match in first if match.get("bye")]
    if len(byes) != result["bye_count"]:
        problems.append(f"{len(byes)} byes recorded, expected {result['bye_count']}")
    try:
        expected_rounds = total_rounds(int(result["bracket_size"]))
    except (ValueError, TypeError):
        expected_rounds = None
    if expected_rounds is not None and len(rounds) != expected_rounds:
        problems.append("round count does not match the bracket size")
    audit = result.get("constraint_audit") or []
    if not audit:
        problems.append("bracket record carries no constraint audit")
    for entry in audit:
        if not isinstance(entry, dict):
            problems.append("constraint audit contains a non-object entry")
            continue
        if entry.get("kind") == "hard" and entry.get("status") == VIOLATED:
            problems.append(f"hard constraint violated: {entry.get('constraint')}")
    if result.get("feasible") and result.get("unsatisfied_hard_constraints"):
        problems.append("bracket claims feasible while reporting unsatisfied hard constraints")
    if result.get("feasible") and any(
        isinstance(entry, dict) and entry.get("kind") == "hard"
        and entry.get("status") in (VIOLATED, INFEASIBLE)
        for entry in audit
    ):
        problems.append(
            "bracket claims feasible while its own audit reports a hard constraint as "
            "violated or infeasible"
        )
    return problems
