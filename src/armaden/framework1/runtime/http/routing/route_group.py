import threading
from dataclasses import dataclass, field
from typing import Any


@dataclass
class GroupState:
    prefix: str = ''
    middleware: list[str] = field(default_factory=list)
    namespace: str | None = None


class RouteGroupStack:
    _instance: 'RouteGroupStack | None' = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        self._stack: list[GroupState] = []

    @classmethod
    def get_instance(cls) -> 'RouteGroupStack':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def push(self, prefix: str = '', middleware: list[str] | None = None, namespace: str | None = None) -> None:
        parent = self._stack[-1] if self._stack else None
        if prefix and not prefix.startswith('/'):
            prefix = '/' + prefix
        resolved_prefix = prefix
        if parent and parent.prefix:
            resolved_prefix = parent.prefix.rstrip('/') + '/' + prefix.lstrip('/')
        resolved_middleware = list(middleware or [])
        if parent:
            resolved_middleware = parent.middleware + resolved_middleware
        resolved_namespace = namespace or (parent.namespace if parent else None)

        self._stack.append(GroupState(
            prefix=resolved_prefix,
            middleware=resolved_middleware,
            namespace=resolved_namespace,
        ))

    def pop(self) -> None:
        if self._stack:
            self._stack.pop()

    def current(self) -> GroupState | None:
        return self._stack[-1] if self._stack else None

    def resolve_path(self, path: str) -> str:
        state = self.current()
        if state and state.prefix:
            resolved = state.prefix.rstrip('/') + '/' + path.lstrip('/')
        else:
            resolved = path
        if not resolved.startswith('/'):
            resolved = '/' + resolved
        return resolved

    def resolve_middleware(self, middleware: list[str]) -> list[str]:
        state = self.current()
        if state and state.middleware:
            return state.middleware + list(middleware)
        return list(middleware)

    def resolve_handler(self, handler: Any) -> Any:
        state = self.current()
        if state and state.namespace and isinstance(handler, (list, tuple)) and len(handler) == 2:
            cls_or_name, method = handler
            if isinstance(cls_or_name, str):
                return [f'{state.namespace}\\{cls_or_name}', method]
            return [cls_or_name, method]
        return handler


class RouteGroup:
    def __init__(
        self,
        prefix: str = '',
        middleware: list[str] | None = None,
        namespace: str | None = None,
    ) -> None:
        self._prefix = prefix
        self._middleware: list[str] = list(middleware) if middleware else []
        self._namespace = namespace

    def prefix(self, prefix: str) -> 'RouteGroup':
        self._prefix = prefix
        return self

    def middleware(self, *mw: str) -> 'RouteGroup':
        self._middleware = list(mw)
        return self

    def namespace(self, ns: str) -> 'RouteGroup':
        self._namespace = ns
        return self

    def __enter__(self) -> 'RouteGroup':
        RouteGroupStack.get_instance().push(
            prefix=self._prefix,
            middleware=self._middleware,
            namespace=self._namespace,
        )
        return self

    def __exit__(self, *args: object) -> None:
        _ = args
        RouteGroupStack.get_instance().pop()
