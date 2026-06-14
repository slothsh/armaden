from importlib import metadata

def config():
    package_name = 'server' if not __package__ else __package__.split('.')[0]
    version_keys = ['major', 'minor', 'patch', 'label']

    return {
        'name': 'Server Tools',
        'description': 'Tools for orchestrating game server executables & exposing them to an API',
        "version": {
            k: int(v) if v.isdigit() else v 
            for k, v in list(zip(version_keys, metadata.version(package_name).replace("-", ".").split(".")))[:len(version_keys)]
        }
    }
