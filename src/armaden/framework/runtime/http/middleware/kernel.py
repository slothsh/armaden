import importlib
from typing import Any

from .middleware import Middleware


class HttpKernel:
    middleware: list[type[Middleware]] = []
    middleware_groups: dict[str, list[type[Middleware]]] = {}
    route_middleware: dict[str, type[Middleware]] = {}

    def __init__(self) -> None:
        self._initialized = False

    def bootstrap(self) -> None:
        if self._initialized:
            return
        self._initialized = True

    def get_middleware(self) -> list[type[Middleware]]:
        return list(self.middleware)

    def get_middleware_groups(self) -> dict[str, list[type[Middleware]]]:
        return dict(self.middleware_groups)

    def get_route_middleware(self) -> dict[str, type[Middleware]]:
        return dict(self.route_middleware)

    def resolve_middleware(self, name_or_class: str | type[Middleware]) -> type[Middleware]:
        if isinstance(name_or_class, type) and issubclass(name_or_class, Middleware):
            return name_or_class
        if name_or_class in self.route_middleware:
            return self.route_middleware[name_or_class]
        return self._resolve_from_string(name_or_class)

    def resolve_middleware_list(self, names: list[str | type[Middleware]]) -> list[type[Middleware]]:
        resolved: list[type[Middleware]] = []
        for name in names:
            if isinstance(name, str) and name in self.middleware_groups:
                group = self.middleware_groups[name]
                resolved.extend(self.resolve_middleware_list(group))
                continue
            resolved.append(self.resolve_middleware(name))
        return resolved

    @staticmethod
    def _resolve_from_string(name: str) -> type[Middleware]:
        try:
            module_path, class_name = name.rsplit('.', 1)
            module = importlib.import_module(module_path)
            return getattr(module, class_name)
        except (ValueError, ImportError, AttributeError) as e:
            raise ImportError(f'Cannot resolve middleware "{name}": {e}') from e


class DefaultKernel(HttpKernel):
    middleware: list[type[Middleware]] = []
    middleware_groups: dict[str, list[type[Middleware]]] = {
        'api': [],
        'web': [],
    }
    route_middleware: dict[str, type[Middleware]] = {}
