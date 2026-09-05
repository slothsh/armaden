from __future__ import annotations

from abc import ABC
from collections.abc import Callable, Mapping
from typing import Self, cast, get_args, get_origin

from armaden.framework.api.support import Dictionary
from armaden.framework.protocols.configurable_protocol import ConfigurableProtocol


class Configurable[T](ConfigurableProtocol[T], ABC):
    config: T

    @classmethod
    def _resolve_config_type(cls) -> type[object]:
        for base in getattr(cls, '__orig_bases__', ()):
            if get_origin(base) is Configurable:
                args = get_args(base)
                if args and isinstance(args[0], type):
                    return args[0]
        raise TypeError(
            f'{cls.__name__} must be declared as Configurable[T] with a TypedDict type'
        )


    def __new__(
        cls,
        *args: object,
        config: T | None = None,
        **kwargs: object,
    ) -> Self:
        _ = args
        _ = kwargs
        raw_config: object = config if config is not None else {}
        instance = super().__new__(cls)

        typed_dict_cls = cls._resolve_config_type()
        empty_mapping: Mapping[str, object] = {}
        defaults = getattr(cls, 'config', empty_mapping)
        default_mapping = (
            cast(Mapping[str, object], defaults)
            if isinstance(defaults, Mapping)
            else empty_mapping
        )
        raw_mapping = (
            cast(Mapping[str, object], raw_config)
            if isinstance(raw_config, Mapping)
            else empty_mapping
        )
        merged: Mapping[str, object] = Dictionary.merge(default_mapping, raw_mapping)
        annotations = getattr(typed_dict_cls, '__annotations__', empty_mapping)
        annotation_mapping = cast(Mapping[str, object], annotations)
        filtered: dict[str, object] = {
            key: value
            for key, value in merged.items()
            if key in annotation_mapping
        }
        config_factory = cast(Callable[..., object], typed_dict_cls)
        object.__setattr__(instance, 'config', cast(T, config_factory(**filtered)))
        return instance


__all__ = [
    'Configurable',
]
