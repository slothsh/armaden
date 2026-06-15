import logging

from server.application.kernel import Kernel

logger = logging.getLogger('server.application')


class Application(Kernel):
    def __init__(self):
        super().__init__(self)


# -- Internal Types -----------------------------------------------------------

class ApplicationException(Exception):
    pass
