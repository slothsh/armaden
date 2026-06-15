
def app():
    from server.application.application import Application
    return Application.instance()
