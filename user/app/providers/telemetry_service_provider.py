import asyncio
import logging
from typing import cast, override

from returns.result import Success

from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.supervisor_protocol import SupervisorProtocol
from armaden.framework.api.service_provider import ServiceProvider
from armaden.framework.api.supervisor import TaskGraphData
from armaden.framework.api.task import (
    ProcessBuilder,
    TaskBuilder,
    TaskRestartPolicy,
)
from armaden.framework.types.result import Result
from app.tasks.telemetry_tasks import (
    CollectServerTelemetryTask,
    FormatTelemetryReportTask,
    TelemetryAlertTask,
    TelemetryReadinessProbeTask,
)

logger = logging.getLogger('app.providers.telemetry_service_provider')


async def _emit_banner() -> Result[None]:
    await asyncio.sleep(0.02)
    logger.info('Telemetry banner emitted')
    return Success(None)


class TelemetryServiceProvider(ServiceProvider):
    name: str = 'telemetry'

    def __init__(self, container: ContainerProtocol) -> None:
        super().__init__(container)


    @override
    def register(self) -> Result[None]:
        return Success(None)


    @override
    def boot(self) -> Result[None]:
        supervisor = cast(
            SupervisorProtocol[TaskGraphData],
            self.app.make(SupervisorProtocol),
        )

        collect = CollectServerTelemetryTask()
        format_report = FormatTelemetryReportTask()

        banner_task = (
            TaskBuilder()
            .name('telemetry_banner')
            .description('Emits a startup banner once telemetry is prepared')
            .on_run(_emit_banner)
            .timeout(5.0)
            .retries(2, delay=0.1, backoff=2.0)
            .priority(5)
            .restart(TaskRestartPolicy.NEVER)
            .shared_thread()
            .build()
        )
        _ = supervisor.submit([collect, format_report, banner_task])

        probe = TelemetryReadinessProbeTask()
        alert = TelemetryAlertTask()
        _ = supervisor.submit([probe, alert])

        try:
            _ = ProcessBuilder(
                supervisor,
                'telemetry_hostinfo',
                ['uname', '-s', '-n'],
            ).timeout(5.0).submit()
        except Exception as exception:
            logger.warning('Telemetry hostinfo process failed: %s', exception)

        return Success(None)
