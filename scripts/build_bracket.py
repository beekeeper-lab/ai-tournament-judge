#!/usr/bin/env python3
"""Retired. Use `atj bracket build`. See scripts/README.md."""

import sys

from _shim import forward

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and not args[0].startswith("-"):
        args = ["--input", args[0]] + args[1:]
    raise SystemExit(forward("build_bracket.py", "bracket build", args))
