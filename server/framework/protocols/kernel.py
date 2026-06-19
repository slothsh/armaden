from returns.result import Result
import asyncio
from typing import Dict, Protocol, Any, Self, Type, TypeVar
from .supervisor import SupervisorInterface
from .error import ErrorInterface

class KernelInterface(Protocol):
    supervisor: SupervisorInterface

    def version(self) -> str: ...
    def environment(self, name: str, default: str | None = None) -> str | None: ...
    def config(self, key: str, default: Any | None = None) -> Any: ...

    async def status(self) -> Dict[str, Any]: ...

    @staticmethod
    def bootstrap(default_application: Type[T], user_application: Type[U] | None = None) -> Result[T | U, ErrorInterface]: ...

    @classmethod
    def instance(cls) -> Self: ...


    @classmethod
    def event_loop(cls) -> asyncio.AbstractEventLoop: ...


T = TypeVar("T", bound=KernelInterface)
U = TypeVar("U", bound=KernelInterface)
