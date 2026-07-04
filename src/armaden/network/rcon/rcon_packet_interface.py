from typing import Protocol


class RconPacketInterface(Protocol):
    def to_bytes(self) -> bytes: ...
