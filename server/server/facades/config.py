from typing import Any
from server.application.application import Application


def config(key: str, default: Any | None = None) -> Any:
    value = Application.instance().config()

    for key in key.split("."):
        value = value[key]

    if value is None:
        return default

    return value
