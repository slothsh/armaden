from typing import ClassVar

from armaden.framework.protocols.event_protocol import EventProtocol


class Event(EventProtocol):
    event_marker: ClassVar[bool] = True
