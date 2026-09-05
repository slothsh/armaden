from __future__ import annotations

import inspect
import logging
from collections.abc import Awaitable, Callable, Mapping
from typing import cast, override

from fastapi import APIRouter, FastAPI
from starlette.requests import Request as StarletteRequest

from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.http_request_protocol import HttpRequestProtocol
from armaden.framework.protocols.route_compiler_protocol import RouteCompilerProtocol
from armaden.framework.protocols.url_generator_protocol import UrlGeneratorProtocol
from armaden.framework.runtime.http.http_controller import HttpController
from armaden.framework.runtime.http.middleware.http_middleware import HttpMiddleware
from armaden.framework.runtime.http.middleware.http_middleware_kernel import HttpMiddlewareKernel
from armaden.framework.runtime.http.middleware.http_middleware_pipeline import (
    HttpMiddlewarePipeline,
)
from armaden.framework.runtime.http.http_request import HttpRequest
from armaden.framework.runtime.http.http_request_context import HttpRequestContext
from armaden.framework.runtime.http.routing.dto.route_definition_data import (
    RouteDefinitionData,
)
from armaden.framework.runtime.http.routing.route_parameter import RouteParameter
from armaden.framework.runtime.http.url_generator import UrlGenerator


logger = logging.getLogger(__name__)


class RouteCompiler(RouteCompilerProtocol[RouteDefinitionData, APIRouter]):
    def __init__(
        self,
        app: FastAPI,
        kernel: HttpMiddlewareKernel | None = None,
        container: ContainerProtocol | None = None,
        url_generator: UrlGeneratorProtocol | None = None,
    ) -> None:
        self._app: FastAPI = app
        self._container: ContainerProtocol | None = container
        self._kernel: HttpMiddlewareKernel | None = kernel
        self._url_generator: UrlGeneratorProtocol = (
            url_generator if url_generator is not None else UrlGenerator.get_instance()
        )


    def _resolve_handler(
        self,
        route: RouteDefinitionData,
    ) -> Callable[[HttpRequestProtocol], Awaitable[object]]:
        handler = route.handler
        if isinstance(handler, (list, tuple)):
            handler_values = cast(list[object] | tuple[object, ...], handler)
        else:
            handler_values = []
        if len(handler_values) == 2:
            controller_type = cast(type[object], handler_values[0])
            method_name = cast(str, handler_values[1])

            async def controller_handler(request: HttpRequestProtocol) -> object:
                if self._container is None:
                    controller = controller_type()
                else:
                    controller = self._container.make(controller_type)
                method = cast(Callable[..., object], getattr(controller, method_name))
                kwargs = self._request_parameters(request)
                try:
                    result = method(**kwargs)
                except TypeError:
                    result = method(request, **kwargs)
                if inspect.isawaitable(result):
                    return await cast(Awaitable[object], result)
                return result

            return controller_handler

        callback = cast(Callable[..., object], handler)

        async def callable_handler(request: HttpRequestProtocol) -> object:
            kwargs = self._request_parameters(request)
            try:
                result = callback(**kwargs)
            except TypeError:
                result = callback(request, **kwargs)
            if inspect.isawaitable(result):
                return await cast(Awaitable[object], result)
            return result

        return callable_handler


    def _request_parameters(self, request: HttpRequestProtocol) -> dict[str, object]:
        parameters = getattr(request, '_request', None)
        path_params = getattr(parameters, 'path_params', {})
        path_mapping = cast(Mapping[str, object], path_params)
        kwargs = dict(path_mapping) if isinstance(path_params, Mapping) else {}
        body = request.post()
        if isinstance(body, dict):
            body_values = cast(dict[str, object], body)
            kwargs.update(body_values)
        return kwargs


    def _resolve_middleware(
        self,
        route: RouteDefinitionData,
    ) -> list[type[HttpMiddleware]]:
        if self._kernel is None:
            return []
        middleware = list(route.middleware)
        if isinstance(route.handler, (list, tuple)):
            handler_values = cast(
                list[object] | tuple[object, ...],
                route.handler,
            )
        else:
            handler_values = []
        if len(handler_values) == 2:
            controller_type = handler_values[0]
            method_name = handler_values[1]
            if (
                isinstance(controller_type, type)
                and isinstance(method_name, str)
                and issubclass(controller_type, HttpController)
            ):
                middleware.extend(
                    controller_type.get_middleware_for_method(method_name)
                )
        return self._kernel.resolve_middleware_list(
            cast(list[str | type[HttpMiddleware]], middleware),
        )


    def _wrap_handler(
        self,
        handler: Callable[[HttpRequestProtocol], Awaitable[object]],
        middleware_classes: list[type[HttpMiddleware]],
    ) -> Callable[[StarletteRequest], Awaitable[object]]:
        async def wrapped(starlette_request: StarletteRequest) -> object:
            request = HttpRequest(starlette_request)
            await request.load_body()
            HttpRequestContext.set_request(request)
            try:
                if not middleware_classes:
                    return await handler(request)
                pipeline = HttpMiddlewarePipeline(
                    middleware_classes,
                    handler,
                    self._container,
                )
                response = await pipeline.send(request)
                await pipeline.terminate(request, response)
                return response
            finally:
                HttpRequestContext.clear_request()

        return wrapped


    @override
    def compile(
        self,
        routes: list[RouteDefinitionData],
        router: APIRouter | None = None,
    ) -> None:
        target = router or self._app.router
        for route in routes:
            fastapi_path, parameter_types = RouteParameter.parse(route.path)
            handler = self._resolve_handler(route)
            middleware = self._resolve_middleware(route)
            wrapped_handler = self._wrap_handler(handler, middleware)
            for method in route.methods:
                route_method = getattr(target, method.lower(), None)
                if not callable(route_method):
                    logger.warning('Unsupported HTTP method %s for route %s', method, route.path)
                    continue
                method_callback = cast(
                    Callable[[str], Callable[..., object]],
                    route_method,
                )
                _ = method_callback(fastapi_path)(wrapped_handler)
            if route.name is not None:
                self._url_generator.register(
                    route.name,
                    route.path,
                    route.methods,
                    parameter_types,
                )
