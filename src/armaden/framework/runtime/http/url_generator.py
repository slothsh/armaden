from __future__ import annotations

import os
import re
from collections.abc import Mapping
from urllib.parse import urlencode

from typing import override

from armaden.framework.protocols.url_generator_protocol import UrlGeneratorProtocol
from armaden.framework.runtime.http.exceptions.route_not_found_exception import (
    RouteNotFoundException,
)
from armaden.framework.runtime.http.exceptions.route_parameter_missing_exception import (
    RouteParameterMissingException,
)
from armaden.framework.runtime.http.http_request_context import HttpRequestContext


class UrlGenerator(UrlGeneratorProtocol):
    _instance: UrlGenerator | None = None

    def __init__(self) -> None:
        self._routes: dict[str, dict[str, object]] = {}


    @classmethod
    def get_instance(cls) -> UrlGenerator:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


    def _base_url(self) -> str:
        configured = os.getenv('APP_URL')
        if configured:
            return configured.rstrip('/')
        try:
            request = HttpRequestContext.get_request()
            url = request.url()
            path = request.path()
            return url.split(path, 1)[0].rstrip('/')
        except RuntimeError:
            return 'http://localhost'


    def _route_parameters(
        self,
        path: str,
        name: str,
        parameters: Mapping[str, object],
    ) -> tuple[str, dict[str, object]]:
        remaining = dict(parameters)

        def replace(match: re.Match[str]) -> str:
            parameter_name = match.group(1)
            if parameter_name not in remaining:
                raise RouteParameterMissingException(
                    f'Missing required parameter "{parameter_name}" for route "{name}"'
                )
            return str(remaining.pop(parameter_name))

        return re.sub(r'\{(\w+)(?::\w+)?\}', replace, path), remaining


    @override
    def current(self) -> str:
        try:
            return HttpRequestContext.get_request().path()
        except RuntimeError:
            return '/'


    @override
    def full(self) -> str:
        try:
            return HttpRequestContext.get_request().full_url()
        except RuntimeError:
            return '/'


    @override
    def has(self, name: str) -> bool:
        return name in self._routes


    @override
    def previous(self, fallback: str = '/') -> str:
        return fallback


    @override
    def register(
        self,
        name: str,
        path: str,
        methods: list[str],
        parameters: Mapping[str, type[object]],
    ) -> None:
        self._routes[name] = {
            'methods': list(methods),
            'parameters': dict(parameters),
            'path': path,
        }


    @override
    def route(
        self,
        name: str,
        parameters: Mapping[str, object] | None = None,
        absolute: bool = True,
    ) -> str:
        if name not in self._routes:
            raise RouteNotFoundException(f'Named route "{name}" not found')
        route = self._routes[name]
        path = str(route['path'])
        resolved, remaining = self._route_parameters(path, name, parameters or {})
        if remaining:
            resolved = f'{resolved}?{urlencode(remaining)}'
        return f'{self._base_url()}{resolved}' if absolute else resolved


    @override
    def to(        self,
        path: str,
        parameters: Mapping[str, object] | None = None,
        absolute: bool = True,
    ) -> str:
        resolved = path
        if parameters:
            resolved = f'{resolved}?{urlencode(parameters)}'
        return f'{self._base_url()}{resolved}' if absolute else resolved
