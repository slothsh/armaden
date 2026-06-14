from server.lib.facades import Env


def config():
    return {
        'address': Env.string('API_ADDRESS', '127.0.0.1'),
        'port': Env.int('API_PORT', 8888),
    }
