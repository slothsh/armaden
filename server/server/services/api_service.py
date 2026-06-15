from returns.result import Success

from server.api.api_server import ApiServer
from server.facades.app import app
from server.http.routes.api_routes import api_routes
from server.lib.service import Service
from server.lib.types import Result


class ApiService(Service):
    def __init__(self):
        super().__init__()
        self._server = ApiServer()


    def __call__(self) -> Result[None]:
        self._server = (
            self._server
            .with_supervisor(app().supervisor)
            .with_routes(api_routes)
            .build()
        )

        app().supervisor.with_server(self._server)

        return Success(None)
