from typing import Any

import logging
from server.bootstrap import Application

logger = logging.getLogger('server.lib.facades')


def env(name: str, default: str | None = None) -> str | None:
    return Application.instance().environment(name, default)


def app() -> Application:
    return Application.instance()


def config(key: str) -> Any:
    value = Application.instance().config()

    for key in key.split("."):
        value = value[key]

    return value
