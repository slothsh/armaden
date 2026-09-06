from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import cast, override

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.protocols.class_discovery_protocol import ClassDiscoveryProtocol
from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.core_application_protocol import CoreApplicationProtocol
from armaden.framework.protocols.queue_resolver_protocol import QueueResolverProtocol
from armaden.framework.protocols.schedule_registry_protocol import ScheduleRegistryProtocol
from armaden.framework.protocols.supervisor_protocol import SupervisorProtocol
from armaden.framework.runtime.error.error import Error
from armaden.framework.runtime.schedule.exceptions.schedule_error import ScheduleError
from armaden.framework.facades.schedule_facade import ScheduleFacade
from armaden.framework.runtime.schedule.schedule_dispatcher import ScheduleDispatcher
from armaden.framework.runtime.schedule.schedule_registry import ScheduleRegistry
from armaden.framework.runtime.schedule.scheduled_event import ScheduledEvent
from armaden.framework.runtime.schedule.scheduled_job_discovery import ScheduledJobDiscovery
from armaden.framework.runtime.service_provider.service_provider import ServiceProvider
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraphData
from armaden.framework.types.result import Result
from armaden.framework.runtime.schedule.enums import ScheduledEventKind

logger = logging.getLogger(__name__)


class ScheduleServiceProvider(ServiceProvider):
    name: str = 'schedule'

    def __init__(self, container: ContainerProtocol) -> None:
        super().__init__(container)
        self._registry: ScheduleRegistry | None = None


    @override
    def boot(self) -> Result[None]:
        if self._registry is None:
            result = self._create_registry()
            if isinstance(result, Failure):
                return result
        registry = self._registry
        if registry is None:
            return Success(None)
        application = cast(
            CoreApplicationProtocol[TaskGraphData],
            self._container.make('app'),
        )
        raw_configuration = application.config('schedule', {})
        configuration: Mapping[str, object] = (
            cast(Mapping[str, object], raw_configuration)
            if isinstance(raw_configuration, Mapping)
            else cast(Mapping[str, object], {})
        )
        discovery_configuration = self._discovery_configuration(configuration)
        if discovery_configuration.get('enabled') is not True:
            logger.debug('Scheduled job discovery is disabled')
            return Success(None)

        paths = self._paths(discovery_configuration.get('paths'))
        discovery = ScheduledJobDiscovery(
            cast(ClassDiscoveryProtocol, self._container.make(ClassDiscoveryProtocol)),
        )
        result = discovery.discover(paths)
        if not is_successful(result):
            return result.map(lambda _: None)

        registered = 0
        for job_type in result.unwrap():
            schedule = getattr(job_type, 'schedule', None)
            if not isinstance(schedule, Mapping):
                continue
            registration = self._register_job(job_type, cast(Mapping[str, object], schedule))
            if isinstance(registration, Failure):
                return registration
            registered += 1

        logger.info(
            'Registered %d discovered scheduled jobs from %d path(s)',
            registered,
            len(paths),
        )
        return Success(None)


    @override
    def register(self) -> Result[None]:
        return Success(None)


    def _create_registry(self) -> Result[None]:
        supervisor = cast(
            SupervisorProtocol[object],
            self._container.make(SupervisorProtocol),
        )
        queue_resolver = cast(
            QueueResolverProtocol,
            self._container.make(QueueResolverProtocol),
        )
        scheduler = supervisor.ensure_scheduler()
        application = cast(CoreApplicationProtocol[TaskGraphData], self._container.make('app'))
        raw_defaults = application.config('schedule.defaults', {})
        defaults: Mapping[str, object] = (
            cast(Mapping[str, object], raw_defaults)
            if isinstance(raw_defaults, Mapping)
            else cast(Mapping[str, object], {})
        )
        ScheduleFacade.configure_defaults(defaults)
        dispatcher = ScheduleDispatcher(queue_resolver, supervisor)
        registry = ScheduleRegistry(
            scheduler,
            dispatcher.dispatch,
            timezone=self._timezone(),
        )
        self._registry = registry
        _ = self._container.instance(ScheduleRegistryProtocol, registry)
        return Success(None)


    def _discovery_configuration(
        self,
        configuration: Mapping[str, object],
    ) -> Mapping[str, object]:
        jobs = configuration.get('jobs', {})
        jobs_mapping: Mapping[str, object] = (
            cast(Mapping[str, object], jobs)
            if isinstance(jobs, Mapping)
            else cast(Mapping[str, object], {})
        )
        discovery = jobs_mapping.get('discovery', {})
        return cast(Mapping[str, object], discovery) if isinstance(discovery, Mapping) else {}


    def _paths(self, value: object) -> list[str]:
        if not isinstance(value, list):
            return ['app/jobs']
        values = cast(list[object], value)
        return [item for item in values if isinstance(item, str)]


    def _register_job(
        self,
        job_type: type[object],
        schedule: Mapping[str, object],
    ) -> Result[None]:
        registry = self._registry
        if registry is None:
            return Success(None)
        event = ScheduledEvent(ScheduledEventKind.JOB, job_type, registry.register)
        name = schedule.get('name')
        if isinstance(name, str):
            _ = event.name(name)
        frequency = schedule.get('frequency', 'every_minute')
        interval = schedule.get('interval')
        if interval is not None and isinstance(interval, (int, float)) and not isinstance(interval, bool):
            _ = event.every_seconds(interval)
        else:
            if not isinstance(frequency, str):
                return Failure(Error(ScheduleError.INVALID_FREQUENCY))
            method = getattr(event, frequency, None)
            if not callable(method):
                return Failure(Error(ScheduleError.INVALID_FREQUENCY, details={'frequency': frequency}))
            _ = method()
        queue = schedule.get('queue', getattr(job_type, 'queue', None))
        if isinstance(queue, str):
            _ = event.on_queue(queue)
        connection = schedule.get('connection', getattr(job_type, 'connection', None))
        if isinstance(connection, str):
            _ = event.on_connection(connection)
        priority = schedule.get('priority', getattr(job_type, 'priority', None))
        if isinstance(priority, int):
            _ = event.priority(priority)
        tags = getattr(job_type, 'tags', ())
        if isinstance(tags, (list, tuple)):
            values = cast(list[object] | tuple[object, ...], tags)
            _ = event.tag(*[tag for tag in values if isinstance(tag, (str, type))])
        result = event.submit()
        _ = result
        return Success(None)


    def _timezone(self) -> str:
        application = cast(CoreApplicationProtocol[TaskGraphData], self._container.make('app'))
        raw_configuration = application.config('schedule.defaults.timezone', 'UTC')
        return raw_configuration if isinstance(raw_configuration, str) else 'UTC'
