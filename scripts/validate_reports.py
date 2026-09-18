#!/usr/bin/env python3
"""Retired. Use `atj validate reports`. See scripts/README.md."""

import sys

from _shim import forward

if __name__ == "__main__":
    raise SystemExit(forward("validate_reports.py", "validate reports", sys.argv[1:]))
