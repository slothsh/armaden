from typing import Dict

from ..protocols.error import ErrorInterface


class Error:
    """Accepts any Enum instance that implements a .message property."""

    def __init__(self, error_type: ErrorInterface, details: Dict | None = None):
        self.type = error_type
        self.context = error_type.value
        self.details = details or {}


    def __repr__(self):
        context_parts = []

        context_parts.append(f"type={self.type.__class__.__name__}.{self.type.name}")
        context_parts.append(f"context=\"{self.context}\"")

        if self.details:
            context_parts.append(f"details={self.details}")

        context = ', '.join(context_parts)

        return f"Error({context})"
