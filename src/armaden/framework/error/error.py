from armaden.framework.error.protocols.error_kind_protocol import ErrorKindProtocol
from armaden.framework.error.protocols.error_protocol import ErrorProtocol
from typing import Any, override


class Error(ErrorProtocol):
    _ERROR_TAG: None

    def __init__(self, kind: ErrorKindProtocol, details: dict[Any, Any] | None = None) -> None:
        self.kind: ErrorKindProtocol = kind
        self.context: str = kind.value
        self.details: dict[Any, Any] = details or {}


    @override
    def __repr__(self) -> str:
        context_parts: list[str] = []

        context_parts.append(f"type={self.kind.__class__.__name__}.{self.kind.name}")
        context_parts.append(f"context=\"{self.context}\"")

        if self.details:
            context_parts.append(f"details={self.details}")

        context = ', '.join(context_parts)

        return f"Error({context})"
