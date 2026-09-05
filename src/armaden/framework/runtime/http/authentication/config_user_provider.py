from __future__ import annotations

from collections.abc import Mapping
from typing import cast, override

from armaden.framework.protocols.user_provider_protocol import UserProviderProtocol
from armaden.framework.runtime.http.authentication.dto.api_user_data import ApiUserData


class ConfigUserProvider(UserProviderProtocol):
    def __init__(self, config: Mapping[str, object]) -> None:
        users = config.get('users', {})
        if isinstance(users, Mapping):
            user_values = cast(Mapping[object, object], users)
            values: list[tuple[str, object]] = [
                (key, value)
                for key, value in user_values.items()
                if isinstance(key, str)
            ]
            self._users: Mapping[str, object] = dict(values)
        else:
            self._users = {}


    @staticmethod
    def _mapping(value: object) -> Mapping[str, object]:
        if not isinstance(value, Mapping):
            return {}
        values = cast(Mapping[object, object], value)
        return {key: item for key, item in values.items() if isinstance(key, str)}


    @override
    def retrieve_by_credentials(
        self,
        username: str,
        password: str,
    ) -> ApiUserData | None:
        if not username:
            return None
        for key, value in self._users.items():
            data = self._mapping(value)
            if data.get('username') == username and data.get('password') == password:
                return ApiUserData(
                    id=str(data.get('id', key)),
                    metadata={'_config_key': key},
                    roles=self._roles(data.get('roles')),
                    username=username,
                )
        return None


    @override
    def retrieve_by_id(self, user_id: str) -> ApiUserData | None:
        if not user_id:
            return None
        for key, value in self._users.items():
            data = self._mapping(value)
            if data.get('id') == user_id:
                return ApiUserData(
                    id=user_id,
                    metadata={'_config_key': key},
                    roles=self._roles(data.get('roles')),
                    username=self._string(data.get('username')),
                )
        return None


    @override
    def retrieve_by_token(self, token: str) -> ApiUserData | None:
        if not token:
            return None
        for key, value in self._users.items():
            data = self._mapping(value)
            if data.get('token') == token:
                return ApiUserData(
                    id=str(data.get('id', key)),
                    metadata={'_config_key': key},
                    roles=self._roles(data.get('roles')),
                )
        return None


    @staticmethod
    def _roles(value: object) -> list[str]:
        if not isinstance(value, list):
            return []
        values = cast(list[object], value)
        return [role for role in values if isinstance(role, str)]


    @staticmethod
    def _string(value: object) -> str | None:
        return value if isinstance(value, str) else None
