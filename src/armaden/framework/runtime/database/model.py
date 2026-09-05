from __future__ import annotations

from collections.abc import Mapping
from typing import ClassVar, override

# pyright: reportMissingTypeStubs=false
from masoniteorm.models import Model as MasoniteModel

from armaden.framework.protocols.database_resolver_protocol import DatabaseResolverProtocol


class Model(MasoniteModel):
    _database_resolver: ClassVar[DatabaseResolverProtocol | None] = None

    @classmethod
    def set_database_resolver(cls, resolver: DatabaseResolverProtocol) -> None:
        Model._database_resolver = resolver


    @override
    def get_connection_details(self) -> Mapping[str, object]:
        resolver = Model._database_resolver
        if resolver is None:
            raise RuntimeError('database resolver is not registered')
        return resolver.get_connection_details()
