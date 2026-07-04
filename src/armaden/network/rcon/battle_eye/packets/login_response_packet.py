from armaden.network.rcon.battle_eye.enums.login_status import LoginStatus

from .packet import BattleEyeInvalidPacketException, Packet


class LoginResponsePacket(Packet):
    def __init__(self, data: bytes, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self._status: int = self._extract_status(data)


    @property
    def authenticated(self) -> bool:
        return self._status == LoginStatus.AUTHENTICATED


    def validate_packet_data(self) -> None:
        packet_data = self._data[7:]

        if packet_data[0] != 0x00:
            raise BattleEyeInvalidPacketException(f"Invalid Battle Eye login response packet identifier, expected value 0x00 but got {packet_data[0]:02x}")


    @classmethod
    def packet_data(cls, status: int) -> bytearray:
        data = bytearray(2)
        data[0] = 0x00
        data[1:2] = int.to_bytes(status, length=1, byteorder='little')
        packet = cls.prepend_header(bytes(data))
        return packet


    def _extract_status(self, data: bytes) -> int:
        if len(data) < 9:
            return 0
        return int.from_bytes(data[8:9], byteorder='little')
