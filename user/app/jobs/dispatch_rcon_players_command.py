from typing import final, override
import logging

from armaden.framework.api.schedule import ScheduledJob
from armaden.games.arma_reforger.arma_reforger_server import ArmaReforgerServer

logger = logging.getLogger(__name__)


@final
class DispatchRconPlayersCommandJob(ScheduledJob):
    queue = 'jobs'
    connection = 'jobs'
    priority = 5
    tags = ('rcon',)
    schedule = {
        'name': 'dispatch-rcon-players-command',
        'interval': 10,
    }


    def __init__(self, server: ArmaReforgerServer) -> None:
        self._server = server


    @override
    async def handle(self, *args: object, **kwargs: object) -> None:
        _ = args
        _ = kwargs

        if not self._server.rcon_client:
            logger.info('RCON client not yet initialized, skipping...')
            return

        if not self._server.rcon_client.connected:
            logger.info('RCON client not yet connected, skipping...')
            return

        if not self._server.rcon_client.authenticated:
            logger.info('RCON client not yet authenticated, skipping...')
            return

        logger.info('Dispatching #players command')
        _ = await self._server.rcon_client.dispatch_registered_command('#players')
