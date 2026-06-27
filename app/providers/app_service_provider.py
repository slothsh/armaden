from returns.result import Success

from armaden.framework.classes.service_provider import ServiceProvider
from armaden.framework.classes.task import TaskBuilder
from armaden.framework.facades import app
from armaden.framework.utils.types import Result
from armaden.games.arma_reforger.arma_reforger_server import ArmaReforgerServer


class AppServiceProvider(ServiceProvider):
    name = 'arma_reforger'

    def register(self) -> Result[None]:
        self._container.singleton(ArmaReforgerServer)
        return Success(None)

    def boot(self) -> Result[None]:
        server = self._container.make(ArmaReforgerServer)

        task = (
            TaskBuilder()
            .name('arma_reforger_server')
            .description('Manages the Arma Reforger dedicated server lifecycle')
            .on_initialize(server.initialize)
            .on_run(server.run)
            .on_shutdown(server.shutdown)
            .on_status(server.status)
            .exclusive_thread()
            .build()
        )

        app().supervisor.add_task(task)
        return Success(None)
