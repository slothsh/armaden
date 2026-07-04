from .packet import BattleEyeInvalidPacketException, Packet


class KeepAlivePacket(Packet):
    def __init__(self, data: bytes, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self.sequence: int = self._extract_sequence(data)


    def validate_packet_data(self) -> None:
        packet_data = self._data[7:]

        if packet_data[0] != 0x01:
            raise BattleEyeInvalidPacketException(f"Invalid Battle Eye keep alive packet identifier, expected value 0x01 but got {packet_data[0]:02x}")

        if len(packet_data) > 2:
            raise BattleEyeInvalidPacketException(f"Keep alive packet data must be exactly 2 bytes, but got length {len(packet_data)}")


    @classmethod
    def packet_data(cls, sequence: int) -> bytearray:
        data = bytearray(2)
        data[0] = 0x01
        data[1:2] = int.to_bytes(sequence, length=1, byteorder='little')
        packet = cls.prepend_header(bytes(data))
        return packet


    def _extract_sequence(self, data: bytes) -> int:
        if len(data) < 9:
            return 0

        return int.from_bytes(data[8:9], byteorder='little')
