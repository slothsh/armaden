import logging
from typing import Any, Callable

from .route_registrar import RouteRegistrar
from .route_group import RouteGroup

logger = logging.getLogger(__name__)


class RouteFacade:
    _registrar = RouteRegistrar.get_instance()

    @classmethod
    def get(cls, path: str, handler: tuple[type, str] | Callable, **options: Any) -> None:
        cls._registrar.get(path, handler, **options)

    @classmethod
    def post(cls, path: str, handler: tuple[type, str] | Callable, **options: Any) -> None:
        cls._registrar.post(path, handler, **options)

    @classmethod
    def put(cls, path: str, handler: tuple[type, str] | Callable, **options: Any) -> None:
        cls._registrar.put(path, handler, **options)

    @classmethod
    def patch(cls, path: str, handler: tuple[type, str] | Callable, **options: Any) -> None:
        cls._registrar.patch(path, handler, **options)

    @classmethod
    def delete(cls, path: str, handler: tuple[type, str] | Callable, **options: Any) -> None:
        cls._registrar.delete(path, handler, **options)

    @classmethod
    def options(cls, path: str, handler: tuple[type, str] | Callable, **options: Any) -> None:
        cls._registrar.options(path, handler, **options)

    @classmethod
    def match(cls, methods: list[str], path: str, handler: tuple[type, str] | Callable, **options: Any) -> None:
        cls._registrar.match(methods, path, handler, **options)

    @classmethod
    def any(cls, path: str, handler: tuple[type, str] | Callable, **options: Any) -> None:
        cls._registrar.any(path, handler, **options)

    @classmethod
    def prefix(cls, prefix: str) -> 'RouteGroup':
        return RouteGroup(prefix=prefix)

    @classmethod
    def middleware(cls, *mw: str) -> 'RouteGroup':
        return RouteGroup(middleware=list(mw))

    @classmethod
    def namespace(cls, ns: str) -> 'RouteGroup':
        return RouteGroup(namespace=ns)

    @classmethod
    def group(cls, callback: Callable[[], None]) -> None:
        with RouteGroup() as _:
            callback()

    @classmethod
    def resource(cls, name: str, controller: type | str, **options: Any) -> None:
        cls._registrar.resource(name, controller, **options)
