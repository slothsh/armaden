from typing import Protocol

from armaden.framework.types.result import Result


class ScheduleDispatcherProtocol[D](Protocol):
    async def dispatch(
        self,
        definition: D,
    ) -> Result[object]: ...
