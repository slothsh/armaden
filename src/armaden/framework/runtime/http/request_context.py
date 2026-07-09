import contextvars
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .request import Request

_request_ctx: contextvars.ContextVar['Request | None'] = contextvars.ContextVar(
    'request', default=None
)


class RequestContext:
    @staticmethod
    def set_request(request: 'Request') -> None:
        _request_ctx.set(request)

    @staticmethod
    def get_request() -> 'Request':
        req = _request_ctx.get(None)
        if req is None:
            raise RuntimeError(
                'No request in context. request() must be called within an HTTP request lifecycle.'
            )
        return req

    @staticmethod
    def clear_request() -> None:
        _request_ctx.set(None)