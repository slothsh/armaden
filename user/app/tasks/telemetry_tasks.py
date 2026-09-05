import asyncio
import logging
import platform
from typing import cast, override

from returns.pipeline import is_successful
from returns.result import Success

from armaden.framework.api.task import (
    Task,
    TaskPolicyData,
    TaskRestartPolicy,
    TaskRuntimeProtocol,
)
from armaden.framework.types.result import Result

logger = logging.getLogger('app.tasks.telemetry')


class CollectServerTelemetryTask(Task):
    name: str = 'collect_server_telemetry'
    description: str | None = 'Collects runtime telemetry for the Arma Reforger server process'
    _policy: TaskPolicyData = TaskPolicyData(timeout=10.0, priority=10)

    @override
    async def run(
        self,
        runtime: TaskRuntimeProtocol,
        **kwargs: object,
    ) -> Result[dict[str, object]]:
        _ = runtime
        _ = kwargs
        await asyncio.sleep(0.05)
        telemetry: dict[str, object] = {
            'hostname': platform.node(),
            'cpu_percent': 12.4,
            'memory_mb': 4096,
            'players': 0,
            'uptime_seconds': 0,
        }
        logger.info('Collected telemetry: %s', telemetry)
        return Success(telemetry)


class FormatTelemetryReportTask(Task):
    name: str = 'format_telemetry_report'
    description: str | None = 'Formats raw telemetry into a human-readable report'
    depends_on: list[str | type[object]] | None = ['collect_server_telemetry']
    _policy: TaskPolicyData = TaskPolicyData(timeout=5.0)

    @override
    async def run(
        self,
        runtime: TaskRuntimeProtocol,
        **kwargs: object,
    ) -> Result[dict[str, object]]:
        _ = kwargs
        raw_result = await runtime.task_output('collect_server_telemetry')
        raw = cast(dict[str, object], raw_result.unwrap())
        report: dict[str, object] = {
            'summary': f"{raw['hostname']} | cpu={raw['cpu_percent']}% | mem={raw['memory_mb']}MB",
            'players': raw['players'],
            'healthy': True,
        }
        logger.info('Formatted telemetry report: %s', report['summary'])
        return Success(report)


class TelemetryReadinessProbeTask(Task):
    name: str = 'telemetry_readiness_probe'
    description: str | None = 'Long-running probe that signals readiness once the telemetry channel is live'
    long_running: bool = True
    _policy: TaskPolicyData = TaskPolicyData(
        ready_timeout=15.0,
        restart=TaskRestartPolicy.ON_FAILURE,
    )

    @override
    async def run(
        self,
        runtime: TaskRuntimeProtocol,
        **kwargs: object,
    ) -> Result[None]:
        _ = kwargs
        logger.info('Telemetry readiness probe starting; signalling ready')
        _ = await runtime.signal_ready()
        await asyncio.sleep(0.05)
        return Success(None)


class TelemetryAlertTask(Task):
    name: str = 'telemetry_alert'
    description: str | None = 'Consumes the readiness signal and emits an alert banner'
    awaits: list[str | type[object]] | None = ['telemetry_readiness_probe']
    _policy: TaskPolicyData = TaskPolicyData(timeout=5.0)

    @override
    async def run(
        self,
        runtime: TaskRuntimeProtocol,
        **kwargs: object,
    ) -> Result[dict[str, object]]:
        _ = kwargs
        readiness = await runtime.task_output('telemetry_readiness_probe')
        if is_successful(readiness):
            alert: dict[str, object] = {
                'level': 'info',
                'message': 'Telemetry channel is live',
            }
        else:
            alert = {
                'level': 'warning',
                'message': 'Telemetry channel failed readiness',
            }
        logger.info('Telemetry alert: %s', alert['message'])
        return Success(alert)
