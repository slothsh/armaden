from armaden.framework.utils.env import Env
from armaden.games.arma_reforger import ArmaReforgerServerConfig


def config() -> ArmaReforgerServerConfig:
    return {
        'executable': Env.string('ARMA_REFORGER_EXECUTABLE'),
        'steamExecutable': Env.string('STEAMCMD_EXECUTABLE'),
        'installDirectory': Env.string('ARMA_REFORGER_INSTALL_DIR'),
        'startup': {
            'profileDirectory': Env.string('ARMA_REFORGER_PROFILE_DIR'),
            'logsDirectory': Env.string('ARMA_REFORGER_LOGS_DIR'),
        },
        'server': {
            'rcon': {
                'permission': Env.string('ARMA_REFORGER_RCON_PERMISSION'),
            },
            'game': {
                'gameProperties': {
                    'serverMaxViewDistance': Env.int('ARMA_REFORGER_GAME_PROPERTIES_SERVER_MAX_VIEW_DISTANCE'),
                },
            },
        },
    }
