from collections.abc import Generator, Mapping
from contextlib import contextmanager
from typing import cast

from armaden.framework.runtime.http.routing.route_group_stack import RouteGroupStack


@contextmanager
def route_module_context(
    configuration: Mapping[str, object] | None,
) -> Generator[None, None, None]:
    if configuration is None:
        yield
        return
    prefix = configuration.get('prefix')
    middleware_object = configuration.get('middleware', [])
    namespace = configuration.get('namespace')
    middleware_values = (
        cast(list[object], middleware_object)
        if isinstance(middleware_object, list)
        else cast(list[object], [])
    )
    middleware = [
        item
        for item in middleware_values
        if isinstance(item, str)
    ]
    stack = RouteGroupStack.get_instance()
    stack.push(
        prefix=prefix if isinstance(prefix, str) else '',
        middleware=middleware,
        namespace=namespace if isinstance(namespace, str) else None,
    )
    try:
        yield
    finally:
        stack.pop()
