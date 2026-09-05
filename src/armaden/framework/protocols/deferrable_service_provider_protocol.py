from typing import Protocol


class DeferrableServiceProviderProtocol(Protocol):
    def provides(self) -> list[object]: ...