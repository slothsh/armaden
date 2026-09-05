from __future__ import annotations

import importlib
import os
from enum import StrEnum
from pathlib import Path
from typing import Callable, cast, override

from returns.result import Failure, Success

from armaden.framework.runtime.error.error import Error
from armaden.framework.protocols.environment_protocol import EnvironmentProtocol
from armaden.framework.types.result import Result


class Environment(EnvironmentProtocol):
    def __init__(self, default: str = 'local') -> None:
        self._environment: str = default


    @property
    @override
    def environment(self) -> str:
        return self._environment


    @override
    def get(self, name: str, default: str | None = None) -> str | None:
        return os.getenv(name, default)


    def _load_file(self, path: Path) -> Result[None]:
        try:
            module = importlib.import_module('dotenv')
            load_dotenv = cast(
                Callable[[str], object],
                getattr(module, 'load_dotenv'),
            )
            _ = load_dotenv(str(path))
            return Success(None)
        except Exception as exception:
            return Failure(Error(EnvironmentError.DOTENV_LOAD_FAILED, details={
                'path': path,
                'exception': exception,
            }))


    @override
    def initialize(self) -> Result[None]:
        if environment := os.getenv('APP_ENV'):
            self._environment = environment
        if not self._environment:
            return Failure(Error(EnvironmentError.INVALID_ENVIRONMENT))

        patterns = (
            f'.env.{self._environment}',
            f'.env.*.{self._environment}',
        )
        explicit_files = [
            path
            for pattern in patterns
            for path in Path('.').glob(pattern)
            if path.is_file()
        ]
        for path in explicit_files:
            result = self._load_file(path)
            if isinstance(result, Failure):
                return result
        if explicit_files:
            return Success(None)

        default_file = Path('.env')
        if default_file.is_file():
            return self._load_file(default_file)
        return Failure(Error(EnvironmentError.MISSING_DOTENV, details={
            'environment': self._environment,
        }))


class EnvironmentError(StrEnum):
    DOTENV_LOAD_FAILED = 'an environment file could not be loaded'
    INVALID_ENVIRONMENT = 'the application environment is invalid'
    MISSING_DOTENV = 'no dotenv file was found for the application environment'