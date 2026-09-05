from __future__ import annotations

from collections.abc import Mapping
from typing import override

from armaden.framework.protocols.http_controller_protocol import HttpControllerProtocol


class HttpController(HttpControllerProtocol):
    middleware: dict[str, Mapping[str, object]] = {}

    @override
    @classmethod
    def get_middleware(cls) -> dict[str, Mapping[str, object]]:
        return dict(cls.middleware)


    @override
    @classmethod
    def get_middleware_for_method(cls, method_name: str) -> list[str]:
        applicable: list[str] = []
        for alias, config in cls.middleware.items():
            only = config.get('only')
            excluded = config.get('except')
            if isinstance(only, list) and method_name not in only:
                continue
            if isinstance(excluded, list) and method_name in excluded:
                continue
            applicable.append(alias)
        return applicable
