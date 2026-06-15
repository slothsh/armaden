from typing import Protocol


class ErrorInterface(Protocol):
    """Enforces that any error type object has a code string and message string."""

    @property
    def value(self) -> str: ...

    @property
    def name(self) -> str: ...
