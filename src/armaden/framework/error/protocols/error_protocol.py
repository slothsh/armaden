from typing import Protocol, override


class ErrorProtocol(Protocol):
    _ERROR_TAG: None

    @override
    def __repr__(self) -> str: ...
