from returns.result import Success

from framework.classes.service import Service
from framework.utils.types import Result
from framework.facades import app

from app.api.api_server import ApiServer
from app.http.routes.api_routes import api_routes


class ApiService(Service):
    name = 'api'

    def __call__(self) -> Result[None]:
        api_server = (
            ApiServer()
            .with_routes(api_routes)
            .build()
        )

        self.status_callbacks.extend([
            ('server', api_server.status)
        ])

        app().supervisor.with_server(api_server)

        return Success(None)
