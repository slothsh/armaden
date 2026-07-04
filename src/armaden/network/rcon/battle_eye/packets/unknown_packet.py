from .packet import Packet


class UnknownPacket(Packet):
    def __init__(self, data: bytes, *args, **kwargs):
        _ = args
        _ = kwargs
        super().__init__(data, validate=False)
