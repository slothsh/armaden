import logging
from typing import Callable, Self, Type, TypeVar, cast

from armaden.framework.utils.types import RouterType
from .app import app

logger = logging.getLogger(__name__)

C = TypeVar("C")

class Route:
    @classmethod
    def get(cls, path: str, controller: Type[C], handler: str) -> Type[Self]:
        try:
            container = app().container
            if 'router' not in container:
                logger.error("Router not bound in container")
                return cls
            router = container['router']
        except Exception as e:
            logger.error("Failed to resolve router from container: %s", e)
            return cls

        instance = controller()
        callback = getattr(instance, handler)
        cast(RouterType, router).get(path)(callback)
        return cls


    @classmethod
    def post(cls, path: str, controller: Type[C], handler: str) -> Type[Self]:
        try:
            container = app().container
            if 'router' not in container:
                logger.error("Router not bound in container")
                return cls
            router = container['router']
        except Exception as e:
            logger.error("Failed to resolve router from container: %s", e)
            return cls

        instance = controller()
        callback = getattr(instance, handler)
        cast(RouterType, router).post(path)(callback)
        return cls
