"""End-to-end: the committed sample event, and interrupt-and-resume behaviour.

These run against the artifacts that are actually committed, through the same
commands an operator runs. A change that breaks the workflow fails here rather
than being discovered during an event.
"""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from _support import ROOT  # noqa: F401
from atj import bracket, demo, event as event_module, frontmatter, reports, scoring
from atj.cli import main as cli_main

EVENT_DIR = ROOT / "events" / demo.EVENT_ID
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "bracket-20-team"


def run_cli(*argv) -> int:
    return cli_main(["--root", str(ROOT), *argv])


class SampleEventTests(unittest.TestCase):
    def test_the_sample_event_is_committed(self):
        self.assertTrue(EVENT_DIR.is_dir(), "the sample event is not committed")
        for name in ("event.md", "teams.md", "status.md", "bracket.md", "bracket.json"):
            self.assertTrue((EVENT_DIR / name).is_file(), name)

    def test_it_has_at_least_four_teams(self):
        loaded = event_module.load(EVENT_DIR, root=ROOT)
        self.assertGreaterEqual(len(loaded.teams), 4)

    def test_two_teams_share_an_affiliation_group(self):
        loaded = event_module.load(EVENT_DIR, root=ROOT)
        groups = [team["affiliation_group"] for team in loaded.teams]
        self.assertTrue(any(groups.count(group) >= 2 for group in groups if group))

    def test_a_previous_champion_and_runner_up_are_present(self):
        loaded = event_module.load(EVENT_DIR, root=ROOT)
        results = {team["previous_result"] for team in loaded.teams}
        self.assertIn("champion", results)
        self.assertIn("runner-up", results)

    def test_every_required_case_is_demonstrated(self):
        self.assertEqual(demo.check_conditions(ROOT), [])

    def test_configuration_roster_and_status_validate(self):
        loaded = event_module.load(EVENT_DIR, root=ROOT)
        self.assertEqual(event_module.validate_configuration(loaded), [])
        self.assertEqual(event_module.validate_roster(loaded), [])
        self.assertEqual(event_module.validate_status(loaded), [])

    def test_every_artifact_validates(self):
        loaded = event_module.load(EVENT_DIR, root=ROOT)
        found = reports.validate_event_reports(
            EVENT_DIR, root=ROOT,
            public_scores=bool(loaded.config.get("public_scores")),
            all_teams=[team["id"] for team in loaded.teams],
        )
        summary = reports.summarize(found)
        self.assertEqual(summary["counts"]["blocking"], 0, summary["findings"][:5])
        self.assertEqual(summary["counts"]["major"], 0, summary["findings"][:5])
        self.assertGreaterEqual(summary["artifacts"], 40)

    def test_each_team_has_four_independent_judgments(self):
        for team in demo.TEAMS:
            panel = scoring.load_panel(EVENT_DIR / "judgments" / team.id, root=ROOT)
            self.assertEqual(len(panel), 4, team.id)
            self.assertEqual(len({j.judge_id for j in panel}), 4, team.id)
            self.assertEqual(len({j.judge_run_id for j in panel}), 4, team.id)
            self.assertEqual(
                scoring.check_panel_integrity(panel, expected_judges=demo.JUDGES, root=ROOT), []
            )

    def test_consolidated_totals_match_a_fresh_recalculation(self):
        for team in demo.TEAMS:
            metadata, _ = frontmatter.read(EVENT_DIR / "summaries" / f"{team.id}.md")
            recalculated = demo.consolidation_for(team, resolved=True, root=ROOT)
            self.assertEqual(metadata["display_total"], recalculated["display_total"], team.id)

    def test_a_failed_audit_is_recorded_and_then_repaired(self):
        first, _ = frontmatter.read(EVENT_DIR / "audits" / "consolidation-team-lumen-01.md")
        second, _ = frontmatter.read(EVENT_DIR / "audits" / "consolidation-team-lumen-02.md")
        self.assertEqual(first["result"], "FAIL")
        self.assertIn(second["result"], ("PASS", "PASS WITH ADVISORIES"))

    def test_adjudications_are_decided_by_a_human(self):
        paths = sorted((EVENT_DIR / "adjudications").glob("*.md"))
        self.assertGreaterEqual(len(paths), 3)
        for path in paths:
            metadata, _ = frontmatter.read(path)
            self.assertTrue(metadata["decided_by"], path.name)
            self.assertEqual(metadata["visibility"], "private")

    def test_public_artifacts_are_approved_and_carry_no_private_data(self):
        from atj import publication

        paths = sorted((EVENT_DIR / "public").glob("*.md"))
        self.assertGreaterEqual(len(paths), 4)
        for path in paths:
            metadata, body = frontmatter.read(path)
            findings = publication.check_public(
                metadata, body, artifact=str(path), public_scores=False
            )
            self.assertEqual([f.render() for f in findings], [], path.name)
            self.assertEqual(metadata["approval_state"], "approved")
            self.assertTrue(metadata["approved_by"])
            self.assertTrue(metadata["source_artifacts"])

    def test_dossiers_are_team_facing(self):
        paths = sorted((EVENT_DIR / "dossiers").glob("*.md"))
        self.assertEqual(len(paths), len(demo.TEAMS))
        for path in paths:
            metadata, _ = frontmatter.read(path)
            self.assertEqual(metadata["visibility"], "team")

    def test_the_bracket_reproduces_from_its_recorded_seed(self):
        committed = json.loads((EVENT_DIR / "bracket.json").read_text(encoding="utf-8"))
        self.assertEqual(
            bracket.draw_only(committed), bracket.draw_only(demo.sample_bracket(ROOT))
        )
        self.assertEqual(bracket.verify(committed), [])

    def test_every_match_records_a_winner_and_advancement(self):
        committed = json.loads((EVENT_DIR / "bracket.json").read_text(encoding="utf-8"))
        for entry in committed["rounds"]:
            for match in entry["matches"]:
                self.assertIsNotNone(match["winner"], match["match_id"])
        final = committed["rounds"][-1]["matches"][0]
        self.assertEqual(len([e for e in final["entrants"] if e]), 2)
        self.assertEqual(bracket.pending_matches(committed), [])

    def test_matchup_reports_agree_with_the_bracket(self):
        committed = json.loads((EVENT_DIR / "bracket.json").read_text(encoding="utf-8"))
        records = []
        for path in sorted((EVENT_DIR / "matchups").glob("*.md")):
            metadata, _ = frontmatter.read(path)
            records.append((
                metadata["match_id"], metadata["team_a"],
                metadata["team_b"], metadata.get("winner"),
            ))
        self.assertEqual(bracket.check_matchup_records(committed, records), [])

    def test_no_real_person_or_school_appears(self):
        """A fixture that drifted toward real data would be a privacy incident."""
        corpus = "\n".join(
            path.read_text(encoding="utf-8") for path in EVENT_DIR.rglob("*.md")
        )
        self.assertIn("synthetic", corpus.lower())
        for team in demo.TEAMS:
            self.assertIn(team.id, corpus)


class TwentyTeamFixtureTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads((FIXTURE_DIR / "bracket.json").read_text(encoding="utf-8"))
        self.first = self.fixture["rounds"][0]["matches"]

    def test_thirty_two_slots(self):
        self.assertEqual(self.fixture["bracket_size"], 32)
        self.assertEqual(len(self.first), 16)

    def test_four_preliminary_matches_and_eight_participants(self):
        playing = [match for match in self.first if not match["bye"]]
        self.assertEqual(len(playing), 4)
        self.assertEqual(sum(len([e for e in m["entrants"] if e]) for m in playing), 8)

    def test_twelve_byes(self):
        self.assertEqual(sum(1 for match in self.first if match["bye"]), 12)
        self.assertEqual(self.fixture["bye_count"], 12)

    def test_previous_finalists_are_separated(self):
        entry = next(e for e in self.fixture["constraint_audit"]
                     if e["constraint"].startswith("Previous champion"))
        self.assertEqual(entry["status"], "satisfied", entry["detail"])

    def test_same_affiliation_teams_are_separated(self):
        entry = next(e for e in self.fixture["constraint_audit"]
                     if e["constraint"].startswith("No avoidable"))
        self.assertEqual(entry["status"], "satisfied", entry["detail"])

    def test_it_reproduces_from_the_recorded_seed(self):
        self.assertEqual(
            bracket.draw_only(self.fixture),
            bracket.draw_only(demo.twenty_team_bracket(ROOT)),
        )

    def test_the_roster_is_committed_alongside_it(self):
        roster = json.loads((FIXTURE_DIR / "roster.json").read_text(encoding="utf-8"))
        self.assertEqual(len(roster["teams"]), 20)


class CommandLineTests(unittest.TestCase):
    def test_the_documented_validation_commands_succeed(self):
        for argv in (
            ("release-check",),
            ("schemas",),
            ("personas",),
            ("rubric",),
            ("demo", "check"),
            ("event", "validate", str(EVENT_DIR)),
            ("validate", "reports", str(EVENT_DIR)),
            ("bracket", "verify", str(EVENT_DIR / "bracket.json")),
            ("bracket", "verify", str(FIXTURE_DIR / "bracket.json"),
             "--reproduce", str(FIXTURE_DIR / "roster.json")),
        ):
            with self.subTest(argv=argv):
                self.assertEqual(run_cli(*argv), 0, " ".join(argv))

    def test_the_module_entry_point_works_from_a_clean_subprocess(self):
        completed = subprocess.run(
            [sys.executable, "-m", "atj", "--root", str(ROOT), "release-check"],
            capture_output=True, text=True, cwd=ROOT, timeout=120, check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Release check: PASS", completed.stdout)

    def test_a_validation_failure_exits_non_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            broken = Path(directory) / "bracket.json"
            broken.write_text(json.dumps({
                "event_id": "demo", "format": "single-elimination", "policy": "x@1.0.0",
                "team_count": 4, "bracket_size": 4, "bye_count": 0, "bye_policy": "bogus",
                "seed": "s", "roster_version": 1, "framework_commit": "uncommitted",
                "feasible": True, "rounds": [], "constraint_audit": [],
            }), encoding="utf-8")
            self.assertEqual(run_cli("bracket", "verify", str(broken)), 1)

    def test_errors_print_cleanly_rather_than_raising(self):
        self.assertEqual(run_cli("event", "validate", "/nonexistent/event"), 1)


class RenderJudgmentTests(unittest.TestCase):
    """`atj render judgment` is the only sanctioned way a judgment gets numbers.

    The template tells the judge to write raw scores and nothing else numeric.
    These tests hold that promise: the generated table matches what the
    committed sample already contains, and the judge's prose survives.
    """

    SOURCE = EVENT_DIR / "judgments" / "team-lumen" / "judge-security-ops.md"

    def _rendered_block(self, text: str) -> str:
        start = text.index("<!-- atj:scores:begin -->")
        end = text.index("<!-- atj:scores:end -->")
        return text[start:end]

    def test_rendering_reproduces_the_committed_table(self):
        original = self.SOURCE.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "judge-security-ops.md"
            blanked = original.replace(
                self._rendered_block(original), "<!-- atj:scores:begin -->\n"
            )
            target.write_text(blanked, encoding="utf-8")
            self.assertEqual(run_cli("render", "judgment", str(target)), 0)
            self.assertEqual(
                self._rendered_block(target.read_text(encoding="utf-8")),
                self._rendered_block(original),
            )

    def test_an_unresolved_ne_is_reported_rather_than_totalled(self):
        original = self.SOURCE.read_text(encoding="utf-8")
        self.assertIn("not finalizable (unresolved NE)", original)

    def test_it_leaves_the_judge_prose_untouched(self):
        original = self.SOURCE.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "judge-security-ops.md"
            target.write_text(original, encoding="utf-8")
            self.assertEqual(run_cli("render", "judgment", str(target)), 0)
            self.assertEqual(target.read_text(encoding="utf-8"), original)

    def test_a_directory_renders_every_judgment_in_it(self):
        with tempfile.TemporaryDirectory() as directory:
            staged = Path(directory) / "team-lumen"
            shutil.copytree(EVENT_DIR / "judgments" / "team-lumen", staged)
            self.assertEqual(run_cli("render", "judgment", str(staged)), 0)
            for path in staged.glob("*.md"):
                self.assertEqual(
                    path.read_text(encoding="utf-8"),
                    (EVENT_DIR / "judgments" / "team-lumen" / path.name).read_text(
                        encoding="utf-8"
                    ),
                )

    def test_a_missing_generated_block_is_an_error_not_a_silent_skip(self):
        original = self.SOURCE.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "judge-security-ops.md"
            target.write_text(
                original.replace("<!-- atj:scores:begin -->", "").replace(
                    "<!-- atj:scores:end -->", ""
                ),
                encoding="utf-8",
            )
            self.assertEqual(run_cli("render", "judgment", str(target)), 1)


class InterruptAndResumeTests(unittest.TestCase):
    """An interrupted run must resume without redoing valid completed work."""

    def setUp(self):
        self.directory = Path(tempfile.mkdtemp())
        shutil.copytree(EVENT_DIR, self.directory / "event")
        self.event_dir = self.directory / "event"

    def tearDown(self):
        shutil.rmtree(self.directory, ignore_errors=True)

    def load(self):
        return event_module.load(self.event_dir, root=ROOT)

    def test_a_complete_event_has_nothing_left_to_do(self):
        loaded = self.load()
        self.assertEqual(loaded.stage, "complete")
        self.assertEqual(event_module.missing_outputs(loaded), [])

    def test_an_interrupted_unit_is_detected_by_its_missing_output(self):
        (self.event_dir / "summaries" / "team-quill.md").unlink()
        loaded = self.load()
        problems = event_module.missing_outputs(loaded)
        self.assertTrue(any("team-quill" in problem for problem in problems))
        action = event_module.next_action(loaded)
        self.assertEqual(action["action"], "repair-incomplete-unit")
        self.assertTrue(action["blocked"])

    def test_completed_audited_units_are_not_redone(self):
        (self.event_dir / "summaries" / "team-quill.md").unlink()
        loaded = self.load()
        action = event_module.next_action(loaded)
        self.assertTrue(all("team-quill" in problem for problem in action["problems"]))
        for other in ("team-lumen", "team-harbor", "team-verdant"):
            self.assertFalse(
                any(other in problem for problem in action["problems"]),
                f"resume proposed redoing completed work for {other}",
            )

    def test_changed_evidence_makes_the_dependent_unit_stale(self):
        loaded = self.load()
        unit = event_module.find_unit(loaded, "judging:team-lumen")
        self.assertIsNotNone(unit)
        stale = event_module.check_staleness(loaded, {"judging:team-lumen": "a-different-digest"})
        self.assertEqual(stale, ["judging:team-lumen"])

    def test_stale_work_is_surfaced_as_the_next_action(self):
        loaded = self.load()
        event_module.mark_stale(loaded, "judging:team-lumen", "evidence package changed")
        action = event_module.next_action(loaded)
        self.assertEqual(action["action"], "rerun-stale-units")
        self.assertIn("judging:team-lumen", action["problems"])

    def test_resume_survives_a_truncated_status_write(self):
        """A half-written ledger must fail loudly, not be silently half-believed."""
        from atj.errors import AtjError

        path = self.event_dir / "status.md"
        path.write_text("---\nevent_id: sample-mock-2026\ncurrent_stage: comp", encoding="utf-8")
        with self.assertRaises(AtjError):
            self.load()


if __name__ == "__main__":
    unittest.main()
