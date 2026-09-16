"""Static ceremony output.

Markdown stays authoritative. This renders a single self-contained HTML file for
display during an event, and a printable team dossier, from **approved public
artifacts only**.

Two rules shape the implementation:

* It reads `events/<event>/public/` and the bracket's structural facts. It never
  opens `judgments/`, `summaries/`, `matchups/`, `adjudications/` or `audits/`.
  The private record is not an input, so it cannot leak through a template bug.
* Every artifact is re-checked through :mod:`atj.publication` at render time. An
  unapproved or non-conforming artifact stops the render rather than being
  quietly skipped, because a ceremony display that silently omits a match is
  worse than one that refuses to build.

No web application, no server, no JavaScript framework: one file that opens from
a filesystem and prints.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

from . import frontmatter, publication
from .errors import ValidationError

PUBLIC_DIR = "public"
SUMMARY_FILE = "event-summary.md"

# Deliberately never read. Named so the exclusion is explicit and testable.
PRIVATE_DIRS = ("judgments", "summaries", "matchups", "adjudications", "audits",
                "evidence", "submissions", "runs")

_HEADING = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def _sections(body: str) -> dict[str, str]:
    """Split a Markdown body into its `##` sections, preserving order."""
    parts: dict[str, str] = {}
    matches = list(_HEADING.finditer(body))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        parts[match.group(1).strip()] = body[match.end():end].strip()
    return parts


def _inline(text: str) -> str:
    """Minimal Markdown to HTML: escape first, then allow bold and code."""
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"`(.+?)`", r"<code>\1</code>", escaped)
    return escaped


def _blocks(text: str) -> str:
    out: list[str] = []
    bullets: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            bullets.append(f"<li>{_inline(stripped[2:])}</li>")
            continue
        if bullets:
            out.append("<ul>" + "".join(bullets) + "</ul>")
            bullets = []
        if stripped.startswith("|"):
            continue  # tables are re-rendered from structured data, not scraped
        if stripped:
            out.append(f"<p>{_inline(stripped)}</p>")
    if bullets:
        out.append("<ul>" + "".join(bullets) + "</ul>")
    return "\n".join(out)


def load_public_artifacts(event_dir: Path) -> dict[str, Any]:
    """Read and re-verify every approved public artifact. Raises on any problem."""
    directory = event_dir / PUBLIC_DIR
    if not directory.is_dir():
        raise ValidationError(f"no public directory: {directory}")

    summary: dict[str, Any] | None = None
    matches: list[dict[str, Any]] = []
    for path in sorted(directory.glob("*.md")):
        metadata, body = frontmatter.read(path)
        findings = publication.check_public(
            metadata, body, artifact=str(path),
            public_scores=bool(metadata.get("scores_published")),
        )
        blocking = [finding for finding in findings if finding.severity == "blocking"]
        if blocking:
            raise ValidationError(
                f"refusing to render: {path.name} is not publishable:\n  "
                + "\n  ".join(finding.render() for finding in blocking)
            )
        entry = {"path": path, "metadata": metadata, "sections": _sections(body)}
        if path.name == SUMMARY_FILE:
            summary = entry
        else:
            matches.append(entry)
    if summary is None:
        raise ValidationError(
            f"no {SUMMARY_FILE} in {directory}; the ceremony view needs an approved "
            f"event summary"
        )
    return {"summary": summary, "matches": matches}


def bracket_view(event_dir: Path) -> dict[str, Any]:
    """Structural bracket facts only: slots, entrants, byes, round names.

    Scores, constraint reasoning and the seed stay private. The public view shows
    who played whom, not how the draw was argued.
    """
    path = event_dir / "bracket.json"
    if not path.is_file():
        return {"rounds": [], "team_count": 0, "note": "no bracket recorded"}
    drawn = json.loads(path.read_text(encoding="utf-8"))
    return {
        "team_count": drawn.get("team_count", 0),
        "bracket_size": drawn.get("bracket_size", 0),
        "bye_count": drawn.get("bye_count", 0),
        "rounds": [
            {
                "round_id": entry.get("round_id", ""),
                "matches": [
                    {
                        "slot": match.get("slot"),
                        "entrants": match.get("entrants", []),
                        "bye": bool(match.get("bye")),
                        "winner": match.get("winner"),
                    }
                    for match in entry.get("matches", [])
                ],
            }
            for entry in drawn.get("rounds", [])
        ],
    }


STYLE = """
:root {
  --ink: #16191d; --muted: #5b6671; --line: #d8dee5; --bg: #ffffff;
  --accent: #1f4e79; --won: #eef5ec; --pending: #f6f7f9;
}
@media (prefers-color-scheme: dark) {
  :root { --ink: #e8ebee; --muted: #9aa5b1; --line: #333a42; --bg: #14171a;
          --accent: #7fb2e5; --won: #1e2a20; --pending: #1b1f23; }
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink);
       font: 16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
main { max-width: 62rem; margin: 0 auto; padding: 2rem 1rem 4rem; }
h1 { font-size: 1.9rem; margin: 0 0 .25rem; }
h2 { font-size: 1.2rem; margin: 2.5rem 0 .75rem; padding-bottom: .3rem;
     border-bottom: 2px solid var(--line); }
h3 { font-size: 1rem; margin: 1.5rem 0 .4rem; }
.sub { color: var(--muted); margin: 0 0 1.5rem; }
.champion { border: 2px solid var(--accent); border-radius: .5rem;
            padding: 1rem 1.25rem; margin: 1rem 0; }
.champion strong { font-size: 1.35rem; color: var(--accent); }
.rounds { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr)); }
.round { border: 1px solid var(--line); border-radius: .4rem; padding: .75rem; }
.round h3 { margin-top: 0; text-transform: capitalize; }
.match { background: var(--pending); border-radius: .3rem; padding: .4rem .6rem;
         margin-bottom: .4rem; font-size: .9rem; }
.match.won { background: var(--won); }
.match .slot { color: var(--muted); font-size: .8rem; }
.entrant.winner { font-weight: 600; }
.bye { color: var(--muted); font-style: italic; }
.card { border: 1px solid var(--line); border-radius: .4rem; padding: 1rem 1.25rem;
        margin-bottom: 1rem; }
.card h3 { margin-top: 0; }
.disclosure { background: var(--pending); border-radius: .4rem; padding: 1rem 1.25rem; }
footer { margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--line);
         color: var(--muted); font-size: .85rem; }
code { background: var(--pending); padding: .1rem .3rem; border-radius: .2rem;
       font-size: .9em; }
@media print {
  body { background: #fff; color: #000; }
  .rounds { grid-template-columns: repeat(2, 1fr); }
  h2 { page-break-after: avoid; }
  .card, .round { page-break-inside: avoid; }
}
"""


def render_ceremony(event_dir: Path) -> str:
    artifacts = load_public_artifacts(event_dir)
    summary = artifacts["summary"]
    sections = summary["sections"]
    event_id = html.escape(str(summary["metadata"].get("event_id", "event")))
    bracket = bracket_view(event_dir)

    round_blocks = []
    for entry in bracket["rounds"]:
        matches = []
        for match in entry["matches"]:
            if match["bye"]:
                entrant = html.escape(str(match["entrants"][0] or "—"))
                matches.append(
                    f'<div class="match"><span class="slot">{match["slot"]}</span> '
                    f'{entrant} <span class="bye">— bye</span></div>'
                )
                continue
            names = []
            for entrant in match["entrants"]:
                if not entrant:
                    names.append('<span class="entrant bye">to be decided</span>')
                    continue
                classes = "entrant winner" if entrant == match["winner"] else "entrant"
                names.append(f'<span class="{classes}">{html.escape(str(entrant))}</span>')
            won = " won" if match["winner"] else ""
            matches.append(
                f'<div class="match{won}"><span class="slot">{match["slot"]}</span> '
                + " vs ".join(names) + "</div>"
            )
        round_blocks.append(
            f'<div class="round"><h3>{html.escape(entry["round_id"])}</h3>'
            + "".join(matches) + "</div>"
        )

    match_cards = []
    for entry in artifacts["matches"]:
        title = entry["path"].stem.replace("-", " ")
        winner = entry["sections"].get("Winner", "")
        why = entry["sections"].get("Why", "")
        both = entry["sections"].get("Both teams did well", "")
        match_cards.append(
            f'<div class="card"><h3>{html.escape(title.title())}</h3>'
            f"{_blocks(winner)}{_blocks(why)}"
            f"<h4>Both teams did well</h4>{_blocks(both)}</div>"
        )

    current_round = next(
        (entry["round_id"] for entry in reversed(bracket["rounds"])
         if any(match["winner"] for match in entry["matches"])),
        "not started",
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{event_id} — ceremony</title>
<style>{STYLE}</style>
</head>
<body>
<main>
<h1>{event_id}</h1>
<p class="sub">Generated from approved public artifacts only. No private judge
report, score, evidence package or deliberation is an input to this page.</p>

<h2>Event overview</h2>
{_blocks(sections.get("Event overview", ""))}

<h2>Champion and finalists</h2>
<div class="champion">{_blocks(sections.get("Champion and finalists", ""))}</div>

<h2>Tournament bracket</h2>
<p class="sub">{bracket['team_count']} teams, {bracket['bracket_size']} slots,
{bracket['bye_count']} byes. Current round: <strong>{html.escape(current_round)}</strong>.</p>
<div class="rounds">{"".join(round_blocks)}</div>

<h2>Completed matchups</h2>
{"".join(match_cards) or "<p>No matchups have been published yet.</p>"}

<h2>Common strengths across the field</h2>
{_blocks(sections.get("Common strengths across the field", ""))}

<h2>Common learning opportunities</h2>
{_blocks(sections.get("Common learning opportunities", ""))}

<h2>How entries were judged</h2>
<div class="disclosure">{_blocks(sections.get("Judging-method disclosure", ""))}</div>

<footer>
Every statement above comes from an artifact a human official approved for
publication. Markdown in <code>{PUBLIC_DIR}/</code> remains the authoritative
record; this page is a rendering of it.
</footer>
</main>
</body>
</html>
"""


def render_dossier(dossier_path: Path) -> str:
    """A printable rendering of one approved team-facing dossier."""
    metadata, body = frontmatter.read(dossier_path)
    findings = publication.check_team_facing(
        metadata, body, artifact=str(dossier_path),
        own_team=str(metadata.get("team_id") or ""),
    )
    blocking = [finding for finding in findings if finding.severity == "blocking"]
    if blocking:
        raise ValidationError(
            f"refusing to render {dossier_path.name}:\n  "
            + "\n  ".join(finding.render() for finding in blocking)
        )
    if metadata.get("approval_state") != "approved":
        raise ValidationError(
            f"{dossier_path.name} is {metadata.get('approval_state')!r}; a dossier is "
            f"rendered for a team only after it is approved"
        )

    team = html.escape(str(metadata.get("team_id", "team")))
    event = html.escape(str(metadata.get("event_id", "event")))
    sections = _sections(body)
    blocks = "".join(
        f'<div class="card"><h3>{html.escape(title)}</h3>{_blocks(text)}</div>'
        for title, text in sections.items()
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{team} — dossier</title>
<style>{STYLE}</style>
</head>
<body>
<main>
<h1>{team}</h1>
<p class="sub">{event} — feedback for your team. Print or save this page.</p>
{blocks}
<footer>
This dossier is for your team only. It is generated from the approved
team-facing Markdown record and contains no other team's private information.
</footer>
</main>
</body>
</html>
"""
