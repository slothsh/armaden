from .packet import BattleEyeInvalidPacketException, Packet


class ServerMessageResponsePacket(Packet):
    def __init__(self, data: bytes, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self._request_sequence: int = self._extract_sequence(data)


    @property
    def request_sequence(self) -> int:
        return self._request_sequence


    def validate_packet_data(self) -> None:
        packet_data = self._data[7:]

        if packet_data[0] != 0x02:
            raise BattleEyeInvalidPacketException(f"Invalid Battle Eye server message response packet identifier, expected value 0x02 but got {packet_data[0]:02x}")


    @classmethod
    def packet_data(cls, request_sequence: int) -> bytearray:
        data = bytearray(2)
        data[0] = 0x02
        data[1:2] = int.to_bytes(request_sequence, length=1, byteorder='little')
        packet = cls.prepend_header(bytes(data))
        return packet


    def _extract_sequence(self, data: bytes) -> int:
        if len(data) < 10:
            return 0
        return int.from_bytes(data[8:9], byteorder='little')
