from __future__ import annotations

from typing import TYPE_CHECKING

from ._registry import get_application

if TYPE_CHECKING:
    from armaden.framework.protocols.filesystem import Filesystem
    from armaden.framework.utils.types import Result


class Storage:

    @classmethod
    def disk(cls, name: str | None = None) -> 'Filesystem':
        container = get_application().container
        if name is None:
            return container.get('filesystem.disk.default')
        return container.get(f'filesystem.disk.{name}')

    @classmethod
    def _default_disk(cls) -> 'Filesystem':
        return cls.disk(None)

    @classmethod
    def exists(cls, path: str) -> 'Result[bool]':
        return cls._default_disk().exists(path)

    @classmethod
    def missing(cls, path: str) -> 'Result[bool]':
        return cls._default_disk().missing(path)

    @classmethod
    def get(cls, path: str) -> 'Result[str]':
        return cls._default_disk().get(path)

    @classmethod
    def put(cls, path: str, contents: str | bytes) -> 'Result[bool]':
        return cls._default_disk().put(path, contents)

    @classmethod
    def delete(cls, path: str) -> 'Result[bool]':
        return cls._default_disk().delete(path)

    @classmethod
    def copy(cls, source: str, destination: str) -> 'Result[bool]':
        return cls._default_disk().copy(source, destination)

    @classmethod
    def move(cls, source: str, destination: str) -> 'Result[bool]':
        return cls._default_disk().move(source, destination)

    @classmethod
    def size(cls, path: str) -> 'Result[int]':
        return cls._default_disk().size(path)

    @classmethod
    def last_modified(cls, path: str) -> 'Result[int]':
        return cls._default_disk().last_modified(path)

    @classmethod
    def files(cls, directory: str | None = None) -> 'Result[list[str]]':
        return cls._default_disk().files(directory)

    @classmethod
    def directories(cls, directory: str | None = None) -> 'Result[list[str]]':
        return cls._default_disk().directories(directory)

    @classmethod
    def make_directory(cls, path: str) -> 'Result[bool]':
        return cls._default_disk().make_directory(path)

    @classmethod
    def delete_directory(cls, path: str) -> 'Result[bool]':
        return cls._default_disk().delete_directory(path)

    @classmethod
    def path(cls, path: str) -> str:
        return cls._default_disk().path(path)

    @classmethod
    def url(cls, path: str) -> str:
        return cls._default_disk().url(path)

    @classmethod
    def temporary_url(cls, path: str, expiration: int) -> str:
        return cls._default_disk().temporary_url(path, expiration)

    @classmethod
    async def exists_async(cls, path: str) -> 'Result[bool]':
        return await cls._default_disk().exists_async(path)

    @classmethod
    async def missing_async(cls, path: str) -> 'Result[bool]':
        return await cls._default_disk().missing_async(path)

    @classmethod
    async def get_async(cls, path: str) -> 'Result[str]':
        return await cls._default_disk().get_async(path)

    @classmethod
    async def put_async(cls, path: str, contents: str | bytes) -> 'Result[bool]':
        return await cls._default_disk().put_async(path, contents)

    @classmethod
    async def delete_async(cls, path: str) -> 'Result[bool]':
        return await cls._default_disk().delete_async(path)

    @classmethod
    async def copy_async(cls, source: str, destination: str) -> 'Result[bool]':
        return await cls._default_disk().copy_async(source, destination)

    @classmethod
    async def move_async(cls, source: str, destination: str) -> 'Result[bool]':
        return await cls._default_disk().move_async(source, destination)

    @classmethod
    async def size_async(cls, path: str) -> 'Result[int]':
        return await cls._default_disk().size_async(path)

    @classmethod
    async def last_modified_async(cls, path: str) -> 'Result[int]':
        return await cls._default_disk().last_modified_async(path)

    @classmethod
    async def files_async(cls, directory: str | None = None) -> 'Result[list[str]]':
        return await cls._default_disk().files_async(directory)

    @classmethod
    async def directories_async(cls, directory: str | None = None) -> 'Result[list[str]]':
        return await cls._default_disk().directories_async(directory)

    @classmethod
    async def make_directory_async(cls, path: str) -> 'Result[bool]':
        return await cls._default_disk().make_directory_async(path)

    @classmethod
    async def delete_directory_async(cls, path: str) -> 'Result[bool]':
        return await cls._default_disk().delete_directory_async(path)


def storage() -> 'Filesystem':
    return Storage.disk()
