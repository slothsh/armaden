from armaden.framework.support.env import Env
from armaden.framework.types.queue import QueueConfiguration


def config() -> QueueConfiguration:
    return {
        'default': Env.string('QUEUE_CONNECTION', 'sync'),
        'connections': {
            'sync': {
                'driver': 'sync',
            },
            'database': {
                'driver': 'database',
                'connection': Env.string('QUEUE_DATABASE_CONNECTION', 'sqlite'),
                'table': Env.string('QUEUE_DATABASE_TABLE', 'jobs'),
                'failed_table': Env.string(
                    'QUEUE_FAILED_DATABASE_TABLE',
                    'failed_jobs',
                ),
                'queue': Env.string('QUEUE_DATABASE_QUEUE', 'default'),
            },
        },
        'worker': {
            'enabled': Env.bool('QUEUE_WORKER_ENABLED', False),
            'num_workers': Env.int('QUEUE_WORKER_COUNT', 1),
            'sleep': Env.int('QUEUE_WORKER_SLEEP', 3),
            'timeout': Env.int('QUEUE_WORKER_TIMEOUT', 60),
            'tries': Env.int('QUEUE_WORKER_TRIES', 3),
            'backoff': Env.int('QUEUE_WORKER_BACKOFF', 2),
        },
        'failed': {
            'driver': 'file',
            'path': Env.string('QUEUE_FAILED_PATH', 'storage/framework/queue/failed'),
        },
    }
