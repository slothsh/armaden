from server.application.application import Application
from server.application.kernel import ApplicationInterface


def app() -> ApplicationInterface:
    return Application.instance()
