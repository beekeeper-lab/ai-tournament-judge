"""JSON Schema validation.

Schemas in ``schemas/`` are loaded into one registry so relative ``$ref``s
resolve offline. No schema is fetched over the network.

Schemas deliberately do not enumerate rubric criteria or pin a rubric version.
Those live in ``framework/rubrics/submission-evaluation.md`` and are enforced by
:mod:`atj.scoring`; duplicating them here would recreate the exact defect the
canonical data model exists to remove.
"""

from __future__ import annotations

import functools
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from .canon import repository_root
from .errors import SchemaError

SCHEMA_DIR = "schemas"

ARTIFACT_SCHEMAS = {
    "event": "event.schema.json",
    "roster": "roster.schema.json",
    "team": "team.schema.json",
    "submission-intake": "submission-intake.schema.json",
    "evidence-manifest": "evidence-manifest.schema.json",
    "judgment": "judgment.schema.json",
    "consolidated-report": "consolidated-report.schema.json",
    "adjudication": "adjudication.schema.json",
    "bracket": "bracket.schema.json",
    "matchup": "matchup.schema.json",
    "dossier": "dossier.schema.json",
    "public-report": "public-report.schema.json",
    "model-run": "model-run.schema.json",
    "status": "status.schema.json",
}


@functools.lru_cache(maxsize=4)
def _registry(root: Path) -> tuple[Registry, dict[str, dict]]:
    directory = root / SCHEMA_DIR
    if not directory.is_dir():
        raise SchemaError(f"schema directory not found: {directory}")
    documents: dict[str, dict] = {}
    resources = []
    for path in sorted(directory.glob("*.schema.json")):
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SchemaError(f"invalid JSON: {exc}", artifact=str(path)) from exc
        identifier = document.get("$id")
        if not identifier:
            raise SchemaError("schema is missing $id", artifact=str(path))
        documents[path.name] = document
        resources.append((identifier, Resource.from_contents(document)))
    return Registry().with_resources(resources), documents


def get_schema(name: str, root: Path | None = None) -> dict:
    base = root or repository_root()
    filename = ARTIFACT_SCHEMAS.get(name, name)
    _, documents = _registry(base)
    if filename not in documents:
        raise SchemaError(f"unknown schema: {name!r} (looked for {filename})")
    return documents[filename]


def validator(name: str, root: Path | None = None) -> Draft202012Validator:
    base = root or repository_root()
    registry, _ = _registry(base)
    return Draft202012Validator(get_schema(name, base), registry=registry)


def validate(
    name: str, instance: Any, *, root: Path | None = None, artifact: str | None = None
) -> list[str]:
    """Return human-readable messages. Empty list means valid.

    Errors are sorted by path so output is stable across runs and diffable in CI.
    """
    messages: list[str] = []
    for error in sorted(validator(name, root).iter_errors(instance), key=lambda e: list(e.path)):
        location = "/".join(str(part) for part in error.path) or "<root>"
        messages.append(f"{name}:{location}: {error.message}")
    return messages


def require(
    name: str, instance: Any, *, root: Path | None = None, artifact: str | None = None
) -> None:
    messages = validate(name, instance, root=root, artifact=artifact)
    if messages:
        raise SchemaError("; ".join(messages), artifact=artifact)


def check_schemas(root: Path | None = None) -> list[str]:
    """Self-check every shipped schema. Used by CI and the release validator."""
    base = root or repository_root()
    problems: list[str] = []
    registry, documents = _registry(base)
    for filename, document in sorted(documents.items()):
        try:
            Draft202012Validator.check_schema(document)
        except Exception as exc:  # noqa: BLE001 - surfaced as a message, not raised
            problems.append(f"{filename}: invalid schema: {exc}")
    for name, filename in sorted(ARTIFACT_SCHEMAS.items()):
        if filename not in documents:
            problems.append(f"{name}: declared schema file is missing: {filename}")
    return problems


def clear_cache() -> None:
    _registry.cache_clear()
