from returns.result import Result

from .service import ServiceInterface
from .error import ErrorInterface
from typing import List, Protocol


class ServiceManagerInterface(Protocol):
    async def initialize(self) -> Result[None, ErrorInterface]: ...
    def add_service(self, service: ServiceInterface) -> Result[None, ErrorInterface]: ...
    def add_services(self, services: List[ServiceInterface]) -> Result[None, ErrorInterface]: ...

    @property
    def services(self) -> List[ServiceInterface]: ...
