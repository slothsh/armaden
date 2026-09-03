from abc import ABC
from typing import get_args, get_origin

from ..utils.dictionary import Dictionary


def _resolve_config_type(cls: type) -> type:
    for base in getattr(cls, '__orig_bases__', []):
        if get_origin(base) is Configurable:
            args = get_args(base)
            if args:
                return args[0]
    raise TypeError(
        f'{cls.__name__} must be declared as Configurable[T] with a TypedDict type'
    )


class Configurable[T](ABC):
    config: T

    def __new__(cls, *args, **kwargs):
        _ = args
        raw_config = kwargs.pop('config', {})
        instance = super().__new__(cls)

        typed_dict_cls = _resolve_config_type(cls)
        defaults = getattr(cls, 'config', None) or {}
        merged = Dictionary.merge(defaults, raw_config)

        filtered = {
            k: v
            for k, v in merged.items()
            if k in typed_dict_cls.__annotations__
        }

        object.__setattr__(instance, 'config', typed_dict_cls(**filtered))
        return instance