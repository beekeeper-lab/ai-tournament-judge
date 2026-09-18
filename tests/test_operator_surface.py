"""The advisories the release's final audit left open, closed.

`docs/final-audit.md` ended in ten advisories and a list of what a human must do
before the framework decides anything real. Four of those advisories were about
the framework being quieter than it should be: a control nobody could list, a
runtime whose privilege mode it reported without judging, a contamination signal
it never looked at, and a weaker check that exited zero. Each test names the
advisory it closes.
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from atj.cli import main as cli_main
from _support import ROOT  # noqa: F401
from atj import (demo, event as event_module, frontmatter, publication, reports,
                 sandbox)
from atj.errors import StateError

SAMPLE = ROOT / "events" / demo.EVENT_ID
LIVE = ROOT / "events" / "live-trial-2026"


def event_copy(source: Path) -> tuple[Path, Path]:
    holder = Path(tempfile.mkdtemp())
    shutil.copytree(source, holder / "event")
    return holder, holder / "event"


class OverridesCanBeReviewed(unittest.TestCase):
    """Advisory 6: "No command currently summarises `status.overrides`."

    `--force-reason` is the one door through every gate the framework enforces,
    and the record it wrote could only be read by opening status.md by hand.
    """

    def force(self, event: Path) -> None:
        loaded = event_module.load(event, root=ROOT)
        event_module.set_stage(loaded, "dossiers")
        loaded.status["stage_gates"]["dossiers-approved"] = "pending"
        event_module.save_status(loaded)
        loaded = event_module.load(event, root=ROOT)
        event_module.advance(
            loaded,
            force_reason="the dossier audit is scheduled after the ceremony",
            force_approver="event-director",
        )
        event_module.save_status(loaded)

    def test_a_forced_advance_is_listed_and_unreviewed(self):
        holder, event = event_copy(LIVE)
        try:
            self.force(event)
            loaded = event_module.load(event, root=ROOT)
            recorded = event_module.overrides(loaded)
            self.assertEqual(len(recorded), 1)
            self.assertEqual(recorded[0]["authorized_by"], "event-director")
            self.assertTrue(recorded[0]["bypassed"])
            self.assertNotIn("reviewed_by", recorded[0])
            # Unreviewed is a non-zero exit: a script cannot miss it either.
            self.assertEqual(cli_main(["--root", str(ROOT), "event", "overrides", str(event)]), 1)
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_a_review_records_that_it_was_read_not_that_it_was_right(self):
        holder, event = event_copy(LIVE)
        try:
            self.force(event)
            self.assertEqual(
                cli_main([
                    "--root", str(ROOT), "event", "overrides", str(event),
                    "--review", "0", "--official", "event-director",
                    "--note", "read the dossier audit afterwards",
                ]), 0,
            )
            loaded = event_module.load(event, root=ROOT)
            entry = event_module.overrides(loaded)[0]
            self.assertEqual(entry["reviewed_by"], "event-director")
            self.assertIn("reviewed_at", entry)
            self.assertEqual(entry["review_note"], "read the dossier audit afterwards")
            self.assertEqual(cli_main(["--root", str(ROOT), "event", "overrides", str(event)]), 0)
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_reviewing_an_override_that_does_not_exist_is_an_error(self):
        holder, event = event_copy(LIVE)
        try:
            loaded = event_module.load(event, root=ROOT)
            with self.assertRaises(StateError):
                event_module.review_override(loaded, 0, official="event-director")
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_an_event_with_no_override_says_so_and_passes(self):
        for event in (LIVE, SAMPLE):
            with self.subTest(event.name):
                self.assertEqual(event_module.overrides(
                    event_module.load(event, root=ROOT)
                ), [])
                self.assertEqual(
                    cli_main(["--root", str(ROOT), "event", "overrides", str(event)]), 0
                )


class PreflightJudgesThePrivilegeMode(unittest.TestCase):
    """Advisory 9: it reported the mode and did not judge it.

    Under a rootful runtime a container escape from a submission is host root.
    """

    def capability(self, rootless):
        return sandbox.Capability(
            runtime="docker", version="27.0", available=True, rootless=rootless
        )

    def test_rootless_needs_no_warning(self):
        self.assertIsNone(self.capability(True).privilege_warning)

    def test_rootful_says_what_an_escape_costs(self):
        warning = self.capability(False).privilege_warning
        self.assertIn("host root", warning)

    def test_an_unknown_mode_is_treated_as_the_worse_one(self):
        warning = self.capability(None).privilege_warning
        self.assertIn("unknown", warning)
        self.assertIn("Treat it as rootful", warning)
        self.assertIn("privilege mode unknown", self.capability(None).summary())

    def test_an_unavailable_runtime_warns_about_nothing(self):
        capability = sandbox.Capability(
            runtime=None, version=None, available=False, rootless=None, reasons=["none found"]
        )
        self.assertIsNone(capability.privilege_warning)


class IdenticalScoreVectorsAreExamined(unittest.TestCase):
    """Advisory 1: the detector measured wording and ignored the numbers.

    Two judges can paraphrase differently and still have been shown each other's
    scores, which is the case the shingle overlap cannot see.
    """

    def test_a_matching_vector_is_reported_as_an_advisory(self):
        findings = reports.check_judge_independence(SAMPLE)
        identical = [f for f in findings if f.rule == "identical-scores"]
        self.assertTrue(identical, "the sample's scripted panels contain a matching pair")
        self.assertTrue(all(f.severity == "advisory" for f in identical), identical)

    def test_live_trial_had_no_matching_vector(self):
        findings = reports.check_judge_independence(LIVE)
        self.assertEqual([f for f in findings if f.rule == "identical-scores"], [])

    def test_making_two_judges_agree_exactly_is_detected(self):
        holder, event = event_copy(LIVE)
        try:
            team = event / "judgments" / "team-ledger"
            source, target = sorted(team.glob("*.md"))[:2]
            donor, _ = frontmatter.read(source)
            metadata, body = frontmatter.read(target)
            metadata["scores"] = dict(donor["scores"])
            target.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
            findings = reports.check_judge_independence(event)
            identical = [f for f in findings if f.rule == "identical-scores"]
            self.assertTrue(identical)
            self.assertIn(source.name, identical[0].detail)
            self.assertIn(target.name, identical[0].detail)
        finally:
            shutil.rmtree(holder, ignore_errors=True)


class TheWeakerBracketCheckIsAskedForByName(unittest.TestCase):
    """Advisory 2: it checked structure only, said so, and exited 0.

    An operator reading the label was not misled. A script reading the exit code
    was.
    """

    def test_the_bare_form_is_a_usage_error(self):
        self.assertEqual(
            cli_main(["--root", str(ROOT), "bracket", "verify",
                      str(SAMPLE / "bracket.json")]), 2
        )

    def test_structure_only_is_available_when_meant(self):
        self.assertEqual(
            cli_main(["--root", str(ROOT), "bracket", "verify",
                      str(SAMPLE / "bracket.json"), "--structure-only"]), 0
        )

    def test_the_full_checks_still_pass(self):
        for extra in (
            ["--event-dir", str(SAMPLE)],
            ["--reproduce", str(ROOT / "tests" / "fixtures" / "bracket-20-team" / "roster.json")],
        ):
            with self.subTest(extra[0]):
                target = (
                    SAMPLE / "bracket.json" if extra[0] == "--event-dir"
                    else ROOT / "tests" / "fixtures" / "bracket-20-team" / "bracket.json"
                )
                self.assertEqual(
                    cli_main(["--root", str(ROOT), "bracket", "verify", str(target), *extra]), 0
                )

    def test_no_committed_artifact_documents_the_bare_form(self):
        """A generated audit cited the bare command, which now errors.

        This is the D3/D18 shape: an artifact naming a command that does not work
        as written. The generator was fixed rather than the checker weakened.
        """
        for path in sorted(SAMPLE.rglob("*.md")):
            text = path.read_text(encoding="utf-8", errors="replace")
            for line in text.splitlines():
                stripped = line.strip()
                if "atj bracket verify" not in stripped or stripped.startswith("|"):
                    continue
                with self.subTest(f"{path.name}: {stripped[:60]}"):
                    self.assertTrue(
                        any(flag in text for flag in
                            ("--event-dir", "--reproduce", "--structure-only")),
                        stripped,
                    )


class TheScoreGateCoversMoreThanItsPatterns(unittest.TestCase):
    """Advisory 3: a total in a shape the patterns miss, with nothing to compare.

    `known_totals` closes the gap the patterns cannot -- and it is empty exactly
    when no total has been finalized, which is the case the advisory named.
    """

    def scan(self, text: str, *, known=()):
        return publication.scan_unapproved_scores(text, artifact="x", known_totals=known)

    def test_the_phrasings_the_patterns_used_to_miss(self):
        for text in (
            "The panel put them at 76.3 after review.",
            "Final tally: 76,3 of one hundred.",
            "They finished with 76.3 overall.",
            "Their score, as recorded, 76.3",
        ):
            with self.subTest(text):
                self.assertTrue(self.scan(text, known=[76.3]), text)
                self.assertTrue(self.scan(text), text)

    def test_a_suspected_total_with_no_finalized_total_is_major(self):
        findings = self.scan("The panel put them at 76.3 after review.")
        self.assertEqual(findings[0].severity, "major")
        self.assertIn("no finalized total", findings[0].detail)

    def test_the_same_number_with_a_finalized_total_is_blocking(self):
        findings = self.scan("The panel put them at 76.3 after review.", known=[76.3])
        self.assertTrue(any(f.severity == "blocking" for f in findings))

    def test_it_does_not_fire_on_versions_counts_or_rounds(self):
        for text in (
            "Built under submission-evaluation@1.1.0 at commit 9d21b770.",
            "The bracket has 4 teams and 0 byes.",
            "Round 1 of 2 complete.",
            "team-ledger advances to the final.",
            "Judged by judge-backend@1.1.0 and three others.",
        ):
            with self.subTest(text):
                self.assertEqual(self.scan(text), [], text)

    def test_the_committed_public_artifacts_stay_clean(self):
        for event in (SAMPLE, LIVE):
            for path in sorted((event / "public").glob("*.md")):
                with self.subTest(f"{event.name}/{path.name}"):
                    self.assertEqual(
                        publication.scan_unapproved_scores(
                            path.read_text(encoding="utf-8"), artifact=str(path)
                        ), [],
                    )


class ExecutionHasNowRunAgainstALiveRuntime(unittest.TestCase):
    """Advisory 4 was true when audited and is not now.

    The doc keeps the original sentence and records what changed. This pins the
    evidence, so the claim cannot rot in either direction.
    """

    def test_the_live_event_committed_real_run_records(self):
        records = sorted((LIVE / "runs").glob("*.json"))
        self.assertGreaterEqual(len(records), 27)
        for path in records:
            with self.subTest(path.name):
                record = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(record["runtime"], "podman")
                self.assertIn("--network none", record["command"])
                self.assertIn(":ro", record["command"])
                self.assertIn("--cap-drop ALL", record["command"])


class TheWheelCarriesItsOwnFramework(unittest.TestCase):
    """D31: the wheel installed a command that could not start.

        $ atj --version
        atj unknown
        $ atj release-check
        canon: framework root not found ... (no framework/rubrics/...)

    `tools/stage_package_data.py` existed to copy the canonical files into
    `atj/data/`, and its docstring said to run it in the build step. There was no
    build step that did -- only a line in `docs/release-checklist.md` telling a
    person to remember. These tests cover the wiring; CI builds the wheel and
    runs it outside the checkout, which is the only way to cover the rest.
    """

    def test_release_check_asserts_the_wiring(self):
        from atj.cli import check_packaging

        self.assertEqual(check_packaging(ROOT), [])

    def test_a_pyproject_that_drops_the_backend_fails(self):
        from atj.cli import check_packaging

        holder = Path(tempfile.mkdtemp())
        try:
            for name in ("VERSION", "pyproject.toml", "MANIFEST.in", "build_backend.py"):
                shutil.copy(ROOT / name, holder / name)
            (holder / "pyproject.toml").write_text(
                (holder / "pyproject.toml").read_text(encoding="utf-8").replace(
                    'build-backend = "build_backend"', 'build-backend = "setuptools.build_meta"'
                ),
                encoding="utf-8",
            )
            problems = check_packaging(holder)
            self.assertTrue(any("in-tree build backend" in p for p in problems), problems)
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_a_version_pyproject_disagreement_fails(self):
        from atj.cli import check_packaging

        holder = Path(tempfile.mkdtemp())
        try:
            for name in ("VERSION", "pyproject.toml", "MANIFEST.in", "build_backend.py"):
                shutil.copy(ROOT / name, holder / name)
            (holder / "VERSION").write_text("9.9.9-beta\n", encoding="utf-8")
            problems = check_packaging(holder)
            self.assertTrue(any("PEP 440" in p for p in problems), problems)
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_the_backend_refuses_to_build_without_data(self):
        """Neither a source tree nor a staged copy means no wheel, not a bad one."""
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "atj_build_backend_probe", ROOT / "build_backend.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        holder = Path(tempfile.mkdtemp())
        try:
            module.ROOT = holder
            with self.assertRaises(SystemExit) as raised:
                module._stage()
            self.assertIn("cannot start", str(raised.exception))
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_the_manifest_ships_what_a_wheel_build_needs(self):
        listed = (ROOT / "MANIFEST.in").read_text(encoding="utf-8")
        for needed in (
            "build_backend.py", "tools/stage_package_data.py", "framework", "schemas",
            "events/_template", "VERSION",
        ):
            with self.subTest(needed):
                self.assertIn(needed, listed)

    def test_ci_verifies_the_wheel_outside_the_checkout(self):
        workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("The wheel installs and runs outside the checkout", workflow)
        self.assertIn("atj release-check", workflow)


class AnApprovalHasAName(unittest.TestCase):
    """The last of D25: the fixture asserted approvals nobody made.

    `atj event approve` writes `approved_by` and `approved_at`. The sample
    generator wrote `approval_state: approved` directly, so 47 committed
    artifacts recorded the state with no name against it -- in the one fixture
    whose job is to demonstrate that an approval is a human act.
    """

    def unsigned(self, event: Path) -> list[str]:
        found = []
        for path in sorted(event.rglob("*.md")):
            try:
                metadata, _ = frontmatter.read(path)
            except Exception:  # noqa: BLE001 - malformed files are another check's problem
                continue
            if metadata.get("approval_state") == "approved" and not metadata.get("approved_by"):
                found.append(str(path.relative_to(event)))
        return found

    def test_the_sample_event_signs_every_approval(self):
        self.assertEqual(self.unsigned(SAMPLE), [])

    def test_release_check_would_catch_an_unsigned_one(self):
        from atj.cli import _unsigned_approvals

        holder = Path(tempfile.mkdtemp())
        try:
            events = holder / "events"
            shutil.copytree(SAMPLE, events / demo.EVENT_ID)
            path = next((events / demo.EVENT_ID / "summaries").glob("*.md"))
            metadata, body = frontmatter.read(path)
            del metadata["approved_by"]
            path.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
            problems, historical = _unsigned_approvals(holder)
            self.assertTrue(any(path.name in p for p in problems), problems)
            self.assertEqual(historical, [])
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_a_completed_event_reports_history_not_failure(self):
        """live-trial-2026 approved five artifacts before the command existed.

        A completed event's artifacts are frozen, so the only repair available
        inside one is to rewrite a frozen record -- D28's trap, which this
        framework has now walked into three times. Reported as history instead.
        """
        from atj.cli import _unsigned_approvals

        problems, historical = _unsigned_approvals(ROOT)
        self.assertEqual(problems, [])
        self.assertTrue(historical, "the live event has unsigned approvals to report")
        self.assertTrue(all("live-trial-2026" in entry for entry in historical), historical)


class TheStatusBodyAgreesWithItsLedger(unittest.TestCase):
    """D30: status.md's prose could contradict the front matter above it.

    live-trial-2026 finished with `final-audit-passed: passed` and
    `current_stage: complete` recorded, and its own body still showed both
    unchecked. This is D19's shape one file over -- an artifact asserting
    something false in its own voice -- in the one file an operator reads to
    answer "where is this event".
    """

    def test_both_committed_events_agree_with_themselves(self):
        for event in (LIVE, SAMPLE):
            with self.subTest(event.name):
                loaded = event_module.load(event, root=ROOT)
                self.assertEqual(event_module.validate_status_narrative(loaded), [])

    def test_an_unticked_passed_gate_is_reported(self):
        holder, event = event_copy(LIVE)
        try:
            status = event / "status.md"
            status.write_text(
                status.read_text(encoding="utf-8").replace(
                    "- [x] Bracket frozen and audited", "- [ ] Bracket frozen and audited", 1
                ),
                encoding="utf-8",
            )
            problems = event_module.validate_status_narrative(
                event_module.load(event, root=ROOT)
            )
            self.assertTrue(any("bracket-audited" in p for p in problems), problems)
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_a_ticked_pending_gate_is_reported(self):
        holder, event = event_copy(SAMPLE)
        try:
            loaded = event_module.load(event, root=ROOT)
            loaded.status["stage_gates"]["tournament-audited"] = "pending"
            event_module.save_status(loaded)
            problems = event_module.validate_status_narrative(
                event_module.load(event, root=ROOT)
            )
            self.assertTrue(any("tournament-audited" in p for p in problems), problems)
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_a_missing_checkbox_is_reported(self):
        holder, event = event_copy(LIVE)
        try:
            status = event / "status.md"
            status.write_text(
                status.read_text(encoding="utf-8").replace(
                    "- [x] Roster frozen\n", "", 1
                ),
                encoding="utf-8",
            )
            problems = event_module.validate_status_narrative(
                event_module.load(event, root=ROOT)
            )
            self.assertTrue(any("roster-frozen" in p for p in problems), problems)
        finally:
            shutil.rmtree(holder, ignore_errors=True)

    def test_the_labels_come_from_the_template(self):
        labels, complete = event_module.status_checkbox_labels(ROOT)
        self.assertEqual(len(labels), len(event_module.STAGE_GATES))
        self.assertEqual(complete, "Event marked complete")


if __name__ == "__main__":
    unittest.main()
