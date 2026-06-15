from abc import ABC, abstractmethod
from typing import Any

from returns.result import Success

from ..utils.types import Result


class Service(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> Result[None]:
        return Success(None)
