from typing import Protocol


class DeferrableProviderProtocol(Protocol):
    def provides(self) -> list[object]: ...