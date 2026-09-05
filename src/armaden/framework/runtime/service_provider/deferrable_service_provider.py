from abc import ABC, abstractmethod
from typing import override

from armaden.framework.protocols.deferrable_service_provider_protocol import (
    DeferrableServiceProviderProtocol,
)


class DeferrableServiceProvider(DeferrableServiceProviderProtocol, ABC):
    @override
    @abstractmethod
    def provides(self) -> list[object]:
        raise NotImplementedError