#!/usr/bin/env python3
"""Retired. Use `atj event init`. See scripts/README.md."""

import sys

from _shim import forward

if __name__ == "__main__":
    raise SystemExit(forward("initialize_event.py", "event init", sys.argv[1:]))
