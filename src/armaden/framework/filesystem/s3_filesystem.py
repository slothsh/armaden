from __future__ import annotations

import asyncio

import fsspec
from returns.result import Failure, Result, Success

from armaden.framework.errors import Error
from armaden.framework.errors.generic import GenericError
from armaden.framework.protocols.error import ErrorInterface
from armaden.framework.protocols.filesystem import Filesystem


class S3Filesystem(Filesystem):

    def __init__(self, config: dict) -> None:
        self._config = config
        self._bucket = config.get('bucket', '')
        self._url = config.get('url')
        self._endpoint = config.get('endpoint')
        self._visibility = config.get('visibility', 'private')

        s3_kwargs: dict = {}

        key = config.get('key')
        secret = config.get('secret')
        if key:
            s3_kwargs['key'] = key
        if secret:
            s3_kwargs['secret'] = secret

        region = config.get('region')
        if region:
            s3_kwargs['client_kwargs'] = {'region_name': region}

        if self._endpoint:
            s3_kwargs['endpoint_url'] = self._endpoint

        if config.get('use_path_style_endpoint'):
            s3_kwargs['config_kwargs'] = {'s3': {'addressing_style': 'path'}}

        self._fs = fsspec.filesystem('s3', **s3_kwargs)

    def driver(self) -> str:
        return 's3'

    def _resolve(self, path: str) -> str:
        return f"{self._bucket}/{path.lstrip('/')}"

    def _relative(self, path: str) -> str:
        prefix = f"{self._bucket}/"
        if path.startswith(prefix):
            return path[len(prefix):]
        return path.lstrip('/')

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
            info = self._fs.info(self._resolve(path))
            last_modified = info.get('LastModified')
            if last_modified is None:
                return Failure(Error(GenericError.EXCEPTION, details={
                    'operation': 'last_modified', 'path': path,
                    'exception': KeyError('LastModified'),
                }))
            return Success(int(last_modified.timestamp()))
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

    # --- Async I/O (s3fs is async-capable, but its coroutines run on the
    #     filesystem's internal loop; delegate via a thread for correctness and
    #     parity with LocalFilesystem, avoiding cross-loop coupling) ---

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
        if self._url:
            return f"{self._url.rstrip('/')}/{path.lstrip('/')}"
        base = (self._endpoint or 'https://s3.amazonaws.com').rstrip('/')
        return f"{base}/{self._bucket}/{path.lstrip('/')}"

    def temporary_url(self, path: str, expiration: int) -> str:
        try:
            return self._fs.url(self._resolve(path), expires=expiration)
        except Exception as exception:
            raise RuntimeError(
                f"Failed to generate temporary URL for '{path}'"
            ) from exception
