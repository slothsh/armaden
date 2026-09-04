from typing import ClassVar

from armaden.framework.facades.exceptions import (
    MissingFacadeAccessorException,
    UnresolvedFacadeRootException,
)
from armaden.framework.facades.facade_meta import FacadeMeta
from armaden.framework.protocols.facade_protocol import FacadeProtocol
from armaden.framework.types.facade import FacadeAccessor, FacadeApplication


class Facade(metaclass=FacadeMeta):
    _cached: ClassVar[bool] = True
    _facade_application: ClassVar[FacadeApplication | None] = None
    _resolved_instances: ClassVar[dict[FacadeAccessor, object]] = {}


    @classmethod
    def clear_resolved_instance(
        cls,
        name: FacadeAccessor | None = None,
    ) -> None:
        key = name if name is not None else cls.get_facade_accessor()
        _ = cls._resolved_instances.pop(key, None)


    @classmethod
    def clear_resolved_instances(cls) -> None:
        cls._resolved_instances.clear()


    @classmethod
    def get_facade_accessor(cls) -> FacadeAccessor:
        raise MissingFacadeAccessorException(
            'Facade does not implement get_facade_accessor.'
        )


    @classmethod
    def get_facade_application(cls) -> FacadeApplication | None:
        return cls._facade_application


    @classmethod
    def get_facade_root(cls) -> object:
        return cls.resolve_facade_instance(cls.get_facade_accessor())


    @classmethod
    def resolve_facade_instance(cls, accessor: FacadeAccessor) -> object:
        if accessor in cls._resolved_instances:
            return cls._resolved_instances[accessor]
        application = cls._facade_application
        if application is None:
            raise UnresolvedFacadeRootException('A facade root has not been set.')
        instance = application.make(accessor)
        if cls._cached:
            cls._resolved_instances[accessor] = instance
        return instance


    @classmethod
    def set_facade_application(cls, application: FacadeApplication) -> None:
        Facade._facade_application = application


    @classmethod
    def swap(cls, instance: object) -> None:
        accessor = cls.get_facade_accessor()
        cls._resolved_instances[accessor] = instance
        application = cls._facade_application
        if application is not None:
            _ = application.instance(accessor, instance)


_facade_contract: type[FacadeProtocol] = Facade