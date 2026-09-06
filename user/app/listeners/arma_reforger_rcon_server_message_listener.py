import logging

from typing import override

from armaden.framework.api.event import EventListener
from armaden.games.arma_reforger.events.rcon_server_message_event import RconServerMessageEvent


logger = logging.getLogger(__name__)


class ArmaReforgerRconServerMessageListener(EventListener[RconServerMessageEvent]):
    @override
    def handle(self, event: RconServerMessageEvent) -> object:
        logger.info('RECEIVED RCON SERVER MESSAGE: %s', event.message)
