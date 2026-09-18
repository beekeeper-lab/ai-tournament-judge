"""Project-local hooks are guard rails, and a guard rail that cries wolf gets routed around.

`.claude/hooks/` is not a security boundary -- `atj validate`, the publication
gate and the audit gates are. But a hook that blocks ordinary work teaches an
operator to disable it, which costs more than the hook was ever worth. During
live-trial-2026 the run-on-host guard blocked a `git commit` whose message body
merely discussed a submission, twice.
"""

import shutil
import subprocess
import unittest
from pathlib import Path

from _support import ROOT  # noqa: F401

GUARD_TESTS = ROOT / "tests" / "hooks" / "test_pre_advance_guard.sh"


class PreAdvanceHookTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which("bash"), "bash is not available")
    def test_the_guard_blocks_real_invocations_and_allows_prose(self):
        """Covers both halves: running submission code, and advancing a stage.

        D23 is the second half of D6. The execution guard learned to read a
        command rather than a string; the gate check kept matching the raw text,
        so a heredoc or a commit message that merely described an advance was
        blocked, and a chain that recorded a gate *before* advancing was blocked
        on a state its own first half was about to change.
        """
        self.assertTrue(GUARD_TESTS.is_file(), f"missing {GUARD_TESTS}")
        completed = subprocess.run(
            ["bash", str(GUARD_TESTS)],
            capture_output=True, text=True, cwd=ROOT, timeout=120, check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("0 failed", completed.stdout)


if __name__ == "__main__":
    unittest.main()
