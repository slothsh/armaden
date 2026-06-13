from server.bootstrap import Application


def app() -> Application:
    return Application.instance()
