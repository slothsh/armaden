"""Arma Reforger BattlEye RCON command interface.

Extends :class:`framework.classes.battle_eye_rcon_client.BattleEyeRconClient` with typed convenience methods for
every command documented on the Arma Reforger server-management wiki.

All methods are coroutines and must be awaited.

Reference
~~~~~~~~~

https://community.bistudio.com/wiki/Arma_Reforger:Server_Management
"""

from framework.classes.battle_eye_rcon_client import BattleEyeRconClient
from .dto import PlayerResponseData


def _parse_players(raw: str) -> list[PlayerResponseData]:
    """Parse the raw ``players`` string into :class:`Player` objects.

    Skips the ``Processing Command:`` line and the column header line.
    """
    players: list[PlayerResponseData] = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("Processing Command:"):
            continue
        player = PlayerResponseData.from_line(line)
        if player is not None:
            players.append(player)
    return players


class ArmaReforgerRconClient(BattleEyeRconClient):
    """Typed façade over the BattlEye RCON protocol for Arma Reforger.

    Each method maps to a single server command.  Responses are returned
    as raw strings — callers are responsible for parsing them when
    necessary.
    """

    # -- generic ------------------------------------------------------

    async def command(self, cmd: str) -> str:
        """Send an arbitrary command string.

        Use this for commands not yet covered by dedicated methods.
        """
        return await self.send(cmd)

    # -- information--------------------------------------------------

    async def players_raw(self) -> str:
        """List connected players — raw string response."""
        return await self.send_with_fallback("players")

    async def players(self) -> list[PlayerResponseData]:
        """List connected players as parsed DTOs."""
        raw = await self.players_raw()
        return _parse_players(raw)

    async def users(self) -> str:
        """List users (admin / player / etc.)."""
        return await self.send_with_fallback("users")

    async def bans(self) -> str:
        """List active bans."""
        return await self.send_with_fallback("bans")

    async def missions(self) -> str:
        """List available missions."""
        return await self.send_with_fallback("missions")

    # -- messaging----------------------------------------------------

    async def say(self, message: str) -> str:
        """Broadcast a global message to all players."""
        return await self.send(f'say {message}')

    # -- player management-------------------------------------------

    async def kick(self, player: str | int, reason: str | None = None) -> str:
        """Kick a player by slot number, name, or UUID.

        Args:
            player: The player's identifier (slot #, name, or in-game UID
                from :meth:`players`).
            reason: Optional kick reason shown to the player.
        """
        cmd = f"kick {player}"
        if reason:
            cmd += f" {reason}"
        return await self.send(cmd)

    # -- ban management------------------------------------------------

    async def ban(
        self,
        player: str | int,
        duration: str | None = None,
        reason: str | None = None,
    ) -> str:
        """Ban a player by slot number, name, or UUID.

        Args:
            player: The player's identifier.
            duration: Ban duration.  ``"0"`` = permanent (default).
                Other examples: ``"60"`` (minutes), ``"1h"``, ``"1d"``.
            reason: Optional ban reason.
        """
        cmd = f"ban {player}"
        if duration is not None:
            cmd += f" {duration}"
        if reason is not None:
            cmd += f" {reason}"
        return await self.send(cmd)

    async def add_ban(
        self,
        guid_or_ip: str,
        duration: str | None = None,
        reason: str | None = None,
    ) -> str:
        """Ban a player by GUID or IP (even if offline).

        Args:
            guid_or_ip: The player's BattlEye GUID or IP address.
            duration: Ban duration (see :meth:`ban`).
            reason: Optional ban reason.
        """
        cmd = f"addban {guid_or_ip}"
        if duration is not None:
            cmd += f" {duration}"
        if reason is not None:
            cmd += f" {reason}"
        return await self.send(cmd)

    async def remove_ban(self, ban_id: str) -> str:
        """Remove a ban by its ID (from ``bans`` output)."""
        return await self.send(f"removeban {ban_id}")

    async def load_bans(self) -> str:
        """Reload the bans file."""
        return await self.send("loadbans")

    async def write_bans(self) -> str:
        """Write current bans to the bans file."""
        return await self.send("writebans")

    # -- server control-----------------------------------------------

    async def lock(self) -> str:
        """Lock the server (no new connections)."""
        return await self.send("lock")

    async def unlock(self) -> str:
        """Unlock the server."""
        return await self.send("unlock")

    async def restart(self) -> str:
        """Restart the current mission."""
        return await self.send("restart")

    async def shutdown(self) -> str:
        """Shut down the server process."""
        return await self.send("shutdown")

    async def restart_server(self) -> str:
        """Restart the server executable."""
        return await self.send("restartserver")

    async def reassign(self) -> str:
        """Reassign roles / slots."""
        return await self.send("reassign")

    # -- mission control----------------------------------------------

    async def load_mission(self, name: str, difficulty: str | None = None) -> str:
        """Load a specific mission.

        Args:
            name: Mission filename (without extension).
            difficulty: Optional difficulty setting.
        """
        cmd = f"mission {name}"
        if difficulty:
            cmd += f" {difficulty}"
        return await self.send(cmd)

    # -- admin--------------------------------------------------------

    async def server_admin(self, cmd: str) -> str:
        """Send a raw ``#serveradmin`` sub-command.

        Args:
            cmd: The sub-command string (e.g. ``"serverinfo"``).
        """
        return await self.send(f"serveradmin {cmd}")
