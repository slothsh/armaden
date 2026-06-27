import asyncio
from collections.abc import Callable, Coroutine
from returns.result import Result
from typing import Protocol, List, Self, Any
from pathlib import Path

from .supervisor_request_interface import SupervisorRequestInterface
from .task import TaskInterface
from .error import ErrorInterface


class SupervisorInterface(Protocol):
    def add_task(self, task: TaskInterface) -> Self: ...
    def add_tasks(self, tasks: List[TaskInterface]) -> Self: ...

    async def initialize(self) -> Result[None, ErrorInterface]: ...
    async def run(self) -> Result[None, ErrorInterface]: ...
    async def shutdown(self) -> Result[None, ErrorInterface]: ...

    async def enqueue_request(self, request: SupervisorRequestInterface) -> Result[None, ErrorInterface]: ...
