from __future__ import annotations

from typing import Protocol

from armaden.framework.protocols.container_protocol import ContainerProtocol


class ContainerInstanceProtocol(Protocol):
    @staticmethod
    def get_instance() -> ContainerProtocol: ...

    @staticmethod
    def set_instance(
        container: ContainerProtocol | None = None,
    ) -> ContainerProtocol | None: ...
