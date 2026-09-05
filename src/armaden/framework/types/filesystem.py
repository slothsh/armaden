from collections.abc import Callable, Mapping

from armaden.framework.protocols.filesystem_protocol import FilesystemProtocol


type FilesystemConfiguration = Mapping[str, object]


type FilesystemConstructor = Callable[[FilesystemConfiguration], FilesystemProtocol]