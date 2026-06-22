import asyncio
from typing import TypedDict

from framework.utils.types import ApiType, RouterType
from framework.protocols.kernel import KernelInterface


class DefaultApplicationHandles(TypedDict):
    app: KernelInterface
    event_loop: asyncio.AbstractEventLoop
    api: ApiType
    router: RouterType
