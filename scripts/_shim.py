"""Shared plumbing for the v0.1.0-alpha compatibility shims.

Each shim forwards to `atj` and prints where the real implementation now lives.
They exist so a half-finished event or an operator's muscle memory does not break
on upgrade. They add no behavior of their own.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from atj.cli import main  # noqa: E402


def forward(script: str, replacement: str, argv: list[str]) -> int:
    print(
        f"note: scripts/{script} is retired; forwarding to `atj {replacement}`. "
        f"Use the atj command directly.",
        file=sys.stderr,
    )
    return main(replacement.split() + argv)
