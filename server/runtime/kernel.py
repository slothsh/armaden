import asyncio
from pathlib import Path
from typing import Any, Dict, Self, TypeVar, cast
from dotenv import load_dotenv
from enum import StrEnum
import logging
import os
import sys
from glob import glob

from returns.pipeline import is_successful
from returns.result import Failure, Success

from framework.protocols import HandleManagerInterface, SupervisorInterface, ServiceManagerInterface
from framework.protocols.application import ApplicationInterface
from framework.enums.health_status import HealthStatus
from framework.utils.dictionary import Dictionary
from framework.utils.types import Result
from framework.errors import Error, GenericError
from .default_application import DefaultApplication
from .module_loader import ModuleLoader
from .supervisor import Supervisor
from .service_manager import ServiceManager
from .handle_manager import HandleManager

logger = logging.getLogger('runtime.kernel')


class Kernel:
    def __init__(self) -> None:
        global HANDLE_MANAGER
        HANDLE_MANAGER = HandleManager()

        HANDLE_MANAGER.register_handles({
            'app': self,
            'event_loop': asyncio.new_event_loop()
        })

        self._status = KernelStatus.NOT_READY
        self._app_env = 'local'
        self._config: Dict[str, Any] = {}

        self._supervisor: SupervisorInterface = Supervisor(HANDLE_MANAGER.handle('event_loop').unwrap())
        self._service_manager: ServiceManagerInterface = ServiceManager()
        self._user_app: ApplicationInterface = DefaultApplication()


    @staticmethod
    def bootstrap() -> Result[None]:
        try:
            # Initialize essentials
            if not is_successful(Kernel._initialize_logging()):
                raise KernelException('Could not successfully initialize logging during application bootstrap')

            # Create the runtime engine
            kernel = Kernel()
            from framework.facades._registry import set_kernel
            set_kernel(kernel)

            # Load the user application
            user_app_result = ModuleLoader.try_load_user_application()
            if is_successful(user_app_result) and (cls := user_app_result.unwrap()):
                if issubclass(cls, ApplicationInterface):
                    logger.info("Successfully loaded user application: %s", cls.__name__)
                    kernel._user_app = cls()
                else:
                    logger.warning("User Application class %s does not implement ApplicationInterface; using DefaultApplication", cls)
            elif not is_successful(user_app_result):
                logger.warning(user_app_result.failure())
                logger.warning("Using the default application as a fallback")

            # Initialize everything else
            if not is_successful(kernel._initialize_environment()):
                logger.warning("The application's environment was not successfully initialized, this is not an issue if you did not provide .env file for your application")
            if not is_successful(kernel._initialize_configs()):
                raise KernelException("The application's configuration files could not be successfully initialized")

            # Update application status
            kernel._status = KernelStatus.READY
            logger.info('Application successfully bootstrapped with status: %s', kernel._status)

            return asyncio.run(kernel(), loop_factory=kernel.event_loop)
        except (KeyboardInterrupt, SystemExit):
            return Success(None)
        except Exception as exception:
            return Failure(Error(GenericError.EXCEPTION, details={ 'exception': exception }))
        except:
            return Failure(Error(GenericError.UNKNOWN))


    async def __call__(self) -> Result[None]:
        self._user_app.configure(self._service_manager, self._supervisor)

        if not is_successful(result := self._user_app.boot()):
            logger.error("Could not boot user application: %s", result.failure())
            return result

        if not is_successful(result := await self._service_manager.initialize()):
            return result

        if not is_successful(result := await self._supervisor.initialize()):
            return result

        if not is_successful(result := await self._supervisor.run()):
            return result

        return Success(None)


    def version(self) -> str:
        from importlib import metadata
        try:
            return metadata.version('server')
        except metadata.PackageNotFoundError:
            return '0.0.0'


    def config(self, key: str, default: Any | None = None) -> Any:
        value = self._config

        for key in key.split("."):
            value = value[key]

        if value is None:
            return default

        return value


    async def status(self) -> Result[Dict[str, Any]]:
        def handle_result(results: Dict[str, Result[Dict[str, Any]]]) -> Dict[str, Any]:
            status: Dict[str, Any] = {}

            for name, result in results.items():
                if not is_successful(result):
                    logger.warning(result.failure())
                    status[name] = { 'status': HealthStatus.UNAVAILABLE }
                    continue

                status[name] = result.unwrap()

            return status

        service_statuses = { service.name: handle_result(result) for service in self._service_manager.services for result in await service.status() }
        app_degraded = Dictionary.has('status', lambda value: value != HealthStatus.OK, [
            *service_statuses.values()
        ])

        user_status_result = await self._user_app.status()
        if is_successful(user_status_result):
            user_status = user_status_result.unwrap()
        else:
            user_status = {}
            logger.warning(user_status_result.failure())

        return Success({
            'status': HealthStatus.DEGRADED if app_degraded else HealthStatus.OK,
            'services': service_statuses,
            **user_status,
        })


    @classmethod
    def handle_manager(cls) -> HandleManagerInterface:
        global HANDLE_MANAGER
        if not HANDLE_MANAGER:
            raise KernelException("The global handle manager is not available. Did you bootstrap the application?")
        return HANDLE_MANAGER


    @classmethod
    def instance(cls) -> Self:
        return cast(Self, cls.handle_manager().handle('app').unwrap())


    @classmethod
    def event_loop(cls) -> asyncio.AbstractEventLoop:
        return cast(asyncio.AbstractEventLoop, cls.handle_manager().handle('event_loop').unwrap())


    @property
    def service_manager(self) -> ServiceManagerInterface:
        return self._service_manager


    @property
    def supervisor(self) -> SupervisorInterface:
        return self._supervisor



    # -- Initializers ---------------------------------------------------------

    @classmethod
    def _initialize_logging(cls) -> Result[None]:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s][%(name)s][%(threadName)s]: %(message)s",
            stream=sys.stdout,
        )

        return Success(None)


    def _initialize_environment(self) -> Result[None]:
        if app_env := os.getenv('APP_ENV'):
            self._app_env = app_env

        if not self._app_env:
            return Failure(Error(KernelError.INVALID_DEFAULT_ENVIRONMENT))

        logger.info("Loading environment configuration for `%s`", self._app_env)

        # Check env files in order
        env_file_patterns = [
            f".env.{self._app_env}",
            f".env.*.{self._app_env}",
        ]

        found_explicit = False
        for pattern in env_file_patterns:
            paths = glob(pattern)
            if len(paths) > 0:
                found_explicit = True

            for path in paths:
                logger.info("Overlaying environment file: %s", path)
                load_dotenv(Path(path).absolute())

        if found_explicit:
            return Success(None)

        default_env = Path('.env').absolute()
        if default_env.is_file():
            logger.info("Loading environment file: %s", default_env)
            load_dotenv(default_env)
            return Success(None)

        return Failure(Error(KernelError.MISSING_DOTENV))


    def _initialize_configs(self) -> Result[None]:
        if not __package__:
            return Failure(Error(KernelError.INVALID_PACKAGE_NAME))

        # Load default configuration first
        config_directory = Path(__file__).absolute().parent / 'config'
        config_files = config_directory.glob('*.py')

        for file in [file for file in config_files if file.is_file() and not file.name.startswith(('.', '_'))]:
            if not is_successful(result := ModuleLoader.try_import_module(f"{__package__}.config.{file.stem}")):
                return result.map(lambda _: None)

            config = getattr(result.unwrap(), 'config')
            if callable(config):
                self._config[file.stem] = config()
            else:
                return Failure(Error(KernelError.CONFIG_MODULE_NOT_CALLABLE, details={
                    'directory': config_directory,
                    'file': file,
                }))

        # Load user configuration
        if not is_successful(result := ModuleLoader.try_load_user_config()):
            return result.map(lambda _: None)

        if not (result := result.unwrap()):
            return Success(None)

        for (key, config) in result:
            if key in self._config:
                self._config[key].update(config())
                continue
            self._config[key] = config()

        return Success(None)


# -- Internal Types -----------------------------------------------------------

T = TypeVar("T", bound=Kernel)
U = TypeVar("U", bound=Kernel)


class KernelStatus(StrEnum):
    NOT_READY = 'NOT_READY'
    READY = 'READY'


class KernelException(Exception):
    pass


class KernelError(StrEnum):
    MISSING_DOTENV = 'no .env file was found in the working directory of the application'
    INVALID_DEFAULT_ENVIRONMENT = 'the application has no default environment configured'
    INVALID_PACKAGE_NAME = "the application's package name is not defined"
    CONFIG_MODULE_NOT_CALLABLE = "the imported configuration factory method is not callable"
