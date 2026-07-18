from __future__ import annotations

from abc import ABC, abstractmethod

from returns.result import Result

from armaden.framework.protocols.error import ErrorInterface


class Filesystem(ABC):

    @abstractmethod
    def exists(self, path: str) -> Result[bool, ErrorInterface]: ...

    @abstractmethod
    def missing(self, path: str) -> Result[bool, ErrorInterface]: ...

    @abstractmethod
    def get(self, path: str) -> Result[str, ErrorInterface]: ...

    @abstractmethod
    def put(self, path: str, contents: str | bytes) -> Result[bool, ErrorInterface]: ...

    @abstractmethod
    def delete(self, path: str) -> Result[bool, ErrorInterface]: ...

    @abstractmethod
    def copy(self, source: str, destination: str) -> Result[bool, ErrorInterface]: ...

    @abstractmethod
    def move(self, source: str, destination: str) -> Result[bool, ErrorInterface]: ...

    @abstractmethod
    def size(self, path: str) -> Result[int, ErrorInterface]: ...

    @abstractmethod
    def last_modified(self, path: str) -> Result[int, ErrorInterface]: ...

    @abstractmethod
    def files(self, directory: str | None = None) -> Result[list[str], ErrorInterface]: ...

    @abstractmethod
    def directories(self, directory: str | None = None) -> Result[list[str], ErrorInterface]: ...

    @abstractmethod
    def make_directory(self, path: str) -> Result[bool, ErrorInterface]: ...

    @abstractmethod
    def delete_directory(self, path: str) -> Result[bool, ErrorInterface]: ...

    @abstractmethod
    async def exists_async(self, path: str) -> Result[bool, ErrorInterface]: ...

    @abstractmethod
    async def missing_async(self, path: str) -> Result[bool, ErrorInterface]: ...

    @abstractmethod
    async def get_async(self, path: str) -> Result[str, ErrorInterface]: ...

    @abstractmethod
    async def put_async(self, path: str, contents: str | bytes) -> Result[bool, ErrorInterface]: ...

    @abstractmethod
    async def delete_async(self, path: str) -> Result[bool, ErrorInterface]: ...

    @abstractmethod
    async def copy_async(self, source: str, destination: str) -> Result[bool, ErrorInterface]: ...

    @abstractmethod
    async def move_async(self, source: str, destination: str) -> Result[bool, ErrorInterface]: ...

    @abstractmethod
    async def size_async(self, path: str) -> Result[int, ErrorInterface]: ...

    @abstractmethod
    async def last_modified_async(self, path: str) -> Result[int, ErrorInterface]: ...

    @abstractmethod
    async def files_async(self, directory: str | None = None) -> Result[list[str], ErrorInterface]: ...

    @abstractmethod
    async def directories_async(self, directory: str | None = None) -> Result[list[str], ErrorInterface]: ...

    @abstractmethod
    async def make_directory_async(self, path: str) -> Result[bool, ErrorInterface]: ...

    @abstractmethod
    async def delete_directory_async(self, path: str) -> Result[bool, ErrorInterface]: ...

    @abstractmethod
    def driver(self) -> str: ...

    def path(self, path: str) -> str:
        raise RuntimeError(
            f"Filesystem driver '{self.driver()}' does not support resolving OS paths"
        )

    def url(self, path: str) -> str:
        raise RuntimeError(
            f"Filesystem driver '{self.driver()}' does not support public URLs"
        )

    def temporary_url(self, path: str, expiration: int) -> str:
        raise RuntimeError(
            f"Filesystem driver '{self.driver()}' does not support temporary URLs"
        )
