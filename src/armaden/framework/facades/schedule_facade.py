from __future__ import annotations

from collections.abc import Mapping
from typing import ClassVar, cast, override

from armaden.framework.facades.facade import Facade
from armaden.framework.runtime.schedule.dto.schedule_inspection_data import ScheduleInspectionData
from armaden.framework.runtime.schedule.dto.scheduled_event_definition_data import (
    ScheduledEventDefinitionData,
)
from armaden.framework.protocols.schedule_registry_protocol import ScheduleRegistryProtocol
from armaden.framework.runtime.schedule.enums import ScheduledEventKind
from armaden.framework.runtime.schedule.schedule_group import ScheduleGroup
from armaden.framework.runtime.schedule.scheduled_event import ScheduledEvent
from armaden.framework.types.result import Result
from armaden.framework.types.schedule import (
    ScheduleCallback,
    ScheduleCommand,
    ScheduleTag,
)


class ScheduleFacade(Facade):
    _configured_defaults: ClassVar[Mapping[str, object]] = {}


    @classmethod
    def _apply_defaults(cls, event: ScheduledEvent) -> ScheduledEvent:
        defaults = {**cls._configured_defaults, **ScheduleGroup.defaults()}
        if isinstance(defaults.get('connection'), str):
            _ = event.on_connection(cast(str, defaults['connection']))
        if isinstance(defaults.get('queue'), str):
            _ = event.on_queue(cast(str, defaults['queue']))
        if isinstance(defaults.get('priority'), int):
            _ = event.priority(cast(int, defaults['priority']))
        if defaults.get('timezone') is not None:
            _ = event.timezone(cast(str, defaults['timezone']))
        if defaults.get('worker') == 'exclusive':
            _ = event.exclusive_worker()
        if isinstance(defaults.get('without_overlapping'), int):
            _ = event.without_overlapping(cast(int, defaults['without_overlapping']))
        if defaults.get('run_in_background') is True:
            _ = event.run_in_background()
        environments = defaults.get('environments')
        if isinstance(environments, (list, tuple)):
            values = cast(list[object] | tuple[object, ...], environments)
            names = [value for value in values if isinstance(value, str)]
            if names:
                _ = event.environments(*names)
        for key, method_name in (
            ('before', 'before'),
            ('after', 'after'),
            ('on_success', 'on_success'),
            ('on_failure', 'on_failure'),
        ):
            hooks = defaults.get(key)
            if callable(hooks):
                hooks = (hooks,)
            if isinstance(hooks, (list, tuple)):
                values = cast(list[object] | tuple[object, ...], hooks)
                method = getattr(event, method_name)
                for hook in values:
                    if callable(hook):
                        _ = method(hook)
        return event


    @classmethod
    def configure_defaults(cls, values: Mapping[str, object]) -> None:
        cls._configured_defaults = dict(values)


    @classmethod
    def group(cls, **defaults: object) -> ScheduleGroup:
        return ScheduleGroup(defaults)

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
        return cls._apply_defaults(ScheduledEvent(
            ScheduledEventKind.CALL,
            callback,
            cls._registry().register,
        ))


    @classmethod
    def definitions(cls, tag: ScheduleTag | None = None) -> list[ScheduleInspectionData]:
        return cls._registry().definitions(tag)


    @classmethod
    def get_jobs(cls, tag: ScheduleTag | None = None) -> list[ScheduleInspectionData]:
        return cls.definitions(tag)


    @override
    @classmethod
    def get_facade_accessor(cls) -> object:
        return ScheduleRegistryProtocol


    @classmethod
    def exec(cls, command: ScheduleCommand) -> ScheduledEvent:
        return cls._apply_defaults(ScheduledEvent(
            ScheduledEventKind.EXEC,
            command,
            cls._registry().register,
        ))


    @classmethod
    def job(
        cls,
        job: object,
        queue: str | None = None,
        connection: str | None = None,
    ) -> ScheduledEvent:
        event: ScheduledEvent = cls._apply_defaults(ScheduledEvent(
            ScheduledEventKind.JOB,
            job,
            cls._registry().register,
        ))
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
    def pause_job(cls, name: str) -> Result[None]:
        return cls._registry().pause(name)


    @classmethod
    def remove_job(cls, name: str) -> Result[None]:
        return cls._registry().remove(name)


    @classmethod
    def resume_job(cls, name: str) -> Result[None]:
        return cls._registry().resume(name)


    @classmethod
    def shutdown(cls) -> Result[None]:
        return cls._registry().shutdown()


    @classmethod
    def start(cls) -> Result[None]:
        return cls._registry().start()
