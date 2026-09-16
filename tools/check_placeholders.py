#!/usr/bin/env python3
"""Fail when an unresolved placeholder appears outside a template or fixture.

Templates are *supposed* to contain `EVENT-ID` and `TBD`; that is what makes them
templates. A real event artifact containing one means a report was written but
never filled in, which is exactly the defect this check exists to catch.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from atj.reports import PLACEHOLDERS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

# Places a placeholder is legitimate: template definitions, the event template,
# hostile test fixtures, the audit records that quote them, and this file.
EXEMPT_PREFIXES = (
    "framework/templates/",
    "events/_template/",
    "tests/fixtures/",
    "docs/release-readiness-audit.md",
    "docs/implementation-plan.md",
    "tools/check_placeholders.py",
    "atj/reports.py",
    "atj/event.py",
    "CHANGELOG.md",
)
SCANNED_SUFFIXES = (".md", ".json", ".yml", ".yaml")
SKIP_PARTS = {".git", "__pycache__", "node_modules", "dist", ".pytest_cache", "workspaces"}


def main() -> int:
    problems: list[str] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in SCANNED_SUFFIXES:
            continue
        if SKIP_PARTS & set(path.parts):
            continue
        relative = str(path.relative_to(ROOT))
        if any(relative.startswith(prefix) for prefix in EXEMPT_PREFIXES):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for placeholder in PLACEHOLDERS:
            if placeholder in text:
                problems.append(f"{relative}: unresolved placeholder {placeholder!r}")
                break

    for problem in problems:
        print(f"ERROR {problem}")
    print(f"Placeholder check: {'FAIL' if problems else 'PASS'} ({len(problems)} problems)")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
