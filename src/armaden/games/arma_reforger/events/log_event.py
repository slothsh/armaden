from dataclasses import dataclass

from armaden.framework.api.event import Event


@dataclass
class LogEvent(Event):
    line: str
