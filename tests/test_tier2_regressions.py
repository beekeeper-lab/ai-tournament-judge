"""Regressions for the tier-2 defects, landed after live-trial-2026 completed.

Tier 2 is the work that could not land during the event because it moves a
version: personas, rubric text, and what `atj score` prints for an official
result. Each test names the defect from `docs/framework-fix-plan.md` it locks
down, and says what the pre-fix behaviour actually did.
"""

import shutil
import tempfile
import unittest
from pathlib import Path

from _support import ROOT  # noqa: F401
from atj import canon, frontmatter, reports, schema, versions
from atj.cli import check_version_archive, check_write_contracts
from atj.errors import AtjError, VersionError

LIVE = ROOT / "events" / "live-trial-2026"


def framework_copy(directory: str) -> Path:
    """A throwaway root holding the framework, its schemas and its components."""
    copy = Path(directory)
    for item in ("framework", "schemas", ".claude"):
        shutil.copytree(ROOT / item, copy / item)
    return copy


def set_persona_version(root: Path, agent_id: str, version: str) -> None:
    path = root / versions.PERSONA_REGISTRY
    text = path.read_text(encoding="utf-8")
    persona = versions.load_personas(root)[agent_id]
    old = f"| {agent_id} | {persona.version} |"
    assert old in text, old
    path.write_text(text.replace(old, f"| {agent_id} | {version} |"), encoding="utf-8")


def add_superseded_row(root: Path, agent_id: str, version: str, replacement: str) -> None:
    path = root / versions.PERSONA_REGISTRY
    text = path.read_text(encoding="utf-8")
    header = "| Agent ID | Version | Retired | Superseded by | Content digest |\n|---|---|---|---|---|\n"
    assert header in text
    row = f"| {agent_id} | {version} | 2026-09-18 | {replacement} | {'0' * 16} |\n"
    path.write_text(text.replace(header, header + row), encoding="utf-8")


class SupersededVersionsKeepACompletedEventValid(unittest.TestCase):
    """D28: a version bump used to falsify every artifact already judged under it.

    `require_versions` compared an artifact's pins against the single canonical
    version and raised on any difference. Bumping `judge-backend` to 1.1.0 --
    which tier 2 requires, and which the fix plan says to do only after the event
    completes -- produced four blocking `version` findings against
    live-trial-2026, whose artifacts are frozen. The only repair available inside
    a completed event is to rewrite a frozen artifact.
    """

    def test_a_bump_without_a_superseded_row_is_still_fatal(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = framework_copy(directory)
            set_persona_version(copy, "judge-backend", "1.2.0")
            with self.assertRaises(VersionError) as raised:
                versions.require_versions(
                    {"rubric": canon.load(copy).reference, "persona": "judge-backend@1.1.0"},
                    root=copy,
                )
            self.assertIn("no superseded row", raised.exception.message)

    def test_a_recorded_retirement_keeps_the_old_pin_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = framework_copy(directory)
            set_persona_version(copy, "judge-backend", "1.2.0")
            add_superseded_row(copy, "judge-backend", "1.1.0", "1.2.0")
            pins = {"rubric": canon.load(copy).reference, "persona": "judge-backend@1.1.0"}
            versions.require_versions(pins, root=copy)
            self.assertEqual(
                versions.superseded_pins(pins, root=copy), ["persona: judge-backend@1.1.0"]
            )

    def test_the_two_tables_are_read_separately(self):
        """A retired row has the same shape as a current one, one table down.

        The first cut of this table read both with one pattern, so retiring
        `judge-backend@1.0.0` made the history row win the dictionary and
        `atj personas` reported the retired version as current.
        """
        personas = versions.load_personas(ROOT)
        retired = versions.load_superseded(ROOT)
        self.assertTrue(retired, "the registry records no retirement to check")
        for (agent_id, version) in retired:
            with self.subTest(f"{agent_id}@{version}"):
                self.assertNotEqual(personas[agent_id].version, version)

    def test_a_retirement_may_not_name_the_current_version(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = framework_copy(directory)
            current = versions.load_personas(copy)["judge-backend"].version
            add_superseded_row(copy, "judge-backend", current, "9.9.9")
            problems = check_version_archive(copy)
            self.assertTrue(
                any("is also the current version" in p for p in problems), problems
            )


class ArchivedRubricsOutliveTheirReplacement(unittest.TestCase):
    """D28, rubric half: recomputation must use the weights that were in force.

    D12 requires a new `submission-evaluation` version. Every artifact in both
    completed events pins 1.0.0, and `_check_judgment_scores` validated scores
    against whatever the rubric says today, so a criterion added or removed by the
    new version would turn a frozen judgment into a phantom mismatch.
    """

    def archive(self, copy: Path, version: str) -> Path:
        rubric = copy / canon.SUBMISSION_RUBRIC
        text = rubric.read_text(encoding="utf-8")
        current = canon.load(copy)
        archived = canon.archive_dir(copy) / f"{current.rubric_id}@{current.version}.md"
        archived.parent.mkdir(parents=True, exist_ok=True)
        archived.write_text(text, encoding="utf-8")
        rubric.write_text(
            text.replace(f"version: {current.version}", f"version: {version}", 1), encoding="utf-8"
        )
        canon.clear_cache()
        return archived

    def tearDown(self):
        canon.clear_cache()

    def test_an_archived_version_stays_loadable_and_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = framework_copy(directory)
            before = canon.load(copy).reference
            self.archive(copy, "9.9.9")
            self.assertNotEqual(canon.load(copy).reference, before)
            self.assertIn(before, canon.superseded_references(copy))
            self.assertEqual(canon.load_reference(before, copy).reference, before)
            versions.require_versions({"rubric": before}, root=copy)

    def test_an_unarchived_version_is_still_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = framework_copy(directory)
            with self.assertRaises(AtjError):
                canon.load_reference("submission-evaluation@0.0.1", copy)

    def test_the_archive_may_not_hold_the_current_version(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = framework_copy(directory)
            current = canon.load(copy)
            archived = canon.archive_dir(copy) / f"{current.rubric_id}@{current.version}.md"
            archived.parent.mkdir(parents=True, exist_ok=True)
            archived.write_text(
                (copy / canon.SUBMISSION_RUBRIC).read_text(encoding="utf-8"), encoding="utf-8"
            )
            problems = check_version_archive(copy)
            self.assertTrue(any("current version" in p for p in problems), problems)

    def test_a_mislabelled_archive_file_is_fatal(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = framework_copy(directory)
            stray = canon.archive_dir(copy) / "submission-evaluation@0.9.0.md"
            stray.parent.mkdir(parents=True, exist_ok=True)
            stray.write_text(
                (copy / canon.SUBMISSION_RUBRIC).read_text(encoding="utf-8"), encoding="utf-8"
            )
            problems = check_version_archive(copy)
            self.assertTrue(any("named" in p for p in problems), problems)


class WriteContractsAreChecked(unittest.TestCase):
    """T2.2/D1: nothing compared a component's tools against the artifact it owes.

    Four judges ran a whole event declaring `Read, Grep, Glob` while
    `judge-submission` required each to produce a judgment document. Both facts
    were written down, in different files, and no check read them together.

    The fix plan proposed giving the judges `Write`. That is the wrong half to
    move: a judge reads untrusted submission content, and
    `test_initial_judges_have_no_tool_that_could_act_on_an_injection` exists to
    keep that surface closed. So the registry declares who persists each
    artifact, the judges keep returning their document for the orchestrator to
    write, and `release-check` now fails if either side of that contract drifts.
    """

    def test_taking_write_away_from_a_component_that_writes_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = framework_copy(directory)
            self.assertEqual(check_write_contracts(copy), [])
            path = copy / versions.AGENT_DIR / "judging-auditor.md"
            text = path.read_text(encoding="utf-8")
            self.assertIn("tools: Read, Grep, Glob, Bash, Write", text)
            path.write_text(text.replace(", Write", "", 1), encoding="utf-8")
            problems = check_write_contracts(copy)
            self.assertTrue(any("no Write" in p for p in problems), problems)

    def test_a_component_that_writes_nothing_may_not_hold_write(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = framework_copy(directory)
            path = copy / versions.AGENT_DIR / "judge-backend.md"
            text = path.read_text(encoding="utf-8")
            path.write_text(
                text.replace("tools: Read, Grep, Glob", "tools: Read, Grep, Glob, Write", 1),
                encoding="utf-8",
            )
            problems = check_write_contracts(copy)
            self.assertTrue(any("writes nothing" in p for p in problems), problems)

    def test_every_evidence_facing_component_returns_rather_than_writes(self):
        for agent_id in (
            "judge-backend", "judge-frontend-ux", "judge-security-ops",
            "judge-product-agentic", "panel-consolidator", "matchup-judge",
        ):
            with self.subTest(agent_id):
                persona = versions.load_personas(ROOT)[agent_id]
                self.assertFalse(persona.must_write, "an evidence-facing agent holds no Write")
                metadata, body = frontmatter.read(versions.component_path(agent_id, ROOT))
                self.assertNotIn("Write", str(metadata["tools"]))
                # The defect was silence, not the tool surface: the definition has
                # to say what the agent produces and who persists it.
                self.assertIn("## Your own artifact", body)
                self.assertIn("no `Write` tool", body)

    def test_the_auditor_declares_where_it_writes(self):
        persona = versions.load_personas(ROOT)["judging-auditor"]
        self.assertTrue(persona.must_write)
        self.assertEqual(persona.writes, "events/<event>/audits/")
        metadata, body = frontmatter.read(versions.component_path("judging-auditor", ROOT))
        self.assertIn("Write", str(metadata["tools"]))
        self.assertIn("events/<event-id>/audits/", body)


class TheRubricAnswersItsOwnQuestions(unittest.TestCase):
    """D12, D8 and D9: three places where the rubric left a judge to invent a rule.

    Each caused a real split in live-trial-2026 on facts the judges agreed about.
    """

    def setUp(self):
        self.rubric = canon.load(ROOT)
        self.text = (ROOT / canon.SUBMISSION_RUBRIC).read_text(encoding="utf-8")

    def test_the_agentic_question_has_a_subject_either_way(self):
        """D12: three of four sub-questions presupposed that AI exists."""
        question = self.rubric.criterion("agentic").question
        self.assertIn("decision about whether to use AI", question)
        self.assertIn("where AI is used", question)

    def test_the_rubric_says_what_to_score_when_there_is_no_ai(self):
        self.assertIn("## A criterion whose subject the submission does not contain", self.text)
        self.assertIn("meets primary expectations", self.text)
        self.assertIn("never scored at the bottom anchors", self.text)
        self.assertIn("`NE` does not apply to an absent subject", self.text)
        self.assertIn("Do not score `agentic` down because a submission contains no AI", self.text)

    def test_the_weights_and_criteria_did_not_move(self):
        """A rubric version that changed the numbers would need a migration.

        This one changes wording and adds rules. Both completed events keep the
        same criterion set, which is what makes the archive sufficient.
        """
        archived = canon.load_reference("submission-evaluation@1.0.0", ROOT)
        self.assertEqual(archived.criterion_ids, self.rubric.criterion_ids)
        self.assertEqual(archived.weights, self.rubric.weights)
        self.assertEqual(
            (archived.scale_min, archived.scale_max),
            (self.rubric.scale_min, self.rubric.scale_max),
        )
        self.assertNotEqual(archived.version, self.rubric.version)

    def test_confidence_on_an_ne_has_one_meaning(self):
        self.assertIn("`confidence` describes the evidence", self.text)
        self.assertIn("evidence-limited is a `high`-confidence `NE`", self.text)

    def test_model_verified_has_a_threshold(self):
        policy = (ROOT / "framework" / "policies" / "evidence-and-citation.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## Model identity", policy)
        self.assertIn("A model's self-report is a team claim", policy)
        verified = schema.get_schema("judgment", ROOT)
        self.assertIn("model", verified.get("properties", {}))


class NeConfidenceIsChecked(unittest.TestCase):
    """D8, enforced: the definition is only worth as much as the check."""

    def judgment(self, criterion: str, confidence: str) -> tuple[Path, Path]:
        temporary = Path(tempfile.mkdtemp())
        event = temporary / "event"
        shutil.copytree(ROOT / "events" / "live-trial-2026", event)
        path = next((event / "judgments" / "team-podcast").glob("*.md"))
        metadata, body = frontmatter.read(path)
        # A new artifact, pinned to the rubric that defines the rule.
        metadata["rubric"] = canon.load(ROOT).reference
        metadata["persona"] = versions.load_personas(ROOT)[str(metadata["judge_id"])].reference
        metadata["scores"][criterion] = "NE"
        metadata["confidence"][criterion] = confidence
        path.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
        return temporary, path

    def findings(self, path: Path, event: Path, criterion: str) -> list[str]:
        report = reports.validate_artifact(path, event, root=ROOT)
        return [
            f.detail for f in report.findings
            if f.rule == "ne-confidence" and repr(criterion) in f.detail
        ]

    def test_an_evidence_limited_ne_must_be_high_confidence(self):
        temporary, path = self.judgment("reliability", "low")
        try:
            detail = self.findings(path, temporary / "event", "reliability")
            self.assertTrue(detail, "an evidence-limited NE at low confidence was not flagged")
            self.assertIn("evidence-limited", detail[0])
        finally:
            shutil.rmtree(temporary)

    def test_an_unaccounted_ne_must_be_low_confidence(self):
        temporary, path = self.judgment("security", "high")
        try:
            detail = self.findings(path, temporary / "event", "security")
            self.assertTrue(detail, "an unaccounted NE at high confidence was not flagged")
            self.assertIn("does not record", detail[0])
        finally:
            shutil.rmtree(temporary)

    def test_the_rule_is_not_read_back_onto_an_earlier_rubric(self):
        """live-trial-2026 was judged before the rule existed; it stays clean."""
        found = reports.validate_event_reports(LIVE, root=ROOT)
        flagged = [
            f.render() for report in found for f in report.findings if f.rule == "ne-confidence"
        ]
        self.assertEqual(flagged, [])


class LiveTrialStaysValidAcrossTheBump(unittest.TestCase):
    """The frozen record is the thing tier 2 must not damage."""

    def test_the_completed_event_has_no_blocking_findings(self):
        found = reports.validate_event_reports(LIVE, root=ROOT)
        summary = reports.summarize(found)
        blocking = [f.render() for f in summary["findings"] if f.severity in ("blocking", "major")]
        self.assertEqual(blocking, [])

    def test_its_judgments_pin_a_persona_version_the_registry_still_honours(self):
        for judgment in sorted((LIVE / "judgments").glob("*/*.md")):
            with self.subTest(judgment.name):
                metadata, _ = frontmatter.read(judgment)
                versions.require_versions(metadata, root=ROOT, artifact=str(judgment))


if __name__ == "__main__":
    unittest.main()
