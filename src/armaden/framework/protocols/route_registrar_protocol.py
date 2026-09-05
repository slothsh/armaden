from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Protocol

from armaden.framework.protocols.route_group_protocol import RouteGroupProtocol


class RouteRegistrarProtocol(Protocol):
    def any(
        self,
        path: str,
        handler: object,
        **options: object,
    ) -> RouteRegistrarProtocol: ...

    def delete(
        self,
        path: str,
        handler: object,
        **options: object,
    ) -> RouteRegistrarProtocol: ...

    def get(
        self,
        path: str,
        handler: object,
        **options: object,
    ) -> RouteRegistrarProtocol: ...

    def get_routes(self) -> Sequence[object]: ...

    def group(self, callback: Callable[[], None]) -> None: ...

    def match(
        self,
        methods: list[str],
        path: str,
        handler: object,
        **options: object,
    ) -> RouteRegistrarProtocol: ...

    def middleware(self, *middleware: str) -> RouteGroupProtocol: ...

    def namespace(self, namespace: str) -> RouteGroupProtocol: ...

    def options(
        self,
        path: str,
        handler: object,
        **options: object,
    ) -> RouteRegistrarProtocol: ...

    def patch(
        self,
        path: str,
        handler: object,
        **options: object,
    ) -> RouteRegistrarProtocol: ...

    def post(
        self,
        path: str,
        handler: object,
        **options: object,
    ) -> RouteRegistrarProtocol: ...

    def prefix(self, prefix: str) -> RouteGroupProtocol: ...

    def put(
        self,
        path: str,
        handler: object,
        **options: object,
    ) -> RouteRegistrarProtocol: ...

    def resource(self, name: str, controller: type[object], **options: object) -> None: ...

    def clear(self) -> None: ...
