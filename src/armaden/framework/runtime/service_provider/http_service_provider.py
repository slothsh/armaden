from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import cast, override

from fastapi import APIRouter, FastAPI
from returns.pipeline import is_successful
from returns.result import Success

from armaden.framework.protocols.application_protocol import ApplicationProtocol
from armaden.framework.protocols.configuration_protocol import ConfigurationProtocol
from armaden.framework.protocols.route_registrar_protocol import RouteRegistrarProtocol
from armaden.framework.protocols.supervisor_protocol import SupervisorProtocol
from armaden.framework.protocols.url_generator_protocol import UrlGeneratorProtocol
from armaden.framework.runtime.application.module_loader import ModuleLoader
from armaden.framework.runtime.http.authentication import AuthenticationManager
from armaden.framework.runtime.http.authentication.middleware import (
    AuthenticationMiddleware,
    AuthenticationWithBasicMiddleware,
    AuthenticationWithHeaderMiddleware,
    AuthenticationWithTokenMiddleware,
)
from armaden.framework.runtime.http.middleware.http_middleware_kernel import HttpMiddlewareKernel
from armaden.framework.runtime.http.default_api import DefaultApi
from armaden.framework.runtime.http.routing.route_compiler import RouteCompiler
from armaden.framework.runtime.http.url_generator import UrlGenerator
from armaden.framework.runtime.http.routing.route_registrar import RouteRegistrar
from armaden.framework.runtime.service_provider.service_provider import ServiceProvider
from armaden.framework.runtime.supervisor.task.task_builder import TaskBuilder
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraphData
from armaden.framework.types.result import Result


logger = logging.getLogger(__name__)


class HttpServiceProvider(ServiceProvider):
    name: str = 'http'


    @override
    def register(self) -> Result[None]:
        self.app.singleton(AuthenticationManager, AuthenticationManager)
        return Success(None)


    @override
    def boot(self) -> Result[None]:
        application = cast(
            ApplicationProtocol[TaskGraphData],
            self.app.make(ApplicationProtocol),
        )
        middleware_kernel = HttpMiddlewareKernel(application)
        middleware_kernel.bootstrap()
        middleware_kernel.middleware = [
            *middleware_kernel.middleware,
            AuthenticationMiddleware,
        ]
        middleware_kernel.route_middleware.update({
            'authentication': AuthenticationMiddleware,
            'authentication.basic': AuthenticationWithBasicMiddleware,
            'authentication.header': AuthenticationWithHeaderMiddleware,
            'authentication.token': AuthenticationWithTokenMiddleware,
        })

        configuration = cast(
            ConfigurationProtocol,
            self.app.make(ConfigurationProtocol),
        )
        authentication_config = configuration.get('auth', {})
        authentication_settings: Mapping[str, object]
        if isinstance(authentication_config, Mapping):
            authentication_settings = cast(
                Mapping[str, object],
                authentication_config,
            )
        else:
            authentication_settings = {}
        authentication_manager = cast(
            AuthenticationManager,
            self.app.make(AuthenticationManager),
        )
        authentication_manager.bootstrap(authentication_settings)

        default_api = DefaultApi()
        api_app = default_api.app
        url_generator = UrlGenerator.get_instance()
        compiler = RouteCompiler(
            api_app,
            middleware_kernel,
            self.app,
            url_generator,
        )
        task = (
            TaskBuilder()
            .name('http_api')
            .description('HTTP API and FastAPI application runtime')
            .on_initialize(default_api.initialize)
            .on_run(default_api.run)
            .on_shutdown(default_api.shutdown)
            .on_status(default_api.status)
            .exclusive_thread()
            .long_running()
            .ready_timeout(30.0)
            .build()
        )
        supervisor = cast(
            SupervisorProtocol[TaskGraphData],
            self.app.make(SupervisorProtocol),
        )
        _ = supervisor.submit([task])

        _ = self.app.instance(APIRouter, api_app.router)
        _ = self.app.instance(FastAPI, api_app)
        route_registrar = RouteRegistrar.get_instance()
        _ = self.app.instance(HttpMiddlewareKernel, middleware_kernel)
        _ = self.app.instance(RouteRegistrarProtocol, route_registrar)
        _ = self.app.instance(UrlGeneratorProtocol, url_generator)
        _ = self.app.instance('api', api_app)
        _ = self.app.instance('http_kernel', middleware_kernel)
        _ = self.app.instance('router', api_app.router)

        routes_result = ModuleLoader.try_discover_user_modules('routes')
        if not is_successful(routes_result):
            logger.warning('Failed to load user route modules: %s', routes_result.failure())
        routes = route_registrar.get_routes()
        if routes:
            compiler.compile(routes, api_app.router)
            logger.info('Compiled %d routes', len(routes))
        route_registrar.clear()
        return Success(None)
