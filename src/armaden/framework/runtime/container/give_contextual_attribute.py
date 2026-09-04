from __future__ import annotations

import inspect
from typing import cast, override

from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.runtime.container.contextual_attribute import ContextualAttribute


class GiveContextualAttribute(ContextualAttribute):
    def __init__(self, concrete: type[object]) -> None:
        self.concrete: type[object] = concrete


    @staticmethod
    @override
    def resolve(
        attribute: object,
        container: ContainerProtocol,
        parameter: inspect.Parameter,
    ) -> object:
        _ = parameter
        give = cast(GiveContextualAttribute, attribute)
        return container.make(give.concrete)
