"""An uninitialized gitlink must be disclosed at intake, not found by an auditor.

Found by `trial-2-2026`: ScribeVault carries `.claude/shared`, a gitlink to a
private repository. `atj intake` cloned without it, recorded nothing, and the
intake record then listed the submission's agent configuration as present while
half of it was absent and unfetchable.
"""

from pathlib import Path

from atj import intake


def _write_gitmodules(directory: Path) -> None:
    (directory / ".gitmodules").write_text(
        '[submodule ".claude/shared"]\n'
        "\tpath = .claude/shared\n"
        "\turl = git@github.com:beekeeper-lab/claude-kit.git\n"
    )


def test_no_gitmodules_means_no_notes(tmp_path):
    assert intake._submodule_notes(tmp_path) == []


def test_uninitialized_gitlink_is_reported(tmp_path, monkeypatch):
    _write_gitmodules(tmp_path)
    monkeypatch.setattr(
        intake, "_git",
        lambda *a, **k: "-3dff46d60e1285f68bb986b516813a535d14ef4d .claude/shared",
    )
    notes = intake._submodule_notes(tmp_path)
    assert len(notes) == 1
    assert ".claude/shared" in notes[0]
    assert "3dff46d60e1285f68bb986b516813a535d14ef4d" in notes[0]
    assert "outside the eligible scope" in notes[0]


def test_materialized_gitlink_is_not_reported(tmp_path, monkeypatch):
    _write_gitmodules(tmp_path)
    monkeypatch.setattr(
        intake, "_git",
        lambda *a, **k: " 3dff46d60e1285f68bb986b516813a535d14ef4d .claude/shared (v1.2)",
    )
    assert intake._submodule_notes(tmp_path) == []


def test_failed_status_is_reported_as_unverified(tmp_path, monkeypatch):
    _write_gitmodules(tmp_path)

    def boom(*a, **k):
        raise intake.ValidationError("git failed", artifact="x")

    monkeypatch.setattr(intake, "_git", boom)
    notes = intake._submodule_notes(tmp_path)
    assert len(notes) == 1
    assert "unverified" in notes[0]


def test_gitlink_at_the_wrong_commit_is_reported(tmp_path, monkeypatch):
    """A `+` gitlink is materialized, and not at the commit the pin names.

    It looks complete to anyone listing the tree, which makes it worse than an
    absent one. Found in `trial-2-2026`, in the repair round for the absent case.
    """
    _write_gitmodules(tmp_path)
    monkeypatch.setattr(
        intake, "_git",
        lambda *a, **k: "+aaaaaaaabbbbbbbbccccccccddddddddeeeeeeee .claude/shared (v2)",
    )
    notes = intake._submodule_notes(tmp_path)
    assert len(notes) == 1
    assert "does not match its own pin" in notes[0]
