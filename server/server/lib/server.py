from server.lib.types import Result
from abc import ABC, abstractmethod


class Server(ABC):
    @abstractmethod
    async def initialize(self) -> Result[None]:
        pass


    @abstractmethod
    async def run(self) -> Result[None]:
        pass


    @abstractmethod
    async def shutdown(self) -> Result[None]:
        pass
