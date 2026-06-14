from server.bootstrap import Application

def env(name: str, default: str | None = None) -> str | None:
    return Application.instance().environment(name, default)


def app() -> Application:
    return Application.instance()
