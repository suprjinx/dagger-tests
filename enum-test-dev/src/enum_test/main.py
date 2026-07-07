import enum

import dagger
from dagger import dag, enum_type, function, object_type


@enum_type
class Severity(enum.Enum):
    """How loud to be."""

    LOW = "LOW"
    """Whisper."""

    MEDIUM = "MEDIUM"
    """Talk."""

    HIGH = "HIGH"
    """Shout."""


@object_type
class EnumTest:
    @function
    async def echo_severity(self, severity: Severity) -> str:
        """Echo back the chosen severity (takes an Enum argument)."""
        return await (
            dag.container()
            .from_("alpine:latest")
            .with_exec(["echo", f"severity={severity.value}"])
            .stdout()
        )
