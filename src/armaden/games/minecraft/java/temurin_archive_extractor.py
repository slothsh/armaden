from __future__ import annotations

import os
import shutil
import stat
import tarfile
import zipfile
from enum import StrEnum
from pathlib import Path, PurePosixPath
from typing import final

from returns.result import Failure, Success

from armaden.framework.api.error import Error
from armaden.framework.types.result import Result

_DEFAULT_FILE_MODE = 0o644
_EXTRACTED_DIRECTORY = 'extracted'


@final
class TemurinArchiveExtractor:
    def extract(self, archive: Path, destination: Path) -> Result[Path]:
        archive_path: Path = Path(archive)
        destination_path: Path = Path(destination)
        name = archive_path.name.lower()

        if name.endswith('.tar.gz') or name.endswith('.tgz'):
            return self._extract_tar(archive_path, destination_path)

        if name.endswith('.zip'):
            return self._extract_zip(archive_path, destination_path)

        return Failure(
            Error(
                TemurinArchiveError.UNSUPPORTED_ARCHIVE,
                details={'archive': str(archive_path)},
            )
        )


    def _extract_tar(self, archive: Path, destination: Path) -> Result[Path]:
        extracted: Path = destination / _EXTRACTED_DIRECTORY

        try:
            extracted.mkdir(parents=True, exist_ok=True)
            root: Path = Path(os.path.realpath(extracted))

            with tarfile.open(archive, 'r:*') as bundle:
                for member in bundle:
                    if member.isdev():
                        return self._unsafe_entry(member.name)

                    if not _is_contained_name(member.name):
                        return self._unsafe_entry(member.name)

                    target: Path = extracted / member.name

                    if not _is_contained_path(target, root):
                        return self._unsafe_entry(member.name)

                    if member.isdir():
                        target.mkdir(parents=True, exist_ok=True)
                        continue

                    if member.issym():
                        if not _is_contained_link(member.linkname, target, root):
                            return self._unsafe_entry(member.name)

                        target.parent.mkdir(parents=True, exist_ok=True)
                        os.symlink(member.linkname, target)
                        continue

                    if member.islnk():
                        if not _is_contained_name(member.linkname):
                            return self._unsafe_entry(member.name)

                        linked: Path = extracted / member.linkname

                        if not _is_contained_path(linked, root):
                            return self._unsafe_entry(member.name)

                        target.parent.mkdir(parents=True, exist_ok=True)
                        os.link(linked, target)
                        continue

                    if not member.isfile():
                        return self._unsafe_entry(member.name)

                    source = bundle.extractfile(member)

                    if source is None:
                        return self._unsafe_entry(member.name)

                    target.parent.mkdir(parents=True, exist_ok=True)

                    with source, target.open('wb') as stream:
                        shutil.copyfileobj(source, stream)

                    mode: int = member.mode & 0o7777

                    if mode == 0:
                        mode = _DEFAULT_FILE_MODE

                    target.chmod(mode)
        except (tarfile.TarError, OSError) as exception:
            return Failure(
                Error(
                    TemurinArchiveError.EXTRACTION_FAILED,
                    details={'archive': str(archive), 'reason': str(exception)},
                )
            )

        return Success(extracted)


    def _extract_zip(self, archive: Path, destination: Path) -> Result[Path]:
        extracted: Path = destination / _EXTRACTED_DIRECTORY

        try:
            extracted.mkdir(parents=True, exist_ok=True)
            root: Path = Path(os.path.realpath(extracted))

            with zipfile.ZipFile(archive) as bundle:
                for entry in bundle.infolist():
                    if not _is_contained_name(entry.filename):
                        return self._unsafe_entry(entry.filename)

                    mode: int = entry.external_attr >> 16

                    if stat.S_ISLNK(mode):
                        return self._unsafe_entry(entry.filename)

                    target: Path = extracted / entry.filename

                    if not _is_contained_path(target, root):
                        return self._unsafe_entry(entry.filename)

                    if entry.is_dir():
                        target.mkdir(parents=True, exist_ok=True)
                        continue

                    target.parent.mkdir(parents=True, exist_ok=True)

                    with bundle.open(entry) as source, target.open('wb') as stream:
                        shutil.copyfileobj(source, stream)

                    permissions: int = mode & 0o7777

                    if permissions == 0:
                        permissions = _DEFAULT_FILE_MODE

                    target.chmod(permissions)
        except (zipfile.BadZipFile, OSError) as exception:
            return Failure(
                Error(
                    TemurinArchiveError.EXTRACTION_FAILED,
                    details={'archive': str(archive), 'reason': str(exception)},
                )
            )

        return Success(extracted)


    def _unsafe_entry(self, name: str) -> Result[Path]:
        return Failure(
            Error(
                TemurinArchiveError.UNSAFE_ENTRY,
                details={'entry': name},
            )
        )


# --- Internal Types ----------------------------------------------------------

class TemurinArchiveError(StrEnum):
    EXTRACTION_FAILED = 'the runtime archive could not be extracted'
    UNSAFE_ENTRY = 'the runtime archive contains an entry that escapes or destabilizes the extraction directory'
    UNSUPPORTED_ARCHIVE = 'the runtime archive has an unsupported format'


def _is_contained_name(name: str) -> bool:
    if name == '' or name.startswith('/') or '\0' in name:
        return False

    if PurePosixPath(name).is_absolute() or Path(name).is_absolute():
        return False

    parts = PurePosixPath(name).parts

    return '..' not in parts


def _is_contained_path(path: Path, root: Path) -> bool:
    return Path(os.path.realpath(path)).is_relative_to(root)


def _is_contained_link(linkname: str, link: Path, root: Path) -> bool:
    if linkname == '' or linkname.startswith('/') or '\0' in linkname:
        return False

    return _is_contained_path(link.parent / linkname, root)
