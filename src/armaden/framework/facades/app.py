from typing import TYPE_CHECKING
from ._registry import get_application

if TYPE_CHECKING:
    from armaden.framework.protocols.kernel import CoreApplicationInterface


def app() -> 'CoreApplicationInterface':
    return get_application()
