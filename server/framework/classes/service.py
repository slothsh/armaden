from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple
from collections.abc import Callable, Coroutine

from returns.result import Success

from ..utils.types import Result

class Service(ABC):
    def __init__(self):
        self.status_callbacks: List[Tuple[str, StatusCallback]] = []


    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> Result[None]:
        pass


    async def status(self) -> Result[Dict[str, Result[StatusReturnValue]]]:
        return Success({ name: await status() for (name, status) in self.status_callbacks })


# -- Internal Types -----------------------------------------------------------

type StatusReturnValue = Dict[str, Any]
type StatusCallback = Callable[[], Coroutine[None, None, Result[StatusReturnValue]]]
