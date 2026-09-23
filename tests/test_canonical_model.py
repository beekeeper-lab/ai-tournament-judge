"""Stage 1 — the rubric Markdown is the only source of official numbers."""

import re
import unittest
from pathlib import Path

from _support import ROOT  # noqa: F401
from atj import canon, ids, schema, versions
from atj.errors import CanonError, SchemaError, ValidationError, VersionError


class CanonicalRubricTests(unittest.TestCase):
    def setUp(self):
        canon.clear_cache()
        self.rubric = canon.load(ROOT)

    def test_rubric_parses_from_markdown(self):
        self.assertEqual(self.rubric.rubric_id, "submission-evaluation")
        self.assertRegex(self.rubric.version, r"^\d+\.\d+\.\d+$")
        self.assertEqual(self.rubric.total_weight, 100)
        self.assertEqual(len(self.rubric.criteria), 7)
        self.assertEqual(self.rubric.scale_min, 0)
        self.assertEqual(self.rubric.scale_max, 5)

    def test_seven_criteria_and_weights_are_preserved(self):
        self.assertEqual(
            self.rubric.weights,
            {"functional": 25, "product": 15, "agentic": 15,
             "engineering": 15, "reliability": 10, "security": 10, "innovation": 10},
        )

    def test_weighted_points_follow_the_documented_formula(self):
        self.assertEqual(self.rubric.weighted_points(5, "functional"), 25.0)
        self.assertEqual(self.rubric.weighted_points(3, "functional"), 15.0)
        self.assertEqual(self.rubric.weighted_points(0, "innovation"), 0.0)

    def test_ne_is_not_a_numeric_zero(self):
        self.assertEqual(
            self.rubric.validate_score("NE", criterion_id="security"), canon.NOT_ENOUGH_EVIDENCE
        )
        self.assertNotEqual(canon.NOT_ENOUGH_EVIDENCE, 0)

    def test_out_of_range_score_is_rejected(self):
        for value in (-1, 6, 5.5, True, None, "3"):
            with self.assertRaises(CanonError):
                self.rubric.validate_score(value, criterion_id="functional")

    def test_unknown_criterion_is_rejected(self):
        with self.assertRaises(CanonError):
            self.rubric.criterion("velocity")

    def test_rubric_version_mismatch_is_fatal_not_a_warning(self):
        with self.assertRaises(VersionError):
            self.rubric.require_reference("submission-evaluation@9.9.9")
        self.rubric.require_reference(self.rubric.reference)

    def test_weight_total_disagreement_is_fatal(self):
        import tempfile

        text = (ROOT / canon.SUBMISSION_RUBRIC).read_text(encoding="utf-8")
        broken = text.replace("| innovation | Innovation and technical ambition | 10 |",
                              "| innovation | Innovation and technical ambition | 11 |")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rubric.md"
            path.write_text(broken, encoding="utf-8")
            with self.assertRaises(CanonError):
                canon.parse_rubric(path)

    def test_no_second_editable_copy_of_the_official_weights_anywhere(self):
        """Alpha defect X1: DEFAULT_WEIGHTS was an editable duplicate.

        Scans the whole tree, not just Python: a Markdown table or a JSON enum
        would drift from the rubric just as easily as a dict.
        """
        from atj.cli import check_no_duplicate_weights

        self.assertEqual(check_no_duplicate_weights(ROOT), [])

    def test_a_decisive_matchup_margin_is_not_a_weight_copy(self):
        """trial-2-2026: a ±2 value makes the criterion margin equal its weight.

        `"product": 15.0` in an `atj matchup` result is a margin, while
        `"product": 15` is still a copy and must still be caught.
        """
        import shutil
        import tempfile
        from atj.cli import check_no_duplicate_weights

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rubric = root / canon.SUBMISSION_RUBRIC
            rubric.parent.mkdir(parents=True)
            shutil.copy(ROOT / canon.SUBMISSION_RUBRIC, rubric)
            (root / "margin.json").write_text('{"product": 15.0}', encoding="utf-8")
            (root / "copy.json").write_text('{"product": 15}', encoding="utf-8")
            problems = check_no_duplicate_weights(root)
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("copy.json", problems[0])

    def test_retired_scripts_no_longer_define_weights(self):
        for name in ("calculate_scores", "build_bracket", "validate_configuration",
                     "validate_reports", "initialize_event"):
            text = (ROOT / "scripts" / f"{name}.py").read_text(encoding="utf-8")
            self.assertIn("Retired", text, name)
            self.assertNotIn("DEFAULT_WEIGHTS", text, name)

    def test_head_to_head_rubric_parses(self):
        h2h = canon.load_head_to_head(ROOT)
        self.assertEqual(h2h.rubric_id, "head-to-head")
        self.assertEqual(h2h.close_call_band, 5.0)
        # The head-to-head rubric derives from the current submission rubric, and
        # says so rather than naming a version this test has to be edited for.
        self.assertEqual(h2h.source_rubric, canon.load(ROOT).reference)
        with self.assertRaises(VersionError):
            h2h.require_reference("head-to-head@2.0.0")


class IdentifierTests(unittest.TestCase):
    def test_evidence_id_is_derived_and_stable(self):
        first = ids.evidence_package_id("e", "team-a", "a" * 40, ids.content_digest("body"))
        second = ids.evidence_package_id("e", "team-a", "a" * 40, ids.content_digest("body"))
        self.assertEqual(first, second)
        self.assertRegex(first, ids.EVIDENCE_ID)

    def test_changed_evidence_changes_the_identifier(self):
        first = ids.evidence_package_id("e", "team-a", "a" * 40, ids.content_digest("body"))
        changed = ids.evidence_package_id("e", "team-a", "a" * 40, ids.content_digest("body 2"))
        self.assertNotEqual(first, changed)

    def test_composite_identifiers_match_their_patterns(self):
        evidence = ids.evidence_package_id("e", "team-a", "b" * 40, ids.content_digest("x"))
        self.assertRegex(ids.judge_run_id("e", "team-a", "judge-backend", evidence), ids.JUDGE_RUN_ID)
        self.assertRegex(ids.matchup_id("e", "round-of-16", 7), ids.MATCHUP_ID)
        self.assertRegex(ids.adjudication_id("e", "team-a-security", 2), ids.ADJUDICATION_ID)

    def test_invalid_identifiers_are_rejected(self):
        for bad in ("Bad ID", "trailing-", "-leading", "Upper", "two--hyphens", ""):
            with self.assertRaises(ValidationError):
                ids.require_slug(bad, kind="team_id")
        with self.assertRaises(ValidationError):
            ids.require_commit("nothex!!")
        with self.assertRaises(ValidationError):
            ids.require_reference("rubric-without-version", kind="rubric")


class SchemaTests(unittest.TestCase):
    def setUp(self):
        schema.clear_cache()

    def event(self, **overrides):
        base = {
            "event_id": "demo", "event_name": "Demo", "status": "draft",
            "rubric": canon.load(ROOT).reference,
            "consolidation_policy": canon.load_consolidation_policy(ROOT).reference,
            "matchup_rubric": canon.load_head_to_head(ROOT).reference,
            "bracket_policy": "bracket-assignment@1.0.0",
            "bye_policy": "performance-qualified",
            "expected_judges": ["judge-backend", "judge-frontend-ux",
                                "judge-security-ops", "judge-product-agentic"],
            "public_scores": False, "framework_commit": "uncommitted",
            "execution_mode": "disabled",
        }
        base.update(overrides)
        return base

    def test_every_shipped_schema_is_itself_valid(self):
        self.assertEqual(schema.check_schemas(ROOT), [])

    def test_valid_event_passes(self):
        self.assertEqual(schema.validate("event", self.event(), root=ROOT), [])

    def test_alpha_defect_x9_invalid_config_now_fails(self):
        messages = schema.validate(
            "event",
            self.event(event_id="NOT A VALID ID!!", bye_policy="nonsense-policy", expected_judges=7),
            root=ROOT,
        )
        self.assertEqual(len(messages), 3, messages)

    def test_public_report_cannot_carry_private_fields(self):
        public = {
            "event_id": "demo", "visibility": "public", "approval_state": "approved",
            "validation_state": "valid", "approved_by": "official", "source_artifacts": ["x"],
        }
        self.assertEqual(schema.validate("public-report", public, root=ROOT), [])
        for private_field in ("scores", "judge_run_ids", "passes", "comparisons",
                              "blocked_reasons", "evidence_package_id", "adjudication_ids"):
            leaked = dict(public, **{private_field: "anything"})
            self.assertTrue(
                schema.validate("public-report", leaked, root=ROOT),
                f"{private_field} leaked into a public artifact without failing validation",
            )

    def test_schemas_do_not_pin_the_rubric_version(self):
        """Alpha defect X12: judgment.schema.json held a third editable copy."""
        for name in schema.ARTIFACT_SCHEMAS:
            text = str(schema.get_schema(name, ROOT))
            self.assertNotIn(canon.load(ROOT).reference, text, f"{name} pins a rubric version")
            self.assertNotIn("submission-evaluation@", text, f"{name} pins a rubric version")

    def test_schemas_do_not_enumerate_criteria(self):
        for name in schema.ARTIFACT_SCHEMAS:
            text = str(schema.get_schema(name, ROOT))
            for criterion in canon.load(ROOT).criterion_ids:
                self.assertNotIn(f"'{criterion}'", text, f"{name} enumerates rubric criteria")

    def test_require_raises_on_invalid_instance(self):
        with self.assertRaises(SchemaError):
            schema.require("event", {"event_id": "demo"}, root=ROOT)


class PersonaVersionTests(unittest.TestCase):
    def test_registry_matches_the_agent_files(self):
        self.assertEqual(versions.check_personas(ROOT), [])

    def test_every_agent_and_skill_is_registered(self):
        """A component that produces an official artifact must carry a version."""
        registry = set(versions.load_personas(ROOT))
        on_disk = {p.stem for p in (ROOT / versions.AGENT_DIR).glob("*.md")}
        on_disk |= {p.parent.name for p in (ROOT / versions.SKILL_DIR).glob("*/SKILL.md")}
        self.assertEqual(registry, on_disk)

    def test_an_edited_component_fails_until_its_version_is_bumped(self):
        import shutil
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory)
            for item in ("framework", "schemas", ".claude"):
                shutil.copytree(ROOT / item, copy / item)
            agent = copy / versions.AGENT_DIR / "judge-backend.md"
            agent.write_text(agent.read_text(encoding="utf-8") + "\nAn edit.\n", encoding="utf-8")
            problems = versions.check_personas(copy)
            self.assertTrue(any("without a version bump" in p for p in problems), problems)
            with self.assertRaises(VersionError):
                versions.require_personas(copy)

    def test_persona_mismatch_is_fatal(self):
        with self.assertRaises(VersionError):
            versions.require_versions(
                {"rubric": canon.load(ROOT).reference, "persona": "judge-backend@9.9.9"},
                root=ROOT,
            )

    def test_missing_rubric_declaration_is_fatal(self):
        with self.assertRaises(VersionError):
            versions.require_versions({}, root=ROOT)

    def test_matching_versions_pass(self):
        versions.require_versions(
            {"rubric": canon.load(ROOT).reference,
             "persona": versions.load_personas(ROOT)["judge-backend"].reference}, root=ROOT
        )


if __name__ == "__main__":
    unittest.main()
