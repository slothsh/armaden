from __future__ import annotations

from typing import Protocol

from armaden.framework.protocols.configuration_protocol import ConfigurationProtocol
from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from armaden.framework.types.result import Result


class DefaultApiProtocol(Protocol):
    async def initialize(
        self,
        runtime: TaskRuntimeProtocol,
        configuration: ConfigurationProtocol,
    ) -> Result[None]: ...

    async def run(self, runtime: TaskRuntimeProtocol) -> Result[None]: ...

    async def shutdown(self, runtime: TaskRuntimeProtocol) -> Result[None]: ...

    async def status(self, runtime: TaskRuntimeProtocol) -> Result[dict[str, object]]: ...