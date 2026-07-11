from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from armaden.framework.runtime.supervisor import Supervisor


class ScheduleFacade:
    def __init__(self, supervisor: 'Supervisor') -> None:
        self._supervisor = supervisor

    def interval(self, name: str, seconds: float):
        from armaden.framework.runtime.builders.schedule_builder import ScheduleBuilder
        return ScheduleBuilder(self._supervisor, name, seconds=seconds)

    def cron(self, name: str, expression: str):
        from armaden.framework.runtime.builders.schedule_builder import ScheduleBuilder
        return ScheduleBuilder(self._supervisor, name, cron=expression)
