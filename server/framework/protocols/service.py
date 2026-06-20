from returns.result import Result
from typing import Any, Mapping, Protocol
from .error import ErrorInterface


class ServiceInterface(Protocol):
    name: str

    def __call__(self, *args: Any, **kwargs: Any) -> Result[None, ErrorInterface]: ...

    async def status(self) -> Result[Mapping[str, Any], ErrorInterface]: ...
