from typing import Any

from armaden.framework.api.rcon.dto.rcon_command_argument_data import RconCommandArgumentData
from armaden.framework.api.rcon import RconCommand


class BanCreateCommand(RconCommand):
    command_name: str = '#ban'
    description: str = 'Create a ban'
    category: str = 'ban'
    args: list[RconCommandArgumentData] = [
        RconCommandArgumentData(
            name='identifier',
            type=str,
            required=True,
            description='Player identifier',
        ),
        RconCommandArgumentData(
            name='duration_seconds',
            type=int,
            required=True,
            description='Ban duration in seconds',
        ),
        RconCommandArgumentData(
            name='reason',
            type=str,
            required=False,
            default=None,
            description='Optional ban reason',
        ),
    ]

    async def execute(self, **kwargs: Any) -> Any:
        args = [
            'create',
            str(kwargs['identifier']),
            str(kwargs['duration_seconds']),
        ]
        if kwargs.get('reason') is not None:
            args.append(kwargs['reason'])
        response = await self._client.send_command(self.command_name, *args)
        return await self.on_response(response)
