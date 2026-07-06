from returns.pipeline import is_successful
from returns.result import Success

from armaden.framework.classes.service_provider import ServiceProvider
from armaden.framework.classes.task import TaskBuilder
from armaden.framework.facades import App
from armaden.framework.utils.types import Result
from armaden.framework.runtime.module_loader import ModuleLoader

from armaden.framework.runtime.services.default_api import DefaultApi

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class HttpServiceProvider(ServiceProvider):
    name = 'http'

    def register(self) -> Result[None]:
        return Success(None)

    def boot(self) -> Result[None]:
        default_api = DefaultApi()

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
        App.supervisor().add_task(task)

        App.instance('api', default_api.app)
        App.instance('router', default_api.app.router)

        routes_directory = Path(__file__).absolute().parent.parent / 'http' / 'routes'
        route_files = routes_directory.glob('*.py')

        for file in [
            file for file in route_files
            if file.is_file() and not file.name.startswith(('.', '_'))
        ]:
            if not is_successful(
                result := ModuleLoader.try_import_module(
                    f"armaden.framework.runtime.http.routes.{file.stem}"
                )
            ):
                logger.error(result.failure)

        return Success(None)
