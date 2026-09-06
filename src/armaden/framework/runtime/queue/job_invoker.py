from __future__ import annotations

import asyncio
import inspect
from collections.abc import Awaitable
from typing import cast

from armaden.framework.protocols.queue_job_protocol import QueueJobProtocol


async def invoke_job_handle(
    job: QueueJobProtocol,
    timeout: float | None = None,
) -> object:
    handle = job.handle
    if inspect.iscoroutinefunction(handle):
        result = cast(Awaitable[object], handle())
    else:
        result = await asyncio.to_thread(handle)
    if not inspect.isawaitable(result):
        return result
    coroutine = result
    if timeout is None:
        return await coroutine
    return await asyncio.wait_for(coroutine, timeout)


def invoke_job_handle_sync(
    job: QueueJobProtocol,
    timeout: float | None = None,
) -> object:
    handle = job.handle
    if inspect.iscoroutinefunction(handle):
        result = cast(Awaitable[object], handle())
    else:
        result = handle()
    if not inspect.isawaitable(result):
        return result
    try:
        _ = asyncio.get_running_loop()
    except RuntimeError:
        if timeout is None:
            return asyncio.run(result)
        return asyncio.run(asyncio.wait_for(result, timeout))
    raise ValueError(
        'Cannot run an async job handle synchronously inside a running event loop; '
        + 'call dispatch on the event loop instead',
    )