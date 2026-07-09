from typing import Any

from armaden.framework.runtime.http.facades.url import URL as _URL, route as _route, url as _url


class URL:
    @classmethod
    def route(cls, name: str, parameters: dict[str, Any] | None = None, absolute: bool = True) -> str:
        return _URL.route(name, parameters, absolute)

    @classmethod
    def has(cls, name: str) -> bool:
        return _URL.has(name)

    @classmethod
    def current(cls) -> str:
        return _URL.current()

    @classmethod
    def full(cls) -> str:
        return _URL.full()

    @classmethod
    def previous(cls, fallback: str = '/') -> str:
        return _URL.previous(fallback)

    @classmethod
    def to(cls, path: str, parameters: dict[str, Any] | None = None, absolute: bool = True) -> str:
        return _URL.to(path, parameters, absolute)


route = _route
url = _url