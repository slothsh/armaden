import os
import sys
from enum import StrEnum
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, List, Mapping, Tuple, TypeVar

from returns.result import Failure, Success

from armaden.framework.errors.error import Error
from armaden.framework.utils.types import Result

T = TypeVar("T")


class ModuleLoader:
    @classmethod
    def try_load_user_application(cls) -> Result[Any | None]:
        try:
            app_directory = os.getenv('APP_DIR')

            if not app_directory:
                return Success(None)

            module_directory = Path(app_directory).absolute()
            module_path = module_directory / 'bootstrap' / 'application.py'

            specification = spec_from_file_location('Application', module_path)

            if not specification or not specification.loader:
                return Failure(Error(ModuleLoaderError.USER_APP_INVALID_PATH, details={
                    'path': module_path,
                    'directory': module_directory
                }))

            module = module_from_spec(specification)

            specification.loader.exec_module(module)

            user_application = module.Application

            return Success(user_application)
        except Exception as exception:
            return Failure(Error(ModuleLoaderError.USER_APP_LOAD_EXCEPTION, details={
                'exception': exception
            }))

    @classmethod
    def try_load_user_app_provider(cls) -> Result[Any | None]:
        try:
            app_directory = os.getenv('APP_DIR')

            if not app_directory:
                return Success(None)

            module_directory = Path(app_directory).absolute()
            provider_path = module_directory / 'bootstrap' / 'providers.py'

            if not provider_path.is_file():
                return Success(None)

            module_dir_str = str(module_directory)
            sys.path.insert(0, module_dir_str)

            try:
                specification = spec_from_file_location('providers', provider_path)

                if not specification or not specification.loader:
                    return Failure(Error(ModuleLoaderError.USER_PROVIDER_INVALID_PATH, details={
                        'path': provider_path,
                        'directory': module_directory
                    }))

                module = module_from_spec(specification)
                specification.loader.exec_module(module)

                providers_func = getattr(module, 'providers', None)
                if not callable(providers_func):
                    return Success(None)

                return Success(providers_func())
            finally:
                if module_dir_str in sys.path:
                    sys.path.remove(module_dir_str)
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
    def try_discover_user_modules(cls, subdir: str) -> Result[List[ModuleType]]:
        app_directory = os.getenv('APP_DIR')

        if not app_directory:
            return Success([])

        module_directory = Path(app_directory).absolute()
        scan_root = module_directory / subdir

        if not scan_root.is_dir():
            return Failure(Error(ModuleLoaderError.USER_DISCOVERY_INVALID_PATH, details={
                'path': scan_root,
                'subdir': subdir,
                'directory': module_directory
            }))

        files = sorted(
            (
                file for file in scan_root.rglob('*.py')
                if file.is_file() and not file.name.startswith(('.', '_'))
            ),
            key=lambda file: str(file),
        )

        module_dir_str = str(module_directory)
        sys.path.insert(0, module_dir_str)

        modules: List[ModuleType] = []
        try:
            for file in files:
                relative = file.relative_to(module_directory).with_suffix('')
                dotted_name = '.'.join(relative.parts)
                try:
                    modules.append(import_module(dotted_name))
                except Exception as exception:
                    return Failure(Error(ModuleLoaderError.USER_DISCOVERY_LOAD_EXCEPTION, details={
                        'name': dotted_name,
                        'file': file,
                        'exception': exception
                    }))
        finally:
            if module_dir_str in sys.path:
                sys.path.remove(module_dir_str)

        return Success(modules)

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
    USER_PROVIDER_INVALID_PATH = "the provided path to the user provider is invalid"
    USER_CONFIG_INVALID_PATH = "the provided path to the user configuration is invalid"
    USER_DISCOVERY_INVALID_PATH = "the discovery directory path is invalid"
    USER_DISCOVERY_LOAD_EXCEPTION = "an exception occurred while importing a user module during type discovery"
    LOAD_MODULE_FAILED = "failed to load module from specified path"
    LOAD_INVALID_PATH = "the provided path to the is invalid"
