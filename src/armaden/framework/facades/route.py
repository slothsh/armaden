from typing import Any, Callable

from armaden.framework.runtime.http.routing.route_facade import RouteFacade
from armaden.framework.runtime.http.routing.route_group import RouteGroup


class Route:
    @classmethod
    def get(cls, path: str, handler: tuple[type, str] | Callable, **options: Any) -> None:
        RouteFacade.get(path, handler, **options)

    @classmethod
    def post(cls, path: str, handler: tuple[type, str] | Callable, **options: Any) -> None:
        RouteFacade.post(path, handler, **options)

    @classmethod
    def put(cls, path: str, handler: tuple[type, str] | Callable, **options: Any) -> None:
        RouteFacade.put(path, handler, **options)

    @classmethod
    def patch(cls, path: str, handler: tuple[type, str] | Callable, **options: Any) -> None:
        RouteFacade.patch(path, handler, **options)

    @classmethod
    def delete(cls, path: str, handler: tuple[type, str] | Callable, **options: Any) -> None:
        RouteFacade.delete(path, handler, **options)

    @classmethod
    def options(cls, path: str, handler: tuple[type, str] | Callable, **options: Any) -> None:
        RouteFacade.options(path, handler, **options)

    @classmethod
    def match(cls, methods: list[str], path: str, handler: tuple[type, str] | Callable, **options: Any) -> None:
        RouteFacade.match(methods, path, handler, **options)

    @classmethod
    def any(cls, path: str, handler: tuple[type, str] | Callable, **options: Any) -> None:
        RouteFacade.any(path, handler, **options)

    @classmethod
    def prefix(cls, prefix: str) -> 'RouteGroup':
        return RouteFacade.prefix(prefix)

    @classmethod
    def middleware(cls, *mw: str) -> 'RouteGroup':
        return RouteFacade.middleware(*mw)

    @classmethod
    def namespace(cls, ns: str) -> 'RouteGroup':
        return RouteFacade.namespace(ns)

    @classmethod
    def group(cls, callback: Callable[[], None]) -> None:
        RouteFacade.group(callback)

    @classmethod
    def resource(cls, name: str, controller: type | str, **options: Any) -> None:
        RouteFacade.resource(name, controller, **options)
