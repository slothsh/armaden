from __future__ import annotations

import asyncio
import os
from collections.abc import Mapping
from pathlib import Path
from typing import override

from returns.result import Failure, Success

from armaden.framework.protocols.error_protocol import ErrorProtocol
from armaden.framework.protocols.filesystem_protocol import FilesystemProtocol
from armaden.framework.protocols.fsspec_filesystem_protocol import (
    FsspecFilesystemProtocol,
)
from armaden.framework.runtime.error.error import Error
from armaden.framework.runtime.filesystem.fsspect_filesystem_factory import (
    create_fsspec_filesystem,
)
from armaden.framework.runtime.filesystem.exceptions.local_filesystem_error import (
    LocalFilesystemError,
)
from armaden.framework.runtime.filesystem.exceptions.local_filesystem_path_exception import (
    LocalFilesystemPathException,
)
from armaden.framework.types.result import Result


class LocalFilesystem(FilesystemProtocol):
    def __init__(self, config: Mapping[str, object]) -> None:
        self._config: Mapping[str, object] = config
        root = config.get('root')
        root_path = root if isinstance(root, str) and root else 'storage/app'
        self._root: Path = Path(root_path).expanduser().absolute().resolve()
        url = config.get('url')
        self._url: str | None = url if isinstance(url, str) else None
        self._visibility: object = config.get('visibility', 'private')
        self._filesystem: FsspecFilesystemProtocol = create_fsspec_filesystem('file')


    @override
    async def copy_async(self, source: str, destination: str) -> Result[bool]:
        return await asyncio.to_thread(self.copy, source, destination)


    @override
    def copy(self, source: str, destination: str) -> Result[bool]:
        try:
            self._filesystem.copy(self._resolve(source), self._resolve(destination))
            return Success(True)
        except LocalFilesystemPathException as exception:
            return Failure(self._path_error(exception))
        except Exception as exception:
            return Failure(self._operation_error('copy', exception, {
                'source': source,
                'destination': destination,
            }))


    @override
    async def delete_async(self, path: str) -> Result[bool]:
        return await asyncio.to_thread(self.delete, path)


    @override
    def delete(self, path: str) -> Result[bool]:
        try:
            self._filesystem.rm(self._resolve(path))
            return Success(True)
        except LocalFilesystemPathException as exception:
            return Failure(self._path_error(exception))
        except Exception as exception:
            return Failure(self._operation_error('delete', exception, {'path': path}))


    @override
    async def delete_directory_async(self, path: str) -> Result[bool]:
        return await asyncio.to_thread(self.delete_directory, path)


    @override
    def delete_directory(self, path: str) -> Result[bool]:
        try:
            self._filesystem.rm(self._resolve(path), recursive=True)
            return Success(True)
        except LocalFilesystemPathException as exception:
            return Failure(self._path_error(exception))
        except Exception as exception:
            return Failure(self._operation_error(
                'delete_directory', exception, {'path': path},
            ))


    @override
    async def directories_async(self, directory: str | None = None) -> Result[list[str]]:
        return await asyncio.to_thread(self.directories, directory)


    @override
    def directories(self, directory: str | None = None) -> Result[list[str]]:
        try:
            entries = self._entries(directory)
            return Success([
                self._relative(name)
                for name, entry_type in entries
                if entry_type == 'directory'
            ])
        except LocalFilesystemPathException as exception:
            return Failure(self._path_error(exception))
        except Exception as exception:
            return Failure(self._operation_error(
                'directories', exception, {'directory': directory},
            ))


    @override
    def driver(self) -> str:
        return 'local'


    @override
    async def exists_async(self, path: str) -> Result[bool]:
        return await asyncio.to_thread(self.exists, path)


    @override
    def exists(self, path: str) -> Result[bool]:
        try:
            return Success(self._filesystem.exists(self._resolve(path)))
        except LocalFilesystemPathException as exception:
            return Failure(self._path_error(exception))
        except Exception as exception:
            return Failure(self._operation_error('exists', exception, {'path': path}))


    @override
    async def files_async(self, directory: str | None = None) -> Result[list[str]]:
        return await asyncio.to_thread(self.files, directory)


    @override
    def files(self, directory: str | None = None) -> Result[list[str]]:
        try:
            entries = self._entries(directory)
            return Success([
                self._relative(name)
                for name, entry_type in entries
                if entry_type == 'file'
            ])
        except LocalFilesystemPathException as exception:
            return Failure(self._path_error(exception))
        except Exception as exception:
            return Failure(self._operation_error(
                'files', exception, {'directory': directory},
            ))


    @override
    async def get_async(self, path: str) -> Result[str | bytes]:
        return await asyncio.to_thread(self.get, path)


    @override
    def get(self, path: str) -> Result[str | bytes]:
        try:
            data = self._filesystem.cat(self._resolve(path))
            return Success(data)
        except LocalFilesystemPathException as exception:
            return Failure(self._path_error(exception))
        except Exception as exception:
            return Failure(self._operation_error('get', exception, {'path': path}))


    @override
    async def last_modified_async(self, path: str) -> Result[int]:
        return await asyncio.to_thread(self.last_modified, path)


    @override
    def last_modified(self, path: str) -> Result[int]:
        try:
            modified = self._filesystem.modified(self._resolve(path))
            return Success(int(modified.timestamp()))
        except LocalFilesystemPathException as exception:
            return Failure(self._path_error(exception))
        except Exception as exception:
            return Failure(self._operation_error(
                'last_modified', exception, {'path': path},
            ))


    @override
    async def make_directory_async(self, path: str) -> Result[bool]:
        return await asyncio.to_thread(self.make_directory, path)


    @override
    def make_directory(self, path: str) -> Result[bool]:
        try:
            self._filesystem.mkdir(self._resolve(path), create_parents=True)
            return Success(True)
        except LocalFilesystemPathException as exception:
            return Failure(self._path_error(exception))
        except Exception as exception:
            return Failure(self._operation_error(
                'make_directory', exception, {'path': path},
            ))


    @override
    async def missing_async(self, path: str) -> Result[bool]:
        return await asyncio.to_thread(self.missing, path)


    @override
    def missing(self, path: str) -> Result[bool]:
        result = self.exists(path)
        if isinstance(result, Failure):
            return result
        return Success(not result.unwrap())


    @override
    async def move_async(self, source: str, destination: str) -> Result[bool]:
        return await asyncio.to_thread(self.move, source, destination)


    @override
    def move(self, source: str, destination: str) -> Result[bool]:
        try:
            self._filesystem.move(self._resolve(source), self._resolve(destination))
            return Success(True)
        except LocalFilesystemPathException as exception:
            return Failure(self._path_error(exception))
        except Exception as exception:
            return Failure(self._operation_error('move', exception, {
                'source': source,
                'destination': destination,
            }))


    @override
    def path(self, path: str) -> str:
        return self._resolve(path)


    @override
    async def put_async(self, path: str, contents: str | bytes) -> Result[bool]:
        return await asyncio.to_thread(self.put, path, contents)


    @override
    def put(self, path: str, contents: str | bytes) -> Result[bool]:
        try:
            data = contents if isinstance(contents, bytes) else contents.encode('utf-8')
            self._filesystem.pipe(self._resolve(path), data)
            return Success(True)
        except LocalFilesystemPathException as exception:
            return Failure(self._path_error(exception))
        except Exception as exception:
            return Failure(self._operation_error('put', exception, {'path': path}))


    @override
    async def size_async(self, path: str) -> Result[int]:
        return await asyncio.to_thread(self.size, path)


    @override
    def size(self, path: str) -> Result[int]:
        try:
            return Success(self._filesystem.size(self._resolve(path)))
        except LocalFilesystemPathException as exception:
            return Failure(self._path_error(exception))
        except Exception as exception:
            return Failure(self._operation_error('size', exception, {'path': path}))


    @override
    def temporary_url(self, path: str, expiration: int) -> str:
        _ = path
        _ = expiration
        raise RuntimeError('Temporary URLs are not supported for the local filesystem')


    @override
    def url(self, path: str) -> str:
        if self._url is None:
            raise RuntimeError("Local filesystem does not support public URLs")
        return f'{self._url.rstrip("/")}/{path.lstrip("/")}'


    def _entries(self, directory: str | None) -> list[tuple[str, str]]:
        entries = self._filesystem.ls(self._resolve(directory or ''), detail=True)
        result: list[tuple[str, str]] = []
        for entry in entries:
            name = entry.get('name')
            entry_type = entry.get('type')
            if isinstance(name, str) and isinstance(entry_type, str):
                result.append((name, entry_type))
        return result


    def _operation_error(
        self,
        operation: str,
        exception: Exception,
        details: Mapping[str, object],
    ) -> ErrorProtocol:
        error_details = dict(details)
        error_details['exception'] = exception
        error_details['operation'] = operation
        return Error(LocalFilesystemError.OPERATION_FAILED, details=error_details)


    def _path_error(self, exception: LocalFilesystemPathException) -> ErrorProtocol:
        return Error(LocalFilesystemError.PATH_OUTSIDE_ROOT, details={
            'path': exception.path,
            'exception': exception,
        })


    def _relative(self, path: str) -> str:
        return os.path.relpath(path, self._root)


    def _resolve(self, path: str) -> str:
        candidate = (self._root / path.lstrip(os.sep)).resolve()
        try:
            _ = candidate.relative_to(self._root)
        except ValueError as exception:
            raise LocalFilesystemPathException(path) from exception
        return str(candidate)
