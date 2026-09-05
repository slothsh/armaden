from collections.abc import Callable, Mapping
from types import ModuleType
from typing import Protocol

from armaden.framework.protocols.service_provider_protocol import ServiceProviderProtocol
from armaden.framework.types.result import Result


type ConfigFactory = Callable[[], Mapping[str, object]]


class ModuleLoaderProtocol(Protocol):
    @classmethod
    def try_discover_user_modules(cls, subdir: str) -> Result[list[ModuleType]]: ...

    @classmethod
    def try_import_module(
        cls,
        name: str,
        package: str | None = None,
    ) -> Result[ModuleType]: ...

    @classmethod
    def try_load_runtime_config(
        cls,
    ) -> Result[list[tuple[str, ConfigFactory]]]: ...

    @classmethod
    def try_load_user_app_provider(
        cls,
    ) -> Result[list[type[ServiceProviderProtocol]] | None]: ...

    @classmethod
    def try_load_user_application(cls) -> Result[type[object] | None]: ...

    @classmethod
    def try_load_user_config(
        cls,
    ) -> Result[list[tuple[str, ConfigFactory]] | None]: ...