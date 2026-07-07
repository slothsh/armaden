import json
from dataclasses import dataclass
from enum import StrEnum
import logging
from typing import Any, Dict, List, Self, Union, cast
from pathlib import Path

from returns.pipeline import is_successful
from returns.result import Failure, Success
from armaden.framework.classes.configurable import Configurable
from armaden.framework.enums.health_status import HealthStatus
from armaden.framework.utils.types import Result
from armaden.framework.errors import Error
from armaden.framework.protocols.task_runtime import TaskRuntimeInterface
from armaden.framework.utils.dictionary import Dictionary
from armaden.games.steamcmd import SteamCmdExecutable
from .arma_reforger_server_executable import ArmaReforgerServerExecutable
from .arma_reforger_rcon_client import ArmaReforgerRconClient
from .arma_reforger_server_config import DEFAULT_CONFIG, Config as ArmaReforgerServerConfig
from .enums.arma_reforger_executable_flag import ArmaReforgerExecutableFlag

logger = logging.getLogger('games.arma_reforger.server')


class ArmaReforgerServer(Configurable[ArmaReforgerServerConfig]):
    def __init__(self, *, config: ArmaReforgerServerConfig = DEFAULT_CONFIG):
        _ = config
        self._paths: PathContainer | None = None

        self._executable = ExecutableContainer(
            steamcmd=SteamCmdExecutable(config={'executable': self.config.get('steamExecutable'), 'installDirectory': self.config.get('steamInstallDirectory')}),
            reforger=ArmaReforgerServerExecutable(config={ 'executable': self.config['executable'], 'installDirectory': self.config['installDirectory'] })
        )

        self._rcon_client: ArmaReforgerRconClient | None = None

        if not self.config['installDirectory']:
            raise ArmaReforgerServerException('The Arma Reforger installation directory must be provided with the configuration')


    # --- Builder Methods -----------------------------------------------------

    def build(self) -> Self:
        return self


    # -- Server Interface -----------------------------------------------------

    async def initialize(self, runtime: TaskRuntimeInterface) -> Result[None]:
        try:
            if not is_successful(result := await self._executable.steamcmd.ensure_installed(runtime)):
                return result.map(lambda _: None)

            if not is_successful(result := await self._executable.reforger.ensure_installed(runtime, self._executable.steamcmd)):
                return result.map(lambda _: None)

            if not is_successful(result := self._executable.reforger.install_directory()):
                return Failure(Error(ArmaReforgerServerError.INITIALIZATION_FAILED, details={
                    'paths': self._paths,
                }))

            install_directory = result.unwrap()
            self._paths = PathContainer(
                install=install_directory,
                config_directory=install_directory / 'Configs',
                config_file=install_directory / 'Configs' / 'config.json'
            )

            if not is_successful(result := await self.install_config()):
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

        if not self._paths:
            return Failure(Error(ArmaReforgerServerError.MISSING_PATHS, details={
                'paths': self._paths
            }))

        await runtime.dispatch_subprocess(
            argv.unwrap(),
            cwd=self._paths.install,
            handle_std_stream=ArmaReforgerServer._log_subprocess
        )

        return await self.shutdown(runtime)


    async def shutdown(self, runtime: TaskRuntimeInterface) -> Result[None]:
        _ = runtime
        return Success(None)


    async def initialize_rcon_client(self, runtime: TaskRuntimeInterface) -> Result[None]:
        _ = runtime

        if rcon_config := self.config['server'] and self.config['server']['rcon']:
            match (rcon_config['port'], rcon_config['password']):
                case int() | None as port, str() | None as password:
                    self._rcon_client = ArmaReforgerRconClient(
                        address='127.0.0.1',
                        port=port or 2011,
                        password=password or ''
                    )

        return Success(None)


    async def run_rcon_client(self, runtime: TaskRuntimeInterface) -> Result[None]:
        _ = runtime
        if not self._rcon_client:
            return Success(None)

        await self._rcon_client.connect()

        return Success(None)


    async def shutdown_rcon_client(self, runtime: TaskRuntimeInterface) -> Result[None]:
        _ = runtime
        if not self._rcon_client:
            return Success(None)

        await self._rcon_client.shutdown()

        return Success(None)


    async def status(self, runtime: TaskRuntimeInterface) -> Result[Dict[str, Any]]:
        _ = runtime
        return Success({
            'status': HealthStatus.OK,
        })


    # -- Executable Helpers -------------------------------------------

    def server_command(self) -> Result[List[str]]:
        reforger = self._executable.reforger.save_params()

        startup_parameters = self.config.get('startup')
        if startup_parameters:
            for parameter, value in startup_parameters.items():
                if is_successful(flag := ArmaReforgerExecutableFlag.from_config(parameter)):
                    # Skip config override for now
                    if flag == ArmaReforgerExecutableFlag.CONFIG_FILE:
                        logger.warning("Skipping Arma Reforger %s startup flag specified from app config")
                        continue
                    reforger.custom(flag.unwrap(), cast(str | int, value))
                else:
                    logger.warning(flag.failure())


        if not self._paths:
            return Failure(Error(ArmaReforgerServerError.MISSING_PATHS, details={
                'paths': self._paths
            }))

        reforger.config(self._paths.config_file)

        argv = reforger.consume_argv()

        reforger.restore_params()

        return Success(argv)


    # -- steamcmd Helpers -------------------------------------------

    async def install_config(self) -> Result[None]:
        config_data: Dict[str, Any] = Dictionary.without(self.config['server'], lambda _, value: value is None)

        if not self._paths:
            return Failure(Error(ArmaReforgerServerError.MISSING_PATHS, details={
                'paths': self._paths
            }))

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
    MISSING_PATHS = "the paths for the arma reforger server are not correctly configured"
