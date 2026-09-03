from __future__ import annotations

from typing import Protocol

from armaden.framework.protocols.container_protocol import ContainerProtocol


class BoundMethodProtocol(Protocol):
    @staticmethod
    def call(
        container: ContainerProtocol,
        callback: object,
        parameters: dict[object, object] | None = None,
        default_method: str | None = None,
    ) -> object: ...
