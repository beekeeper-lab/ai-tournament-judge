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
from .errors import ValidationError, VersionError
from .frontmatter import read

PERSONA_REGISTRY = "framework/personas.md"
AGENT_DIR = ".claude/agents"
SKILL_DIR = ".claude/skills"
DIGEST_LENGTH = 16
PENDING = "PENDING"

_PERSONA_ROW = re.compile(
    r"^\|\s*([a-z][a-z0-9-]*)\s*\|\s*(\d+\.\d+\.\d+)\s*\|\s*([^|]*?)\s*\|\s*([0-9a-f]{16}|PENDING)\s*\|\s*$",
    re.MULTILINE,
)


@dataclass(frozen=True)
class Persona:
    agent_id: str
    version: str
    role: str
    content_digest: str

    @property
    def reference(self) -> str:
        return f"{self.agent_id}@{self.version}"


def load_personas(root: Path | None = None) -> dict[str, Persona]:
    base = root or canon.repository_root()
    path = base / PERSONA_REGISTRY
    _, body = read(path)
    personas: dict[str, Persona] = {}
    for agent_id, version, role, digest in _PERSONA_ROW.findall(body):
        personas[agent_id] = Persona(agent_id, version, role, digest)
    if not personas:
        raise ValidationError("persona registry contains no rows", artifact=str(path))
    return personas


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
    changed: list[str] = []

    def replace(match: re.Match[str]) -> str:
        agent_id, version, role, old = match.groups()
        try:
            new = agent_digest(agent_id, base)
        except ValidationError:
            return match.group(0)
        if new != old:
            changed.append(f"{agent_id}: {old} -> {new}")
        return f"| {agent_id} | {version} | {role} | {new} |"

    path.write_text(_PERSONA_ROW.sub(replace, text), encoding="utf-8")
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
    # A matchup artifact pins the head-to-head rubric in `rubric`; everything
    # else pins the submission rubric there.
    if str(declared).startswith(f"{head_to_head.rubric_id}@"):
        head_to_head.require_reference(str(declared), artifact=artifact)
    else:
        submission.require_reference(str(declared), artifact=artifact)

    for field, kind in VERSIONED_CONTRACTS.items():
        if field == "rubric" or field not in metadata or metadata[field] is None:
            continue
        value = str(metadata[field])
        if kind == "submission":
            submission.require_reference(value, artifact=artifact)
        elif kind == "consolidation":
            canon.load_consolidation_policy(base).require_reference(value, artifact=artifact)
        elif kind == "head-to-head":
            head_to_head.require_reference(value, artifact=artifact)
        elif kind == "bracket":
            canon.load_bracket_policy(base).require_reference(value, artifact=artifact)

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
        if known.version != version:
            raise VersionError(
                f"persona mismatch: artifact declares {persona!r}, registry has "
                f"{known.reference!r}",
                artifact=artifact,
            )
