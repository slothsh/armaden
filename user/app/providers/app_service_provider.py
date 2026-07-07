from returns.result import Success

from armaden.framework.classes.service_provider import ServiceProvider
from armaden.framework.classes.task import TaskBuilder
from armaden.framework.facades import App, config
from armaden.framework.utils.types import Result
from armaden.games.arma_reforger import ArmaReforgerServer


class AppServiceProvider(ServiceProvider):
    name = 'arma_reforger'

    def __init__(self):
        self.server = ArmaReforgerServer(config=config('arma_reforger'))


    def register(self) -> Result[None]:
        App.instance(ArmaReforgerServer, self.server)
        return Success(None)


    def boot(self) -> Result[None]:
        server_task = (
            TaskBuilder()
            .name('arma_reforger_server')
            .description('Manages the Arma Reforger dedicated server lifecycle')
            .on_initialize(self.server.initialize)
            .on_run(self.server.run)
            .on_shutdown(self.server.shutdown)
            .on_status(self.server.status)
            .exclusive_thread()
            .build()
        )

        rcon_task = (
            TaskBuilder()
            .name('arma_reforger_rcon')
            .description('Arma Reforger dedicated server remote console')
            .on_initialize(self.server.initialize_rcon_client)
            .on_run(self.server.run_rcon_client)
            .on_shutdown(self.server.shutdown_rcon_client)
            .exclusive_thread()
            .build()
        )

        App.supervisor().add_task(server_task)
        App.supervisor().add_task(rcon_task)

        return Success(None)
