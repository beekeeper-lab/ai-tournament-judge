"""Error taxonomy.

Every failure surfaced to an operator carries a stable code so hooks, CI, and
audit reports can refer to it without matching on prose.
"""

from __future__ import annotations


class AtjError(Exception):
    """Base class. `code` is stable; `message` is for humans."""

    code = "atj-error"

    def __init__(self, message: str, *, artifact: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.artifact = artifact

    def render(self) -> str:
        where = f" [{self.artifact}]" if self.artifact else ""
        return f"{self.code}: {self.message}{where}"


class CanonError(AtjError):
    """The canonical rubric could not be read or is self-inconsistent."""

    code = "canon"


class VersionError(AtjError):
    """A version incompatibility. Always fatal; never downgraded to a warning."""

    code = "version"


class SchemaError(AtjError):
    """Structured data failed schema validation."""

    code = "schema"


class ValidationError(AtjError):
    """An artifact failed a content rule."""

    code = "validation"


class StateError(AtjError):
    """An illegal event-state transition or an out-of-order operation."""

    code = "state"


class ConstraintError(AtjError):
    """A hard bracket or policy constraint cannot be satisfied."""

    code = "constraint"


class SafetyError(AtjError):
    """A safety control could not be guaranteed. Never caught to continue."""

    code = "safety"
