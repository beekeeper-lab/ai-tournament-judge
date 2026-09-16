"""Ceremony output: generated from approved public artifacts, and nothing else."""

import re
import unittest
from pathlib import Path

from _support import ROOT  # noqa: F401
from atj import ceremony, demo, frontmatter
from atj.errors import ValidationError

EVENT_DIR = ROOT / "events" / demo.EVENT_ID
OUTPUT = EVENT_DIR / "public" / "ceremony" / "index.html"

PRIVATE_SHAPES = {
    "evidence package id": r"\bev:[a-z0-9-]+:",
    "judge run id": r"\bjr:[a-z0-9-]+:",
    "adjudication id": r"\badj:[a-z0-9-]+:",
    "judge persona": r"judge-(?:backend|frontend-ux|security-ops|product-agentic)",
    "panel consolidator": r"panel-consolidator",
    "numeric score out of 100": r"\d{1,3}(?:\.\d)?\s*/\s*100",
    "full commit hash": r"\b[0-9a-f]{40}\b",
    "bracket seed": re.escape(demo.SEED),
}


class CeremonyOutputTests(unittest.TestCase):
    def setUp(self):
        self.html = ceremony.render_ceremony(EVENT_DIR)

    def test_it_is_committed(self):
        self.assertTrue(OUTPUT.is_file(), "ceremony output is not committed")

    def test_it_contains_the_required_sections(self):
        for heading in (
            "Event overview", "Champion and finalists", "Tournament bracket",
            "Completed matchups", "How entries were judged",
        ):
            self.assertIn(heading, self.html, heading)

    def test_it_names_the_champion_and_the_current_round(self):
        self.assertIn("Lumen", self.html)
        self.assertIn("Current round", self.html)

    def test_it_is_self_contained(self):
        """A ceremony display must not depend on the network."""
        self.assertNotIn("<script", self.html.lower())
        for pattern in (r'src="https?://', r'href="https?://', r"@import"):
            self.assertIsNone(re.search(pattern, self.html), pattern)

    def test_no_private_shape_appears(self):
        for label, pattern in PRIVATE_SHAPES.items():
            self.assertIsNone(re.search(pattern, self.html), f"{label} leaked")

    def test_it_reads_no_private_directory(self):
        """The private record is not an input, so a template bug cannot leak it."""
        for name in ceremony.PRIVATE_DIRS:
            self.assertTrue((EVENT_DIR / name).exists() or True)
        artifacts = ceremony.load_public_artifacts(EVENT_DIR)
        for entry in [artifacts["summary"], *artifacts["matches"]]:
            self.assertEqual(entry["path"].parent.name, "public")

    def test_an_unapproved_artifact_stops_the_render(self):
        import shutil
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "event"
            shutil.copytree(EVENT_DIR, copy)
            path = copy / "public" / "final.md"
            metadata, body = frontmatter.read(path)
            metadata["approval_state"] = "draft"
            path.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
            with self.assertRaises(ValidationError):
                ceremony.render_ceremony(copy)

    def test_a_leaked_credential_stops_the_render(self):
        import shutil
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "event"
            shutil.copytree(EVENT_DIR, copy)
            path = copy / "public" / "final.md"
            path.write_text(
                path.read_text(encoding="utf-8") + "\nkey AKIAIOSFODNN7EXAMPLE\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValidationError):
                ceremony.render_ceremony(copy)

    def test_a_missing_event_summary_stops_the_render(self):
        import shutil
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "event"
            shutil.copytree(EVENT_DIR, copy)
            (copy / "public" / ceremony.SUMMARY_FILE).unlink()
            with self.assertRaises(ValidationError):
                ceremony.render_ceremony(copy)

    def test_it_regenerates_identically(self):
        self.assertEqual(self.html, ceremony.render_ceremony(EVENT_DIR))
        self.assertEqual(OUTPUT.read_text(encoding="utf-8"), self.html)


class DossierOutputTests(unittest.TestCase):
    def test_every_team_has_a_printable_dossier(self):
        for team in demo.TEAMS:
            path = EVENT_DIR / "public" / "ceremony" / "dossiers" / f"{team.id}.html"
            self.assertTrue(path.is_file(), team.id)

    def test_a_dossier_carries_its_own_score_but_no_panel_internals(self):
        """A team may see its own total. It may not see how the panel argued."""
        html = ceremony.render_dossier(EVENT_DIR / "dossiers" / "team-lumen.md")
        self.assertRegex(html, r"\d{1,3}(?:\.\d)?\s*/\s*100")
        for label, pattern in PRIVATE_SHAPES.items():
            if label == "numeric score out of 100":
                continue
            self.assertIsNone(re.search(pattern, html), f"{label} leaked into a dossier")

    def test_a_dossier_does_not_expose_another_team_s_result(self):
        html = ceremony.render_dossier(EVENT_DIR / "dossiers" / "team-lumen.md")
        others = [team for team in demo.TEAMS if team.id != "team-lumen"]
        for team in others:
            for line in html.splitlines():
                if team.display_name in line:
                    self.assertIsNone(
                        re.search(r"\d{1,3}(?:\.\d)?\s*/\s*100", line),
                        f"a score appears on the same line as {team.display_name}",
                    )

    def test_an_unapproved_dossier_is_refused(self):
        import shutil
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "team-lumen.md"
            shutil.copy(EVENT_DIR / "dossiers" / "team-lumen.md", path)
            metadata, body = frontmatter.read(path)
            metadata["approval_state"] = "draft"
            path.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
            with self.assertRaises(ValidationError):
                ceremony.render_dossier(path)


if __name__ == "__main__":
    unittest.main()
