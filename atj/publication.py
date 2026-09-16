"""Publication boundary enforcement.

`framework/policies/report-publication.md` describes three visibility levels. In
v0.1.0-alpha nothing enforced them: a file in `public/` carrying
`visibility: private`, a live-looking credential, explicit judge deliberation and
an unapproved numeric score validated clean. This module is the enforcement.

The rules are deliberately conservative. A false positive costs an operator one
review; a false negative publishes a student's private record.

Scanning text cannot prove the absence of private content, and this module does
not claim it can. It is one control among several: schema-level field bans,
directory/visibility agreement, approval gating, and human publication approval.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .errors import ValidationError

PRIVATE, TEAM, PUBLIC = "private", "team", "public"

# Directory name -> the visibility artifacts there must declare.
DIRECTORY_VISIBILITY = {
    "judgments": PRIVATE,
    "summaries": PRIVATE,
    "matchups": PRIVATE,
    "audits": PRIVATE,
    "adjudications": PRIVATE,
    "evidence": PRIVATE,
    "submissions": PRIVATE,
    "runs": PRIVATE,
    "dossiers": TEAM,
    "public": PUBLIC,
}

# Front-matter keys that may never appear on a public artifact.
PRIVATE_ONLY_FIELDS = (
    "scores", "judge_run_ids", "judge_run_id", "judge_id", "persona",
    "comparisons", "passes", "blocked_reasons", "evidence_package_id",
    "adjudication_ids", "adjudication_id", "total", "display_total",
    "provisional_total", "commit", "commit_a", "commit_b",
    "evidence_package_a", "evidence_package_b", "source_scores",
)

# Keys a team-facing dossier may not carry: another team's identity, or the
# panel's internal deliberation.
TEAM_FORBIDDEN_FIELDS = ("judge_run_ids", "passes", "comparisons", "blocked_reasons")

_SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("AWS access key id", re.compile(r"\b(?:AKIA|ASIA|AIDA|AROA)[0-9A-Z]{16}\b")),
    ("AWS secret access key", re.compile(r"(?i)aws.{0,24}secret.{0,24}['\"][0-9a-zA-Z/+]{40}['\"]")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[0-9A-Za-z]{30,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[0-9A-Za-z-]{10,}\b")),
    ("OpenAI-style key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("Anthropic-style key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}\b")),
    ("private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----")),
    ("JSON Web Token", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}\b")),
    ("bearer credential", re.compile(r"(?i)\bauthorization:\s*bearer\s+[A-Za-z0-9._\-]{20,}")),
    ("inline password assignment", re.compile(r"(?i)\b(?:password|passwd|secret|api[_-]?key)\s*[:=]\s*['\"][^'\"\s]{8,}['\"]")),
    ("connection string with credentials", re.compile(r"(?i)\b[a-z][a-z0-9+.-]*://[^\s:@/]+:[^\s:@/]+@")),
)

# Phrases that indicate private deliberation has leaked into a shared artifact.
_DELIBERATION_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("judge deliberation", re.compile(r"(?i)\b(?:private )?(?:judge|panel) deliberation\b")),
    ("internal note", re.compile(r"(?i)\binternal(?:ly)? (?:note|only|comment)\b")),
    ("do not publish marker", re.compile(r"(?i)\bdo not (?:publish|share|disclose)\b")),
    ("named judge persona", re.compile(r"\bjudge-(?:backend|frontend-ux|security-ops|product-agentic)\b")),
    ("panel consolidator", re.compile(r"\bpanel-consolidator\b")),
    ("hidden reasoning marker", re.compile(r"(?i)\b(?:chain[- ]of[- ]thought|hidden reasoning|scratchpad)\b")),
    ("exploit instructions", re.compile(r"(?i)\b(?:exploit (?:steps|chain|payload)|proof[- ]of[- ]concept exploit)\b")),
)

_PRIVATE_ID_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("evidence package id", re.compile(r"\bev:[a-z0-9-]+:[a-z0-9-]+:[0-9a-f]{12}:[0-9a-f]{8}\b")),
    ("judge run id", re.compile(r"\bjr:[a-z0-9-]+:[a-z0-9-]+:[a-z0-9-]+:[0-9a-f]{8}:[0-9]{2}\b")),
    ("adjudication id", re.compile(r"\badj:[a-z0-9-]+:[a-z0-9-]+:[0-9]{2}\b")),
    ("full commit hash", re.compile(r"\b[0-9a-f]{40}\b")),
)

_SCORE_PATTERN = re.compile(r"\b\d{1,3}(?:\.\d)?\s*/\s*100\b")


@dataclass(frozen=True)
class Finding:
    severity: str
    rule: str
    detail: str
    artifact: str

    def render(self) -> str:
        return f"{self.severity.upper()} [{self.rule}] {self.artifact}: {self.detail}"


def scan_secrets(text: str, *, artifact: str = "") -> list[Finding]:
    findings = []
    for label, pattern in _SECRET_PATTERNS:
        for match in pattern.finditer(text):
            excerpt = match.group(0)
            redacted = excerpt[:6] + "…" if len(excerpt) > 8 else "…"
            findings.append(Finding("blocking", "secret", f"{label} ({redacted})", artifact))
    return findings


def scan_deliberation(text: str, *, artifact: str = "") -> list[Finding]:
    findings = []
    for label, pattern in _DELIBERATION_PATTERNS:
        match = pattern.search(text)
        if match:
            findings.append(
                Finding("blocking", "deliberation", f"{label}: {match.group(0)!r}", artifact)
            )
    return findings


def scan_private_identifiers(text: str, *, artifact: str = "") -> list[Finding]:
    findings = []
    for label, pattern in _PRIVATE_ID_PATTERNS:
        match = pattern.search(text)
        if match:
            findings.append(
                Finding("blocking", "private-identifier", f"{label}: {match.group(0)!r}", artifact)
            )
    return findings


def scan_foreign_teams(
    text: str, *, own_team: str, all_teams: Iterable[str], artifact: str = ""
) -> list[Finding]:
    """A team-facing dossier may name an opponent, but not carry its private detail.

    The dossier's own matchup history necessarily names opponents, so this reports
    an advisory for review rather than blocking. What blocks is another team's
    private identifiers, which the identifier scan already covers.
    """
    findings = []
    for team in sorted(set(all_teams) - {own_team}):
        if re.search(rf"\b{re.escape(team)}\b", text):
            findings.append(
                Finding("advisory", "foreign-team",
                        f"names another team ({team}); confirm only match-public detail is included",
                        artifact)
            )
    return findings


def check_public(
    metadata: dict[str, Any], body: str, *, artifact: str = "", public_scores: bool = False
) -> list[Finding]:
    """Everything that must hold before an artifact may be published."""
    findings: list[Finding] = []

    if metadata.get("visibility") != PUBLIC:
        findings.append(Finding(
            "blocking", "visibility",
            f"artifact is in a public location but declares visibility "
            f"{metadata.get('visibility')!r}",
            artifact,
        ))

    for field in PRIVATE_ONLY_FIELDS:
        if field in metadata:
            findings.append(Finding(
                "blocking", "private-field",
                f"private-only field {field!r} present on a public artifact", artifact,
            ))

    if metadata.get("approval_state") != "approved":
        findings.append(Finding(
            "blocking", "approval",
            f"approval_state is {metadata.get('approval_state')!r}; a human official must "
            f"approve publication", artifact,
        ))
    if not metadata.get("approved_by"):
        findings.append(Finding(
            "blocking", "approval", "approved_by is empty; publication approval is a human act",
            artifact,
        ))
    if not metadata.get("source_artifacts"):
        findings.append(Finding(
            "blocking", "provenance",
            "source_artifacts is empty; a public artifact must be traceable to the approved "
            "private records it was generated from", artifact,
        ))

    findings.extend(scan_secrets(body, artifact=artifact))
    findings.extend(scan_deliberation(body, artifact=artifact))
    findings.extend(scan_private_identifiers(body, artifact=artifact))

    if not public_scores and not metadata.get("scores_published"):
        match = _SCORE_PATTERN.search(body)
        if match:
            findings.append(Finding(
                "blocking", "unapproved-score",
                f"numeric score {match.group(0)!r} in a public artifact while the event has "
                f"public_scores disabled", artifact,
            ))
    return findings


def check_team_facing(
    metadata: dict[str, Any], body: str, *, artifact: str = "",
    own_team: str | None = None, all_teams: Iterable[str] = (),
) -> list[Finding]:
    findings: list[Finding] = []
    if metadata.get("visibility") != TEAM:
        findings.append(Finding(
            "blocking", "visibility",
            f"team-facing artifact declares visibility {metadata.get('visibility')!r}", artifact,
        ))
    for field in TEAM_FORBIDDEN_FIELDS:
        if field in metadata:
            findings.append(Finding(
                "blocking", "private-field",
                f"panel-internal field {field!r} present on a team-facing artifact", artifact,
            ))
    findings.extend(scan_secrets(body, artifact=artifact))
    findings.extend(scan_deliberation(body, artifact=artifact))
    if own_team:
        findings.extend(
            scan_foreign_teams(body, own_team=own_team, all_teams=all_teams, artifact=artifact)
        )
    return findings


def check_private(metadata: dict[str, Any], body: str, *, artifact: str = "") -> list[Finding]:
    """Private artifacts still must not accumulate live credentials."""
    findings: list[Finding] = []
    if metadata.get("visibility") != PRIVATE:
        findings.append(Finding(
            "blocking", "visibility",
            f"artifact in a private location declares visibility {metadata.get('visibility')!r}",
            artifact,
        ))
    findings.extend(scan_secrets(body, artifact=artifact))
    return findings


def expected_visibility(path: Path, event_dir: Path) -> str | None:
    try:
        relative = path.relative_to(event_dir)
    except ValueError:
        return None
    return DIRECTORY_VISIBILITY.get(relative.parts[0] if relative.parts else "")


def check_artifact(
    path: Path,
    event_dir: Path,
    metadata: dict[str, Any],
    body: str,
    *,
    public_scores: bool = False,
    all_teams: Iterable[str] = (),
) -> list[Finding]:
    """Route an artifact to the checks its location requires."""
    artifact = str(path)
    visibility = expected_visibility(path, event_dir)
    if visibility is None:
        return []
    if visibility == PUBLIC:
        return check_public(metadata, body, artifact=artifact, public_scores=public_scores)
    if visibility == TEAM:
        return check_team_facing(
            metadata, body, artifact=artifact,
            own_team=str(metadata.get("team_id") or ""), all_teams=all_teams,
        )
    return check_private(metadata, body, artifact=artifact)


def require_publishable(findings: Iterable[Finding]) -> None:
    blocking = [f for f in findings if f.severity == "blocking"]
    if blocking:
        raise ValidationError(
            "publication blocked:\n  " + "\n  ".join(f.render() for f in blocking)
        )
