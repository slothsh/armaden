from __future__ import annotations

from collections.abc import Mapping
from typing import cast, override

from armaden.framework.facades.facade import Facade
from armaden.framework.protocols.url_generator_protocol import UrlGeneratorProtocol


class UrlFacade(Facade):
    @override
    @classmethod
    def get_facade_accessor(cls) -> object:
        return UrlGeneratorProtocol


    @classmethod
    def current(cls) -> str:
        return cast(UrlGeneratorProtocol, cls.get_facade_root()).current()


    @classmethod
    def full(cls) -> str:
        return cast(UrlGeneratorProtocol, cls.get_facade_root()).full()


    @classmethod
    def has(cls, name: str) -> bool:
        return cast(UrlGeneratorProtocol, cls.get_facade_root()).has(name)


    @classmethod
    def previous(cls, fallback: str = '/') -> str:
        return cast(UrlGeneratorProtocol, cls.get_facade_root()).previous(fallback)


    @classmethod
    def route(
        cls,
        name: str,
        parameters: Mapping[str, object] | None = None,
        absolute: bool = True,
    ) -> str:
        return cast(UrlGeneratorProtocol, cls.get_facade_root()).route(
            name,
            parameters,
            absolute,
        )


    @classmethod
    def to(
        cls,
        path: str,
        parameters: Mapping[str, object] | None = None,
        absolute: bool = True,
    ) -> str:
        return cast(UrlGeneratorProtocol, cls.get_facade_root()).to(
            path,
            parameters,
            absolute,
        )
