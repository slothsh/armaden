import platform as host_platform
from collections.abc import Mapping
from enum import StrEnum

from returns.result import Failure, Success

from armaden.framework.api.error import Error
from armaden.framework.types.result import Result
from armaden.games.minecraft.java.dto import TemurinPlatformData

_ARCHITECTURE_NAMES: Mapping[str, str] = {
    'aarch64': 'aarch64',
    'aarch64_be': 'aarch64',
    'amd64': 'x64',
    'arm64': 'aarch64',
    'armv7l': 'arm',
    'armv8l': 'arm',
    'ppc64le': 'ppc64le',
    'riscv64': 'riscv64',
    's390x': 's390x',
    'x86_64': 'x64',
}

_OS_NAMES: Mapping[str, str] = {
    'AIX': 'aix',
    'Darwin': 'mac',
    'Linux': 'linux',
    'SunOS': 'solaris',
    'Windows': 'windows',
}


def resolve_current_platform() -> Result[TemurinPlatformData]:
    os_name = _OS_NAMES.get(host_platform.system())
    architecture = _ARCHITECTURE_NAMES.get(host_platform.machine())

    if os_name is None:
        return Failure(
            Error(
                TemurinPlatformError.UNSUPPORTED_OS,
                details={
                    'system': host_platform.system(),
                    'supported': sorted(_OS_NAMES.values()),
                },
            )
        )

    if architecture is None:
        return Failure(
            Error(
                TemurinPlatformError.UNSUPPORTED_ARCHITECTURE,
                details={
                    'machine': host_platform.machine(),
                    'supported': sorted(_ARCHITECTURE_NAMES.values()),
                },
            )
        )

    return Success(TemurinPlatformData(architecture=architecture, os=os_name))


# --- Internal Types ----------------------------------------------------------

class TemurinPlatformError(StrEnum):
    UNSUPPORTED_ARCHITECTURE = 'the current cpu architecture has no temurin artifact'
    UNSUPPORTED_OS = 'the current operating system has no temurin artifact'
