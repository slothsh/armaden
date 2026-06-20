from abc import ABC, abstractmethod
from typing import Any, Dict

from ..utils.types import Result


class Server(ABC):
    @abstractmethod
    async def initialize(self) -> Result[None]: ...


    @abstractmethod
    async def run(self) -> Result[None]: ...


    @abstractmethod
    async def shutdown(self) -> Result[None]: ...


    @abstractmethod
    async def status(self) -> Result[Dict[str, Any]]: ...
