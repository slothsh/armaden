from server.facades.env import Env


def config():
    return {
        'address': Env.string('API_ADDRESS', '0.0.0.0'),
        'port': Env.int('API_PORT', 8888),
    }
