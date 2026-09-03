from armaden.framework.runtime.supervisor.enums.supervisor_request_kind import SupervisorRequestKind
from dataclasses import dataclass, field
from datetime import datetime
from typing import TypedDict


class SupervisorRequestArgs(TypedDict):
    task_id: int


@dataclass(frozen=True)
class SupervisorRequestData:
    kind: SupervisorRequestKind
    task_id: int
    args: SupervisorRequestArgs | None = field(default=None, compare=False)


@dataclass(frozen=True)
class SupervisorRequestInfoData:
    data: SupervisorRequestData
    time_received: datetime = field(default=datetime.now(), compare=False)
