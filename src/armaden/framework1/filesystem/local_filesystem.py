from __future__ import annotations

import asyncio
import os
from pathlib import Path

import fsspec
from returns.result import Failure, Result, Success

from armaden.framework.errors import Error
from armaden.framework.errors.generic import GenericError
from armaden.framework.protocols.error import ErrorInterface
from armaden.framework.protocols.filesystem import Filesystem


class LocalFilesystem(Filesystem):

    def __init__(self, config: dict) -> None:
        self._config = config
        root = config.get('root') or 'storage/app'
        self._root = str(Path(root).expanduser().absolute())
        self._url = config.get('url')
        self._visibility = config.get('visibility', 'private')
        self._fs = fsspec.filesystem('file')

    def driver(self) -> str:
        return 'local'

    def _resolve(self, path: str) -> str:
        return os.path.normpath(os.path.join(self._root, path.lstrip(os.sep)))

    def _relative(self, path: str) -> str:
        return os.path.relpath(path, self._root)

    # --- Synchronous I/O ---

    def exists(self, path: str) -> Result[bool, ErrorInterface]:
        try:
            return Success(self._fs.exists(self._resolve(path)))
        except Exception as exception:
            return Failure(Error(GenericError.EXCEPTION, details={
                'operation': 'exists', 'path': path, 'exception': exception,
            }))

    def missing(self, path: str) -> Result[bool, ErrorInterface]:
        try:
            return Success(not self._fs.exists(self._resolve(path)))
        except Exception as exception:
            return Failure(Error(GenericError.EXCEPTION, details={
                'operation': 'missing', 'path': path, 'exception': exception,
            }))

    def get(self, path: str) -> Result[str, ErrorInterface]:
        try:
            data = self._fs.cat(self._resolve(path))
            if isinstance(data, bytes):
                return Success(data.decode('utf-8'))
            return Success(str(data))
        except Exception as exception:
            return Failure(Error(GenericError.EXCEPTION, details={
                'operation': 'get', 'path': path, 'exception': exception,
            }))

    def put(self, path: str, contents: str | bytes) -> Result[bool, ErrorInterface]:
        try:
            data = contents if isinstance(contents, bytes) else contents.encode('utf-8')
            self._fs.pipe(self._resolve(path), data)
            return Success(True)
        except Exception as exception:
            return Failure(Error(GenericError.EXCEPTION, details={
                'operation': 'put', 'path': path, 'exception': exception,
            }))

    def delete(self, path: str) -> Result[bool, ErrorInterface]:
        try:
            self._fs.rm(self._resolve(path))
            return Success(True)
        except Exception as exception:
            return Failure(Error(GenericError.EXCEPTION, details={
                'operation': 'delete', 'path': path, 'exception': exception,
            }))

    def copy(self, source: str, destination: str) -> Result[bool, ErrorInterface]:
        try:
            self._fs.copy(self._resolve(source), self._resolve(destination))
            return Success(True)
        except Exception as exception:
            return Failure(Error(GenericError.EXCEPTION, details={
                'operation': 'copy', 'source': source, 'destination': destination,
                'exception': exception,
            }))

    def move(self, source: str, destination: str) -> Result[bool, ErrorInterface]:
        try:
            self._fs.move(self._resolve(source), self._resolve(destination))
            return Success(True)
        except Exception as exception:
            return Failure(Error(GenericError.EXCEPTION, details={
                'operation': 'move', 'source': source, 'destination': destination,
                'exception': exception,
            }))

    def size(self, path: str) -> Result[int, ErrorInterface]:
        try:
            return Success(int(self._fs.size(self._resolve(path))))
        except Exception as exception:
            return Failure(Error(GenericError.EXCEPTION, details={
                'operation': 'size', 'path': path, 'exception': exception,
            }))

    def last_modified(self, path: str) -> Result[int, ErrorInterface]:
        try:
            modified = self._fs.modified(self._resolve(path))
            return Success(int(modified.timestamp()))
        except Exception as exception:
            return Failure(Error(GenericError.EXCEPTION, details={
                'operation': 'last_modified', 'path': path, 'exception': exception,
            }))

    def files(self, directory: str | None = None) -> Result[list[str], ErrorInterface]:
        try:
            entries = self._fs.ls(self._resolve(directory or ''), detail=True)
            return Success([
                self._relative(entry['name'])
                for entry in entries
                if entry.get('type') == 'file'
            ])
        except Exception as exception:
            return Failure(Error(GenericError.EXCEPTION, details={
                'operation': 'files', 'directory': directory, 'exception': exception,
            }))

    def directories(self, directory: str | None = None) -> Result[list[str], ErrorInterface]:
        try:
            entries = self._fs.ls(self._resolve(directory or ''), detail=True)
            return Success([
                self._relative(entry['name'])
                for entry in entries
                if entry.get('type') == 'directory'
            ])
        except Exception as exception:
            return Failure(Error(GenericError.EXCEPTION, details={
                'operation': 'directories', 'directory': directory, 'exception': exception,
            }))

    def make_directory(self, path: str) -> Result[bool, ErrorInterface]:
        try:
            self._fs.mkdir(self._resolve(path), create_parents=True)
            return Success(True)
        except Exception as exception:
            return Failure(Error(GenericError.EXCEPTION, details={
                'operation': 'make_directory', 'path': path, 'exception': exception,
            }))

    def delete_directory(self, path: str) -> Result[bool, ErrorInterface]:
        try:
            self._fs.rm(self._resolve(path), recursive=True)
            return Success(True)
        except Exception as exception:
            return Failure(Error(GenericError.EXCEPTION, details={
                'operation': 'delete_directory', 'path': path, 'exception': exception,
            }))

    # --- Async I/O (LocalFileSystem exposes no async API; delegate via thread) ---

    async def exists_async(self, path: str) -> Result[bool, ErrorInterface]:
        return await asyncio.to_thread(self.exists, path)

    async def missing_async(self, path: str) -> Result[bool, ErrorInterface]:
        return await asyncio.to_thread(self.missing, path)

    async def get_async(self, path: str) -> Result[str, ErrorInterface]:
        return await asyncio.to_thread(self.get, path)

    async def put_async(self, path: str, contents: str | bytes) -> Result[bool, ErrorInterface]:
        return await asyncio.to_thread(self.put, path, contents)

    async def delete_async(self, path: str) -> Result[bool, ErrorInterface]:
        return await asyncio.to_thread(self.delete, path)

    async def copy_async(self, source: str, destination: str) -> Result[bool, ErrorInterface]:
        return await asyncio.to_thread(self.copy, source, destination)

    async def move_async(self, source: str, destination: str) -> Result[bool, ErrorInterface]:
        return await asyncio.to_thread(self.move, source, destination)

    async def size_async(self, path: str) -> Result[int, ErrorInterface]:
        return await asyncio.to_thread(self.size, path)

    async def last_modified_async(self, path: str) -> Result[int, ErrorInterface]:
        return await asyncio.to_thread(self.last_modified, path)

    async def files_async(self, directory: str | None = None) -> Result[list[str], ErrorInterface]:
        return await asyncio.to_thread(self.files, directory)

    async def directories_async(self, directory: str | None = None) -> Result[list[str], ErrorInterface]:
        return await asyncio.to_thread(self.directories, directory)

    async def make_directory_async(self, path: str) -> Result[bool, ErrorInterface]:
        return await asyncio.to_thread(self.make_directory, path)

    async def delete_directory_async(self, path: str) -> Result[bool, ErrorInterface]:
        return await asyncio.to_thread(self.delete_directory, path)

    # --- Non-I/O ---

    def path(self, path: str) -> str:
        return self._resolve(path)

    def url(self, path: str) -> str:
        if not self._url:
            raise RuntimeError(
                "Local filesystem does not support public URLs (no 'url' configured)"
            )
        return f"{self._url.rstrip('/')}/{path.lstrip('/')}"

    def temporary_url(self, path: str, expiration: int) -> str:
        raise RuntimeError(
            'Temporary URLs are not supported for the local filesystem'
        )
