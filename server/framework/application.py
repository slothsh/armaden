from framework.classes.instance_container import InstanceContainer
from framework.protocols.application import ApplicationInterface
from framework.protocols.supervisor import SupervisorInterface


class Application(ApplicationInterface):
    def __init__(self, container: InstanceContainer) -> None:
        self._container = container

    @property
    def supervisor(self) -> SupervisorInterface:
        return self._container.make(SupervisorInterface)
