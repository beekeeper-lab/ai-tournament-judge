import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_bracket import build  # noqa: E402


def teams(count=20):
    values = []
    for index in range(count):
        team = {
            "id": f"team-{index:02d}",
            "score": 100 - index,
            "affiliation_group": f"school-{index % 5}",
            "previous_result": "none",
        }
        values.append(team)
    values[0]["previous_result"] = "champion"
    values[1]["previous_result"] = "runner-up"
    return values


class BracketTests(unittest.TestCase):
    def test_twenty_team_shape_and_unique_entries(self):
        result = build({"teams": teams(), "seed": "demo", "bye_policy": "performance-qualified"})
        self.assertEqual(result["bracket_size"], 32)
        self.assertEqual(result["bye_count"], 12)
        entrants = [entry for match in result["first_round"] for entry in match["entrants"] if entry]
        self.assertEqual(len(entrants), 20)
        self.assertEqual(len(set(entrants)), 20)

    def test_same_seed_is_reproducible(self):
        payload = {"teams": teams(), "seed": "repeatable", "bye_policy": "random-lottery"}
        self.assertEqual(build(payload), build(payload))

    def test_performance_byes_select_top_scores(self):
        result = build({"teams": teams(), "seed": "demo", "bye_policy": "performance-qualified"})
        self.assertEqual(set(result["bye_teams"]), {f"team-{index:02d}" for index in range(12)})

    def test_previous_finalists_are_in_opposite_halves(self):
        result = build({"teams": teams(), "seed": "demo", "bye_policy": "performance-qualified"})
        positions = {}
        for index, match in enumerate(result["first_round"]):
            for entrant in match["entrants"]:
                if entrant in {"team-00", "team-01"}:
                    positions[entrant] = index
        midpoint = len(result["first_round"]) // 2
        self.assertNotEqual(positions["team-00"] // midpoint, positions["team-01"] // midpoint)

    def test_duplicate_team_is_rejected(self):
        values = teams(4)
        values[1]["id"] = values[0]["id"]
        with self.assertRaises(ValueError):
            build({"teams": values, "seed": "demo", "bye_policy": "random-lottery"})


if __name__ == "__main__":
    unittest.main()
