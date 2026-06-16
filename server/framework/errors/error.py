from typing import Dict, Protocol


class Error:
    """Accepts any Enum instance that implements a .message property."""
    _ERROR_TAG: None

    def __init__(self, kind: ErrorKindInterface, details: Dict | None = None) -> None:
        self.kind = kind
        self.context = kind.value
        self.details = details or {}


    def __repr__(self) -> str:
        context_parts = []

        context_parts.append(f"type={self.kind.__class__.__name__}.{self.kind.name}")
        context_parts.append(f"context=\"{self.context}\"")

        if self.details:
            context_parts.append(f"details={self.details}")

        context = ', '.join(context_parts)

        return f"Error({context})"


# -- Internal Types -----------------------------------------------------------

class ErrorKindInterface(Protocol):
    """Enforces that any error type object has a code string and message string."""

    @property
    def value(self) -> str: ...

    @property
    def name(self) -> str: ...
