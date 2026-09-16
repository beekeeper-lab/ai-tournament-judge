import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_reports import validate_file  # noqa: E402


class ReportValidationTests(unittest.TestCase):
    def test_valid_report(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.md"
            path.write_text("---\nevent_id: demo\nvisibility: private\n---\n# Report\n", encoding="utf-8")
            self.assertEqual(validate_file(path), [])

    def test_placeholder_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.md"
            path.write_text("---\nevent_id: EVENT-ID\nvisibility: private\n---\n# Report\n", encoding="utf-8")
            self.assertTrue(validate_file(path))


if __name__ == "__main__":
    unittest.main()
