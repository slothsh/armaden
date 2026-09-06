from __future__ import annotations

from typing import cast, override

from armaden.framework.facades.facade import Facade
from armaden.framework.runtime.schedule.dto.schedule_inspection_data import ScheduleInspectionData
from armaden.framework.runtime.schedule.dto.scheduled_event_definition_data import (
    ScheduledEventDefinitionData,
)
from armaden.framework.protocols.schedule_registry_protocol import ScheduleRegistryProtocol
from armaden.framework.runtime.schedule.enums import ScheduledEventKind
from armaden.framework.runtime.schedule.scheduled_event import ScheduledEvent
from armaden.framework.types.result import Result
from armaden.framework.types.schedule import (
    ScheduleCallback,
    ScheduleCommand,
    ScheduleTag,
)


class ScheduleFacade(Facade):
    @classmethod
    def _registry(
        cls,
    ) -> ScheduleRegistryProtocol[ScheduledEventDefinitionData, ScheduleInspectionData]:
        return cast(
            ScheduleRegistryProtocol[ScheduledEventDefinitionData, ScheduleInspectionData],
            cls.get_facade_root(),
        )


    @classmethod
    def call(cls, callback: ScheduleCallback) -> ScheduledEvent:
        return ScheduledEvent(
            ScheduledEventKind.CALL,
            callback,
            cls._registry().register,
        )


    @classmethod
    def definitions(cls, tag: ScheduleTag | None = None) -> list[ScheduleInspectionData]:
        return cls._registry().definitions(tag)


    @override
    @classmethod
    def get_facade_accessor(cls) -> object:
        return ScheduleRegistryProtocol


    @classmethod
    def exec(cls, command: ScheduleCommand) -> ScheduledEvent:
        return ScheduledEvent(
            ScheduledEventKind.EXEC,
            command,
            cls._registry().register,
        )


    @classmethod
    def job(
        cls,
        job: object,
        queue: str | None = None,
        connection: str | None = None,
    ) -> ScheduledEvent:
        event = ScheduledEvent(
            ScheduledEventKind.JOB,
            job,
            cls._registry().register,
        )
        if queue is not None:
            _ = event.on_queue(queue)
        if connection is not None:
            _ = event.on_connection(connection)
        priority = getattr(job, 'priority', None)
        if isinstance(priority, int):
            _ = event.priority(priority)
        tags = getattr(job, 'tags', ())
        if isinstance(tags, (list, tuple)):
            tag_values = cast(list[object] | tuple[object, ...], tags)
            _ = event.tag(*[
                tag
                for tag in tag_values
                if isinstance(tag, (str, type))
            ])
        return event


    @classmethod
    def remove_job(cls, name: str) -> Result[None]:
        return cls._registry().remove(name)


    @classmethod
    def shutdown(cls) -> Result[None]:
        return cls._registry().shutdown()


    @classmethod
    def start(cls) -> Result[None]:
        return cls._registry().start()
