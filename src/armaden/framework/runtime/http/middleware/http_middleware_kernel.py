from __future__ import annotations

import importlib
from collections.abc import Mapping
from typing import cast, override

from armaden.framework.protocols.http_middleware_kernel_protocol import (
    HttpMiddlewareKernelProtocol,
)
from armaden.framework.runtime.http.middleware.http_middleware import HttpMiddleware


class HttpMiddlewareKernel(HttpMiddlewareKernelProtocol[HttpMiddleware]):
    middleware: list[type[HttpMiddleware]] = []
    middleware_groups: dict[str, list[str | type[HttpMiddleware]]] = {}
    route_middleware: dict[str, type[HttpMiddleware]] = {}

    def __init__(self, application: object | None = None) -> None:
        self._application: object | None = application
        self._initialized: bool = False


    def _resolve_from_string(self, name: str) -> type[HttpMiddleware]:
        try:
            module_name, class_name = name.rsplit('.', 1)
            module = importlib.import_module(module_name)
            middleware = getattr(module, class_name)
        except (AttributeError, ImportError, ValueError) as exception:
            raise ImportError(
                f'Cannot resolve HTTP middleware "{name}": {exception}'
            ) from exception
        if not isinstance(middleware, type) or not issubclass(middleware, HttpMiddleware):
            raise TypeError(f'HTTP middleware "{name}" is not an HttpMiddleware class.')
        return middleware


    @override
    def bootstrap(self) -> None:
        if self._initialized:
            return
        self._initialized = True


    @override
    def get_middleware(self) -> list[type[HttpMiddleware]]:
        application_middleware = getattr(self._application, 'middleware', [])
        if not isinstance(application_middleware, list):
            application_middleware = []
        values = cast(list[type[HttpMiddleware]], application_middleware)
        return [*values, *self.middleware]


    @override
    def get_middleware_groups(self) -> dict[str, list[str | type[HttpMiddleware]]]:
        application_groups = getattr(self._application, 'middleware_groups', {})
        if not isinstance(application_groups, Mapping):
            application_groups = {}
        group_mapping = cast(Mapping[object, object], application_groups)
        groups: dict[str, list[str | type[HttpMiddleware]]] = {}
        for name, values in group_mapping.items():
            if isinstance(name, str) and isinstance(values, list):
                groups[name] = cast(list[str | type[HttpMiddleware]], values)
        groups.update(self.middleware_groups)
        return groups


    @override
    def get_route_middleware(self) -> dict[str, type[HttpMiddleware]]:
        return dict(self.route_middleware)


    @override
    def resolve_middleware(
        self,
        middleware: str | type[HttpMiddleware],
    ) -> type[HttpMiddleware]:
        if isinstance(middleware, type):
            return middleware
        if middleware in self.route_middleware:
            return self.route_middleware[middleware]
        return self._resolve_from_string(middleware)


    @override
    def resolve_middleware_list(
        self,
        middleware: list[str | type[HttpMiddleware]],
    ) -> list[type[HttpMiddleware]]:
        groups = self.get_middleware_groups()
        resolved: list[type[HttpMiddleware]] = []
        for value in middleware:
            if isinstance(value, str) and value in groups:
                resolved.extend(self.resolve_middleware_list(groups[value]))
            else:
                resolved.append(self.resolve_middleware(value))
        return resolved
