#!/usr/bin/env python3
"""Perform dependency-free structural validation of an event directory."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED = ("event.md", "teams.md", "status.md", "bracket.md")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def validate(event_dir: Path, strict: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for name in REQUIRED:
        path = event_dir / name
        if not path.is_file():
            errors.append(f"Missing {path}")
            continue
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER.match(text)
        if not match:
            errors.append(f"Missing YAML front matter: {path}")
            continue
        if name != "bracket.md" and "event_id:" not in match.group(1):
            errors.append(f"Missing event_id: {path}")
        if "replace-me" in text or "TBD" in text:
            message = f"Template placeholder remains: {path}"
            (errors if strict else warnings).append(message)
    expected_dirs = ("submissions", "evidence", "judgments", "summaries", "matchups", "dossiers", "public", "audits")
    for name in expected_dirs:
        if not (event_dir / name).is_dir():
            errors.append(f"Missing directory: {event_dir / name}")
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("event_dir", type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    errors, warnings = validate(args.event_dir, args.strict)
    if not args.quiet:
        for warning in warnings:
            print(f"WARNING: {warning}")
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Validation: {'FAIL' if errors else 'PASS'} ({len(errors)} errors, {len(warnings)} warnings)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
