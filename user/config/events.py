from armaden.framework.support.env import Env
from armaden.framework.types.events import EventsConfiguration


def config() -> EventsConfiguration:
    return {
        'listeners': {
            'discovery': {
                'enabled': Env.bool('EVENT_LISTENER_DISCOVERY_ENABLED', True),
                'paths': Env.json(
                    'EVENT_LISTENER_DISCOVERY_PATHS',
                    ['app/listeners'],
                ),
            },
        },
        'queue': {
            'connection': Env.string('EVENT_QUEUE_CONNECTION', 'sync'),
            'queue': Env.string('EVENT_QUEUE', 'default'),
        },
    }
