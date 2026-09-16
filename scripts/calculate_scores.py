#!/usr/bin/env python3
"""Calculate official panel scores from JSON.

Input shape:
{
  "weights": {"functional": 25, ...},
  "judges": [{"judge_id": "judge-backend", "scores": {"functional": 3, ...}}]
}
"""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any


DEFAULT_WEIGHTS = {
    "functional": 25,
    "product": 15,
    "agentic": 15,
    "engineering": 15,
    "reliability": 10,
    "security": 10,
    "innovation": 10,
}


def agreement_level(values: list[float]) -> str:
    score_range = max(values) - min(values)
    if score_range <= 1:
        return "aligned"
    if score_range <= 2:
        return "material-disagreement"
    return "severe-disagreement"


def calculate(payload: dict[str, Any]) -> dict[str, Any]:
    weights = payload.get("weights", DEFAULT_WEIGHTS)
    judges = payload.get("judges", [])
    if not judges:
        raise ValueError("At least one judge is required")
    if abs(sum(weights.values()) - 100) > 1e-9:
        raise ValueError("Criterion weights must total 100")

    result: dict[str, Any] = {"criteria": {}, "judge_count": len(judges)}
    total = 0.0
    for criterion, weight in weights.items():
        values: list[float] = []
        for judge in judges:
            score = judge.get("scores", {}).get(criterion)
            if score == "NE" or score is None:
                raise ValueError(
                    f"Judge {judge.get('judge_id', '<unknown>')} has unresolved {criterion}: {score}"
                )
            score = float(score)
            if not 0 <= score <= 5:
                raise ValueError(f"Score outside 0-5 for {criterion}: {score}")
            values.append(score)

        mean = statistics.fmean(values)
        points = mean / 5 * float(weight)
        median = statistics.median(values)
        outliers = [
            judges[index].get("judge_id", str(index))
            for index, value in enumerate(values)
            if abs(value - median) >= 2
        ]
        result["criteria"][criterion] = {
            "scores": values,
            "mean": round(mean, 4),
            "minimum": min(values),
            "maximum": max(values),
            "range": max(values) - min(values),
            "weight": weight,
            "weighted_points": round(points, 4),
            "agreement": agreement_level(values),
            "possible_outliers": outliers,
        }
        total += points

    result["total"] = round(total, 4)
    result["display_total"] = round(total, 1)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON input file")
    parser.add_argument("--output", type=Path, help="Write JSON result to this path")
    args = parser.parse_args()
    result = calculate(json.loads(args.input.read_text(encoding="utf-8")))
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
