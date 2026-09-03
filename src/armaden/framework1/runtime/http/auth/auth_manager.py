from typing import Any, Callable

from .api_user import ApiUser
from .config_user_provider import ConfigUserProvider
from .guards import AuthGuard, BasicAuthGuard, CustomHeaderGuard, TokenGuard

GUARD_MAP: dict[str, type[AuthGuard]] = {
    'token': TokenGuard,
    'basic': BasicAuthGuard,
    'header': CustomHeaderGuard,
}


class AuthManager:
    def __init__(self) -> None:
        self._guards: dict[str, AuthGuard] = {}
        self._custom_creators: dict[str, Callable] = {}
        self._config: dict[str, Any] = {}
        self._provider: ConfigUserProvider | None = None
        self._default_guard: str = 'token'
        self._booted = False

    def bootstrap(self, auth_config: dict[str, Any] | None = None) -> None:
        if auth_config is None:
            auth_config = {}
        self._config = auth_config
        self._default_guard = auth_config.get('defaults', {}).get('guard', 'token')
        self._booted = True

    def extend(self, driver: str, creator: Callable[[dict[str, Any], str], AuthGuard]) -> None:
        self._custom_creators[driver] = creator

    def guard(self, name: str | None = None) -> AuthGuard:
        name = name or self._default_guard
        if name not in self._guards:
            self._guards[name] = self._resolve_guard(name)
        return self._guards[name]

    def get_default_guard(self) -> str:
        return self._default_guard

    async def authenticate(self, request: Any, guard_name: str | None = None) -> ApiUser | None:
        return await self.guard(guard_name).attempt(request)

    def _resolve_guard(self, name: str) -> AuthGuard:
        guard_configs = self._config.get('guards', {})
        cfg = guard_configs.get(name, {})
        driver = cfg.get('driver', name)

        provider = self._get_provider()

        creator = self._custom_creators.get(driver)
        if creator is not None:
            return creator(cfg, name)

        guard_cls = GUARD_MAP.get(driver)
        if guard_cls is not None:
            return guard_cls(provider, cfg)

        raise RuntimeError(
            f'Auth guard "{name}" has no registered driver "{driver}". '
            f'Available drivers: {list(GUARD_MAP)} + {list(self._custom_creators)}'
        )

    def _get_provider(self) -> ConfigUserProvider:
        if self._provider is not None:
            return self._provider
        provider_config = self._config.get('providers', {})
        user_provider = provider_config.get('users', {})
        driver = user_provider.get('driver', 'config')
        if driver == 'config':
            self._provider = ConfigUserProvider(self._config)
        else:
            self._provider = ConfigUserProvider(self._config)
        return self._provider