import logging
from typing import Callable, Self, Type, TypeVar, cast

from returns.pipeline import is_successful
from ...runtime.kernel import Kernel
from ...utils.types import RouterType

logger = logging.getLogger(__name__)

C = TypeVar("C")

class Route:
    @classmethod
    def get(cls, path: str, controller: Type[C], handler: str) -> Type[Self]:
        if not is_successful(result := Kernel.handle_manager().handle('router')):
            logger.error(result.failure())
        else:
            instance = controller()
            callback = getattr(instance, handler)
            cast(RouterType, result.unwrap()).get(path)(callback)
        return cls


    @classmethod
    def post(cls, path: str, controller: Type[C], handler: str) -> Type[Self]:
        if not is_successful(result := Kernel.handle_manager().handle('router')):
            logger.error(result.failure())
        else:
            instance = controller()
            callback = getattr(instance, handler)
            cast(RouterType, result.unwrap()).post(path)(callback)
        return cls
