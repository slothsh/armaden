from fastapi import FastAPI, APIRouter
from app.http.controllers import LifecycleController, RconController


def api_routes(app: FastAPI):
    # -- Lifecycle --------------------------------------------------------

    lifecycle_controller = LifecycleController()
    lifecyle_router = APIRouter(
        prefix='',
        dependencies=[]
    )

    lifecyle_router.get("/health")(lifecycle_controller.health)
    lifecyle_router.post("/restart")(lifecycle_controller.restart)

    app.include_router(lifecyle_router)

    # -- RCON -------------------------------------------------------------

    rcon_router = APIRouter(
        prefix='/rcon',
        dependencies=[]
    )

    rcon_router.get("/players")(RconController.rcon_players)
    rcon_router.get("/bans")(RconController.rcon_bans)
    rcon_router.get("/missions")(RconController.rcon_missions)
    rcon_router.get("/users")(RconController.rcon_users)
    rcon_router.post("/say")(RconController.rcon_say)
    rcon_router.post("/kick")(RconController.rcon_kick)
    rcon_router.post("/ban")(RconController.rcon_ban)
    rcon_router.post("/add-ban")(RconController.rcon_add_ban)
    rcon_router.post("/remove-ban")(RconController.rcon_remove_ban)
    rcon_router.post("/load-bans")(RconController.rcon_load_bans)
    rcon_router.post("/write-bans")(RconController.rcon_write_bans)
    rcon_router.post("/lock")(RconController.rcon_lock)
    rcon_router.post("/unlock")(RconController.rcon_unlock)
    rcon_router.post("/restart")(RconController.rcon_restart)
    rcon_router.post("/shutdown")(RconController.rcon_shutdown)
    rcon_router.post("/restart-server")(RconController.rcon_restart_server)
    rcon_router.post("/reassign")(RconController.rcon_reassign)
    rcon_router.post("/load-mission")(RconController.rcon_load_mission)
    rcon_router.post("/server-admin")(RconController.rcon_server_admin)
    rcon_router.post("/command")(RconController.rcon_command)

    app.include_router(rcon_router)
