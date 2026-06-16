import json
from dataclasses import dataclass
from enum import StrEnum
import logging
from typing import Any, Dict, List, Self, Union
from pathlib import Path

from returns.pipeline import is_successful
from returns.result import Failure, Success
from framework.enums.health_status import HealthStatus
from framework.facades import app
from framework.facades import config
from framework.classes.server import Server
from framework.utils.types import Result
from framework.errors import Error
from framework.utils.dictionary import Dictionary
from games.steamcmd import SteamCmdExecutable
from .arma_reforger_server_executable import ArmaReforgerServerExecutable
from .arma_reforger_rcon_client import ArmaReforgerRconClient
from .enums.arma_reforger_executable_flag import ArmaReforgerExecutableFlag

logger = logging.getLogger('games.arma_reforger.server')


class ArmaReforgerServer(Server):
    STEAM_APP_ID: int = 1874900
    STEAM_APP_ID_CLIENT: int = 1874880

    def __init__(self):
        self._executable = ExecutableContainer(
            steamcmd=SteamCmdExecutable(),
            reforger=ArmaReforgerServerExecutable()
        )

        self._rcon_client = ArmaReforgerRconClient(
            config('arma_reforger.reforger.server.rcon.address'),
            config('arma_reforger.reforger.server.rcon.port'),
            config('arma_reforger.reforger.server.rcon.password')
        )

        install_directory = Path(config('arma_reforger.reforger.installDirectory', '/arma')).absolute()

        self._paths = PathContainer(
            install=install_directory,
            config_directory=install_directory / 'Configs',
            config_file=install_directory / 'Configs' / 'config.json'
        )


    # --- Accessor Methods -----------------------------------------------------

    def rcon_client(self) -> ArmaReforgerRconClient | None:
        return self._rcon_client


    # --- Builder Methods -----------------------------------------------------

    def build(self) -> Self:
        return self


    # -- Server Interface -----------------------------------------------------

    async def initialize(self) -> Result[None]:
        try:
            if not is_successful(result := await self.install_game_assets(validate=True)):
                return result

            if not is_successful(result := self.install_config()):
                return result

            return Success(None)
        except Exception as e:
            return Failure(Error(ArmaReforgerServerError.INITIALIZATION_FAILED, {
                'exception': e
            }))


    async def run(self) -> Result[None]:
        argv = self.server_command()
        if not is_successful(argv):
            return argv.map(lambda _: None)

        await app().supervisor.dispatch_subprocess(
            argv.unwrap(),
            cwd=self._paths.install,
            handle_std_stream=ArmaReforgerServer._log_subprocess
        )

        return await self.shutdown()


    async def shutdown(self) -> Result[None]:
        return Success(None)


    async def status(self) -> Result[Dict[str, Any]]:
        return Success({
            'status': HealthStatus.OK,
        })


    # -- Executable Helpers -------------------------------------------

    def server_command(self) -> Result[List[str]]:
        reforger = self._executable.reforger.save_params()

        startup_parameters: dict[str, str]
        if startup_parameters := config('arma_reforger.reforger.startup'):
            for parameter, value in startup_parameters.items():
                if is_successful(flag := ArmaReforgerExecutableFlag.from_config(parameter)):
                    # Skip config override for now
                    if flag == ArmaReforgerExecutableFlag.CONFIG_FILE:
                        logger.warning("Skipping Arma Reforger %s startup flag specified from app config")
                        continue
                    reforger.custom(flag.unwrap(), value)
                else:
                    logger.warning(flag.failure())

        reforger.config(self._paths.config_file)

        argv = reforger.consume_argv()

        reforger.restore_params()

        return Success(argv)


    # -- steamcmd Helpers -------------------------------------------

    async def install_game_assets(self, validate: bool = False) -> Result[None]:
        argv = (
            self._executable.steamcmd
            .save_params()
            .force_install_dir(self._paths.install)
            .login_anonymous()
            .app_update(self.STEAM_APP_ID, validate=validate)
            .quit()
            .consume_argv()
        )

        self._executable.steamcmd.restore_params()

        future = app().supervisor.dispatch_subprocess(
            argv, cwd=self._paths.install,
            handle_std_stream=ArmaReforgerServer._log_subprocess
        )

        if not is_successful(result := await future):
            logger.info('An error occurred trying to install the Arma Reforger Server Assets: %s', result.failure())
            return result.map(lambda _: None)

        return Success(None)


    def install_config(self) -> Result[None]:
        config_data: Dict[str, Any] = Dictionary.without(config('arma_reforger.reforger.server'), lambda _, value: value is None)

        self._paths.config_directory.mkdir(exist_ok=True)

        with open(self._paths.config_file, 'w') as config_file:
            logger.info('Writing Arma Reforger Server config file')
            json.dump(config_data, config_file, indent=4)

        logger.info('Config file successfully written!')

        return Success(None)


    # -- General Helpers -------------------------------------------

    def _serialize_config(self) -> Result[None]:
        return Success(None)


    @classmethod
    async def _log_subprocess(cls, line: str) -> Result[None]:
        logger.info(line)
        return Success(None)


# --- Internal Types ----------------------------------------------------------

type ExecutableUnion = Union[SteamCmdExecutable, ArmaReforgerServerExecutable]

@dataclass
class ExecutableContainer:
    steamcmd: SteamCmdExecutable
    reforger: ArmaReforgerServerExecutable


@dataclass
class PathContainer:
    install: Path
    config_directory: Path
    config_file: Path


class ArmaReforgerServerError(StrEnum):
    INITIALIZATION_FAILED = "an error occurred while initializing the arma reforger server"
