import logging

from returns.result import Failure, Success

from enum import StrEnum
from typing import Dict, Generic, TypeVar, Any, Mapping, cast

from ..errors.error import Error
from ..utils.types import Result


logger = logging.getLogger(__name__)

H = TypeVar('H', bound=Mapping[str, Any])


class HandleManager(Generic[H]):
    def __init__(self) -> None:
        self._handles: H = cast(H, {})


    def handle(self, key: str) -> Result[Any]:
        if key not in self._handles:
            return Failure(Error(HandleManagerError.HANDLE_NOT_FOUND, details={
                'key': key
            }))

        return Success(self._handles[key])


    def register_handle(self, key: str, handle: Any) -> Result[None]:
        cast(Dict[str, Any], self._handles)[key] = handle
        return Success(None)


    def register_handles(self, handles: Mapping[str, Any]) -> Result[None]:
        cast(Dict[str, Any], self._handles).update(handles)
        return Success(None)


# -- Internal Types -------------------------------------------------------

class HandleManagerError(StrEnum):
    HANDLE_NOT_FOUND = 'the requested handle was not found in the handle manager'
