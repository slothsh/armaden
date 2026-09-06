from armaden.framework.types.queue import QueueConfiguration


def config() -> QueueConfiguration:
    return {
        'default': 'jobs',
        'connections': {
            'jobs': {
                'driver': 'database',
                'connection': 'sqlite',
                'table': 'jobs',
                'failed_table': 'failed_jobs',
                'queue': 'jobs',
            },
        },
        'queues': {
            'jobs': {},
        },
        'worker': {
            'enabled': True,
            'num_workers': 1,
            'sleep': 1,
            'timeout': 60,
            'tries': 3,
            'backoff': 2,
        },
    }
