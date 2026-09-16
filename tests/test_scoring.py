import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from calculate_scores import DEFAULT_WEIGHTS, calculate  # noqa: E402


class ScoringTests(unittest.TestCase):
    def payload(self, score):
        return {
            "weights": DEFAULT_WEIGHTS,
            "judges": [
                {"judge_id": f"judge-{index}", "scores": {key: score for key in DEFAULT_WEIGHTS}}
                for index in range(4)
            ],
        }

    def test_perfect_score_is_one_hundred(self):
        self.assertEqual(calculate(self.payload(5))["total"], 100)

    def test_midpoint_score_is_sixty(self):
        self.assertEqual(calculate(self.payload(3))["total"], 60)

    def test_unresolved_evidence_blocks_total(self):
        payload = self.payload(3)
        payload["judges"][0]["scores"]["security"] = "NE"
        with self.assertRaises(ValueError):
            calculate(payload)

    def test_large_range_is_severe_disagreement(self):
        payload = self.payload(3)
        payload["judges"][0]["scores"]["functional"] = 0
        payload["judges"][1]["scores"]["functional"] = 5
        result = calculate(payload)
        self.assertEqual(result["criteria"]["functional"]["agreement"], "severe-disagreement")


if __name__ == "__main__":
    unittest.main()
