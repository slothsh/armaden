from __future__ import annotations

from typing import TYPE_CHECKING

from .local_filesystem import LocalFilesystem
from .s3_filesystem import S3Filesystem

if TYPE_CHECKING:
    from armaden.framework.protocols.filesystem import Filesystem


DRIVER_MAP = {
    'local': LocalFilesystem,
    's3': S3Filesystem,
}


def create_filesystem(config: dict) -> 'Filesystem':
    driver_name = config.get('driver')
    if not driver_name:
        raise ValueError("Filesystem disk config is missing a 'driver' key")

    driver_class = DRIVER_MAP.get(driver_name)
    if driver_class is None:
        supported = ', '.join(sorted(DRIVER_MAP))
        raise ValueError(
            f"Unsupported filesystem driver '{driver_name}'. "
            f"Supported drivers: {supported}"
        )

    return driver_class(config)


__all__ = [
    'LocalFilesystem',
    'S3Filesystem',
    'DRIVER_MAP',
    'create_filesystem',
]
