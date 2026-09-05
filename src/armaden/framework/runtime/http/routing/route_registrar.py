from __future__ import annotations

from collections.abc import Callable, Mapping
from threading import Lock
from typing import ClassVar, cast, override

from armaden.framework.protocols.route_registrar_protocol import RouteRegistrarProtocol
from armaden.framework.runtime.http.routing.dto.route_definition_data import (
    RouteDefinitionData,
)
from armaden.framework.runtime.http.routing.route_group import RouteGroup
from armaden.framework.runtime.http.routing.route_group_stack import RouteGroupStack


class RouteRegistrar(RouteRegistrarProtocol):
    _ALL_METHODS: ClassVar[list[str]] = [
        'GET',
        'POST',
        'PUT',
        'PATCH',
        'DELETE',
        'OPTIONS',
        'HEAD',
    ]
    _instance: RouteRegistrar | None = None
    _lock: Lock = Lock()

    def __init__(self) -> None:
        self._routes: list[RouteDefinitionData] = []


    def _register(
        self,
        methods: list[str],
        path: str,
        handler: object,
        options: Mapping[str, object],
    ) -> RouteRegistrar:
        stack = RouteGroupStack.get_instance()
        middleware_value = options.get('middleware', [])
        middleware_items = cast(list[object], middleware_value) if isinstance(middleware_value, list) else []
        middleware = [value for value in middleware_items if isinstance(value, str)]
        where_value = options.get('where', {})
        if isinstance(where_value, Mapping):
            where_mapping = cast(Mapping[object, object], where_value)
        else:
            where_mapping: Mapping[object, object] = {}
        where: dict[str, str] = {}
        for key, value in where_mapping.items():
            if isinstance(key, str) and isinstance(value, str):
                where[key] = value
        name = options.get('name')
        self._routes.append(RouteDefinitionData(
            handler=stack.resolve_handler(handler),
            methods=methods,
            middleware=stack.resolve_middleware(middleware),
            name=name if isinstance(name, str) else None,
            path=stack.resolve_path(path),
            where=where,
        ))
        return self


    @classmethod
    def get_instance(cls) -> RouteRegistrar:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance


    @override
    def any(self, path: str, handler: object, **options: object) -> RouteRegistrar:
        return self._register(self._ALL_METHODS, path, handler, options)


    @override
    def clear(self) -> None:
        self._routes.clear()


    @override
    def delete(self, path: str, handler: object, **options: object) -> RouteRegistrar:
        return self._register(['DELETE'], path, handler, options)


    @override
    def get(self, path: str, handler: object, **options: object) -> RouteRegistrar:
        return self._register(['GET'], path, handler, options)


    @override
    def get_routes(self) -> list[RouteDefinitionData]:
        return list(self._routes)


    @override
    def group(self, callback: Callable[[], None]) -> None:
        with RouteGroup():
            callback()


    @override
    def match(
        self,
        methods: list[str],
        path: str,
        handler: object,
        **options: object,
    ) -> RouteRegistrar:
        return self._register(methods, path, handler, options)


    @override
    def middleware(self, *middleware: str) -> RouteGroup:
        return RouteGroup(middleware=list(middleware))


    @override
    def namespace(self, namespace: str) -> RouteGroup:
        return RouteGroup(namespace=namespace)


    @override
    def options(self, path: str, handler: object, **options: object) -> RouteRegistrar:
        return self._register(['OPTIONS'], path, handler, options)


    @override
    def patch(self, path: str, handler: object, **options: object) -> RouteRegistrar:
        return self._register(['PATCH'], path, handler, options)


    @override
    def post(self, path: str, handler: object, **options: object) -> RouteRegistrar:
        return self._register(['POST'], path, handler, options)


    @override
    def prefix(self, prefix: str) -> RouteGroup:
        return RouteGroup(prefix=prefix)


    @override
    def put(self, path: str, handler: object, **options: object) -> RouteRegistrar:
        return self._register(['PUT'], path, handler, options)


    @override
    def resource(
        self,
        name: str,
        controller: type[object],
        **options: object,
    ) -> None:
        only_value = options.get('only')
        exclude_value = options.get('except')
        only = cast(list[str] | None, only_value) if isinstance(only_value, list) else None
        exclude = cast(list[str] | None, exclude_value) if isinstance(exclude_value, list) else None
        actions = {
            'index': ('GET', f'/{name}'),
            'store': ('POST', f'/{name}'),
            'show': ('GET', f'/{name}/{{id:int}}'),
            'update': ('PUT', f'/{name}/{{id:int}}'),
            'destroy': ('DELETE', f'/{name}/{{id:int}}'),
        }
        for action, (method, path) in actions.items():
            if only is not None and action not in only:
                continue
            if exclude is not None and action in exclude:
                continue
            _ = self._register(
                [method],
                path,
                (controller, action),
                {**options, 'name': f'{name}.{action}'},
            )
