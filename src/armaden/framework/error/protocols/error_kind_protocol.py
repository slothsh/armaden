from typing import Protocol


class ErrorKindProtocol(Protocol):
    @property
    def value(self) -> str: ...

    @property
    def name(self) -> str: ...
