from __future__ import annotations

import logging
from collections.abc import Mapping
from enum import StrEnum
from importlib import import_module
from typing import ClassVar, cast, override

from returns.result import Failure, Success

from armaden.framework.protocols.application_protocol import ApplicationProtocol
from armaden.framework.protocols.class_discovery_protocol import (
    ClassDiscoveryProtocol,
)
from armaden.framework.protocols.configuration_protocol import (
    ConfigurationProtocol,
)
from armaden.framework.protocols.discovery_binder_protocol import (
    DiscoveryBinderProtocol,
)
from armaden.framework.protocols.supervisor_protocol import SupervisorProtocol
from armaden.framework.runtime.discovery.class_discovery import ClassDiscovery
from armaden.framework.runtime.discovery.discovery_binder import DiscoveryBinder
from armaden.framework.runtime.discovery.dto.discovery_settings_data import (
    DiscoverySettingsData,
)
from armaden.framework.runtime.error.error import Error
from armaden.framework.runtime.service_provider.service_provider import (
    ServiceProvider,
)
from armaden.framework.types.result import Result

logger = logging.getLogger(__name__)


class DiscoveryServiceProvider(ServiceProvider):
    FRAMEWORK_EXCLUDED_INTERFACES: ClassVar[frozenset[type[object]]] = frozenset({
        ApplicationProtocol,
        SupervisorProtocol,
    })
    name: str = 'discovery'


    @override
    def boot(self) -> Result[None]:
        configuration = cast(
            ConfigurationProtocol,
            self._container.make(ConfigurationProtocol),
        )
        settings_result = self._parse_settings(configuration)
        if isinstance(settings_result, Failure):
            return settings_result
        settings = settings_result.unwrap()
        binder = DiscoveryBinder(self._container, settings)
        _ = self._container.instance(DiscoveryBinderProtocol, binder)

        if not settings.enabled:
            logger.debug('Class discovery is disabled')
            return Success(None)

        discovery = cast(
            ClassDiscoveryProtocol,
            self._container.make(ClassDiscoveryProtocol),
        )
        classes_result = discovery.discover(settings.paths)
        if isinstance(classes_result, Failure):
            return classes_result
        classes = classes_result.unwrap()
        bind_result = binder.bind(classes)
        if isinstance(bind_result, Failure):
            return bind_result
        logger.info(
            'Discovery bound %d user class(es) from %d path(s): %s',
            len(classes),
            len(settings.paths),
            ', '.join(settings.paths),
        )
        return Success(None)


    @override
    def register(self) -> Result[None]:
        self._container.singleton(ClassDiscoveryProtocol, ClassDiscovery)
        return Success(None)


    def _parse_settings(
        self,
        configuration: ConfigurationProtocol,
    ) -> Result[DiscoverySettingsData]:
        raw = configuration.get('app.discovery', {})
        discovery: Mapping[str, object] = (
            cast(Mapping[str, object], raw)
            if isinstance(raw, Mapping)
            else {}
        )
        enabled_value = discovery.get('enabled', False)
        paths_value = discovery.get('paths', [])
        paths_list: list[object] = (
            cast(list[object], paths_value)
            if isinstance(paths_value, list)
            else []
        )
        paths = [value for value in paths_list if isinstance(value, str)]
        raw_bind = discovery.get('bind', {})
        bind: Mapping[str, object] = (
            cast(Mapping[str, object], raw_bind)
            if isinstance(raw_bind, Mapping)
            else {}
        )
        excluded_result = self._resolve_excluded(bind)
        if isinstance(excluded_result, Failure):
            return excluded_result
        return Success(DiscoverySettingsData(
            bind_interfaces=self._bool_setting(bind, 'interfaces', True),
            bind_self=self._bool_setting(bind, 'self', True),
            enabled=enabled_value is True,
            excluded_interfaces=excluded_result.unwrap(),
            paths=paths,
            shared=self._bool_setting(bind, 'shared', True),
        ))


    def _bool_setting(
        self,
        mapping: Mapping[str, object],
        key: str,
        default: bool,
    ) -> bool:
        value = mapping.get(key, default)
        return value if isinstance(value, bool) else default


    def _resolve_excluded(
        self,
        bind: Mapping[str, object],
    ) -> Result[frozenset[type]]:
        raw_value = bind.get('excluded_interfaces', [])
        values: list[object] = (
            cast(list[object], raw_value)
            if isinstance(raw_value, list)
            else []
        )
        dotted_paths = [value for value in values if isinstance(value, str)]
        resolved: set[type] = set(self.FRAMEWORK_EXCLUDED_INTERFACES)
        for dotted in dotted_paths:
            module_name, separator, attribute = dotted.rpartition('.')
            if not separator or not module_name or not attribute:
                return Failure(Error(
                    DiscoveryProviderError.INVALID_EXCLUDED_INTERFACE,
                    details={'path': dotted},
                ))
            try:
                module = import_module(module_name)
                value = getattr(module, attribute)
            except (AttributeError, ImportError, ValueError) as exception:
                return Failure(Error(
                    DiscoveryProviderError.EXCLUDED_INTERFACE_RESOLUTION,
                    details={'path': dotted, 'exception': exception},
                ))
            if not isinstance(value, type):
                return Failure(Error(
                    DiscoveryProviderError.INVALID_EXCLUDED_INTERFACE,
                    details={'path': dotted},
                ))
            resolved.add(value)
        return Success(frozenset(resolved))


class DiscoveryProviderError(StrEnum):
    EXCLUDED_INTERFACE_RESOLUTION = 'an excluded discovery interface failed to resolve'
    INVALID_EXCLUDED_INTERFACE = 'an excluded discovery interface path is invalid'
