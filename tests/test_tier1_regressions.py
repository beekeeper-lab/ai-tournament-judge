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
from atj import (canon, demo, event as event_module, frontmatter, render, reports,
                 scoring, versions)
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
        remove the only control standing over an invented one. `matchup-passes/`
        was the live example until D22 declared it; the property is about any
        directory the framework does not know.
        """
        temporary, directory = sandbox(SAMPLE)
        try:
            stray = directory / "working-notes"
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


class AuditFindingsScopeTheGate(unittest.TestCase):
    """D16: the stage completion gate had no scope filter.

    `can_advance` branched on an audit's verdict alone, so a finding against a
    framework document, an ignored path, or activity-log prose held a stage gate
    exactly as hard as a wrong score. live-trial-2026's `judgments-audited` gate
    took three passes and five repair rounds, and those repair rounds produced
    five new defects.
    """

    def audit(self, **overrides) -> dict:
        base = {
            "event_id": demo.EVENT_ID,
            "audit_scope": "initial-judging stage",
            "audit_id": "judging",
            "rubric": canon.load(ROOT).reference,
            "persona": versions.load_personas(ROOT)["judging-auditor"].reference,
            "framework_commit": "uncommitted",
            "started_at": "2026-05-18T09:00:00Z",
            "completed_at": "2026-05-18T10:00:00Z",
            "visibility": "private",
            "approval_state": "approved",
            "validation_state": "valid",
            "result": "FAIL",
        }
        base.update(overrides)
        return base

    def finding(self, **overrides) -> dict:
        base = {"id": "F1", "severity": "major", "scope": "framework",
                "blocking": False, "summary": "the fix plan says three, not four"}
        base.update(overrides)
        return base

    def test_a_framework_finding_does_not_hold_an_event_gate(self):
        metadata = self.audit(findings=[self.finding(), self.finding(id="F2")])
        self.assertEqual(event_module.gate_findings_problems(metadata, "judging.md"), [])
        self.assertIn(
            "the gate opened",
            event_module.gate_opens_over_a_failing_verdict(metadata) or "",
        )

    def test_an_event_blocking_finding_holds_the_gate(self):
        metadata = self.audit(findings=[
            self.finding(),
            self.finding(id="F3", scope="event", blocking=True,
                         summary="team-lumen's total does not reproduce"),
        ])
        problems = event_module.gate_findings_problems(metadata, "judging.md")
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("F3", problems[0])
        self.assertIsNone(event_module.gate_opens_over_a_failing_verdict(metadata))

    def test_an_event_finding_the_auditor_did_not_mark_blocking_does_not_hold(self):
        """`blocking` is the auditor's judgment, not a function of severity."""
        metadata = self.audit(findings=[
            self.finding(id="F4", severity="major", scope="event", blocking=False,
                         summary="activity-log prose is imprecise; history is correct"),
        ])
        self.assertEqual(event_module.gate_findings_problems(metadata, "judging.md"), [])

    def test_a_failing_audit_with_no_findings_still_holds_the_gate(self):
        metadata = self.audit(findings=[])
        problems = event_module.gate_findings_problems(metadata, "judging.md")
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("no findings are recorded", problems[0])

    def test_without_findings_the_verdict_alone_still_decides(self):
        """Fifteen committed audits carry no `findings:`. None may change meaning."""
        self.assertEqual(
            len(event_module.gate_findings_problems(self.audit(), "judging.md")), 1
        )
        self.assertEqual(
            event_module.gate_findings_problems(
                self.audit(result="PASS WITH ADVISORIES"), "judging.md"
            ),
            [],
        )
        self.assertIsNone(
            event_module.gate_opens_over_a_failing_verdict(self.audit())
        )

    def test_the_committed_audits_are_unaffected(self):
        """Fifteen audits across two completed events carry no `findings:`.

        None of them may change meaning, and none may start holding a gate it
        did not hold before.
        """
        audits = sorted((ROOT / "events").glob("*/audits/*.md"))
        self.assertGreaterEqual(len(audits), 15)
        for audit in audits:
            with self.subTest(audit=str(audit.relative_to(ROOT))):
                metadata, _ = frontmatter.read(audit)
                self.assertNotIn("findings", metadata)
                passing = metadata["result"] in event_module.PASS_RESULTS
                problems = event_module.gate_findings_problems(metadata, audit.name)
                self.assertEqual(problems == [], passing, problems)

    def test_an_opened_gate_is_written_into_the_ledger(self):
        temporary, directory = sandbox(SAMPLE)
        try:
            audit = directory / "audits" / "judging-scoped.md"
            metadata = self.audit(findings=[self.finding()])
            metadata["event_id"] = demo.EVENT_ID
            audit.write_text(
                frontmatter.dump(metadata, "\n# Judging Audit\n\nOne framework finding.\n"),
                encoding="utf-8",
            )
            code, output = run_cli(
                "event", "gate", str(directory), "judgments-audited", "passed",
                "--audit", str(audit),
            )
            self.assertEqual(code, 0, output)
            self.assertIn("the gate opened", output)
            status, _ = frontmatter.read(directory / "status.md")
            self.assertIn("judgments-audited", status.get("gate_notes", {}))
        finally:
            shutil.rmtree(temporary)


class AuditsHaveASchema(unittest.TestCase):
    """D26: the artifact kind that authorizes every stage transition had none.

    `atj/reports.py` mapped `audits` to no schema at all, so the one artifact a
    gate reads was the least validated in the framework.
    """

    def test_audits_are_routed_to_a_schema(self):
        from atj import reports as reports_module

        self.assertEqual(reports_module.ARTIFACT_KINDS["audits"][0], "audit")

    def test_every_committed_audit_validates(self):
        from atj import schema as schema_module

        audits = sorted((ROOT / "events").glob("*/audits/*.md"))
        self.assertGreaterEqual(len(audits), 15)
        for audit in audits:
            with self.subTest(audit=str(audit.relative_to(ROOT))):
                metadata, _ = frontmatter.read(audit)
                self.assertEqual(
                    schema_module.validate("audit", metadata, root=ROOT, artifact=str(audit)),
                    [],
                )

    def test_a_bogus_verdict_is_rejected(self):
        from atj import schema as schema_module

        metadata, _ = frontmatter.read(SAMPLE / "audits" / "final-event.md")
        metadata["result"] = "MOSTLY FINE"
        self.assertTrue(schema_module.validate("audit", metadata, root=ROOT))

    def test_a_public_audit_is_rejected(self):
        from atj import schema as schema_module

        metadata, _ = frontmatter.read(SAMPLE / "audits" / "final-event.md")
        metadata["visibility"] = "public"
        self.assertTrue(schema_module.validate("audit", metadata, root=ROOT))

    def test_a_malformed_finding_is_rejected(self):
        from atj import schema as schema_module

        metadata, _ = frontmatter.read(SAMPLE / "audits" / "final-event.md")
        metadata["findings"] = [{"id": "F1", "severity": "major", "scope": "elsewhere",
                                 "blocking": True, "summary": "x"}]
        self.assertTrue(schema_module.validate("audit", metadata, root=ROOT))

    def test_the_template_still_ships_a_draft_and_says_how_to_move_it(self):
        text = (ROOT / "framework" / "templates" / "audit-report.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("approval_state: draft", text)
        self.assertIn("atj event approve", text)


class ApprovalStateCanBeWritten(unittest.TestCase):
    """D25: six sites read `approval_state` and nothing could set it.

    Sixteen live-trial-2026 artifacts reached the final gate still `draft` while
    their stage gates read `passed`, including both team dossiers —
    `atj/ceremony.py:372` refuses to render a dossier that is not approved, so
    neither deliverable could be released under a gate named `dossiers-approved`.
    `demo_writer.py` writes `approved` directly, so the sample event could not
    catch it.
    """

    def test_approving_sets_the_state_and_names_the_official(self):
        temporary, directory = sandbox(SAMPLE)
        try:
            target = directory / "audits" / "bracket.md"
            metadata, body = frontmatter.read(target)
            metadata["approval_state"] = "draft"
            metadata["validation_state"] = "unvalidated"
            target.write_text(frontmatter.dump(metadata, body), encoding="utf-8")

            code, output = run_cli("event", "approve", str(target), "--event-dir", str(directory))
            self.assertEqual(code, 0, output)
            after, _ = frontmatter.read(target)
            self.assertEqual(after["approval_state"], "approved")
            self.assertEqual(after["validation_state"], "valid")
            self.assertTrue(after["approved_by"])
            self.assertTrue(after["approved_at"])
        finally:
            shutil.rmtree(temporary)

    def test_an_invalid_artifact_is_not_approved(self):
        """An approval says a human reviewed a valid artifact. Nothing is written."""
        temporary, directory = sandbox(SAMPLE)
        try:
            target = directory / "audits" / "bracket.md"
            metadata, body = frontmatter.read(target)
            metadata["approval_state"] = "draft"
            metadata["result"] = "MOSTLY FINE"
            target.write_text(frontmatter.dump(metadata, body), encoding="utf-8")

            code, output = run_cli("event", "approve", str(target), "--event-dir", str(directory))
            self.assertEqual(code, 1, output)
            self.assertIn("Refused", output)
            self.assertEqual(frontmatter.read(target)[0]["approval_state"], "draft")
        finally:
            shutil.rmtree(temporary)

    def test_withdrawing_clears_the_approving_official(self):
        temporary, directory = sandbox(SAMPLE)
        try:
            target = directory / "audits" / "bracket.md"
            run_cli("event", "approve", str(target), "--event-dir", str(directory))
            self.assertIn("approved_by", frontmatter.read(target)[0])
            code, output = run_cli(
                "event", "approve", str(target), "--state", "withdrawn",
                "--event-dir", str(directory),
            )
            self.assertEqual(code, 0, output)
            after, _ = frontmatter.read(target)
            self.assertEqual(after["approval_state"], "withdrawn")
            self.assertNotIn("approved_by", after)
        finally:
            shutil.rmtree(temporary)

    def test_approval_unblocks_the_gate_the_template_would_have_blocked(self):
        """The D25/D26 pair, end to end: template draft -> approve -> gate opens."""
        temporary, directory = sandbox(SAMPLE)
        try:
            template = ROOT / "framework" / "templates" / "audit-report.md"
            metadata, template_body = frontmatter.read(template)
            metadata.update({
                "event_id": demo.EVENT_ID,
                "audit_scope": "bracket stage",
                "audit_id": "bracket-fresh",
                "commit": None,
                "evidence_package_id": None,
                "rubric": canon.load(ROOT).reference,
                "persona": versions.load_personas(ROOT)["judging-auditor"].reference,
                "framework_commit": "uncommitted",
                "model_requested": "claude-opus-5",
                "model_used": "claude-opus-5",
                "started_at": "2026-05-18T09:00:00Z",
                "completed_at": "2026-05-18T10:00:00Z",
                "result": "PASS",
                "findings": [],
            })
            audit = directory / "audits" / "bracket-fresh.md"
            # The template's own body, so the required sections are present and
            # this is the path an auditor actually walks.
            body = template_body.replace("**FAIL** until all blocking findings are resolved.",
                                         "**PASS.** The draw reproduces.")
            audit.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
            self.assertEqual(metadata["approval_state"], "draft")
            problems = event_module.audit_supports_gate(
                audit, stage="bracket", root=ROOT, event_id=demo.EVENT_ID
            )
            self.assertTrue(any("approval_state" in p for p in problems), problems)

            code, output = run_cli("event", "approve", str(audit), "--event-dir", str(directory))
            self.assertEqual(code, 0, output)
            self.assertEqual(
                event_module.audit_supports_gate(
                    audit, stage="bracket", root=ROOT, event_id=demo.EVENT_ID
                ),
                [],
            )
        finally:
            shutil.rmtree(temporary)


class UnroutedTemplatesAreRouted(unittest.TestCase):
    """D27: two templates described artifacts the validator had no kind for.

    `calibration-report.md` invited `persona: PANEL-VERSIONS` and
    `manual-override-record.md` invited `persona: HUMAN-OFFICIAL` — neither can
    resolve in the registry and neither contained a string from
    `reports.PLACEHOLDERS`, so an author who left either in place got no finding
    at all. The larger half was that neither artifact had a kind in
    `ARTIFACT_KINDS` or a directory in `EVENT_SUBDIRS`, so nothing written from
    them was validated by anything. `manual-override-record.md` is the artifact
    for a human overriding a tool result, which is the last one that should be
    unchecked.
    """

    TEMPLATES = ("calibration-report.md", "manual-override-record.md")

    def test_the_old_persona_values_are_gone(self):
        for name in self.TEMPLATES:
            with self.subTest(template=name):
                text = (ROOT / "framework" / "templates" / name).read_text(encoding="utf-8")
                self.assertNotIn("persona: PANEL-VERSIONS", text)
                self.assertNotIn("persona: HUMAN-OFFICIAL\n", text)
                self.assertIn("persona: PERSONA@VERSION", text)

    def test_every_template_persona_is_caught_as_a_placeholder(self):
        """The class, not the two known cases.

        An unreplaced persona must be caught as a placeholder before the work is
        done, not as `unknown persona` after it — the ruling D10 made for the
        adjudication template, applied to every template that invites one.
        """
        from atj import reports as reports_module

        for template in sorted((ROOT / "framework" / "templates").glob("*.md")):
            metadata, _ = frontmatter.read(template)
            persona = str(metadata.get("persona") or "")
            if not persona:
                continue
            with self.subTest(template=template.name):
                recognised = any(
                    holder in persona for holder in reports_module.PLACEHOLDERS
                ) or persona.endswith("@VERSION")
                self.assertTrue(
                    recognised,
                    f"{template.name} invites persona {persona!r}, which no "
                    f"placeholder rule recognises",
                )

    def test_an_unreplaced_persona_is_a_placeholder_finding(self):
        temporary, directory = sandbox(SAMPLE)
        try:
            target = directory / "audits" / "bracket.md"
            metadata, body = frontmatter.read(target)
            metadata["persona"] = "judging-auditor@VERSION"
            target.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
            findings = reports.validate_artifact(target, directory, root=ROOT).blocking
            self.assertIn("placeholder", [f.rule for f in findings])
        finally:
            shutil.rmtree(temporary)

    def test_both_kinds_are_routed_with_a_schema(self):
        from atj import reports as reports_module

        for kind, schema_name, template in (
            ("calibrations", "calibration", "calibration-report.md"),
            ("overrides", "manual-override", "manual-override-record.md"),
        ):
            with self.subTest(kind=kind):
                self.assertEqual(
                    reports_module.ARTIFACT_KINDS[kind], (schema_name, template)
                )

    def test_every_routed_kind_has_somewhere_to_live(self):
        from atj import publication as publication_module
        from atj import reports as reports_module

        for kind in reports_module.ARTIFACT_KINDS:
            with self.subTest(kind=kind):
                self.assertIn(kind, event_module.ALL_EVENT_SUBDIRS)
                self.assertIn(kind, publication_module.DIRECTORY_VISIBILITY)

    def test_the_new_directories_are_optional(self):
        """Neither completed event may become invalid for lacking a directory.

        live-trial-2026 does hold `matchup-passes/`, which D22 later declared as
        the home for a single order-balanced pass. The property under test is that
        an optional directory is never required, not that no event has one.
        """
        for name in ("live-trial-2026", demo.EVENT_ID):
            with self.subTest(event=name):
                directory = ROOT / "events" / name
                loaded = event_module.load(directory, root=ROOT)
                self.assertEqual(event_module.validate_configuration(loaded), [])
        for optional in event_module.OPTIONAL_EVENT_SUBDIRS:
            with self.subTest(optional=optional):
                self.assertNotIn(optional, event_module.EVENT_SUBDIRS)

    def test_a_new_event_gets_them(self):
        temporary = Path(tempfile.mkdtemp())
        try:
            created = event_module.initialize(
                "probe-2027", event_name="Probe", destination=temporary, root=ROOT
            )
            for subdir in event_module.ALL_EVENT_SUBDIRS:
                self.assertTrue((created / subdir).is_dir(), subdir)
        finally:
            shutil.rmtree(temporary)

    def test_an_artifact_written_from_each_template_is_validated(self):
        temporary, directory = sandbox(SAMPLE)
        try:
            written = self.write_both(directory)
            for path in written:
                with self.subTest(artifact=path.name):
                    report = reports.validate_artifact(path, directory, root=ROOT)
                    self.assertIsNotNone(report.kind)
                    self.assertEqual(report.findings, [])

            # And the old placeholder now fails, blocking, on shape.
            override = directory / "overrides" / "record-01.md"
            metadata, body = frontmatter.read(override)
            metadata["persona"] = "HUMAN-OFFICIAL"
            override.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
            findings = reports.validate_artifact(override, directory, root=ROOT).blocking
            self.assertTrue(findings)
            self.assertIn("schema", [f.rule for f in findings])
        finally:
            shutil.rmtree(temporary)

    def test_the_disclosure_gate_reaches_them(self):
        """Before this they were `location-unknown`, which fails closed but says
        nothing useful. A private artifact kind should be routed, not blocked."""
        temporary, directory = sandbox(SAMPLE)
        try:
            self.write_both(directory)
            code, output = run_cli("validate", "publication", str(directory))
            self.assertEqual(code, 0, output)
            self.assertNotIn("location-unknown", output)
        finally:
            shutil.rmtree(temporary)

    def write_both(self, directory: Path) -> list[Path]:
        """One artifact of each kind, built from its own template."""
        written = []
        for subdir, template, overrides in (
            ("overrides", "manual-override-record.md", {
                "override_id": "ovr-01", "scope": "team", "team_id": "team-lumen",
                "match_id": None, "authorized_by": "event-director",
                "model_requested": "not-applicable", "model_used": "not-applicable",
            }),
            ("calibrations", "calibration-report.md", {
                "calibration_id": "cal-01", "scope": "pre-event-calibration",
                "sample_id": "sample-a", "team_id": None,
                "model_requested": "claude-opus-5", "model_used": "claude-opus-5",
            }),
        ):
            metadata, body = frontmatter.read(
                ROOT / "framework" / "templates" / template
            )
            metadata.update(overrides)
            metadata.update({
                "event_id": demo.EVENT_ID, "commit": None,
                "evidence_package_id": None,
                "rubric": canon.load(ROOT).reference,
                "persona": versions.load_personas(ROOT)["judging-auditor"].reference,
                "framework_commit": "uncommitted",
                "started_at": "2026-05-18T09:00:00Z",
                "completed_at": "2026-05-18T09:30:00Z",
            })
            target = directory / subdir
            target.mkdir(exist_ok=True)
            path = target / "record-01.md"
            path.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
            written.append(path)
        return written
