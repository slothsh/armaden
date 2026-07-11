import asyncio
import logging
import platform

from returns.pipeline import is_successful
from returns.result import Success

from armaden.framework.enums.restart_policy import RestartPolicy
from armaden.framework.enums.task_threading_policy import TaskThreadingPolicy
from armaden.framework.protocols.task import Lifecycle, Pipeline
from armaden.framework.protocols.task_runtime import TaskRuntimeInterface
from armaden.framework.runtime.task import Task, TaskPolicy
from armaden.framework.utils.types import Result

logger = logging.getLogger('app.tasks.telemetry')


class CollectServerTelemetryTask(Task):
    name = 'collect_server_telemetry'
    description = 'Collects runtime telemetry for the Arma Reforger server process'
    policy = TaskPolicy(timeout=10.0, priority=10)

    async def run(self) -> Result[dict]:
        await asyncio.sleep(0.05)
        telemetry = {
            'hostname': platform.node(),
            'cpu_percent': 12.4,
            'memory_mb': 4096,
            'players': 0,
            'uptime_seconds': 0,
        }
        logger.info('Collected telemetry: %s', telemetry)
        return Success(telemetry)


class FormatTelemetryReportTask(Task):
    name = 'format_telemetry_report'
    description = 'Formats raw telemetry into a human-readable report'
    depends_on = [CollectServerTelemetryTask]
    policy = TaskPolicy(timeout=5.0)

    async def run(self, telemetry: Pipeline[CollectServerTelemetryTask, dict]) -> Result[dict]:
        raw = telemetry.unwrap() if hasattr(telemetry, 'unwrap') else telemetry
        report = {
            'summary': f"{raw['hostname']} | cpu={raw['cpu_percent']}% | mem={raw['memory_mb']}MB",
            'players': raw['players'],
            'healthy': True,
        }
        logger.info('Formatted telemetry report: %s', report['summary'])
        return Success(report)


class TelemetryReadinessProbeTask(Task):
    name = 'telemetry_readiness_probe'
    description = 'Long-running probe that signals readiness once the telemetry channel is live'
    long_running = True
    policy = TaskPolicy(ready_timeout=15.0, restart=RestartPolicy.ON_FAILURE)

    async def run(self, runtime: TaskRuntimeInterface) -> Result[None]:
        logger.info('Telemetry readiness probe starting; signalling ready')
        await runtime.signal_ready()
        await asyncio.sleep(0.05)
        return Success(None)


class TelemetryAlertTask(Task):
    name = 'telemetry_alert'
    description = 'Consumes the readiness signal and emits an alert banner'
    awaits = [TelemetryReadinessProbeTask]
    policy = TaskPolicy(timeout=5.0)

    async def run(self, readiness: Lifecycle[TelemetryReadinessProbeTask]) -> Result[dict]:
        if is_successful(readiness):
            alert = {'level': 'info', 'message': 'Telemetry channel is live'}
        else:
            alert = {'level': 'warning', 'message': 'Telemetry channel failed readiness'}
        logger.info('Telemetry alert: %s', alert['message'])
        return Success(alert)
