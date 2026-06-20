import os
from enum import StrEnum
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, List, Mapping, Tuple, Type, TypeVar

from returns.result import Failure, Success

from framework.errors.error import Error
from framework.utils.types import Result

T = TypeVar("T")


class ModuleLoader:
    @classmethod
    def try_load_user_application(cls, *, inherits: Type[T]) -> Result[T | None]:
        try:
            _ = inherits
            app_directory = os.getenv('APP_DIR')

            if not app_directory:
                return Success(None)

            module_directory = Path(app_directory).absolute()
            module_path = module_directory / 'application.py'

            specification = spec_from_file_location('Application', module_path)

            if not specification or not specification.loader:
                return Failure(Error(ModuleLoaderError.USER_APP_INVALID_PATH, details={
                    'path': module_path,
                    'directory': module_directory
                }))

            module = module_from_spec(specification)

            specification.loader.exec_module(module)

            user_application: T = module.Application

            return Success(user_application)
        except Exception as exception:
            return Failure(Error(ModuleLoaderError.USER_APP_LOAD_EXCEPTION, details={
                'exception': exception
            }))


    @classmethod
    def try_load_user_config(cls) -> Result[List[Tuple[str, Callable[[], Mapping[str, Any]]]] | None]:
        try:
            app_directory = os.getenv('APP_DIR')

            if not app_directory:
                return Success(None)

            config_directory = Path(app_directory).absolute() / 'config'
            config_files = config_directory.glob('*.py')
            configs: List[Tuple[str, Callable[[], Mapping[str, Any]]]] | None = []

            for file in [file for file in config_files if file.is_file() and not file.name.startswith(('.', '_'))]:
                specification = spec_from_file_location('Config', file)

                if not specification or not specification.loader:
                    return Failure(Error(ModuleLoaderError.USER_CONFIG_INVALID_PATH, details={
                        'file': file,
                        'directory': config_directory
                    }))

                module = module_from_spec(specification)

                specification.loader.exec_module(module)

                config: Callable[[], Mapping[str, Any]] = getattr(module, 'config')

                if callable(config):
                    configs.append((file.stem, config))

            return Success(configs)
        except Exception as exception:
            return Failure(Error(ModuleLoaderError.USER_APP_LOAD_EXCEPTION, details={
                'exception': exception
            }))


    @classmethod
    def try_import_module(cls, name: str, package: str | None = None) -> Result[ModuleType]:
        try:
            return Success(import_module(name, package))
        except Exception as exception:
            return Failure(Error(ModuleLoaderError.LOAD_MODULE_FAILED, details={
                'name': name,
                'package': package,
                'exception': exception
            }))


# -- Internal Types -----------------------------------------------------------

class ModuleLoaderError(StrEnum):
    USER_APP_APP_DIR_NOT_DEFINED = "the user app environment variable is not defined"
    USER_APP_LOAD_EXCEPTION = "an exception occurred while trying to load the user app from the host system"
    USER_APP_INVALID_PATH = "the provided path to the user application is invalid"
    USER_CONFIG_INVALID_PATH = "the provided path to the user configuration is invalid"
    LOAD_MODULE_FAILED = "failed to load module from specified path"
    LOAD_INVALID_PATH = "the provided path to the is invalid"
