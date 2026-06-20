import asyncio
from typing import TypedDict

from ..utils.types import ApiType, RouterType
from ..protocols.kernel import KernelInterface


class DefaultApplicationHandles(TypedDict):
    app: KernelInterface
    event_loop: asyncio.AbstractEventLoop
    api: ApiType
    router: RouterType
