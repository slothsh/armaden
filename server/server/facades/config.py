from typing import Any


def config(key: str, default: Any | None = None) -> Any:
    from server.application.application import Application
    return Application.instance().config(key, default)
