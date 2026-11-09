from __future__ import annotations

import asyncio
import json
import os
import uuid
from enum import StrEnum
from pathlib import Path
from typing import final, override

from returns.pipeline import is_successful
from returns.result import Failure, Success

from armaden.framework.api.error import Error
from armaden.framework.types.result import Result
from armaden.network.http.protocols.http_transport_protocol import (
    HttpTransportProtocol,
)
from armaden.games.minecraft.paper.dto.paper_artifact_manifest_data import (
    PaperArtifactManifestData,
)
from armaden.games.minecraft.paper.dto.paper_build_data import PaperBuildData
from armaden.games.minecraft.paper.dto.paper_download_data import PaperDownloadData
from armaden.games.minecraft.paper.protocols.paper_artifact_installer_protocol import (
    PaperArtifactInstallerProtocol,
)
from armaden.games.minecraft.paper.protocols.paper_downloads_protocol import (
    PaperDownloadsProtocol,
)

_MANIFEST_NAME = 'paper.artifact.json'
_SERVER_DOWNLOAD = 'server:default'


@final
class PaperArtifactInstaller(PaperArtifactInstallerProtocol):
    def __init__(
        self,
        *,
        artifacts_directory: Path,
        build: int | None,
        downloads: PaperDownloadsProtocol,
        transport: HttpTransportProtocol,
        version: str,
    ) -> None:
        self._artifacts_directory: Path = Path(artifacts_directory)
        self._build: int | None = build
        self._downloads: PaperDownloadsProtocol = downloads
        self._manifest_path: Path = self._artifacts_directory / _MANIFEST_NAME
        self._transport: HttpTransportProtocol = transport
        self._version: str = version


    @override
    async def install(self) -> Result[PaperArtifactManifestData]:
        if not self._version:
            return Failure(
                Error(
                    PaperArtifactError.VERSION_REQUIRED,
                    details={'version': self._version},
                )
            )

        metadata = await self._downloads.version_metadata(self._version)

        if not is_successful(metadata):
            return Failure(metadata.failure())

        build_result: Result[PaperBuildData]

        if self._build is None:
            build_result = await self._downloads.latest_build(self._version)
            policy = 'latest'
        else:
            if self._build not in metadata.unwrap().builds:
                return Failure(
                    Error(
                        PaperArtifactError.BUILD_INVALID,
                        details={
                            'version': self._version,
                            'build': self._build,
                            'available': metadata.unwrap().builds,
                        },
                    )
                )

            build_result = await self._downloads.build_metadata(self._version, self._build)
            policy = 'pinned'

        if not is_successful(build_result):
            return Failure(build_result.failure())

        resolved_build: PaperBuildData = build_result.unwrap()
        download: PaperDownloadData | None = resolved_build.downloads.get(_SERVER_DOWNLOAD)

        if download is None:
            return Failure(
                Error(
                    PaperArtifactError.DOWNLOAD_MISSING,
                    details={
                        'version': self._version,
                        'build': resolved_build.number,
                        'downloads': sorted(resolved_build.downloads),
                    },
                )
            )

        artifact_path: Path = self._artifacts_directory / download.name
        active = self.artifact()

        if is_successful(active):
            manifest: PaperArtifactManifestData = active.unwrap()

            if (
                manifest.version == self._version
                and manifest.build == resolved_build.number
                and manifest.sha256 == download.sha256
                and manifest.build_policy == policy
                and manifest.artifact_path == str(artifact_path)
                and artifact_path.exists()
            ):
                return Success(manifest)

        downloaded = await self._transport.download_file(
            download.url,
            artifact_path,
            sha256=download.sha256,
        )

        if not is_successful(downloaded):
            return Failure(downloaded.failure())

        manifest = PaperArtifactManifestData(
            artifact_path=str(artifact_path),
            build=resolved_build.number,
            build_policy=policy,
            channel=resolved_build.channel,
            name=download.name,
            sha256=download.sha256,
            size=download.size,
            time=resolved_build.time,
            url=download.url,
            version=self._version,
        )
        persisted = await asyncio.to_thread(self._write_manifest, manifest)

        if not is_successful(persisted):
            return Failure(persisted.failure())

        return Success(manifest)


    @override
    def artifact(self) -> Result[PaperArtifactManifestData]:
        try:
            payload: object = json.loads(self._manifest_path.read_text())
        except OSError:
            return Failure(
                Error(
                    PaperArtifactError.NO_ACTIVE_ARTIFACT,
                    details={'manifest': str(self._manifest_path)},
                )
            )
        except ValueError:
            return Failure(
                Error(
                    PaperArtifactError.MANIFEST_INVALID,
                    details={'manifest': str(self._manifest_path)},
                )
            )

        return PaperArtifactManifestData.from_mapping(payload)


    @override
    async def update(self) -> Result[PaperArtifactManifestData]:
        return await self.install()


    def _write_manifest(self, manifest: PaperArtifactManifestData) -> Result[None]:
        temporary: Path = self._manifest_path.with_name(
            f'.{self._manifest_path.name}.{uuid.uuid4().hex}.tmp'
        )

        try:
            self._artifacts_directory.mkdir(parents=True, exist_ok=True)
            _ = temporary.write_text(json.dumps(manifest.to_mapping()))
            os.replace(temporary, self._manifest_path)
        except OSError as exception:
            temporary.unlink(missing_ok=True)
            return Failure(
                Error(
                    PaperArtifactError.INSTALLATION_FAILED,
                    details={'manifest': str(self._manifest_path), 'reason': str(exception)},
                )
            )

        return Success(None)


# --- Internal Types ----------------------------------------------------------

class PaperArtifactError(StrEnum):
    BUILD_INVALID = 'the configured paper build does not exist for the requested version'
    DOWNLOAD_MISSING = 'the resolved paper build has no server download'
    INSTALLATION_FAILED = 'the paper server artifact could not be installed'
    MANIFEST_INVALID = 'the paper artifact manifest is not valid json'
    NO_ACTIVE_ARTIFACT = 'no paper server artifact has been installed yet'
    VERSION_REQUIRED = 'a paper version must be configured to resolve an artifact'
