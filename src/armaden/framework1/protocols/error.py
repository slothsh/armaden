from typing import Protocol


class ErrorInterface(Protocol):
    _ERROR_TAG: None

    def __repr__(self) -> str: ...
