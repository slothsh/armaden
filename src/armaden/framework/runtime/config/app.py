from armaden.framework.support.env import Env
from armaden.framework.types.app import AppConfiguration


def config() -> AppConfiguration:
    return {
        'name': Env.string('APP_NAME', 'Armaden'),
        'discovery': {
            'enabled': Env.bool('APP_DISCOVERY_ENABLED', False),
            'paths': Env.json('APP_DISCOVERY_PATHS', ['app']),
            'bind': {
                'self': True,
                'shared': True,
                'interfaces': True,
                'excluded_interfaces': Env.optional_json(
                    'APP_DISCOVERY_EXCLUDED_INTERFACES',
                ),
            },
        },
    }
