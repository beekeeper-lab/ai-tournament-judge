#!/usr/bin/env python3
"""Fail when an unresolved placeholder appears outside a template or fixture.

Templates are *supposed* to contain `EVENT-ID` and `TBD`; that is what makes them
templates. A real event artifact containing one means a report was written but
never filled in, which is exactly the defect this check exists to catch.
"""

from __future__ import annotations

import sys
import re
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
# D29: files that *document* placeholders rather than containing unresolved ones.
# A placeholder here is allowed only inside backticks -- as a citation, which is
# what quoting it makes it. `docs/framework-fix-plan.md` explains D10, D27 and
# D29 themselves, each of which is about a template inviting
# `persona: PERSONA@VERSION`, so the plan cannot discuss them without naming
# them. Naming one in running prose is still a defect, and still caught.
QUOTED_ONLY = (
    "docs/framework-fix-plan.md",
    "docs/final-audit.md",
    "docs/agent-verification.md",
)
_QUOTED = re.compile(r"`[^`\n]*`")

SCANNED_SUFFIXES = (".md", ".json", ".yml", ".yaml", ".html")
SKIP_PARTS = {".git", "__pycache__", "node_modules", "dist", ".pytest_cache",
              "workspaces", "data"}


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
        if any(relative == name for name in QUOTED_ONLY):
            # Remove the citations, then hold the rest to the same standard.
            text = _QUOTED.sub("", text)
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
