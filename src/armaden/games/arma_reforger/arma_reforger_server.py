import json
from dataclasses import dataclass
from enum import StrEnum
import logging
from typing import Any, Dict, List, Self, Union
from pathlib import Path

from returns.pipeline import is_successful
from returns.result import Failure, Success
from armaden.framework.enums.health_status import HealthStatus
from armaden.framework.utils.types import Result
from armaden.framework.errors import Error
from armaden.framework.protocols.task_runtime import TaskRuntimeInterface
from armaden.framework.utils.dictionary import Dictionary
from armaden.games.steamcmd import SteamCmdExecutable
from .arma_reforger_server_executable import ArmaReforgerServerExecutable
from .arma_reforger_rcon_client import ArmaReforgerRconClient
from .arma_reforger_config import Config, DEFAULT_CONFIG
from .enums.arma_reforger_executable_flag import ArmaReforgerExecutableFlag

logger = logging.getLogger('games.arma_reforger.server')


class ArmaReforgerServer:
    STEAM_APP_ID: int = 1874900
    STEAM_APP_ID_CLIENT: int = 1874880

    def __init__(self, config: Config | None = None):
        self._config: Config = Dictionary.merge(DEFAULT_CONFIG, config or {})

        self._executable = ExecutableContainer(
            steamcmd=SteamCmdExecutable(config={'executable': self._config.get('steamExecutable')}),
            reforger=ArmaReforgerServerExecutable(config=self._config)
        )

        self._rcon_client = ArmaReforgerRconClient(
            self._config['server']['rcon']['address'],
            self._config['server']['rcon']['port'],
            self._config['server']['rcon']['password']
        )

        if not self._config['installDirectory']:
            raise ArmaReforgerServerException('The Arma Reforger installation directory must be provided with the configuration')

        install_directory = Path(self._config['installDirectory']).absolute()

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

    async def initialize(self, runtime: TaskRuntimeInterface) -> Result[None]:
        try:
            if not is_successful(result := self._executable.steamcmd.ensure_installed()):
                return result.map(lambda _: None)

            if not is_successful(result := await self.install_game_assets(runtime, validate=True)):
                return result

            if not is_successful(result := self.install_config()):
                return result

            return Success(None)
        except Exception as e:
            return Failure(Error(ArmaReforgerServerError.INITIALIZATION_FAILED, {
                'exception': e
            }))


    async def run(self, runtime: TaskRuntimeInterface) -> Result[None]:
        argv = self.server_command()
        if not is_successful(argv):
            return argv.map(lambda _: None)

        await runtime.dispatch_subprocess(
            argv.unwrap(),
            cwd=self._paths.install,
            handle_std_stream=ArmaReforgerServer._log_subprocess
        )

        return await self.shutdown(runtime)


    async def shutdown(self, runtime: TaskRuntimeInterface) -> Result[None]:
        return Success(None)


    async def status(self, runtime: TaskRuntimeInterface) -> Result[Dict[str, Any]]:
        return Success({
            'status': HealthStatus.OK,
        })


    # -- Executable Helpers -------------------------------------------

    def server_command(self) -> Result[List[str]]:
        reforger = self._executable.reforger.save_params()

        startup_parameters: dict[str, str] | None
        if startup_parameters := self._config.get('startup'):
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

    async def install_game_assets(self, runtime: TaskRuntimeInterface, validate: bool = False) -> Result[None]:
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

        result = await runtime.dispatch_subprocess(
            argv, cwd=self._paths.install,
            handle_std_stream=ArmaReforgerServer._log_subprocess
        )

        if not is_successful(result):
            logger.info('An error occurred trying to install the Arma Reforger Server Assets: %s', result.failure())
            return result.map(lambda _: None)

        return Success(None)


    def install_config(self) -> Result[None]:
        config_data: Dict[str, Any] = Dictionary.without(self._config['server'], lambda _, value: value is None)

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


class ArmaReforgerServerException(Exception):
    pass


class ArmaReforgerServerError(StrEnum):
    INITIALIZATION_FAILED = "an error occurred while initializing the arma reforger server"
