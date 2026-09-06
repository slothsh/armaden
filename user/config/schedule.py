from armaden.framework.support.env import Env
from armaden.framework.types.schedule import ScheduleConfiguration


def config() -> ScheduleConfiguration:
    return {
        'defaults': {
            'connection': Env.string('SCHEDULE_CONNECTION'),
            'priority': Env.int('SCHEDULE_PRIORITY', 0),
            'queue': Env.string('SCHEDULE_QUEUE'),
            'timezone': Env.string('SCHEDULE_TIMEZONE', 'UTC'),
            'worker': Env.string('SCHEDULE_WORKER', 'shared'),
        },
        'jobs': {
            'discovery': {
                'enabled': Env.bool('SCHEDULE_JOB_DISCOVERY_ENABLED', True),
                'paths': Env.json(
                    'SCHEDULE_JOB_DISCOVERY_PATHS',
                    ['app/jobs'],
                ),
            },
        },
        'scheduler': {
            'enabled': Env.bool('SCHEDULER_ENABLED', True),
        },
    }
