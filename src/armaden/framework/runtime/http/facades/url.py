from typing import Any

from ..url_generator import UrlGenerator


class URL:
    _generator = UrlGenerator.get_instance()

    @classmethod
    def route(cls, name: str, parameters: dict[str, Any] | None = None, absolute: bool = True) -> str:
        return cls._generator.route(name, parameters, absolute)

    @classmethod
    def has(cls, name: str) -> bool:
        return cls._generator.has(name)

    @classmethod
    def current(cls) -> str:
        return cls._generator.current()

    @classmethod
    def full(cls) -> str:
        return cls._generator.full()

    @classmethod
    def previous(cls, fallback: str = '/') -> str:
        return cls._generator.previous(fallback)

    @classmethod
    def to(cls, path: str, parameters: dict[str, Any] | None = None, absolute: bool = True) -> str:
        return cls._generator.to(path, parameters, absolute)


def route(name: str, parameters: dict[str, Any] | None = None, absolute: bool = True) -> str:
    return UrlGenerator.get_instance().route(name, parameters, absolute)


def url(path: str = '/', parameters: dict[str, Any] | None = None) -> str:
    return UrlGenerator.get_instance().to(path, parameters)
