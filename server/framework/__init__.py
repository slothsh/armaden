from .utils.types import Result
from .errors import Error, GenericError
from .classes.server import Server
from .protocols import ServiceInterface, KernelInterface, ApplicationInterface
from .classes.executable import Executable
from .utils.dictionary import Dictionary

__all__ = [
    'Result',
    'Error',
    'GenericError',
    'Server',
    'ServiceInterface',
    'KernelInterface',
    'ApplicationInterface',
    'Executable',
    'Dictionary',
]
