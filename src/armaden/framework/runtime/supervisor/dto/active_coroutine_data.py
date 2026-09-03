from __future__ import annotations

import asyncio
from dataclasses import dataclass

from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol


@dataclass
class ActiveCoroutineData:
    coro: asyncio.Task[object]
    loop: asyncio.AbstractEventLoop | None
    runtime: TaskRuntimeProtocol
