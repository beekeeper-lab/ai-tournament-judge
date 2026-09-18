"""Safe Markdown front-matter parsing.

Front matter is the machine-readable half of every human-reviewable artifact.
It is parsed with a bounded SafeLoader: no object construction, no tags, no code
execution, and a hard cap on node count so an alias-expansion bomb in an
untrusted report cannot hang the validator. Submission and report content is
untrusted data.
"""

from __future__ import annotations

import datetime as _datetime
import re
from pathlib import Path
from typing import Any

import yaml

from .errors import ValidationError

_FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)

# Guards against a pathological front-matter block in an untrusted file.
MAX_FRONTMATTER_BYTES = 64 * 1024
# Nested YAML aliases expand multiplicatively: seven levels of a nine-element
# alias is a few hundred bytes of input and tens of millions of constructed
# objects, so a byte limit is no defence. Anchors and aliases have no legitimate
# use in this framework's front matter, so they are refused outright. That is a
# complete defence rather than a budget an attacker can tune against.
MAX_YAML_NODES = 50_000


class _BoundedLoader(yaml.SafeLoader):
    """SafeLoader that refuses anchors, aliases, and oversized documents.

    Front matter is read from submissions and reports, which CLAUDE.md classes as
    untrusted. A validator that can be hung by the file it is validating is not a
    validator.
    """

    def __init__(self, stream):
        super().__init__(stream)
        self._node_budget = MAX_YAML_NODES

    def compose_node(self, parent, index):
        self._node_budget -= 1
        if self._node_budget < 0:
            raise yaml.YAMLError(
                f"front matter composes more than {MAX_YAML_NODES} nodes; refusing to parse"
            )
        return super().compose_node(parent, index)

    def compose_scalar_node(self, anchor):
        self._reject_anchor(anchor)
        return super().compose_scalar_node(anchor)

    def compose_sequence_node(self, anchor):
        self._reject_anchor(anchor)
        return super().compose_sequence_node(anchor)

    def compose_mapping_node(self, anchor):
        self._reject_anchor(anchor)
        return super().compose_mapping_node(anchor)

    @staticmethod
    def _reject_anchor(anchor):
        if anchor is not None:
            raise yaml.YAMLError(
                "front matter uses a YAML anchor. Anchors and aliases are refused: "
                "nested aliases expand multiplicatively and this content is untrusted."
            )


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
        metadata = yaml.load(raw, Loader=_BoundedLoader)
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

    ``dump(*split(text)) == text`` for any artifact this framework writes, and
    that matters: every ``atj render`` command reads an artifact, changes one
    generated block and writes the whole file back. A dump that reflowed the
    front matter or ate a blank line would put unexplained churn in the diff of
    a reviewed artifact, and a reviewer who learns to skim render diffs is a
    reviewer who will skim the one that moved a number.

    ``width`` is set beyond any plausible line so a long scalar — a
    ``blocked_reasons`` entry naming four judges, say — is not re-wrapped into a
    continuation line on the first re-render.
    """
    block = yaml.dump(
        normalize(metadata), Dumper=_Dumper, sort_keys=False,
        default_flow_style=False, allow_unicode=True, width=1 << 20,
    )
    return f"---\n{block}---\n{body}"


def has_frontmatter(text: str) -> bool:
    return _FRONTMATTER.match(text) is not None
