"""Regressions for defects found by the independent Stage 1 audits.

Each test names the finding it locks down. They exist because every one of these
passed the previous test suite.
"""

import copy
import json
import tempfile
import unittest
from pathlib import Path

from _support import ROOT  # noqa: F401
from atj import bracket, canon, frontmatter, matchup, publication, scoring, versions
from atj.errors import AtjError, ValidationError, VersionError

RUBRIC = canon.load(ROOT)
PANEL = ("judge-backend", "judge-frontend-ux", "judge-security-ops", "judge-product-agentic")


def comparisons(**values):
    return {criterion: values.get(criterion, 0) for criterion in RUBRIC.criterion_ids}


class CloseCallBandTests(unittest.TestCase):
    """B1: narrowing the band turned human-review results into auto-advancement."""

    def resolve(self, band=None):
        return matchup.calculate(
            team_a="team-a", team_b="team-b",
            a_first={"presented_first": "team-a", "comparisons": comparisons(security=1)},
            b_first={"presented_first": "team-b", "comparisons": comparisons(security=-1)},
            close_call_band=band, root=ROOT,
        )

    def test_the_rubric_band_is_a_floor(self):
        canonical = canon.load_head_to_head(ROOT).close_call_band
        for narrow in (0, 1, canonical - 0.1, -5):
            with self.assertRaises(ValidationError, msg=narrow):
                self.resolve(narrow)

    def test_widening_is_allowed(self):
        self.assertEqual(self.resolve(30)["close_call_band"], 30.0)

    def test_a_margin_on_the_band_still_requires_adjudication(self):
        result = self.resolve()
        self.assertEqual(result["combined_margin"], 5.0)
        self.assertEqual(result["outcome"], matchup.ADJUDICATION_REQUIRED)
        self.assertIsNone(result["winner"])

    def test_version_check_rejects_a_narrowed_band(self):
        for narrow in (0, 1, 4.9, -3):
            with self.assertRaises(VersionError, msg=narrow):
                versions.require_versions(
                    {"rubric": "head-to-head@1.0.0", "close_call_band": narrow}, root=ROOT
                )

    def test_a_band_above_the_maximum_margin_is_rejected(self):
        with self.assertRaises(ValidationError):
            self.resolve(101)


class FinalistConflictTests(unittest.TestCase):
    """M1: a finalist pair that also shared a group lost its hard penalty."""

    def roster(self, count):
        teams = [
            {"id": f"t{index:02d}", "affiliation_group": "north" if index < 2 else f"s{index % 4}",
             "previous_result": "none", "score": 100 - index}
            for index in range(count)
        ]
        teams[0]["previous_result"] = "champion"
        teams[1]["previous_result"] = "runner-up"
        return teams

    def test_conflict_reasons_reports_every_reason(self):
        champion = bracket.Entrant("a", "north", "champion")
        runner_up = bracket.Entrant("b", "north", "runner-up")
        reasons = bracket.conflict_reasons(champion, runner_up)
        self.assertIn("affiliation north", reasons)
        self.assertIn(bracket.FINALIST_REASON, reasons)

    def test_finalists_sharing_a_group_are_still_separated(self):
        for count in (5, 6, 8, 12, 16, 20, 32):
            for index in range(6):
                result = bracket.build(
                    event_id="demo", teams=self.roster(count), seed=f"seed-{index}",
                    bye_policy="random-lottery", root=ROOT,
                )
                entry = next(e for e in result["constraint_audit"]
                             if e["constraint"].startswith("Previous champion"))
                self.assertNotEqual(entry["status"], "violated", f"n={count} seed-{index}")


class ByePolicyAuditTests(unittest.TestCase):
    """M7: the bye-policy constraint asserted satisfaction instead of checking it."""

    def roster(self):
        teams = [
            {"id": f"t{index:02d}", "affiliation_group": f"s{index % 4}",
             "previous_result": "none", "score": 100 - index * 3}
            for index in range(6)
        ]
        teams[0]["previous_result"] = "champion"
        teams[1]["previous_result"] = "runner-up"
        return teams

    def test_a_tampered_bye_is_caught(self):
        teams = self.roster()
        good = bracket.build(event_id="demo", teams=teams, seed="s",
                             bye_policy="performance-qualified", root=ROOT)
        self.assertEqual(bracket.verify(good, teams), [])

        tampered = copy.deepcopy(good)
        top, bottom = "t00", "t05"
        for match in tampered["rounds"][0]["matches"]:
            entrants = match["entrants"]
            if match["bye"] and entrants[0] == top:
                entrants[0] = bottom
                match["winner"] = bottom
            elif not match["bye"] and bottom in entrants:
                entrants[entrants.index(bottom)] = top
        self.assertTrue(bracket.verify(tampered, teams))

    def test_verify_without_a_roster_cannot_re_derive_and_says_nothing_false(self):
        teams = self.roster()
        good = bracket.build(event_id="demo", teams=teams, seed="s",
                             bye_policy="performance-qualified", root=ROOT)
        self.assertEqual(bracket.verify(good), [])

    def test_bye_policies_come_from_the_canonical_policy_file(self):
        """M2: the policy list was a third editable copy."""
        declared = canon.load_bracket_policy(ROOT).metadata["bye_policies"]
        self.assertEqual(list(bracket.bye_policies(ROOT)), list(declared))
        self.assertEqual(
            bracket.default_bye_policy(ROOT),
            canon.load_bracket_policy(ROOT).metadata["default_bye_policy"],
        )


class NestedPrivateFieldTests(unittest.TestCase):
    """M4: the public field ban was top-level only."""

    BASE = {
        "event_id": "demo", "visibility": "public", "approval_state": "approved",
        "approved_by": "official", "source_artifacts": ["matchups/x.md"],
    }

    def test_a_nested_mapping_cannot_smuggle_private_fields(self):
        metadata = dict(self.BASE, panel={
            "scores": {"functional": 5}, "judge_id": "judge-backend",
            "judge_run_id": "jr:demo:team-a:judge-backend:deadbeef:01", "total": 91.5,
        })
        findings = publication.check_public(metadata, "# Summary\n\nText.\n")
        banned = {f.detail.split("'")[1] for f in findings if f.rule == "private-field"}
        self.assertTrue({"scores", "judge_id", "judge_run_id", "total"} <= banned, banned)

    def test_a_field_inside_a_list_is_also_caught(self):
        metadata = dict(self.BASE, rounds=[{"matches": [{"scores": {"functional": 4}}]}])
        findings = publication.check_public(metadata, "# Summary\n\nText.\n")
        self.assertTrue(any(f.rule == "private-field" for f in findings))

    def test_a_credential_in_metadata_is_caught(self):
        metadata = dict(self.BASE, note="key AKIAIOSFODNN7EXAMPLE")
        findings = publication.check_public(metadata, "# Summary\n\nText.\n")
        self.assertTrue(any(f.rule == "secret" for f in findings))


class PublicationGateFailsClosedTests(unittest.TestCase):
    """m1: an unrecognised location reported CLEAR on a file full of secrets."""

    def test_unknown_location_blocks(self):
        findings = publication.check_artifact(
            Path("/elsewhere/report.md"), Path("/events/demo"),
            {"visibility": "public"}, "AKIAIOSFODNN7EXAMPLE",
        )
        self.assertTrue(findings)
        self.assertEqual(findings[0].rule, "location-unknown")
        self.assertEqual(findings[0].severity, "blocking")

    def test_a_nested_public_path_is_still_recognised(self):
        event_dir = Path("/events/demo")
        self.assertEqual(
            publication.expected_visibility(event_dir / "public" / "round1" / "x.md", event_dir),
            "public",
        )


class DisagreementBlocksFinalizationTests(unittest.TestCase):
    """m2: a severe disagreement produced a clean official total."""

    def judgment(self, judge_id, functional):
        scores = {criterion: 3 for criterion in RUBRIC.criterion_ids}
        scores["functional"] = functional
        return scoring.Judgment(
            judge_id=judge_id, judge_run_id=f"jr:e:t:{judge_id}:deadbeef:01",
            team_id="t", commit="a" * 40,
            evidence_package_id="ev:e:t:" + "a" * 12 + ":deadbeef",
            rubric=RUBRIC.reference, persona=f"{judge_id}@1.0.0", scores=scores, source=judge_id,
        )

    def panel(self, values):
        return [self.judgment(judge, value) for judge, value in zip(PANEL, values)]

    def test_severe_disagreement_blocks_until_adjudicated(self):
        result = scoring.consolidate(self.panel([0, 4, 4, 5]), expected_judges=PANEL, root=ROOT)
        self.assertFalse(result["finalized"])
        self.assertIsNone(result["total"])
        self.assertIsNone(result["display_total"])
        self.assertTrue(any("severe disagreement" in r for r in result["blocked_reasons"]))

    def test_a_possible_outlier_blocks_until_adjudicated(self):
        result = scoring.consolidate(self.panel([5, 3, 3, 3]), expected_judges=PANEL, root=ROOT)
        self.assertFalse(result["finalized"])
        self.assertTrue(any("possible outlier" in r for r in result["blocked_reasons"]))

    def test_a_recorded_resolution_unblocks_it(self):
        result = scoring.consolidate(
            self.panel([0, 4, 4, 5]), expected_judges=PANEL, root=ROOT,
            resolutions={"functional": {"resolved_score": None, "rationale": "reviewed"}},
        )
        self.assertTrue(result["finalized"])
        self.assertIsNotNone(result["total"])

    def test_an_aligned_panel_is_unaffected(self):
        self.assertTrue(
            scoring.consolidate(self.panel([3, 3, 3, 3]), expected_judges=PANEL, root=ROOT)["finalized"]
        )


class YamlBombTests(unittest.TestCase):
    """M8: a 284-byte alias bomb took 69 seconds to parse."""

    def bomb(self, depth):
        lines = ["a: &a [1,1,1,1,1,1,1,1,1]"]
        previous = "a"
        for index in range(depth):
            name = f"n{index}"
            lines.append(f"{name}: &{name} [" + ",".join([f"*{previous}"] * 9) + "]")
            previous = name
        return "---\n" + "\n".join(lines) + "\n---\nbody\n"

    def test_an_alias_bomb_is_refused_immediately(self):
        import time

        started = time.monotonic()
        with self.assertRaises(ValidationError):
            frontmatter.split(self.bomb(8))
        self.assertLess(time.monotonic() - started, 1.0)

    def test_ordinary_front_matter_still_parses(self):
        metadata, _ = frontmatter.split(
            "---\nevent_id: demo\nlist: [a, b]\nnested:\n  key: value\n---\nbody\n"
        )
        self.assertEqual(metadata["nested"]["key"], "value")

    def test_python_object_tags_are_still_refused(self):
        with self.assertRaises(ValidationError):
            frontmatter.split("---\n!!python/object/apply:os.system ['echo hi']\n---\nbody\n")


class RosterShadowingTests(unittest.TestCase):
    """M6: a `teams:` list in front matter silently replaced the reviewed table."""

    def test_declaring_both_is_an_error(self):
        from atj import event as event_module

        with tempfile.TemporaryDirectory() as directory:
            event_dir = Path(directory) / "demo"
            event_dir.mkdir()
            for name in ("event.md", "status.md", "bracket.md"):
                (event_dir / name).write_text("---\nevent_id: demo\n---\nbody\n", encoding="utf-8")
            (event_dir / "teams.md").write_text(
                "---\nevent_id: demo\nteams:\n  - id: ghost-team\n    display_name: Ghost\n"
                "    eligible: true\n---\n\n"
                "| Team ID | Display name | Affiliation group | Previous result | Submission status | Eligible |\n"
                "|---|---|---|---|---|---|\n"
                "| team-real | Real | school | none | received | yes |\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValidationError):
                event_module.load(event_dir, root=ROOT)


class VersionSkewTests(unittest.TestCase):
    """M3: template rubric literals were never resolved against the canon."""

    def test_release_check_resolves_every_declared_version(self):
        from atj.cli import check_declared_versions

        self.assertEqual(check_declared_versions(ROOT), [])

    def test_a_bumped_rubric_is_detected(self):
        import shutil

        from atj.cli import check_declared_versions

        with tempfile.TemporaryDirectory() as directory:
            copy_root = Path(directory)
            for item in ("framework", "schemas", "events", ".claude"):
                shutil.copytree(ROOT / item, copy_root / item)
            rubric = copy_root / canon.SUBMISSION_RUBRIC
            current = canon.load(ROOT).version
            rubric.write_text(
                rubric.read_text(encoding="utf-8").replace(
                    f"version: {current}", "version: 9.9.9", 1
                ),
                encoding="utf-8",
            )
            canon.clear_cache()
            problems = check_declared_versions(copy_root)
            canon.clear_cache()
            self.assertTrue(problems)
            self.assertTrue(any("rubric mismatch" in problem for problem in problems))


class TieBreakSourceTests(unittest.TestCase):
    """m3: the tie-break order was a hard-coded copy."""

    def test_order_comes_from_the_rubric(self):
        declared = canon.load_head_to_head(ROOT).tie_break_order
        self.assertEqual(matchup.tie_break_order(ROOT), declared)
        self.assertEqual(declared[0], "functional")


if __name__ == "__main__":
    unittest.main()
