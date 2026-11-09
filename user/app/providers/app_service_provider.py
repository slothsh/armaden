import logging
from enum import StrEnum
from typing import cast, override

from returns.result import Failure, Success

from armaden.framework.api.error import Error
from armaden.framework.api.service_provider import ServiceProvider
from armaden.framework.api.supervisor import TaskGraphData
from armaden.framework.api.task import TaskBuilder
from armaden.framework.protocols.configuration_protocol import ConfigurationProtocol
from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.supervisor_protocol import SupervisorProtocol
from armaden.framework.support.env import Env
from armaden.framework.types.result import Result
from armaden.framework.types.task import TaskCallback, TaskStatusCallback
from armaden.games.arma_reforger import (
    ArmaReforgerServer,
    ArmaReforgerServerConfig,
)
from armaden.games.minecraft import MinecraftServer, MinecraftServerConfig

logger = logging.getLogger(__name__)

_ARMA_REFORGER = 'arma_reforger'
_MINECRAFT = 'minecraft'
_SUPPORTED_GAMES = frozenset({_ARMA_REFORGER, _MINECRAFT})

_MINECRAFT_READY_TIMEOUT = 600.0


class AppServiceProvider(ServiceProvider):
    name: str = 'arma_reforger'
    server: ArmaReforgerServer | MinecraftServer

    _game: str

    def __init__(self, container: ContainerProtocol) -> None:
        super().__init__(container)
        self._game = cast(str, Env.string('APP_GAME', _ARMA_REFORGER))


    @override
    def register(self) -> Result[None]:
        if self._game == _MINECRAFT:
            return self._register_minecraft()

        if self._game == _ARMA_REFORGER:
            return self._register_arma_reforger()

        return Success(None)


    @override
    def boot(self) -> Result[None]:
        if self._game not in _SUPPORTED_GAMES:
            return Failure(
                Error(
                    AppServiceProviderError.UNSUPPORTED_GAME,
                    details={
                        'game': self._game,
                        'selector': 'APP_GAME',
                        'supported': sorted(_SUPPORTED_GAMES),
                    },
                )
            )

        if self._game == _MINECRAFT:
            return self._boot_minecraft()

        return self._boot_arma_reforger()


    def _boot_arma_reforger(self) -> Result[None]:
        server = cast(ArmaReforgerServer, self.server)

        server_task = (
            TaskBuilder()
            .name('arma_reforger_server')
            .description('Manages the Arma Reforger dedicated server lifecycle')
            .on_initialize(cast(TaskCallback, server.initialize))
            .on_run(cast(TaskCallback, server.run))
            .on_shutdown(cast(TaskCallback, server.shutdown))
            .on_status(cast(TaskStatusCallback, server.status))
            .exclusive_thread()
            .long_running()
            .ready_timeout(120.0)
            .build()
        )

        rcon_task = (
            TaskBuilder()
            .name('arma_reforger_rcon')
            .description('Arma Reforger dedicated server remote console')
            .on_initialize(cast(TaskCallback, server.initialize_rcon_client))
            .on_run(cast(TaskCallback, server.run_rcon_client))
            .on_shutdown(cast(TaskCallback, server.shutdown_rcon_client))
            .awaits('arma_reforger_server')
            .exclusive_thread()
            .long_running()
            .ready_timeout(30.0)
            .build()
        )

        supervisor = cast(
            SupervisorProtocol[TaskGraphData],
            self.app.make(SupervisorProtocol),
        )
        _ = supervisor.submit([server_task, rcon_task])

        return Success(None)


    def _boot_minecraft(self) -> Result[None]:
        server = cast(MinecraftServer, self.server)

        server_task = (
            TaskBuilder()
            .name('minecraft_server')
            .description('Manages the Minecraft dedicated server lifecycle')
            .on_initialize(cast(TaskCallback, server.initialize))
            .on_run(cast(TaskCallback, server.run))
            .on_shutdown(cast(TaskCallback, server.shutdown))
            .on_status(cast(TaskStatusCallback, server.status))
            .exclusive_thread()
            .long_running()
            .ready_timeout(_MINECRAFT_READY_TIMEOUT)
            .build()
        )

        supervisor = cast(
            SupervisorProtocol[TaskGraphData],
            self.app.make(SupervisorProtocol),
        )
        _ = supervisor.submit([server_task])

        return Success(None)


    def _register_arma_reforger(self) -> Result[None]:
        configuration = cast(
            ConfigurationProtocol,
            self.app.make(ConfigurationProtocol),
        )
        arma_config = cast(
            ArmaReforgerServerConfig,
            configuration.get('arma_reforger', {}),
        )

        self.server = ArmaReforgerServer(config=arma_config)

        _ = self.app.instance(ArmaReforgerServer, cast(object, self.server))

        return Success(None)


    def _register_minecraft(self) -> Result[None]:
        configuration = cast(
            ConfigurationProtocol,
            self.app.make(ConfigurationProtocol),
        )
        minecraft_config = cast(
            MinecraftServerConfig,
            configuration.get('minecraft', {}),
        )

        self.server = MinecraftServer(config=minecraft_config)

        _ = self.app.instance(MinecraftServer, cast(object, self.server))

        return Success(None)


# --- Internal Types ----------------------------------------------------------

class AppServiceProviderError(StrEnum):
    UNSUPPORTED_GAME = 'the requested game application is not supported'