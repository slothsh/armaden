from __future__ import annotations

from collections.abc import Mapping
from contextvars import ContextVar, Token


class ScheduleGroup:
    _defaults: ContextVar[tuple[Mapping[str, object], ...]] = ContextVar(
        'schedule_group_defaults',
        default=(),
    )

    def __init__(self, values: Mapping[str, object]) -> None:
        self._token: Token[tuple[Mapping[str, object], ...]] | None = None
        self._values: Mapping[str, object] = dict(values)


    def __enter__(self) -> ScheduleGroup:
        stack = self._defaults.get()
        self._token = self._defaults.set((*stack, self._values))
        return self


    def __exit__(self, *args: object) -> None:
        _ = args
        if self._token is not None:
            self._defaults.reset(self._token)
            self._token = None


    @classmethod
    def defaults(cls) -> Mapping[str, object]:
        values: dict[str, object] = {}
        for group in cls._defaults.get():
            values.update(group)
        return values
