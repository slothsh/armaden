import os
import json
from typing import Any


def env(name: str, default: Any | None = None) -> str | None:
    if result := os.getenv(name):
        return result
    return default


class Env:
    """Facade for reading typed environment variables from the application."""

    @classmethod
    def string(cls, name: str, default: str | None = None) -> str | None:
        return env(name, default)


    @classmethod
    def bool(cls, name: str, default: bool | None = None) -> bool | None:
        value = env(name)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes', 'on')


    @classmethod
    def int(cls, name: str, default: int | None = None) -> int | None:
        value = env(name)
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default


    @classmethod
    def json(cls, name: str, default: Any | None = None):
        value = env(name)
        if value is None:
            return default
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return default


    @classmethod
    def optional_json(cls, name: str):
        value = env(name)
        if value is None or value.strip() == '':
            return None
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return None
