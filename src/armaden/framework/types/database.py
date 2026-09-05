from collections.abc import Mapping


type DatabaseConfiguration = Mapping[str, object]
type DatabaseBindings = tuple[object, ...]
