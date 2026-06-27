from armaden.framework.classes.instance_container import InstanceContainer
from armaden.framework.protocols.application import ApplicationInterface
from armaden.framework.protocols.supervisor import SupervisorInterface


class Application(ApplicationInterface):
    def __init__(self, container: InstanceContainer) -> None:
        self._container = container

    @property
    def supervisor(self) -> SupervisorInterface:
        return self._container.make(SupervisorInterface)
