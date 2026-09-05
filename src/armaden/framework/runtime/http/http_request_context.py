from __future__ import annotations

import contextvars
from typing import ClassVar

from armaden.framework.protocols.http_request_protocol import HttpRequestProtocol


class HttpRequestContext:
    _request_context: ClassVar[
        contextvars.ContextVar[HttpRequestProtocol | None]
    ] = contextvars.ContextVar(
        'armaden_request',
        default=None,
    )

    @staticmethod
    def clear_request() -> None:
        _ = HttpRequestContext._request_context.set(None)


    @staticmethod
    def get_request() -> HttpRequestProtocol:
        request = HttpRequestContext._request_context.get()
        if request is None:
            raise RuntimeError(
                'No request in context. request() must be called within an HTTP request lifecycle.'
            )
        return request


    @staticmethod
    def set_request(request: HttpRequestProtocol) -> None:
        _ = HttpRequestContext._request_context.set(request)
