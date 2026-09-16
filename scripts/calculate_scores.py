#!/usr/bin/env python3
"""Retired. Use `atj score`. See scripts/README.md."""

import sys

from _shim import forward

if __name__ == "__main__":
    raise SystemExit(forward("calculate_scores.py", "score", sys.argv[1:]))
