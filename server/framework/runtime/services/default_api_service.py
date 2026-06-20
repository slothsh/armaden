import logging

from pathlib import Path
from returns.pipeline import is_successful
from returns.result import Success

from framework.runtime.module_loader import ModuleLoader

from .default_api import DefaultApi

from ..facades import app
from ...classes.service import Service
from ...utils.types import Result

logger = logging.getLogger(__name__)


class DefaultApiService(Service):
    name = 'api'
    
    def __call__(self) -> Result[None]:
        self.default_api = DefaultApi()

        app().supervisor.with_server(self.default_api)

        app().handle_manager().register_handles({
            'api': self.default_api.app,
            'router': self.default_api.app.router,
        })

        routes_directory = Path(__file__).absolute().parent.parent / 'http' / 'routes'
        route_files = routes_directory.glob('*.py')

        for file in [file for file in route_files if file.is_file() and not file.name.startswith(('.', '_'))]:
            logger.info("Importing %s", file)
            if not is_successful(result := ModuleLoader.try_import_module(f"..http.routes.{file.stem}", __package__)):
                logger.error(result.failure)

        return Success(None)
