from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import cast, override

from armaden.framework.protocols.authentication_guard_protocol import AuthenticationGuardProtocol
from armaden.framework.protocols.authentication_manager_protocol import AuthenticationManagerProtocol
from armaden.framework.protocols.http_request_protocol import HttpRequestProtocol
from armaden.framework.runtime.http.authentication.config_user_provider import ConfigUserProvider
from armaden.framework.runtime.http.authentication.guards import (
    AuthenticationGuard,
    BasicAuthenticationGuard,
    CustomHeaderGuard,
    TokenGuard,
)


class AuthenticationManager(AuthenticationManagerProtocol):
    _guard_types: dict[str, type[AuthenticationGuard]] = {
        'basic': BasicAuthenticationGuard,
        'header': CustomHeaderGuard,
        'token': TokenGuard,
    }

    def __init__(self) -> None:
        self._config: Mapping[str, object] = {}
        self._custom_creators: dict[str, Callable[..., AuthenticationGuardProtocol]] = {}
        self._default_guard: str = 'token'
        self._guards: dict[str, AuthenticationGuardProtocol] = {}
        self._provider: ConfigUserProvider | None = None


    @override
    async def authenticate(
        self,
        request: HttpRequestProtocol,
        guard_name: str | None = None,
    ) -> object | None:
        return await self.guard(guard_name).attempt(request)


    @override
    def bootstrap(self, authentication_config: Mapping[str, object] | None = None) -> None:
        self._config = authentication_config or {}
        defaults = self._mapping(self._config.get('defaults'))
        guard = defaults.get('guard')
        self._default_guard = guard if isinstance(guard, str) else 'token'
        self._guards.clear()
        self._provider = None


    @override
    def extend(self, driver: str, creator: Callable[..., AuthenticationGuardProtocol]) -> None:
        self._custom_creators[driver] = creator


    @override
    def get_default_guard(self) -> str:
        return self._default_guard


    @override
    def guard(self, name: str | None = None) -> AuthenticationGuardProtocol:
        guard_name = name or self._default_guard
        if guard_name not in self._guards:
            self._guards[guard_name] = self._resolve_guard(guard_name)
        return self._guards[guard_name]


    def _get_provider(self) -> ConfigUserProvider:
        if self._provider is not None:
            return self._provider
        providers = self._mapping(self._config.get('providers'))
        user_provider = self._mapping(providers.get('users'))
        _ = user_provider.get('driver', 'config')
        self._provider = ConfigUserProvider(self._config)
        return self._provider


    @staticmethod
    def _mapping(value: object) -> Mapping[str, object]:
        if not isinstance(value, Mapping):
            return {}
        values = cast(Mapping[object, object], value)
        return {key: item for key, item in values.items() if isinstance(key, str)}


    def _resolve_guard(self, name: str) -> AuthenticationGuardProtocol:
        guards = self._mapping(self._config.get('guards'))
        config = self._mapping(guards.get(name))
        driver_value = config.get('driver', name)
        driver = driver_value if isinstance(driver_value, str) else name
        creator = self._custom_creators.get(driver)
        if creator is not None:
            return creator(config, name)
        guard_type = self._guard_types.get(driver)
        if guard_type is None:
            available = [*self._guard_types, *self._custom_creators]
            raise RuntimeError(
                f'Authentication guard "{name}" has no registered driver "{driver}". '
                + f'Available drivers: {available}'
            )
        guard_factory = cast(
            Callable[[ConfigUserProvider, Mapping[str, object]], AuthenticationGuard],
            guard_type,
        )
        return guard_factory(self._get_provider(), config)
