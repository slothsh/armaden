from __future__ import annotations

from collections.abc import Mapping
from typing import cast, override

from returns.result import Success

from armaden.framework.protocols.application_protocol import ApplicationProtocol
from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.supervisor_protocol import SupervisorProtocol
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraphData
from armaden.framework.types.result import Result


class Application(ApplicationProtocol[TaskGraphData]):
    middleware: list[type[object]] = []
    middleware_groups: dict[str, list[type[object]]] = {}

    def __init__(self, container: ContainerProtocol) -> None:
        self._container: ContainerProtocol = container


    @override
    def boot(self) -> Result[None]:
        return Success(None)


    @override
    def route_groups(self) -> dict[str, dict[str, object]]:
        return {}


    @override
    async def status(self) -> Result[Mapping[str, object]]:
        return Success({})


    @property
    @override
    def supervisor(self) -> SupervisorProtocol[TaskGraphData]:
        return cast(
            SupervisorProtocol[TaskGraphData],
            self._container.make(SupervisorProtocol),
        )