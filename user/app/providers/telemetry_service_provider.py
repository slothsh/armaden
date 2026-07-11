import asyncio
import logging

from returns.result import Success

from armaden.framework.classes.service_provider import ServiceProvider
from armaden.framework.enums.restart_policy import RestartPolicy
from armaden.framework.facades import App
from armaden.framework.runtime.task_builder import TaskBuilder
from armaden.framework.utils.types import Result
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
    name = 'telemetry'

    def register(self) -> Result[None]:
        return Success(None)

    def boot(self) -> Result[None]:
        supervisor = App.supervisor()

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
            .restart(RestartPolicy.NEVER)
            .shared_thread()
            .build()
        )
        supervisor.concurrency().pipeline(collect, format_report, banner_task).submit()

        probe = TelemetryReadinessProbeTask()
        alert = TelemetryAlertTask()
        supervisor.submit([probe, alert])

        try:
            supervisor.process().command('telemetry_hostinfo', ['uname', '-s', '-n']).timeout(5.0).submit()
        except Exception as exception:
            logger.warning('Telemetry hostinfo process failed: %s', exception)

        return Success(None)
