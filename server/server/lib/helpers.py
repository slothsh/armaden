from typing import Any
from collections.abc import Callable


class Dictionary:
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
