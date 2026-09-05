from typing import Protocol, Self


class DatabaseQueryBuilderProtocol(Protocol):
    def table(self, name: str) -> Self: ...
