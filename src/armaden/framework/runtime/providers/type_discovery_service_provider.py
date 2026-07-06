import inspect
import logging
from abc import ABC
from enum import StrEnum
from typing import Dict, Tuple

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.classes.service_provider import ServiceProvider
from armaden.framework.errors.error import Error
from armaden.framework.facades import config
from armaden.framework.protocols.application import ApplicationInterface
from armaden.framework.protocols.supervisor import SupervisorInterface
from armaden.framework.runtime.module_loader import ModuleLoader
from armaden.framework.utils.types import Result

logger = logging.getLogger(__name__)


# -- Interfaces that must never be auto-bound by discovery --------------------

EXCLUDED_INTERFACES = frozenset({
    ApplicationInterface,
    SupervisorInterface,
})


class TypeDiscoveryServiceProvider(ServiceProvider):
    name = 'discovery'

    def register(self) -> Result[None]:
        paths = config('app.discovery.paths', ['app'])
        seen: Dict[type, Tuple[str, str]] = {}

        for path in paths:
            result = ModuleLoader.try_discover_user_modules(path)
            if not is_successful(result):
                logger.error("Type discovery failed for path '%s': %s", path, result.failure())
                return result.map(lambda _: None)

            for module in result.unwrap():
                for cls in self._declared_classes(module):
                    if inspect.isabstract(cls):
                        continue

                    bind_result = self._bind_class(cls, module, seen)
                    if not is_successful(bind_result):
                        return bind_result

        return Success(None)

    def _declared_classes(self, module):
        return [
            obj for _, obj in inspect.getmembers(module, inspect.isclass)
            if obj.__module__ == module.__name__
        ]

    def _bind_class(self, cls, module, seen: Dict[type, Tuple[str, str]]) -> Result[None]:
        file_location = getattr(module, '__file__', '<unknown>')

        for base in cls.__mro__[1:]:
            if base in (ABC, object) or not inspect.isabstract(base):
                continue

            if base in EXCLUDED_INTERFACES:
                logger.error(
                    "User type [%s] (%s) attempted to bind excluded framework interface [%s]",
                    cls.__name__,
                    file_location,
                    base.__name__,
                )
                return Failure(Error(TypeDiscoveryError.EXCLUDED_INTERFACE_BINDING, details={
                    'class': cls.__name__,
                    'interface': base.__name__,
                    'file': file_location,
                }))

            if base in seen:
                original_name, original_file = seen[base]
                logger.warning(
                    "Duplicate implementation for interface [%s]: [%s] (%s) ignored; "
                    "keeping first-discovered [%s] (%s)",
                    base.__name__,
                    cls.__name__,
                    file_location,
                    original_name,
                    original_file,
                )
                continue

            self._container.bind(base, cls, shared=True)
            seen[base] = (cls.__name__, file_location)

        self._container.bind(cls, cls)
        return Success(None)


# -- Internal Types -----------------------------------------------------------

class TypeDiscoveryError(StrEnum):
    EXCLUDED_INTERFACE_BINDING = "a user type attempted to bind an excluded framework interface"
