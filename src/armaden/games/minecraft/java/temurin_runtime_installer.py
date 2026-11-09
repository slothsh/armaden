from __future__ import annotations

import asyncio
import json
import os
import re
import shutil
import subprocess
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
from armaden.games.minecraft.java.dto import (
    JavaCompatibilityData,
    JavaRuntimeManifestData,
    TemurinBinaryData,
    TemurinPlatformData,
    TemurinReleaseData,
)
from armaden.games.minecraft.java.enums import JavaRuntimeSource, TemurinImageType
from armaden.games.minecraft.java.protocols import (
    JavaCompatibilityProtocol,
    JavaRuntimeInstallerProtocol,
    TemurinCatalogProtocol,
)
from armaden.games.minecraft.java.temurin_archive_extractor import TemurinArchiveExtractor
from armaden.games.minecraft.java.temurin_platform import resolve_current_platform

_MANIFEST_NAME = 'manifest.json'
_STAGING_PREFIX = '.staging-'
_VERSION_OUTPUT_PATTERN = re.compile(r'version "(.+?)"')
_WINDOWS_JAVA_EXECUTABLE = 'java.exe'


@final
class TemurinRuntimeInstaller(JavaRuntimeInstallerProtocol):
    def __init__(
        self,
        *,
        catalog: TemurinCatalogProtocol,
        compatibility: JavaCompatibilityProtocol,
        runtimes_directory: Path,
        transport: HttpTransportProtocol,
        executable: str | None = None,
        pinned: bool = False,
        platform: TemurinPlatformData | None = None,
        preferred_major: int = 25,
    ) -> None:
        self._catalog: TemurinCatalogProtocol = catalog
        self._compatibility: JavaCompatibilityProtocol = compatibility
        self._executable: str | None = executable
        self._extractor: TemurinArchiveExtractor = TemurinArchiveExtractor()
        self._pinned: bool = pinned
        self._platform: TemurinPlatformData | None = platform
        self._preferred_major: int = preferred_major
        self._runtimes_directory: Path = Path(runtimes_directory)
        self._temurin_directory: Path = self._runtimes_directory / 'temurin'
        self._manifest_path: Path = self._temurin_directory / _MANIFEST_NAME
        self._transport: HttpTransportProtocol = transport


    @override
    async def install(self, paper_version: str) -> Result[JavaRuntimeManifestData]:
        if self._executable is not None:
            return await self._install_external(paper_version)

        return await self._install_managed(paper_version)


    @override
    def runtime(self) -> Result[JavaRuntimeManifestData]:
        try:
            payload: object = json.loads(self._manifest_path.read_text())
        except OSError:
            return Failure(
                Error(
                    TemurinRuntimeError.NO_ACTIVE_RUNTIME,
                    details={'manifest': str(self._manifest_path)},
                )
            )
        except ValueError:
            return Failure(
                Error(
                    TemurinRuntimeError.MANIFEST_INVALID,
                    details={'manifest': str(self._manifest_path)},
                )
            )

        return JavaRuntimeManifestData.from_mapping(payload)


    @override
    async def update(self, paper_version: str) -> Result[JavaRuntimeManifestData]:
        return await self.install(paper_version)


    async def _install_external(self, paper_version: str) -> Result[JavaRuntimeManifestData]:
        executable: str = self._executable if self._executable is not None else ''
        discovery = await asyncio.to_thread(self._discover_external_version, executable)

        if not is_successful(discovery):
            return Failure(discovery.failure())

        full_version, major = discovery.unwrap()
        compatibility: Result[JavaCompatibilityData] = (
            await self._compatibility.java_compatibility(paper_version)
        )

        if not is_successful(compatibility):
            return Failure(compatibility.failure())

        minimum_major = compatibility.unwrap().minimum_major

        if major < minimum_major:
            return Failure(
                Error(
                    TemurinRuntimeError.EXTERNAL_EXECUTABLE_INCOMPATIBLE,
                    details={
                        'executable': executable,
                        'major': major,
                        'minimum_major': minimum_major,
                        'paper_version': paper_version,
                    },
                )
            )

        manifest = JavaRuntimeManifestData(
            executable=executable,
            full_version=full_version,
            major=major,
            selection='external-override',
            source=JavaRuntimeSource.EXTERNAL,
        )
        persisted = await asyncio.to_thread(self._write_manifest, manifest)

        if not is_successful(persisted):
            return Failure(persisted.failure())

        return Success(manifest)


    async def _install_managed(self, paper_version: str) -> Result[JavaRuntimeManifestData]:
        compatibility: Result[JavaCompatibilityData] = (
            await self._compatibility.java_compatibility(paper_version)
        )

        if not is_successful(compatibility):
            return Failure(compatibility.failure())

        minimum_major = compatibility.unwrap().minimum_major
        platform = self._resolve_platform()

        if not is_successful(platform):
            return Failure(platform.failure())

        selection = await self._resolve_release(platform.unwrap(), minimum_major)

        if not is_successful(selection):
            return Failure(selection.failure())

        release, binary, policy = selection.unwrap()

        return await self._install_release(platform.unwrap(), release, binary, policy)


    async def _install_release(
        self,
        platform: TemurinPlatformData,
        release: TemurinReleaseData,
        binary: TemurinBinaryData,
        selection: str,
    ) -> Result[JavaRuntimeManifestData]:
        runtime_directory: Path = (
            self._temurin_directory
            / f'temurin-{binary.image_type.value}-{release.major}-{release.full_version}'
        )
        executable_name: str = (
            _WINDOWS_JAVA_EXECUTABLE if platform.os == 'windows' else 'java'
        )
        executable_path: Path = runtime_directory / 'bin' / executable_name
        active = self.runtime()

        if is_successful(active):
            manifest: JavaRuntimeManifestData = active.unwrap()

            if (
                manifest.source == JavaRuntimeSource.MANAGED
                and manifest.major == release.major
                and manifest.full_version == release.full_version
                and manifest.checksum == binary.checksum
                and manifest.image_type == binary.image_type
                and manifest.directory == str(runtime_directory)
                and manifest.executable == str(executable_path)
                and executable_path.exists()
            ):
                return Success(manifest)

        staging: Path = self._temurin_directory / f'{_STAGING_PREFIX}{uuid.uuid4().hex}'
        archive_path: Path = staging / binary.name

        try:
            download = await self._transport.download_file(
                binary.link,
                archive_path,
                sha256=binary.checksum,
            )

            if not is_successful(download):
                return Failure(download.failure())

            extraction = await asyncio.to_thread(self._extractor.extract, archive_path, staging)

            if not is_successful(extraction):
                return Failure(extraction.failure())

            extracted_root: Path = extraction.unwrap()
            located = await asyncio.to_thread(self._locate_single_root, extracted_root)

            if not is_successful(located):
                return Failure(located.failure())

            runtime_root: Path = located.unwrap()
            runtime_executable: Path = runtime_root / 'bin' / executable_name

            if not runtime_executable.exists():
                return Failure(
                    Error(
                        TemurinRuntimeError.ARCHIVE_LAYOUT_INVALID,
                        details={'missing': str(runtime_executable)},
                    )
                )

            published = await asyncio.to_thread(
                self._publish_runtime,
                runtime_root,
                runtime_directory,
            )

            if not is_successful(published):
                return Failure(published.failure())
        finally:
            await asyncio.to_thread(_remove_directory, staging)

        manifest = JavaRuntimeManifestData(
            architecture=platform.architecture,
            artifact_name=binary.name,
            checksum=binary.checksum,
            directory=str(runtime_directory),
            executable=str(executable_path),
            full_version=release.full_version,
            image_type=binary.image_type,
            major=release.major,
            os=platform.os,
            selection=selection,
            source=JavaRuntimeSource.MANAGED,
            vendor=release.vendor,
        )
        persisted = await asyncio.to_thread(self._write_manifest, manifest)

        if not is_successful(persisted):
            return Failure(persisted.failure())

        return Success(manifest)


    def _locate_single_root(self, extracted: Path) -> Result[Path]:
        entries: list[Path] = [entry for entry in extracted.iterdir() if entry.is_dir()]

        if len(entries) != 1:
            return Failure(
                Error(
                    TemurinRuntimeError.ARCHIVE_LAYOUT_INVALID,
                    details={'directory': str(extracted), 'entries': len(entries)},
                )
            )

        return Success(entries[0])


    def _publish_runtime(self, source: Path, target: Path) -> Result[None]:
        try:
            if target.exists():
                return Success(None)

            target.parent.mkdir(parents=True, exist_ok=True)
            os.replace(source, target)
        except OSError as exception:
            return Failure(
                Error(
                    TemurinRuntimeError.INSTALLATION_FAILED,
                    details={
                        'source': str(source),
                        'target': str(target),
                        'reason': str(exception),
                    },
                )
            )

        return Success(None)


    def _resolve_platform(self) -> Result[TemurinPlatformData]:
        if self._platform is not None:
            return Success(self._platform)

        return resolve_current_platform()


    async def _resolve_release(
        self,
        platform: TemurinPlatformData,
        minimum_major: int,
    ) -> Result[tuple[TemurinReleaseData, TemurinBinaryData, str]]:
        preference: int = self._preferred_major
        candidates: list[int] = []

        if self._pinned:
            if preference < minimum_major:
                return Failure(
                    Error(
                        TemurinRuntimeError.INCOMPATIBLE_PINNED_VERSION,
                        details={
                            'pinned_major': preference,
                            'minimum_major': minimum_major,
                        },
                    )
                )

            candidates = [preference]
        elif preference >= minimum_major:
            candidates = [preference, minimum_major]
        else:
            candidates = [minimum_major]

        for major in dict.fromkeys(candidates):
            for image_type in (TemurinImageType.JRE, TemurinImageType.JDK):
                release: Result[TemurinReleaseData] = (
                    await self._catalog.latest_release(image_type, major, platform)
                )

                if not is_successful(release):
                    continue

                resolved: TemurinReleaseData = release.unwrap()
                binaries: list[TemurinBinaryData] = [
                    binary
                    for binary in resolved.binaries
                    if binary.image_type == image_type
                ]

                if not binaries:
                    continue

                policy: str = (
                    'preference' if major == preference else 'minimum-required'
                )

                return Success((resolved, binaries[0], f'{policy}:{image_type.value}'))

        if self._pinned:
            return Failure(
                Error(
                    TemurinRuntimeError.PINNED_VERSION_UNAVAILABLE,
                    details={
                        'pinned_major': preference,
                        'os': platform.os,
                        'architecture': platform.architecture,
                    },
                )
            )

        return Failure(
            Error(
                TemurinRuntimeError.NO_COMPATIBLE_RUNTIME,
                details={
                    'minimum_major': minimum_major,
                    'preferred_major': preference,
                    'os': platform.os,
                    'architecture': platform.architecture,
                },
            )
        )


    def _write_manifest(self, manifest: JavaRuntimeManifestData) -> Result[None]:
        temporary: Path = self._manifest_path.with_name(
            f'.{self._manifest_path.name}.{uuid.uuid4().hex}.tmp'
        )

        try:
            self._temurin_directory.mkdir(parents=True, exist_ok=True)
            _ = temporary.write_text(json.dumps(manifest.to_mapping()))
            os.replace(temporary, self._manifest_path)
        except OSError as exception:
            temporary.unlink(missing_ok=True)
            return Failure(
                Error(
                    TemurinRuntimeError.INSTALLATION_FAILED,
                    details={'manifest': str(self._manifest_path), 'reason': str(exception)},
                )
            )

        return Success(None)


    def _discover_external_version(self, executable: str) -> Result[tuple[str, int]]:
        try:
            completed: subprocess.CompletedProcess[bytes] = subprocess.run(
                [executable, '-version'],
                capture_output=True,
                timeout=30,
            )
        except (OSError, subprocess.SubprocessError) as exception:
            return Failure(
                Error(
                    TemurinRuntimeError.EXTERNAL_EXECUTABLE_INVALID,
                    details={'executable': executable, 'reason': str(exception)},
                )
            )

        output: str = (
            completed.stderr.decode('utf-8', 'replace')
            + completed.stdout.decode('utf-8', 'replace')
        )
        match = _VERSION_OUTPUT_PATTERN.search(output)

        if completed.returncode != 0 or match is None:
            return Failure(
                Error(
                    TemurinRuntimeError.EXTERNAL_EXECUTABLE_INVALID,
                    details={'executable': executable, 'output': output[:512]},
                )
            )

        full_version: str = match.group(1)
        segments: list[str] = full_version.split('.')

        try:
            major: int = (
                int(segments[1])
                if segments[0] == '1' and len(segments) > 1
                else int(segments[0])
            )
        except (IndexError, ValueError):
            return Failure(
                Error(
                    TemurinRuntimeError.EXTERNAL_EXECUTABLE_INVALID,
                    details={'executable': executable, 'version': full_version},
                )
            )

        return Success((full_version, major))


# --- Internal Types ----------------------------------------------------------

class TemurinRuntimeError(StrEnum):
    ARCHIVE_LAYOUT_INVALID = 'the extracted runtime does not have the expected single-root bin layout'
    EXTERNAL_EXECUTABLE_INCOMPATIBLE = 'the configured external java executable is older than the version required by the target paper version'
    EXTERNAL_EXECUTABLE_INVALID = 'the configured external java executable could not be executed or reports no version'
    INCOMPATIBLE_PINNED_VERSION = 'the explicitly pinned java major version is not compatible with the target paper version'
    INSTALLATION_FAILED = 'the temurin runtime could not be installed'
    MANIFEST_INVALID = 'the java runtime manifest is not valid json'
    NO_ACTIVE_RUNTIME = 'no java runtime has been installed yet'
    NO_COMPATIBLE_RUNTIME = 'no temurin runtime is available for the target paper version and platform'
    PINNED_VERSION_UNAVAILABLE = 'the explicitly pinned java major version has no temurin artifact for this platform'


def _remove_directory(directory: Path) -> None:
    shutil.rmtree(directory, ignore_errors=True)
