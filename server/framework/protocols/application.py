from typing import Protocol
from .kernel import KernelInterface


class ApplicationInterface(KernelInterface, Protocol):
    pass
