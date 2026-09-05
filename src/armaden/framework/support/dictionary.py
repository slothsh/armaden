from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import cast


class Dictionary:
    @classmethod
    def has(
        cls,
        key: str,
        value: object | Callable[[object], bool],
        data: object,
    ) -> bool:
        if isinstance(data, Mapping):
            mapping = cast(Mapping[object, object], data)
            for current_key, current_value in mapping.items():
                if current_key == key:
                    if callable(value):
                        if value(current_value):
                            return True
                    elif current_value == value:
                        return True
                if cls.has(key, value, current_value):
                    return True
        elif isinstance(data, list):
            items = cast(list[object], data)
            return any(cls.has(key, value, item) for item in items)
        return False


    @classmethod
    def merge[T: Mapping[str, object]](
        cls,
        base: T,
        override: Mapping[str, object],
    ) -> T:
        result: dict[str, object] = {}
        for key in base.keys() | override.keys():
            override_value = override.get(key)
            if key in override and override_value is not None:
                base_value = base.get(key)
                if isinstance(base_value, Mapping) and isinstance(override_value, Mapping):
                    result[key] = cls.merge(
                        cast(Mapping[str, object], base_value),
                        cast(Mapping[str, object], override_value),
                    )
                else:
                    result[key] = override_value
            elif key in base:
                result[key] = base[key]
        return cast(T, result)


    @classmethod
    def without(
        cls,
        data: object,
        predicate: Callable[[object, object], bool],
    ) -> object:
        if isinstance(data, Mapping):
            mapping = cast(Mapping[object, object], data)
            return {
                key: cls.without(value, predicate)
                for key, value in mapping.items()
                if not predicate(key, value)
            }
        if isinstance(data, list):
            items = cast(list[object], data)
            return [
                cls.without(item, predicate)
                for item in items
                if not predicate(None, item)
            ]
        return data
