from framework.utils.env import env
from importlib import metadata


def config():
    version_keys = ['major', 'minor', 'patch', 'label']

    try:
        version = metadata.version('server')
    except metadata.PackageNotFoundError:
        version = '0.0.0'

    return {
        'name': env('APP_NAME', 'Server Tools'),
        'description': env('APP_DESCRIPTION', 'Tools for orchestrating game server executables & exposing them to an API'),
        'version': {
            k: int(v) if v.isdigit() else v
            for k, v in list(zip(version_keys, version.replace("-", ".").split(".")))[:len(version_keys)]
        }
    }
