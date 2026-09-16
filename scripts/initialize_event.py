#!/usr/bin/env python3
"""Create a new event directory from events/_template."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


VALID_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def initialize(repository: Path, event_id: str) -> Path:
    if not VALID_ID.fullmatch(event_id):
        raise ValueError("Event ID must contain lowercase letters, digits, and single hyphens")
    source = repository / "events" / "_template"
    target = repository / "events" / event_id
    if target.exists():
        raise FileExistsError(f"Event already exists: {target}")
    shutil.copytree(source, target)
    for name in ("event.md", "teams.md", "status.md", "bracket.md"):
        path = target / name
        path.write_text(path.read_text(encoding="utf-8").replace("replace-me", event_id), encoding="utf-8")
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("event_id")
    parser.add_argument("--repository", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(initialize(args.repository.resolve(), args.event_id))


if __name__ == "__main__":
    main()
