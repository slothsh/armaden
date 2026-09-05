from __future__ import annotations

from threading import Lock
from typing import cast, override

from armaden.framework.protocols.route_group_stack_protocol import (
    RouteGroupStackProtocol,
)
from armaden.framework.runtime.http.routing.dto.route_group_state_data import (
    RouteGroupStateData,
)


class RouteGroupStack(RouteGroupStackProtocol[RouteGroupStateData]):
    _instance: RouteGroupStack | None = None
    _lock: Lock = Lock()

    def __init__(self) -> None:
        self._stack: list[RouteGroupStateData] = []


    @override
    def current(self) -> RouteGroupStateData | None:
        return self._stack[-1] if self._stack else None


    @override
    @classmethod
    def get_instance(cls) -> RouteGroupStack:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance


    @override
    def pop(self) -> None:
        if self._stack:
            _ = self._stack.pop()


    @override
    def push(
        self,
        prefix: str = '',
        middleware: list[str] | None = None,
        namespace: str | None = None,
    ) -> None:
        parent = self.current()
        normalized_prefix = f'/{prefix.lstrip("/")}' if prefix else ''
        if parent is not None and parent.prefix:
            normalized_prefix = (
                f'{parent.prefix.rstrip("/")}/{normalized_prefix.lstrip("/")}'
            )
        resolved_middleware = list(middleware or [])
        if parent is not None:
            resolved_middleware = [*parent.middleware, *resolved_middleware]
        resolved_namespace = namespace or (parent.namespace if parent else None)
        _ = self._stack.append(RouteGroupStateData(
            middleware=resolved_middleware,
            namespace=resolved_namespace,
            prefix=normalized_prefix,
        ))


    @override
    def resolve_handler(self, handler: object) -> object:
        original_handler: object = handler
        state = self.current()
        if state is not None and state.namespace and isinstance(handler, (list, tuple)):
            values = cast(list[object] | tuple[object, ...], handler)
            if len(values) == 2:
                controller = values[0]
                method = values[1]
                if isinstance(controller, str):
                    resolved_handler: list[object] = [
                        f'{state.namespace}\\{controller}',
                        method,
                    ]
                    return resolved_handler
        return original_handler


    @override
    def resolve_middleware(self, middleware: list[str]) -> list[str]:
        state = self.current()
        if state is None:
            return list(middleware)
        return [*state.middleware, *middleware]


    @override
    def resolve_path(self, path: str) -> str:
        state = self.current()
        if state is not None and state.prefix:
            path = f'{state.prefix.rstrip("/")}/{path.lstrip("/")}'
        return path if path.startswith('/') else f'/{path}'
