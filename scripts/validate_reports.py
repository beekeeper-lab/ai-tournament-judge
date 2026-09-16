#!/usr/bin/env python3
"""Validate basic identity, front matter, placeholders, and visibility in event reports."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
REPORT_DIRS = ("judgments", "summaries", "matchups", "dossiers", "public", "audits")


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        return [f"Missing front matter: {path}"]
    metadata = match.group(1)
    if "event_id:" not in metadata:
        errors.append(f"Missing event_id: {path}")
    if "visibility:" not in metadata and path.parent.name not in {"summaries", "matchups"}:
        errors.append(f"Missing visibility: {path}")
    placeholders = ("EVENT-ID", "TEAM-ID", "IMMUTABLE-COMMIT", "EVIDENCE-ID", "TBD")
    if any(value in text for value in placeholders):
        errors.append(f"Unresolved placeholder: {path}")
    return errors


def validate_event(event_dir: Path) -> list[str]:
    errors: list[str] = []
    for directory in REPORT_DIRS:
        root = event_dir / directory
        if root.is_dir():
            for path in root.rglob("*.md"):
                errors.extend(validate_file(path))
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("event_dir", type=Path)
    args = parser.parse_args()
    errors = validate_event(args.event_dir)
    for error in errors:
        print(f"ERROR: {error}")
    print(f"Report validation: {'FAIL' if errors else 'PASS'} ({len(errors)} errors)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
