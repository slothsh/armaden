import inspect
import logging
from typing import Any, Callable

from fastapi import APIRouter, FastAPI
from starlette.requests import Request as StarletteRequest

from armaden.framework.runtime.http.middleware.middleware import Middleware

from ..controller import Controller
from ..middleware.kernel import HttpKernel
from ..middleware.pipeline import MiddlewarePipeline
from ..request import Request
from ..request_context import RequestContext
from .route import RouteDefinition
from .route_parameter import RouteParameter

logger = logging.getLogger(__name__)


class RouteCompiler:
    def __init__(self, app: FastAPI, kernel: HttpKernel | None = None, container: Any = None) -> None:
        self._app = app
        self._kernel = kernel
        self._container = container

    def compile(
        self,
        routes: list[RouteDefinition],
        router: APIRouter | None = None,
    ) -> None:
        target = router or self._app.router

        from ..url_generator import UrlGenerator
        url_gen = UrlGenerator.get_instance()

        for route in routes:
            fastapi_path, param_types = RouteParameter.parse(route.path)
            resolved_handler = self._resolve_handler(route)
            middleware_classes = self._resolve_middleware(route)
            wrapped_handler = self._wrap_handler(resolved_handler, middleware_classes, param_types)

            for method in route.methods:
                method_lower = method.lower()
                route_method = getattr(target, method_lower, None)
                if route_method is None:
                    logger.warning('Unsupported HTTP method %s for route %s', method, route.path)
                    continue
                route_method(fastapi_path)(wrapped_handler)

            if route.name:
                url_gen.register(route.name, route.path, route.methods, param_types)

    def _resolve_handler(self, route: RouteDefinition) -> Callable:
        handler = route.handler

        if isinstance(handler, (list, tuple)):
            controller_cls, method_name = handler
            async def _controller_handler(request: StarletteRequest) -> Any:
                wrapped_request = Request(request)
                await wrapped_request._load_body()
                RequestContext.set_request(wrapped_request)
                try:
                    controller_instance = self._container.make(controller_cls)
                    method = getattr(controller_instance, method_name)
                    kwargs: dict[str, Any] = dict(request.path_params)
                    try:
                        body = await request.json()
                        if isinstance(body, dict):
                            kwargs.update(body)
                    except Exception:
                        pass
                    try:
                        result = method(**kwargs)
                    except TypeError:
                        result = method(wrapped_request, **kwargs)
                    if inspect.isawaitable(result):
                        result = await result
                    return result
                finally:
                    RequestContext.clear_request()
            return _controller_handler

        async def _callable_handler(request: StarletteRequest) -> Any:
            wrapped_request = Request(request)
            await wrapped_request._load_body()
            RequestContext.set_request(wrapped_request)
            try:
                kwargs: dict[str, Any] = dict(request.path_params)
                try:
                    body = await request.json()
                    if isinstance(body, dict):
                        kwargs.update(body)
                except Exception:
                    pass
                result = handler(**kwargs)
                if inspect.isawaitable(result):
                    result = await result
                return result
            finally:
                RequestContext.clear_request()

        return _callable_handler

    def _resolve_middleware(self, route: RouteDefinition) -> list[type]:
        kernel = self._kernel
        if kernel is None:
            return []

        global_mw: list[str | type[Middleware]] = [mw for mw in kernel.get_middleware()]
        route_mw = list(route.middleware)

        if isinstance(route.handler, (list, tuple)):
            controller_cls, method_name = route.handler
            if issubclass(controller_cls, Controller):
                controller_mw = controller_cls.get_middleware_for_method(method_name)
                route_mw = route_mw + controller_mw

        all_mw = global_mw + route_mw
        return kernel.resolve_middleware_list(all_mw)

    def _wrap_handler(
        self,
        handler: Callable,
        middleware_classes: list[type],
        param_types: dict[str, type],
    ) -> Callable:
        _ = param_types

        if not middleware_classes:
            return handler

        async def _wrapped(request: StarletteRequest) -> Any:
            wrapped_request = Request(request)
            await wrapped_request._load_body()
            RequestContext.set_request(wrapped_request)
            try:
                pipeline = MiddlewarePipeline(
                    middleware_classes,
                    lambda _: handler(request),
                    container=self._container,
                )
                response = await pipeline.send(wrapped_request)
                await pipeline.terminate(wrapped_request, response)
                return response
            finally:
                RequestContext.clear_request()

        return _wrapped
