from abc import ABC
from typing import Any, Callable, Self
import zlib


class Packet(ABC):
    def __init__(self, data: bytes, *, validate: bool = True):
        self._data: bytearray = bytearray(data)
        if validate:
            self.validate_packet_header()
            self.validate_packet_data()


    def __repr__(self) -> str:
        fields = [f"{key}={str(value)}" for key, value in list(self.__dict__.items())]
        return f"{type(self).__name__}({' '.join(fields)})"


    def validate_packet_header(self) -> None:
        if len(self._data) < 7:
            raise BattleEyeInvalidPacketException(f"BattleEye rcon datagram must be at least length 7, but got length {len(self._data)}")

        magic_number = bytes(self._data[0:2])
        if magic_number != b"BE":
            raise BattleEyeInvalidPacketException(f"Invalid magic number in BattleEye Rcon client: {magic_number}")

        if self._data[6] != 0xff:
            raise BattleEyeInvalidPacketException(f"Invalid terminator at end of BattleEye Rcon client header: {self._data[6]}")

        client_checksum = int.from_bytes(self._data[2:6], byteorder='little')
        data_checksum = zlib.crc32(self._data[6:]) & 0xffffffff

        if client_checksum != data_checksum:
            raise BattleEyeInvalidPacketException(f"The client's checksum does not match the checksum of the payload, client: {client_checksum:08x} data: {data_checksum:08x}")


    def validate_packet_data(self) -> None:
        raise NotImplementedError()


    @classmethod
    def prepend_header(cls, data: bytes) -> bytearray:
        header = bytearray(7 + len(data))
        terminated_data = bytearray([0xff])
        terminated_data.extend(data)
        checksum = zlib.crc32(terminated_data) & 0xffffffff
        header[0:2] = b"BE"
        header[2:6] = int.to_bytes(checksum, length=4, byteorder='little')
        header[6:] = terminated_data
        return header


    @classmethod
    def packet_data(cls, *args, **kwargs) -> bytearray:
        _ = args
        _ = kwargs
        raise NotImplementedError()


    @classmethod
    def try_any_from_datagram(cls, datagram: bytes, factories: list[Callable[..., Self]], default: Callable[..., Self]) -> Self:
        for factory in factories:
            try:
                instance: Self = factory(bytearray(datagram))
                return instance
            except BattleEyeInvalidPacketException:
                continue

        return default(bytearray(datagram))


    @classmethod
    def new(cls, factory: Callable[..., Self], *args, **kwargs) -> Self:
        instance: Self = factory(bytearray([]), validate=False)
        data = instance.packet_data(*args, **kwargs)
        return factory(data, validate=True)


    def to_bytes(self) -> bytes:
        return bytes(self._data)


# -- Internal Types ----------------------------------------------------------=

class BattleEyeInvalidPacketException(Exception):
    pass
