"""Regressions for defects found by live-trial-2026.

Each test names the defect from `docs/framework-fix-plan.md` that it locks down.
Both of these passed the previous suite.
"""

import contextlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path

from _support import ROOT  # noqa: F401
from atj import demo, frontmatter, render, reports, schema, versions
from atj.cli import main as cli_main

EVENT_DIR = ROOT / "events" / demo.EVENT_ID
TEMPLATE = ROOT / "framework" / "templates" / "adjudication-report.md"


def sandbox_event():
    directory = Path(tempfile.mkdtemp())
    shutil.copytree(EVENT_DIR, directory / "event")
    return directory, directory / "event"


class AdjudicationRequiredIsPrintedTests(unittest.TestCase):
    """D7: `atj score`'s text output printed `blocked_reasons` and nothing else.

    An operator read the console, saw no adjudication mentioned, and wrote "no
    adjudication required" into the ledger while the committed JSON recorded the
    opposite. It took a full audit round to catch.
    """

    NEEDS_ADJUDICATION = {
        "adjudication_required": [
            {"criterion": "security", "trigger": "unresolved-ne"},
            {"criterion": "innovation", "trigger": "severe-disagreement"},
        ]
    }

    def test_the_notice_names_every_criterion_and_its_trigger(self):
        notice = render.adjudication_notice(self.NEEDS_ADJUDICATION)
        self.assertIn("security: unresolved-ne", notice)
        self.assertIn("innovation: severe-disagreement", notice)

    def test_nothing_is_printed_when_no_adjudication_is_required(self):
        self.assertEqual(render.adjudication_notice({"adjudication_required": []}), "")

    def test_the_console_reports_an_adjudication_the_json_demands(self):
        holder, event_dir = sandbox_event()
        try:
            for path in (event_dir / "adjudications").glob("*.md"):
                path.unlink()
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                code = cli_main(["--root", str(ROOT), "score",
                                 str(event_dir / "judgments" / "team-lumen")])
            printed = buffer.getvalue()
            self.assertEqual(code, 1)
            self.assertIn("Finalization blocked", printed)
            self.assertIn("Adjudication required", printed)
            self.assertIn("security: unresolved-ne", printed)
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_the_official_consolidated_table_is_unchanged(self):
        """The notice is an operator prompt, not part of the written record.

        `consolidated_table` is committed verbatim into every consolidated team
        report, so adding the notice there would rewrite the sample event.
        """
        self.assertNotIn(
            "Adjudication required", render.consolidated_table(dict(
                self.NEEDS_ADJUDICATION,
                criteria={}, finalized=False, display_total=None,
                provisional_total=58.25, blocked_reasons=["security: unresolved NE"],
            ))
        )


class AdjudicationPersonaTests(unittest.TestCase):
    """D10: the template invited a persona the validator could never accept.

    `persona` names what produced the record and must resolve in
    `framework/personas.md`. The deciding human is `decided_by`.
    """

    def template_metadata(self):
        metadata, _ = frontmatter.read(TEMPLATE)
        return metadata

    def test_the_template_no_longer_invites_an_unregisterable_persona(self):
        persona = str(self.template_metadata()["persona"])
        self.assertIn(persona, reports.PLACEHOLDERS,
                      "an unreplaced persona must be caught as a placeholder, "
                      "not as an unknown persona after the work is done")
        self.assertNotIn("HUMAN", persona)

    def test_the_template_shows_every_field_the_schema_requires(self):
        metadata = self.template_metadata()
        for field in schema.get_schema("adjudication", ROOT)["required"]:
            self.assertIn(field, metadata, field)

    def test_the_schema_rejects_a_human_named_as_the_persona(self):
        metadata = dict(self.committed_adjudication())
        metadata["persona"] = "ADJUDICATOR-AGENT-OR-HUMAN@VERSION"
        self.assertTrue(schema.validate("adjudication", metadata, root=ROOT))

    def test_the_schema_requires_a_persona_at_all(self):
        metadata = dict(self.committed_adjudication())
        del metadata["persona"]
        self.assertTrue(schema.validate("adjudication", metadata, root=ROOT))

    def committed_adjudication(self):
        path = sorted((EVENT_DIR / "adjudications").glob("*.md"))[0]
        metadata, _ = frontmatter.read(path)
        return metadata

    def test_every_committed_adjudication_names_a_registered_component(self):
        personas = versions.load_personas(ROOT)
        paths = sorted((EVENT_DIR / "adjudications").glob("*.md"))
        self.assertTrue(paths)
        for path in paths:
            metadata, _ = frontmatter.read(path)
            with self.subTest(path.name):
                name, version = str(metadata["persona"]).split("@")
                self.assertIn(name, personas)
                self.assertEqual(personas[name].version, version)
                self.assertTrue(str(metadata["decided_by"]).strip(),
                                "the deciding human belongs in decided_by")


if __name__ == "__main__":
    unittest.main()
