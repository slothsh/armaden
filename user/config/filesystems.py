from armaden.framework.support.env import Env
from armaden.framework.types.filesystem import FilesystemConfiguration


def config() -> FilesystemConfiguration:
    return {
        'default': Env.string('FILESYSTEM_DISK', 'local'),
        'disks': {
            'local': {
                'driver': 'local',
                'root': Env.string(
                    'APP_STORAGE_PATH',
                    '/armaden/storage/app',
                ),
                'url': Env.string('LOCAL_STORAGE_URL', '/storage'),
                'visibility': 'public',
            },
        },
    }
