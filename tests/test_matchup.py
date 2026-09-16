"""Order-balanced head-to-head resolution."""

import unittest

from _support import ROOT  # noqa: F401
from atj import canon, matchup
from atj.errors import ValidationError

RUBRIC = canon.load(ROOT)
H2H = canon.load_head_to_head(ROOT)
A, B = "team-alpha", "team-beta"


def comparisons(**values):
    return {criterion: values.get(criterion, 0) for criterion in RUBRIC.criterion_ids}


def resolve(a_values, b_values, band=None, presented=(A, B)):
    return matchup.calculate(
        team_a=A, team_b=B,
        a_first={"presented_first": presented[0], "comparisons": a_values},
        b_first={"presented_first": presented[1], "comparisons": b_values},
        close_call_band=band, root=ROOT,
    )


class NormalizationTests(unittest.TestCase):
    def test_b_first_pass_is_negated_into_a_orientation(self):
        raw = comparisons(functional=2)
        normalized = matchup.normalize_pass(
            raw, presented_first=B, team_a=A, team_b=B,
            minimum=H2H.minimum_value, maximum=H2H.maximum_value,
        )
        self.assertEqual(normalized["functional"], -2)

    def test_a_first_pass_is_unchanged(self):
        raw = comparisons(functional=2)
        normalized = matchup.normalize_pass(
            raw, presented_first=A, team_a=A, team_b=B,
            minimum=H2H.minimum_value, maximum=H2H.maximum_value,
        )
        self.assertEqual(normalized["functional"], 2)

    def test_swapping_the_teams_mirrors_the_margin(self):
        """The orientation convention must be symmetric or half the bracket inverts."""
        forward = resolve(comparisons(functional=2, product=1), comparisons(functional=-2, product=-1))
        mirrored = matchup.calculate(
            team_a=B, team_b=A,
            a_first={"presented_first": B, "comparisons": comparisons(functional=-2, product=-1)},
            b_first={"presented_first": A, "comparisons": comparisons(functional=2, product=1)},
            root=ROOT,
        )
        self.assertEqual(forward["combined_margin"], -mirrored["combined_margin"])
        self.assertEqual(forward["winner"], mirrored["winner"])

    def test_value_bounds_come_from_the_rubric_table(self):
        self.assertEqual((H2H.minimum_value, H2H.maximum_value), (-2, 2))
        with self.assertRaises(ValidationError):
            resolve(comparisons(functional=3), comparisons(functional=-3))

    def test_non_integer_comparison_is_rejected(self):
        with self.assertRaises(ValidationError):
            resolve(comparisons(functional=1.5), comparisons(functional=-1))
        with self.assertRaises(ValidationError):
            resolve(comparisons(functional=True), comparisons(functional=-1))


class MarginTests(unittest.TestCase):
    def test_maximum_margin_is_one_hundred(self):
        result = resolve(
            {c: 2 for c in RUBRIC.criterion_ids}, {c: -2 for c in RUBRIC.criterion_ids}
        )
        self.assertEqual(result["combined_margin"], 100.0)

    def test_minimum_margin_is_minus_one_hundred(self):
        result = resolve(
            {c: -2 for c in RUBRIC.criterion_ids}, {c: 2 for c in RUBRIC.criterion_ids}
        )
        self.assertEqual(result["combined_margin"], -100.0)

    def test_criterion_margin_uses_the_rubric_weight(self):
        result = resolve(comparisons(functional=2), comparisons(functional=-2))
        self.assertEqual(result["criteria"]["functional"]["combined_margin"],
                         float(RUBRIC.weights["functional"]))

    def test_criteria_must_match_the_rubric(self):
        with self.assertRaises(ValidationError):
            resolve({"velocity": 1}, {"velocity": -1})


class OutcomeTests(unittest.TestCase):
    def test_consistent_decisive_result_is_confirmed(self):
        result = resolve(comparisons(functional=2, product=1), comparisons(functional=-2, product=-1))
        self.assertEqual(result["outcome"], matchup.CONFIRMED)
        self.assertEqual(result["winner"], A)
        self.assertFalse(result["order_disagreement"])

    def test_order_disagreement_blocks_a_winner(self):
        result = resolve(comparisons(functional=2), comparisons(functional=2))
        self.assertEqual(result["outcome"], matchup.ADJUDICATION_REQUIRED)
        self.assertIsNone(result["winner"])
        self.assertTrue(result["order_disagreement"])

    def test_close_call_blocks_a_winner(self):
        result = resolve(comparisons(reliability=1), comparisons(reliability=-1))
        self.assertEqual(result["combined_margin"], 5.0)
        self.assertEqual(result["outcome"], matchup.ADJUDICATION_REQUIRED)
        self.assertIsNone(result["winner"])

    def test_just_outside_the_band_is_confirmed(self):
        result = resolve(comparisons(reliability=1, security=1), comparisons(reliability=-1, security=-1))
        self.assertEqual(result["combined_margin"], 10.0)
        self.assertEqual(result["outcome"], matchup.CONFIRMED)

    def test_an_event_may_widen_the_band_but_never_narrow_it(self):
        """Narrowing turns results needing human review into automatic advancement."""
        values = (comparisons(reliability=1, security=1), comparisons(reliability=-1, security=-1))
        # Widening sends more matchups to a human: allowed.
        self.assertEqual(resolve(*values, band=20)["outcome"], matchup.ADJUDICATION_REQUIRED)
        # Narrowing is refused, including to exactly zero.
        for narrow in (0, 1, 4.9, -3):
            with self.assertRaises(ValidationError):
                resolve(*values, band=narrow)

    def test_an_input_file_cannot_narrow_the_band_through_the_cli(self):
        import json
        import tempfile
        from atj.cli import main

        payload = {
            "team_a": A, "team_b": B, "close_call_band": 0,
            "a_first": {"presented_first": A, "comparisons": comparisons(security=1)},
            "b_first": {"presented_first": B, "comparisons": comparisons(security=-1)},
        }
        with tempfile.TemporaryDirectory() as directory:
            path = f"{directory}/matchup.json"
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(payload, handle)
            self.assertEqual(main(["--root", str(ROOT), "matchup", path]), 1)

    def test_a_band_on_the_boundary_still_requires_adjudication(self):
        result = resolve(comparisons(security=1), comparisons(security=-1))
        self.assertEqual(result["combined_margin"], 5.0)
        self.assertEqual(result["outcome"], matchup.ADJUDICATION_REQUIRED)
        self.assertIsNone(result["winner"])

    def test_dead_tie_requires_adjudication(self):
        result = resolve(comparisons(), comparisons())
        self.assertEqual(result["outcome"], matchup.ADJUDICATION_REQUIRED)
        self.assertIsNone(result["winner"])

    def test_adjudication_never_returns_a_winner_to_advance(self):
        """The caller cannot advance a team it was never given."""
        for a_values, b_values in (
            (comparisons(functional=2), comparisons(functional=2)),
            (comparisons(reliability=1), comparisons(reliability=-1)),
            (comparisons(), comparisons()),
        ):
            result = resolve(a_values, b_values)
            if result["outcome"] == matchup.ADJUDICATION_REQUIRED:
                self.assertIsNone(result["winner"])
                self.assertTrue(result["adjudication_reasons"])

    def test_order_balancing_must_actually_have_happened(self):
        with self.assertRaises(ValidationError):
            resolve(comparisons(functional=2), comparisons(functional=2), presented=(A, A))

    def test_criterion_level_order_conflict_is_reported(self):
        result = resolve(comparisons(functional=2, security=1), comparisons(functional=-2, security=1))
        self.assertIn("security", result["criterion_order_disagreements"])
        self.assertTrue(result["criteria"]["security"]["order_disagreement"])

    def test_identical_teams_are_rejected(self):
        with self.assertRaises(ValidationError):
            matchup.calculate(
                team_a=A, team_b=A,
                a_first={"presented_first": A, "comparisons": comparisons()},
                b_first={"presented_first": A, "comparisons": comparisons()},
                root=ROOT,
            )

    def test_negative_band_is_rejected(self):
        with self.assertRaises(ValidationError):
            resolve(comparisons(), comparisons(), band=-1)


class TieBreakTests(unittest.TestCase):
    def test_functional_breaks_first(self):
        result = resolve(comparisons(functional=1, product=-2), comparisons(functional=-1, product=2))
        self.assertEqual(matchup.tie_break(result, root=ROOT)["step"], "functional")

    def test_reliability_breaks_second(self):
        result = resolve(comparisons(reliability=1), comparisons(reliability=-1))
        broken = matchup.tie_break(result, root=ROOT)
        self.assertEqual(broken["step"], "reliability")
        self.assertEqual(broken["winner"], A)

    def test_exhausted_tie_break_refers_to_a_human(self):
        result = resolve(comparisons(), comparisons())
        broken = matchup.tie_break(result, root=ROOT)
        self.assertFalse(broken["resolved"])
        self.assertIsNone(broken["winner"])


class DeterminismTests(unittest.TestCase):
    def test_same_input_gives_same_result(self):
        values = (comparisons(functional=2, agentic=-1), comparisons(functional=-2, agentic=1))
        self.assertEqual(resolve(*values), resolve(*values))


if __name__ == "__main__":
    unittest.main()
