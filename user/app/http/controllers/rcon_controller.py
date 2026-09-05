import logging
from typing import cast

from armaden.framework.api.http import HttpController
from armaden.games.arma_reforger import ArmaReforgerServer
from app.http.classes.api import Api
from app.http.dto.api_data import ApiResponseData
from armaden.network.rcon.battle_eye.battle_eye_rcon_client import CommandResponse

logger = logging.getLogger(__name__)


class RconController(HttpController):
    def __init__(self, server: ArmaReforgerServer) -> None:
        self._server: ArmaReforgerServer = server

    async def players(self) -> ApiResponseData:
        if not self._server.rcon_client:
            return Api.error(message='Could not fetch players')

        players = cast(CommandResponse , await self._server.rcon_client.dispatch_registered_command('#players'))

        if not players:
            return Api.error(message='No response from the server command')

        if players.error:
            return Api.error(message=players.error)

        return Api.success(message=players.response)


    async def restart(self) -> ApiResponseData:
        if not self._server.rcon_client:
            return Api.error(message='Could not restart the server')

        restart = cast(CommandResponse, await self._server.rcon_client.dispatch_registered_command('#restart'))

        if not restart:
            return Api.error(message='No response from the server command')

        if restart.error:
            return Api.error(message=restart.error)

        return Api.success(message=restart.response)
        
