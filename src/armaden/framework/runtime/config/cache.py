from armaden.framework.utils.env import Env


def config():
    return {
        'default': Env.string('CACHE_STORE', 'file'),
        'stores': {
            'file': {
                'driver': 'file',
                'disk': Env.string('CACHE_FILE_DISK', 'local'),
                'path': Env.string('CACHE_FILE_PATH', 'storage/framework/cache/data'),
            },
        },
        'prefix': Env.string('CACHE_PREFIX', 'armaden_cache'),
        'hash_keys': Env.bool('CACHE_HASH_KEYS', True),
        'serializer': {
            'default': Env.string('CACHE_SERIALIZER', 'json'),
            'auto_detect_type': Env.bool('CACHE_SERIALIZER_AUTO_DETECT', True),
            'version': 1,
        },
        'ttl': Env.int('CACHE_DEFAULT_TTL', 3600),
    }
