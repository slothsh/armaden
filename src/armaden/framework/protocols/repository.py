from __future__ import annotations

from typing import Protocol, TypeVar, runtime_checkable

T = TypeVar('T')


@runtime_checkable
class Repository(Protocol[T]):
    def register(self, entity: T) -> None:
        ...

    def get(self, key: str) -> T | None:
        ...

    def all(self) -> list[T]:
        ...

    def remove(self, key: str) -> None:
        ...
