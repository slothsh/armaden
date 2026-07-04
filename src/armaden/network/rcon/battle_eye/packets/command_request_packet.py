from .packet import BattleEyeInvalidPacketException, Packet


class CommandRequestPacket(Packet):
    def __init__(self, data: bytes, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self._sequence: int = self._extract_sequence(data)
        self._command_name: str = self._extract_command_name(data)
        self._command_args: list[str] = self._extract_command_args(data)


    @property
    def sequence(self) -> int:
        return self._sequence


    @property
    def command_name(self) -> str:
        return self._command_name


    @property
    def command_args(self) -> list[str]:
        return self._command_args


    def validate_packet_data(self) -> None:
        packet_data = self._data[7:]

        if packet_data[0] != 0x01:
            raise BattleEyeInvalidPacketException(f"Invalid Battle Eye command request packet identifier, expected value 0x01 but got {packet_data[0]:02x}")


    @classmethod
    def packet_data(cls, sequence: int, argv: list[str]) -> bytearray:
        argv_string = ' '.join(argv)
        data = bytearray(2 + len(argv_string))
        data[0] = 0x01
        data[1:2] = int.to_bytes(sequence, length=1, byteorder='little')
        data[2:] = argv_string.encode('ascii')
        packet = cls.prepend_header(bytes(data))
        return packet


    def _extract_sequence(self, data: bytes) -> int:
        if len(data) < 10:
            return 0
        return int.from_bytes(data[8:9], byteorder='little')


    def _extract_command_name(self, data: bytes) -> str:
        if len(data) < 10:
            return ''
        return data[9:].decode('ascii').split(' ')[0]


    def _extract_command_args(self, data: bytes) -> list[str]:
        if len(data) < 10:
            return []
        return data[9:].decode('ascii').split(' ')[1:]
