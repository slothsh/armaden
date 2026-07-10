from typing import Any

from armaden.framework.runtime.http.middleware.middleware import Middleware, NextCallable

from ..request import Request
from .auth_manager import AuthManager


class Authenticate(Middleware):
    def __init__(self, auth_manager: AuthManager, guard: str | None = None) -> None:
        self._auth_manager = auth_manager
        self._guard = guard

    async def handle(self, request: Request, next: NextCallable) -> Any:
        guard = self._auth_manager.guard(self._guard)
        user = await guard.attempt(request)
        if user is not None:
            request.set_user(user)
        return await next(request)

    async def terminate(self, request: Request, response: Any) -> None:
        pass


class AuthenticateWithToken(Authenticate):
    def __init__(self, auth_manager: AuthManager) -> None:
        super().__init__(auth_manager, guard='token')


class AuthenticateWithBasic(Authenticate):
    def __init__(self, auth_manager: AuthManager) -> None:
        super().__init__(auth_manager, guard='basic')


class AuthenticateWithHeader(Authenticate):
    def __init__(self, auth_manager: AuthManager) -> None:
        super().__init__(auth_manager, guard='header')