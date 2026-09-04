from typing import Protocol

from armaden.framework.types.facade import FacadeAccessor, FacadeApplication


class FacadeProtocol(Protocol):
    @classmethod
    def clear_resolved_instance(
        cls,
        name: FacadeAccessor | None = None,
    ) -> None: ...

    @classmethod
    def clear_resolved_instances(cls) -> None: ...

    @classmethod
    def get_facade_accessor(cls) -> FacadeAccessor: ...

    @classmethod
    def get_facade_application(cls) -> FacadeApplication | None: ...

    @classmethod
    def get_facade_root(cls) -> object: ...

    @classmethod
    def resolve_facade_instance(cls, accessor: FacadeAccessor) -> object: ...

    @classmethod
    def set_facade_application(cls, application: FacadeApplication) -> None: ...

    @classmethod
    def swap(cls, instance: object) -> None: ...