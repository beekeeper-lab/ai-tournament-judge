"""Stable identifiers.

Every official fact is addressable by a string that a human can read and a
script can verify. Identifiers are derived, never invented at random, so the
same inputs always produce the same identifier and a changed input produces a
visibly different one. That property is what makes staleness detectable.

Shapes
------
event                 ``spring-2026-finals``
team                  ``team-lumen``
submission commit     40 lowercase hex (abbreviated to 12 inside composite IDs)
evidence package      ``ev:<event>:<team>:<commit12>:<digest8>``
rubric version        ``submission-evaluation@1.0.0``
persona version       ``judge-backend@1.0.0``
framework commit      40 lowercase hex, or ``uncommitted``
judge run             ``jr:<event>:<team>:<judge>:<evidence-digest8>:<attempt>``
matchup               ``mu:<event>:<round>:<slot>``
adjudication          ``adj:<event>:<scope>:<seq02>``
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from .errors import ValidationError

SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX_ANY = re.compile(r"^[0-9a-f]{7,64}$")
REFERENCE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*@\d+\.\d+\.\d+$")
UNCOMMITTED = "uncommitted"

EVIDENCE_ID = re.compile(r"^ev:[a-z0-9-]+:[a-z0-9-]+:[0-9a-f]{12}:[0-9a-f]{8}$")
JUDGE_RUN_ID = re.compile(r"^jr:[a-z0-9-]+:[a-z0-9-]+:[a-z0-9-]+:[0-9a-f]{8}:\d{2}$")
MATCHUP_ID = re.compile(r"^mu:[a-z0-9-]+:[a-z0-9-]+:\d{2}$")
ADJUDICATION_ID = re.compile(r"^adj:[a-z0-9-]+:[a-z0-9-]+:\d{2}$")


def require_slug(value: str, *, kind: str, artifact: str | None = None) -> str:
    if not isinstance(value, str) or not SLUG.fullmatch(value):
        raise ValidationError(
            f"{kind} must be lowercase alphanumeric with single hyphens, got {value!r}",
            artifact=artifact,
        )
    return value


def require_commit(value: str, *, artifact: str | None = None, full: bool = False) -> str:
    if not isinstance(value, str):
        raise ValidationError(f"commit must be a string, got {value!r}", artifact=artifact)
    pattern = HEX40 if full else HEX_ANY
    if not pattern.fullmatch(value):
        expect = "40 lowercase hex characters" if full else "at least 7 lowercase hex characters"
        raise ValidationError(f"commit must be {expect}, got {value!r}", artifact=artifact)
    return value


def require_reference(value: str, *, kind: str, artifact: str | None = None) -> str:
    """Validate an ``id@semver`` reference such as ``submission-evaluation@1.0.0``."""
    if not isinstance(value, str) or not REFERENCE.fullmatch(value):
        raise ValidationError(
            f"{kind} must look like name@MAJOR.MINOR.PATCH, got {value!r}", artifact=artifact
        )
    return value


def split_reference(value: str) -> tuple[str, str]:
    name, _, version = value.partition("@")
    return name, version


def digest(*parts: str, length: int = 8) -> str:
    """Stable short digest over ordered parts. Order is significant."""
    payload = "\x1f".join(parts).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:length]


def file_digest(path: Path, length: int = 64) -> str:
    """SHA-256 of a file, used to identify material evidence artifacts."""
    sha = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()[:length]


def content_digest(text: str, length: int = 8) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


DIGEST = re.compile(r"^[0-9a-f]{8,64}$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def evidence_package_id(event_id: str, team_id: str, commit: str, manifest_digest: str) -> str:
    """Identify an evidence package by what it contains, not when it was made.

    Re-preparing identical evidence yields the same ID; changing any recorded
    evidence yields a different one, which is what marks downstream judgments
    stale.
    """
    require_slug(event_id, kind="event_id")
    require_slug(team_id, kind="team_id")
    require_commit(commit)
    if not DIGEST.fullmatch(manifest_digest):
        raise ValidationError(
            f"manifest digest must be lowercase hex, got {manifest_digest!r}"
        )
    return f"ev:{event_id}:{team_id}:{commit[:12]}:{manifest_digest[:8]}"


def judge_run_id(
    event_id: str, team_id: str, judge_id: str, evidence_package: str, attempt: int = 1
) -> str:
    require_slug(event_id, kind="event_id")
    require_slug(team_id, kind="team_id")
    require_slug(judge_id, kind="judge_id")
    if not EVIDENCE_ID.fullmatch(evidence_package):
        raise ValidationError(f"malformed evidence package id: {evidence_package!r}")
    if not 1 <= attempt <= 99:
        raise ValidationError(f"attempt must be 1-99, got {attempt}")
    return f"jr:{event_id}:{team_id}:{judge_id}:{evidence_package.rsplit(':', 1)[-1]}:{attempt:02d}"


def matchup_id(event_id: str, round_id: str, slot: int) -> str:
    require_slug(event_id, kind="event_id")
    require_slug(round_id, kind="round_id")
    if not 1 <= slot <= 99:
        raise ValidationError(f"matchup slot must be 1-99, got {slot}")
    return f"mu:{event_id}:{round_id}:{slot:02d}"


def adjudication_id(event_id: str, scope: str, sequence: int) -> str:
    require_slug(event_id, kind="event_id")
    require_slug(scope, kind="adjudication scope")
    if not 1 <= sequence <= 99:
        raise ValidationError(f"adjudication sequence must be 1-99, got {sequence}")
    return f"adj:{event_id}:{scope}:{sequence:02d}"


def persona_reference(agent_id: str, version: str) -> str:
    require_slug(agent_id, kind="agent_id")
    if not SEMVER.fullmatch(str(version)):
        raise ValidationError(f"persona version must be MAJOR.MINOR.PATCH, got {version!r}")
    return f"{agent_id}@{version}"


PATTERNS = {
    "event_id": SLUG,
    "team_id": SLUG,
    "judge_id": SLUG,
    "round_id": SLUG,
    "commit": HEX_ANY,
    "framework_commit": re.compile(r"^([0-9a-f]{7,64}|uncommitted)$"),
    "evidence_package_id": EVIDENCE_ID,
    "judge_run_id": JUDGE_RUN_ID,
    "match_id": MATCHUP_ID,
    "adjudication_id": ADJUDICATION_ID,
    "rubric": REFERENCE,
    "persona": REFERENCE,
    "consolidation_policy": REFERENCE,
    "matchup_rubric": REFERENCE,
    "bracket_policy": REFERENCE,
}


def validate_identifier(field: str, value: str, *, artifact: str | None = None) -> str:
    """Validate a known identifier field.

    An unknown field name raises rather than passing the value through: silently
    accepting anything is how an unchecked field reaches an official artifact.
    """
    pattern = PATTERNS.get(field)
    if pattern is None:
        raise ValidationError(
            f"no identifier rule for field {field!r}; known fields: "
            f"{', '.join(sorted(PATTERNS))}",
            artifact=artifact,
        )
    if not isinstance(value, str) or not pattern.fullmatch(value):
        raise ValidationError(
            f"{field} does not match the required shape {pattern.pattern}: {value!r}",
            artifact=artifact,
        )
    return value
