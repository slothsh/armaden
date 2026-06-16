from returns.result import Result
from typing import Any, Protocol
from .error import ErrorInterface


class ServiceInterface(Protocol):
    def __call__(self, *args: Any, **kwargs: Any) -> Result[None, ErrorInterface]: ...
