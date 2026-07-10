import threading
from typing import Any, Callable

from .route import RouteDefinition
from .route_group import RouteGroup, RouteGroupStack

_ALL_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD']


class RouteRegistrar:
    _instance: 'RouteRegistrar | None' = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        self._routes: list[RouteDefinition] = []

    @classmethod
    def get_instance(cls) -> 'RouteRegistrar':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    # -- Registration methods -------------------------------------------------

    def get(self, path: str, handler: tuple[type, str] | Callable, **options: Any) -> 'RouteRegistrar':
        return self._register(['GET'], path, handler, **options)

    def post(self, path: str, handler: tuple[type, str] | Callable, **options: Any) -> 'RouteRegistrar':
        return self._register(['POST'], path, handler, **options)

    def put(self, path: str, handler: tuple[type, str] | Callable, **options: Any) -> 'RouteRegistrar':
        return self._register(['PUT'], path, handler, **options)

    def patch(self, path: str, handler: tuple[type, str] | Callable, **options: Any) -> 'RouteRegistrar':
        return self._register(['PATCH'], path, handler, **options)

    def delete(self, path: str, handler: tuple[type, str] | Callable, **options: Any) -> 'RouteRegistrar':
        return self._register(['DELETE'], path, handler, **options)

    def options(self, path: str, handler: tuple[type, str] | Callable, **options: Any) -> 'RouteRegistrar':
        return self._register(['OPTIONS'], path, handler, **options)

    def match(self, methods: list[str], path: str, handler: tuple[type, str] | Callable, **options: Any) -> 'RouteRegistrar':
        return self._register(methods, path, handler, **options)

    def any(self, path: str, handler: tuple[type, str] | Callable, **options: Any) -> 'RouteRegistrar':
        return self._register(_ALL_METHODS, path, handler, **options)

    # -- Grouping methods -----------------------------------------------------

    def prefix(self, prefix: str) -> 'RouteGroup':
        return RouteGroup(prefix=prefix)

    def middleware(self, *mw: str) -> 'RouteGroup':
        return RouteGroup(middleware=list(mw))

    def namespace(self, ns: str) -> 'RouteGroup':
        return RouteGroup(namespace=ns)

    def group(self, callback: Callable[[], None]) -> None:
        with RouteGroup() as _:
            callback()

    # -- Resource routes ------------------------------------------------------

    def resource(self, name: str, controller: type, **options: Any) -> None:
        only: list[str] | None = options.get('only')
        exclude: list[str] | None = options.get('except')
        resource_actions: dict[str, tuple[str, str]] = {
            'index':   ('GET',     f'/{name}'),
            'store':   ('POST',    f'/{name}'),
            'show':    ('GET',     f'/{name}/{{id:int}}'),
            'update':  ('PUT',     f'/{name}/{{id:int}}'),
            'destroy': ('DELETE',  f'/{name}/{{id:int}}'),
        }

        for action, (method, path) in resource_actions.items():
            if only is not None and action not in only:
                continue
            if exclude is not None and action in exclude:
                continue
            self._register(
                [method],
                path,
                (controller, action),
                name=f'{name}.{action}',
            )

    # -- Accessors ------------------------------------------------------------

    def get_routes(self) -> list[RouteDefinition]:
        return list(self._routes)

    def clear(self) -> None:
        self._routes.clear()

    # -- Internal -------------------------------------------------------------

    def _register(
        self,
        methods: list[str],
        path: str,
        handler: tuple[type, str] | Callable,
        **options: Any,
    ) -> 'RouteRegistrar':
        stack = RouteGroupStack.get_instance()
        resolved_path = stack.resolve_path(path)
        resolved_middleware = stack.resolve_middleware(options.get('middleware', []))
        resolved_handler = stack.resolve_handler(handler)
        name = options.get('name')
        where = options.get('where', {})

        self._routes.append(RouteDefinition(
            methods=methods,
            path=resolved_path,
            handler=resolved_handler,
            name=name,
            middleware=resolved_middleware,
            where=where,
        ))
        return self
