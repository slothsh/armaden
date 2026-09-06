from typing import override

from returns.result import Success

from armaden.framework.api.rcon import RconServerMessageHandler
from armaden.framework.types.result import Result
from armaden.games.arma_reforger.events.rcon_server_message_event import RconServerMessageEvent


class DispatchEventServerMessageHandler(RconServerMessageHandler):
    name: str = 'dispatch_event'
    description: str = 'Dispatches an event whenever a server message is received. The event can be subscribed/listened to be handled by user code.'
    category: str = 'logging'


    @override
    async def handle(self, server_message: str) -> Result[None]:
        _ = await RconServerMessageEvent.dispatch(message=server_message)
        return Success(None)
