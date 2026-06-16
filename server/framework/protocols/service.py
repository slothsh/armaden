from returns.result import Result
from typing import Any, Dict, Protocol
from .error import ErrorInterface


class ServiceInterface(Protocol):
    name: str

    def __call__(self, *args: Any, **kwargs: Any) -> Result[None, ErrorInterface]: ...

    async def status(self) -> Result[Dict[str, Result[Dict[str, Any], ErrorInterface]], ErrorInterface]: ...
