from dataclasses import dataclass

from .packet import BattleEyeInvalidPacketException, Packet


class CommandResponsePacket(Packet):
    def __init__(self, data: bytes, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        header, request_sequence, response_data = self._extract_response(data)

        self._response_header: CommandHeader | None = header
        self._request_sequence: int = request_sequence
        self._response_data: bytes | None = response_data


    @property
    def response_header(self) -> CommandHeader | None:
        return self._response_header


    @property
    def request_sequence(self) -> int:
        return self._request_sequence


    @property
    def response_data(self) -> bytes | None:
        return self._response_data


    def validate_packet_data(self) -> None:
        packet_data = self._data[7:]

        if len(packet_data) < 2:
            raise BattleEyeInvalidPacketException(f"Invalid Battle Eye command response packet length, expected value length 2, but got {len(packet_data)}")

        if packet_data[0] != 0x01:
            raise BattleEyeInvalidPacketException(f"Invalid Battle Eye command response packet identifier, expected value 0x01 but got {packet_data[0]:02x}")


    @classmethod
    def packet_data(
        cls,
        request_sequence: int,
        response_data: bytes | None = None,
        command_header: tuple[int, int] | None = None,
    ) -> bytearray:
        header_size = 3 if command_header else 0
        response_data_size = len(response_data) if response_data else 0
        data = bytearray(2 + header_size + response_data_size)
        data[0] = 0x01
        if command_header:
            data[1:2] = int.to_bytes(request_sequence, length=1, byteorder='little')
            data[2] = 0x00
            data[3:4] = int.to_bytes(command_header[0], length=1, byteorder='little')
            data[4:5] = int.to_bytes(command_header[1], length=1, byteorder='little')
            if response_data:
                data[5:] = response_data
        else:
            data[1:2] = int.to_bytes(request_sequence, length=1, byteorder='little')
            if response_data:
                data[2:] = response_data
        packet = cls.prepend_header(bytes(data))
        return packet


    def _extract_response(self, data: bytes) -> tuple[CommandHeader | None, int, bytes | None]:
        header = None
        request_sequence = 0
        response_data: bytes | None = None

        if len(data) < 9:
            return header, request_sequence, response_data

        request_sequence = int.from_bytes(data[8:9], byteorder='little')

        if len(data) < 10:
            return header, request_sequence, response_data

        if data[9] != 0x00:
            response_data = data[9:]
            return header, request_sequence, response_data

        if len(data) < 12:
            return header, request_sequence, response_data

        total_packets = int.from_bytes(data[10:11], byteorder='little')
        index = int.from_bytes(data[11:12], byteorder='little')
        header = CommandHeader(total_packets=total_packets, index=index)
        
        if len(data) >= 12:
            response_data = data[12:]

        return header, request_sequence, response_data


# -- Internal Types -----------------------------------------------------------

@dataclass(frozen=True)
class CommandHeader:
    total_packets: int
    index: int
