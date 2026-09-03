from __future__ import annotations

from typing import cast


class Array:
    @staticmethod
    def array_wrap(value: object | None) -> list[object]:
        if value is None:
            return []
        if isinstance(value, (list, tuple, set)):
            values = cast(list[object] | tuple[object, ...] | set[object], value)
            return list(values)
        return [value]
