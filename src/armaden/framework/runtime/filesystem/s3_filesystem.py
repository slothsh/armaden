from __future__ import annotations

import asyncio
from collections.abc import Mapping
from datetime import datetime
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
from armaden.framework.runtime.filesystem.exceptions.s3_filesystem_error import (
    S3FilesystemError,
)
from armaden.framework.runtime.filesystem.exceptions.s3_filesystem_path_exception import (
    S3FilesystemPathException,
)
from armaden.framework.types.result import Result


class S3Filesystem(FilesystemProtocol):
    def __init__(self, config: Mapping[str, object]) -> None:
        self._config: Mapping[str, object] = config
        bucket = config.get('bucket')
        self._bucket: str = bucket if isinstance(bucket, str) else ''
        url = config.get('url')
        self._url: str | None = url if isinstance(url, str) and url else None
        endpoint = config.get('endpoint')
        self._endpoint: str | None = endpoint if isinstance(endpoint, str) and endpoint else None
        self._visibility: object = config.get('visibility', 'private')

        s3_kwargs: dict[str, object] = {}
        key = config.get('key')
        secret = config.get('secret')
        if isinstance(key, str) and key:
            s3_kwargs['key'] = key
        if isinstance(secret, str) and secret:
            s3_kwargs['secret'] = secret

        region = config.get('region')
        if isinstance(region, str) and region:
            s3_kwargs['client_kwargs'] = {'region_name': region}
        if self._endpoint is not None:
            s3_kwargs['endpoint_url'] = self._endpoint
        if config.get('use_path_style_endpoint') is True:
            s3_kwargs['config_kwargs'] = {'s3': {'addressing_style': 'path'}}

        self._filesystem: FsspecFilesystemProtocol = create_fsspec_filesystem(
            's3',
            s3_kwargs,
        )


    @override
    async def copy_async(self, source: str, destination: str) -> Result[bool]:
        return await asyncio.to_thread(self.copy, source, destination)


    @override
    def copy(self, source: str, destination: str) -> Result[bool]:
        try:
            self._filesystem.copy(self._resolve(source), self._resolve(destination))
            return Success(True)
        except S3FilesystemPathException as exception:
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
        except S3FilesystemPathException as exception:
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
        except S3FilesystemPathException as exception:
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
        except S3FilesystemPathException as exception:
            return Failure(self._path_error(exception))
        except Exception as exception:
            return Failure(self._operation_error(
                'directories', exception, {'directory': directory},
            ))


    @override
    def driver(self) -> str:
        return 's3'


    @override
    async def exists_async(self, path: str) -> Result[bool]:
        return await asyncio.to_thread(self.exists, path)


    @override
    def exists(self, path: str) -> Result[bool]:
        try:
            return Success(self._filesystem.exists(self._resolve(path)))
        except S3FilesystemPathException as exception:
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
        except S3FilesystemPathException as exception:
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
        except S3FilesystemPathException as exception:
            return Failure(self._path_error(exception))
        except Exception as exception:
            return Failure(self._operation_error('get', exception, {'path': path}))


    @override
    async def last_modified_async(self, path: str) -> Result[int]:
        return await asyncio.to_thread(self.last_modified, path)


    @override
    def last_modified(self, path: str) -> Result[int]:
        try:
            info = self._filesystem.info(self._resolve(path))
            modified = info.get('LastModified')
            if not isinstance(modified, datetime):
                return Failure(self._operation_error(
                    'last_modified', KeyError('LastModified'), {'path': path},
                ))
            return Success(int(modified.timestamp()))
        except S3FilesystemPathException as exception:
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
        except S3FilesystemPathException as exception:
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
        except S3FilesystemPathException as exception:
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
        except S3FilesystemPathException as exception:
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
        except S3FilesystemPathException as exception:
            return Failure(self._path_error(exception))
        except Exception as exception:
            return Failure(self._operation_error('size', exception, {'path': path}))


    @override
    def temporary_url(self, path: str, expiration: int) -> str:
        try:
            return self._filesystem.url(self._resolve(path), expires=expiration)
        except S3FilesystemPathException as exception:
            raise RuntimeError(str(self._path_error(exception))) from exception
        except Exception as exception:
            raise RuntimeError(f"Failed to generate temporary URL for '{path}'") from exception


    @override
    def url(self, path: str) -> str:
        if self._url is not None:
            return f'{self._url.rstrip("/")}/{path.lstrip("/")}'
        endpoint = (self._endpoint or 'https://s3.amazonaws.com').rstrip('/')
        return f'{endpoint}/{self._bucket}/{path.lstrip("/")}'


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
        return Error(S3FilesystemError.OPERATION_FAILED, details=error_details)


    def _path_error(self, exception: S3FilesystemPathException) -> ErrorProtocol:
        return Error(S3FilesystemError.PATH_OUTSIDE_ROOT, details={
            'path': exception.path,
            'exception': exception,
        })


    def _relative(self, path: str) -> str:
        prefix = f'{self._bucket}/'
        if path.startswith(prefix):
            return path[len(prefix):]
        return path.lstrip('/')


    def _resolve(self, path: str) -> str:
        path_parts = path.replace('\\', '/').split('/')
        if '..' in path_parts:
            raise S3FilesystemPathException(path)
        return f'{self._bucket}/{path.lstrip("/")}'
