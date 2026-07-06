from typing import Any
from .app import App


def config(key: str, default: Any | None = None) -> Any:
    return App.config(key, default)
