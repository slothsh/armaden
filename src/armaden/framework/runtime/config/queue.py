from armaden.framework.support.env import Env
from armaden.framework.types.queue import QueueConfiguration


def config() -> QueueConfiguration:
    return {
        'default': Env.string('QUEUE_CONNECTION', 'sync'),
        'connections': {
            'sync': {
                'driver': 'sync',
            },
        },
        'failed': {
            'driver': 'file',
            'path': Env.string('QUEUE_FAILED_PATH', 'storage/framework/queue/failed'),
        },
    }
