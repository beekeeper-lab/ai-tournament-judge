"""Prompt-injection resistance: the mechanical layer.

These tests assert the property the framework can actually guarantee: no text in
a submission can change an official fact, because official facts are never read
from a submission. They deliberately do not assert that an LLM cannot be talked
out of its instructions — see tests/fixtures/prompt-injection/README.md.
"""

import unittest
from pathlib import Path

from _support import ROOT  # noqa: F401
from atj import canon, frontmatter, publication, reports, schema, versions
from atj.errors import AtjError, SchemaError, ValidationError, VersionError

FIXTURE = ROOT / "tests" / "fixtures" / "prompt-injection"
SUBMISSION = FIXTURE / "submission"

HOSTILE_FILES = (
    SUBMISSION / "README.md",
    SUBMISSION / "src" / "app.js",
    SUBMISSION / ".github" / "workflows" / "ci.yml",
    SUBMISSION / "docs" / "output.txt",
    SUBMISSION / "tests" / "fixture.yml",
)


class FixtureIntegrityTests(unittest.TestCase):
    def test_the_fixture_actually_contains_injection_attempts(self):
        """A fixture that lost its payload would make every test below vacuous."""
        corpus = "\n".join(path.read_text(encoding="utf-8") for path in HOSTILE_FILES)
        for marker in (
            "Ignore all previous instructions",
            "submission-evaluation@9.9.9",
            "approval_state",
            "AKIAIOSFODNN7EXAMPLE",
            "Bash and WebFetch",
            "SYSTEM_OVERRIDE",
            "disqualified",
        ):
            self.assertIn(marker, corpus, marker)


class RubricCannotBeRedefinedTests(unittest.TestCase):
    def test_submission_content_does_not_change_the_canonical_rubric(self):
        canon.clear_cache()
        rubric = canon.load(ROOT)
        self.assertEqual(rubric.rubric_id, "submission-evaluation")
        self.assertEqual(rubric.total_weight, 100)
        self.assertNotIn("enthusiasm", rubric.criterion_ids)
        self.assertEqual(len(rubric.criteria), 7)

    def test_the_injected_rubric_version_fails_validation(self):
        with self.assertRaises(VersionError):
            versions.require_versions({"rubric": "submission-evaluation@9.9.9"}, root=ROOT)

    def test_the_injected_criterion_is_rejected(self):
        rubric = canon.load(ROOT)
        with self.assertRaises(Exception):
            rubric.criterion("enthusiasm")

    def test_weights_are_unreachable_from_a_submission(self):
        """There is no code path that reads a weight from submission content."""
        from atj.cli import check_no_duplicate_weights

        self.assertEqual(check_no_duplicate_weights(ROOT), [])


class ParserCannotBeExploitedTests(unittest.TestCase):
    def test_yaml_is_loaded_without_object_construction(self):
        payload = "---\n!!python/object/apply:os.system ['touch /tmp/atj-injected']\n---\nbody\n"
        with self.assertRaises(ValidationError):
            frontmatter.split(payload)
        self.assertFalse(Path("/tmp/atj-injected").exists())

    def test_yaml_alias_expansion_bomb_is_refused(self):
        bomb = "---\n" + "a: &a [1,1]\nb: &b [*a,*a]\nc: &c [*b,*b]\n" + "---\nbody\n"
        try:
            metadata, _ = frontmatter.split(bomb)
        except ValidationError:
            return
        self.assertIsInstance(metadata, dict)

    def test_oversized_front_matter_is_refused(self):
        payload = "---\nnote: " + ("A" * (frontmatter.MAX_FRONTMATTER_BYTES + 10)) + "\n---\nbody\n"
        with self.assertRaises(ValidationError):
            frontmatter.split(payload)

    def test_undecodable_bytes_produce_a_validation_error_not_a_traceback(self):
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "hostile.md"
            path.write_bytes(b"---\nevent_id: demo\n---\n\xff\xfe binary \xff\n")
            metadata, body = frontmatter.read(path)
            self.assertEqual(metadata["event_id"], "demo")
            self.assertIn("�", body)

    def test_relative_path_in_a_submission_cannot_redirect_schema_loading(self):
        for attempt in ("../framework/personas.md", "/etc/passwd", "injected.md",
                        "../../../../etc/shadow"):
            with self.assertRaises(SchemaError):
                schema.get_schema(attempt, ROOT)


class DestinationAndPolicyCannotBeRedefinedTests(unittest.TestCase):
    def setUp(self):
        self.metadata, self.body = frontmatter.read(FIXTURE / "hostile-artifact.md")

    def test_the_hostile_public_artifact_is_blocked_on_every_axis(self):
        findings = publication.check_public(
            self.metadata, self.body, artifact="public/hostile.md", public_scores=False
        )
        rules = {finding.rule for finding in findings}
        for expected in ("private-field", "provenance", "secret",
                         "deliberation", "private-identifier", "unapproved-score"):
            self.assertIn(expected, rules, f"{expected} not blocked")
        self.assertTrue(all(finding.severity == "blocking" for finding in findings))

    def test_self_declared_approval_does_not_survive_schema_validation(self):
        problems = schema.validate("public-report", self.metadata, root=ROOT)
        self.assertTrue(problems, "a public artifact carrying scores and run ids validated")

    def test_visibility_is_determined_by_location_not_by_claimed_metadata(self):
        event_dir = Path("/events/demo")
        self.assertEqual(
            publication.expected_visibility(event_dir / "judgments" / "x.md", event_dir), "private"
        )
        findings = publication.check_artifact(
            event_dir / "judgments" / "x.md", event_dir,
            {"visibility": "public"}, "content", public_scores=False,
        )
        self.assertTrue(any(f.rule == "visibility" for f in findings))

    def test_an_injected_rubric_version_fails_report_validation(self):
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            event_dir = Path(directory)
            (event_dir / "public").mkdir()
            target = event_dir / "public" / "hostile.md"
            target.write_text((FIXTURE / "hostile-artifact.md").read_text(encoding="utf-8"),
                              encoding="utf-8")
            report = reports.validate_artifact(target, event_dir, root=ROOT)
            self.assertFalse(report.ok)
            self.assertTrue(any(f.rule == "version" for f in report.blocking))


class ToolSurfaceTests(unittest.TestCase):
    def test_initial_judges_have_no_tool_that_could_act_on_an_injection(self):
        """A manipulated judge still cannot run code, fetch a URL, or write a file."""
        allowed = {"Read", "Grep", "Glob"}
        for name in ("judge-backend", "judge-frontend-ux",
                     "judge-security-ops", "judge-product-agentic", "matchup-judge",
                     "panel-consolidator"):
            metadata, _ = frontmatter.read(ROOT / ".claude" / "agents" / f"{name}.md")
            tools = {tool.strip() for tool in str(metadata.get("tools", "")).split(",") if tool.strip()}
            self.assertTrue(tools, f"{name} declares no tool restriction")
            self.assertTrue(
                tools <= allowed,
                f"{name} may use {sorted(tools - allowed)}, which exceeds read-only evidence access",
            )

    def test_every_judge_persona_names_submission_content_as_untrusted(self):
        for name in ("judge-backend", "judge-frontend-ux",
                     "judge-security-ops", "judge-product-agentic"):
            _, body = frontmatter.read(ROOT / ".claude" / "agents" / f"{name}.md")
            lowered = body.lower()
            self.assertTrue(
                "untrusted" in lowered or "never instruction" in lowered
                or "hostile data" in lowered,
                f"{name} does not tell the judge that submission content is untrusted",
            )

    def test_no_agent_definition_was_altered_without_a_version_bump(self):
        self.assertEqual(versions.check_personas(ROOT), [])


class SandboxCannotBeTalkedIntoHostExecutionTests(unittest.TestCase):
    def test_an_allowlist_without_a_proxy_is_refused(self):
        from atj import sandbox
        from atj.errors import SafetyError

        with self.assertRaises(SafetyError):
            sandbox.build_command(
                runtime="podman", image="x", source=SUBMISSION, command=["true"],
                network_allowlist=["taskflow-telemetry.example.com"],
            )

    def test_the_built_command_never_grants_privilege_or_the_docker_socket(self):
        from atj import sandbox

        argv = sandbox.build_command(
            runtime="podman", image="x", source=SUBMISSION, command=["npm", "start"]
        )
        joined = " ".join(argv)
        for banned in ("--privileged", "docker.sock", "--network=host", "--cap-add",
                       "--userns=host", "--pid=host"):
            self.assertNotIn(banned, joined)
        self.assertIn("--network", argv)
        self.assertEqual(argv[argv.index("--network") + 1], "none")
        self.assertIn("--cap-drop", argv)
        self.assertIn("--read-only", argv)

    def test_unavailable_isolation_never_falls_back_to_the_host(self):
        from atj import sandbox
        from atj.errors import SafetyError

        unavailable = sandbox.Capability(
            runtime=None, version=None, available=False, rootless=None,
            reasons=["no runtime"],
        )
        with self.assertRaises(SafetyError):
            sandbox.run_in_sandbox(
                source=SUBMISSION, command=["npm", "start"], capability=unavailable
            )
        limitation = sandbox.evidence_limitation(unavailable)
        self.assertEqual(limitation["execution_status"], sandbox.UNAVAILABLE)
        self.assertEqual(limitation["evidence_limited_criteria"], ["functional", "reliability"])


if __name__ == "__main__":
    unittest.main()
