"""Safe Markdown front-matter parsing.

Front matter is the machine-readable half of every human-reviewable artifact.
It is parsed with ``yaml.safe_load`` only: no object construction, no tags, no
code execution. Submission and report content is untrusted data.
"""

from __future__ import annotations

import datetime as _datetime
import re
from pathlib import Path
from typing import Any

import yaml

from .errors import ValidationError

_FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)

# Guard against a pathological front-matter block in an untrusted file.
MAX_FRONTMATTER_BYTES = 64 * 1024


def split(text: str, *, artifact: str | None = None) -> tuple[dict[str, Any], str]:
    """Return ``(metadata, body)``.

    Raises if the document has no front matter, if the block is absurdly large,
    or if it does not parse to a mapping.
    """
    match = _FRONTMATTER.match(text)
    if not match:
        raise ValidationError("missing YAML front matter", artifact=artifact)
    raw = match.group(1)
    if len(raw.encode("utf-8")) > MAX_FRONTMATTER_BYTES:
        raise ValidationError("front matter exceeds size limit", artifact=artifact)
    try:
        metadata = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise ValidationError(f"unparseable front matter: {exc}", artifact=artifact) from exc
    if metadata is None:
        metadata = {}
    if not isinstance(metadata, dict):
        raise ValidationError("front matter must be a mapping", artifact=artifact)
    return normalize(metadata), text[match.end():]


TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def normalize(value: Any) -> Any:
    """Coerce YAML's implicit date types back to canonical UTC strings.

    PyYAML turns an unquoted ``2026-09-16T15:14:35Z`` into a ``datetime``, which
    then fails the schema's string pattern. Normalising on read means an operator
    can write a timestamp with or without quotes and get the same result.
    """
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, _datetime.datetime):
        return value.astimezone(_datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if isinstance(value, _datetime.date):
        return value.strftime("%Y-%m-%d")
    return value


class _Dumper(yaml.SafeDumper):
    """Quotes timestamp-shaped strings so they survive the next safe_load."""


def _represent_str(dumper: yaml.SafeDumper, data: str):
    style = '"' if TIMESTAMP.match(data) else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


_Dumper.add_representer(str, _represent_str)


def read(path: Path) -> tuple[dict[str, Any], str]:
    return split(read_text(path), artifact=str(path))


def read_text(path: Path) -> str:
    """Read an artifact that may contain untrusted bytes.

    Undecodable bytes are replaced rather than raising: a malformed submission
    file must produce a validation error, not a traceback out of the validator.
    """
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_bytes().decode("utf-8", errors="replace")
    except OSError as exc:
        raise ValidationError(f"cannot read artifact: {exc}", artifact=str(path)) from exc


def dump(metadata: dict[str, Any], body: str) -> str:
    """Render front matter + body deterministically.

    Key order is preserved as given, so callers control the reading order of the
    generated artifact. ``sort_keys=False`` is deliberate.
    """
    block = yaml.dump(
        normalize(metadata), Dumper=_Dumper, sort_keys=False,
        default_flow_style=False, allow_unicode=True,
    )
    if not body.startswith("\n"):
        body = "\n" + body
    return f"---\n{block}---{body}"


def has_frontmatter(text: str) -> bool:
    return _FRONTMATTER.match(text) is not None
