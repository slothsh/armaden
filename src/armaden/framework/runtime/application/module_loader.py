from __future__ import annotations

import os
import sys
from collections.abc import Callable
from enum import StrEnum
from importlib import import_module
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
from typing import cast, override

from returns.result import Failure, Success

from armaden.framework.runtime.error.error import Error
from armaden.framework.protocols.module_loader_protocol import (
    ConfigFactory,
    ModuleLoaderProtocol,
)
from armaden.framework.protocols.service_provider_protocol import ServiceProviderProtocol
from armaden.framework.types.result import Result


class ModuleLoader(ModuleLoaderProtocol):
    @classmethod
    def _application_directory(cls) -> Path | None:
        app_directory = os.getenv('APP_DIR')
        if not app_directory:
            return None
        return Path(app_directory).absolute()


    @classmethod
    def _load_file_module(cls, name: str, path: Path) -> ModuleType:
        specification = spec_from_file_location(name, path)
        if specification is None or specification.loader is None:
            raise ModuleNotFoundError(f'Unable to load module from {path}')
        module = module_from_spec(specification)
        specification.loader.exec_module(module)
        return module


    @override
    @classmethod
    def try_discover_user_modules(cls, subdir: str) -> Result[list[ModuleType]]:
        try:
            module_directory = cls._application_directory()
            if module_directory is None:
                return Success([])
            scan_root = module_directory / subdir
            if not scan_root.is_dir():
                return Failure(Error(ModuleLoaderError.USER_DISCOVERY_INVALID_PATH, details={
                    'path': scan_root,
                    'subdir': subdir,
                    'directory': module_directory,
                }))

            files = sorted(
                (
                    file for file in scan_root.rglob('*.py')
                    if file.is_file() and not file.name.startswith(('.', '_'))
                ),
                key=str,
            )
            module_directory_string = str(module_directory)
            path_inserted = module_directory_string not in sys.path
            if path_inserted:
                sys.path.insert(0, module_directory_string)
            modules: list[ModuleType] = []
            try:
                for file in files:
                    relative = file.relative_to(module_directory).with_suffix('')
                    dotted_name = '.'.join(relative.parts)
                    try:
                        modules.append(import_module(dotted_name))
                    except Exception as exception:
                        return Failure(Error(
                            ModuleLoaderError.USER_DISCOVERY_LOAD_EXCEPTION,
                            details={
                                'name': dotted_name,
                                'file': file,
                                'exception': exception,
                            },
                        ))
            finally:
                if path_inserted:
                    sys.path.remove(module_directory_string)
            return Success(modules)
        except Exception as exception:
            return Failure(Error(
                ModuleLoaderError.USER_DISCOVERY_LOAD_EXCEPTION,
                details={'exception': exception},
            ))


    @override
    @classmethod
    def try_import_module(
        cls,
        name: str,
        package: str | None = None,
    ) -> Result[ModuleType]:
        try:
            return Success(import_module(name, package))
        except Exception as exception:
            return Failure(Error(ModuleLoaderError.LOAD_MODULE_FAILED, details={
                'name': name,
                'package': package,
                'exception': exception,
            }))


    @override
    @classmethod
    def try_load_runtime_config(
        cls,
    ) -> Result[list[tuple[str, ConfigFactory]]]:
        try:
            config_directory = Path(__file__).absolute().parent.parent / 'config'
            configs: list[tuple[str, ConfigFactory]] = []
            for file in sorted(config_directory.glob('*.py'), key=str):
                if not file.is_file() or file.name.startswith(('.', '_')):
                    continue
                module = cls._load_file_module('RuntimeConfig', file)
                config = getattr(module, 'config', None)
                if not callable(config):
                    return Failure(Error(
                        ModuleLoaderError.RUNTIME_CONFIG_INVALID_PATH,
                        details={'file': file, 'directory': config_directory},
                    ))
                configs.append((file.stem, cast(ConfigFactory, config)))
            return Success(configs)
        except Exception as exception:
            return Failure(Error(ModuleLoaderError.RUNTIME_CONFIG_LOAD_EXCEPTION, details={
                'exception': exception,
            }))


    @override
    @classmethod
    def try_load_user_app_provider(
        cls,
    ) -> Result[list[type[ServiceProviderProtocol]] | None]:
        try:
            module_directory = cls._application_directory()
            if module_directory is None:
                return Success(None)
            provider_path = module_directory / 'bootstrap' / 'providers.py'
            if not provider_path.is_file():
                return Success(None)

            module_directory_string = str(module_directory)
            path_inserted = module_directory_string not in sys.path
            if path_inserted:
                sys.path.insert(0, module_directory_string)
            try:
                module = cls._load_file_module('providers', provider_path)
                providers = getattr(module, 'providers', None)
                if not callable(providers):
                    return Success(None)
                provider_factory = cast(Callable[[], object], providers)
                provider_values_object = provider_factory()
                if not isinstance(provider_values_object, list):
                    return Failure(Error(
                        ModuleLoaderError.USER_APP_LOAD_EXCEPTION,
                        details={'path': provider_path, 'message': 'providers() must return a list'},
                    ))
                provider_values: list[object] = cast(list[object], provider_values_object)
                if not all(isinstance(provider, type) for provider in provider_values):
                    return Failure(Error(
                        ModuleLoaderError.USER_APP_LOAD_EXCEPTION,
                        details={'path': provider_path, 'message': 'providers() must return provider classes'},
                    ))
                provider_classes = [
                    cast(type[ServiceProviderProtocol], provider)
                    for provider in provider_values
                ]
                return Success(provider_classes)
            finally:
                if path_inserted:
                    sys.path.remove(module_directory_string)
        except Exception as exception:
            return Failure(Error(ModuleLoaderError.USER_APP_LOAD_EXCEPTION, details={
                'exception': exception,
            }))


    @override
    @classmethod
    def try_load_user_application(cls) -> Result[type[object] | None]:
        try:
            module_directory = cls._application_directory()
            if module_directory is None:
                return Success(None)
            application_path = module_directory / 'bootstrap' / 'application.py'
            module = cls._load_file_module('Application', application_path)
            application = getattr(module, 'Application', None)
            if not isinstance(application, type):
                return Failure(Error(
                    ModuleLoaderError.USER_APP_LOAD_EXCEPTION,
                    details={'path': application_path, 'message': 'Application must be a class'},
                ))
            return Success(application)
        except Exception as exception:
            return Failure(Error(ModuleLoaderError.USER_APP_LOAD_EXCEPTION, details={
                'exception': exception,
            }))


    @override
    @classmethod
    def try_load_user_config(
        cls,
    ) -> Result[list[tuple[str, ConfigFactory]] | None]:
        try:
            module_directory = cls._application_directory()
            if module_directory is None:
                return Success(None)
            config_directory = module_directory / 'config'
            configs: list[tuple[str, ConfigFactory]] = []
            for file in sorted(config_directory.glob('*.py'), key=str):
                if not file.is_file() or file.name.startswith(('.', '_')):
                    continue
                module = cls._load_file_module('Config', file)
                config = getattr(module, 'config', None)
                if not callable(config):
                    return Failure(Error(
                        ModuleLoaderError.USER_CONFIG_INVALID_PATH,
                        details={'file': file, 'directory': config_directory},
                    ))
                configs.append((file.stem, cast(ConfigFactory, config)))
            return Success(configs)
        except Exception as exception:
            return Failure(Error(ModuleLoaderError.USER_APP_LOAD_EXCEPTION, details={
                'exception': exception,
            }))


class ModuleLoaderError(StrEnum):
    LOAD_INVALID_PATH = 'the provided path to the is invalid'
    LOAD_MODULE_FAILED = 'failed to load module from specified path'
    RUNTIME_CONFIG_INVALID_PATH = 'the provided path to the runtime configuration is invalid'
    RUNTIME_CONFIG_LOAD_EXCEPTION = 'an exception occurred while loading runtime configuration'
    USER_APP_LOAD_EXCEPTION = 'an exception occurred while trying to load the user app from the host system'
    USER_APP_INVALID_PATH = 'the provided path to the user application is invalid'
    USER_APP_NOT_DEFINED = 'the user app environment variable is not defined'
    USER_CONFIG_INVALID_PATH = 'the provided path to the user configuration is invalid'
    USER_DISCOVERY_INVALID_PATH = 'the discovery directory path is invalid'
    USER_DISCOVERY_LOAD_EXCEPTION = 'an exception occurred while importing a user module during type discovery'
    USER_PROVIDER_INVALID_PATH = 'the provided path to the user provider is invalid'