from armaden.network.rcon.battle_eye.battle_eye_rcon_client import BattleEyeRconClient, CommandResponse


class ArmaReforgerRconClient(BattleEyeRconClient):
    """High-level RCON client for Arma Reforger with typed command methods.

    Each method returns an awaitable ``CommandResponse`` that resolves when
    the server responds (or raises ``TimeoutError`` on multi-packet timeout).
    """

    # -- Auth -----------------------------------------------------------------

    async def login(self) -> CommandResponse:
        return await self.send_command("#login")

    async def logout(self) -> CommandResponse:
        return await self.send_command("#logout")

    # -- Info -----------------------------------------------------------------

    async def roles(self) -> CommandResponse:
        return await self.send_command("#roles")

    async def get_id(self) -> CommandResponse:
        return await self.send_command("#id")

    async def players(self) -> CommandResponse:
        return await self.send_command("#players")

    # -- Server ---------------------------------------------------------------

    async def restart(self) -> CommandResponse:
        return await self.send_command("#restart")

    async def shutdown(self) -> CommandResponse:
        return await self.send_command("#shutdown")

    # -- Player ---------------------------------------------------------------

    async def kick(self, player_id: int) -> CommandResponse:
        return await self.send_command("#kick", str(player_id))

    # -- Ban ------------------------------------------------------------------

    async def ban_create(
        self,
        identifier: str | int,
        duration_seconds: int,
        reason: str | None = None,
    ) -> CommandResponse:
        args = ["#ban", "create", str(identifier), str(duration_seconds)]
        if reason is not None:
            args.append(reason)
        return await self.send_command(*args)

    async def ban_remove(self, identity_id: str | int) -> CommandResponse:
        return await self.send_command("#ban", "remove", str(identity_id))

    async def ban_list(self, page: int | None = None) -> CommandResponse:
        if page is not None:
            return await self.send_command("#ban", "list", str(page))
        return await self.send_command("#ban", "list")
