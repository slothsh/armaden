import os
from enum import StrEnum
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from typing import Type, TypeVar

from returns.result import Failure, Success

from framework.errors.error import Error
from framework.utils.types import Result

T = TypeVar("T")


class ModuleLoader:
    @classmethod
    def try_load_user_application(cls, _: Type[T]) -> Result[T | None]:
        try:
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


# -- Internal Types -----------------------------------------------------------

class ModuleLoaderError(StrEnum):
    USER_APP_APP_DIR_NOT_DEFINED = "the user app environment variable is not defined"
    USER_APP_LOAD_EXCEPTION = "an exception occurred while trying to load the user app from the host system"
    USER_APP_INVALID_PATH = "the provided path to the  is invalid"
