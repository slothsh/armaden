from collections.abc import Mapping
from typing import Protocol

from armaden.framework.protocols.supervisor_protocol import SupervisorProtocol
from armaden.framework.types.result import Result


class ApplicationProtocol[G](Protocol):
    middleware: list[type[object]]
    middleware_groups: dict[str, list[type[object]]]

    def boot(self) -> Result[None]: ...

    def route_groups(self) -> dict[str, dict[str, object]]: ...

    async def status(self) -> Result[Mapping[str, object]]: ...

    @property
    def supervisor(self) -> SupervisorProtocol[G]: ...