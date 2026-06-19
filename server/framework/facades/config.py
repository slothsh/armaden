from typing import Any

from framework.classes.kernel import Kernel


def config(key: str, default: Any | None = None) -> Any:
    return Kernel.instance().config(key, default)
