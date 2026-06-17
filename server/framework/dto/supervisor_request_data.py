from dataclasses import dataclass, field
from typing import TypedDict

from framework.enums.supervisor_request_kind import SupervisorRequestKind


@dataclass(frozen=True)
class SupervisorRequestData:
    kind: SupervisorRequestKind
    thread_id: int
    args: SupervisorRequestArgs | None = field(default=None, compare=False)


class SupervisorRequestArgs(TypedDict):
    thread_id: int
