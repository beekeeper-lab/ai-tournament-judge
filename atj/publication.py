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
import json
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
    "matchup-passes": PRIVATE,
    "audits": PRIVATE,
    "adjudications": PRIVATE,
    "evidence": PRIVATE,
    "submissions": PRIVATE,
    "runs": PRIVATE,
    "calibrations": PRIVATE,
    "overrides": PRIVATE,
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

# Scores get published in prose, not only as "73.3/100". Every form below was
# found publishing an official total past a gate that reported CLEAR.
_SCORE_PATTERN = re.compile(
    r"\b\d{1,3}(?:\.\d+)?\s*(?:/|out of|of)\s*100\b"
    r"|\b\d{1,3}\.\d+\s*(?:points|pts)\b"
    r"|\bscored?\s+\d{1,3}\.\d+\b"
    r"|\bfinished\s+(?:on|with)\s+\d{1,3}\.\d+\b"
    r"|\btotal\s+(?:of\s+)?\d{1,3}\.\d+\b",
    re.IGNORECASE,
)

# Personal data has no place in any artifact this framework produces. Teams are
# identified by team id; people are not identified at all.
_PII_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    # Excludes `name@1.2.3` version references, which are not addresses.
    ("email address", re.compile(r"\b[\w.+-]+@(?!\d+\.\d+\.\d+\b)[\w-]+\.[\w.-]{2,}\b")),
    ("phone number", re.compile(r"(?<!\d)(?:\+\d{1,3}[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?!\d)")),
    ("student or employee id", re.compile(r"(?i)\b(?:student|employee|matric)\s*(?:id|number|no\.?)\s*[:#]?\s*\w{4,}")),
    ("government id", re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)")),
    ("street address", re.compile(r"(?i)\b\d{1,5}\s+[A-Z][a-z]+\s+(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Drive|Dr)\b")),
)

# A sentence that both names another team and reads like a finding about it.
_FINDING_WORDS = re.compile(
    r"(?i)\b(?:vulnerab|exploit|defect|bug|failure|weakness|deficien|insecure|"
    r"broken|missing|score[ds]?|rated|penali[sz])\w*"
)


def scan_pii(text: str, *, artifact: str = "") -> list[Finding]:
    findings = []
    for label, pattern in _PII_PATTERNS:
        match = pattern.search(text)
        if match:
            findings.append(Finding(
                "blocking", "personal-data",
                f"{label} present; artifacts identify teams, never people", artifact,
            ))
    return findings


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


def scan_private_identifiers(
    text: str, *, artifact: str = "", own_team: str | None = None,
    own_commit: str | None = None,
) -> list[Finding]:
    """Find private identifiers.

    With ``own_team``, this is a team-facing scan: a team may legitimately be told
    which commit and evidence package were judged, so its *own* identifiers are
    allowed and only another team's are flagged. Without it, every private
    identifier is flagged, which is the public rule.
    """
    findings = []
    for label, pattern in _PRIVATE_ID_PATTERNS:
        for match in pattern.finditer(text):
            value = match.group(0)
            if own_team and f":{own_team}:" in value:
                continue
            if own_commit and value.startswith(own_commit[:12]):
                continue
            findings.append(
                Finding("blocking", "private-identifier", f"{label}: {value!r}", artifact)
            )
            break
    return findings


def scan_foreign_teams(
    text: str, *, own_team: str, all_teams: Iterable[str], artifact: str = "",
    display_names: dict[str, str] | None = None,
) -> list[Finding]:
    """A team-facing dossier may name an opponent; it may not carry their record.

    Naming an opponent is unavoidable in a matchup history, so a bare mention is
    an advisory. A mention that also carries a score, or sits in a sentence that
    reads like a finding about that team, is another team's private record
    reaching this team, and blocks.
    """
    findings = []
    display_names = display_names or {}
    for team in sorted(set(all_teams) - {own_team}):
        # Teams are named in prose by their display name far more often than by
        # their id, and matching only the id let another team's record through.
        aliases = [team]
        display = display_names.get(team)
        if display and display.lower() != own_team.lower():
            aliases.append(display)
        pattern = re.compile(
            "|".join(rf"\b{re.escape(alias)}\b" for alias in aliases), re.IGNORECASE
        )
        if not pattern.search(text):
            continue
        severity, detail = "advisory", (
            f"names another team ({team}); confirm only match-public detail is included"
        )
        for sentence in re.split(r"(?<=[.!?])\s+|\n", text):
            if not pattern.search(sentence):
                continue
            if _SCORE_PATTERN.search(sentence):
                severity, detail = "blocking", (
                    f"carries another team's score alongside {team}: {sentence.strip()[:120]!r}"
                )
                break
            if _FINDING_WORDS.search(sentence):
                severity, detail = "major", (
                    f"states a finding about another team ({team}): "
                    f"{sentence.strip()[:120]!r}"
                )
        findings.append(Finding(severity, "foreign-team", detail, artifact))
    return findings


def _walk_keys(value: Any, path: str = "") -> list[tuple[str, str]]:
    """Every key in a nested structure, with the path that reaches it."""
    found: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            where = f"{path}.{key}" if path else str(key)
            found.append((str(key), where))
            found.extend(_walk_keys(item, where))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(_walk_keys(item, f"{path}[{index}]"))
    return found


def _banned_fields(metadata: dict[str, Any], banned: Iterable[str]) -> list[tuple[str, str]]:
    """Banned keys anywhere in the metadata, not only at the top level."""
    forbidden = set(banned)
    return [(key, where) for key, where in _walk_keys(metadata) if key in forbidden]


def scan_unapproved_scores(
    text: str, *, artifact: str = "", known_totals: Iterable[float] = (),
    pattern_scan: bool = True,
) -> list[Finding]:
    """Numeric totals in content an event has not authorized scores for.

    Pattern matching catches the shapes a score is usually written in.
    ``known_totals`` closes the gap the patterns cannot: a specific official total
    appearing where it is not authorized blocks regardless of phrasing.

    ``pattern_scan=False`` is for the team tier, where a team seeing *its own*
    score is the point of the artifact; only another team's total is a leak.
    """
    findings: list[Finding] = []
    match = _SCORE_PATTERN.search(text) if pattern_scan else None
    if match:
        findings.append(Finding(
            "blocking", "unapproved-score",
            f"numeric score {match.group(0)!r} present while the event has public_scores "
            f"disabled", artifact,
        ))
    for total in known_totals:
        if re.search(rf"(?<![\d.]){re.escape(f'{total:g}')}(?![\d])", text):
            findings.append(Finding(
                "blocking", "unapproved-score",
                f"the official total {total:g} appears in content the event has not "
                f"authorized scores for", artifact,
            ))
            break
    return findings


def check_public(
    metadata: dict[str, Any], body: str, *, artifact: str = "", public_scores: bool = False,
    known_totals: Iterable[float] = (),
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

    for field, where in _banned_fields(metadata, PRIVATE_ONLY_FIELDS):
        findings.append(Finding(
            "blocking", "private-field",
            f"private-only field {field!r} present on a public artifact at {where!r}", artifact,
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

    surface = body + "\n" + json.dumps(metadata, default=str, sort_keys=True)
    findings.extend(scan_secrets(surface, artifact=artifact))
    findings.extend(scan_deliberation(surface, artifact=artifact))
    findings.extend(scan_private_identifiers(surface, artifact=artifact))

    if not public_scores:
        # scores_published is a claim the artifact makes, not an authorization it
        # grants. Only the event official's public_scores setting decides this.
        if metadata.get("scores_published"):
            findings.append(Finding(
                "blocking", "unapproved-score",
                "artifact declares scores_published: true while the event has public_scores "
                "disabled; an artifact cannot authorize its own disclosure", artifact,
            ))
        findings.extend(
            scan_unapproved_scores(body, artifact=artifact, known_totals=known_totals)
        )
    findings.extend(scan_pii(body, artifact=artifact))
    return findings


def check_team_facing(
    metadata: dict[str, Any], body: str, *, artifact: str = "",
    own_team: str | None = None, all_teams: Iterable[str] = (),
    display_names: dict[str, str] | None = None,
    other_totals: Iterable[float] = (),
) -> list[Finding]:
    findings: list[Finding] = []
    if metadata.get("visibility") != TEAM:
        findings.append(Finding(
            "blocking", "visibility",
            f"team-facing artifact declares visibility {metadata.get('visibility')!r}", artifact,
        ))
    for field, where in _banned_fields(metadata, TEAM_FORBIDDEN_FIELDS):
        findings.append(Finding(
            "blocking", "private-field",
            f"panel-internal field {field!r} present on a team-facing artifact at {where!r}",
            artifact,
        ))
    surface = body + "\n" + json.dumps(metadata, default=str, sort_keys=True)
    findings.extend(scan_secrets(surface, artifact=artifact))
    findings.extend(scan_deliberation(surface, artifact=artifact))
    findings.extend(scan_private_identifiers(
        surface, artifact=artifact, own_team=own_team,
        own_commit=str(metadata.get("commit") or "") or None,
    ))
    findings.extend(scan_pii(surface, artifact=artifact))
    # A team may see its own total. Another team's total in its dossier is that
    # team's private record reaching the wrong audience.
    findings.extend(scan_unapproved_scores(
        surface, artifact=artifact, known_totals=other_totals, pattern_scan=False
    ))
    if own_team:
        findings.extend(scan_foreign_teams(
            surface, own_team=own_team, all_teams=all_teams, artifact=artifact,
            display_names=display_names,
        ))
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


def official_totals(event_dir: Path) -> dict[str, float]:
    """Every finalized official total in this event, by team.

    Used to block a specific number appearing where it is not authorized, which
    pattern matching alone cannot do reliably.
    """
    from . import frontmatter as fm

    totals: dict[str, float] = {}
    directory = event_dir / "summaries"
    if not directory.is_dir():
        return totals
    for path in sorted(directory.glob("*.md")):
        try:
            metadata, _ = fm.read(path)
        except Exception:  # noqa: BLE001 - reported by report validation
            continue
        if metadata.get("finalized") and metadata.get("display_total") is not None:
            totals[str(metadata.get("team_id") or path.stem)] = float(metadata["display_total"])
    return totals


def check_artifact(
    path: Path,
    event_dir: Path,
    metadata: dict[str, Any],
    body: str,
    *,
    public_scores: bool = False,
    all_teams: Iterable[str] = (),
    display_names: dict[str, str] | None = None,
    totals: dict[str, float] | None = None,
) -> list[Finding]:
    """Route an artifact to the checks its location requires."""
    artifact = str(path)
    visibility = expected_visibility(path, event_dir)
    if visibility is None:
        # A publication gate that cannot tell where an artifact lives must not
        # report it clear. Failing open here would have passed a file full of
        # credentials whenever --event-dir was wrong or the path was nested.
        return [Finding(
            "blocking", "location-unknown",
            f"cannot determine the required visibility for this artifact relative to "
            f"{event_dir}. Either --event-dir is wrong, or the artifact sits in a "
            f"directory the framework does not declare "
            f"({', '.join(sorted(DIRECTORY_VISIBILITY))}). Undeclared locations are "
            f"blocked, not skipped: nothing stored outside a declared directory can be "
            f"cleared for release",
            artifact,
        )]
    totals = totals if totals is not None else official_totals(event_dir)
    if visibility == PUBLIC:
        return check_public(
            metadata, body, artifact=artifact, public_scores=public_scores,
            known_totals=totals.values(),
        )
    if visibility == TEAM:
        own = str(metadata.get("team_id") or path.stem)
        return check_team_facing(
            metadata, body, artifact=artifact, own_team=own, all_teams=all_teams,
            display_names=display_names,
            other_totals=[value for team, value in totals.items() if team != own],
        )
    return check_private(metadata, body, artifact=artifact)


def require_publishable(findings: Iterable[Finding]) -> None:
    blocking = [f for f in findings if f.severity == "blocking"]
    if blocking:
        raise ValidationError(
            "publication blocked:\n  " + "\n  ".join(f.render() for f in blocking)
        )
