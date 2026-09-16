"""Canonical rubric access.

`framework/rubrics/submission-evaluation.md` is the single authoritative source
for criterion IDs, names, weights, score range, and rubric version. Nothing else
in this repository may hold an editable copy of those numbers.

The Markdown table is the definition; this module is the only reader. If the
table and the front matter disagree, that is a fatal defect, not a warning.
"""

from __future__ import annotations

import functools
import re
from dataclasses import dataclass
from pathlib import Path

from .errors import CanonError, VersionError
from .frontmatter import read

SUBMISSION_RUBRIC = "framework/rubrics/submission-evaluation.md"
HEAD_TO_HEAD_RUBRIC = "framework/rubrics/head-to-head.md"
CONSOLIDATION_RUBRIC = "framework/rubrics/panel-consolidation.md"
BRACKET_POLICY = "framework/rubrics/bracket-assignment.md"

# | id | Criterion name | 25 | Central question |
_CRITERION_ROW = re.compile(
    r"^\|\s*([a-z][a-z0-9_-]*)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*([^|]*?)\s*\|\s*$", re.MULTILINE
)
# | 3 | Solid for the event; ... |
_ANCHOR_ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*$", re.MULTILINE)

NOT_ENOUGH_EVIDENCE = "NE"


@dataclass(frozen=True)
class Criterion:
    id: str
    name: str
    weight: int
    question: str


@dataclass(frozen=True)
class Rubric:
    """An immutable view of the authoritative rubric."""

    rubric_id: str
    version: str
    scale_min: int
    scale_max: int
    criteria: tuple[Criterion, ...]
    anchors: dict[int, str]
    source: str
    display_decimals: int = 1
    rounding: str = "half-up"

    @property
    def reference(self) -> str:
        """The `id@version` string recorded in every artifact."""
        return f"{self.rubric_id}@{self.version}"

    @property
    def criterion_ids(self) -> tuple[str, ...]:
        return tuple(c.id for c in self.criteria)

    @property
    def weights(self) -> dict[str, int]:
        return {c.id: c.weight for c in self.criteria}

    @property
    def total_weight(self) -> int:
        return sum(c.weight for c in self.criteria)

    def criterion(self, criterion_id: str) -> Criterion:
        for candidate in self.criteria:
            if candidate.id == criterion_id:
                return candidate
        raise CanonError(f"unknown criterion: {criterion_id}", artifact=self.source)

    def require_reference(self, reference: str, *, artifact: str | None = None) -> None:
        """Fatal on any mismatch. A version skew is never a warning."""
        if reference != self.reference:
            raise VersionError(
                f"rubric mismatch: artifact declares {reference!r}, canonical rubric is "
                f"{self.reference!r}; migrate or re-run rather than continuing",
                artifact=artifact,
            )

    def validate_score(self, value, *, criterion_id: str, artifact: str | None = None):
        """Return a float score, or the `NE` sentinel. Never coerces `NE` to 0."""
        if value == NOT_ENOUGH_EVIDENCE:
            return NOT_ENOUGH_EVIDENCE
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise CanonError(
                f"{criterion_id}: score must be a number or {NOT_ENOUGH_EVIDENCE!r}, got {value!r}",
                artifact=artifact,
            )
        score = float(value)
        if not self.scale_min <= score <= self.scale_max:
            raise CanonError(
                f"{criterion_id}: score {score} outside {self.scale_min}-{self.scale_max}",
                artifact=artifact,
            )
        return score

    def weighted_points(self, score: float, criterion_id: str) -> float:
        """criterion_points = score / scale_max * weight."""
        weight = self.criterion(criterion_id).weight
        span = self.scale_max - self.scale_min
        if span <= 0:
            raise CanonError("rubric scale span must be positive", artifact=self.source)
        return (score - self.scale_min) / span * weight


def _require(metadata: dict, key: str, source: str):
    if key not in metadata:
        raise CanonError(f"rubric front matter missing {key!r}", artifact=source)
    return metadata[key]


def parse_rubric(path: Path) -> Rubric:
    metadata, body = read(path)
    source = str(path)
    rubric_id = str(_require(metadata, "rubric_id", source))
    version = str(_require(metadata, "version", source))
    scale_min = int(_require(metadata, "scale_min", source))
    scale_max = int(_require(metadata, "scale_max", source))

    criteria: list[Criterion] = []
    seen: set[str] = set()
    for cid, name, weight, question in _CRITERION_ROW.findall(body):
        if cid in {"id", "score"}:  # table header rows
            continue
        if cid in seen:
            raise CanonError(f"duplicate criterion id in rubric table: {cid}", artifact=source)
        seen.add(cid)
        criteria.append(Criterion(id=cid, name=name, weight=int(weight), question=question))
    if not criteria:
        raise CanonError("no criterion rows found in rubric table", artifact=source)

    anchors: dict[int, str] = {}
    for score, meaning in _ANCHOR_ROW.findall(body):
        anchors[int(score)] = meaning

    rubric = Rubric(
        rubric_id=rubric_id,
        version=version,
        scale_min=scale_min,
        scale_max=scale_max,
        criteria=tuple(criteria),
        anchors=anchors,
        source=source,
        display_decimals=int(metadata.get("display_decimals", 1)),
        rounding=str(metadata.get("rounding", "half-up")),
    )

    # The front matter states the intended total; the table defines it. Disagreement
    # means one of the two was edited alone, which is exactly the defect that the
    # single-source-of-truth rule exists to prevent.
    declared_total = metadata.get("total_weight")
    if declared_total is not None and int(declared_total) != rubric.total_weight:
        raise CanonError(
            f"rubric table weights total {rubric.total_weight} but front matter declares "
            f"total_weight: {declared_total}",
            artifact=source,
        )
    if rubric.total_weight != 100:
        raise CanonError(
            f"criterion weights must total 100, got {rubric.total_weight}", artifact=source
        )
    if rubric.scale_max <= rubric.scale_min:
        raise CanonError("scale_max must exceed scale_min", artifact=source)
    return rubric


@dataclass(frozen=True)
class HeadToHeadRubric:
    rubric_id: str
    version: str
    source_rubric: str
    close_call_band: float
    order_balancing: str
    values: dict[str, int]
    source: str
    tie_break_order: tuple[str, ...] = ()

    @property
    def metadata_order(self) -> tuple[str, ...]:
        return self.tie_break_order

    @property
    def reference(self) -> str:
        return f"{self.rubric_id}@{self.version}"

    @property
    def minimum_value(self) -> int:
        """Lowest comparative value, read from the rubric's own table."""
        if not self.values:
            raise CanonError("head-to-head rubric declares no comparison values",
                             artifact=self.source)
        return min(self.values.values())

    @property
    def maximum_value(self) -> int:
        if not self.values:
            raise CanonError("head-to-head rubric declares no comparison values",
                             artifact=self.source)
        return max(self.values.values())

    def require_reference(self, reference: str, *, artifact: str | None = None) -> None:
        if reference != self.reference:
            raise VersionError(
                f"matchup rubric mismatch: artifact declares {reference!r}, canonical is "
                f"{self.reference!r}",
                artifact=artifact,
            )


def parse_head_to_head(path: Path) -> HeadToHeadRubric:
    metadata, body = read(path)
    source = str(path)
    values: dict[str, int] = {}
    for row in re.findall(r"^\|\s*([^|]+?)\s*\|\s*(-?\d+)\s*\|\s*$", body, re.MULTILINE):
        values[row[0]] = int(row[1])
    return HeadToHeadRubric(
        rubric_id=str(_require(metadata, "rubric_id", source)),
        version=str(_require(metadata, "version", source)),
        source_rubric=str(_require(metadata, "source_rubric", source)),
        close_call_band=float(_require(metadata, "close_call_band", source)),
        order_balancing=str(metadata.get("order_balancing", "required")),
        values=values,
        source=source,
        tie_break_order=tuple(str(step) for step in metadata.get("tie_break_order") or ()),
    )


@dataclass(frozen=True)
class PolicyVersion:
    policy_id: str
    version: str
    metadata: dict
    source: str = ""

    @property
    def reference(self) -> str:
        return f"{self.policy_id}@{self.version}"

    def require_reference(self, reference: str, *, artifact: str | None = None) -> None:
        if reference != self.reference:
            raise VersionError(
                f"policy mismatch: artifact declares {reference!r}, canonical policy is "
                f"{self.reference!r}",
                artifact=artifact,
            )

    def number(self, key: str, default=None):
        """Read a declared numeric threshold from the policy front matter."""
        value = self.metadata.get(key, default)
        if value is None:
            raise CanonError(f"policy {self.policy_id!r} does not declare {key!r}",
                             artifact=self.source)
        return value


def parse_policy(path: Path, *, id_key: str = "policy_id") -> PolicyVersion:
    metadata, _ = read(path)
    source = str(path)
    return PolicyVersion(
        policy_id=str(_require(metadata, id_key, source)),
        version=str(_require(metadata, "version", source)),
        metadata=metadata,
        source=source,
    )


def repository_root(start: Path | None = None) -> Path:
    """Locate the framework root by its canonical rubric, not by `.git`.

    Keeping this independent of Git means the tooling works from a packaged
    checkout, a CI export, or a worktree.
    """
    current = (start or Path(__file__).resolve()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / SUBMISSION_RUBRIC).is_file():
            return candidate
    raise CanonError(f"framework root not found above {current} (no {SUBMISSION_RUBRIC})")


def _stamp(path: Path) -> tuple[int, int]:
    """File identity for cache keys.

    Caching on the path alone would serve a stale rubric to a long-running
    process after the file was corrected on disk. Keying on mtime and size means
    an edited rubric is picked up on the next call.
    """
    try:
        info = path.stat()
    except OSError as exc:
        raise CanonError(f"cannot read {path}: {exc}", artifact=str(path)) from exc
    return (info.st_mtime_ns, info.st_size)


@functools.lru_cache(maxsize=16)
def _load_rubric_cached(path: Path, stamp: tuple[int, int]) -> Rubric:
    return parse_rubric(path)


@functools.lru_cache(maxsize=16)
def _load_h2h_cached(path: Path, stamp: tuple[int, int]) -> HeadToHeadRubric:
    return parse_head_to_head(path)


@functools.lru_cache(maxsize=16)
def _load_policy_cached(path: Path, stamp: tuple[int, int], id_key: str) -> PolicyVersion:
    return parse_policy(path, id_key=id_key)


def load(root: Path | None = None) -> Rubric:
    path = (root or repository_root()) / SUBMISSION_RUBRIC
    return _load_rubric_cached(path, _stamp(path))


def load_head_to_head(root: Path | None = None) -> HeadToHeadRubric:
    path = (root or repository_root()) / HEAD_TO_HEAD_RUBRIC
    return _load_h2h_cached(path, _stamp(path))


def load_bracket_policy(root: Path | None = None) -> PolicyVersion:
    path = (root or repository_root()) / BRACKET_POLICY
    return _load_policy_cached(path, _stamp(path), "policy_id")


def load_consolidation_policy(root: Path | None = None) -> PolicyVersion:
    path = (root or repository_root()) / CONSOLIDATION_RUBRIC
    return _load_policy_cached(path, _stamp(path), "rubric_id")


def clear_cache() -> None:
    for fn in (_load_rubric_cached, _load_h2h_cached, _load_policy_cached):
        fn.cache_clear()
