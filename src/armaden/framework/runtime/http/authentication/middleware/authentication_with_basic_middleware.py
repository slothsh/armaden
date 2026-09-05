from armaden.framework.runtime.http.authentication.authentication_manager import AuthenticationManager
from armaden.framework.runtime.http.authentication.middleware.authentication_middleware import (
    AuthenticationMiddleware,
)


class AuthenticationWithBasicMiddleware(AuthenticationMiddleware):
    def __init__(self, authentication_manager: AuthenticationManager) -> None:
        super().__init__(authentication_manager, guard='basic', block=True)
