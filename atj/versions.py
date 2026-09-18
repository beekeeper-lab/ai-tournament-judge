"""Version and provenance facts.

Three things must be pinned to make a judgment reproducible and disputable:
the rubric version, the persona version, and the framework commit. Each has
exactly one source, and a mismatch is fatal rather than advisory.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from . import canon, ids
from .errors import AtjError, ValidationError, VersionError
from .frontmatter import read

PERSONA_REGISTRY = "framework/personas.md"
AGENT_DIR = ".claude/agents"
SKILL_DIR = ".claude/skills"
DIGEST_LENGTH = 16
PENDING = "PENDING"

_PERSONA_ROW = re.compile(
    r"^\|\s*([a-z][a-z0-9-]*)\s*\|\s*(\d+\.\d+\.\d+)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|"
    r"\s*([0-9a-f]{16}|PENDING)\s*\|\s*$",
    re.MULTILINE,
)
# | judge-backend | 1.0.0 | 2026-09-18 | 1.1.0 | 7571907d5863c02d |
_SUPERSEDED_ROW = re.compile(
    r"^\|\s*([a-z][a-z0-9-]*)\s*\|\s*(\d+\.\d+\.\d+)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|"
    r"\s*(\d+\.\d+\.\d+)\s*\|\s*([0-9a-f]{16})\s*\|\s*$",
    re.MULTILINE,
)
# A component that must write its own artifact declares where. `-` means it
# writes nothing and must hold no write capability.
WRITES_NOTHING = "-"
# The registry holds two tables. The current one is authoritative for what a
# component is now; the history below it is authoritative for what it was. They
# have the same column count, so a reader that does not split them first reads a
# retired row as the current one -- which is how the first attempt at this table
# reported `judge-backend@1.0.0` as current immediately after retiring it.
SUPERSEDED_HEADING = "## Superseded versions"


@dataclass(frozen=True)
class Persona:
    agent_id: str
    version: str
    role: str
    writes: str
    content_digest: str

    @property
    def reference(self) -> str:
        return f"{self.agent_id}@{self.version}"

    @property
    def must_write(self) -> bool:
        """Whether this component's own skill requires it to produce a file."""
        return self.writes not in ("", WRITES_NOTHING)


@dataclass(frozen=True)
class SupersededPersona:
    """A retired persona version. No new artifact may pin it; old ones stay valid."""

    agent_id: str
    version: str
    retired_on: str
    superseded_by: str
    content_digest: str

    @property
    def reference(self) -> str:
        return f"{self.agent_id}@{self.version}"


def load_personas(root: Path | None = None) -> dict[str, Persona]:
    base = root or canon.repository_root()
    path = base / PERSONA_REGISTRY
    _, body = read(path)
    body = current_table(body)
    personas: dict[str, Persona] = {}
    for agent_id, version, role, writes, digest in _PERSONA_ROW.findall(body):
        personas[agent_id] = Persona(agent_id, version, role, writes, digest)
    if not personas:
        raise ValidationError("persona registry contains no rows", artifact=str(path))
    return personas


def current_table(body: str) -> str:
    """Just the current-version table: everything above the history heading."""
    return body.split(SUPERSEDED_HEADING, 1)[0]


def superseded_table(body: str) -> str:
    parts = body.split(SUPERSEDED_HEADING, 1)
    return parts[1] if len(parts) == 2 else ""


def load_superseded(root: Path | None = None) -> dict[tuple[str, str], SupersededPersona]:
    """Retired persona versions, keyed by ``(agent_id, version)``.

    Without this table a persona bump invalidates every artifact a completed event
    produced under the old version, and the only repair inside the event is to
    rewrite a frozen record. Recording the retirement keeps the old artifacts
    valid and still stops new work from pinning a version that no longer exists.
    """
    base = root or canon.repository_root()
    _, body = read(base / PERSONA_REGISTRY)
    retired: dict[tuple[str, str], SupersededPersona] = {}
    for agent_id, version, retired_on, replacement, digest in _SUPERSEDED_ROW.findall(
        superseded_table(body)
    ):
        retired[(agent_id, version)] = SupersededPersona(
            agent_id, version, retired_on, replacement, digest
        )
    return retired


def component_path(component_id: str, root: Path | None = None) -> Path | None:
    """Locate a registered component: an agent file or a skill definition."""
    base = root or canon.repository_root()
    agent = base / AGENT_DIR / f"{component_id}.md"
    if agent.is_file():
        return agent
    skill = base / SKILL_DIR / component_id / "SKILL.md"
    if skill.is_file():
        return skill
    return None


def agent_digest(component_id: str, root: Path | None = None) -> str:
    path = component_path(component_id, root)
    if path is None:
        raise ValidationError(f"component definition not found for {component_id!r}")
    return ids.file_digest(path, length=DIGEST_LENGTH)


def require_personas(root: Path | None = None) -> None:
    """Fatal form of :func:`check_personas`. Drift is never a warning."""
    problems = check_personas(root)
    if problems:
        raise VersionError("persona registry is out of date: " + "; ".join(problems),
                           artifact=PERSONA_REGISTRY)


def components_available(root: Path | None = None) -> bool:
    """Whether the project-local Claude components are present.

    An installed wheel ships the framework data but not `.claude/`, which is a
    working-copy concern. Reporting drift against files that were never installed
    would be a false failure.
    """
    base = root or canon.repository_root()
    return (base / AGENT_DIR).is_dir() or (base / SKILL_DIR).is_dir()


def check_personas(root: Path | None = None) -> list[str]:
    """Report drift between declared persona versions and component files on disk."""
    base = root or canon.repository_root()
    if not components_available(base):
        return []
    problems: list[str] = []
    personas = load_personas(base)
    on_disk = {p.stem for p in sorted((base / AGENT_DIR).glob("*.md"))}
    on_disk |= {p.parent.name for p in sorted((base / SKILL_DIR).glob("*/SKILL.md"))}
    for agent_id, persona in sorted(personas.items()):
        if agent_id not in on_disk:
            problems.append(
                f"{agent_id}: declared in the registry but no agent or skill definition exists"
            )
            continue
        actual = agent_digest(agent_id, base)
        if persona.content_digest == PENDING:
            problems.append(f"{agent_id}: digest is PENDING; run `atj personas --refresh`")
        elif persona.content_digest != actual:
            problems.append(
                f"{agent_id}: persona changed without a version bump "
                f"(registry {persona.content_digest}, file {actual}); "
                f"increment the version and refresh the digest"
            )
    for agent_id in sorted(on_disk - set(personas)):
        problems.append(f"{agent_id}: definition exists but is not in the component registry")
    return problems


def refresh_personas(root: Path | None = None) -> list[str]:
    """Rewrite the registry's digest column from the agent files. Versions untouched."""
    base = root or canon.repository_root()
    path = base / PERSONA_REGISTRY
    text = path.read_text(encoding="utf-8")
    # A retired row records the digest that version carried when it was retired.
    # Recomputing it from today's file would overwrite the one fact the history
    # exists to keep.
    head, marker, history = text.partition(SUPERSEDED_HEADING)
    changed: list[str] = []

    def replace(match: re.Match[str]) -> str:
        agent_id, version, role, writes, old = match.groups()
        try:
            new = agent_digest(agent_id, base)
        except ValidationError:
            return match.group(0)
        if new != old:
            changed.append(f"{agent_id}: {old} -> {new}")
        return f"| {agent_id} | {version} | {role} | {writes} | {new} |"

    path.write_text(_PERSONA_ROW.sub(replace, head) + marker + history, encoding="utf-8")
    return changed


def framework_commit(root: Path | None = None) -> str:
    """The commit official artifacts were produced at, or ``uncommitted``.

    A dirty working tree yields ``uncommitted`` on purpose: an artifact must not
    claim provenance from a commit that does not contain the code that made it.
    """
    base = root or canon.repository_root()
    try:
        head = subprocess.run(
            ["git", "-C", str(base), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=15, check=False,
        )
        if head.returncode != 0:
            return ids.UNCOMMITTED
        dirty = subprocess.run(
            ["git", "-C", str(base), "status", "--porcelain"],
            capture_output=True, text=True, timeout=15, check=False,
        )
        if dirty.returncode != 0 or dirty.stdout.strip():
            return ids.UNCOMMITTED
        return head.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ids.UNCOMMITTED


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# Artifact field -> the canonical loader that defines its version.
VERSIONED_CONTRACTS = {
    "rubric": "submission",
    "source_rubric": "submission",
    "consolidation_policy": "consolidation",
    "matchup_rubric": "head-to-head",
    "bracket_policy": "bracket",
}


def require_versions(
    metadata: dict,
    *,
    root: Path | None = None,
    artifact: str | None = None,
    expect_persona: str | None = None,
) -> None:
    """Fail on any version incompatibility. Never a warning.

    Every versioned contract an artifact pins is checked against its canonical
    definition: the submission rubric, the consolidation policy, the head-to-head
    rubric, the bracket policy, and the persona registry. Checking only the
    submission rubric would let three of the five skew silently.
    """
    base = root or canon.repository_root()
    submission = canon.load(base)

    declared = metadata.get("rubric")
    if declared is None:
        raise VersionError("artifact does not declare a rubric version", artifact=artifact)

    head_to_head = canon.load_head_to_head(base)

    def require_contract(contract, value: str) -> None:
        """Accept the current version, or one the archive records as superseded."""
        if value == contract.reference or canon.is_superseded(value, base):
            return
        contract.require_reference(value, artifact=artifact)

    # A matchup artifact pins the head-to-head rubric in `rubric`; everything
    # else pins the submission rubric there.
    if str(declared).startswith(f"{head_to_head.rubric_id}@"):
        require_contract(head_to_head, str(declared))
    else:
        require_contract(submission, str(declared))

    for field, kind in VERSIONED_CONTRACTS.items():
        if field == "rubric" or field not in metadata or metadata[field] is None:
            continue
        value = str(metadata[field])
        if kind == "submission":
            require_contract(submission, value)
        elif kind == "consolidation":
            require_contract(canon.load_consolidation_policy(base), value)
        elif kind == "head-to-head":
            require_contract(head_to_head, value)
        elif kind == "bracket":
            require_contract(canon.load_bracket_policy(base), value)

    band = metadata.get("close_call_band")
    if band is not None:
        # The rubric's band is the FLOOR. A wider band sends more matchups to a
        # human, which is the safe direction. A narrower one converts close calls
        # into automatic advancement, so it is refused.
        value = float(band)
        if value < float(head_to_head.close_call_band):
            raise VersionError(
                f"close_call_band {band} is below the rubric floor of "
                f"{head_to_head.close_call_band}. An event may widen the band, sending more "
                f"matchups to a human official, but never narrow it: that would turn "
                f"results requiring review into automatic advancements",
                artifact=artifact,
            )
        if value > 100:
            raise VersionError(
                f"close_call_band {band} exceeds the maximum possible margin of 100",
                artifact=artifact,
            )

    persona = metadata.get("persona") or expect_persona
    if persona is not None:
        name, version = ids.split_reference(str(persona))
        personas = load_personas(base)
        known = personas.get(name)
        if known is None:
            raise VersionError(f"unknown persona: {persona!r}", artifact=artifact)
        if known.version != version and (name, version) not in load_superseded(base):
            raise VersionError(
                f"persona mismatch: artifact declares {persona!r}, registry has "
                f"{known.reference!r} and no superseded row records {persona!r}",
                artifact=artifact,
            )


def superseded_pins(metadata: dict, root: Path | None = None) -> list[str]:
    """Which versioned pins in an artifact name a retired version.

    Accepting a superseded pin silently would make a frozen record look current.
    The validator reports these as advisories, so a reader of a completed event
    can see which contracts have moved on since it was judged.
    """
    base = root or canon.repository_root()
    retired: list[str] = []
    for field in VERSIONED_CONTRACTS:
        value = metadata.get(field)
        if value and canon.is_superseded(str(value), base):
            retired.append(f"{field}: {value}")
    persona = metadata.get("persona")
    if persona:
        try:
            name, version = ids.split_reference(str(persona))
        except AtjError:
            return retired
        if (name, version) in load_superseded(base):
            retired.append(f"persona: {persona}")
    return retired
