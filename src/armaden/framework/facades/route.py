from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import cast, override

from armaden.framework.facades.facade import Facade
from armaden.framework.protocols.route_registrar_protocol import RouteRegistrarProtocol


class RouteFacade(Facade):
    @classmethod
    def _registrar(cls) -> RouteRegistrarProtocol:
        return cast(RouteRegistrarProtocol, cls.get_facade_root())


    @classmethod
    def any(
        cls,
        path: str,
        handler: object,
        **options: object,
    ) -> RouteRegistrarProtocol:
        return cls._registrar().any(path, handler, **options)


    @classmethod
    def clear(cls) -> None:
        cls._registrar().clear()


    @classmethod
    def delete(
        cls,
        path: str,
        handler: object,
        **options: object,
    ) -> RouteRegistrarProtocol:
        return cls._registrar().delete(path, handler, **options)


    @classmethod
    def get(
        cls,
        path: str,
        handler: object,
        **options: object,
    ) -> RouteRegistrarProtocol:
        return cls._registrar().get(path, handler, **options)


    @override
    @classmethod
    def get_facade_accessor(cls) -> object:
        return RouteRegistrarProtocol


    @classmethod
    def get_routes(cls) -> Sequence[object]:
        return cls._registrar().get_routes()


    @classmethod
    def group(cls, callback: Callable[[], None]) -> None:
        cls._registrar().group(callback)


    @classmethod
    def match(
        cls,
        methods: list[str],
        path: str,
        handler: object,
        **options: object,
    ) -> RouteRegistrarProtocol:
        return cls._registrar().match(methods, path, handler, **options)


    @classmethod
    def middleware(cls, *middleware: str) -> object:
        return cls._registrar().middleware(*middleware)


    @classmethod
    def namespace(cls, namespace: str) -> object:
        return cls._registrar().namespace(namespace)


    @classmethod
    def options(
        cls,
        path: str,
        handler: object,
        **options: object,
    ) -> RouteRegistrarProtocol:
        return cls._registrar().options(path, handler, **options)


    @classmethod
    def patch(
        cls,
        path: str,
        handler: object,
        **options: object,
    ) -> RouteRegistrarProtocol:
        return cls._registrar().patch(path, handler, **options)


    @classmethod
    def post(
        cls,
        path: str,
        handler: object,
        **options: object,
    ) -> RouteRegistrarProtocol:
        return cls._registrar().post(path, handler, **options)


    @classmethod
    def prefix(cls, prefix: str) -> object:
        return cls._registrar().prefix(prefix)


    @classmethod
    def put(
        cls,
        path: str,
        handler: object,
        **options: object,
    ) -> RouteRegistrarProtocol:
        return cls._registrar().put(path, handler, **options)


    @classmethod
    def resource(
        cls,
        name: str,
        controller: type[object],
        **options: object,
    ) -> None:
        cls._registrar().resource(name, controller, **options)
