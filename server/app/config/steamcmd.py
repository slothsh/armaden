from framework.utils.env import env


def config():
    return {
        'executable': env('STEAMCMD_EXECUTABLE')
    }
