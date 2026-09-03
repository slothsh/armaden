_BOOTSTRAP_APPLICATION = """from returns.result import Success
from armaden.framework.application import Application as ApplicationBase
from armaden.framework.utils.types import Result


class Application(ApplicationBase):
    def boot(self) -> Result[None]:
        # TODO: Register services, bind tasks, or configure the container here.
        return Success(None)
"""


_BOOTSTRAP_PROVIDERS = """from typing import List
from armaden.framework.classes.service_provider import ServiceProvider
from app.providers.app_service_provider import AppServiceProvider


def providers() -> List[ServiceProvider]:
    return [AppServiceProvider]
"""


_APP_SERVICE_PROVIDER = """from returns.result import Success
from armaden.framework.classes.service_provider import ServiceProvider
from armaden.framework.classes.task import TaskBuilder
from armaden.framework.facades import App
from armaden.framework.utils.types import Result


class AppServiceProvider(ServiceProvider):
    name = 'app'

    def register(self) -> Result[None]:
        # TODO: Register bindings on the service container.
        return Success(None)

    def boot(self) -> Result[None]:
        # TODO: Build and register tasks with the supervisor.
        #
        # Example:
        #   task = (
        #       TaskBuilder()
        #       .name('my_task')
        #       .on_initialize(self.initialize)
        #       .on_run(self.run)
        #       .build()
        #   )
        #   App.supervisor().add_task(task)
        return Success(None)
"""


_CONFIG_APP = """from armaden.framework.utils.env import Env


def config():
    return {{
        'name': Env.string('APP_NAME', '{name}'),
        'description': Env.string('APP_DESCRIPTION', 'An Armaden-powered application'),
    }}
"""


_ENV = """APP_DIR=.
APP_NAME={name}
APP_ENV=local
API_ADDRESS=0.0.0.0
API_PORT=8888
"""


class Templates:
    @staticmethod
    def bootstrap_application() -> str:
        return _BOOTSTRAP_APPLICATION

    @staticmethod
    def bootstrap_providers() -> str:
        return _BOOTSTRAP_PROVIDERS

    @staticmethod
    def app_service_provider() -> str:
        return _APP_SERVICE_PROVIDER

    @staticmethod
    def config_app(name: str) -> str:
        return _CONFIG_APP.format(name=name)

    @staticmethod
    def env(name: str) -> str:
        return _ENV.format(name=name)
