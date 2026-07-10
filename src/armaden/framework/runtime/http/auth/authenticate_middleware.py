from typing import Any

from armaden.framework.runtime.http.middleware.middleware import Middleware, NextCallable

from ..request import Request
from .auth_manager import AuthManager


class Authenticate(Middleware):
    def __init__(self, auth_manager: AuthManager) -> None:
        self._auth_manager = auth_manager

    async def handle(self, request: Request, next: NextCallable) -> Any:
        user = await self._auth_manager.authenticate(request)
        if user is not None:
            request.set_user(user)
        return await next(request)

    async def terminate(self, request: Request, response: Any) -> None:
        pass
