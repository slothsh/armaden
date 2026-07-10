from returns.result import Success

from armaden.framework.classes.service_provider import ServiceProvider
from armaden.framework.classes.task import TaskBuilder
from armaden.framework.utils.types import Result

from armaden.framework.runtime.http.middleware.kernel import HttpKernel
from armaden.framework.runtime.http.routing.route_registrar import RouteRegistrar
from armaden.framework.runtime.http.routing.route_compiler import RouteCompiler
from armaden.framework.runtime.services.default_api import DefaultApi
from armaden.framework.protocols.application import ApplicationInterface
from armaden.framework.runtime.http.auth import (
    AuthManager,
    Authenticate,
    AuthenticateWithBasic,
    AuthenticateWithHeader,
    AuthenticateWithToken,
)

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class HttpServiceProvider(ServiceProvider):
    name = 'http'

    def register(self) -> Result[None]:
        self._container.singleton(AuthManager, AuthManager)
        return Success(None)

    def boot(self) -> Result[None]:
        application = self._container.make(ApplicationInterface)
        kernel = HttpKernel(application)
        kernel.bootstrap()

        auth_config = self._container.make('app').config('auth', {})
        auth_manager = self._container.make(AuthManager)
        auth_manager.bootstrap(auth_config)

        kernel.middleware.append(Authenticate)

        kernel.route_middleware.update({
            'auth': Authenticate,
            'auth.basic': AuthenticateWithBasic,
            'auth.token': AuthenticateWithToken,
            'auth.header': AuthenticateWithHeader,
        })

        self._container.instance(HttpKernel, kernel)

        self._container.instance('http_kernel', kernel)

        default_api = DefaultApi()
        api_app = default_api.app
        compiler = RouteCompiler(api_app, kernel, container=self._container)

        task = (
            TaskBuilder()
            .name('http_api')
            .description('HTTP API and FastAPI application runtime')
            .on_initialize(default_api.initialize)
            .on_run(default_api.run)
            .on_shutdown(default_api.shutdown)
            .on_status(default_api.status)
            .exclusive_thread()
            .build()
        )
        self._container.make('app').supervisor.add_task(task)

        self._container.instance('api', api_app)
        self._container.instance('router', api_app.router)

        route_files_dir = Path(__file__).absolute().parent.parent / 'http' / 'routes'
        import importlib
        for file in [
            f for f in route_files_dir.glob('*.py')
            if f.is_file() and not f.name.startswith(('.', '_'))
        ]:
            try:
                importlib.import_module(f'armaden.framework.runtime.http.routes.{file.stem}')
            except ImportError as e:
                logger.warning('Failed to load route file %s: %s', file.name, e)

        registrar = RouteRegistrar.get_instance()
        routes = registrar.get_routes()
        if routes:
            compiler.compile(routes, api_app.router)
            logger.info('Compiled %d routes', len(routes))

        registrar.clear()
        return Success(None)
