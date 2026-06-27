import logging

from pathlib import Path
from returns.pipeline import is_successful
from returns.result import Success

from framework.classes.service_provider import ServiceProvider
from framework.utils.types import Result
from runtime.module_loader import ModuleLoader

from .default_api import DefaultApi

from framework.facades import app

logger = logging.getLogger(__name__)


class DefaultApiServiceProvider(ServiceProvider):
    name = 'api'

    def register(self) -> Result[None]:
        return Success(None)

    def boot(self) -> Result[None]:
        default_api = DefaultApi()

        app().supervisor.with_server(default_api)

        app().container.instance('api', default_api.app)
        app().container.instance('router', default_api.app.router)

        routes_directory = Path(__file__).absolute().parent.parent / 'http' / 'routes'
        route_files = routes_directory.glob('*.py')

        for file in [file for file in route_files if file.is_file() and not file.name.startswith(('.', '_'))]:
            if not is_successful(result := ModuleLoader.try_import_module(f"runtime.http.routes.{file.stem}")):
                logger.error(result.failure)

        return Success(None)
