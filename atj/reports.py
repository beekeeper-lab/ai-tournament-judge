"""Artifact validation.

Every check here is derived from something already canonical: the schemas define
structure, the rubric defines criteria and weights, the persona registry defines
persona versions, the templates define required sections, and
`framework/policies/report-publication.md` defines visibility. Nothing in this
module is a second copy of any of those.

The v0.1.0-alpha validator checked for the substring ``event_id:``, a five-item
placeholder blocklist, and nothing else. An empty report passed. A report
claiming "score 9 of 5" passed. A public artifact containing a credential passed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from . import canon, frontmatter, ids, publication, schema, versions
from .errors import AtjError
from .publication import Finding

# Event subdirectory -> (schema name, template file)
ARTIFACT_KINDS = {
    "evidence": ("evidence-manifest", "evidence-manifest.md"),
    "judgments": ("judgment", "individual-judgment.md"),
    "summaries": ("consolidated-report", "consolidated-team-report.md"),
    "matchups": ("matchup", "matchup-report.md"),
    "adjudications": ("adjudication", "adjudication-report.md"),
    "dossiers": ("dossier", "team-dossier.md"),
    "audits": (None, "audit-report.md"),
    "submissions": ("submission-intake", "submission-intake.md"),
    "runs": ("model-run", "model-run-record.md"),
    "public": ("public-report", None),
}

TEMPLATE_DIR = "framework/templates"

PLACEHOLDERS = (
    "EVENT-ID", "TEAM-ID", "TEAM-A", "TEAM-B", "JUDGE-ID", "MATCH-ID", "ROUND-ID",
    "IMMUTABLE-COMMIT", "EVIDENCE-ID", "FRAMEWORK-COMMIT", "MODEL-REQUESTED",
    "MODEL-USED", "PERSONA@VERSION", "ADJUDICATION-ID", "AUDIT-ID", "RUN-ID",
    "OVERRIDE-ID", "CALIBRATION-ID", "SEED", "INPUT-DIGEST", "SCOPE",
    "HUMAN-OFFICIAL-ROLE", "REPOSITORY-URL-OR-PATH", "YYYY-MM-DDTHH:MM:SSZ",
    "replace-me", "REPLACE-ME", "TBD",
)

_HEADING = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_EVIDENCE_REF = re.compile(r"\[\[(?:evidence|ev):([^\]]+)\]\]")


@dataclass
class ArtifactReport:
    path: Path
    kind: str | None
    findings: list[Finding]

    @property
    def blocking(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "blocking"]

    @property
    def ok(self) -> bool:
        return not self.blocking


def _finding(severity: str, rule: str, detail: str, path: Path) -> Finding:
    return Finding(severity, rule, detail, str(path))


def template_sections(template: str, root: Path) -> list[str]:
    """Required ``##`` sections, read from the template itself."""
    path = root / TEMPLATE_DIR / template
    if not path.is_file():
        return []
    _, body = frontmatter.read(path)
    return [heading.strip() for heading in _HEADING.findall(body)]


def artifact_kind(path: Path, event_dir: Path) -> str | None:
    try:
        relative = path.relative_to(event_dir)
    except ValueError:
        return None
    return relative.parts[0] if relative.parts else None


def validate_artifact(
    path: Path,
    event_dir: Path,
    *,
    root: Path,
    public_scores: bool = False,
    all_teams: Iterable[str] = (),
    require_sections: bool = True,
) -> ArtifactReport:
    findings: list[Finding] = []
    kind = artifact_kind(path, event_dir)

    try:
        metadata, body = frontmatter.read(path)
    except AtjError as exc:
        return ArtifactReport(path, kind, [_finding("blocking", "front-matter", exc.message, path)])

    schema_name, template = ARTIFACT_KINDS.get(kind or "", (None, None))

    if schema_name:
        for message in schema.validate(schema_name, metadata, root=root, artifact=str(path)):
            findings.append(_finding("blocking", "schema", message, path))

    # Version compatibility. Public artifacts pin a rubric too, and a skew there
    # matters just as much: a public summary generated under an old rubric is
    # a misstatement of how the team was judged.
    if "rubric" in metadata:
        try:
            versions.require_versions(metadata, root=root, artifact=str(path))
        except AtjError as exc:
            findings.append(_finding("blocking", "version", exc.message, path))

    for placeholder in PLACEHOLDERS:
        if placeholder in body or placeholder in str(metadata):
            findings.append(
                _finding("blocking", "placeholder", f"unresolved placeholder {placeholder!r}", path)
            )
            break

    if require_sections and template:
        present = {heading.lower() for heading in _HEADING.findall(body)}
        for required in template_sections(template, root):
            if required.lower() not in present:
                findings.append(
                    _finding("major", "section", f"missing required section: {required!r}", path)
                )

    for field, value in sorted(metadata.items()):
        if field not in ids.PATTERNS or value in (None, ""):
            continue
        try:
            ids.validate_identifier(field, str(value), artifact=str(path))
        except AtjError as exc:
            findings.append(_finding("blocking", "identifier", exc.message, path))

    if schema_name == "judgment":
        findings.extend(_check_judgment_scores(metadata, path, root))

    if not body.strip():
        findings.append(_finding("blocking", "empty", "artifact has no content below its front matter", path))

    findings.extend(
        publication.check_artifact(
            path, event_dir, metadata, body,
            public_scores=public_scores, all_teams=all_teams,
        )
    )
    return ArtifactReport(path, kind, findings)


def _check_judgment_scores(metadata: dict[str, Any], path: Path, root: Path) -> list[Finding]:
    """Scores must match the canonical rubric exactly, in ids and in range."""
    findings: list[Finding] = []
    rubric = canon.load(root)
    scores = metadata.get("scores")
    if not isinstance(scores, dict):
        return [_finding("blocking", "scores", "scores must be a mapping", path)]
    supplied, expected = set(scores), set(rubric.criterion_ids)
    for missing in sorted(expected - supplied):
        findings.append(_finding("blocking", "scores", f"missing criterion {missing!r}", path))
    for extra in sorted(supplied - expected):
        findings.append(
            _finding("blocking", "scores", f"criterion {extra!r} is not in the rubric", path)
        )
    for criterion in sorted(supplied & expected):
        try:
            rubric.validate_score(scores[criterion], criterion_id=criterion, artifact=str(path))
        except AtjError as exc:
            findings.append(_finding("blocking", "scores", exc.message, path))
    return findings


def missing_evidence_references(body: str, manifest_ids: Iterable[str]) -> list[str]:
    """Report `[[evidence:ID]]` citations that the manifest does not define."""
    known = set(manifest_ids)
    return sorted({ref for ref in _EVIDENCE_REF.findall(body) if ref not in known})


def validate_event_reports(
    event_dir: Path,
    *,
    root: Path,
    public_scores: bool = False,
    all_teams: Iterable[str] = (),
) -> list[ArtifactReport]:
    reports: list[ArtifactReport] = []
    for kind in sorted(ARTIFACT_KINDS):
        directory = event_dir / kind
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*.md")):
            reports.append(
                validate_artifact(
                    path, event_dir, root=root,
                    public_scores=public_scores, all_teams=all_teams,
                )
            )
    return reports


def summarize(reports: Iterable[ArtifactReport]) -> dict[str, Any]:
    reports = list(reports)
    findings = [finding for report in reports for finding in report.findings]
    counts = {
        severity: sum(1 for f in findings if f.severity == severity)
        for severity in ("blocking", "major", "minor", "advisory")
    }
    return {
        "artifacts": len(reports),
        "counts": counts,
        "result": "FAIL" if counts["blocking"] or counts["major"]
        else ("PASS WITH ADVISORIES" if counts["minor"] or counts["advisory"] else "PASS"),
        "findings": findings,
    }
