"""Publication boundary: the alpha's highest-consequence gap."""

import unittest
from pathlib import Path

from _support import ROOT  # noqa: F401
from atj import publication as pub

PUBLIC_METADATA = {
    "event_id": "demo", "visibility": "public", "approval_state": "approved",
    "approved_by": "head official", "source_artifacts": ["matchups/mu-demo-final-01.md"],
    "scores_published": False,
}


class PublicBoundaryTests(unittest.TestCase):
    def test_the_exact_alpha_artifact_is_now_blocked(self):
        body = (
            "# Public Summary\n"
            "Internal note: judge-security-ops found a hardcoded AWS key "
            "AKIAIOSFODNN7EXAMPLE in team-b.\n"
            "Private deliberation: the panel argued team-a should lose on a technicality.\n"
            "Raw consolidated score 41.3/100.\n"
            "Evidence ev:demo:team-b:abcdef012345:deadbeef was used.\n"
        )
        findings = pub.check_public(
            {"event_id": "demo", "visibility": "private"}, body, artifact="public/m1.md"
        )
        rules = {finding.rule for finding in findings}
        for expected in ("visibility", "approval", "provenance", "secret",
                         "deliberation", "private-identifier", "unapproved-score"):
            self.assertIn(expected, rules, f"{expected} not caught")
        self.assertTrue(all(f.severity == "blocking" for f in findings))

    def test_a_clean_approved_summary_passes(self):
        body = "# Summary\n\nAlpha advances on stronger demonstrated reliability.\n"
        self.assertEqual(pub.check_public(PUBLIC_METADATA, body, artifact="public/ok.md"), [])

    def test_unapproved_artifact_is_blocked(self):
        for change in ({"approval_state": "draft"}, {"approved_by": None}, {"source_artifacts": []}):
            metadata = dict(PUBLIC_METADATA, **change)
            findings = pub.check_public(metadata, "# Summary\n\nText.\n")
            self.assertTrue(findings, change)

    def test_private_only_fields_are_refused(self):
        for field in pub.PRIVATE_ONLY_FIELDS:
            metadata = dict(PUBLIC_METADATA, **{field: "anything"})
            findings = pub.check_public(metadata, "# Summary\n\nText.\n")
            self.assertTrue(
                any(f.rule == "private-field" for f in findings),
                f"{field} reached a public artifact",
            )

    def test_scores_allowed_only_when_the_event_publishes_them(self):
        body = "# Summary\n\nFinal score 88.5/100.\n"
        self.assertTrue(pub.check_public(PUBLIC_METADATA, body, public_scores=False))
        self.assertEqual(pub.check_public(PUBLIC_METADATA, body, public_scores=True), [])


class SecretScanTests(unittest.TestCase):
    CASES = (
        "AKIAIOSFODNN7EXAMPLE",
        "ghp_0123456789abcdefghijklmnopqrstuvwxyz",
        "AIzaSyA1234567890abcdefghijklmnopqrstuv",
        "xoxb-1234567890-abcdefghij",
        "sk-abcdefghijklmnopqrstuvwxyz0123",
        "sk-ant-abcdefghijklmnopqrstuvwxyz0123",
        "-----BEGIN RSA PRIVATE KEY-----",
        "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dBjftJeZ4CVP",
        'password: "hunter2hunter2"',
        "postgres://user:secretpw@db.internal:5432/app",
        "Authorization: Bearer abcdefghijklmnopqrstuvwxyz0123456789",
    )

    def test_each_credential_shape_is_detected(self):
        for candidate in self.CASES:
            with self.subTest(candidate=candidate[:20]):
                self.assertTrue(pub.scan_secrets(candidate), candidate)

    def test_the_secret_is_not_echoed_in_full(self):
        finding = pub.scan_secrets("AKIAIOSFODNN7EXAMPLE")[0]
        self.assertNotIn("AKIAIOSFODNN7EXAMPLE", finding.detail)

    def test_ordinary_prose_is_not_flagged(self):
        clean = (
            "The team documented its secrets handling and used environment variables "
            "for the API key rather than committing it."
        )
        self.assertEqual(pub.scan_secrets(clean), [])

    def test_private_artifacts_are_scanned_too(self):
        findings = pub.check_private({"visibility": "private"}, "key AKIAIOSFODNN7EXAMPLE")
        self.assertTrue(findings)


class TeamFacingTests(unittest.TestCase):
    METADATA = {"event_id": "demo", "team_id": "team-a", "visibility": "team",
                "approval_state": "approved", "validation_state": "valid"}

    def test_clean_dossier_passes(self):
        body = "# Dossier\n\nYour retry logic was the strongest in the field.\n"
        self.assertEqual(
            pub.check_team_facing(self.METADATA, body, own_team="team-a", all_teams=["team-a", "team-b"]),
            [],
        )

    def test_judge_persona_names_are_blocked(self):
        body = "# Dossier\n\njudge-backend thought your API layer was weak.\n"
        findings = pub.check_team_facing(self.METADATA, body, own_team="team-a")
        self.assertTrue(any(f.rule == "deliberation" for f in findings))

    def test_wrong_visibility_is_blocked(self):
        findings = pub.check_team_facing(dict(self.METADATA, visibility="private"), "# D\n\nx\n")
        self.assertTrue(any(f.rule == "visibility" for f in findings))

    def test_naming_another_team_is_an_advisory_not_a_block(self):
        body = "# Dossier\n\nYou beat team-b in the quarterfinal.\n"
        findings = pub.check_team_facing(
            self.METADATA, body, own_team="team-a", all_teams=["team-a", "team-b"]
        )
        self.assertTrue(findings)
        self.assertTrue(all(f.severity == "advisory" for f in findings))

    def test_panel_internal_fields_are_blocked(self):
        for field in pub.TEAM_FORBIDDEN_FIELDS:
            findings = pub.check_team_facing(
                dict(self.METADATA, **{field: "x"}), "# D\n\nx\n", own_team="team-a"
            )
            self.assertTrue(any(f.rule == "private-field" for f in findings), field)


class RoutingTests(unittest.TestCase):
    def test_directory_determines_the_required_visibility(self):
        event_dir = Path("/events/demo")
        self.assertEqual(pub.expected_visibility(event_dir / "public" / "a.md", event_dir), "public")
        self.assertEqual(pub.expected_visibility(event_dir / "dossiers" / "a.md", event_dir), "team")
        self.assertEqual(pub.expected_visibility(event_dir / "judgments" / "a.md", event_dir), "private")
        self.assertIsNone(pub.expected_visibility(Path("/elsewhere/a.md"), event_dir))

    def test_require_publishable_raises_on_blocking_findings(self):
        from atj.errors import ValidationError

        with self.assertRaises(ValidationError):
            pub.require_publishable(pub.scan_secrets("AKIAIOSFODNN7EXAMPLE"))
        pub.require_publishable([])


if __name__ == "__main__":
    unittest.main()
