from typing import Any

from armaden.framework.api.rcon.dto.rcon_command_argument_data import RconCommandArgumentData
from armaden.framework.api.rcon import RconCommand


class BanRemoveCommand(RconCommand):
    command_name: str = '#ban'
    description: str = 'Remove a ban'
    category: str = 'ban'
    args: list[RconCommandArgumentData] = [
        RconCommandArgumentData(
            name='identity_id',
            type=str,
            required=True,
            description='Ban identity ID to remove',
        ),
    ]

    async def execute(self, **kwargs: Any) -> Any:
        response = await self._client.send_command(
            self.command_name, 'remove', str(kwargs['identity_id'])
        )
        return await self.on_response(response)
