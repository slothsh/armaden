import logging
from typing import Callable, Self, Type, TypeVar, cast

from returns.pipeline import is_successful
from framework.utils.types import RouterType
from .app import app

logger = logging.getLogger(__name__)

C = TypeVar("C")

class Route:
    @classmethod
    def get(cls, path: str, controller: Type[C], handler: str) -> Type[Self]:
        if not is_successful(result := app().handle_manager().handle('router')):
            logger.error(result.failure())
            return cls

        instance = controller()
        callback = getattr(instance, handler)
        cast(RouterType, result.unwrap()).get(path)(callback)
        return cls


    @classmethod
    def post(cls, path: str, controller: Type[C], handler: str) -> Type[Self]:
        if not is_successful(result := app().handle_manager().handle('router')):
            logger.error(result.failure())
            return cls

        instance = controller()
        callback = getattr(instance, handler)
        cast(RouterType, result.unwrap()).post(path)(callback)
        return cls
