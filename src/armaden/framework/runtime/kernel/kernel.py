from __future__ import annotations

from abc import ABC, abstractmethod
from typing import override

from armaden.framework.protocols.core_application_protocol import CoreApplicationProtocol
from armaden.framework.protocols.kernel_protocol import KernelProtocol
from armaden.framework.types.result import Result


class Kernel[A, R](KernelProtocol[A, R], ABC):
    def __init__(self, application: CoreApplicationProtocol[A]) -> None:
        self._application: CoreApplicationProtocol[A] = application


    @property
    @override
    def application(self) -> CoreApplicationProtocol[A]:
        return self._application


    @override
    @abstractmethod
    def bootstrap(self) -> Result[None]:
        raise NotImplementedError


    @override
    @abstractmethod
    def handle(self) -> Result[R]:
        raise NotImplementedError


    @override
    @abstractmethod
    def terminate(self) -> None:
        raise NotImplementedError