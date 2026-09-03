from armaden.framework.runtime.supervisor.dto.process_info_data import ProcessInfoData
from armaden.framework.runtime.supervisor.dto.thread_info_data import ThreadInfoData
from armaden.framework.runtime.supervisor.task.protocols.task_protocol import TaskProtocol
from armaden.framework.types.result import Result
from asyncio import Future
from dataclasses import dataclass
from threading import Thread
import asyncio


@dataclass
class TaskStateData:
    task_id: int
    thread_info: ThreadInfoData
    task: TaskProtocol
    initialized: bool
    future: Future[Result[None]] | None
    event_loop: asyncio.AbstractEventLoop
    processes: list[ProcessInfoData]
    thread: Thread
    started: bool = False
