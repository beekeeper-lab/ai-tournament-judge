"""ai-tournament-judge deterministic tooling.

Mechanical operations only: parsing, validation, arithmetic, rendering, state
transitions, and seeded bracket assignment. No LLM judgment happens here and
nothing in this package is a substitute for one.
"""

__all__ = ["VERSION"]

from pathlib import Path as _Path


def _read_version() -> str:
    """The VERSION file is the single source. pyproject mirrors it in PEP 440 form."""
    candidate = _Path(__file__).resolve().parent.parent / "VERSION"
    try:
        return candidate.read_text(encoding="utf-8").strip()
    except OSError:
        return "unknown"


VERSION = _read_version()
