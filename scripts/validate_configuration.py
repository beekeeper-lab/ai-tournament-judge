#!/usr/bin/env python3
"""Retired. Use `atj event validate`. See scripts/README.md."""

import sys

from _shim import forward

if __name__ == "__main__":
    raise SystemExit(forward("validate_configuration.py", "event validate", sys.argv[1:]))
