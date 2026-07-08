from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any

from armaden.framework.classes.instance_container import ContextualAttribute

if TYPE_CHECKING:
    from armaden.framework.classes.instance_container import InstanceContainer


class Give(ContextualAttribute):
    def __init__(self, concrete: type) -> None:
        self.concrete = concrete

    @staticmethod
    def resolve(attribute: Give, container: InstanceContainer, parameter: inspect.Parameter) -> Any:
        return container.make(attribute.concrete)


class Config(ContextualAttribute):
    def __init__(self, key: str, default: Any = None) -> None:
        self.key = key
        self.default = default

    @staticmethod
    def resolve(attribute: Config, container: InstanceContainer, parameter: inspect.Parameter) -> Any:
        return container.make('app').config(attribute.key, attribute.default)


class Tag(ContextualAttribute):
    def __init__(self, tag: str) -> None:
        self.tag = tag

    @staticmethod
    def resolve(attribute: Tag, container: InstanceContainer, parameter: inspect.Parameter) -> Any:
        return container.tagged(attribute.tag)


_BUILTIN_ATTRIBUTES: dict[str, Any] = {
    'Give': Give.resolve,
    'Config': Config.resolve,
    'Tag': Tag.resolve,
}


def register_builtin_attributes(container) -> None:
    for name, handler in _BUILTIN_ATTRIBUTES.items():
        container.when_has_attribute(name, handler)
