from typing import Protocol

from armaden.framework.protocols.core_application_protocol import CoreApplicationProtocol
from armaden.framework.types.result import Result


class KernelProtocol[A, R](Protocol):
    @property
    def application(self) -> CoreApplicationProtocol[A]: ...

    def bootstrap(self) -> Result[None]: ...

    def handle(self) -> Result[R]: ...

    def terminate(self) -> None: ...