"""Regressions for the tier-1 defects landed after live-trial-2026 completed.

Each test names the defect from `docs/framework-fix-plan.md` that it locks down.
Every one of them passes against the pre-fix tree only by accident or not at all;
the docstrings say which behaviour was wrong and why it mattered in the event.
"""

import contextlib
import io
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from _support import ROOT  # noqa: F401
from atj import demo, event as event_module, frontmatter, render, scoring
from atj.cli import main as cli_main
from atj.errors import AtjError

SAMPLE = ROOT / "events" / demo.EVENT_ID
LIVE = ROOT / "events" / "live-trial-2026"


def sandbox(source: Path) -> tuple[Path, Path]:
    directory = Path(tempfile.mkdtemp())
    shutil.copytree(source, directory / "event")
    return directory, directory / "event"


def run_cli(*argv: str) -> tuple[int, str]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
        try:
            code = cli_main(list(argv))
        except SystemExit as exit_:  # argparse --help
            code = int(exit_.code or 0)
    return code, buffer.getvalue()


class ByeCountGatesTheScoreRequirement(unittest.TestCase):
    """D20: a validation rule whose only in-scope repairs were both offences.

    `performance-qualified` byes need a consolidated score for every eligible
    team, and the check fired on the policy name alone. live-trial-2026 has two
    teams, so its bracket grants zero byes and the policy consumes no score — but
    one team legitimately has no total (unresolved `NE`), so the event was
    permanently invalid. The only two repairs available inside the event were to
    fabricate a total or to change an active event's bye policy, and CLAUDE.md
    forbids both.
    """

    def test_no_byes_means_no_score_requirement(self):
        temporary, directory = sandbox(LIVE)
        try:
            loaded = event_module.load(directory, root=ROOT)
            self.assertEqual(event_module.bye_count(loaded), 0)
            self.assertEqual(loaded.config.get("bye_policy"), "performance-qualified")
            unscored = [t["id"] for t in loaded.eligible_teams if t.get("score") is None]
            self.assertTrue(unscored, "fixture no longer has an unscored eligible team")
            self.assertEqual(event_module.validate_roster(loaded), [])
        finally:
            shutil.rmtree(temporary)

    def test_byes_still_require_every_score(self):
        temporary, directory = sandbox(LIVE)
        try:
            loaded = event_module.load(directory, root=ROOT)
            # Three eligible teams need a four-slot bracket, so one bye exists
            # and the policy has something to allocate.
            (directory / "bracket.json").write_text(
                json.dumps({"bye_count": 1}), encoding="utf-8"
            )
            problems = event_module.validate_roster(loaded)
            self.assertTrue(
                any("performance-qualified byes need" in p for p in problems),
                problems,
            )
        finally:
            shutil.rmtree(temporary)


class CompletedAtSurvivesARecord(unittest.TestCase):
    """D15: re-recording a unit overwrote when the work actually finished.

    The ledger's `completed_at` is read by the audit trail and by the operator
    reconstructing an event. Carrying an audit result forward is not doing the
    work again, so it must not restamp the clock.
    """

    def test_unchanged_inputs_keep_the_original_time(self):
        temporary, directory = sandbox(SAMPLE)
        try:
            loaded = event_module.load(directory, root=ROOT)
            unit = event_module.record_unit(
                loaded, unit_id="judging:team-lumen", stage="initial-judging",
                input_digest="abc123", outputs=["judgments/team-lumen/"],
                completed_at="2026-01-01T00:00:00Z",
            )
            self.assertEqual(unit["completed_at"], "2026-01-01T00:00:00Z")
            again = event_module.record_unit(
                loaded, unit_id="judging:team-lumen", stage="initial-judging",
                input_digest="abc123", outputs=["judgments/team-lumen/"],
                audit_result="PASS",
            )
            self.assertEqual(again["completed_at"], "2026-01-01T00:00:00Z")
            self.assertEqual(again["audit_result"], "PASS")
        finally:
            shutil.rmtree(temporary)

    def test_changed_inputs_restamp(self):
        temporary, directory = sandbox(SAMPLE)
        try:
            loaded = event_module.load(directory, root=ROOT)
            event_module.record_unit(
                loaded, unit_id="judging:team-lumen", stage="initial-judging",
                input_digest="abc123", outputs=[],
                completed_at="2026-01-01T00:00:00Z",
            )
            moved = event_module.record_unit(
                loaded, unit_id="judging:team-lumen", stage="initial-judging",
                input_digest="different", outputs=[],
            )
            self.assertNotEqual(moved["completed_at"], "2026-01-01T00:00:00Z")
        finally:
            shutil.rmtree(temporary)

    def test_now_restamps_on_demand(self):
        temporary, directory = sandbox(SAMPLE)
        try:
            loaded = event_module.load(directory, root=ROOT)
            event_module.record_unit(
                loaded, unit_id="judging:team-lumen", stage="initial-judging",
                input_digest="abc123", outputs=[],
                completed_at="2026-01-01T00:00:00Z",
            )
            restamped = event_module.record_unit(
                loaded, unit_id="judging:team-lumen", stage="initial-judging",
                input_digest="abc123", outputs=[], completed_at="now",
            )
            self.assertNotEqual(restamped["completed_at"], "2026-01-01T00:00:00Z")
        finally:
            shutil.rmtree(temporary)

    def test_cli_rejects_a_malformed_timestamp(self):
        code, output = run_cli(
            "event", "unit", str(SAMPLE), "record",
            "--id", "judging:team-lumen", "--completed-at", "yesterday",
        )
        self.assertEqual(code, 2, output)
        self.assertIn("not a UTC timestamp", output)


class WholeTreeScansAskGit(unittest.TestCase):
    """D17: a worktree inside the repository broke `release-check`.

    The single-source check walked the filesystem, so a second checkout under the
    repository looked like a second editable copy of the official weights — and
    `tests/test_canonical_model.py` asserts against those weights on purpose.
    Gitignoring the worktree does not help: a worktree's files are tracked in its
    own index, and the walk never asked git anything.
    """

    def test_tracked_files_excludes_a_nested_worktree(self):
        from atj.cli import tracked_files

        listed = tracked_files(ROOT)
        if listed is None:
            self.skipTest("not a git checkout")
        self.assertIn(ROOT / "atj" / "cli.py", listed)
        self.assertFalse(
            [p for p in listed if ".claude/worktrees/" in str(p)],
            "a nested worktree's files must not be listed as this repository's",
        )

    def test_release_check_passes_with_a_worktree_present(self):
        if not (ROOT / ".git").exists():
            self.skipTest("not a git checkout")
        worktree = ROOT / ".claude" / "worktrees" / "atj-d17-regression"
        if worktree.exists():
            self.skipTest("a worktree of that name already exists")
        created = subprocess.run(
            ["git", "-C", str(ROOT), "worktree", "add", "--detach", str(worktree), "HEAD"],
            capture_output=True, check=False,
        )
        if created.returncode != 0:
            self.skipTest(f"cannot create a worktree here: {created.stderr!r}")
        try:
            from atj.cli import check_no_duplicate_weights

            self.assertEqual(check_no_duplicate_weights(ROOT), [])
        finally:
            subprocess.run(
                ["git", "-C", str(ROOT), "worktree", "remove", "--force", str(worktree)],
                capture_output=True, check=False,
            )

    def test_an_export_still_gets_scanned(self):
        """No `.git` means no git answer, and the walk must still happen."""
        from atj.cli import tracked_files

        temporary = Path(tempfile.mkdtemp())
        try:
            self.assertIsNone(tracked_files(temporary))
        finally:
            shutil.rmtree(temporary)


class PublicationGateTakesADirectory(unittest.TestCase):
    """D24: the event-wide disclosure check CLAUDE.md mandates could not be run.

    `atj validate publication` accepted one artifact path and raised
    `Is a directory` on anything else, so "run it before anything leaves the
    panel" meant naming every artifact by hand.
    """

    def test_a_whole_event_is_gated_in_one_call(self):
        code, output = run_cli("validate", "publication", str(SAMPLE))
        self.assertEqual(code, 0, output)
        self.assertIn("artifact(s)", output)
        self.assertIn("CLEAR", output)
        import re

        count = int(re.search(r"\((\d+) artifact", output).group(1))
        self.assertGreater(count, 40, output)

    def test_a_single_artifact_still_works(self):
        code, output = run_cli(
            "validate", "publication", str(SAMPLE / "public" / "final.md")
        )
        self.assertEqual(code, 0, output)
        self.assertIn("1 artifact(s)", output)

    def test_an_undeclared_directory_blocks_rather_than_being_skipped(self):
        """The property the tournament audit relied on for D22, at event scope.

        Nothing stored outside a declared directory can be cleared for release.
        A directory scan that quietly skipped an unrecognised directory would
        remove the only control standing over `matchup-passes/`.
        """
        temporary, directory = sandbox(SAMPLE)
        try:
            stray = directory / "matchup-passes"
            stray.mkdir()
            shutil.copy(directory / "matchups" / "final.md", stray / "pass-a-first.md")
            code, output = run_cli("validate", "publication", str(directory))
            self.assertEqual(code, 1, output)
            self.assertIn("location-unknown", output)
            self.assertIn("pass-a-first.md", output)
        finally:
            shutil.rmtree(temporary)


class ConsolidatedReportsAreGenerated(unittest.TestCase):
    """D18 and D19: the template named two commands and neither existed.

    Both of live-trial-2026's panel reports were transcribed by hand, both
    consolidators disclosed it unprompted, and each table had to be verified cell
    by cell against the canonical JSON by a throwaway script.
    """

    def test_render_consolidated_reproduces_a_committed_report(self):
        temporary, directory = sandbox(SAMPLE)
        try:
            summaries = directory / "summaries"
            code, output = run_cli("render", "consolidated", str(summaries))
            self.assertEqual(code, 0, output)
            self.assertNotIn("rendered", output)
            for name in sorted(p.name for p in summaries.glob("*.md")):
                self.assertEqual(
                    (SAMPLE / "summaries" / name).read_text(encoding="utf-8"),
                    (summaries / name).read_text(encoding="utf-8"),
                    f"{name} is not reproduced by its own generator",
                )
        finally:
            shutil.rmtree(temporary)

    def test_a_hand_edited_table_is_restored(self):
        temporary, directory = sandbox(SAMPLE)
        try:
            target = directory / "summaries" / "team-lumen.md"
            metadata, body = frontmatter.read(target)
            metadata["approval_state"] = "draft"
            tampered = body.replace("| **Overall**", "| **Overall** <!-- edited -->", 1)
            self.assertNotEqual(tampered, body)
            target.write_text(frontmatter.dump(metadata, tampered), encoding="utf-8")
            code, output = run_cli("render", "consolidated", str(target))
            self.assertEqual(code, 0, output)
            self.assertNotIn("<!-- edited -->", target.read_text(encoding="utf-8"))
        finally:
            shutil.rmtree(temporary)

    def test_an_approved_report_is_not_silently_rewritten(self):
        temporary, directory = sandbox(SAMPLE)
        try:
            target = directory / "summaries" / "team-lumen.md"
            metadata, body = frontmatter.read(target)
            self.assertEqual(metadata["approval_state"], "approved")
            metadata["display_total"] = 99.9
            target.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
            code, output = run_cli("render", "consolidated", str(target))
            self.assertNotEqual(code, 0, output)
            self.assertIn("approved", output)
            self.assertEqual(
                frontmatter.read(target)[0]["display_total"], 99.9,
                "a refused render must change nothing",
            )
        finally:
            shutil.rmtree(temporary)

    def test_the_template_no_longer_claims_a_command_that_does_not_exist(self):
        text = (ROOT / "framework" / "templates" / "consolidated-team-report.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("atj consolidate`", text)
        self.assertNotIn("Never transcribed by hand", text)
        self.assertIn("atj render consolidated", text)

    def test_every_command_the_template_names_is_a_real_subcommand(self):
        """D3, D18 and D19 are one defect repeating. Assert the class, not a case."""
        import re

        cited: set[str] = set()
        for template in sorted((ROOT / "framework" / "templates").glob("*.md")):
            for match in re.findall(r"`atj ([a-z][a-z -]*)`", template.read_text(encoding="utf-8")):
                cited.add(" ".join(match.split()))
        self.assertTrue(cited, "no atj commands cited by any template")
        for command in sorted(cited):
            code, output = run_cli(*command.split(), "--help")
            self.assertEqual(code, 0, f"template cites `atj {command}`, which fails: {output}")


class ConsolidatedTableIsItsOwnFixedPoint(unittest.TestCase):
    """A generated block must survive its own regeneration unchanged.

    `consolidated_table` emitted a trailing empty row that `replace_block` then
    stripped, so a correct report was never byte-identical to its regeneration
    and every re-render produced a one-line diff a reviewer had to explain.
    """

    def test_no_trailing_blank_when_nothing_is_blocked(self):
        judgments = scoring.load_panel(SAMPLE / "judgments" / "team-lumen", root=ROOT)
        result = scoring.consolidate(
            judgments,
            expected_judges=[j.judge_id for j in judgments],
            resolutions=scoring.load_resolutions(
                SAMPLE / "adjudications", team_id="team-lumen", root=ROOT
            ),
            root=ROOT,
        )
        table = render.consolidated_table(result, ROOT)
        self.assertEqual(table, table.rstrip())

    def test_front_matter_round_trips_exactly(self):
        """`dump(*split(text)) == text`, or every render dirties its own diff."""
        for artifact in (
            SAMPLE / "summaries" / "team-lumen.md",
            SAMPLE / "judgments" / "team-lumen" / "judge-backend.md",
            SAMPLE / "dossiers" / "team-lumen.md",
            SAMPLE / "audits" / "final-event.md",
        ):
            with self.subTest(artifact=artifact.name):
                text = artifact.read_text(encoding="utf-8")
                metadata, body = frontmatter.split(text)
                self.assertEqual(frontmatter.dump(metadata, body), text)


if __name__ == "__main__":
    unittest.main()
