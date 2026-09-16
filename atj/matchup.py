"""Deterministic head-to-head calculation.

Two independent comparative passes are run by an LLM judge: one presenting Team A
first, one presenting Team B first. Those passes are not deterministic. Everything
this module does with their output is.

Orientation convention
----------------------
A pass reports values from the point of view of the team it saw *first*: a
positive value favours the first-presented team. The B-first pass is therefore
negated to bring it into the canonical A/B orientation before anything is
compared or combined. Getting this backwards would silently invert half the
tournament, so it is asserted in both directions by the test suite.

Values and weights come from ``framework/rubrics/head-to-head.md`` and
``framework/rubrics/submission-evaluation.md``.
"""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from typing import Any

from . import canon
from .errors import ValidationError

A_FIRST = "a_first"
B_FIRST = "b_first"
CONFIRMED = "confirmed"
ADJUDICATION_REQUIRED = "adjudication-required"

# Comparative value bounds are read from the head-to-head rubric's own table;
# see HeadToHeadRubric.minimum_value / .maximum_value.


def _round(value: float | Decimal, places: int = 4) -> float:
    quant = Decimal(1).scaleb(-places)
    return float(Decimal(str(value)).quantize(quant, rounding=ROUND_HALF_UP))


def normalize_pass(
    comparisons: dict[str, Any], *, presented_first: str, team_a: str, team_b: str,
    minimum: int, maximum: int, artifact: str | None = None,
) -> dict[str, int]:
    """Return comparisons in canonical A-positive orientation.

    The B-first pass is negated. Nothing else about it is altered.
    """
    if presented_first not in (team_a, team_b):
        raise ValidationError(
            f"presented_first {presented_first!r} is neither team in this matchup",
            artifact=artifact,
        )
    sign = 1 if presented_first == team_a else -1
    normalized: dict[str, int] = {}
    for criterion, value in comparisons.items():
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValidationError(
                f"{criterion}: comparison value must be an integer {minimum}..{maximum}, "
                f"got {value!r}",
                artifact=artifact,
            )
        if not minimum <= value <= maximum:
            raise ValidationError(
                f"{criterion}: comparison value {value} outside {minimum}..{maximum}",
                artifact=artifact,
            )
        normalized[criterion] = sign * value
    return normalized


def criterion_margin(
    value: int, criterion_id: str, rubric: canon.Rubric, maximum: int
) -> float:
    """criterion_margin = comparison_value / max_value * criterion_weight."""
    weight = rubric.criterion(criterion_id).weight
    return value / maximum * weight


def _pass_result(
    comparisons: dict[str, int], rubric: canon.Rubric, maximum: int
) -> tuple[dict[str, float], float]:
    supplied = set(comparisons)
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
            f"matchup comparisons do not match the canonical rubric ({'; '.join(detail)})"
        )
    margins = {
        c: criterion_margin(comparisons[c], c, rubric, maximum) for c in rubric.criterion_ids
    }
    return margins, sum(margins.values())


def _pick(margin: float, team_a: str, team_b: str) -> str | None:
    if margin > 0:
        return team_a
    if margin < 0:
        return team_b
    return None


def calculate(
    *,
    team_a: str,
    team_b: str,
    a_first: dict[str, Any],
    b_first: dict[str, Any],
    close_call_band: float | None = None,
    rubric: canon.Rubric | None = None,
    head_to_head: canon.HeadToHeadRubric | None = None,
    root: Path | None = None,
) -> dict[str, Any]:
    """Resolve one matchup.

    ``a_first`` and ``b_first`` each carry ``presented_first`` and ``comparisons``.

    A winner is confirmed only when both passes pick the same team *and* the
    combined absolute margin exceeds the close-call band. Otherwise the outcome
    is ``adjudication-required`` and ``winner`` is ``None`` — a caller cannot
    advance a team it was never given.
    """
    rubric = rubric or canon.load(root)
    head_to_head = head_to_head or canon.load_head_to_head(root)
    band = float(close_call_band if close_call_band is not None else head_to_head.close_call_band)
    if band < 0:
        raise ValidationError(f"close_call_band must be non-negative, got {band}")
    if team_a == team_b:
        raise ValidationError(f"a matchup needs two distinct teams, got {team_a!r} twice")
    minimum_value = head_to_head.minimum_value
    maximum_value = head_to_head.maximum_value

    passes: dict[str, Any] = {}
    normalized: dict[str, dict[str, int]] = {}
    for label, payload in ((A_FIRST, a_first), (B_FIRST, b_first)):
        presented = str(payload.get("presented_first", team_a if label == A_FIRST else team_b))
        raw = dict(payload.get("comparisons") or {})
        values = normalize_pass(
            raw, presented_first=presented, team_a=team_a, team_b=team_b,
            minimum=minimum_value, maximum=maximum_value, artifact=label,
        )
        margins, total = _pass_result(values, rubric, maximum_value)
        normalized[label] = values
        passes[label] = {
            "presented_first": presented,
            "raw_comparisons": raw,
            "normalized_comparisons": values,
            "criterion_margins": {c: _round(m) for c, m in margins.items()},
            "margin": _round(total),
            "picks": _pick(total, team_a, team_b),
        }

    if passes[A_FIRST]["presented_first"] == passes[B_FIRST]["presented_first"]:
        raise ValidationError(
            "order balancing failed: both passes presented the same team first; "
            "the reversed pass was not run"
        )

    combined = (passes[A_FIRST]["margin"] + passes[B_FIRST]["margin"]) / 2
    combined = _round(combined)

    criterion_detail: dict[str, Any] = {}
    disagreeing_criteria: list[str] = []
    for criterion in rubric.criterion_ids:
        first = normalized[A_FIRST][criterion]
        second = normalized[B_FIRST][criterion]
        disagrees = (first > 0 > second) or (first < 0 < second)
        if disagrees:
            disagreeing_criteria.append(criterion)
        criterion_detail[criterion] = {
            "weight": rubric.criterion(criterion).weight,
            "a_first_value": first,
            "b_first_normalized_value": second,
            "combined_margin": _round(
                (criterion_margin(first, criterion, rubric, maximum_value)
                 + criterion_margin(second, criterion, rubric, maximum_value)) / 2
            ),
            "order_disagreement": disagrees,
        }

    pick_a = passes[A_FIRST]["picks"]
    pick_b = passes[B_FIRST]["picks"]
    order_disagreement = pick_a != pick_b

    reasons: list[str] = []
    if order_disagreement:
        reasons.append(
            f"presentation-order disagreement: A-first picked {pick_a or 'no winner'}, "
            f"B-first picked {pick_b or 'no winner'}"
        )
    if pick_a is None and pick_b is None:
        reasons.append("both passes found the teams substantially equal")
    if abs(combined) <= band:
        reasons.append(
            f"combined margin {combined} is inside the close-call band of {band}"
        )
    if disagreeing_criteria and not order_disagreement:
        reasons.append(
            "criterion-level order disagreement on: " + ", ".join(disagreeing_criteria)
        )

    confirmed = not order_disagreement and pick_a is not None and abs(combined) > band
    # Criterion-level order disagreement is reported but, on its own, does not
    # block a decisive overall result. head-to-head.md requires human review for
    # conflicting *winners*, contradictory evidence, and close calls.
    if confirmed:
        outcome, winner = CONFIRMED, pick_a
    else:
        outcome, winner = ADJUDICATION_REQUIRED, None

    return {
        "rubric": head_to_head.reference,
        "source_rubric": rubric.reference,
        "team_a": team_a,
        "team_b": team_b,
        "close_call_band": band,
        "passes": passes,
        "criteria": criterion_detail,
        "combined_margin": combined,
        "order_disagreement": order_disagreement,
        "criterion_order_disagreements": disagreeing_criteria,
        "outcome": outcome,
        "winner": winner,
        "adjudication_reasons": reasons if outcome == ADJUDICATION_REQUIRED else [],
    }


TIE_BREAK_ORDER = ("functional", "reliability", "product")


def tie_break(result: dict[str, Any], *, rubric: canon.Rubric | None = None,
              root: Path | None = None) -> dict[str, Any]:
    """Apply the rubric's declared tie-break order.

    Steps 1-3 are mechanical. Step 4 (fewest confirmed critical security or data
    risks) needs evidence this module does not hold, and step 5 is a human
    decision. Both are returned as a referral, never guessed.
    """
    rubric = rubric or canon.load(root)
    for criterion in TIE_BREAK_ORDER:
        if criterion not in result["criteria"]:
            continue
        margin = result["criteria"][criterion]["combined_margin"]
        if margin > 0:
            return {"resolved": True, "winner": result["team_a"], "step": criterion}
        if margin < 0:
            return {"resolved": True, "winner": result["team_b"], "step": criterion}
    return {
        "resolved": False,
        "winner": None,
        "step": "security-risk-count-or-human-decision",
        "note": "mechanical tie-break exhausted; refer to a human official",
    }
