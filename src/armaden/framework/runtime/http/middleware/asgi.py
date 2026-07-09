from starlette.requests import Request as StarletteRequest

from ..request import Request
from ..request_context import RequestContext
from .kernel import HttpKernel
from .middleware import Middleware
from .pipeline import MiddlewarePipeline


class AsgiMiddlewareAdapter:
    def __init__(self, middleware_class: type[Middleware]) -> None:
        self._middleware_class = middleware_class

    async def __call__(self, scope, receive, send) -> None:
        starlette_request = StarletteRequest(scope=scope, receive=receive)
        request = Request(starlette_request)
        RequestContext.set_request(request)

        try:
            async def asgi_next(req: Request) -> None:
                pass

            mw = self._middleware_class()
            response = await mw.handle(request, asgi_next)
            if response is not None:
                await response(scope, receive, send)
                await mw.terminate(request, response)
            else:
                async def noop_response(s, r, se):
                    pass
                await noop_response(scope, receive, send)
        finally:
            RequestContext.clear_request()
