class ServerMessagePacket(Packet):
    def write_acknowledge_server_message_packet(self, sequence: int) -> bytearray:
        packet = bytearray(2)
        packet[0] = 0x02
        packet[1:2] = int.to_bytes(sequence, length=1, byteorder='little')
        return packet
