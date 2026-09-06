from __future__ import annotations

from typing import override

from returns.pipeline import is_successful
from returns.result import Success

from armaden.framework.protocols.class_discovery_protocol import ClassDiscoveryProtocol
from armaden.framework.protocols.scheduled_job_discovery_protocol import (
    ScheduledJobDiscoveryProtocol,
)
from armaden.framework.runtime.schedule.scheduled_job import ScheduledJob
from armaden.framework.types.result import Result


class ScheduledJobDiscovery(ScheduledJobDiscoveryProtocol):
    def __init__(self, class_discovery: ClassDiscoveryProtocol) -> None:
        self._class_discovery: ClassDiscoveryProtocol = class_discovery


    @override
    def discover(self, paths: list[str]) -> Result[list[type[object]]]:
        result = self._class_discovery.discover(paths)
        if not is_successful(result):
            return result.map(lambda _: [])
        return Success([
            job_type
            for job_type in result.unwrap()
            if self._is_scheduled_job(job_type)
        ])


    @staticmethod
    def _is_scheduled_job(value: type[object]) -> bool:
        return issubclass(value, ScheduledJob) and value is not ScheduledJob
