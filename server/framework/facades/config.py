from typing import Any

from framework.kernel import Kernel


def config(key: str, default: Any | None = None) -> Any:
    return Kernel.instance().config(key, default)
