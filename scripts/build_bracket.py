#!/usr/bin/env python3
"""Build a reproducible constrained-random single-elimination bracket from JSON."""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def next_power_of_two(value: int) -> int:
    if value < 2:
        raise ValueError("At least two teams are required")
    return 1 << math.ceil(math.log2(value))


def choose_byes(teams: list[dict[str, Any]], count: int, policy: str, rng: random.Random) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    shuffled = teams[:]
    rng.shuffle(shuffled)
    if count == 0:
        return [], shuffled
    if policy == "random-lottery":
        ordered = shuffled
    elif policy == "performance-qualified":
        if any("score" not in team for team in shuffled):
            raise ValueError("performance-qualified byes require every team to have a score")
        ordered = sorted(shuffled, key=lambda team: float(team["score"]), reverse=True)
    elif policy == "banded-lottery":
        if any("band" not in team for team in shuffled):
            raise ValueError("banded-lottery requires every team to have a band")
        bands: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for team in shuffled:
            bands[str(team["band"])].append(team)
        ordered = []
        for band in sorted(bands):
            rng.shuffle(bands[band])
            ordered.extend(bands[band])
    else:
        raise ValueError(f"Unknown bye policy: {policy}")
    return ordered[:count], ordered[count:]


def affiliation(team: dict[str, Any]) -> str:
    return str(team.get("affiliation_group") or "")


def pair_play_in_teams(teams: list[dict[str, Any]], rng: random.Random) -> list[list[dict[str, Any]]]:
    remaining = teams[:]
    rng.shuffle(remaining)
    pairs: list[list[dict[str, Any]]] = []
    while remaining:
        first = remaining.pop()
        different = [i for i, candidate in enumerate(remaining) if affiliation(candidate) != affiliation(first)]
        partner_index = rng.choice(different) if different else rng.randrange(len(remaining))
        second = remaining.pop(partner_index)
        pairs.append([first, second])
    return pairs


def unit_priority(unit: list[dict[str, Any]], counts: Counter[str]) -> tuple[int, int]:
    finalist = any(team.get("previous_result") in {"champion", "runner-up"} for team in unit)
    frequency = max((counts[affiliation(team)] for team in unit if affiliation(team)), default=0)
    return (1 if finalist else 0, frequency)


def placement_penalty(unit: list[dict[str, Any]], position: int, placed: dict[int, list[dict[str, Any]]]) -> int:
    penalty = 0
    for other_position, other_unit in placed.items():
        if position // 2 == other_position // 2:
            region_penalty = 1000
        elif position // 4 == other_position // 4:
            region_penalty = 100
        elif position // 8 == other_position // 8:
            region_penalty = 10
        else:
            region_penalty = 0
        for team in unit:
            for other in other_unit:
                if affiliation(team) and affiliation(team) == affiliation(other):
                    penalty += region_penalty
                results = {team.get("previous_result"), other.get("previous_result")}
                if results == {"champion", "runner-up"} and position // 8 == other_position // 8:
                    penalty += 10000
    return penalty


def arrange_units(units: list[list[dict[str, Any]]], rng: random.Random) -> list[list[dict[str, Any]]]:
    counts = Counter(affiliation(team) for unit in units for team in unit if affiliation(team))
    rng.shuffle(units)
    units.sort(key=lambda unit: unit_priority(unit, counts), reverse=True)
    available = list(range(len(units)))
    placed: dict[int, list[dict[str, Any]]] = {}
    for unit in units:
        scored = [(placement_penalty(unit, position, placed), rng.random(), position) for position in available]
        _, _, selected = min(scored)
        placed[selected] = unit
        available.remove(selected)
    return [placed[index] for index in range(len(units))]


def build(payload: dict[str, Any]) -> dict[str, Any]:
    teams = payload.get("teams", [])
    ids = [team.get("id") for team in teams]
    if len(ids) != len(set(ids)) or any(not team_id for team_id in ids):
        raise ValueError("Team IDs must be present and unique")
    size = next_power_of_two(len(teams))
    bye_count = size - len(teams)
    if (len(teams) - bye_count) % 2:
        raise ValueError("Invalid play-in team count")
    seed = str(payload.get("seed", "default-seed"))
    policy = payload.get("bye_policy", "performance-qualified")
    rng = random.Random(seed)
    bye_teams, play_in_teams = choose_byes(teams, bye_count, policy, rng)
    units = [[team] for team in bye_teams] + pair_play_in_teams(play_in_teams, rng)
    arranged = arrange_units(units, rng)

    slots: list[dict[str, Any]] = []
    for match_index, unit in enumerate(arranged, start=1):
        if len(unit) == 1:
            entrants: list[str | None] = [unit[0]["id"], None]
        else:
            entrants = [unit[0]["id"], unit[1]["id"]]
        if rng.random() < 0.5:
            entrants.reverse()
        slots.append({"first_round_match": match_index, "entrants": entrants})

    return {
        "format": "single-elimination",
        "team_count": len(teams),
        "bracket_size": size,
        "bye_count": bye_count,
        "bye_policy": policy,
        "seed": seed,
        "bye_teams": sorted(team["id"] for team in bye_teams),
        "first_round": slots,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON containing teams, seed, and bye_policy")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(json.loads(args.input.read_text(encoding="utf-8")))
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
