import json
from dataclasses import dataclass
from enum import StrEnum
import logging
from typing import Any, Dict, List, Self, Union
from pathlib import Path

from returns.pipeline import is_successful
from returns.result import Failure, Success
from server.arma.reforger.arma_reforger_server_executable import ArmaReforgerServerExecutable
from server.arma.reforger.arma_reforger_rcon_client import ArmaReforgerRconClient
from server.arma.reforger.enums.arma_reforger_executable_flag import ArmaReforgerExecutableFlag
from server.lib import config
from server.lib import Result, Server, Error
from server.lib.interfaces import AsyncStreamArg, QueueableSupervisor
from server.lib.helpers import Dictionary
from server.steamcmd import SteamCmdExecutable

logger = logging.getLogger('server.arma.reforger.server')


class ArmaReforgerServer(Server):
    STEAM_APP_ID: int = 1874900
    STEAM_APP_ID_CLIENT: int = 1874880

    def __init__(self):
        self._supervisor: QueueableSupervisor | None = None

        self._executable = ExecutableContainer(
            steamcmd=SteamCmdExecutable(),
            reforger=ArmaReforgerServerExecutable()
        )

        self._rcon_client = ArmaReforgerRconClient(
            config('arma.reforger.server.rcon.address'),
            config('arma.reforger.server.rcon.port'),
            config('arma.reforger.server.rcon.password')
        )

        install_directory = Path(config('arma.reforger.installDirectory', '/arma')).absolute()

        self._paths = PathContainer(
            install=install_directory,
            config_directory=install_directory / 'Configs',
            config_file=install_directory / 'Configs' / 'config.json'
        )


    # --- Accessor Methods -----------------------------------------------------

    def rcon_client(self) -> ArmaReforgerRconClient | None:
        return self._rcon_client


    # --- Builder Methods -----------------------------------------------------

    def with_supervisor(self, supervisor: QueueableSupervisor) -> Self:
        self._supervisor = supervisor
        return self


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
        if not self._supervisor:
            return Failure(Error(ArmaReforgerServerError.SUPERVISOR_UNAVAILABLE))

        argv = self.server_command()
        if not is_successful(argv):
            return argv.map(lambda _: None)

        await self._supervisor.dispatch_subprocess(
            argv.unwrap(),
            cwd=self._paths.install,
            handle_std_streams=ArmaReforgerServer._log_subprocess
        )

        return await self.shutdown()


    async def shutdown(self) -> Result[None]:
        return Success(None)

    
    # -- Executable Helpers -------------------------------------------

    def server_command(self) -> Result[List[str]]:
        reforger = self._executable.reforger.save_params()

        startup_parameters: dict[str, str]
        if startup_parameters := config('arma.reforger.startup'):
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
        if not self._supervisor:
            return Failure(Error(ArmaReforgerServerError.SUPERVISOR_UNAVAILABLE))

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

        future = self._supervisor.dispatch_subprocess(
            argv, cwd=self._paths.install,
            handle_std_streams=ArmaReforgerServer._log_subprocess
        )

        if not is_successful(result := await future):
            logger.info('An error occurred trying to install the Arma Reforger Server Assets: %s', result.failure())
            return result.map(lambda _: None)

        return Success(None)


    def install_config(self) -> Result[None]:
        config_data: Dict[str, Any] = Dictionary.without(config('arma.reforger.server'), lambda _, value: value is None)

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
    async def _log_subprocess(cls, stdout: AsyncStreamArg, stderr: AsyncStreamArg) -> Result[None]:
        if stdout:
            while True:
                line_bytes = await stdout.readline()

                if not line_bytes:
                    break

                if line := line_bytes.decode(errors='replace').strip():
                    logger.info(line)

        if stderr:
            while True:
                line_bytes = await stderr.readline()

                if not line_bytes:
                    break

                if line := line_bytes.decode(errors='replace').strip():
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
    SUPERVISOR_UNAVAILABLE = "an arma reforger server's supervisor is unavailable"
