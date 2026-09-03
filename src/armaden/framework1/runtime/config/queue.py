from armaden.framework.utils.env import Env


def config():
    return {
        'default': Env.string('QUEUE_CONNECTION', 'sync'),
        'connections': {
            'sync': {
                'driver': 'sync',
            },
            'database': {
                'driver': 'database',
                'connection': Env.string('DB_QUEUE_CONNECTION', 'sqlite'),
                'table': Env.string('DB_QUEUE_TABLE', 'jobs'),
                'failed_table': Env.string('DB_FAILED_JOBS_TABLE', 'failed_jobs'),
                'queue': 'default',
                'retry_after': Env.int('DB_QUEUE_RETRY_AFTER', 90),
            },
            'cache': {
                'driver': 'cache',
                'store': Env.string('CACHE_QUEUE_STORE', 'file'),
                'queue': 'default',
                'retry_after': Env.int('CACHE_QUEUE_RETRY_AFTER', 90),
            },
        },
        'queues': {
            'default': {'priority': 0},
            'high': {'priority': 10},
            'low': {'priority': -10},
        },
        'worker': {
            'num_workers': Env.int('QUEUE_WORKERS', 4),
            'sleep': Env.int('QUEUE_WORKER_SLEEP', 3),
            'timeout': Env.int('QUEUE_WORKER_TIMEOUT', 60),
            'tries': Env.int('QUEUE_WORKER_TRIES', 3),
            'backoff': Env.int('QUEUE_WORKER_BACKOFF', 2),
            'max_exceptions': Env.int('QUEUE_WORKER_MAX_EXCEPTIONS', 3),
        },
        'failed': {
            'database': {
                'connection': Env.string('DB_FAILED_CONNECTION', 'sqlite'),
                'table': Env.string('DB_FAILED_TABLE', 'failed_jobs'),
            },
            'cache': {
                'store': Env.string('CACHE_FAILED_STORE', 'file'),
            },
        },
        'discovery': {
            'paths': ['app/jobs'],
        },
    }
