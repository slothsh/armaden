from typing import Any

from armaden.framework.protocols.application import ApplicationInterface

from .api_user import ApiUser
from .config_user_provider import ConfigUserProvider
from .guards import AuthGuard, BasicAuthGuard, CustomHeaderGuard, TokenGuard

GUARD_MAP: dict[str, type[AuthGuard]] = {
    'token': TokenGuard,
    'basic': BasicAuthGuard,
    'header': CustomHeaderGuard,
}


class AuthManager:
    def __init__(self, app: ApplicationInterface) -> None:
        self._app = app
        self._guards: dict[str, AuthGuard] = {}
        self._provider: ConfigUserProvider | None = None
        self._default_guard: str = 'token'

    def bootstrap(self) -> None:
        auth_config = self._app.config('auth', {})
        self._default_guard = auth_config.get('defaults', {}).get('guard', 'token')
        guard_configs = auth_config.get('guards', {})

        provider = self._resolve_provider(auth_config)
        self._provider = provider

        for name, cfg in guard_configs.items():
            driver = cfg.get('driver', name)
            guard_cls = GUARD_MAP.get(driver)
            if guard_cls is None:
                continue
            self._guards[name] = guard_cls(provider, cfg)

    def _resolve_provider(self, auth_config: dict[str, Any]) -> ConfigUserProvider:
        provider_config = auth_config.get('providers', {})
        user_provider = provider_config.get('users', {})
        driver = user_provider.get('driver', 'config')
        if driver == 'config':
            return ConfigUserProvider(auth_config)
        return ConfigUserProvider(auth_config)

    def guard(self, name: str | None = None) -> AuthGuard | None:
        return self._guards.get(name or self._default_guard)

    def get_default_guard(self) -> str:
        return self._default_guard

    async def authenticate(self, request: Any) -> ApiUser | None:
        guard = self.guard()
        if guard is None:
            return None
        return await guard.attempt(request)
