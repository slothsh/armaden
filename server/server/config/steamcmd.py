from server.lib.facades import env


def config():
    return {
        'executable': env('STEAMCMD_EXECUTABLE')
    }
