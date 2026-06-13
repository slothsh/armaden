from typing import Dict, Protocol

from returns.result import Result as ReturnsResult

type Result[S] = ReturnsResult[S, Error]


class ErrorTypeProtocol(Protocol):
    """Enforces that any error type object has a code string and message string."""

    @property
    def value(self) -> str: ...

    @property
    def name(self) -> str: ...


class Error:
    """Accepts any Enum instance that implements a .message property."""

    def __init__(self, error_type: ErrorTypeProtocol, details: Dict | None = None):
        self.type = error_type
        self.context = error_type.value
        self.details = details or {}


    def __repr__(self):
        return f"Error(type={self.type.__class__.__name__}.{self.type.name}, context='{self.context}')"
