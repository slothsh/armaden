from returns.result import Success

from server.api.api_server import ApiServer
from server.facades.app import app
from server.http.routes.api_routes import api_routes
from server.lib.service import Service
from server.lib.types import Result


class ApiService(Service):
    def __call__(self) -> Result[None]:
        app().supervisor.with_server(
            ApiServer()
                .with_routes(api_routes)
                .build()
        )

        return Success(None)
