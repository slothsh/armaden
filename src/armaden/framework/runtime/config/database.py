from armaden.framework.support.env import Env
from armaden.framework.types.database import DatabaseConfiguration


def config() -> DatabaseConfiguration:
    return {
        'default': Env.string('DB_CONNECTION', 'sqlite'),
        'connections': {
            'sqlite': {
                'driver': 'sqlite',
                'database': Env.string('DB_DATABASE', 'database.sqlite3'),
                'foreign_key_constraints': Env.bool('DB_FOREIGN_KEYS', True),
            },
            'pgsql': {
                'driver': 'pgsql',
                'host': Env.string('DB_HOST', '127.0.0.1'),
                'port': Env.int('DB_PORT', 5432),
                'database': Env.string('DB_DATABASE', ''),
                'username': Env.string('DB_USERNAME', ''),
                'password': Env.string('DB_PASSWORD', ''),
                'prefix': '',
            },
            'mysql': {
                'driver': 'mysql',
                'host': Env.string('DB_HOST', '127.0.0.1'),
                'port': Env.int('DB_PORT', 3306),
                'database': Env.string('DB_DATABASE', ''),
                'username': Env.string('DB_USERNAME', ''),
                'password': Env.string('DB_PASSWORD', ''),
                'prefix': '',
            },
            'mssql': {
                'driver': 'mssql',
                'host': Env.string('DB_HOST', '127.0.0.1'),
                'port': Env.int('DB_PORT', 1433),
                'database': Env.string('DB_DATABASE', ''),
                'username': Env.string('DB_USERNAME', ''),
                'password': Env.string('DB_PASSWORD', ''),
                'prefix': '',
            },
        },
    }
