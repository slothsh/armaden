from enum import IntEnum


class LoginStatus(IntEnum):
    DENIED = 0x00
    AUTHENTICATED = 0x01
