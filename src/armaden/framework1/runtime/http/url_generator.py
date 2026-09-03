import re
from typing import Any
from urllib.parse import urlencode

from armaden.framework.facades import App


class UrlGenerator:
    _instance: 'UrlGenerator | None' = None

    def __init__(self) -> None:
        self._routes: dict[str, dict[str, Any]] = {}

    @classmethod
    def get_instance(cls) -> 'UrlGenerator':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def register(self, name: str, path: str, methods: list[str], parameters: dict[str, type]) -> None:
        if name in self._routes:
            import logging
            logging.getLogger(__name__).warning('Duplicate named route: %s', name)
        self._routes[name] = {
            'path': path,
            'methods': methods,
            'parameters': parameters,
        }

    def route(self, name: str, parameters: dict[str, Any] | None = None, absolute: bool = True) -> str:
        if name not in self._routes:
            raise RouteNotFoundException(f'Named route "{name}" not found')
        route_info = self._routes[name]
        path = route_info['path']
        params = parameters or {}

        def _sub(match: re.Match) -> str:
            param_name = match.group(1)
            if param_name in params:
                return str(params.pop(param_name))
            raise RouteParameterMissingException(
                f'Missing required parameter "{param_name}" for route "{name}"'
            )

        resolved = re.sub(r'\{(\w+)(?::\w+)?\}', _sub, path)
        if params:
            resolved += '?' + urlencode(params)

        if absolute:
            return self._base_url() + resolved
        return resolved

    def has(self, name: str) -> bool:
        return name in self._routes

    def current(self) -> str:
        from .helpers import request
        try:
            return request().path()
        except RuntimeError:
            return '/'

    def full(self) -> str:
        from .helpers import request
        try:
            return request().full_url()
        except RuntimeError:
            return '/'

    def previous(self, fallback: str = '/') -> str:
        return fallback

    def to(self, path: str, parameters: dict[str, Any] | None = None, absolute: bool = True) -> str:
        resolved = path
        if parameters:
            resolved += '?' + urlencode(parameters)
        if absolute:
            return self._base_url() + resolved
        return resolved

    def _base_url(self) -> str:
        try:
            url = App.config('app.url', None)
            if url:
                return url.rstrip('/')
        except Exception:
            pass
        try:
            from .helpers import request
            req = request()
            scheme = req._request.url.scheme
            host = req._request.url.netloc
            return f'{scheme}://{host}'
        except RuntimeError:
            return 'http://localhost'


class RouteNotFoundException(Exception):
    pass


class RouteParameterMissingException(Exception):
    pass
