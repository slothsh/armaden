from typing import final, override
import logging

from armaden.framework.api.schedule import ScheduledJob
from armaden.games.arma_reforger.arma_reforger_rcon_client import ArmaReforgerRconClient

logger = logging.getLogger(__name__)


@final
class DispatchRconPlayersCommandJob(ScheduledJob):
    queue = 'rcon'
    connection = 'rcon'
    priority = 5
    tags = ('rcon',)
    schedule = {
       'name': 'dispatch-rcon-players',
       'interval': 10,
       'queue': 'rcon',
       'connection': 'rcon',
       'priority': 5,
    }


    def __init__(self, rcon_client: ArmaReforgerRconClient) -> None:
        self._rcon_client = rcon_client


    @override
    async def handle(self, *args: object, **kwargs: object) -> None:
        _ = args
        _ = kwargs
        logger.info('Dispatching #players command')
        _ = await self._rcon_client.dispatch_registered_command('#players')
