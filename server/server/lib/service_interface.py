from typing import Any, Protocol
from server.lib.types import Result


class ServiceInterface(Protocol):
    def __call__(self, *args: Any, **kwargs: Any) -> Result[None]: ...
