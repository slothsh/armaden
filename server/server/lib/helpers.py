from typing import Any, Dict


class Dictionary:
    @classmethod
    def remove_none(cls, data: Dict[Any, Any]) -> Dict[Any, Any]:
        if isinstance(data, dict):
            return {
                k: Dictionary.remove_none(v) 
                for k, v in data.items() 
                if v is not None
            }
        elif isinstance(data, list):
            return [
                Dictionary.remove_none(item) 
                for item in data 
                if item is not None
            ]

        return data
