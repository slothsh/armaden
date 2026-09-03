from __future__ import annotations

import inspect
from typing import Protocol

from armaden.framework.protocols.container_protocol import ContainerProtocol


class ContextualAttributeProtocol(Protocol):
    @staticmethod
    def resolve(
        attribute: object,
        container: ContainerProtocol,
        parameter: inspect.Parameter,
    ) -> object: ...
