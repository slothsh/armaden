from typing import Any
from collections.abc import Callable


class Dictionary:
    @classmethod
    def has(cls, key: str, value: Any | Callable[[Any], bool], data: Any) -> bool:
        if isinstance(data, dict):
            for k, v in data.items():
                if k == key:
                    if callable(value):
                        if value(v):
                            return True
                    elif v == value:
                        return True
                if Dictionary.has(key, value, v):
                    return True
        elif isinstance(data, list):
            for item in data:
                if Dictionary.has(key, value, item):
                    return True
        return False


    @classmethod
    def without(cls, data: Any, predicate: Callable[[Any, Any], bool]) -> Any:
        if isinstance(data, dict):
            return {
                k: Dictionary.without(v, predicate)
                for k, v in data.items()
                if not predicate(k, v)
            }
        elif isinstance(data, list):
            return [
                Dictionary.without(item, predicate)
                for item in data
                if not predicate(None, item)
            ]

        return data

    @classmethod
    def merge(cls, base: Any, override: Any) -> Any:
        result = {}
        for key in base.keys() | override.keys():
            if key in override and override[key] is not None:
                if isinstance(base.get(key), dict) and isinstance(override[key], dict):
                    result[key] = cls.merge(base[key], override[key])
                else:
                    result[key] = override[key]
            elif key in base:
                result[key] = base[key]
        return result
