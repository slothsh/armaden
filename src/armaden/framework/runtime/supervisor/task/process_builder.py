from __future__ import annotations

from pathlib import Path
from typing import override

from armaden.framework.protocols.process_builder_protocol import ProcessBuilderProtocol
from armaden.framework.protocols.supervisor_protocol import SupervisorProtocol
from armaden.framework.runtime.supervisor.task.dto.task_graph_data import TaskGraphData
from armaden.framework.runtime.supervisor.task.dto.task_policy_data import TaskPolicyData
from armaden.framework.runtime.supervisor.task.enums.task_restart_policy import TaskRestartPolicy
from armaden.framework.runtime.supervisor.task.enums.task_threading_policy import TaskThreadingPolicy
from armaden.framework.runtime.supervisor.task.process_task import ProcessTask
from armaden.framework.types.process import ProcessStreamCallback


class ProcessBuilder(ProcessBuilderProtocol[TaskThreadingPolicy, TaskGraphData]):
    def __init__(
        self,
        supervisor: SupervisorProtocol[TaskGraphData],
        name: str,
        argv: list[str],
    ) -> None:
        self._argv: list[str] = list(argv)
        self._awaits: list[str | type[object]] = []
        self._auto_restart: bool = False
        self._cwd: Path | str | None = None
        self._depends_on: list[str | type[object]] = []
        self._env: dict[str, str] = {}
        self._long_running: bool = False
        self._name: str = name
        self._on_stderr: ProcessStreamCallback | None = None
        self._on_stdout: ProcessStreamCallback | None = None
        self._restart_policy: TaskRestartPolicy | None = None
        self._supervisor: SupervisorProtocol[TaskGraphData] = supervisor
        self._timeout: float | None = None


    @override
    def awaits(self, *references: str | type[object]) -> ProcessBuilder:
        self._awaits.extend(references)
        return self


    @override
    def auto_restart(self) -> ProcessBuilder:
        self._auto_restart = True
        self._restart_policy = TaskRestartPolicy.ALWAYS
        return self


    @override
    def build(self) -> ProcessTask:
        restart = self._restart_policy
        if restart is None:
            restart = TaskRestartPolicy.ALWAYS if self._auto_restart else TaskRestartPolicy.NEVER
        return ProcessTask(
            name=self._name,
            argv=list(self._argv),
            cwd=self._cwd,
            env=dict(self._env),
            on_stderr=self._on_stderr,
            on_stdout=self._on_stdout,
            policy=TaskPolicyData(timeout=self._timeout, restart=restart),
            depends_on=list(self._depends_on),
            awaits=list(self._awaits),
            long_running=self._long_running,
        )


    @override
    def cwd(self, path: Path | str) -> ProcessBuilder:
        self._cwd = path
        return self


    @override
    def depends_on(self, *references: str | type[object]) -> ProcessBuilder:
        self._depends_on.extend(references)
        return self


    @override
    def env(self, **values: str) -> ProcessBuilder:
        self._env.update(values)
        return self


    @override
    def long_running(self) -> ProcessBuilder:
        self._long_running = True
        return self


    @override
    def on_stderr(self, callback: ProcessStreamCallback) -> ProcessBuilder:
        self._on_stderr = callback
        return self


    @override
    def on_stdout(self, callback: ProcessStreamCallback) -> ProcessBuilder:
        self._on_stdout = callback
        return self


    @override
    def submit(self) -> TaskGraphData:
        return self._supervisor.submit([self.build()])


    @override
    def timeout(self, seconds: float) -> ProcessBuilder:
        self._timeout = seconds
        return self