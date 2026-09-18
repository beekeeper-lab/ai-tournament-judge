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
    "audits": ("audit", "audit-report.md"),
    "submissions": ("submission-intake", "submission-intake.md"),
    "runs": ("model-run", "model-run-record.md"),
    "public": ("public-report", None),
    "calibrations": ("calibration", "calibration-report.md"),
    "overrides": ("manual-override", "manual-override-record.md"),
}

TEMPLATE_DIR = "framework/templates"

PLACEHOLDERS = (
    "EVENT-ID", "TEAM-ID", "TEAM-A", "TEAM-B", "JUDGE-ID", "MATCH-ID", "ROUND-ID",
    "IMMUTABLE-COMMIT", "EVIDENCE-ID", "FRAMEWORK-COMMIT", "MODEL-REQUESTED",
    "MODEL-USED", "PERSONA@VERSION", "ADJUDICATION-ID", "AUDIT-ID", "RUN-ID",
    "OVERRIDE-ID", "CALIBRATION-ID", "SAMPLE-ID", "SEED", "INPUT-DIGEST", "SCOPE",
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
    display_names: dict[str, str] | None = None,
    totals: dict[str, float] | None = None,
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

    # Nine templates invite `persona: <component>@VERSION`, which is more useful
    # to an author than a bare `PERSONA@VERSION` because it names the component
    # that should have produced the artifact. Left unreplaced it was caught only
    # as `persona mismatch` after the work was done — the same weakness D10
    # settled for the adjudication template. Matched on the field rather than as
    # a substring, because live-trial-2026's adjudication quotes the old
    # placeholder in its own prose and is frozen.
    if str(metadata.get("persona", "")).endswith("@VERSION"):
        findings.append(_finding(
            "blocking", "placeholder",
            f"persona {metadata['persona']!r} still carries the template's @VERSION. "
            f"Replace it with the registered version from framework/personas.md",
            path,
        ))

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
            display_names=display_names, totals=totals,
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


SIMILARITY_THRESHOLD = 0.80


def _shingles(text: str, size: int = 6) -> set[tuple[str, ...]]:
    words = re.findall(r"[a-z0-9']+", text.lower())
    return {tuple(words[i:i + size]) for i in range(max(0, len(words) - size + 1))}


def check_judge_independence(event_dir: Path) -> list[Finding]:
    """Detect judgments that look like each other rather than like the evidence.

    Independence is instructed, not enforced by the tool surface: a judge that was
    handed a sibling's report would produce text that resembles it. Near-duplicate
    prose between two judges on the same team is the observable consequence, so
    that is what this measures. A low score here proves nothing; a high one is a
    contamination signal an auditor must resolve.
    """
    findings: list[Finding] = []
    root = event_dir / "judgments"
    if not root.is_dir():
        return findings
    for team_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        bodies: dict[str, set] = {}
        for path in sorted(team_dir.glob("*.md")):
            try:
                _, body = frontmatter.read(path)
            except AtjError:
                continue
            bodies[path.name] = _shingles(body)
        names = sorted(bodies)
        for index, first in enumerate(names):
            for second in names[index + 1:]:
                left, right = bodies[first], bodies[second]
                if not left or not right:
                    continue
                overlap = len(left & right) / len(left | right)
                if overlap >= SIMILARITY_THRESHOLD:
                    findings.append(_finding(
                        "major", "independence",
                        f"{first} and {second} share {overlap:.0%} of their wording. "
                        f"Independent judges working from the same evidence do not "
                        f"phrase it the same way; check whether one saw the other.",
                        team_dir,
                    ))
    return findings


def check_consolidation(
    event_dir: Path, *, root: Path, expected_judges: Iterable[str] | None = None
) -> list[Finding]:
    """Recompute every consolidated total from the judgments it claims to summarise.

    A summary's official numbers are written into Markdown by an agent. Until this
    check existed, nothing compared them back against the judge reports, so a
    transcription error or an edited total passed every gate and then fed bye
    seeding. `atj score` being deterministic is irrelevant if its output is never
    the thing that ships.
    """
    from . import scoring

    findings: list[Finding] = []
    directory = event_dir / "summaries"
    if not directory.is_dir():
        return findings

    for path in sorted(directory.glob("*.md")):
        try:
            metadata, _ = frontmatter.read(path)
        except AtjError as exc:
            findings.append(_finding("blocking", "consolidation", exc.message, path))
            continue
        team_id = str(metadata.get("team_id") or path.stem)
        judgments_dir = event_dir / "judgments" / team_id
        if not judgments_dir.is_dir():
            findings.append(_finding(
                "blocking", "consolidation",
                f"no judgments directory for {team_id}; the summary cannot be verified", path,
            ))
            continue
        try:
            panel = scoring.load_panel(judgments_dir, root=root)
            resolutions = scoring.load_resolutions(
                event_dir / "adjudications", team_id=team_id, root=root
            )
            recomputed = scoring.consolidate(
                panel, expected_judges=expected_judges, resolutions=resolutions, root=root
            )
        except AtjError as exc:
            findings.append(_finding(
                "blocking", "consolidation",
                f"cannot recompute this summary: {exc.message}", path,
            ))
            continue

        for field in ("total", "display_total", "finalized"):
            claimed = metadata.get(field)
            actual = recomputed[field]
            if claimed != actual:
                findings.append(_finding(
                    "blocking", "consolidation",
                    f"{field} is {claimed!r} but recomputing from "
                    f"judgments/{team_id}/ gives {actual!r}",
                    path,
                ))

        claimed_runs = sorted(metadata.get("judge_run_ids") or [])
        actual_runs = sorted(recomputed["judge_run_ids"])
        if claimed_runs != actual_runs:
            findings.append(_finding(
                "blocking", "consolidation",
                f"judge_run_ids do not match the judgments on disk: "
                f"claimed {claimed_runs}, found {actual_runs}",
                path,
            ))
    return findings


def validate_event_reports(
    event_dir: Path,
    *,
    root: Path,
    public_scores: bool = False,
    all_teams: Iterable[str] = (),
    expected_judges: Iterable[str] | None = None,
) -> list[ArtifactReport]:
    reports: list[ArtifactReport] = []
    totals = publication.official_totals(event_dir)
    display_names = {
        str(team.get("id")): str(team.get("display_name") or team.get("id"))
        for team in _roster_display_names(event_dir)
    }
    for kind in sorted(ARTIFACT_KINDS):
        directory = event_dir / kind
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*.md")):
            reports.append(
                validate_artifact(
                    path, event_dir, root=root,
                    public_scores=public_scores, all_teams=all_teams,
                    display_names=display_names, totals=totals,
                )
            )

    # Rendered output in a public location is published content too. Scanning
    # only Markdown left every ceremony HTML file outside the gate.
    public_dir = event_dir / "public"
    if public_dir.is_dir():
        for path in sorted(public_dir.rglob("*.html")):
            reports.append(_validate_rendered(
                path, event_dir, public_scores=public_scores, totals=totals.values()
            ))

    dossier_dir = event_dir / "dossiers"
    if dossier_dir.is_dir():
        for path in sorted(dossier_dir.rglob("*.html")):
            reports.append(_validate_rendered_team(
                path, all_teams=all_teams, display_names=display_names, totals=totals
            ))

    consolidation = check_consolidation(
        event_dir, root=root, expected_judges=expected_judges
    )
    if consolidation:
        reports.append(ArtifactReport(event_dir / "summaries", "summaries", consolidation))

    independence = check_judge_independence(event_dir)
    if independence:
        reports.append(ArtifactReport(event_dir / "judgments", "judgments", independence))
    return reports


def _roster_display_names(event_dir: Path) -> list[dict]:
    from . import event as event_module

    path = event_dir / "teams.md"
    if not path.is_file():
        return []
    try:
        metadata, body = frontmatter.read(path)
    except AtjError:
        return []
    return metadata.get("teams") or event_module.parse_roster_table(body)


def _validate_rendered_team(
    path: Path, *, all_teams: Iterable[str], display_names: dict[str, str] | None = None,
    totals: dict[str, float] | None = None,
) -> ArtifactReport:
    """Gate rendered team-facing HTML. A team may see its own score, not another's."""
    try:
        text = frontmatter.read_text(path)
    except AtjError as exc:
        return ArtifactReport(path, "dossiers", [_finding("blocking", "read", exc.message, path)])
    findings = publication.scan_secrets(text, artifact=str(path))
    findings += publication.scan_deliberation(text, artifact=str(path))
    findings += publication.scan_private_identifiers(
        text, artifact=str(path), own_team=path.stem
    )
    findings += publication.scan_pii(text, artifact=str(path))
    findings += publication.scan_foreign_teams(
        text, own_team=path.stem, all_teams=all_teams, artifact=str(path),
        display_names=display_names,
    )
    findings += publication.scan_unapproved_scores(
        text, artifact=str(path), pattern_scan=False,
        known_totals=[v for team, v in (totals or {}).items() if team != path.stem],
    )
    return ArtifactReport(path, "dossiers", findings)


def _validate_rendered(
    path: Path, event_dir: Path, *, public_scores: bool,
    totals: Iterable[float] = (),
) -> ArtifactReport:
    """Gate rendered HTML sitting in a public location."""
    try:
        text = frontmatter.read_text(path)
    except AtjError as exc:
        return ArtifactReport(path, "public", [_finding("blocking", "read", exc.message, path)])
    findings = publication.scan_secrets(text, artifact=str(path))
    findings += publication.scan_deliberation(text, artifact=str(path))
    findings += publication.scan_private_identifiers(text, artifact=str(path))
    findings += publication.scan_pii(text, artifact=str(path))
    if not public_scores:
        findings += publication.scan_unapproved_scores(
            text, artifact=str(path), known_totals=totals or ()
        )
    return ArtifactReport(path, "public", findings)


def rendered_publication_findings(
    path: Path, event_dir: Path, *, public_scores: bool,
    all_teams: Iterable[str] = (), display_names: dict[str, str] | None = None,
    totals: dict[str, float] | None = None,
) -> list[Finding]:
    """Disclosure findings for rendered HTML, routed by where it lives.

    `atj validate publication` needs the same coverage over rendered output that
    `atj validate reports` already has, so a directory-wide disclosure gate does
    not stop at the Markdown (D24).
    """
    visibility = publication.expected_visibility(path, event_dir)
    if visibility == publication.TEAM:
        return _validate_rendered_team(
            path, all_teams=all_teams, display_names=display_names, totals=totals
        ).findings
    if visibility == publication.PUBLIC:
        return _validate_rendered(
            path, event_dir, public_scores=public_scores, totals=(totals or {}).values()
        ).findings
    try:
        text = frontmatter.read_text(path)
    except AtjError as exc:
        return [_finding("blocking", "read", exc.message, path)]
    return publication.scan_secrets(text, artifact=str(path))


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
