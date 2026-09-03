from pathlib import Path

from armaden.framework.utils.env import Env


def config():
    return {
        'default': Env.string('FILESYSTEM_DISK', 'local'),
        'disks': {
            'local': {
                'driver': 'local',
                'root': str(Path('storage/app').absolute()),
                'url': Env.string('LOCAL_STORAGE_URL', '/storage'),
                'visibility': 'public',
            },
            's3': {
                'driver': 's3',
                'key': Env.string('AWS_ACCESS_KEY_ID', ''),
                'secret': Env.string('AWS_SECRET_ACCESS_KEY', ''),
                'region': Env.string('AWS_DEFAULT_REGION', 'us-east-1'),
                'bucket': Env.string('AWS_BUCKET', ''),
                'url': Env.string('AWS_URL', ''),
                'endpoint': Env.string('AWS_ENDPOINT', ''),
                'use_path_style_endpoint': Env.bool('AWS_USE_PATH_STYLE_ENDPOINT', False),
                'visibility': 'public',
            },
        },
        'links': {
            'public/storage': 'storage/app/public',
        },
    }
