from typing import Any

from armaden.framework.classes.rcon_command_arg_spec import RconCommandArgSpec
from armaden.framework.protocols.rcon_command import RconCommandInterface


class KickCommand(RconCommandInterface):
    command_name: str = '#kick'
    description: str = 'Kick a player by ID'
    category: str = 'player'
    args: list = [
        RconCommandArgSpec(
            name='player_id',
            type=int,
            required=True,
            description='Player ID to kick',
        ),
    ]

    async def execute(self, **kwargs: Any) -> Any:
        player_id = str(kwargs['player_id'])
        response = await self._client.send_command(self.command_name, player_id)
        return await self.on_response(response)
