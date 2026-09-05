from __future__ import annotations

import inspect
import logging
from abc import ABC
from typing import cast, override

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.discovery_binder_protocol import (
    DiscoveryBinderProtocol,
)
from armaden.framework.runtime.container.tags import MultiImplementationTag
from armaden.framework.runtime.discovery.dto.discovery_settings_data import (
    DiscoverySettingsData,
)
from armaden.framework.runtime.discovery.exceptions.discovery_binder_error import (
    DiscoveryBinderError,
)
from armaden.framework.runtime.discovery.tags import (
    SharedBindingTag,
    SkipBindingTag,
    TransientBindingTag,
)
from armaden.framework.runtime.error.error import Error
from armaden.framework.types.result import Result

logger = logging.getLogger(__name__)


class DiscoveryBinder(DiscoveryBinderProtocol):
    def __init__(
        self,
        container: ContainerProtocol,
        settings: DiscoverySettingsData,
    ) -> None:
        self._container: ContainerProtocol = container
        self._settings: DiscoverySettingsData = settings


    @override
    def bind(self, classes: list[type[object]]) -> Result[None]:
        seen: dict[type, tuple[str, str]] = {}
        for cls in classes:
            result = self._bind_class(cls, seen)
            if not is_successful(result):
                return result
        return Success(None)


    def _bind_class(
        self,
        cls: type[object],
        seen: dict[type[object], tuple[str, str]],
    ) -> Result[None]:
        if issubclass(cls, SkipBindingTag):
            return Success(None)
        shared = self._shared_setting(cls)
        if self._settings.bind_self:
            self._container.bind(cls, cls, shared=shared)
        if not self._settings.bind_interfaces:
            return Success(None)
        return self._bind_interfaces(cls, shared, seen)


    def _bind_interfaces(
        self,
        cls: type[object],
        shared: bool,
        seen: dict[type[object], tuple[str, str]],
    ) -> Result[None]:
        bases = cast(tuple[type[object], ...], cls.__mro__)
        for base in bases[1:]:
            if base in (ABC, object) or not inspect.isabstract(base):
                continue
            if issubclass(base, MultiImplementationTag):
                continue
            if base in self._settings.excluded_interfaces:
                logger.error(
                    'Discovered type [%s] (%s) attempted to bind excluded interface [%s]',
                    cls.__name__,
                    cls.__module__,
                    base.__name__,
                )
                return Failure(Error(DiscoveryBinderError.EXCLUDED_INTERFACE_BINDING, details={
                    'class': cls.__name__,
                    'interface': base.__name__,
                    'module': cls.__module__,
                }))
            if base in seen:
                original_name, original_module = seen[base]
                logger.warning(
                    'Duplicate implementation for interface [%s]: [%s] (%s) ignored; '
                    + 'keeping first-discovered [%s] (%s)',
                    base.__name__,
                    cls.__name__,
                    cls.__module__,
                    original_name,
                    original_module,
                )
                continue
            self._container.bind(base, cls, shared=shared)
            seen[base] = (cls.__name__, cls.__module__)
        return Success(None)


    def _shared_setting(self, cls: type[object]) -> bool:
        if issubclass(cls, SharedBindingTag):
            return True
        if issubclass(cls, TransientBindingTag):
            return False
        return self._settings.shared
