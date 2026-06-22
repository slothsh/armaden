from typing import Any
from .app import app


def config(key: str, default: Any | None = None) -> Any:
    return app().config(key, default)
