import os
from typing import cast

from armaden.games.arma_reforger import ArmaReforgerServerConfig


def _integer(name: str) -> int | None:
    value = os.getenv(name)
    return int(value) if value is not None else None


def _string(name: str) -> str | None:
    return os.getenv(name)


def config() -> ArmaReforgerServerConfig:
    return cast(ArmaReforgerServerConfig, cast(object, {
        'executable': _string('ARMA_REFORGER_EXECUTABLE'),
        'steamExecutable': _string('STEAMCMD_EXECUTABLE'),
        'installDirectory': _string('ARMA_REFORGER_INSTALL_DIR'),
        'steamInstallDirectory': _string('STEAMCMD_INSTALL_DIR'),
        'startup': {
            'profileDirectory': _string('ARMA_REFORGER_PROFILE_DIR'),
            'logsDirectory': _string('ARMA_REFORGER_LOGS_DIR'),
        },
        'server': {
            'rcon': {
                'permission': _string('ARMA_REFORGER_RCON_PERMISSION'),
                'password': 'foobarbaz',
            },
            'game': {
                'gameProperties': {
                    'serverMaxViewDistance': _integer(
                        'ARMA_REFORGER_GAME_PROPERTIES_SERVER_MAX_VIEW_DISTANCE',
                    ),
                },
            },
        },
    }))
