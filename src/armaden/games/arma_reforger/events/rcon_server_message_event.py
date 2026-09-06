from dataclasses import dataclass

from armaden.framework.api.event import Event


@dataclass
class RconServerMessageEvent(Event):
    message: str
