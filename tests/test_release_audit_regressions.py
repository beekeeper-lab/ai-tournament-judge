"""Regressions for the second independent release audit.

Each names the finding it locks down. All of these passed the 288-test suite.
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from _support import ROOT  # noqa: F401
from atj import bracket, ceremony, demo, event as event_module, frontmatter, publication, reports, scoring
from atj.cli import main as cli_main
from atj.errors import AtjError, StateError, ValidationError

EVENT_DIR = ROOT / "events" / demo.EVENT_ID


def copy_event():
    holder = Path(tempfile.mkdtemp())
    shutil.copytree(EVENT_DIR, holder / "event")
    return holder, holder / "event"


class ForgedAdjudicationTests(unittest.TestCase):
    """F1: one adjudication file could move any team's official total."""

    def forge(self, event_dir, **overrides):
        source = next((event_dir / "adjudications").glob("*team-lumen-security*"))
        metadata, body = frontmatter.read(source)
        metadata.update(overrides)
        target = event_dir / "adjudications" / "forged.md"
        target.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
        return target

    def resolutions(self, event_dir, team="team-lumen"):
        return scoring.load_resolutions(
            event_dir / "adjudications", team_id=team, root=ROOT
        )

    def test_a_record_for_another_team_is_ignored(self):
        holder, event_dir = copy_event()
        try:
            self.forge(event_dir, team_id="team-quill",
                       score_override={"criterion": "security", "resolved_score": 5,
                                       "rationale": "x"})
            self.assertEqual(
                [r["resolved_score"] for r in self.resolutions(event_dir).values()], [2]
            )
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_an_unscoped_record_is_ignored(self):
        holder, event_dir = copy_event()
        try:
            self.forge(event_dir, team_id=None, scope="matchup",
                       score_override={"criterion": "security", "resolved_score": 5,
                                       "rationale": "x"})
            self.assertEqual(
                [r["resolved_score"] for r in self.resolutions(event_dir).values()], [2]
            )
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_a_criterion_record_carrying_a_match_id_is_fatal(self):
        holder, event_dir = copy_event()
        try:
            self.forge(event_dir, match_id="mu:sample-mock-2026:final:01")
            with self.assertRaises(ValidationError):
                self.resolutions(event_dir)
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_two_resolutions_for_one_criterion_is_a_conflict(self):
        holder, event_dir = copy_event()
        try:
            self.forge(event_dir, adjudication_id="adj:sample-mock-2026:team-lumen-security:02")
            with self.assertRaises(ValidationError):
                self.resolutions(event_dir)
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_loading_resolutions_without_a_team_is_refused(self):
        with self.assertRaises(ValidationError):
            scoring.load_resolutions(EVENT_DIR / "adjudications", root=ROOT)

    def test_the_genuine_adjudication_still_applies(self):
        self.assertEqual(
            [r["resolved_score"] for r in self.resolutions(EVENT_DIR).values()], [2]
        )


class ForcePathTests(unittest.TestCase):
    """F3: `--force-reason ""` advanced a stage and recorded nothing."""

    def event(self):
        holder = Path(tempfile.mkdtemp())
        for item in ("framework", "schemas", "events", ".claude"):
            shutil.copytree(ROOT / item, holder / item)
        directory = event_module.initialize("probe-2026", root=holder)
        return holder, event_module.load(directory, root=holder)

    def test_an_empty_reason_does_not_advance(self):
        holder, loaded = self.event()
        try:
            for reason in ("", "  ", "\n"):
                with self.assertRaises(StateError):
                    event_module.advance(loaded, force_reason=reason, force_approver="x")
            self.assertEqual(loaded.stage, "configuration")
            self.assertEqual(loaded.status.get("overrides", []), [])
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_an_override_needs_a_named_approver(self):
        holder, loaded = self.event()
        try:
            with self.assertRaises(StateError):
                event_module.advance(loaded, force_reason="waived")
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_an_override_records_what_it_bypassed(self):
        holder, loaded = self.event()
        try:
            event_module.advance(loaded, force_reason="official waived", force_approver="head")
            record = loaded.status["overrides"][0]
            self.assertEqual(record["from"], "configuration")
            self.assertEqual(record["authorized_by"], "head")
            self.assertTrue(record["bypassed"])
        finally:
            shutil.rmtree(holder, ignore_errors=True)


class GateScopeTests(unittest.TestCase):
    """F8: an audit from any event and any stage authorized a gate."""

    def test_an_audit_from_another_event_is_refused(self):
        problems = event_module.audit_supports_gate(
            EVENT_DIR / "audits" / "bracket.md", stage="bracket", root=ROOT,
            event_id="some-other-event",
        )
        self.assertTrue(any("audits event" in problem for problem in problems))

    def test_an_audit_of_another_stage_is_refused(self):
        problems = event_module.audit_supports_gate(
            EVENT_DIR / "audits" / "bracket.md", stage="dossiers", root=ROOT,
            event_id=demo.EVENT_ID,
        )
        self.assertTrue(any("does not name" in problem for problem in problems))

    def test_the_matching_audit_passes(self):
        self.assertEqual(
            event_module.audit_supports_gate(
                EVENT_DIR / "audits" / "bracket.md", stage="bracket", root=ROOT,
                event_id=demo.EVENT_ID,
            ),
            [],
        )


class StaleBlocksAdvanceTests(unittest.TestCase):
    """F11: `event status` said stale and `event advance` proceeded anyway."""

    def test_a_stale_unit_blocks_advancement(self):
        holder, event_dir = copy_event()
        try:
            path = event_dir / "judgments" / "team-lumen" / "judge-backend.md"
            path.write_text(path.read_text(encoding="utf-8") + "\nedit\n", encoding="utf-8")
            loaded = event_module.load(event_dir, root=ROOT)
            loaded.status["current_stage"] = "consolidation"
            allowed, reasons = event_module.can_advance(loaded)
            self.assertFalse(allowed)
            self.assertTrue(any("inputs changed" in reason for reason in reasons))
        finally:
            shutil.rmtree(holder, ignore_errors=True)


class AdvancementIntegrityTests(unittest.TestCase):
    """F4 and F9: the winner came from prose and source matches went unchecked."""

    def test_the_advancing_team_comes_from_a_structured_field(self):
        path = next((EVENT_DIR / "adjudications").glob("*close-call*"))
        metadata, _ = frontmatter.read(path)
        self.assertEqual(metadata["advances_team"], "team-quill")

    def test_an_adjudication_without_the_field_is_refused(self):
        holder, event_dir = copy_event()
        try:
            path = next((event_dir / "adjudications").glob("*close-call*"))
            metadata, body = frontmatter.read(path)
            metadata["impact"] = "team-harbor does not advance; team-quill advances"
            metadata.pop("advances_team")
            path.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
            drawn = json.loads((event_dir / "bracket.json").read_text(encoding="utf-8"))
            for entry in drawn["rounds"]:
                for match in entry["matches"]:
                    match["winner"] = None
            (event_dir / "bracket.json").write_text(json.dumps(drawn), encoding="utf-8")
            self.assertEqual(cli_main([
                "--root", str(ROOT), "bracket", "advance", str(event_dir / "bracket.json"),
                "--match", "mu:sample-mock-2026:semifinal:01",
                "--from", str(event_dir / "matchups" / "semifinal-2.md"),
                "--event-dir", str(event_dir),
            ]), 1)
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_a_later_round_cannot_be_decided_first(self):
        holder, event_dir = copy_event()
        try:
            drawn = json.loads((event_dir / "bracket.json").read_text(encoding="utf-8"))
            for entry in drawn["rounds"]:
                for match in entry["matches"]:
                    match["winner"] = None
                    if entry["round_index"] > 1:
                        match["entrants"] = ["team-lumen", "team-quill"]
            (event_dir / "bracket.json").write_text(json.dumps(drawn), encoding="utf-8")
            self.assertEqual(cli_main([
                "--root", str(ROOT), "bracket", "advance", str(event_dir / "bracket.json"),
                "--match", "mu:sample-mock-2026:final:01",
                "--from", str(event_dir / "matchups" / "final.md"),
                "--event-dir", str(event_dir),
            ]), 1)
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_a_report_disagreeing_with_the_bracket_is_refused(self):
        holder, event_dir = copy_event()
        try:
            path = event_dir / "matchups" / "final.md"
            metadata, body = frontmatter.read(path)
            metadata["team_b"] = "team-harbor"
            path.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
            drawn = json.loads((event_dir / "bracket.json").read_text(encoding="utf-8"))
            for entry in drawn["rounds"]:
                for match in entry["matches"]:
                    match["winner"] = None
            (event_dir / "bracket.json").write_text(json.dumps(drawn), encoding="utf-8")
            self.assertEqual(cli_main([
                "--root", str(ROOT), "bracket", "advance", str(event_dir / "bracket.json"),
                "--match", "mu:sample-mock-2026:final:01", "--from", str(path),
                "--event-dir", str(event_dir),
            ]), 1)
        finally:
            shutil.rmtree(holder, ignore_errors=True)


class ScoreDisclosureTests(unittest.TestCase):
    """F5, F6, F7: official totals reached public and team-facing output."""

    PUBLIC = {
        "event_id": "demo", "visibility": "public", "approval_state": "approved",
        "approved_by": "official", "source_artifacts": ["x"],
    }

    def test_prose_forms_of_a_score_are_caught(self):
        for phrasing in (
            "Lumen finished on 73.3 out of 100.",
            "Quill scored 72.3 overall.",
            "Verdant reached a total of 59.8.",
            "Harbor earned 53.3 points.",
        ):
            self.assertTrue(
                publication.scan_unapproved_scores(phrasing), phrasing
            )

    def test_a_known_official_total_blocks_regardless_of_phrasing(self):
        findings = publication.scan_unapproved_scores(
            "The champion's mark this year was 73.3, a strong showing.",
            known_totals=[73.3],
        )
        self.assertTrue(findings)

    def test_another_teams_total_blocks_in_a_dossier(self):
        findings = publication.check_team_facing(
            {"team_id": "team-lumen", "visibility": "team"},
            "Quill finished on 72.3 out of 100, ahead of you.",
            own_team="team-lumen", all_teams=["team-lumen", "team-quill"],
            display_names={"team-quill": "Quill"}, other_totals=[72.3],
        )
        self.assertTrue(any(f.severity == "blocking" for f in findings))

    def test_a_display_name_is_matched_not_only_the_id(self):
        findings = publication.scan_foreign_teams(
            "Quill had a serious security weakness.", own_team="team-lumen",
            all_teams=["team-lumen", "team-quill"], display_names={"team-quill": "Quill"},
        )
        self.assertTrue(any(f.severity == "major" for f in findings))

    def test_a_team_may_still_see_its_own_score(self):
        findings = publication.check_team_facing(
            {"team_id": "team-lumen", "visibility": "team"},
            "Overall panel result: 73.3 / 100.",
            own_team="team-lumen", all_teams=["team-lumen"], other_totals=[],
        )
        self.assertEqual([f.render() for f in findings], [])

    def test_the_renderer_uses_the_official_setting_not_the_artifact_claim(self):
        holder, event_dir = copy_event()
        try:
            path = event_dir / "public" / "final.md"
            metadata, body = frontmatter.read(path)
            metadata["scores_published"] = True
            path.write_text(
                frontmatter.dump(metadata, body + "\nFinal mark: 73.3 / 100.\n"),
                encoding="utf-8",
            )
            with self.assertRaises(ValidationError):
                ceremony.render_ceremony(event_dir, public_scores=False)
        finally:
            shutil.rmtree(holder, ignore_errors=True)


class PackagingTests(unittest.TestCase):
    """F2, F15: the wheel was built from a committed, stale build tree."""

    def test_build_output_is_not_tracked(self):
        import subprocess

        listed = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "build", "ai_tournament_judge.egg-info"],
            capture_output=True, text=True, check=False,
        )
        if listed.returncode != 0:
            self.skipTest("not a Git work tree")
        self.assertEqual(listed.stdout.strip(), "", "stale build output is tracked")

    def test_the_staging_tool_clears_a_stale_build_tree(self):
        text = (ROOT / "tools" / "stage_package_data.py").read_text(encoding="utf-8")
        self.assertIn('ROOT / "build"', text)


class EventInitDestinationTests(unittest.TestCase):
    """F10: an installed package wrote events into site-packages."""

    def test_initialize_accepts_a_separate_destination(self):
        holder = Path(tempfile.mkdtemp())
        try:
            framework = holder / "framework-root"
            for item in ("framework", "schemas", "events"):
                shutil.copytree(ROOT / item, framework / item)
            destination = holder / "operator"
            destination.mkdir()
            target = event_module.initialize(
                "probe-2026", root=framework, destination=destination
            )
            self.assertEqual(target, destination / "events" / "probe-2026")
            self.assertFalse((framework / "events" / "probe-2026").exists())
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_the_cli_refuses_to_write_inside_an_installed_package(self):
        holder = Path(tempfile.mkdtemp())
        try:
            fake = holder / "site-packages"
            fake.mkdir()
            self.assertEqual(
                cli_main(["--root", str(ROOT), "event", "init", "probe-2026",
                          "--dir", str(fake)]),
                1,
            )
        finally:
            shutil.rmtree(holder, ignore_errors=True)


class HookPrecisionTests(unittest.TestCase):
    """F21: the pre-advance hook matched the phrase anywhere in a command."""

    def run_hook(self, command):
        import subprocess

        return subprocess.run(
            [str(ROOT / ".claude" / "hooks" / "pre-advance.sh")],
            input=json.dumps({"tool_input": {"command": command}}),
            capture_output=True, text=True, cwd=ROOT, check=False,
        ).returncode

    def test_an_unrelated_command_mentioning_the_phrase_is_allowed(self):
        self.assertEqual(
            self.run_hook("echo 'see atj event advance events/foo in the README'"), 0
        )
        self.assertEqual(self.run_hook("python3 -m pytest tests/ -q"), 0)

    def test_a_real_advance_on_a_pending_gate_is_blocked(self):
        self.assertEqual(
            self.run_hook("python3 -m atj event advance events/_template"), 2
        )


if __name__ == "__main__":
    unittest.main()
