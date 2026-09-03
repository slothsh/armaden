from typing import Any

from .api_user import ApiUser


class ConfigUserProvider:
    def __init__(self, config: dict[str, Any]) -> None:
        self._users: dict[str, dict[str, Any]] = config.get('users', {})

    def retrieve_by_token(self, token: str) -> ApiUser | None:
        if not token:
            return None
        for key, data in self._users.items():
            if data.get('token') == token:
                return ApiUser(
                    id=data['id'],
                    roles=data.get('roles', []),
                    metadata={'_config_key': key},
                )
        return None

    def retrieve_by_credentials(self, username: str, password: str) -> ApiUser | None:
        if not username:
            return None
        for key, data in self._users.items():
            if data.get('username') == username and data.get('password') == password:
                return ApiUser(
                    id=data['id'],
                    roles=data.get('roles', []),
                    username=username,
                    metadata={'_config_key': key},
                )
        return None

    def retrieve_by_id(self, user_id: str) -> ApiUser | None:
        if not user_id:
            return None
        for key, data in self._users.items():
            if data.get('id') == user_id:
                return ApiUser(
                    id=data['id'],
                    roles=data.get('roles', []),
                    username=data.get('username'),
                    metadata={'_config_key': key},
                )
        return None
