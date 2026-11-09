from __future__ import annotations

import asyncio
from enum import StrEnum
from pathlib import Path
from typing import final, override

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.api.error import Error
from armaden.framework.protocols.task_runtime_protocol import TaskRuntimeProtocol
from armaden.framework.types.result import Result
from armaden.games.minecraft.java.dto import JavaRuntimeManifestData
from armaden.games.minecraft.java.protocols import (
    JavaCompatibilityProtocol,
    TemurinCatalogProtocol,
)
from armaden.games.minecraft.java.temurin_catalog import AdoptiumTemurinCatalog
from armaden.games.minecraft.java.temurin_runtime_installer import (
    TemurinRuntimeInstaller,
)
from armaden.games.minecraft.minecraft_server_config import (
    Config as MinecraftServerConfig,
)
from armaden.games.minecraft.paper.configuration import (
    EulaFile,
    ServerPropertiesData,
    ServerPropertiesFile,
)
from armaden.games.minecraft.paper.dto import PaperArtifactManifestData
from armaden.games.minecraft.paper.paper_artifact_installer import (
    PaperArtifactInstaller,
)
from armaden.games.minecraft.paper.paper_downloads_client import (
    FillPaperDownloadsClient,
)
from armaden.games.minecraft.paper.paper_java_compatibility import (
    PaperJavaCompatibility,
)
from armaden.games.minecraft.paper.paper_launch_command import PaperLaunchCommand
from armaden.games.minecraft.paper.protocols import (
    PaperDownloadsProtocol,
)
from armaden.games.minecraft.protocols import MinecraftServerBackendProtocol
from armaden.network.http import HttpTransportProtocol, RequestsHttpTransport

_ARTIFACTS_DIRECTORY_NAME = 'artifacts'
_DEFAULT_INSTALLATION_DIRECTORY = 'minecraft-server'
_RUNTIMES_DIRECTORY_NAME = 'runtimes'


@final
class PaperBackend(MinecraftServerBackendProtocol):
    def __init__(
        self,
        config: MinecraftServerConfig,
        *,
        catalog: TemurinCatalogProtocol | None = None,
        compatibility: JavaCompatibilityProtocol | None = None,
        downloads: PaperDownloadsProtocol | None = None,
        transport: HttpTransportProtocol | None = None,
    ) -> None:
        self._config: MinecraftServerConfig = config
        self._transport: HttpTransportProtocol = transport or RequestsHttpTransport()
        self._downloads: PaperDownloadsProtocol = (
            downloads or FillPaperDownloadsClient(self._transport)
        )
        self._compatibility: JavaCompatibilityProtocol = (
            compatibility or PaperJavaCompatibility(self._downloads)
        )
        self._catalog: TemurinCatalogProtocol = (
            catalog or AdoptiumTemurinCatalog(self._transport)
        )
        self._installation_directory: Path = self._resolve_installation_directory()
        self._artifacts_directory: Path = self._installation_directory / _ARTIFACTS_DIRECTORY_NAME
        self._runtimes_directory: Path = self._installation_directory / _RUNTIMES_DIRECTORY_NAME
        self._java_manifest: JavaRuntimeManifestData | None = None
        self._artifact_manifest: PaperArtifactManifestData | None = None


    @override
    async def install(self, runtime: TaskRuntimeProtocol) -> Result[None]:
        _ = runtime

        if not is_successful(version := self._resolve_paper_version()):
            return version.map(lambda _: None)

        artifact = await self._build_artifact_installer(version.unwrap()).install()

        if not is_successful(artifact):
            return Failure(artifact.failure())

        self._artifact_manifest = artifact.unwrap()

        java_manifest = await self._build_java_installer().install(version.unwrap())

        if not is_successful(java_manifest):
            return Failure(java_manifest.failure())

        self._java_manifest = java_manifest.unwrap()
        return Success(None)


    @override
    def launch_command(self) -> Result[list[str]]:
        if not is_successful(command := self._build_launch_command()):
            return command.map(lambda _: [])

        argv = command.unwrap().argv()

        if not is_successful(argv):
            return argv.map(lambda _: [])

        return argv


    @override
    def launch_environment(self) -> dict[str, str]:
        if not is_successful(command := self._build_launch_command()):
            return {}

        return command.unwrap().environment()


    @override
    async def prepare(self) -> Result[None]:
        if not is_successful(directories := await asyncio.to_thread(self._ensure_directories)):
            return directories

        if not is_successful(eula := await asyncio.to_thread(self._write_eula)):
            return eula

        if not is_successful(properties := await asyncio.to_thread(self._write_server_properties)):
            return properties

        return Success(None)


    @override
    async def update(self, runtime: TaskRuntimeProtocol) -> Result[None]:
        _ = runtime

        if not is_successful(version := self._resolve_paper_version()):
            return version.map(lambda _: None)

        artifact = await self._build_artifact_installer(version.unwrap()).update()

        if not is_successful(artifact):
            return Failure(artifact.failure())

        self._artifact_manifest = artifact.unwrap()

        java_manifest = await self._build_java_installer().update(version.unwrap())

        if not is_successful(java_manifest):
            return Failure(java_manifest.failure())

        self._java_manifest = java_manifest.unwrap()
        return Success(None)


    @override
    def working_directory(self) -> Path:
        return self._installation_directory


    def _build_artifact_installer(self, version: str) -> PaperArtifactInstaller:
        paper = self._config.get('paper') or {}

        return PaperArtifactInstaller(
            artifacts_directory=self._artifacts_directory,
            build=paper.get('build'),
            downloads=self._downloads,
            transport=self._transport,
            version=version,
        )


    def _build_java_installer(self) -> TemurinRuntimeInstaller:
        java = self._config.get('java') or {}

        return TemurinRuntimeInstaller(
            catalog=self._catalog,
            compatibility=self._compatibility,
            runtimes_directory=self._runtimes_directory,
            transport=self._transport,
            executable=java.get('executable'),
            pinned=bool(java.get('pin')),
            preferred_major=java.get('version') or 25,
        )


    def _build_launch_command(self) -> Result[PaperLaunchCommand]:
        java_manifest = self._java_manifest
        artifact_manifest = self._artifact_manifest

        if java_manifest is None or artifact_manifest is None:
            return Failure(
                Error(
                    PaperBackendError.NOT_INSTALLED,
                    details={
                        'artifact_installed': artifact_manifest is not None,
                        'java_installed': java_manifest is not None,
                    },
                )
            )

        return PaperLaunchCommand.from_server_config(
            self._config,
            java_executable=java_manifest.executable,
            paper_jar=artifact_manifest.artifact_path,
            working_directory=self._installation_directory,
        )


    def _ensure_directories(self) -> Result[None]:
        try:
            self._installation_directory.mkdir(parents=True, exist_ok=True)
        except OSError as exception:
            return Failure(
                Error(
                    PaperBackendError.INSTALLATION_DIRECTORY_FAILED,
                    details={
                        'directory': str(self._installation_directory),
                        'error': str(exception),
                    },
                )
            )

        return Success(None)


    def _resolve_installation_directory(self) -> Path:
        installation = self._config.get('installation') or {}
        return Path(installation.get('directory') or _DEFAULT_INSTALLATION_DIRECTORY).absolute()


    def _resolve_paper_version(self) -> Result[str]:
        paper = self._config.get('paper') or {}
        version = paper.get('version')

        if not version:
            return Failure(
                Error(
                    PaperBackendError.PAPER_VERSION_REQUIRED,
                    details={'paper': paper},
                )
            )

        return Success(version)


    def _write_eula(self) -> Result[None]:
        eula = self._config.get('eula') or {}
        accepted = eula.get('accepted')
        return EulaFile(self._installation_directory / EulaFile.FILE_NAME).write(
            accepted if accepted is not None else True
        )


    def _write_server_properties(self) -> Result[None]:
        server = self._config.get('server') or {}
        values = ServerPropertiesData.from_server_config(server)
        return ServerPropertiesFile(
            self._installation_directory / ServerPropertiesFile.FILE_NAME
        ).ensure(values)


# --- Internal Types ----------------------------------------------------------

class PaperBackendError(StrEnum):
    INSTALLATION_DIRECTORY_FAILED = (
        'the paper server installation directory could not be created'
    )
    NOT_INSTALLED = 'the paper server java runtime or artifact has not been installed'
    PAPER_VERSION_REQUIRED = 'a paper version must be configured to install the paper server'
