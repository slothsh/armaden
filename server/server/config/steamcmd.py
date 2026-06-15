from server.facades.env import env


def config():
    return {
        'executable': env('STEAMCMD_EXECUTABLE')
    }
