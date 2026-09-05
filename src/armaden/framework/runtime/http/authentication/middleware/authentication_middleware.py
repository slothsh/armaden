from __future__ import annotations

from typing import override

from starlette.responses import JSONResponse

from armaden.framework.protocols.http_middleware_protocol import NextCallable
from armaden.framework.protocols.http_request_protocol import HttpRequestProtocol
from armaden.framework.runtime.http.authentication.authentication_manager import AuthenticationManager
from armaden.framework.runtime.http.middleware.http_middleware import HttpMiddleware


class AuthenticationMiddleware(HttpMiddleware):
    def __init__(
        self,
        authentication_manager: AuthenticationManager,
        guard: str | None = None,
        block: bool = False,
    ) -> None:
        super().__init__()
        self._authentication_manager: AuthenticationManager = authentication_manager
        self._block: bool = block
        self._guard: str | None = guard


    @override
    async def handle(self, request: HttpRequestProtocol, next: NextCallable) -> object:
        user = await self._authentication_manager.authenticate(request, self._guard)
        if user is not None:
            request.set_user(user)
            return await next(request)
        if self._block:
            return JSONResponse(content={'error': 'Unauthenticated'}, status_code=401)
        return await next(request)
