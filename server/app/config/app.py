from framework.utils.env import env


def config():
    return {
        'description': env('APP_DESCRIPTION', 'FOO BAR BAZ'),
    }
