from armaden.framework.utils.env import Env


def config():
    return {
        'defaults': {
            'guard': Env.string('AUTH_GUARD', 'token'),
        },
        'guards': {
            'token': {
                'driver': 'token',
                'header': 'Authorization',
                'prefix': 'Bearer',
                'field': None,
            },
            'basic': {
                'driver': 'basic',
                'header': 'Authorization',
                'prefix': 'Basic',
            },
            'header': {
                'driver': 'header',
                'header': Env.string('AUTH_CUSTOM_HEADER', 'X-API-Key'),
                'prefix': None,
            },
        },
        'providers': {
            'users': {
                'driver': 'config',
            },
        },
        'users': {
            'api': {
                'id': 'api-system',
                'roles': ['admin'],
                'token': Env.string('API_TOKEN', ''),
            },
            'service': {
                'id': 'service-account',
                'roles': ['service'],
                'token': Env.string('SERVICE_TOKEN', ''),
            },
            'admin': {
                'id': 'admin-user',
                'username': Env.string('ADMIN_USERNAME', 'admin'),
                'password': Env.string('ADMIN_PASSWORD', ''),
                'roles': ['admin'],
            },
        },
    }
