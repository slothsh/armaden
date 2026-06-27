from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from armaden.framework.protocols.kernel import CoreApplicationInterface

_application: 'CoreApplicationInterface | None' = None


def set_application(application: 'CoreApplicationInterface') -> None:
    global _application
    _application = application


def get_application() -> 'CoreApplicationInterface':
    if _application is None:
        raise RuntimeError("No application registered. Did you bootstrap the application?")
    return _application
