from typing import Any, Mapping, Protocol

from returns.result import Result

from ..protocols.error import ErrorInterface


class HandleManagerInterface(Protocol):
    def handle(self, key: str) -> Result[None, ErrorInterface]: ...
    def register_handle(self, key: str, handle: Any) -> Result[None, ErrorInterface]: ...
    def register_handles(self, handles: Mapping[str, Any]) -> Result[None, ErrorInterface]: ...
