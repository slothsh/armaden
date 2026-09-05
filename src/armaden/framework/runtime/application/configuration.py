from __future__ import annotations

from collections.abc import Mapping
from enum import StrEnum
from typing import cast, override

from returns.result import Failure, Success

from armaden.framework.runtime.error.error import Error
from armaden.framework.protocols.configuration_protocol import ConfigurationProtocol
from armaden.framework.support.dictionary import Dictionary
from armaden.framework.runtime.application.module_loader import ModuleLoader
from armaden.framework.types.result import Result


class Configuration(ConfigurationProtocol):
    def __init__(self) -> None:
        self._values: dict[str, object] = {}


    @override
    def all(self) -> Mapping[str, object]:
        return dict(self._values)


    @override
    def get(self, key: str, default: object | None = None) -> object | None:
        value: object = self._values
        try:
            for part in key.split('.'):
                if not isinstance(value, Mapping):
                    return default
                mapping = cast(Mapping[str, object], value)
                value = mapping[part]
        except KeyError:
            return default
        return value if value is not None else default


    @override
    def load(self) -> Result[None]:
        runtime_result = ModuleLoader.try_load_runtime_config()
        if isinstance(runtime_result, Failure):
            return runtime_result
        user_result = ModuleLoader.try_load_user_config()
        if isinstance(user_result, Failure):
            return user_result
        user_factories = user_result.unwrap() or []
        try:
            for name, factory in runtime_result.unwrap():
                self._values[name] = dict(factory())
            for name, factory in user_factories:
                user_configuration = factory()
                existing = self._values.get(name)
                if isinstance(existing, Mapping):
                    self._values[name] = Dictionary.merge(
                        cast(Mapping[str, object], existing),
                        user_configuration,
                    )
                else:
                    self._values[name] = dict(user_configuration)
        except Exception as exception:
            return Failure(Error(ConfigurationError.FACTORY_FAILED, details={
                'exception': exception,
            }))
        return Success(None)


class ConfigurationError(StrEnum):
    FACTORY_FAILED = 'a configuration factory failed to load'