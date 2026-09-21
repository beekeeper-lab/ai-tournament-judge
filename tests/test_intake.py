"""Submission intake: the step that turns a delivery into pinned evidence.

Intake is where untrusted input first touches the operator's disk, so most of
these tests are about what the command refuses to do.
"""

import shutil
import stat
import subprocess
import tempfile
import unittest
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from _support import ROOT  # noqa: F401
from atj import event as event_module
from atj import frontmatter, intake, reports
from atj.errors import SafetyError, StateError, ValidationError

NOW = datetime(2026, 5, 1, 12, 0, 0, tzinfo=timezone.utc)


class TemporaryFramework:
    """A disposable copy of the framework, so tests never write to the repository."""

    def __enter__(self) -> Path:
        self.directory = Path(tempfile.mkdtemp())
        for item in ("framework", "schemas", "events", ".claude"):
            shutil.copytree(ROOT / item, self.directory / item)
        return self.directory

    def __exit__(self, *exc):
        shutil.rmtree(self.directory, ignore_errors=True)


def make_event(root: Path, *, stage: str = "intake") -> event_module.Event:
    directory = event_module.initialize("test-event", root=root, event_name="Test Event")
    config_path = directory / "event.md"
    metadata, body = frontmatter.read(config_path)
    metadata.update({
        "event_id": "test-event", "event_name": "Test Event", "status": "active",
        "framework_commit": "uncommitted", "started_at": "2026-05-01T12:00:00Z",
        "completed_at": None, "approval_state": "approved", "validation_state": "validated",
        "officials": {key: "event-director" for key in metadata.get("officials", {})},
    })
    config_path.write_text(frontmatter.dump(metadata, body), encoding="utf-8")

    roster_path = directory / "teams.md"
    roster_meta, roster_body = frontmatter.read(roster_path)
    roster_meta["event_id"] = "test-event"
    roster_path.write_text(frontmatter.dump(roster_meta, roster_body), encoding="utf-8")

    status_path = directory / "status.md"
    status_meta, status_body = frontmatter.read(status_path)
    status_meta["event_id"] = "test-event"
    status_meta["current_stage"] = stage
    status_path.write_text(frontmatter.dump(status_meta, status_body), encoding="utf-8")
    return event_module.load(directory, root=root)


def git(*args: str, cwd: Path) -> str:
    completed = subprocess.run(
        ["git", *args], cwd=str(cwd), capture_output=True, text=True, check=True,
        env={
            "PATH": "/usr/bin:/bin", "HOME": str(cwd),
            "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t.invalid",
            "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t.invalid",
        },
    )
    return completed.stdout.strip()


def make_repo(path: Path, *, commits: int = 1) -> list[str]:
    path.mkdir(parents=True, exist_ok=True)
    git("init", "--quiet", "--initial-branch=main", cwd=path)
    hashes = []
    for index in range(commits):
        (path / "app.py").write_text(f"version = {index}\n", encoding="utf-8")
        git("add", "--all", cwd=path)
        git("commit", "--quiet", "-m", f"commit {index}", cwd=path)
        hashes.append(git("rev-parse", "HEAD", cwd=path))
    return hashes


def make_zip(path: Path, entries: dict[str, str], *, wrapper: str | None = None) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as bundle:
        for name, content in entries.items():
            bundle.writestr(f"{wrapper}/{name}" if wrapper else name, content)
    return path


class ArchiveIntakeTests(unittest.TestCase):
    def test_an_archive_is_pinned_to_a_reproducible_snapshot_commit(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            archive = make_zip(root / "src" / "a.zip", {"app.py": "x = 1\n"})
            first = intake.run(event, "team-alpha", str(archive),
                               workspace=root / "ws1", now=NOW)
            second = intake.run(event, "team-alpha", str(archive),
                                workspace=root / "ws2", now=NOW)
            self.assertEqual(first.pin, "snapshot")
            self.assertEqual(
                first.commit, second.commit,
                "the same delivered tree must pin to the same commit on every run",
            )

    def test_a_changed_archive_cannot_reuse_the_same_commit(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            original = intake.run(
                event, "team-alpha",
                str(make_zip(root / "src" / "a.zip", {"app.py": "x = 1\n"})),
                workspace=root / "ws", now=NOW,
            )
            changed = intake.run(
                event, "team-alpha",
                str(make_zip(root / "src" / "b.zip", {"app.py": "x = 2\n"})),
                workspace=root / "ws", force=True, now=NOW,
            )
            self.assertNotEqual(original.commit, changed.commit)

    def test_a_single_wrapper_directory_is_unwrapped(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            archive = make_zip(
                root / "src" / "a.zip", {"app.py": "x = 1\n"}, wrapper="project-main"
            )
            result = intake.run(event, "team-alpha", str(archive),
                                workspace=root / "ws", now=NOW)
            self.assertTrue((result.checkout / "app.py").is_file())

    def test_an_archive_carrying_its_own_history_keeps_it(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            source = root / "src" / "repo"
            head = make_repo(source)[-1]
            archive = root / "src" / "a.zip"
            archive.parent.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(archive, "w") as bundle:
                for item in sorted(source.rglob("*")):
                    if item.is_file() and not item.is_symlink():
                        bundle.write(item, item.relative_to(source))
            result = intake.run(event, "team-alpha", str(archive),
                                workspace=root / "ws", now=NOW)
            self.assertEqual(result.pin, "cloned")
            self.assertEqual(result.commit, head)


class ArchiveSafetyTests(unittest.TestCase):
    def _refuses(self, archive: Path, root: Path, event) -> str:
        with self.assertRaises(SafetyError) as caught:
            intake.run(event, "team-alpha", str(archive), workspace=root / "ws", now=NOW)
        self.assertFalse(
            (root / "ws" / "test-event" / "team-alpha").exists(),
            "a refused archive must leave no checkout behind",
        )
        return caught.exception.message

    def test_parent_directory_traversal_is_refused(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            archive = make_zip(root / "src" / "evil.zip", {"../../pwned.txt": "owned"})
            self.assertIn("traversal", self._refuses(archive, root, event))

    def test_an_absolute_path_is_refused(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            archive = make_zip(root / "src" / "evil.zip", {"/etc/cron.d/job": "owned"})
            self.assertIn("absolute path", self._refuses(archive, root, event))

    def test_a_symbolic_link_is_refused(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            archive = root / "src" / "evil.zip"
            archive.parent.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(archive, "w") as bundle:
                info = zipfile.ZipInfo("link")
                info.external_attr = (stat.S_IFLNK | 0o777) << 16
                bundle.writestr(info, "/etc/passwd")
            self.assertIn("symbolic link", self._refuses(archive, root, event))

    def test_too_many_entries_is_refused(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            archive = make_zip(
                root / "src" / "big.zip",
                {f"f{index}": "" for index in range(intake.MAX_ENTRIES + 1)},
            )
            self.assertIn("intake limit", self._refuses(archive, root, event))

    def test_an_over_compressed_entry_is_refused(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            archive = root / "src" / "bomb.zip"
            archive.parent.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
                bundle.writestr("bomb", "0" * (intake.MAX_RATIO * 5000))
            self.assertIn("expands more than", self._refuses(archive, root, event))


class GitIntakeTests(unittest.TestCase):
    def test_a_local_repository_is_pinned_to_its_own_head(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            source = root / "src" / "repo"
            head = make_repo(source)[-1]
            result = intake.run(event, "team-alpha", str(source),
                                workspace=root / "ws", now=NOW)
            self.assertEqual(result.pin, "cloned")
            self.assertEqual(result.commit, head)
            self.assertEqual(result.source_kind, "git-repo")

    def test_ref_selects_an_earlier_commit(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            source = root / "src" / "repo"
            first, _second = make_repo(source, commits=2)
            result = intake.run(event, "team-alpha", str(source), ref=first,
                                workspace=root / "ws", now=NOW)
            self.assertEqual(result.commit, first)
            self.assertEqual((result.checkout / "app.py").read_text(), "version = 0\n")

    def test_uncommitted_source_changes_are_reported_and_not_ingested(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            source = root / "src" / "repo"
            make_repo(source)
            (source / "app.py").write_text("version = 99\n", encoding="utf-8")
            result = intake.run(event, "team-alpha", str(source),
                                workspace=root / "ws", now=NOW)
            self.assertTrue(any("uncommitted" in note for note in result.notes))
            self.assertEqual((result.checkout / "app.py").read_text(), "version = 0\n")

    def test_ref_on_a_source_without_history_is_refused(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            archive = make_zip(root / "src" / "a.zip", {"app.py": "x = 1\n"})
            with self.assertRaises(ValidationError):
                intake.run(event, "team-alpha", str(archive), ref="abc1234",
                           workspace=root / "ws", now=NOW)

    def test_a_missing_source_is_refused_before_anything_is_written(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            with self.assertRaises(ValidationError):
                intake.run(event, "team-alpha", str(root / "src" / "nothing"),
                           workspace=root / "ws", now=NOW)
            self.assertFalse((event.directory / "submissions" / "team-alpha.md").exists())


class RecordAndRosterTests(unittest.TestCase):
    def test_the_generated_record_passes_report_validation(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            archive = make_zip(root / "src" / "a.zip", {"app.py": "x = 1\n"})
            result = intake.run(event, "team-alpha", str(archive),
                                workspace=root / "ws", display_name="Alpha", now=NOW)
            report = reports.validate_artifact(result.record, event.directory, root=root)
            self.assertEqual(
                [finding.render() for finding in report.findings], [],
                "intake must produce an artifact the framework's own validator accepts",
            )

    def test_the_record_names_how_the_commit_was_obtained(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            archive = make_zip(root / "src" / "a.zip", {"app.py": "x = 1\n"})
            result = intake.run(event, "team-alpha", str(archive),
                                workspace=root / "ws", now=NOW)
            body = result.record.read_text(encoding="utf-8")
            self.assertIn("snapshot", body)
            self.assertIn("is not the team's own commit", body)

    def test_the_recorded_checkout_path_is_repository_relative(self):
        """Configuration F10 / intake F8. The provenance table printed the
        operator's absolute home path into a record committed to a public
        repository. The path identifies the checkout, so it is written the way
        every reader of the repository sees it.
        """
        with TemporaryFramework() as root:
            event = make_event(root)
            archive = make_zip(root / "src" / "a.zip", {"app.py": "x = 1\n"})
            result = intake.run(event, "team-alpha", str(archive),
                                workspace=root / "ws", now=NOW)
            body = result.record.read_text(encoding="utf-8")
            line = next(l for l in body.splitlines() if l.startswith("| Checkout |"))
            self.assertNotIn(str(root), line)
            self.assertIn("ws/", line)
            self.assertNotIn("| `/", line)

    def test_a_new_team_is_added_to_the_roster_and_read_back(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            archive = make_zip(root / "src" / "a.zip", {"app.py": "x = 1\n"})
            result = intake.run(
                event, "team-alpha", str(archive), workspace=root / "ws",
                display_name="Alpha", affiliation_group="north-school", now=NOW,
            )
            reloaded = event_module.load(event.directory, root=root)
            team = reloaded.team("team-alpha")
            self.assertEqual(team["commit"], result.commit)
            self.assertEqual(team["affiliation_group"], "north-school")
            self.assertTrue(team["eligible"])

    def test_re_ingest_preserves_decisions_the_operator_made(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            roster = event.directory / "teams.md"
            metadata, body = frontmatter.read(roster)
            body += (
                "\n| team-alpha | Alpha | north-school | champion | received | no |  |  |\n"
            )
            roster.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
            reloaded = event_module.load(event.directory, root=root)

            archive = make_zip(root / "src" / "a.zip", {"app.py": "x = 1\n"})
            intake.run(reloaded, "team-alpha", str(archive), workspace=root / "ws", now=NOW)

            team = event_module.load(event.directory, root=root).team("team-alpha")
            self.assertEqual(team["previous_result"], "champion")
            self.assertFalse(team["eligible"], "intake must not re-open an ineligible team")
            self.assertEqual(team["display_name"], "Alpha")

    def test_every_other_roster_row_is_left_alone(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            roster = event.directory / "teams.md"
            metadata, body = frontmatter.read(roster)
            body += "\n| team-beta | Beta | south-school | none | received | yes |  |  |\n"
            roster.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
            before = roster.read_text(encoding="utf-8")

            archive = make_zip(root / "src" / "a.zip", {"app.py": "x = 1\n"})
            intake.run(event_module.load(event.directory, root=root), "team-alpha",
                       str(archive), workspace=root / "ws", now=NOW)

            after = roster.read_text(encoding="utf-8")
            beta = "| team-beta | Beta | south-school | none | received | yes |"
            self.assertIn(beta, before)
            self.assertIn(beta, after)


class StateGuardTests(unittest.TestCase):
    def test_an_existing_checkout_is_not_replaced_without_force(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            archive = make_zip(root / "src" / "a.zip", {"app.py": "x = 1\n"})
            intake.run(event, "team-alpha", str(archive), workspace=root / "ws", now=NOW)
            with self.assertRaises(StateError):
                intake.run(event, "team-alpha", str(archive), workspace=root / "ws", now=NOW)

    def test_a_failed_forced_re_ingest_leaves_the_existing_checkout_intact(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            good = make_zip(root / "src" / "a.zip", {"app.py": "x = 1\n"})
            first = intake.run(event, "team-alpha", str(good),
                               workspace=root / "ws", now=NOW)
            evil = make_zip(root / "src" / "evil.zip", {"../../pwned.txt": "owned"})
            with self.assertRaises(SafetyError):
                intake.run(event, "team-alpha", str(evil),
                           workspace=root / "ws", force=True, now=NOW)
            self.assertEqual((first.checkout / "app.py").read_text(), "x = 1\n")

    def test_a_frozen_roster_is_not_modified(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            roster = event.directory / "teams.md"
            metadata, body = frontmatter.read(roster)
            metadata["frozen"] = True
            roster.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
            reloaded = event_module.load(event.directory, root=root)
            archive = make_zip(root / "src" / "a.zip", {"app.py": "x = 1\n"})
            with self.assertRaises(StateError) as caught:
                intake.run(reloaded, "team-alpha", str(archive),
                           workspace=root / "ws", now=NOW)
            self.assertIn("frozen", caught.exception.message)

    def test_intake_after_the_intake_stage_is_refused(self):
        with TemporaryFramework() as root:
            event = make_event(root, stage="initial-judging")
            archive = make_zip(root / "src" / "a.zip", {"app.py": "x = 1\n"})
            with self.assertRaises(StateError) as caught:
                intake.run(event, "team-alpha", str(archive),
                           workspace=root / "ws", now=NOW)
            self.assertIn("initial-judging", caught.exception.message)

    def test_force_is_what_overrides_a_frozen_roster(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            roster = event.directory / "teams.md"
            metadata, body = frontmatter.read(roster)
            metadata["frozen"] = True
            roster.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
            reloaded = event_module.load(event.directory, root=root)
            archive = make_zip(root / "src" / "a.zip", {"app.py": "x = 1\n"})
            result = intake.run(reloaded, "team-alpha", str(archive),
                                workspace=root / "ws", force=True, now=NOW)
            self.assertTrue(result.record.is_file())

    def test_an_invalid_team_id_is_refused(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            archive = make_zip(root / "src" / "a.zip", {"app.py": "x = 1\n"})
            with self.assertRaises(Exception):
                intake.run(event, "Team Alpha", str(archive),
                           workspace=root / "ws", now=NOW)


class ExecutionTests(unittest.TestCase):
    def test_intake_never_runs_the_submission(self):
        """A build file that would announce itself must stay silent."""
        with TemporaryFramework() as root:
            event = make_event(root)
            marker = root / "executed.txt"
            archive = make_zip(root / "src" / "a.zip", {
                "Makefile": f"all:\n\ttouch {marker}\n",
                "setup.py": f"open({str(marker)!r}, 'w').write('x')\n",
                "package.json": '{"scripts": {"postinstall": "touch /tmp/atj-intake-test"}}\n',
            })
            intake.run(event, "team-alpha", str(archive), workspace=root / "ws", now=NOW)
            self.assertFalse(marker.exists())

    def test_a_source_repository_hook_does_not_run(self):
        with TemporaryFramework() as root:
            event = make_event(root)
            source = root / "src" / "repo"
            make_repo(source)
            marker = root / "hook-ran.txt"
            hook = source / ".git" / "hooks" / "post-checkout"
            hook.write_text(f"#!/bin/sh\ntouch {marker}\n", encoding="utf-8")
            hook.chmod(0o755)
            intake.run(event, "team-alpha", str(source), workspace=root / "ws", now=NOW)
            self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
