from typing import cast
from armaden.framework.support.env import Env

from armaden.games.arma_reforger import ArmaReforgerServerConfig


def config() -> ArmaReforgerServerConfig:
    return cast(ArmaReforgerServerConfig, cast(object, {
        'executable': Env.string('ARMA_REFORGER_EXECUTABLE'),
        'steamExecutable': Env.string('STEAMCMD_EXECUTABLE'),
        'installDirectory': Env.string('ARMA_REFORGER_INSTALL_DIR'),
        'steamInstallDirectory': Env.string('STEAMCMD_INSTALL_DIR'),
        'skipUpdate': Env.bool('STEAMCMD_SKIP_UPDATE', False),
        'startup': {
            'profileDirectory': Env.string('ARMA_REFORGER_PROFILE_DIR'),
            'logsDirectory': Env.string('ARMA_REFORGER_LOGS_DIR'),
            },
        'server': {
            'rcon': {
                'permission': Env.string('ARMA_REFORGER_RCON_PERMISSION'),
                'password': 'foobarbaz',
                },
            'game': {
                'gameProperties': {
                    'serverMaxViewDistance': Env.int(
                        'ARMAREFORGER_GAME_PROPERTIES_SERVER_MAX_VIEW_DISTANCE',
                        ),
                    },
                },
            },
        }))
