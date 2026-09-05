from typing import cast, override

from armaden.framework.facades.facade import Facade
from armaden.framework.protocols.filesystem_protocol import FilesystemProtocol
from armaden.framework.types.result import Result


class StorageFacade(Facade):
    @classmethod
    def copy(cls, source: str, destination: str) -> Result[bool]:
        return cls._default_disk().copy(source, destination)


    @classmethod
    async def copy_async(cls, source: str, destination: str) -> Result[bool]:
        return await cls._default_disk().copy_async(source, destination)


    @classmethod
    def delete(cls, path: str) -> Result[bool]:
        return cls._default_disk().delete(path)


    @classmethod
    async def delete_async(cls, path: str) -> Result[bool]:
        return await cls._default_disk().delete_async(path)


    @classmethod
    def delete_directory(cls, path: str) -> Result[bool]:
        return cls._default_disk().delete_directory(path)


    @classmethod
    async def delete_directory_async(cls, path: str) -> Result[bool]:
        return await cls._default_disk().delete_directory_async(path)


    @classmethod
    def directories(cls, directory: str | None = None) -> Result[list[str]]:
        return cls._default_disk().directories(directory)


    @classmethod
    async def directories_async(cls, directory: str | None = None) -> Result[list[str]]:
        return await cls._default_disk().directories_async(directory)


    @classmethod
    def disk(cls, name: str | None = None) -> FilesystemProtocol:
        if name is None:
            return cls._default_disk()
        application = cls.get_facade_application()
        if application is None:
            return cast(FilesystemProtocol, cls.get_facade_root())
        return cast(
            FilesystemProtocol,
            application.make(f'filesystem.disk.{name}'),
        )


    @classmethod
    def exists(cls, path: str) -> Result[bool]:
        return cls._default_disk().exists(path)


    @classmethod
    async def exists_async(cls, path: str) -> Result[bool]:
        return await cls._default_disk().exists_async(path)


    @classmethod
    def files(cls, directory: str | None = None) -> Result[list[str]]:
        return cls._default_disk().files(directory)


    @classmethod
    async def files_async(cls, directory: str | None = None) -> Result[list[str]]:
        return await cls._default_disk().files_async(directory)


    @classmethod
    def get(cls, path: str) -> Result[str | bytes]:
        return cls._default_disk().get(path)


    @classmethod
    async def get_async(cls, path: str) -> Result[str | bytes]:
        return await cls._default_disk().get_async(path)


    @override
    @classmethod
    def get_facade_accessor(cls) -> object:
        return 'filesystem.disk.default'


    @classmethod
    def last_modified(cls, path: str) -> Result[int]:
        return cls._default_disk().last_modified(path)


    @classmethod
    async def last_modified_async(cls, path: str) -> Result[int]:
        return await cls._default_disk().last_modified_async(path)


    @classmethod
    def make_directory(cls, path: str) -> Result[bool]:
        return cls._default_disk().make_directory(path)


    @classmethod
    async def make_directory_async(cls, path: str) -> Result[bool]:
        return await cls._default_disk().make_directory_async(path)


    @classmethod
    def missing(cls, path: str) -> Result[bool]:
        return cls._default_disk().missing(path)


    @classmethod
    async def missing_async(cls, path: str) -> Result[bool]:
        return await cls._default_disk().missing_async(path)


    @classmethod
    def move(cls, source: str, destination: str) -> Result[bool]:
        return cls._default_disk().move(source, destination)


    @classmethod
    async def move_async(cls, source: str, destination: str) -> Result[bool]:
        return await cls._default_disk().move_async(source, destination)


    @classmethod
    def path(cls, path: str) -> str:
        return cls._default_disk().path(path)


    @classmethod
    def put(cls, path: str, contents: str | bytes) -> Result[bool]:
        return cls._default_disk().put(path, contents)


    @classmethod
    async def put_async(cls, path: str, contents: str | bytes) -> Result[bool]:
        return await cls._default_disk().put_async(path, contents)


    @classmethod
    def size(cls, path: str) -> Result[int]:
        return cls._default_disk().size(path)


    @classmethod
    async def size_async(cls, path: str) -> Result[int]:
        return await cls._default_disk().size_async(path)


    @classmethod
    def temporary_url(cls, path: str, expiration: int) -> str:
        return cls._default_disk().temporary_url(path, expiration)


    @classmethod
    def url(cls, path: str) -> str:
        return cls._default_disk().url(path)


    @classmethod
    def _default_disk(cls) -> FilesystemProtocol:
        return cast(FilesystemProtocol, cls.get_facade_root())
