import asyncio
import logging
import signal as signal_module
from pathlib import Path
from typing import TYPE_CHECKING, Any

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.enums.restart_policy import RestartPolicy
from armaden.framework.errors import Error
from armaden.framework.runtime.errors import TaskError
from armaden.framework.runtime.task import Task
from armaden.framework.runtime.task_graph import TaskGraph
from armaden.framework.utils.types import AsyncStreamCallback, Result

if TYPE_CHECKING:
    from armaden.framework.runtime.supervisor import Supervisor

logger = logging.getLogger(__name__)


class SubprocessHandle:
    STARTING = 'starting'
    RUNNING = 'running'
    STOPPING = 'stopping'
    STOPPED = 'stopped'

    def __init__(self, name: str) -> None:
        self.name = name
        self.process: asyncio.subprocess.Process | None = None
        self.pid: int | None = None
        self.state = self.STARTING

    async def start(self, argv: list[str], cwd: Path | str | None = None, env: dict | None = None) -> Result[None]:
        try:
            import os
            full_env = os.environ.copy()
            if env:
                full_env.update(env)
            self.process = await asyncio.create_subprocess_exec(
                argv[0], *argv[1:],
                cwd=cwd,
                env=full_env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            self.pid = self.process.pid
            self.state = self.RUNNING
            return Success(None)
        except Exception as exception:
            return Failure(Error(TaskError.SUBPROCESS_ERROR, details={'name': self.name, 'error': str(exception)}))

    async def stop(self, timeout: float = 30.0) -> Result[None]:
        if self.process is None or self.state == self.STOPPED:
            return Success(None)
        self.state = self.STOPPING
        try:
            self.process.send_signal(signal_module.SIGINT)
            try:
                await asyncio.wait_for(self.process.wait(), timeout=timeout)
            except asyncio.TimeoutError:
                logger.warning("Process '%s' did not exit on SIGINT; escalating to SIGTERM", self.name)
                self.process.terminate()
                try:
                    await asyncio.wait_for(self.process.wait(), timeout=timeout)
                except asyncio.TimeoutError:
                    logger.warning("Process '%s' did not exit on SIGTERM; escalating to SIGKILL", self.name)
                    self.process.kill()
                    await self.process.wait()
        except ProcessLookupError:
            pass
        finally:
            self.state = self.STOPPED
            self.process = None
            self.pid = None
        return Success(None)

    async def restart(self) -> Result[None]:
        await self.stop()
        return await self._start_again()

    async def _start_again(self) -> Result[None]:
        raise NotImplementedError('SubprocessHandle.restart requires stored argv')

    def send_signal(self, sig: int) -> None:
        if self.process is not None:
            self.process.send_signal(sig)


class _ProcessTask(Task):
    def __init__(
        self,
        name: str,
        argv: list[str],
        cwd: Path | str | None = None,
        env: dict | None = None,
        on_stdout: AsyncStreamCallback | None = None,
        on_stderr: AsyncStreamCallback | None = None,
        long_running: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(name=name, long_running=long_running, **kwargs)
        self._argv = list(argv)
        self._cwd = cwd
        self._env = env
        self._on_stdout = on_stdout
        self._on_stderr = on_stderr
        self._handle: SubprocessHandle | None = None

    @property
    def handle(self) -> SubprocessHandle | None:
        return self._handle

    async def run(self) -> Result[Any]:
        self._handle = SubprocessHandle(self.name or 'process')
        start_result = await self._handle.start(self._argv, cwd=self._cwd, env=self._env)
        if not is_successful(start_result):
            return start_result

        if self.long_running:
            runtime = self._runtime_ref
            if runtime is not None:
                await runtime.signal_ready()

        pump_tasks: list[asyncio.Task] = []
        if self._on_stdout is not None and self._handle.process is not None and self._handle.process.stdout is not None:
            pump_tasks.append(asyncio.create_task(self._drain(self._handle.process.stdout, self._on_stdout)))
        if self._on_stderr is not None and self._handle.process is not None and self._handle.process.stderr is not None:
            pump_tasks.append(asyncio.create_task(self._drain(self._handle.process.stderr, self._on_stderr)))

        return_code = await self._handle.process.wait()
        await asyncio.gather(*pump_tasks, return_exceptions=True)

        if return_code == 0:
            return Success(return_code)
        return Failure(Error(TaskError.SUBPROCESS_ERROR, details={'name': self.name, 'exit_code': return_code}))

    async def shutdown(self) -> Result[None]:
        if self._handle is not None:
            await self._handle.stop()
        return Success(None)

    async def _drain(self, stream, callback: AsyncStreamCallback) -> None:
        try:
            while True:
                line = await stream.readline()
                if not line:
                    break
                text = line.decode(errors='replace').strip()
                if text:
                    result = callback(text)
                    if hasattr(result, '__await__'):
                        await result
        except asyncio.CancelledError:
            raise

    _runtime_ref: Any = None


class ProcessBuilder:
    def __init__(self, supervisor: 'Supervisor', name: str, argv: list[str]) -> None:
        self._supervisor = supervisor
        self._name = name
        self._argv = list(argv)
        self._cwd: Path | str | None = None
        self._env: dict | None = None
        self._on_stdout: AsyncStreamCallback | None = None
        self._on_stderr: AsyncStreamCallback | None = None
        self._timeout: float | None = None
        self._depends_on: list[str | type] = []
        self._awaits: list[str | type] = []
        self._long_running = False
        self._restart_policy: RestartPolicy | None = None
        self._auto_restart = False

    def cwd(self, path: Path | str) -> 'ProcessBuilder':
        self._cwd = path
        return self

    def env(self, **kwargs) -> 'ProcessBuilder':
        self._env = {**(self._env or {}), **kwargs}
        return self

    def on_stdout(self, callback: AsyncStreamCallback) -> 'ProcessBuilder':
        self._on_stdout = callback
        return self

    def on_stderr(self, callback: AsyncStreamCallback) -> 'ProcessBuilder':
        self._on_stderr = callback
        return self

    def auto_restart(self) -> 'ProcessBuilder':
        self._auto_restart = True
        self._restart_policy = RestartPolicy.ALWAYS
        return self

    def timeout(self, seconds: float) -> 'ProcessBuilder':
        self._timeout = seconds
        return self

    def depends_on(self, *names: str | type) -> 'ProcessBuilder':
        self._depends_on.extend(names)
        return self

    def awaits(self, *names: str | type) -> 'ProcessBuilder':
        self._awaits.extend(names)
        return self

    def long_running(self) -> 'ProcessBuilder':
        self._long_running = True
        return self

    def build(self) -> _ProcessTask:
        restart = self._restart_policy if self._restart_policy is not None else RestartPolicy.NEVER
        from armaden.framework.runtime.task import TaskPolicy
        policy = TaskPolicy(timeout=self._timeout, restart=restart)
        return _ProcessTask(
            name=self._name,
            argv=self._argv,
            cwd=self._cwd,
            env=self._env,
            on_stdout=self._on_stdout,
            on_stderr=self._on_stderr,
            long_running=self._long_running,
            depends_on=list(self._depends_on),
            awaits=list(self._awaits),
            policy=policy,
        )

    def submit(self) -> TaskGraph:
        return self._supervisor.submit([self.build()])
