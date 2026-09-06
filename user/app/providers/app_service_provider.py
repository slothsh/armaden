from typing import cast, override

from returns.result import Success

from armaden.framework.protocols.configuration_protocol import ConfigurationProtocol
from armaden.framework.protocols.container_protocol import ContainerProtocol
from armaden.framework.protocols.supervisor_protocol import SupervisorProtocol
from armaden.framework.api.service_provider import ServiceProvider
from armaden.framework.api.supervisor import TaskGraphData
from armaden.framework.api.task import TaskBuilder
from armaden.framework.types.result import Result
from armaden.framework.types.task import TaskCallback, TaskStatusCallback
from armaden.games.arma_reforger import (
    ArmaReforgerRconClient,
    ArmaReforgerServer,
    ArmaReforgerServerConfig,
)


class AppServiceProvider(ServiceProvider):
    name: str = 'arma_reforger'
    server: ArmaReforgerServer

    def __init__(self, container: ContainerProtocol) -> None:
        super().__init__(container)


    @override
    def register(self) -> Result[None]:
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
        _ = self.app.instance(ArmaReforgerRconClient, cast(object, self.server.rcon_client))

        return Success(None)


    @override
    def boot(self) -> Result[None]:
        server_task = (
            TaskBuilder()
            .name('arma_reforger_server')
            .description('Manages the Arma Reforger dedicated server lifecycle')
            .on_initialize(cast(TaskCallback, self.server.initialize))
            .on_run(cast(TaskCallback, self.server.run))
            .on_shutdown(cast(TaskCallback, self.server.shutdown))
            .on_status(cast(TaskStatusCallback, self.server.status))
            .exclusive_thread()
            .long_running()
            .ready_timeout(120.0)
            .build()
        )

        rcon_task = (
            TaskBuilder()
            .name('arma_reforger_rcon')
            .description('Arma Reforger dedicated server remote console')
            .on_initialize(cast(TaskCallback, self.server.initialize_rcon_client))
            .on_run(cast(TaskCallback, self.server.run_rcon_client))
            .on_shutdown(cast(TaskCallback, self.server.shutdown_rcon_client))
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
