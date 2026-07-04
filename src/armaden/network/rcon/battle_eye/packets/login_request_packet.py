from .packet import BattleEyeInvalidPacketException, Packet


class LoginRequestPacket(Packet):
    def __init__(self, data: bytes, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self._password: str = self._extract_password(data)


    @property
    def password(self) -> str:
        return self._password


    def validate_packet_data(self) -> None:
        packet_data = self._data[7:]

        if packet_data[0] != 0x00:
            raise BattleEyeInvalidPacketException(f"Invalid Battle Eye login request packet identifier, expected value 0x00 but got {packet_data[0]:02x}")


    @classmethod
    def packet_data(cls, password: str) -> bytearray:
        data = bytearray(1 + len(password))
        data[0] = 0x00
        data[1:] = password.encode('ascii')
        packet = cls.prepend_header(bytes(data))
        return packet


    def _extract_password(self, data: bytes) -> str:
        if len(data) < 9:
            return ''
        return data[8:].decode('ascii')
