import asyncio
from typing import TYPE_CHECKING, Any, Protocol, Self
from returns.result import Result

if TYPE_CHECKING:
    from framework.classes.instance_container import InstanceContainer

from .supervisor import SupervisorInterface
from .error import ErrorInterface


class KernelInterface(Protocol):
    def boot(self) -> Result[None, ErrorInterface]: ...

    async def __call__(self) -> Result[None, ErrorInterface]: ...

    def version(self) -> str: ...
    def config(self, key: str, default: Any | None = None) -> Any: ...

    @property
    def container(self) -> InstanceContainer: ...

    @classmethod
    def instance(cls) -> Self: ...

    @classmethod
    def event_loop(cls) -> asyncio.AbstractEventLoop: ...

    @property
    def supervisor(self) -> SupervisorInterface: ...
