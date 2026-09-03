from armaden.framework.protocols.container_dunder_protocol import ContainerDunderProtocol
from armaden.framework.protocols.container_methods_protocol import ContainerMethodsProtocol
from typing import Protocol


class ContainerProtocol(ContainerDunderProtocol, ContainerMethodsProtocol, Protocol):
    pass
