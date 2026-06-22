from framework.protocols.application import ApplicationInterface
from framework.protocols.service_manager import ServiceManagerInterface
from framework.protocols.supervisor import SupervisorInterface


class Application(ApplicationInterface):
    """Convenience base that stores injected runtime dependencies
    so user code can write ``self.supervisor`` and ``self.service_manager``.
    """

    def configure(
        self,
        service_manager: ServiceManagerInterface,
        supervisor: SupervisorInterface,
    ) -> None:
        self._service_manager = service_manager
        self._supervisor = supervisor

    @property
    def service_manager(self) -> ServiceManagerInterface:
        if self._service_manager is None:
            raise RuntimeError("service_manager not available – did you call configure()?")
        return self._service_manager

    @property
    def supervisor(self) -> SupervisorInterface:
        if self._supervisor is None:
            raise RuntimeError("supervisor not available – did you call configure()?")
        return self._supervisor
