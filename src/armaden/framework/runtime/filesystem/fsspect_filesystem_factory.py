from collections.abc import Callable, Mapping
from importlib import import_module
from typing import cast

from armaden.framework.protocols.fsspec_filesystem_protocol import (
    FsspecFilesystemProtocol,
)


def create_fsspec_filesystem(
    protocol: str,
    options: Mapping[str, object] | None = None,
) -> FsspecFilesystemProtocol:
    module = import_module('fsspec')
    factory = cast(Callable[..., object], getattr(module, 'filesystem'))
    parameters = dict(options or {})
    return cast(FsspecFilesystemProtocol, factory(protocol, **parameters))
