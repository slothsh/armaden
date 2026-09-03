from typing import Any

from starlette.responses import JSONResponse

from armaden.framework.runtime.http.middleware.middleware import Middleware, NextCallable

from ..request import Request
from .auth_manager import AuthManager


class Authenticate(Middleware):
    def __init__(
        self,
        auth_manager: AuthManager,
        guard: str | None = None,
        block: bool = False,
    ) -> None:
        self._auth_manager = auth_manager
        self._guard = guard
        self._block = block

    async def handle(self, request: Request, next: NextCallable) -> Any:
        guard = self._auth_manager.guard(self._guard)
        user = await guard.attempt(request)

        if user is not None:
            request.set_user(user)
            return await next(request)

        if self._block:
            return JSONResponse(
                content={'error': 'Unauthenticated'},
                status_code=401,
            )

        return await next(request)

    async def terminate(self, request: Request, response: Any) -> None:
        pass


class AuthenticateWithToken(Authenticate):
    def __init__(self, auth_manager: AuthManager) -> None:
        super().__init__(auth_manager, guard='token', block=True)


class AuthenticateWithBasic(Authenticate):
    def __init__(self, auth_manager: AuthManager) -> None:
        super().__init__(auth_manager, guard='basic', block=True)


class AuthenticateWithHeader(Authenticate):
    def __init__(self, auth_manager: AuthManager) -> None:
        super().__init__(auth_manager, guard='header', block=True)