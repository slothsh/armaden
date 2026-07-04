from .packet import BattleEyeInvalidPacketException, Packet


class ServerMessageRequestPacket(Packet):
    def __init__(self, data: bytes, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self._sequence: int = self._extract_sequence(data)
        self._message_data: bytes = self._extract_message_data(data)


    @property
    def sequence(self) -> int:
        return self._sequence


    @property
    def message_data(self) -> bytes:
        return self._message_data


    def validate_packet_data(self) -> None:
        packet_data = self._data[7:]

        if packet_data[0] != 0x02:
            raise BattleEyeInvalidPacketException(f"Invalid Battle Eye server message packet identifier, expected value 0x02 but got {packet_data[0]:02x}")


    @classmethod
    def packet_data(cls, sequence: int, message_data: bytes) -> bytearray:
        data = bytearray(2 + len(message_data))
        data[0] = 0x02
        data[1:2] = int.to_bytes(sequence, length=1, byteorder='little')
        data[2:] = message_data
        packet = cls.prepend_header(bytes(data))
        return packet


    def _extract_sequence(self, data: bytes) -> int:
        if len(data) < 10:
            return 0
        return int.from_bytes(data[8:9], byteorder='little')


    def _extract_message_data(self, data: bytes) -> bytes:
        if len(data) < 10:
            return b""
        return data[9:]
