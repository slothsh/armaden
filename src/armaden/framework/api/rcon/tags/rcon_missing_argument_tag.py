class RconMissingArgumentTag:
    __slots__: tuple[str, ...] = ()


RCON_MISSING_ARGUMENT = RconMissingArgumentTag()

__all__ = [
    'RconMissingArgumentTag',
    'RCON_MISSING_ARGUMENT',
]
