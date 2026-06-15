import json
from typing import Any


def env(name: str, default: Any | None = None) -> str | None:
    from server.application.application import Application
    return Application.instance().environment(name, default)


class Env:
    """Facade for reading typed environment variables from the application."""

    @classmethod
    def string(cls, name: str, default: str | None = None) -> str | None:
        from server.application.application import Application
        return Application.instance().environment(name, default)


    @classmethod
    def bool(cls, name: str, default: bool | None = None) -> bool | None:
        from server.application.application import Application
        value = Application.instance().environment(name)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes', 'on')


    @classmethod
    def int(cls, name: str, default: int | None = None) -> int | None:
        from server.application.application import Application
        value = Application.instance().environment(name)
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default


    @classmethod
    def json(cls, name: str, default):
        from server.application.application import Application
        value = Application.instance().environment(name)
        if value is None:
            return default
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return default


    @classmethod
    def optional_json(cls, name: str):
        from server.application.application import Application
        value = Application.instance().environment(name)
        if value is None or value.strip() == '':
            return None
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return None
