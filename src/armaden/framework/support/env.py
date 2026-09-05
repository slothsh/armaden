import json as json_module
import os


def env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    return value if value else default


class Env:
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
        except (TypeError, ValueError):
            return default


    @classmethod
    def json(cls, name: str, default: object | None = None) -> object | None:
        value = env(name)
        if value is None:
            return default
        try:
            return json_module.loads(value)
        except (TypeError, json_module.JSONDecodeError):
            return default


    @classmethod
    def optional_json(cls, name: str) -> object | None:
        value = env(name)
        if value is None or value.strip() == '':
            return None
        try:
            return json_module.loads(value)
        except (TypeError, json_module.JSONDecodeError):
            return None


    @classmethod
    def string(cls, name: str, default: str | None = None) -> str | None:
        return env(name, default)
