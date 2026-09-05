from typing import Any

from armaden.framework.api.rcon.dto.rcon_command_argument_data import RconCommandArgumentData
from armaden.framework.api.rcon import RconCommand


class KickCommand(RconCommand):
    command_name: str = '#kick'
    description: str = 'Kick a player by ID'
    category: str = 'player'
    args: list[RconCommandArgumentData] = [
        RconCommandArgumentData(
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
