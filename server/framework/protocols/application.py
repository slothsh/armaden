from abc import ABC, abstractmethod
from typing import Any, Mapping, Sequence

from returns.result import Success

from .service import ServiceInterface
from .service_manager import ServiceManagerInterface
from .supervisor import SupervisorInterface
from ..utils.types import Result


class ApplicationInterface(ABC):
    def configure(
        self,
        service_manager: ServiceManagerInterface,
        supervisor: SupervisorInterface,
    ) -> None:
        pass

    @abstractmethod
    def boot(self) -> Result[None]:
        ...

    @property
    def services(self) -> Sequence[ServiceInterface]:
        return []

    async def status(self) -> Result[Mapping[str, Any]]:
        return Success({})
