from typing import Protocol


class CacheSerializerProtocol(Protocol):
    def deserialize(self, data: str | bytes) -> object: ...

    def serialize(self, value: object) -> str: ...
