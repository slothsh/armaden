from __future__ import annotations

import inspect
from typing import cast, override

from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.runtime.container.contextual_attribute import ContextualAttribute


class TagContextualAttribute(ContextualAttribute):
    def __init__(self, tag: str) -> None:
        self.tag: str = tag


    @staticmethod
    @override
    def resolve(
        attribute: object,
        container: ContainerProtocol,
        parameter: inspect.Parameter,
    ) -> list[object]:
        _ = parameter
        tag = cast(TagContextualAttribute, attribute)
        return container.tagged(tag.tag)
