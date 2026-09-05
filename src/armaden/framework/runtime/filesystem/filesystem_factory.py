from armaden.framework.protocols.filesystem_protocol import FilesystemProtocol
from armaden.framework.runtime.filesystem.exceptions.filesystem_factory_error import (
    FilesystemFactoryError,
)
from armaden.framework.runtime.filesystem.local_filesystem import LocalFilesystem
from armaden.framework.runtime.filesystem.s3_filesystem import S3Filesystem
from armaden.framework.types.filesystem import (
    FilesystemConfiguration,
    FilesystemConstructor,
)


DRIVER_MAP: dict[str, FilesystemConstructor] = {
    'local': LocalFilesystem,
    's3': S3Filesystem,
}


def create_filesystem(config: FilesystemConfiguration) -> FilesystemProtocol:
    driver = config.get('driver')
    if not isinstance(driver, str) or not driver:
        raise ValueError(FilesystemFactoryError.MISSING_DRIVER.value)
    filesystem_type = DRIVER_MAP.get(driver)
    if filesystem_type is None:
        supported = ', '.join(sorted(DRIVER_MAP))
        raise ValueError(f'{FilesystemFactoryError.UNSUPPORTED_DRIVER.value}: {driver}. Supported drivers: {supported}')
    return filesystem_type(config)
