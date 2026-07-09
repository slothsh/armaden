from abc import ABC, abstractmethod
from typing import Any, Callable, Coroutine

from ..request import Request

NextCallable = Callable[[Request], Coroutine[Any, Any, Any]]


class Middleware(ABC):
    @abstractmethod
    async def handle(self, request: Request, next: NextCallable) -> Any:
        raise NotImplementedError

    async def terminate(self, request: Request, response: Any) -> None:
        pass
