from __future__ import annotations

from typing import Self, override

from armaden.framework.protocols.contextual_binding_builder_protocol import (
    ContextualBindingBuilderProtocol,
)
from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.support.array import Array


class ContextualBindingBuilder(ContextualBindingBuilderProtocol):
    def __init__(self, container: ContainerProtocol, concrete: list[object]):
        self.abstract: object | None = None
        self.container: ContainerProtocol = container
        self.concrete: list[object] = Array.array_wrap(concrete)


    @override
    def give(self, implementation: object) -> Self:
        for concrete in self.concrete:
            self.container.add_contextual_binding(concrete, self.abstract, implementation)
        return self


    @override
    def give_config(self, key: str) -> Self:
        for concrete in self.concrete:
            self.container.add_contextual_binding(
                concrete, self.abstract, {'__config__': key}
            )
        return self


    @override
    def give_tagged(self, tag: str) -> Self:
        for concrete in self.concrete:
            self.container.add_contextual_binding(
                concrete, self.abstract, {'__tagged__': tag}
            )
        return self


    @override
    def needs(self, abstract: object) -> Self:
        self.abstract = abstract
        return self
