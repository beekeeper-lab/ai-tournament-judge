"""Deterministic Markdown rendering.

Humans review Markdown; official numbers are generated into it. Generated blocks
are delimited by ``<!-- atj:<name>:begin -->`` / ``<!-- atj:<name>:end -->`` so a
re-render replaces only the generated region and leaves the reviewer's prose
untouched.

Rendering is a pure function of the structured result. It never rounds
differently from :mod:`atj.scoring`, because it formats values that module has
already rounded.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from . import canon, frontmatter
from .canon import NOT_ENOUGH_EVIDENCE
from .errors import ValidationError

BEGIN = "<!-- atj:{name}:begin -->"
END = "<!-- atj:{name}:end -->"


def _block(name: str) -> re.Pattern[str]:
    return re.compile(
        re.escape(BEGIN.format(name=name)) + r".*?" + re.escape(END.format(name=name)),
        re.DOTALL,
    )


def replace_block(text: str, name: str, content: str) -> str:
    """Replace one generated region. Raises if the markers are absent."""
    pattern = _block(name)
    if not pattern.search(text):
        raise ValidationError(
            f"generated block {name!r} not found; the artifact is missing its "
            f"{BEGIN.format(name=name)} / {END.format(name=name)} markers"
        )
    replacement = f"{BEGIN.format(name=name)}\n{content.rstrip()}\n{END.format(name=name)}"
    return pattern.sub(lambda _: replacement, text, count=1)


def has_block(text: str, name: str) -> bool:
    return bool(_block(name).search(text))


def _number(value: Any, places: int = 1) -> str:
    if value is None:
        return "—"
    if value == NOT_ENOUGH_EVIDENCE:
        return NOT_ENOUGH_EVIDENCE
    return f"{float(value):.{places}f}"


def _total_weight(root: Path | None = None) -> int:
    return canon.load(root).total_weight


def individual_scores_table(result: dict[str, Any], root: Path | None = None) -> str:
    rows = ["| Criterion | Raw score or NE | Weight | Weighted points | Confidence |",
            "|---|---:|---:|---:|---|"]
    for criterion, entry in result["criteria"].items():
        rows.append(
            f"| {criterion} | {_number(entry['raw'], 1)} | {entry['weight']} | "
            f"{_number(entry['weighted_points'], 2)} | {entry.get('confidence') or '—'} |"
        )
    total = ("not finalizable (unresolved NE)" if result["total"] is None
             else _number(result["display_total"]))
    rows.append(f"| **Total** |  | **{_total_weight(root)}** | **{total}** |  |")
    if result["unresolved_ne"]:
        rows.append("")
        rows.append(
            "`NE` on " + ", ".join(result["unresolved_ne"])
            + " — this judge produced no finalizable total. `NE` is not a zero."
        )
    return "\n".join(rows)


def consolidated_table(result: dict[str, Any], root: Path | None = None) -> str:
    rows = ["| Criterion | Judge scores | Mean | Weight | Points | Agreement |",
            "|---|---|---:|---:|---:|---|"]
    for criterion, entry in result["criteria"].items():
        scores = ", ".join(
            f"{judge}={_number(value, 1) if value != NOT_ENOUGH_EVIDENCE else NOT_ENOUGH_EVIDENCE}"
            for judge, value in sorted(entry["source_scores"].items())
        )
        flag = " ⚑outlier" if entry["possible_outliers"] else ""
        rows.append(
            f"| {criterion} | {scores} | {_number(entry['mean'], 2)} | {entry['weight']} | "
            f"{_number(entry['weighted_points'], 2)} | {entry['agreement']}{flag} |"
        )
    weight = _total_weight(root)
    if result["finalized"]:
        rows.append(
            f"| **Overall** |  |  | **{weight}** | **{_number(result['display_total'])}** |  |"
        )
    else:
        rows.append(f"| **Overall** |  |  | **{weight}** | **not finalized** |  |")
    if result["blocked_reasons"]:
        # Only when there is something to say. A trailing empty row made the
        # generated block end in a blank line that `replace_block` then strips,
        # so a correct report was never byte-identical to its own regeneration.
        rows.append("")
        rows.append("**Finalization blocked:**")
        for reason in result["blocked_reasons"]:
            rows.append(f"- {reason}")
        rows.append("")
        rows.append(
            f"Provisional sum of scored criteria: "
            f"{_number(result['provisional_total'], 2)} / {weight}. This is not an official "
            "total and must not be published or used for bye seeding."
        )
    return "\n".join(rows)


def adjudication_notice(result: dict[str, Any]) -> str:
    """The consolidation's outstanding adjudications, for the console.

    `consolidated_table` prints `blocked_reasons` but not `adjudication_required`,
    and the two are not the same list: a criterion can require adjudication
    without blocking, and an operator reading only the table sees no mention of
    an adjudication that the written JSON demands. That is how live-trial-2026
    got "no adjudication required" into its ledger while
    `summaries/team-podcast.json` recorded the opposite (D7).

    Kept out of `consolidated_table` on purpose: that function's output is
    committed into every consolidated team report, and this is an operator
    prompt, not part of the official record.
    """
    required = result.get("adjudication_required") or []
    if not required:
        return ""
    rows = ["**Adjudication required:**"]
    for entry in required:
        rows.append(f"- {entry['criterion']}: {entry['trigger']}")
    rows.append("")
    rows.append(
        "Recorded as `adjudication_required` in the structured result. Do not "
        "report this panel as needing no adjudication."
    )
    return "\n".join(rows)


def matchup_table(result: dict[str, Any], root: Path | None = None) -> str:
    rows = ["| Criterion | Weight | A-first value | B-first normalized | Combined margin | Order |",
            "|---|---:|---:|---:|---:|---|"]
    for criterion, entry in result["criteria"].items():
        flag = "conflict" if entry["order_disagreement"] else "consistent"
        rows.append(
            f"| {criterion} | {entry['weight']} | {entry['a_first_value']:+d} | "
            f"{entry['b_first_normalized_value']:+d} | {entry['combined_margin']:+.2f} | {flag} |"
        )
    rows.append("")
    rows.extend([
        f"- A-first pass margin: **{result['passes']['a_first']['margin']:+.2f}** "
        f"(picked {result['passes']['a_first']['picks'] or 'no winner'})",
        f"- B-first pass margin, normalized: **{result['passes']['b_first']['margin']:+.2f}** "
        f"(picked {result['passes']['b_first']['picks'] or 'no winner'})",
        f"- Combined margin: **{result['combined_margin']:+.2f}** on a "
        f"−{_total_weight(root)}…+{_total_weight(root)} scale "
        f"(positive favours {result['team_a']})",
        f"- Close-call band: ±{result['close_call_band']:g}",
        f"- Outcome: **{result['outcome']}**"
        + (f", winner **{result['winner']}**" if result["winner"] else ""),
    ])
    if result["adjudication_reasons"]:
        rows.append("")
        rows.append("**Why this needs adjudication:**")
        for reason in result["adjudication_reasons"]:
            rows.append(f"- {reason}")
    return "\n".join(rows)


def bracket_tables(result: dict[str, Any]) -> str:
    rows = ["| Slot | Entrant A | Entrant B | Entry | Notes |", "|---:|---|---|---|---|"]
    for match in result["rounds"][0]["matches"]:
        left, right = match["entrants"]
        if match["bye"]:
            rows.append(f"| {match['slot']} | {left} | — | bye | advances to round 2 |")
        else:
            rows.append(f"| {match['slot']} | {left} | {right} | {result['rounds'][0]['round_id']} | |")
    rows.append("")
    rows.append("| Constraint | Kind | Status | Detail |")
    rows.append("|---|---|---|---|")
    for entry in result["constraint_audit"]:
        detail = entry["detail"].replace("|", "\\|")
        rows.append(f"| {entry['constraint']} | {entry['kind']} | {entry['status']} | {detail} |")
        for exception in entry.get("exceptions") or []:
            rows.append(f"|  |  | exception | {str(exception).replace('|', chr(92) + '|')} |")
    rows.append("")
    rows.append(
        f"Reproduce with: `python3 -m atj bracket build --event-dir <event-dir> "
        f"--seed {result['seed']}` (roster version {result['roster_version']}, "
        f"input digest `{result['input_digest']}`)."
    )
    return "\n".join(rows)


def render_into(
    path: Path, blocks: dict[str, str], *, metadata_updates: dict[str, Any] | None = None
) -> None:
    """Write generated blocks and metadata into an existing artifact."""
    metadata, body = frontmatter.read(path)
    for name, content in blocks.items():
        body = replace_block(body, name, content)
    if metadata_updates:
        metadata.update(metadata_updates)
    path.write_text(frontmatter.dump(metadata, body), encoding="utf-8")


def from_template(
    template_path: Path, target: Path, *, metadata: dict[str, Any], blocks: dict[str, str] | None = None
) -> None:
    """Instantiate a template with real metadata, then fill generated blocks."""
    _, body = frontmatter.read(template_path)
    for name, content in (blocks or {}).items():
        if has_block(body, name):
            body = replace_block(body, name, content)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(frontmatter.dump(metadata, body), encoding="utf-8")
