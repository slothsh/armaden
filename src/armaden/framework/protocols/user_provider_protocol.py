from __future__ import annotations

from typing import Protocol


class UserProviderProtocol(Protocol):
    def retrieve_by_credentials(self, username: str, password: str) -> object | None: ...

    def retrieve_by_id(self, user_id: str) -> object | None: ...

    def retrieve_by_token(self, token: str) -> object | None: ...