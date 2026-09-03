from __future__ import annotations

import inspect
from abc import ABC, abstractmethod
from typing import override

from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.contextual_attribute_protocol import (
    ContextualAttributeProtocol,
)


class ContextualAttribute(ContextualAttributeProtocol, ABC):
    @staticmethod
    @override
    @abstractmethod
    def resolve(
        attribute: object,
        container: ContainerProtocol,
        parameter: inspect.Parameter,
    ) -> object:
        raise NotImplementedError
