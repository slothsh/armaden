class LifecycleTag[S]:
    __slots__: tuple[str, ...] = ()


class PipelineTag[S, O]:
    __slots__: tuple[str, ...] = ()


class UnresolvedSentinelTag:
    __slots__: tuple[str, ...] = ()
