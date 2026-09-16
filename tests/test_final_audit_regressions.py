"""Regressions for the final independent release audit.

Every one of these passed the previous 244-test suite. Each test names the
finding it locks down.
"""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from _support import ROOT  # noqa: F401
from atj import bracket, ceremony, demo, event as event_module, frontmatter, publication, reports
from atj.cli import main as cli_main
from atj.errors import ValidationError

EVENT_DIR = ROOT / "events" / demo.EVENT_ID


def sandbox_event():
    directory = Path(tempfile.mkdtemp())
    shutil.copytree(EVENT_DIR, directory / "event")
    return directory, directory / "event"


class CleanCheckoutTests(unittest.TestCase):
    """F1: git tracks no empty directory, so `runs/` was missing on checkout."""

    def test_every_event_subdirectory_is_tracked(self):
        listed = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", f"events/{demo.EVENT_ID}/"],
            capture_output=True, text=True, check=False,
        )
        tracked = {Path(line).parts[2] for line in listed.stdout.splitlines()
                   if len(Path(line).parts) > 3}
        for subdir in event_module.EVENT_SUBDIRS:
            self.assertIn(subdir, tracked, f"{subdir}/ has no tracked file")

    def test_the_generator_writes_a_keepfile_into_each_subdirectory(self):
        for subdir in event_module.EVENT_SUBDIRS:
            directory = EVENT_DIR / subdir
            self.assertTrue(directory.is_dir(), subdir)
            self.assertTrue(any(directory.iterdir()), f"{subdir}/ is empty")


class ConsolidationVerificationTests(unittest.TestCase):
    """F2: a summary's official total was never compared to its judgments."""

    def test_the_committed_summaries_verify(self):
        self.assertEqual(
            reports.check_consolidation(EVENT_DIR, root=ROOT, expected_judges=demo.JUDGES), []
        )

    def test_a_tampered_total_is_caught(self):
        holder, event_dir = sandbox_event()
        try:
            path = event_dir / "summaries" / "team-quill.md"
            metadata, body = frontmatter.read(path)
            metadata["display_total"] = 99.9
            path.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
            findings = reports.check_consolidation(
                event_dir, root=ROOT, expected_judges=demo.JUDGES
            )
            self.assertTrue(any(f.rule == "consolidation" for f in findings))
            self.assertTrue(all(f.severity == "blocking" for f in findings))
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_a_judgment_edited_after_consolidation_is_caught(self):
        holder, event_dir = sandbox_event()
        try:
            path = event_dir / "judgments" / "team-lumen" / "judge-backend.md"
            metadata, body = frontmatter.read(path)
            metadata["scores"]["functional"] = 1
            path.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
            findings = reports.check_consolidation(
                event_dir, root=ROOT, expected_judges=demo.JUDGES
            )
            self.assertTrue(findings)
        finally:
            shutil.rmtree(holder, ignore_errors=True)


class AdjudicationApplicationTests(unittest.TestCase):
    """F3: no operator command could produce the sample event's own total."""

    def test_the_cli_reproduces_the_committed_total(self):
        self.assertEqual(
            cli_main(["--root", str(ROOT), "score",
                      str(EVENT_DIR / "judgments" / "team-lumen")]), 0
        )

    def test_without_the_adjudication_the_total_is_blocked(self):
        holder, event_dir = sandbox_event()
        try:
            for path in (event_dir / "adjudications").glob("*.md"):
                path.unlink()
            self.assertEqual(
                cli_main(["--root", str(ROOT), "score",
                          str(event_dir / "judgments" / "team-lumen")]), 1
            )
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_a_draft_adjudication_does_not_unblock_a_total(self):
        from atj import scoring

        holder, event_dir = sandbox_event()
        try:
            for path in (event_dir / "adjudications").glob("*.md"):
                metadata, body = frontmatter.read(path)
                metadata["approval_state"] = "draft"
                path.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
            resolutions = scoring.load_resolutions(
                event_dir / "adjudications", team_id="team-lumen", root=ROOT
            )
            self.assertEqual(resolutions, {})
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_the_source_score_is_never_overwritten(self):
        from atj import scoring

        resolutions = scoring.load_resolutions(
            EVENT_DIR / "adjudications", team_id="team-lumen", root=ROOT
        )
        result = scoring.consolidate(
            scoring.load_panel(EVENT_DIR / "judgments" / "team-lumen", root=ROOT),
            expected_judges=demo.JUDGES, resolutions=resolutions, root=ROOT,
        )
        self.assertEqual(
            result["criteria"]["security"]["source_scores"]["judge-security-ops"], "NE"
        )
        self.assertTrue(result["finalized"])


class TeamFacingOutputTests(unittest.TestCase):
    """F4 and F5: team-facing content reached the public tree, ungated."""

    def test_no_dossier_output_lives_under_public(self):
        self.assertEqual(list((EVENT_DIR / "public").rglob("*dossier*")), [])

    def test_rendered_dossiers_are_in_the_team_facing_directory(self):
        for team in demo.TEAMS:
            self.assertTrue((EVENT_DIR / "dossiers" / f"{team.id}.html").is_file(), team.id)

    def test_html_in_a_public_location_is_gated(self):
        holder, event_dir = sandbox_event()
        try:
            leaked = event_dir / "public" / "ceremony" / "leak.html"
            leaked.write_text("<p>score 91.5 / 100 key AKIAIOSFODNN7EXAMPLE</p>", encoding="utf-8")
            found = reports.validate_event_reports(
                event_dir, root=ROOT, public_scores=False,
                all_teams=[t.id for t in demo.TEAMS], expected_judges=demo.JUDGES,
            )
            rules = {f.rule for report in found for f in report.findings}
            self.assertIn("secret", rules)
            self.assertIn("unapproved-score", rules)
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_another_team_s_score_in_a_dossier_blocks(self):
        findings = publication.check_team_facing(
            {"team_id": "team-quill", "visibility": "team"},
            "team-harbor scored 53.3 / 100 in this event.",
            own_team="team-quill", all_teams=["team-quill", "team-harbor"],
        )
        self.assertTrue(any(f.severity == "blocking" and f.rule == "foreign-team"
                            for f in findings))

    def test_another_team_s_finding_in_a_dossier_is_major(self):
        findings = publication.check_team_facing(
            {"team_id": "team-quill", "visibility": "team"},
            "team-harbor had a broken correlation heuristic.",
            own_team="team-quill", all_teams=["team-quill", "team-harbor"],
        )
        self.assertTrue(any(f.severity == "major" for f in findings))

    def test_a_bare_opponent_mention_stays_advisory(self):
        findings = publication.check_team_facing(
            {"team_id": "team-quill", "visibility": "team"},
            "You met team-harbor in the semifinal.",
            own_team="team-quill", all_teams=["team-quill", "team-harbor"],
        )
        self.assertTrue(findings)
        self.assertTrue(all(f.severity == "advisory" for f in findings))

    def test_personal_data_blocks_anywhere(self):
        for payload in (
            "reach the lead at ada.lovelace@example-school.edu",
            "call 555-123-4567",
            "student id: 8842991",
        ):
            self.assertTrue(publication.scan_pii(payload), payload)

    def test_a_version_reference_is_not_mistaken_for_an_email(self):
        self.assertEqual(publication.scan_pii("persona: judge-backend@1.0.0"), [])

    def test_a_team_may_see_its_own_identifiers(self):
        findings = publication.scan_private_identifiers(
            "ev:demo:team-quill:0123456789ab:deadbeef", own_team="team-quill"
        )
        self.assertEqual(findings, [])
        findings = publication.scan_private_identifiers(
            "ev:demo:team-harbor:0123456789ab:deadbeef", own_team="team-quill"
        )
        self.assertTrue(findings)


class ScoresPublishedTests(unittest.TestCase):
    """F6: an artifact's own flag overrode the event official."""

    def test_an_artifact_cannot_authorize_its_own_disclosure(self):
        findings = publication.check_public(
            {"event_id": "demo", "visibility": "public", "approval_state": "approved",
             "approved_by": "official", "source_artifacts": ["x"], "scores_published": True},
            "The final score was 91.5 / 100.", public_scores=False,
        )
        self.assertTrue(any(f.rule == "unapproved-score" for f in findings))
        self.assertGreaterEqual(len([f for f in findings if f.rule == "unapproved-score"]), 2)


class AdvancementTests(unittest.TestCase):
    """F7: no winner was ever recorded and match ids contradicted the reports."""

    def setUp(self):
        self.drawn = json.loads((EVENT_DIR / "bracket.json").read_text(encoding="utf-8"))

    def test_every_match_records_its_winner(self):
        for entry in self.drawn["rounds"]:
            for match in entry["matches"]:
                self.assertIsNotNone(match["winner"], match["match_id"])

    def test_the_final_entrants_were_carried_forward(self):
        final = self.drawn["rounds"][-1]["matches"][0]
        self.assertEqual(len([e for e in final["entrants"] if e]), 2)

    def test_match_ids_agree_with_the_matchup_reports(self):
        records = []
        for path in sorted((EVENT_DIR / "matchups").glob("*.md")):
            metadata, _ = frontmatter.read(path)
            records.append((metadata["match_id"], metadata["team_a"],
                            metadata["team_b"], metadata.get("winner")))
        self.assertEqual(bracket.check_matchup_records(self.drawn, records), [])

    def test_a_contradicting_matchup_record_is_caught(self):
        self.assertTrue(bracket.check_matchup_records(
            self.drawn,
            [("mu:sample-mock-2026:final:01", "team-lumen", "team-harbor", None)],
        ))

    def test_advancing_a_non_entrant_is_refused(self):
        with self.assertRaises(ValidationError):
            bracket.advance(json.loads(json.dumps(self.drawn)),
                            "mu:sample-mock-2026:final:01", "team-verdant")

    def test_rewriting_a_recorded_winner_is_refused(self):
        with self.assertRaises(ValidationError):
            bracket.advance(json.loads(json.dumps(self.drawn)),
                            "mu:sample-mock-2026:final:01", "team-quill")

    def test_the_cli_refuses_to_advance_an_unresolved_matchup(self):
        holder, event_dir = sandbox_event()
        try:
            for path in (event_dir / "adjudications").glob("*semifinal*"):
                path.unlink()
            path = event_dir / "matchups" / "semifinal-2.md"
            metadata, body = frontmatter.read(path)
            self.assertEqual(metadata["outcome"], "adjudication-required")
            self.assertIsNone(metadata["winner"])
            drawn = json.loads((event_dir / "bracket.json").read_text(encoding="utf-8"))
            for entry in drawn["rounds"]:
                for match in entry["matches"]:
                    match["winner"] = None
            (event_dir / "bracket.json").write_text(json.dumps(drawn), encoding="utf-8")
            self.assertEqual(cli_main([
                "--root", str(ROOT), "bracket", "advance",
                str(event_dir / "bracket.json"), "--match", metadata["match_id"],
                "--from", str(path), "--event-dir", str(event_dir),
            ]), 1)
        finally:
            shutil.rmtree(holder, ignore_errors=True)


class UnitLedgerTests(unittest.TestCase):
    """F8: staleness was library code no command called."""

    def test_the_committed_ledger_is_current(self):
        loaded = event_module.load(EVENT_DIR, root=ROOT)
        self.assertEqual(event_module.stale_units(loaded), [])
        self.assertTrue(loaded.status["units"])

    def test_an_edited_judgment_makes_its_unit_stale(self):
        holder, event_dir = sandbox_event()
        try:
            path = event_dir / "judgments" / "team-lumen" / "judge-backend.md"
            path.write_text(path.read_text(encoding="utf-8") + "\nAn edit.\n", encoding="utf-8")
            loaded = event_module.load(event_dir, root=ROOT)
            drifted = {entry["unit_id"] for entry in event_module.stale_units(loaded)}
            self.assertIn("judging:team-lumen", drifted)
            self.assertEqual(
                event_module.next_action(loaded)["action"], "rerun-stale-units"
            )
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_the_unit_command_reports_drift(self):
        holder, event_dir = sandbox_event()
        try:
            path = event_dir / "evidence" / "team-quill" / "manifest.md"
            path.write_text(path.read_text(encoding="utf-8") + "\nAn edit.\n", encoding="utf-8")
            self.assertEqual(
                cli_main(["--root", str(ROOT), "event", "unit", str(event_dir), "list"]), 1
            )
        finally:
            shutil.rmtree(holder, ignore_errors=True)


class GateTests(unittest.TestCase):
    """F9: a gate was a boolean with no audit behind it."""

    def event(self):
        holder, event_dir = sandbox_event()
        loaded = event_module.load(event_dir, root=ROOT)
        return holder, event_dir, loaded

    def test_passing_a_gate_requires_an_audit_artifact(self):
        holder, event_dir, _ = self.event()
        try:
            self.assertEqual(cli_main([
                "--root", str(ROOT), "event", "gate", str(event_dir),
                "bracket-audited", "passed",
            ]), 2)
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_a_failing_audit_cannot_pass_a_gate(self):
        holder, event_dir, _ = self.event()
        try:
            self.assertEqual(cli_main([
                "--root", str(ROOT), "event", "gate", str(event_dir),
                "consolidation-audited", "passed",
                "--audit", "audits/consolidation-team-lumen-01.md",
            ]), 1)
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_a_passing_audit_passes_the_gate(self):
        holder, event_dir, _ = self.event()
        try:
            self.assertEqual(cli_main([
                "--root", str(ROOT), "event", "gate", str(event_dir),
                "consolidation-audited", "passed",
                "--audit", "audits/consolidation-team-lumen-02.md",
            ]), 0)
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_a_stage_with_no_work_cannot_advance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for item in ("framework", "schemas", "events", ".claude"):
                shutil.copytree(ROOT / item, root / item)
            target = event_module.initialize("empty-event", root=root)
            path = target / "teams.md"
            metadata, _ = frontmatter.read(path)
            path.write_text(frontmatter.dump(metadata, """
| Team ID | Display name | Affiliation group | Previous result | Submission status | Eligible |
|---|---|---|---|---|---|
| team-one | One | school-a | none | received | yes |
| team-two | Two | school-b | none | received | yes |
"""), encoding="utf-8")
            loaded = event_module.load(target, root=root)
            loaded.status["current_stage"] = "initial-judging"
            loaded.status["stage_gates"]["judgments-audited"] = "passed"
            allowed, reasons = event_module.can_advance(loaded)
            self.assertFalse(allowed)
            self.assertTrue(any("no completed work" in reason for reason in reasons))


class IndependenceDetectorTests(unittest.TestCase):
    """F10: independence was asserted and never observed."""

    def test_the_committed_judgments_are_not_near_duplicates(self):
        self.assertEqual(reports.check_judge_independence(EVENT_DIR), [])

    def test_a_copied_report_is_detected(self):
        holder, event_dir = sandbox_event()
        try:
            source = event_dir / "judgments" / "team-lumen" / "judge-backend.md"
            target = event_dir / "judgments" / "team-lumen" / "judge-frontend-ux.md"
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            findings = reports.check_judge_independence(event_dir)
            self.assertTrue(any(f.rule == "independence" for f in findings))
        finally:
            shutil.rmtree(holder, ignore_errors=True)


class CeremonyRenderingTests(unittest.TestCase):
    """F14 and F16: unescaped fields, and a silently dropped results table."""

    def test_the_approved_results_table_is_rendered(self):
        html = ceremony.render_ceremony(EVENT_DIR)
        self.assertIn("<table>", html)
        self.assertIn("Champion", html)

    def test_markup_in_a_bracket_field_cannot_reach_the_page(self):
        holder, event_dir = sandbox_event()
        try:
            path = event_dir / "bracket.json"
            drawn = json.loads(path.read_text(encoding="utf-8"))
            drawn["team_count"] = "4</p><script>alert(1)</script><p>"
            path.write_text(json.dumps(drawn), encoding="utf-8")
            with self.assertRaises(ValidationError):
                ceremony.render_ceremony(event_dir)
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_the_current_round_reflects_recorded_winners(self):
        self.assertIn("Current round: <strong>final", ceremony.render_ceremony(EVENT_DIR))


class AtomicLedgerTests(unittest.TestCase):
    """F15: an interrupt during a ledger write destroyed the recovery record."""

    def test_a_backup_is_kept_and_the_write_is_atomic(self):
        holder, event_dir = sandbox_event()
        try:
            loaded = event_module.load(event_dir, root=ROOT)
            loaded.status["blocked"] = True
            loaded.status["blocked_reason"] = "test"
            event_module.save_status(loaded)
            self.assertTrue((event_dir / "status.md.bak").is_file())
            self.assertFalse((event_dir / "status.md.tmp").exists())
            reloaded = event_module.load(event_dir, root=ROOT)
            self.assertTrue(reloaded.status["blocked"])
        finally:
            shutil.rmtree(holder, ignore_errors=True)


class PackagedInstallTests(unittest.TestCase):
    """F11: the wheel shipped code with none of the data it reads."""

    def test_the_staging_tool_collects_every_data_tree(self):
        completed = subprocess.run(
            [sys.executable, "tools/stage_package_data.py"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        staged = ROOT / "atj" / "data"
        try:
            for required in ("framework/rubrics/submission-evaluation.md",
                             "schemas/common.schema.json",
                             "events/_template/event.md", "VERSION"):
                self.assertTrue((staged / required).is_file(), required)
        finally:
            shutil.rmtree(staged, ignore_errors=True)

    def test_staged_data_is_excluded_from_source_scans(self):
        from atj.cli import check_no_duplicate_weights

        staged = ROOT / "atj" / "data"
        subprocess.run([sys.executable, "tools/stage_package_data.py"],
                       cwd=ROOT, capture_output=True, check=False)
        try:
            self.assertEqual(check_no_duplicate_weights(ROOT), [])
        finally:
            shutil.rmtree(staged, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
