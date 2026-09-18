#!/usr/bin/env python3
"""Copy the framework data a wheel needs into atj/data/ before building.

The tooling reads its canonical facts from `framework/`, `schemas/`,
`events/_template/` and `VERSION` at run time. A wheel that ships only the Python
installs a command that cannot start, which is exactly what shipped before this
existed. Run this in the build step, not by hand.
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "atj" / "data"
TREES = ("framework", "schemas")
FILES = ("VERSION",)


def main() -> int:
    # setuptools reuses build/lib when mtimes match, which shipped a wheel built
    # from a stale committed copy rather than from source. Start clean.
    for stale in (ROOT / "build", ROOT / "ai_tournament_judge.egg-info"):
        if stale.exists():
            shutil.rmtree(stale)
    if TARGET.exists():
        shutil.rmtree(TARGET)
    TARGET.mkdir(parents=True)
    for tree in TREES:
        shutil.copytree(ROOT / tree, TARGET / tree)
    shutil.copytree(ROOT / "events" / "_template", TARGET / "events" / "_template")
    for name in FILES:
        shutil.copy(ROOT / name, TARGET / name)
    count = sum(1 for path in TARGET.rglob("*") if path.is_file())
    print(f"staged {count} data files into {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
