import json
from typing import Any

import logging
from server.application import Application, ApplicationInterface

logger = logging.getLogger('server.lib.facades')


def env(name: str, default: Any | None = None) -> str | None:
    return Application.instance().environment(name, default)


def app() -> ApplicationInterface:
    return Application.instance()


def config(key: str, default: Any | None = None) -> Any:
    value = Application.instance().config()

    for key in key.split("."):
        value = value[key]

    if value is None:
        return default

    return value


class Env:
    """Facade for reading typed environment variables from the application."""

    @classmethod
    def string(cls, name: str, default: str | None = None) -> str | None:
        return Application.instance().environment(name, default)


    @classmethod
    def bool(cls, name: str, default: bool | None = None) -> bool | None:
        value = Application.instance().environment(name)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes', 'on')


    @classmethod
    def int(cls, name: str, default: int | None = None) -> int | None:
        value = Application.instance().environment(name)
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default


    @classmethod
    def json(cls, name: str, default):
        value = Application.instance().environment(name)
        if value is None:
            return default
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return default


    @classmethod
    def optional_json(cls, name: str):
        value = Application.instance().environment(name)
        if value is None or value.strip() == '':
            return None
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return None
