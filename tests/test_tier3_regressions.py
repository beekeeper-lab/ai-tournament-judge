"""Regressions for the tier-3 defects: the ones that needed a schema migration.

D4/T3.1 makes a misdirected citation structurally detectable. D21 makes the
bracket, tournament and dossier stages visible to drift detection. D23 finishes
the job D6 started on the hook. T3.2 writes down what the audit rounds proved.
"""

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from _support import ROOT  # noqa: F401
from atj import canon, demo, event as event_module, frontmatter, reports

SAMPLE = ROOT / "events" / demo.EVENT_ID
LIVE = ROOT / "events" / "live-trial-2026"


class ACitationIsClaimedFromBothEnds(unittest.TestCase):
    """D4/T3.1: nine requirement rows cited an observation that said nothing
    about them, and `atj validate reports` returned zero findings at every
    stage, because the ids resolved. Resolution is all a schema can see.
    """

    def manifest(self) -> tuple[Path, Path, str]:
        temporary = Path(tempfile.mkdtemp())
        event = temporary / "event"
        shutil.copytree(SAMPLE, event)
        path = next((event / "evidence").glob("*/manifest.md"))
        return temporary, event, path.read_text(encoding="utf-8")

    def findings(self, path: Path, event: Path) -> list[str]:
        report = reports.validate_artifact(path, event, root=ROOT)
        return [f.render() for f in report.findings if f.rule == "citation-symmetry"]

    def test_the_sample_manifests_are_symmetric(self):
        for manifest in sorted((SAMPLE / "evidence").glob("*/manifest.md")):
            with self.subTest(manifest.parent.name):
                self.assertEqual(self.findings(manifest, SAMPLE), [])

    def test_a_requirement_citing_the_wrong_observation_is_blocking(self):
        temporary, event, text = self.manifest()
        path = next((event / "evidence").glob("*/manifest.md"))
        try:
            # req-01 cites the first observation; repoint it at the third, which
            # claims to support req-03 and says nothing about req-01. Exactly the
            # shape of the nine rows evidence audit round 1 found.
            observations = [
                row.split("|")[1].strip()
                for row in text.splitlines()
                if row.startswith("| ev-") or row.startswith("| e-")
            ]
            self.assertGreaterEqual(len(observations), 3, text)
            first, third = observations[0], observations[2]
            broken = text.replace(
                f"partially demonstrated — [[evidence:{first}]]",
                f"partially demonstrated — [[evidence:{third}]]",
            )
            self.assertNotEqual(broken, text, "the fixture no longer cites its observations")
            path.write_text(broken, encoding="utf-8")
            found = self.findings(path, event)
            self.assertTrue(found, "a misdirected citation was not detected")
            self.assertTrue(any("BLOCKING" in f for f in found), found)
            self.assertTrue(any("does not claim" in f for f in found), found)
        finally:
            shutil.rmtree(temporary)

    def test_an_observation_claiming_an_uncited_requirement_is_major(self):
        temporary, event, text = self.manifest()
        path = next((event / "evidence").glob("*/manifest.md"))
        try:
            broken = text.replace("| req-01 |", "| req-09 |", 1)
            path.write_text(broken, encoding="utf-8")
            found = self.findings(path, event)
            self.assertTrue(any("claims to support req-01" in f for f in found), found)
        finally:
            shutil.rmtree(temporary)

    def test_a_manifest_without_the_column_cannot_be_checked_and_says_so(self):
        """live-trial-2026 predates the column, so it advises rather than fails.

        A manifest pinned to the current rubric has no such excuse: without the
        column, the framework would be claiming a check it cannot perform.
        """
        for manifest in sorted((LIVE / "evidence").glob("*/manifest.md")):
            with self.subTest(manifest.parent.name):
                found = self.findings(manifest, LIVE)
                self.assertTrue(found)
                self.assertTrue(all("ADVISORY" in f for f in found), found)

        temporary, event, text = self.manifest()
        path = next((event / "evidence").glob("*/manifest.md"))
        try:
            metadata, body = frontmatter.read(path)
            self.assertEqual(str(metadata["rubric"]), canon.load(ROOT).reference)
            path.write_text(
                frontmatter.dump(metadata, body.replace("| Supports ", "| Supported ")),
                encoding="utf-8",
            )
            found = self.findings(path, event)
            self.assertTrue(any("BLOCKING" in f for f in found), found)
        finally:
            shutil.rmtree(temporary)


class EveryStageCanBeRecordedAsAUnit(unittest.TestCase):
    """D21: `derive_digests` covered evidence, judging and consolidation only.

    The bracket, tournament and dossier stages could not be recorded at all, and
    a unit whose digest cannot be re-derived is skipped by `stale_units` and by
    the drift check in `can_advance` -- so the sample event's committed ledger
    carried three kinds of unit with invented digests that nothing ever checked.
    """

    def test_the_previously_underivable_stages_now_derive(self):
        loaded = event_module.load(LIVE, root=ROOT)
        derived = event_module.derive_digests(loaded)
        self.assertIn("bracket:draw", derived)
        self.assertIn("matchup:mu-final-01", derived)
        for team in ("team-ledger", "team-podcast"):
            self.assertIn(f"dossier:{team}", derived)

    def test_the_committed_sample_ledger_is_fully_derivable(self):
        loaded = event_module.load(SAMPLE, root=ROOT)
        derived = event_module.derive_digests(loaded)
        for unit in loaded.status.get("units", []):
            with self.subTest(unit["unit_id"]):
                self.assertIn(
                    unit["unit_id"], derived,
                    "a unit whose digest cannot be re-derived is invisible to drift detection",
                )
        self.assertEqual(event_module.stale_units(loaded), [])

    def test_an_edited_matchup_makes_its_unit_stale(self):
        temporary = Path(tempfile.mkdtemp())
        event = temporary / "event"
        shutil.copytree(SAMPLE, event)
        try:
            loaded = event_module.load(event, root=ROOT)
            self.assertEqual(event_module.stale_units(loaded), [])
            report = next((event / "matchups").glob("*.md"))
            report.write_text(
                report.read_text(encoding="utf-8") + "\nAn edit nobody audited.\n",
                encoding="utf-8",
            )
            loaded = event_module.load(event, root=ROOT)
            drifted = {entry["unit_id"] for entry in event_module.stale_units(loaded)}
            self.assertIn(f"matchup:{report.stem}", drifted)
        finally:
            shutil.rmtree(temporary)

    def test_an_edited_dossier_makes_its_unit_stale(self):
        temporary = Path(tempfile.mkdtemp())
        event = temporary / "event"
        shutil.copytree(SAMPLE, event)
        try:
            dossier = next((event / "dossiers").glob("*.md"))
            dossier.write_text(
                dossier.read_text(encoding="utf-8") + "\nAn edit nobody audited.\n",
                encoding="utf-8",
            )
            loaded = event_module.load(event, root=ROOT)
            drifted = {entry["unit_id"] for entry in event_module.stale_units(loaded)}
            self.assertIn(f"dossier:{dossier.stem}", drifted)
        finally:
            shutil.rmtree(temporary)

    def test_a_moved_score_makes_the_bracket_stale(self):
        temporary = Path(tempfile.mkdtemp())
        event = temporary / "event"
        shutil.copytree(SAMPLE, event)
        try:
            summary = next((event / "summaries").glob("*.md"))
            summary.write_text(
                summary.read_text(encoding="utf-8") + "\nA later edit.\n", encoding="utf-8"
            )
            loaded = event_module.load(event, root=ROOT)
            drifted = {entry["unit_id"] for entry in event_module.stale_units(loaded)}
            self.assertIn("bracket:draw", drifted)
        finally:
            shutil.rmtree(temporary)


class ThePlaceholderCheckReadsCitations(unittest.TestCase):
    """D29: CI was red on `tools/check_placeholders.py`, and the file it flagged
    was the fix plan explaining the placeholder defects themselves.

    A full exemption would have been the easy repair and the wrong one: the plan
    would then be free to leave a real unresolved placeholder in prose. A quoted
    placeholder is a citation; an unquoted one is still a defect.
    """

    def run_checker(self, root: Path | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["python3", str(ROOT / "tools" / "check_placeholders.py")],
            capture_output=True, text=True, cwd=str(root or ROOT), timeout=120, check=False,
        )

    def test_the_repository_passes(self):
        completed = self.run_checker()
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_an_unquoted_placeholder_in_the_same_file_still_fails(self):
        plan = ROOT / "docs" / "framework-fix-plan.md"
        original = plan.read_text(encoding="utf-8")
        try:
            plan.write_text(
                original + "\nThe persona field still reads PERSONA@VERSION here.\n",
                encoding="utf-8",
            )
            completed = self.run_checker()
            self.assertEqual(completed.returncode, 1, completed.stdout)
            self.assertIn("framework-fix-plan.md", completed.stdout)
        finally:
            plan.write_text(original, encoding="utf-8")


class TheRepairRoundIsAudited(unittest.TestCase):
    """T3.2: nine defects in live-trial-2026 were introduced by repairs."""

    def test_the_rubric_set_states_the_rule(self):
        text = (ROOT / "framework" / "rubrics" / "README.md").read_text(encoding="utf-8")
        self.assertIn("A repair round is audited before the gate", text)
        self.assertIn("one round too early", text)
        self.assertIn("Repair is a source of defects", text)

    def test_it_states_what_validation_cannot_tell_you(self):
        text = (ROOT / "framework" / "rubrics" / "README.md").read_text(encoding="utf-8")
        self.assertIn("well-formed", text)
        self.assertIn("does not mean", text)
        self.assertIn("load-bearing", text)


if __name__ == "__main__":
    unittest.main()
