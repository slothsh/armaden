import asyncio
from typing import Any, Mapping, Protocol, Self
from returns.result import Result

from framework.protocols.handle_manager import HandleManagerInterface

from .service_manager import ServiceManagerInterface
from .supervisor import SupervisorInterface
from .error import ErrorInterface


class KernelInterface(Protocol):
    def boot(self) -> Result[None, ErrorInterface]: ...

    async def __call__(self) -> Result[None, ErrorInterface]: ...

    def version(self) -> str: ...
    def config(self, key: str, default: Any | None = None) -> Any: ...

    @classmethod
    def handle_manager(cls) -> HandleManagerInterface: ...

    @classmethod
    def instance(cls) -> Self: ...

    @classmethod
    def event_loop(cls) -> asyncio.AbstractEventLoop: ...

    @property
    def service_manager(self) -> ServiceManagerInterface: ...


    @property
    def supervisor(self) -> SupervisorInterface: ...
