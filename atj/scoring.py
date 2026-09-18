"""Official scoring and panel consolidation.

All arithmetic here is deterministic and reproducible. The LLM judgment that
produced the raw scores is not, and nothing in this module implies otherwise.

Criteria, weights, scale, and rubric version come from
``framework/rubrics/submission-evaluation.md`` via :mod:`atj.canon`. This module
holds no copy of them.

Rounding uses ``Decimal`` with the rule and precision declared in the rubric's
front matter. Binary floats would make .5 cases depend on representation, and
Python's default banker's rounding would turn 73.25 into 73.2 — an official total
must not change by 0.1 depending on which library rounded it.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal
from pathlib import Path
from typing import Any, Iterable

from . import canon, schema, versions
from .canon import NOT_ENOUGH_EVIDENCE, Rubric
from .errors import ValidationError

ALIGNED = "aligned"
MATERIAL = "material-disagreement"
SEVERE = "severe-disagreement"
NOT_SCORED = "not-scored"

def _thresholds(root: Path | None = None) -> dict[str, int]:
    """Agreement thresholds, read from framework/rubrics/panel-consolidation.md.

    They are declared in that file's front matter so the policy document and the
    code cannot drift apart.
    """
    policy = canon.load_consolidation_policy(root)
    return {
        "minimum_panel": int(policy.number("minimum_panel")),
        "aligned_max_range": int(policy.number("aligned_max_range")),
        "material_max_range": int(policy.number("material_max_range")),
        "outlier_distance": int(policy.number("outlier_distance")),
    }


_ROUNDING = {"half-up": ROUND_HALF_UP, "half-even": ROUND_HALF_EVEN}


def panel_rubric(judgments: Iterable["Judgment"], *, root: Path | None = None) -> Rubric:
    """The rubric a panel was judged under, read from the panel itself.

    Recomputing a completed event under today's rubric restates an official
    result under a contract nobody applied to it. Every judgment in a panel pins
    the same version -- panel integrity requires it -- so the panel names its own
    rubric, and a retired version is loaded from the archive. A panel that
    disagrees with itself is an error, not something to average over.
    """
    references = {judgment.rubric for judgment in judgments}
    if not references:
        return canon.load(root)
    if len(references) > 1:
        raise ValidationError(
            "this panel does not agree on one rubric version: "
            + ", ".join(sorted(references))
            + ". Judgments produced under different rubric versions are not "
              "comparable and cannot be consolidated"
        )
    return canon.load_reference(references.pop(), root)


def _rounding_mode(root: Path | None = None, rubric: Rubric | None = None) -> str:
    """The rounding rule, declared in the rubric's front matter."""
    declared = str((rubric or canon.load(root)).rounding)
    if declared not in _ROUNDING:
        raise ValidationError(
            f"rubric declares an unknown rounding rule {declared!r}; "
            f"expected one of {', '.join(sorted(_ROUNDING))}"
        )
    return declared


def _round(value: float | Decimal, places: int, root: Path | None = None) -> float:
    quant = Decimal(1).scaleb(-places)
    return float(Decimal(str(value)).quantize(quant, rounding=_ROUNDING[_rounding_mode(root)]))


@dataclass(frozen=True)
class Judgment:
    """One judge's scores for one team. Immutable once loaded."""

    judge_id: str
    judge_run_id: str
    team_id: str
    commit: str
    evidence_package_id: str
    rubric: str
    persona: str
    scores: dict[str, Any]
    confidence: dict[str, str] = field(default_factory=dict)
    source: str = ""

    @classmethod
    def from_metadata(cls, metadata: dict, *, source: str = "") -> "Judgment":
        return cls(
            judge_id=str(metadata["judge_id"]),
            judge_run_id=str(metadata["judge_run_id"]),
            team_id=str(metadata["team_id"]),
            commit=str(metadata["commit"]),
            evidence_package_id=str(metadata["evidence_package_id"]),
            rubric=str(metadata["rubric"]),
            persona=str(metadata["persona"]),
            scores=dict(metadata["scores"]),
            confidence=dict(metadata.get("confidence") or {}),
            source=source or str(metadata.get("judge_run_id", "")),
        )


def individual_score(
    judgment: Judgment, rubric: Rubric | None = None, *, root: Path | None = None
) -> dict[str, Any]:
    """Per-judge weighted result.

    An `NE` on any criterion means this judge produced no finalizable total. The
    partial total is reported for transparency but `total` stays ``None`` so it
    can never be mistaken for a score.
    """
    rubric = rubric or canon.load_reference(judgment.rubric, root)
    rubric.require_reference(judgment.rubric, artifact=judgment.source)

    supplied = set(judgment.scores)
    expected = set(rubric.criterion_ids)
    if supplied != expected:
        missing = sorted(expected - supplied)
        extra = sorted(supplied - expected)
        detail = []
        if missing:
            detail.append(f"missing {missing}")
        if extra:
            detail.append(f"not in the rubric: {extra}")
        raise ValidationError(
            f"judgment criteria do not match the canonical rubric ({'; '.join(detail)})",
            artifact=judgment.source,
        )

    criteria: dict[str, Any] = {}
    partial = Decimal("0")
    unresolved: list[str] = []
    for criterion in rubric.criteria:
        raw = rubric.validate_score(
            judgment.scores[criterion.id], criterion_id=criterion.id, artifact=judgment.source
        )
        if raw == NOT_ENOUGH_EVIDENCE:
            unresolved.append(criterion.id)
            criteria[criterion.id] = {
                "raw": NOT_ENOUGH_EVIDENCE,
                "weight": criterion.weight,
                "weighted_points": None,
                "confidence": judgment.confidence.get(criterion.id),
            }
            continue
        points = rubric.weighted_points(raw, criterion.id)
        partial += Decimal(str(points))
        criteria[criterion.id] = {
            "raw": raw,
            "weight": criterion.weight,
            "weighted_points": _round(points, 4),
            "confidence": judgment.confidence.get(criterion.id),
        }

    return {
        "judge_id": judgment.judge_id,
        "judge_run_id": judgment.judge_run_id,
        "persona": judgment.persona,
        "criteria": criteria,
        "unresolved_ne": unresolved,
        "total": None if unresolved else _round(partial, 4),
        "display_total": None if unresolved else _round(partial, rubric.display_decimals, root),
        "partial_total": _round(partial, 4),
    }


def _agreement(values: list[float], thresholds: dict[str, int]) -> str:
    spread = max(values) - min(values)
    if spread <= thresholds["aligned_max_range"]:
        return ALIGNED
    if spread <= thresholds["material_max_range"]:
        return MATERIAL
    return SEVERE


def _outliers(judge_ids: list[str], values: list[float], thresholds: dict[str, int]) -> list[str]:
    if len(values) < 3:
        return []
    median = statistics.median(values)
    return [
        judge_id
        for judge_id, value in zip(judge_ids, values)
        if abs(value - median) >= thresholds["outlier_distance"]
    ]


def check_panel_integrity(
    judgments: Iterable[Judgment], *, expected_judges: Iterable[str] | None = None,
    root: Path | None = None,
) -> list[str]:
    """Structural independence checks. Returns problems; empty means clean.

    These close alpha defect X8, where a one-judge panel and four copies of the
    same judge both produced clean official totals.
    """
    judgments = list(judgments)
    problems: list[str] = []
    minimum = _thresholds(root)["minimum_panel"]
    if len(judgments) < minimum:
        problems.append(
            f"panel has {len(judgments)} judgment(s); at least {minimum} are required"
        )

    seen_ids: dict[str, int] = {}
    seen_runs: dict[str, int] = {}
    for judgment in judgments:
        seen_ids[judgment.judge_id] = seen_ids.get(judgment.judge_id, 0) + 1
        seen_runs[judgment.judge_run_id] = seen_runs.get(judgment.judge_run_id, 0) + 1
    for judge_id, count in sorted(seen_ids.items()):
        if count > 1:
            problems.append(f"judge {judge_id!r} appears {count} times; judges must be distinct")
    for run_id, count in sorted(seen_runs.items()):
        if count > 1:
            problems.append(f"judge_run_id {run_id!r} appears {count} times; reports were reused")

    if expected_judges is not None:
        expected = set(expected_judges)
        present = set(seen_ids)
        for missing in sorted(expected - present):
            problems.append(f"configured judge {missing!r} produced no judgment")
        for unexpected in sorted(present - expected):
            problems.append(f"judgment from unconfigured judge {unexpected!r}")

    for attribute, label in (
        ("team_id", "team"),
        ("commit", "submission commit"),
        ("evidence_package_id", "evidence package"),
        ("rubric", "rubric version"),
    ):
        distinct = sorted({getattr(judgment, attribute) for judgment in judgments})
        if len(distinct) > 1:
            problems.append(
                f"judgments disagree on {label}: {distinct}; they did not evaluate the same thing"
            )
    return problems


def consolidate(
    judgments: Iterable[Judgment],
    *,
    rubric: Rubric | None = None,
    expected_judges: Iterable[str] | None = None,
    resolutions: dict[str, Any] | None = None,
    root: Path | None = None,
) -> dict[str, Any]:
    """Neutral panel consolidation.

    The consolidator never replaces a judge's score. ``resolutions`` carries
    adjudicated per-criterion outcomes that are recorded *alongside* the source
    scores, exactly as the consolidation policy requires.
    """
    judgments = sorted(judgments, key=lambda j: j.judge_id)
    rubric = rubric or panel_rubric(judgments, root=root)
    resolutions = resolutions or {}

    thresholds = _thresholds(root)
    integrity = check_panel_integrity(judgments, expected_judges=expected_judges, root=root)
    for judgment in judgments:
        rubric.require_reference(judgment.rubric, artifact=judgment.source)

    individuals = [individual_score(judgment, rubric, root=root) for judgment in judgments]

    criteria: dict[str, Any] = {}
    total = Decimal("0")
    blocked: list[str] = []
    adjudication_required: list[dict[str, str]] = []
    accepted_ne: list[dict[str, Any]] = []

    for criterion in rubric.criteria:
        judge_ids: list[str] = []
        values: list[float] = []
        ne_judges: list[str] = []
        sources: dict[str, Any] = {}
        for judgment in judgments:
            raw = rubric.validate_score(
                judgment.scores[criterion.id],
                criterion_id=criterion.id,
                artifact=judgment.source,
            )
            sources[judgment.judge_id] = raw
            if raw == NOT_ENOUGH_EVIDENCE:
                ne_judges.append(judgment.judge_id)
            else:
                judge_ids.append(judgment.judge_id)
                values.append(raw)

        resolution = resolutions.get(criterion.id)
        resolved_score = None
        ne_disposition = None
        # D11: an adjudication could *clear* an NE by supplying a score, and had
        # no way to *accept* one. `atj score` then re-reported the accepted NE as
        # unresolved and kept demanding adjudication, so a decision that had been
        # made was indistinguishable from one nobody had made.
        # `resolved_score: NE` is that decision, stated explicitly: the official
        # reviewed the criterion and the NE stands.
        if resolution is not None and resolution.get("resolved_score") is not None:
            candidate = rubric.validate_score(
                resolution["resolved_score"], criterion_id=criterion.id,
                artifact=str(resolution.get("adjudication_id") or "adjudication"),
            )
            if resolution.get("authority_withheld"):
                # The record exists and carries no authority to move a total.
                pass
            elif candidate == NOT_ENOUGH_EVIDENCE:
                ne_disposition = NE_ACCEPTED
            else:
                resolved_score = candidate
                ne_disposition = NE_CLEARED

        # An adjudicated score stands in for each judge who recorded NE. The
        # judge's own NE is preserved in source_scores; the resolution is
        # recorded beside it, never written over it.
        mean_values = list(values)
        if resolved_score is not None and ne_judges:
            mean_values.extend([resolved_score] * len(ne_judges))

        entry: dict[str, Any] = {
            "criterion": criterion.id,
            "name": criterion.name,
            "weight": criterion.weight,
            "source_scores": sources,
            "ne_judges": ne_judges,
            "scores": values,
            "mean_inputs": mean_values,
            "minimum": min(values) if values else None,
            "maximum": max(values) if values else None,
            "range": (max(values) - min(values)) if values else None,
            "mean": None,
            "weighted_points": None,
            "agreement": NOT_SCORED,
            "possible_outliers": _outliers(judge_ids, values, thresholds),
            "resolution": resolution,
            "ne_disposition": ne_disposition,
        }

        if ne_judges and resolved_score is None:
            # An NE is not a zero and is not averaged away. The rubric forbids an
            # official total while a criterion is NE, so an accepted NE still
            # blocks finalization -- but it blocks it as a decision that was made,
            # not as one that is outstanding.
            if ne_disposition == NE_ACCEPTED:
                accepted_ne.append({
                    "criterion": criterion.id,
                    "adjudication_id": resolution.get("adjudication_id"),
                    "decided_by": resolution.get("decided_by"),
                })
                blocked.append(
                    f"{criterion.id}: NE accepted by adjudication "
                    f"{resolution.get('adjudication_id')} "
                    f"({resolution.get('decided_by')}); the rubric permits no official total "
                    f"while a criterion is NE"
                )
            else:
                blocked.append(
                    f"{criterion.id}: unresolved NE from {', '.join(sorted(ne_judges))}"
                    + (
                        f"; adjudication {resolution.get('adjudication_id')} carries no "
                        f"authority ({resolution.get('authority_withheld')})"
                        if resolution is not None and resolution.get("authority_withheld")
                        else ""
                    )
                )
                adjudication_required.append(
                    {"criterion": criterion.id, "trigger": "unresolved-ne"}
                )
        if mean_values:
            mean = statistics.fmean(mean_values)
            points = rubric.weighted_points(mean, criterion.id)
            entry["mean"] = _round(mean, 4)
            entry["weighted_points"] = _round(points, 4)
            entry["resolved_score"] = resolved_score
            # Agreement describes what the judges said, not what the adjudicator
            # decided, so it is computed from the judges' own scores.
            entry["agreement"] = _agreement(values, thresholds) if values else NOT_SCORED
            if not ne_judges or resolved_score is not None:
                total += Decimal(str(points))
            if entry["agreement"] == SEVERE:
                adjudication_required.append(
                    {"criterion": criterion.id, "trigger": "severe-disagreement"}
                )
                if resolution is None:
                    blocked.append(
                        f"{criterion.id}: severe disagreement (range {entry['range']:g}) "
                        f"with no recorded adjudication"
                    )
                elif not resolution.get("rationale"):
                    blocked.append(
                        f"{criterion.id}: the adjudication records no reasoning for the "
                        f"severe disagreement"
                    )
            if entry["possible_outliers"]:
                adjudication_required.append(
                    {"criterion": criterion.id, "trigger": "possible-outlier"}
                )
                if resolution is None:
                    blocked.append(
                        f"{criterion.id}: possible outlier "
                        f"({', '.join(entry['possible_outliers'])}) with no recorded adjudication"
                    )
        if resolution is not None:
            entry["resolution_note"] = (
                "adjudicated resolution recorded alongside the source scores; "
                "no source score was modified"
            )
        criteria[criterion.id] = entry

    finalized = not blocked and not integrity
    result: dict[str, Any] = {
        "rubric": rubric.reference,
        "judge_count": len(judgments),
        "judge_ids": [judgment.judge_id for judgment in judgments],
        "judge_run_ids": [judgment.judge_run_id for judgment in judgments],
        "individuals": individuals,
        "criteria": criteria,
        "total": _round(total, 4) if finalized else None,
        "display_total": (
            _round(total, rubric.display_decimals, root) if finalized else None
        ),
        "provisional_total": _round(total, 4),
        "finalized": finalized,
        "blocked_reasons": blocked + integrity,
        "integrity_problems": integrity,
        "adjudication_required": adjudication_required,
        # D11: a decision that was made, reported as such. An accepted NE still
        # blocks an official total; it does not keep asking for the adjudication
        # it already has.
        "accepted_ne": accepted_ne,
        "withheld_authority": [
            dict(entry) for entry in (
                resolution for resolution in resolutions.values()
                if resolution.get("authority_withheld")
            )
        ],
    }
    return result


def load_judgment_file(path: Path, *, root: Path | None = None) -> Judgment:
    """Parse, schema-check, and version-check one judgment Markdown file."""
    from .frontmatter import read

    metadata, _ = read(path)
    schema.require("judgment", metadata, root=root, artifact=str(path))
    versions.require_versions(metadata, root=root, artifact=str(path))
    return Judgment.from_metadata(metadata, source=str(path))


HUMAN_OFFICIAL = "human-official"
AGENT_SUBSTITUTED = "agent-substituted"
NE_ACCEPTED = "accepted"
NE_CLEARED = "cleared"


def load_resolutions(directory: Path, *, team_id: str | None = None,
                     root: Path | None = None,
                     withheld: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Read adjudicated per-criterion resolutions for one team.

    Every condition here closes a way an adjudication could move a total it had
    no authority over. A record must be approved, resolved, name a human decider,
    be scoped to a criterion of *this* team, carry no match id, and validate
    against the adjudication schema and the canonical versions. Two approved
    resolutions for the same criterion are a conflict, not a last-file-wins race.
    """
    from . import schema as schema_module
    from . import versions as versions_module
    from .frontmatter import read

    resolutions: dict[str, Any] = {}
    withheld = withheld if withheld is not None else []
    if not directory.is_dir():
        return resolutions
    if not team_id:
        raise ValidationError(
            "a team id is required to load adjudications; resolutions are scoped to a "
            "team and applying an unscoped one would let a single record move any total"
        )

    for path in sorted(directory.glob("*.md")):
        metadata, _ = read(path)
        criterion = metadata.get("criterion")
        if not criterion:
            continue
        if metadata.get("scope") != "criterion":
            continue
        if metadata.get("resolution") != "resolved":
            continue
        if metadata.get("approval_state") != "approved":
            continue
        if not metadata.get("decided_by"):
            continue
        # D13: `decided_by` names a role, and an agent can write a role into a
        # required field as easily as a human can. The framework cannot verify
        # that a person decided; it can require the record to say which it was,
        # and refuse to move an official total on an answer it cannot rely on.
        # A record written before the field existed says nothing, and silence is
        # treated as insufficient rather than as consent.
        authority = metadata.get("decision_authority")
        authority_withheld = None
        if authority != HUMAN_OFFICIAL:
            authority_withheld = (
                f"decision_authority is {authority!r}; only {HUMAN_OFFICIAL!r} may move an "
                f"official total"
                if authority else
                "the record declares no decision_authority, so nothing establishes that a "
                "human official decided it"
            )
            withheld.append({
                "adjudication_id": metadata.get("adjudication_id"),
                "criterion": str(criterion),
                "decided_by": metadata.get("decided_by"),
                "decision_authority": authority,
                "source": str(path),
                "reason": authority_withheld,
            })
        # A criterion resolution belongs to exactly one team and to no matchup.
        if metadata.get("team_id") != team_id:
            continue
        if metadata.get("match_id"):
            raise ValidationError(
                f"adjudication {metadata.get('adjudication_id')!r} is scoped to a criterion "
                f"but also names a match; a record cannot be both",
                artifact=str(path),
            )
        schema_module.require("adjudication", metadata, root=root, artifact=str(path))
        versions_module.require_versions(metadata, root=root, artifact=str(path))

        key = str(criterion)
        if key in resolutions:
            raise ValidationError(
                f"two approved adjudications resolve {key!r} for {team_id}: "
                f"{resolutions[key]['source']} and {path}. A human official must "
                f"withdraw one before a total can be finalized.",
                artifact=str(path),
            )
        override = metadata.get("score_override")
        resolutions[key] = {
            "criterion": key,
            "adjudication_id": metadata.get("adjudication_id"),
            "resolved_score": (override or {}).get("resolved_score"),
            "rationale": (override or {}).get("rationale") or metadata.get("resolution_detail"),
            "decided_by": metadata.get("decided_by"),
            "decision_authority": authority,
            "authority_withheld": authority_withheld,
            "amendments": list(metadata.get("amendments") or []),
            "source": str(path),
        }
    return resolutions


def load_panel(directory: Path, *, root: Path | None = None) -> list[Judgment]:
    if not directory.is_dir():
        raise ValidationError(f"judgment directory not found: {directory}")
    return [load_judgment_file(path, root=root) for path in sorted(directory.glob("*.md"))]
