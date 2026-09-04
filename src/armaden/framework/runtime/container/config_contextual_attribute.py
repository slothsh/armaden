from __future__ import annotations

import inspect
from typing import cast, override

from armaden.framework.protocols.configuration_protocol import ConfigurationProtocol
from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.runtime.container.contextual_attribute import ContextualAttribute


class ConfigContextualAttribute(ContextualAttribute):
    def __init__(self, key: str, default: object | None = None) -> None:
        self.default: object | None = default
        self.key: str = key


    @staticmethod
    @override
    def resolve(
        attribute: object,
        container: ContainerProtocol,
        parameter: inspect.Parameter,
    ) -> object | None:
        _ = parameter
        config = cast(ConfigContextualAttribute, attribute)
        configuration = cast(
            ConfigurationProtocol,
            container.make(ConfigurationProtocol),
        )
        return configuration.get(config.key, config.default)
