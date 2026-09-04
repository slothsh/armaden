from abc import ABC, abstractmethod
from typing import override

from armaden.framework.protocols.deferrable_provider_protocol import (
    DeferrableProviderProtocol,
)


class DeferrableProvider(DeferrableProviderProtocol, ABC):
    @override
    @abstractmethod
    def provides(self) -> list[object]:
        raise NotImplementedError