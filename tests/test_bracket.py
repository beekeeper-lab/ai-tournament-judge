"""Bracket assignment: shape, hard constraints, reproducibility, infeasibility.

The alpha implementation passed a four-test suite that only ever built one
20-team bracket with one seed. These tests sweep every supported size, every bye
policy, and many seeds, because that is where its two constraint defects lived.
"""

import unittest

from _support import ROOT  # noqa: F401
from atj import bracket, schema
from atj.errors import ConstraintError, ValidationError

SIZES = range(bracket.MIN_TEAMS, bracket.MAX_TEAMS + 1)
SEEDS = [f"seed-{index}" for index in range(8)]


def roster(count, groups=5, finalists=True, scores=True, bands=True):
    teams = []
    for index in range(count):
        team = {
            "id": f"team-{index:02d}",
            "affiliation_group": f"school-{index % groups}",
            "previous_result": "none",
        }
        if scores:
            team["score"] = 100 - index
        if bands:
            team["band"] = f"band-{index // 4}"
        teams.append(team)
    if finalists and count >= 2:
        teams[0]["previous_result"] = "champion"
        teams[1]["previous_result"] = "runner-up"
    return teams


def build(count, seed="seed-0", policy="performance-qualified", **kwargs):
    return bracket.build(
        event_id="demo", teams=roster(count, **kwargs), seed=seed, bye_policy=policy, root=ROOT
    )


def constraint(result, prefix):
    for entry in result["constraint_audit"]:
        if entry["constraint"].startswith(prefix):
            return entry
    raise AssertionError(f"no constraint starting with {prefix!r}")


class ShapeTests(unittest.TestCase):
    def test_every_supported_size_produces_a_valid_bracket(self):
        for count in SIZES:
            with self.subTest(count=count):
                result = build(count)
                self.assertEqual(bracket.verify(result), [])
                self.assertEqual(schema.validate("bracket", result, root=ROOT), [])

    def test_each_team_appears_exactly_once(self):
        for count in SIZES:
            result = build(count)
            placed = [
                entrant for match in result["rounds"][0]["matches"]
                for entrant in match["entrants"] if entrant
            ]
            self.assertEqual(len(placed), count)
            self.assertEqual(len(set(placed)), count)

    def test_bracket_size_is_the_next_power_of_two(self):
        self.assertEqual(bracket.bracket_size(2), 2)
        self.assertEqual(bracket.bracket_size(3), 4)
        self.assertEqual(bracket.bracket_size(17), 32)
        self.assertEqual(bracket.bracket_size(32), 32)

    def test_full_round_structure_is_generated(self):
        result = build(20)
        self.assertEqual(
            [entry["round_id"] for entry in result["rounds"]],
            ["preliminary", "round-of-16", "quarterfinal", "semifinal", "final"],
        )
        self.assertEqual(len(result["rounds"][-1]["matches"]), 1)

    def test_twenty_team_bracket_matches_the_documented_shape(self):
        result = build(20)
        first = result["rounds"][0]["matches"]
        self.assertEqual(result["bracket_size"], 32)
        self.assertEqual(result["bye_count"], 12)
        self.assertEqual(sum(1 for match in first if match["bye"]), 12)
        self.assertEqual(sum(1 for match in first if not match["bye"]), 4)
        self.assertEqual(sum(2 for match in first if not match["bye"]), 8)

    def test_out_of_range_team_counts_are_rejected(self):
        for count in (0, 1, 33, 64):
            with self.assertRaises(ValidationError):
                bracket.build(event_id="demo", teams=roster(max(count, 0)), seed="s", root=ROOT)


class HardConstraintTests(unittest.TestCase):
    def test_previous_finalists_never_share_a_half_avoidably(self):
        """Alpha defect X2: broken at every size except a 32-slot bracket."""
        for count in SIZES:
            for policy in bracket.BYE_POLICIES:
                for seed in SEEDS:
                    result = build(count, seed=seed, policy=policy)
                    entry = constraint(result, "Previous champion")
                    self.assertNotEqual(
                        entry["status"], "violated",
                        f"n={count} {policy} {seed}: {entry['detail']}",
                    )

    def test_no_avoidable_same_affiliation_first_round_match(self):
        """Alpha defect X3: greedy pairing stranded same-group teams."""
        for count in SIZES:
            for groups in (2, 3, 5):
                for seed in SEEDS:
                    result = build(count, seed=seed, policy="random-lottery", groups=groups)
                    entry = constraint(result, "No avoidable")
                    self.assertNotEqual(
                        entry["status"], "violated",
                        f"n={count} groups={groups} {seed}: {entry['exceptions']}",
                    )

    def test_a_feasible_bracket_reports_no_unsatisfied_hard_constraints(self):
        for count in SIZES:
            result = build(count)
            if result["feasible"]:
                self.assertEqual(result["unsatisfied_hard_constraints"], [])

    def test_every_constraint_reports_a_status(self):
        result = build(20)
        self.assertGreaterEqual(len(result["constraint_audit"]), 6)
        for entry in result["constraint_audit"]:
            self.assertIn(entry["status"], (
                "satisfied", "maximized", "violated", "not-applicable", "infeasible"
            ))
            self.assertTrue(entry["detail"])


class InfeasibilityTests(unittest.TestCase):
    def test_single_affiliation_field_is_reported_not_hidden(self):
        teams = [
            {"id": f"team-{index:02d}", "affiliation_group": "only-school",
             "previous_result": "none"}
            for index in range(8)
        ]
        result = bracket.build(
            event_id="demo", teams=teams, seed="s", bye_policy="random-lottery", root=ROOT
        )
        entry = constraint(result, "No avoidable")
        self.assertEqual(entry["status"], "infeasible")
        self.assertFalse(result["feasible"])
        self.assertTrue(entry["exceptions"])

    def test_two_finalists_alone_in_a_two_team_event_is_infeasible(self):
        result = build(2)
        self.assertEqual(constraint(result, "Previous champion")["status"], "infeasible")
        self.assertFalse(result["feasible"])

    def test_pairing_feasibility_is_computed_correctly(self):
        entrants = [bracket.Entrant.from_dict(team) for team in roster(4, groups=1)]
        feasible, reason = bracket.pairing_feasible(entrants)
        self.assertFalse(feasible)
        self.assertIn("holds", reason)
        entrants = [bracket.Entrant.from_dict(team) for team in roster(4, groups=2, finalists=False)]
        self.assertTrue(bracket.pairing_feasible(entrants)[0])

    def test_no_finalists_marks_the_constraint_not_applicable(self):
        result = build(12, finalists=False)
        self.assertEqual(constraint(result, "Previous champion")["status"], "not-applicable")


class PolicyTests(unittest.TestCase):
    def test_unknown_bye_policy_is_rejected_even_with_zero_byes(self):
        """Alpha defect X5: the policy check ran after an early return."""
        with self.assertRaises(ValidationError):
            bracket.build(event_id="demo", teams=roster(4), seed="s", bye_policy="bogus", root=ROOT)
        with self.assertRaises(ValidationError):
            bracket.build(event_id="demo", teams=roster(20), seed="s", bye_policy="bogus", root=ROOT)

    def test_performance_byes_go_to_the_highest_scores(self):
        result = build(20, policy="performance-qualified")
        self.assertEqual(set(result["bye_teams"]), {f"team-{index:02d}" for index in range(12)})

    def test_performance_byes_require_scores(self):
        with self.assertRaises(ValidationError):
            bracket.build(
                event_id="demo", teams=roster(20, scores=False), seed="s",
                bye_policy="performance-qualified", root=ROOT,
            )

    def test_banded_lottery_requires_bands(self):
        with self.assertRaises(ValidationError):
            bracket.build(
                event_id="demo", teams=roster(20, bands=False), seed="s",
                bye_policy="banded-lottery", root=ROOT,
            )

    def test_every_declared_policy_is_supported(self):
        for policy in bracket.BYE_POLICIES:
            result = build(20, policy=policy)
            self.assertEqual(result["bye_policy"], policy)
            self.assertEqual(len(result["bye_teams"]), 12)

    def test_default_bye_policy_is_performance_qualified(self):
        self.assertEqual(bracket.DEFAULT_BYE_POLICY, "performance-qualified")


class ReproducibilityTests(unittest.TestCase):
    def test_same_seed_reproduces_byte_for_byte(self):
        for count in (4, 11, 20, 32):
            self.assertEqual(build(count, seed="fixed"), build(count, seed="fixed"))

    def test_different_seed_generally_differs(self):
        differences = sum(
            1 for seed in SEEDS
            if build(20, seed=seed)["rounds"] != build(20, seed="seed-0")["rounds"]
        )
        self.assertGreater(differences, 0)

    def test_seed_must_be_supplied_and_recorded(self):
        with self.assertRaises(ValidationError):
            bracket.build(event_id="demo", teams=roster(8), seed="", root=ROOT)
        self.assertEqual(build(8, seed="written-down")["seed"], "written-down")

    def test_input_digest_changes_when_any_input_changes(self):
        base = build(20)["input_digest"]
        self.assertEqual(build(20)["input_digest"], base)
        changed = roster(20)
        changed[5]["score"] = 1
        self.assertNotEqual(
            bracket.build(event_id="demo", teams=changed, seed="seed-0", root=ROOT)["input_digest"],
            base,
        )
        self.assertNotEqual(build(20, seed="other")["input_digest"], base)
        self.assertNotEqual(build(20, policy="random-lottery")["input_digest"], base)


class RosterValidationTests(unittest.TestCase):
    def test_duplicate_team_id_is_rejected(self):
        teams = roster(8)
        teams[1]["id"] = teams[0]["id"]
        with self.assertRaises(ValidationError):
            bracket.build(event_id="demo", teams=teams, seed="s", root=ROOT)

    def test_two_champions_is_rejected(self):
        teams = roster(8)
        teams[2]["previous_result"] = "champion"
        with self.assertRaises(ValidationError):
            bracket.build(event_id="demo", teams=teams, seed="s", root=ROOT)

    def test_invalid_team_id_is_rejected(self):
        teams = roster(8)
        teams[0]["id"] = "Team Zero!"
        with self.assertRaises(ValidationError):
            bracket.build(event_id="demo", teams=teams, seed="s", root=ROOT)

    def test_unknown_previous_result_is_rejected(self):
        teams = roster(8)
        teams[3]["previous_result"] = "semifinalist"
        with self.assertRaises(ValidationError):
            bracket.build(event_id="demo", teams=teams, seed="s", root=ROOT)


class MeetingRoundTests(unittest.TestCase):
    def test_adjacent_slots_meet_in_round_two(self):
        self.assertEqual(bracket.meeting_round(0, 1, 16), 2)

    def test_opposite_halves_meet_in_the_final(self):
        self.assertEqual(bracket.meeting_round(0, 15, 16), 5)
        self.assertEqual(bracket.meeting_round(0, 8, 16), 5)

    def test_meeting_round_scales_with_bracket_size(self):
        """The alpha code hard-coded //8 as 'half', true only for 16 units."""
        self.assertEqual(bracket.meeting_round(0, 1, 2), 2)
        self.assertEqual(bracket.meeting_round(0, 2, 4), 3)
        self.assertEqual(bracket.meeting_round(0, 4, 8), 4)


if __name__ == "__main__":
    unittest.main()
