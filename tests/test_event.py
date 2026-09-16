"""Event lifecycle: initialization, validation, transitions, staleness, resume."""

import shutil
import tempfile
import unittest
from pathlib import Path

from _support import ROOT  # noqa: F401
from atj import event as event_module
from atj import frontmatter, schema
from atj.errors import StateError, ValidationError

TEMPLATE_FILES = ("event.md", "teams.md", "status.md", "bracket.md")

ROSTER_BODY = """
| Team ID | Display name | Affiliation group | Previous result | Submission status | Eligible |
|---|---|---|---|---|---|
| team-alpha | Alpha | north-school | champion | received | yes |
| team-beta | Beta | north-school | runner-up | received | yes |
| team-gamma | Gamma | south-school | none | received | yes |
| team-delta | Delta | east-school | none | received | yes |
"""


class TemporaryFramework:
    """A disposable copy of the framework, so tests never write to the repository."""

    def __enter__(self):
        self.directory = Path(tempfile.mkdtemp())
        for item in ("framework", "schemas", "events", ".claude"):
            shutil.copytree(ROOT / item, self.directory / item)
        return self.directory

    def __exit__(self, *exc):
        shutil.rmtree(self.directory, ignore_errors=True)


def complete_roster(event_dir: Path) -> None:
    path = event_dir / "teams.md"
    metadata, _ = frontmatter.read(path)
    metadata["frozen"] = True
    path.write_text(frontmatter.dump(metadata, "\n# Teams\n" + ROSTER_BODY), encoding="utf-8")


class InitializationTests(unittest.TestCase):
    def test_initialize_creates_a_schema_valid_event(self):
        with TemporaryFramework() as root:
            target = event_module.initialize("spring-demo", root=root, event_name="Spring Demo")
            self.assertTrue(target.is_dir())
            for name in TEMPLATE_FILES:
                self.assertTrue((target / name).is_file(), name)
            for subdir in event_module.EVENT_SUBDIRS:
                self.assertTrue((target / subdir).is_dir(), subdir)

            metadata, _ = frontmatter.read(target / "event.md")
            self.assertEqual(schema.validate("event", metadata, root=root), [])
            status, _ = frontmatter.read(target / "status.md")
            self.assertEqual(schema.validate("status", status, root=root), [])

    def test_initialize_substitutes_every_placeholder_in_identity_fields(self):
        with TemporaryFramework() as root:
            target = event_module.initialize("spring-demo", root=root, event_name="Spring Demo")
            metadata, _ = frontmatter.read(target / "event.md")
            self.assertEqual(metadata["event_id"], "spring-demo")
            self.assertEqual(metadata["event_name"], "Spring Demo")
            self.assertNotIn("replace-me", str(metadata))
            self.assertNotIn("FRAMEWORK-COMMIT", str(metadata))

    def test_execution_is_disabled_by_default(self):
        with TemporaryFramework() as root:
            target = event_module.initialize("spring-demo", root=root)
            metadata, _ = frontmatter.read(target / "event.md")
            self.assertEqual(metadata["execution_mode"], "disabled")

    def test_invalid_event_id_is_rejected(self):
        with TemporaryFramework() as root:
            for bad in ("Spring Demo", "spring_demo", "-leading", ""):
                with self.assertRaises(ValidationError):
                    event_module.initialize(bad, root=root)

    def test_existing_event_is_not_overwritten(self):
        with TemporaryFramework() as root:
            event_module.initialize("spring-demo", root=root)
            with self.assertRaises(ValidationError):
                event_module.initialize("spring-demo", root=root)


class ValidationTests(unittest.TestCase):
    def test_a_completed_event_validates(self):
        with TemporaryFramework() as root:
            target = event_module.initialize("spring-demo", root=root, event_name="Spring Demo")
            complete_roster(target)
            loaded = event_module.load(target, root=root)
            self.assertEqual(event_module.validate_configuration(loaded), [])
            self.assertEqual(event_module.validate_status(loaded), [])
            self.assertEqual(event_module.validate_roster(loaded), [])

    def test_roster_table_is_parsed_from_markdown(self):
        with TemporaryFramework() as root:
            target = event_module.initialize("spring-demo", root=root)
            complete_roster(target)
            loaded = event_module.load(target, root=root)
            self.assertEqual(
                [team["id"] for team in loaded.teams],
                ["team-alpha", "team-beta", "team-gamma", "team-delta"],
            )
            self.assertEqual(loaded.team("team-alpha")["previous_result"], "champion")
            self.assertEqual(loaded.team("team-beta")["affiliation_group"], "north-school")
            self.assertEqual(len(loaded.eligible_teams), 4)

    def test_mismatched_event_ids_are_caught(self):
        with TemporaryFramework() as root:
            target = event_module.initialize("spring-demo", root=root)
            complete_roster(target)
            path = target / "status.md"
            metadata, body = frontmatter.read(path)
            metadata["event_id"] = "other-event"
            path.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
            loaded = event_module.load(target, root=root)
            self.assertTrue(
                any("different event_id" in p for p in event_module.validate_configuration(loaded))
            )

    def test_two_champions_on_the_roster_is_caught(self):
        with TemporaryFramework() as root:
            target = event_module.initialize("spring-demo", root=root)
            complete_roster(target)
            loaded = event_module.load(target, root=root)
            loaded.roster["teams"][2]["previous_result"] = "champion"
            self.assertTrue(
                any("more than one team" in p for p in event_module.validate_roster(loaded))
            )

    def test_missing_directory_is_caught(self):
        with TemporaryFramework() as root:
            target = event_module.initialize("spring-demo", root=root)
            complete_roster(target)
            shutil.rmtree(target / "matchups")
            loaded = event_module.load(target, root=root)
            self.assertTrue(
                any("missing required directory" in p
                    for p in event_module.validate_configuration(loaded))
            )


class TransitionTests(unittest.TestCase):
    def setUp(self):
        self.context = TemporaryFramework()
        self.root = self.context.__enter__()
        self.directory = event_module.initialize("spring-demo", root=self.root)
        complete_roster(self.directory)
        self.event = event_module.load(self.directory, root=self.root)

    def tearDown(self):
        self.context.__exit__(None, None, None)

    def test_only_forward_by_one_stage_is_legal(self):
        self.assertEqual(event_module.legal_transitions("configuration"), ("intake",))
        self.assertEqual(event_module.legal_transitions("dossiers"), ("final-audit",))
        self.assertEqual(event_module.legal_transitions("complete"), ())

    def test_advance_is_blocked_until_the_gate_passes(self):
        allowed, reasons = event_module.can_advance(self.event)
        self.assertFalse(allowed)
        self.assertTrue(any("stage gate" in reason for reason in reasons))
        with self.assertRaises(StateError):
            event_module.advance(self.event)

    def test_advance_succeeds_once_the_gate_passes(self):
        self.event.status["stage_gates"]["configuration-audited"] = "passed"
        self.assertEqual(event_module.advance(self.event), "intake")
        self.assertEqual(self.event.stage, "intake")

    def test_blocked_event_cannot_advance(self):
        self.event.status["stage_gates"]["configuration-audited"] = "passed"
        self.event.status["blocked"] = True
        self.event.status["blocked_reason"] = "awaiting official"
        allowed, reasons = event_module.can_advance(self.event)
        self.assertFalse(allowed)
        self.assertTrue(any("blocked" in reason for reason in reasons))

    def test_failed_audit_blocks_advancement(self):
        self.event.status["stage_gates"]["configuration-audited"] = "passed"
        self.event.status["units"] = [{
            "unit_id": "config", "stage": "configuration", "state": "complete",
            "input_digest": "x", "audit_result": "FAIL",
        }]
        allowed, reasons = event_module.can_advance(self.event)
        self.assertFalse(allowed)
        self.assertTrue(any("failed audits" in reason for reason in reasons))

    def test_incomplete_unit_blocks_advancement(self):
        self.event.status["stage_gates"]["configuration-audited"] = "passed"
        self.event.status["units"] = [{
            "unit_id": "config", "stage": "configuration", "state": "in-progress",
            "input_digest": "x", "audit_result": "not-audited",
        }]
        self.assertFalse(event_module.can_advance(self.event)[0])

    def test_human_override_is_recorded_not_silent(self):
        target = event_module.advance(self.event, force_reason="official waived the gate")
        self.assertEqual(target, "intake")
        self.assertEqual(len(self.event.status["overrides"]), 1)
        self.assertEqual(
            self.event.status["overrides"][0]["reason"], "official waived the gate"
        )

    def test_going_backwards_marks_dependent_units_stale(self):
        event_module.set_stage(self.event, "bracket")
        self.event.status["units"] = [
            {"unit_id": "judge-alpha", "stage": "initial-judging", "state": "complete",
             "input_digest": "x", "audit_result": "PASS"},
            {"unit_id": "draw", "stage": "bracket", "state": "complete",
             "input_digest": "y", "audit_result": "PASS"},
        ]
        event_module.set_stage(self.event, "initial-judging")
        states = {unit["unit_id"]: unit["state"] for unit in self.event.status["units"]}
        self.assertEqual(states, {"judge-alpha": "stale", "draw": "stale"})

    def test_status_round_trips_through_disk(self):
        self.event.status["stage_gates"]["configuration-audited"] = "passed"
        event_module.advance(self.event)
        event_module.save_status(self.event)
        reloaded = event_module.load(self.directory, root=self.root)
        self.assertEqual(reloaded.stage, "intake")


class ResumeTests(unittest.TestCase):
    def setUp(self):
        self.context = TemporaryFramework()
        self.root = self.context.__enter__()
        self.directory = event_module.initialize("spring-demo", root=self.root)
        complete_roster(self.directory)
        self.event = event_module.load(self.directory, root=self.root)

    def tearDown(self):
        self.context.__exit__(None, None, None)

    def test_completed_audited_work_is_not_redone(self):
        self.event.status["stage_gates"]["configuration-audited"] = "passed"
        (self.directory / "audits" / "config.md").write_text("ok", encoding="utf-8")
        event_module.record_unit(
            self.event, unit_id="config", stage="configuration",
            input_digest="abc", outputs=["audits/config.md"], audit_result="PASS",
        )
        action = event_module.next_action(self.event)
        self.assertEqual(action["action"], "advance-stage")

    def test_missing_output_is_detected_after_an_interruption(self):
        event_module.record_unit(
            self.event, unit_id="config", stage="configuration",
            input_digest="abc", outputs=["audits/never-written.md"], audit_result="PASS",
        )
        problems = event_module.missing_outputs(self.event)
        self.assertEqual(len(problems), 1)
        action = event_module.next_action(self.event)
        self.assertEqual(action["action"], "repair-incomplete-unit")
        self.assertTrue(action["blocked"])

    def test_changed_input_makes_a_unit_stale(self):
        event_module.record_unit(
            self.event, unit_id="judge-alpha", stage="initial-judging",
            input_digest="digest-1", outputs=[], audit_result="PASS",
        )
        self.assertEqual(
            event_module.check_staleness(self.event, {"judge-alpha": "digest-2"}), ["judge-alpha"]
        )
        self.assertEqual(
            event_module.check_staleness(self.event, {"judge-alpha": "digest-1"}), []
        )

    def test_stale_units_are_the_next_action(self):
        event_module.record_unit(
            self.event, unit_id="judge-alpha", stage="initial-judging",
            input_digest="digest-1", outputs=[], audit_result="PASS",
        )
        event_module.mark_stale(self.event, "judge-alpha", "evidence package changed")
        action = event_module.next_action(self.event)
        self.assertEqual(action["action"], "rerun-stale-units")
        self.assertEqual(action["problems"], ["judge-alpha"])

    def test_failed_audit_is_the_next_action_and_blocks(self):
        event_module.record_unit(
            self.event, unit_id="judge-alpha", stage="initial-judging",
            input_digest="d", outputs=[], audit_result="FAIL",
        )
        action = event_module.next_action(self.event)
        self.assertEqual(action["action"], "repair-failed-audit")
        self.assertTrue(action["blocked"])

    def test_recording_a_unit_twice_updates_rather_than_duplicates(self):
        for digest in ("one", "two"):
            event_module.record_unit(
                self.event, unit_id="config", stage="configuration",
                input_digest=digest, outputs=[], audit_result="PASS",
            )
        units = [u for u in self.event.status["units"] if u["unit_id"] == "config"]
        self.assertEqual(len(units), 1)
        self.assertEqual(units[0]["input_digest"], "two")


if __name__ == "__main__":
    unittest.main()
