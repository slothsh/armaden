import logging
from typing import Any
from fastapi import HTTPException, Request
from framework.classes.rcon_client import RconClientConnectionError, RconClientError
from games.arma_reforger import ArmaReforgerRconClient
from app.http.dto.rcon_data import *

logger = logging.getLogger('app.http.controllers.rcon')


class RconController:
    @classmethod
    async def rcon_players(cls, request: Request) -> dict[str, Any]:
        rcon = await _ensure_rcon(request)
        try:
            players = await rcon.players()
        except RconClientError as exc:
            raise HTTPException(status_code=502, detail=str(exc))
        return {
            "status": "ok",
            "response": [
                {"slot": p.slot, "uid": p.uid, "name": p.name} for p in players
            ],
        }


    @classmethod
    async def rcon_bans(cls, request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).bans())


    @classmethod
    async def rcon_missions(cls, request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).missions())


    @classmethod
    async def rcon_users(cls, request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).users())


    @classmethod
    async def rcon_say(cls, request: Request, payload: SayRequestData) -> dict[str, Any]:
        return await _rcon_response(
            (await _ensure_rcon(request)).say(payload.message)
        )


    @classmethod
    async def rcon_kick(cls, request: Request, payload: KickRequestData) -> dict[str, Any]:
        return await _rcon_response(
            (await _ensure_rcon(request)).kick(payload.player_id, payload.reason)
        )


    @classmethod
    async def rcon_ban(cls, request: Request, payload: BanRequestData) -> dict[str, Any]:
        return await _rcon_response(
            (await _ensure_rcon(request)).ban(
                payload.player_id, payload.duration, payload.reason
            )
        )


    @classmethod
    async def rcon_add_ban(cls, request: Request, payload: AddBanRequestData) -> dict[str, Any]:
        return await _rcon_response(
            (await _ensure_rcon(request)).add_ban(
                payload.guid_or_ip, payload.duration, payload.reason
            )
        )


    @classmethod
    async def rcon_remove_ban(cls, request: Request, payload: RemoveBanRequestData) -> dict[str, Any]:
        return await _rcon_response(
            (await _ensure_rcon(request)).remove_ban(payload.ban_id)
        )


    @classmethod
    async def rcon_load_bans(cls, request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).load_bans())


    @classmethod
    async def rcon_write_bans(cls, request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).write_bans())


    @classmethod
    async def rcon_lock(cls, request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).lock())


    @classmethod
    async def rcon_unlock(cls, request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).unlock())


    @classmethod
    async def rcon_restart(cls, request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).restart())


    @classmethod
    async def rcon_shutdown(cls, request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).shutdown())


    @classmethod
    async def rcon_restart_server(cls, request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).restart_server())


    @classmethod
    async def rcon_reassign(cls, request: Request) -> dict[str, Any]:
        return await _rcon_response((await _ensure_rcon(request)).reassign())


    @classmethod
    async def rcon_load_mission(cls, request: Request, payload: LoadMissionRequestData) -> dict[str, Any]:
        return await _rcon_response(
            (await _ensure_rcon(request)).load_mission(
                payload.name, payload.difficulty
            )
        )


    @classmethod
    async def rcon_server_admin(cls, request: Request, payload: ServerAdminRequestData) -> dict[str, Any]:
        return await _rcon_response(
            (await _ensure_rcon(request)).server_admin(payload.cmd)
        )


    @classmethod
    async def rcon_command(cls, request: Request, payload: CommandRequestData) -> dict[str, Any]:
        return await _rcon_response(
            (await _ensure_rcon(request)).command(payload.cmd)
        )


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

async def _ensure_rcon(request: Request) -> ArmaReforgerRconClient:
    """Return the shared RCON client, connecting on first use."""
    rcon: ArmaReforgerRconClient = request.app.state.rcon
    if not rcon.is_connected:
        try:
            await rcon.connect()
        except RconClientConnectionError as exc:
            raise HTTPException(status_code=503, detail=str(exc))
    return rcon


async def _rcon_response(cmd_coro: Any) -> dict[str, Any]:
    """Execute an RCON command and wrap the result."""
    try:
        response = await cmd_coro
    except RconClientError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    return {"status": "ok", "response": response}
