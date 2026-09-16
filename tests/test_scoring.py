"""Scoring, consolidation, and panel integrity."""

import unittest

from _support import ROOT  # noqa: F401
from atj import canon, scoring
from atj.canon import NOT_ENOUGH_EVIDENCE
from atj.errors import ValidationError, VersionError

RUBRIC = canon.load(ROOT)
PANEL = ("judge-backend", "judge-frontend-ux", "judge-security-ops", "judge-product-agentic")
EVIDENCE = "ev:demo:team-a:" + "a" * 12 + ":deadbeef"


def judgment(judge_id, overrides=None, **kwargs):
    scores = {criterion: 3 for criterion in RUBRIC.criterion_ids}
    scores.update(overrides or {})
    payload = dict(
        judge_id=judge_id,
        judge_run_id=f"jr:demo:team-a:{judge_id}:deadbeef:01",
        team_id="team-a",
        commit="a" * 40,
        evidence_package_id=EVIDENCE,
        rubric=RUBRIC.reference,
        persona=f"{judge_id}@1.0.0",
        scores=scores,
        source=judge_id,
    )
    payload.update(kwargs)
    return scoring.Judgment(**payload)


def panel(overrides_by_judge=None):
    overrides_by_judge = overrides_by_judge or {}
    return [judgment(j, overrides_by_judge.get(j)) for j in PANEL]


class IndividualScoreTests(unittest.TestCase):
    def test_all_fives_is_one_hundred(self):
        result = scoring.individual_score(
            judgment("judge-backend", {c: 5 for c in RUBRIC.criterion_ids}), root=ROOT
        )
        self.assertEqual(result["total"], 100.0)

    def test_all_threes_is_sixty(self):
        self.assertEqual(scoring.individual_score(judgment("judge-backend"), root=ROOT)["total"], 60.0)

    def test_all_zeros_is_zero(self):
        result = scoring.individual_score(
            judgment("judge-backend", {c: 0 for c in RUBRIC.criterion_ids}), root=ROOT
        )
        self.assertEqual(result["total"], 0.0)

    def test_weighted_points_follow_the_rubric_weights(self):
        result = scoring.individual_score(
            judgment("judge-backend", {c: 5 for c in RUBRIC.criterion_ids}), root=ROOT
        )
        for criterion, weight in RUBRIC.weights.items():
            self.assertEqual(result["criteria"][criterion]["weighted_points"], float(weight))

    def test_ne_blocks_the_individual_total(self):
        result = scoring.individual_score(judgment("judge-backend", {"security": "NE"}), root=ROOT)
        self.assertIsNone(result["total"])
        self.assertEqual(result["unresolved_ne"], ["security"])
        self.assertEqual(result["criteria"]["security"]["raw"], NOT_ENOUGH_EVIDENCE)
        # The partial is exposed for transparency but is not a score.
        self.assertEqual(result["partial_total"], 54.0)

    def test_criteria_must_match_the_rubric_exactly(self):
        with self.assertRaises(ValidationError):
            scoring.individual_score(judgment("judge-backend", {"velocity": 3}), root=ROOT)
        missing = dict.fromkeys(list(RUBRIC.criterion_ids)[:-1], 3)
        with self.assertRaises(ValidationError):
            scoring.individual_score(judgment("judge-backend", scores=missing), root=ROOT)

    def test_rubric_version_skew_is_fatal(self):
        with self.assertRaises(VersionError):
            scoring.individual_score(
                judgment("judge-backend", rubric="submission-evaluation@2.0.0"), root=ROOT
            )


class ConsolidationTests(unittest.TestCase):
    def test_aligned_panel_consolidates(self):
        result = scoring.consolidate(panel(), expected_judges=PANEL, root=ROOT)
        self.assertTrue(result["finalized"])
        self.assertEqual(result["total"], 60.0)
        self.assertEqual(result["display_total"], 60.0)
        self.assertEqual(result["blocked_reasons"], [])

    def test_mean_is_the_arithmetic_mean_of_valid_scores(self):
        result = scoring.consolidate(
            panel({"judge-backend": {"functional": 5}, "judge-frontend-ux": {"functional": 4}}),
            expected_judges=PANEL, root=ROOT,
        )
        entry = result["criteria"]["functional"]
        self.assertEqual(entry["mean"], 3.75)
        self.assertEqual(entry["weighted_points"], 18.75)
        self.assertEqual(entry["minimum"], 3.0)
        self.assertEqual(entry["maximum"], 5.0)
        self.assertEqual(entry["range"], 2.0)

    def test_source_scores_are_preserved(self):
        result = scoring.consolidate(
            panel({"judge-backend": {"security": 1}}), expected_judges=PANEL, root=ROOT
        )
        self.assertEqual(
            result["criteria"]["security"]["source_scores"],
            {"judge-backend": 1.0, "judge-frontend-ux": 3.0,
             "judge-security-ops": 3.0, "judge-product-agentic": 3.0},
        )

    def test_agreement_levels_match_the_policy(self):
        cases = {
            0: scoring.ALIGNED, 1: scoring.ALIGNED,
            2: scoring.MATERIAL, 3: scoring.SEVERE, 5: scoring.SEVERE,
        }
        for spread, expected in cases.items():
            overrides = {judge: {"functional": 0} for judge in PANEL}
            overrides["judge-backend"] = {"functional": spread}
            result = scoring.consolidate(
                panel(overrides), expected_judges=PANEL, root=ROOT
            )
            self.assertEqual(result["criteria"]["functional"]["agreement"], expected, spread)

    def test_possible_outlier_is_detected(self):
        result = scoring.consolidate(
            panel({"judge-backend": {"innovation": 5}}), expected_judges=PANEL, root=ROOT
        )
        entry = result["criteria"]["innovation"]
        self.assertEqual(entry["possible_outliers"], ["judge-backend"])
        self.assertIn(
            {"criterion": "innovation", "trigger": "possible-outlier"},
            result["adjudication_required"],
        )

    def test_severe_disagreement_requires_adjudication(self):
        result = scoring.consolidate(
            panel({"judge-backend": {"functional": 0}, "judge-frontend-ux": {"functional": 5}}),
            expected_judges=PANEL, root=ROOT,
        )
        self.assertIn(
            {"criterion": "functional", "trigger": "severe-disagreement"},
            result["adjudication_required"],
        )

    def test_unresolved_ne_blocks_finalization(self):
        result = scoring.consolidate(
            panel({"judge-security-ops": {"security": "NE"}}), expected_judges=PANEL, root=ROOT
        )
        self.assertFalse(result["finalized"])
        self.assertIsNone(result["total"])
        self.assertIsNone(result["display_total"])
        self.assertTrue(result["blocked_reasons"])
        self.assertIn(
            {"criterion": "security", "trigger": "unresolved-ne"}, result["adjudication_required"]
        )

    def test_ne_is_not_averaged_as_zero(self):
        with_ne = scoring.consolidate(
            panel({"judge-security-ops": {"security": "NE"}}), expected_judges=PANEL, root=ROOT
        )
        self.assertEqual(with_ne["criteria"]["security"]["mean"], 3.0)
        self.assertEqual(with_ne["criteria"]["security"]["ne_judges"], ["judge-security-ops"])

    def test_adjudicated_resolution_never_edits_a_source_score(self):
        result = scoring.consolidate(
            panel({"judge-backend": {"security": 1}}), expected_judges=PANEL, root=ROOT,
            resolutions={"security": {"resolved_score": 3, "rationale": "evidence located"}},
        )
        self.assertEqual(result["criteria"]["security"]["source_scores"]["judge-backend"], 1.0)
        self.assertIsNotNone(result["criteria"]["security"]["resolution"])

    def test_consolidation_is_order_independent(self):
        forward = scoring.consolidate(panel(), expected_judges=PANEL, root=ROOT)
        backward = scoring.consolidate(list(reversed(panel())), expected_judges=PANEL, root=ROOT)
        self.assertEqual(forward, backward)

    def test_consolidation_is_repeatable(self):
        first = scoring.consolidate(panel(), expected_judges=PANEL, root=ROOT)
        second = scoring.consolidate(panel(), expected_judges=PANEL, root=ROOT)
        self.assertEqual(first, second)


class PanelIntegrityTests(unittest.TestCase):
    def test_single_judge_panel_is_rejected(self):
        problems = scoring.check_panel_integrity(
            [judgment("judge-backend")], expected_judges=PANEL, root=ROOT
        )
        self.assertTrue(any("at least" in p for p in problems))

    def test_duplicate_judge_is_rejected(self):
        problems = scoring.check_panel_integrity(
            [judgment("judge-backend") for _ in range(4)], expected_judges=PANEL, root=ROOT
        )
        self.assertTrue(any("must be distinct" in p for p in problems))

    def test_reused_report_is_detected(self):
        first = judgment("judge-backend")
        second = judgment("judge-frontend-ux", judge_run_id=first.judge_run_id)
        problems = scoring.check_panel_integrity([first, second], root=ROOT)
        self.assertTrue(any("reports were reused" in p for p in problems))

    def test_missing_configured_judge_is_reported(self):
        problems = scoring.check_panel_integrity(
            panel()[:3], expected_judges=PANEL, root=ROOT
        )
        self.assertTrue(any("produced no judgment" in p for p in problems))

    def test_unconfigured_judge_is_reported(self):
        problems = scoring.check_panel_integrity(
            panel() + [judgment("judge-uninvited")], expected_judges=PANEL, root=ROOT
        )
        self.assertTrue(any("unconfigured judge" in p for p in problems))

    def test_judges_must_have_evaluated_the_same_thing(self):
        mixed = panel()
        mixed[0] = judgment("judge-backend", commit="b" * 40)
        problems = scoring.check_panel_integrity(mixed, expected_judges=PANEL, root=ROOT)
        self.assertTrue(any("submission commit" in p for p in problems))

    def test_integrity_failure_blocks_finalization(self):
        result = scoring.consolidate(panel()[:1], expected_judges=PANEL, root=ROOT)
        self.assertFalse(result["finalized"])
        self.assertIsNone(result["total"])


class ThresholdSourceTests(unittest.TestCase):
    def test_thresholds_come_from_the_consolidation_policy(self):
        policy = canon.load_consolidation_policy(ROOT)
        thresholds = scoring._thresholds(ROOT)
        self.assertEqual(thresholds["aligned_max_range"], int(policy.metadata["aligned_max_range"]))
        self.assertEqual(thresholds["material_max_range"], int(policy.metadata["material_max_range"]))
        self.assertEqual(thresholds["outlier_distance"], int(policy.metadata["outlier_distance"]))
        self.assertEqual(thresholds["minimum_panel"], int(policy.metadata["minimum_panel"]))


if __name__ == "__main__":
    unittest.main()
