from .packet import Packet


class CommandPacket(Packet):
    def send_command_packet(self, command: str) -> None:
        chunks = [command[i:i+4] for i in range(0, len(command), 4)]
        for sequence, chunk in enumerate(chunks):
            command_packet = self.write_command_packet(chunk, sequence)
            full_packet = self.write_header_to_packet(command_packet)
            self.send(full_packet)
            time.sleep(1)


    def write_command_packet(self, command: str, sequence: int) -> bytearray:
        packet = bytearray(2 + len(command))
        packet[0] = 0x01
        packet[1:2] = int.to_bytes(sequence, length=1, byteorder='little')
        packet[2:] = command.encode('ascii')
        return packet


    def handle_command_response_packet(self, packet: bytearray) -> None:
        if len(packet) < 1:
            raise BattleEyePacketException('Expected packet length to be at least length 1 for server command response')

        sequence = int.from_bytes(packet[0:1], byteorder='little')
        if sequence > 255:
            raise BattleEyePacketException(f"Sequence number in server command response must be less than 255: {sequence:02x}")

        if self._responses[sequence]:
            raise BattleEyePacketException(f"Sequence number {sequence:02x} has already been received")

        if len(packet[1:]) > 0:
            self._responses[sequence] = packet[1:].decode('ascii')
