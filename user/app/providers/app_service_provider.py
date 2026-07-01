from typing import cast

from returns.result import Success

from armaden.framework.classes.service_provider import ServiceProvider
from armaden.framework.classes.task import TaskBuilder
from armaden.framework.facades import app, config
from armaden.framework.utils.types import Result
from armaden.games.arma_reforger import ArmaReforgerServer
from armaden.games.arma_reforger.arma_reforger_server_config import Config


class AppServiceProvider(ServiceProvider):
    name = 'arma_reforger'

    def register(self) -> Result[None]:
        user_config = cast(Config, config('arma_reforger'))
        server = ArmaReforgerServer(user_config)
        self._container.instance(ArmaReforgerServer, server)
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
