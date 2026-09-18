"""In-tree PEP 517 backend that stages the framework data before building.

`atj` reads its canonical facts -- the rubrics, the schemas, the event template
and `VERSION` -- from files at run time, and a wheel that ships only the Python
installs a command that cannot start:

    $ atj --version
    atj unknown
    $ atj release-check
    canon: framework root not found ... (no framework/rubrics/submission-evaluation.md)

`tools/stage_package_data.py` copies those files into `atj/data/`, and its own
docstring says to run it in the build step. There was no build step that did,
only a line in `docs/release-checklist.md` telling a person to remember. This is
that build step: any `pip install .`, `python -m build` or editable install goes
through it, so the wheel cannot be built without its data again.
"""

from __future__ import annotations

import sys
from pathlib import Path

from setuptools import build_meta as _upstream

ROOT = Path(__file__).resolve().parent
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))


def _stage() -> None:
    """Copy the canonical sources into `atj/data/`, when they are here to copy.

    A wheel built from an sdist has no `framework/` tree of its own to stage
    from -- the sdist ships the already-staged `atj/data/` instead. Re-staging
    there would delete the only copy, so this is a no-op in that case and a hard
    failure when neither exists, because a wheel with no data is the defect this
    backend was written for.
    """
    if (ROOT / "framework" / "rubrics").is_dir():
        import stage_package_data

        stage_package_data.main()
        return
    if (ROOT / "atj" / "data" / "VERSION").is_file():
        print("build_backend: framework/ is absent and atj/data/ is already staged")
        return
    raise SystemExit(
        "build_backend: neither framework/ nor a staged atj/data/ is present, so the "
        "wheel would install a command that cannot start"
    )


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    _stage()
    return _upstream.build_wheel(wheel_directory, config_settings, metadata_directory)


def build_sdist(sdist_directory, config_settings=None):
    _stage()
    return _upstream.build_sdist(sdist_directory, config_settings)


def build_editable(wheel_directory, config_settings=None, metadata_directory=None):
    _stage()
    return _upstream.build_editable(wheel_directory, config_settings, metadata_directory)


# Everything else is setuptools' own, unchanged.
get_requires_for_build_wheel = _upstream.get_requires_for_build_wheel
get_requires_for_build_sdist = _upstream.get_requires_for_build_sdist
get_requires_for_build_editable = _upstream.get_requires_for_build_editable
prepare_metadata_for_build_wheel = _upstream.prepare_metadata_for_build_wheel
prepare_metadata_for_build_editable = _upstream.prepare_metadata_for_build_editable
