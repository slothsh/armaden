from __future__ import annotations

import asyncio
from enum import StrEnum
from pathlib import Path
from typing import cast, final, override

import pytest
from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.api.configurable import Configurable
from armaden.framework.api.error import Error
from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from armaden.framework.types.coroutine import AsyncStreamCallback
from armaden.framework.types.result import Result
from armaden.games.minecraft import (
    MinecraftServer,
    MinecraftServerBackend,
    MinecraftServerConfig,
    MinecraftServerError,
)
from armaden.games.minecraft.paper.paper_backend import PaperBackend, PaperBackendError
from armaden.games.minecraft.protocols import MinecraftServerBackendProtocol


class FakeBackendError(StrEnum):
    DISPATCH_FAILED = 'fake runtime dispatch failed'
    INSTALL_FAILED = 'fake backend installation failed'
    READY_FAILED = 'fake runtime readiness failed'


@final
class FakeBackend(MinecraftServerBackendProtocol):
    def __init__(self, config: MinecraftServerConfig) -> None:
        _ = config
        self.install_result: Result[None] = Success(None)
        self.launch_result: Result[list[str]] = Success(['java', '-jar', 'paper.jar'])


    @override
    async def install(self, runtime: TaskRuntimeProtocol) -> Result[None]:
        _ = runtime
        return self.install_result


    @override
    def launch_command(self) -> Result[list[str]]:
        return self.launch_result


    @override
    async def prepare(self) -> Result[None]:
        return Success(None)


    @override
    async def update(self, runtime: TaskRuntimeProtocol) -> Result[None]:
        _ = runtime
        return Success(None)


@final
class FailingInstallBackend(MinecraftServerBackendProtocol):
    def __init__(self, config: MinecraftServerConfig) -> None:
        _ = config


    @override
    async def install(self, runtime: TaskRuntimeProtocol) -> Result[None]:
        _ = runtime
        return Failure(Error(FakeBackendError.INSTALL_FAILED))


    @override
    def launch_command(self) -> Result[list[str]]:
        return Success(['java', '-jar', 'paper.jar'])


    @override
    async def prepare(self) -> Result[None]:
        return Success(None)


    @override
    async def update(self, runtime: TaskRuntimeProtocol) -> Result[None]:
        _ = runtime
        return Success(None)


@final
class FakeRuntime(TaskRuntimeProtocol):
    def __init__(self) -> None:
        self.dispatch_cwds: list[Path | str | None] = []
        self.dispatch_result: Result[str] = Success('')
        self.dispatched: list[list[str]] = []
        self.ready_count: int = 0
        self.ready_result: Result[None] = Success(None)


    @override
    async def dispatch_subprocess(
        self,
        argv: list[str],
        cwd: Path | str | None = None,
        handle_std_stream: AsyncStreamCallback | None = None,
    ) -> Result[str]:
        _ = handle_std_stream
        self.dispatched.append(list(argv))
        self.dispatch_cwds.append(cwd)
        return self.dispatch_result


    @property
    @override
    def graph_id(self) -> str:
        return 'graph-fake'


    @property
    @override
    def name(self) -> str:
        return 'runtime-fake'


    @override
    async def signal_ready(self) -> Result[None]:
        self.ready_count += 1
        return self.ready_result


    @override
    async def task_output(self, name: str) -> Result[object]:
        _ = name
        return Success(None)


def patch_backend_registry(
    monkeypatch: pytest.MonkeyPatch,
    backend: type[FakeBackend] | type[FailingInstallBackend],
) -> None:
    monkeypatch.setattr(
        MinecraftServer,
        '_BACKEND_REGISTRY',
        {MinecraftServerBackend.PAPER: backend},
    )


async def run_lifecycle(server: MinecraftServer, runtime: FakeRuntime) -> Result[None]:
    initialization = await server.initialize(runtime)
    if not is_successful(initialization):
        return initialization
    return await server.run(runtime)


def test_public_server_surface_exposes_typed_configurable() -> None:
    server = MinecraftServer()

    assert isinstance(server, Configurable)
    assert isinstance(server.config, dict)
    assert server.config.get('backend') == MinecraftServerBackend.PAPER


def test_server_accepts_partial_typed_config() -> None:
    config: MinecraftServerConfig = {'backend': MinecraftServerBackend.PAPER}
    server = MinecraftServer(config=config)

    java = server.config.get('java')
    assert java is not None
    assert java.get('version') == 25


def test_initialize_routes_paper_selection_to_backend() -> None:
    server = MinecraftServer(config={'backend': 'paper'})

    result = asyncio.run(server.initialize(FakeRuntime()))

    assert not is_successful(result)
    error = cast(Error, result.failure())
    assert error.kind == PaperBackendError.INSTALLATION_NOT_IMPLEMENTED


def test_initialize_reports_uninitialized_state_after_installation_failure() -> None:
    server = MinecraftServer()
    runtime = FakeRuntime()

    _ = asyncio.run(server.initialize(runtime))
    result = asyncio.run(server.status(runtime))

    assert is_successful(result)
    assert result.unwrap() == {
        'backend': MinecraftServerBackend.PAPER,
        'initialized': False,
    }


def test_initialize_rejects_unknown_backend_with_structured_error() -> None:
    server = MinecraftServer(config={'backend': 'curseforge'})

    result = asyncio.run(server.initialize(FakeRuntime()))

    assert not is_successful(result)
    error = cast(Error, result.failure())
    assert error.kind == MinecraftServerError.UNKNOWN_BACKEND
    assert error.details['backend'] == 'curseforge'
    assert error.details['supported'] == ['paper']


def test_initialize_rejects_paper_build_without_version() -> None:
    server = MinecraftServer(config={'paper': {'build': 130}})

    result = asyncio.run(server.initialize(FakeRuntime()))

    assert not is_successful(result)
    error = cast(Error, result.failure())
    assert error.kind == MinecraftServerError.INVALID_CONFIGURATION


def test_run_requires_completed_initialization() -> None:
    server = MinecraftServer()

    result = asyncio.run(server.run(FakeRuntime()))

    assert not is_successful(result)
    error = cast(Error, result.failure())
    assert error.kind == MinecraftServerError.NOT_INITIALIZED


def test_status_reports_backend_and_initialized_state() -> None:
    server = MinecraftServer()

    result = asyncio.run(server.status(FakeRuntime()))

    assert is_successful(result)
    assert result.unwrap() == {
        'backend': MinecraftServerBackend.PAPER,
        'initialized': False,
    }


def test_shutdown_succeeds_without_graceful_console_handling() -> None:
    server = MinecraftServer()

    result = asyncio.run(server.shutdown())

    assert is_successful(result)
    assert result.unwrap() is None


def test_paper_backend_exposes_backend_contract() -> None:
    backend = PaperBackend({})

    assert callable(backend.install)
    assert callable(backend.launch_command)
    assert callable(backend.prepare)
    assert callable(backend.update)


def test_initialize_succeeds_with_fake_backend(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    patch_backend_registry(monkeypatch, FakeBackend)
    runtime = FakeRuntime()
    server = MinecraftServer(config={'installation': {'directory': '/tmp/minecraft'}})

    result = asyncio.run(server.initialize(runtime))
    status = asyncio.run(server.status(runtime))

    assert is_successful(result)
    assert status.unwrap() == {
        'backend': MinecraftServerBackend.PAPER,
        'initialized': True,
    }


def test_run_dispatches_launch_command_and_returns_shutdown(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    patch_backend_registry(monkeypatch, FakeBackend)
    runtime = FakeRuntime()
    server = MinecraftServer(config={'installation': {'directory': '/tmp/minecraft'}})

    result = asyncio.run(run_lifecycle(server, runtime))

    assert is_successful(result)
    assert result.unwrap() is None
    assert runtime.dispatched == [['java', '-jar', 'paper.jar']]
    assert runtime.dispatch_cwds == ['/tmp/minecraft']
    assert runtime.ready_count == 1


def test_run_propagates_signal_ready_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    patch_backend_registry(monkeypatch, FakeBackend)
    runtime = FakeRuntime()
    runtime.ready_result = Failure(Error(FakeBackendError.READY_FAILED))
    server = MinecraftServer()

    result = asyncio.run(run_lifecycle(server, runtime))

    assert not is_successful(result)
    error = cast(Error, result.failure())
    assert error.kind == FakeBackendError.READY_FAILED
    assert runtime.dispatched == []


def test_run_propagates_dispatch_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    patch_backend_registry(monkeypatch, FakeBackend)
    runtime = FakeRuntime()
    runtime.dispatch_result = Failure(Error(FakeBackendError.DISPATCH_FAILED))
    server = MinecraftServer()

    result = asyncio.run(run_lifecycle(server, runtime))

    assert not is_successful(result)
    error = cast(Error, result.failure())
    assert error.kind == FakeBackendError.DISPATCH_FAILED
    assert runtime.dispatched == [['java', '-jar', 'paper.jar']]


def test_run_is_blocked_after_failed_initialization(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    patch_backend_registry(monkeypatch, FailingInstallBackend)
    runtime = FakeRuntime()
    server = MinecraftServer()

    async def scenario() -> tuple[Result[None], Result[None]]:
        initialization = await server.initialize(runtime)
        return initialization, await server.run(runtime)

    initialization, run_result = asyncio.run(scenario())

    assert not is_successful(initialization)
    initialization_error = cast(Error, initialization.failure())
    assert initialization_error.kind == FakeBackendError.INSTALL_FAILED

    assert not is_successful(run_result)
    run_error = cast(Error, run_result.failure())
    assert run_error.kind == MinecraftServerError.NOT_INITIALIZED


def test_reinitialization_clears_stale_backend_state(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    patch_backend_registry(monkeypatch, FakeBackend)
    runtime = FakeRuntime()
    server = MinecraftServer(config={'backend': 'paper'})

    async def scenario() -> tuple[Result[None], Result[None], Result[None]]:
        first = await server.initialize(runtime)
        patch_backend_registry(monkeypatch, FailingInstallBackend)
        second = await server.initialize(runtime)
        return first, second, await server.run(runtime)

    first, second, run_result = asyncio.run(scenario())

    assert is_successful(first)
    assert not is_successful(second)
    second_error = cast(Error, second.failure())
    assert second_error.kind == FakeBackendError.INSTALL_FAILED

    assert not is_successful(run_result)
    run_error = cast(Error, run_result.failure())
    assert run_error.kind == MinecraftServerError.NOT_INITIALIZED

    status = asyncio.run(server.status(runtime))
    assert status.unwrap() == {
        'backend': MinecraftServerBackend.PAPER,
        'initialized': False,
    }