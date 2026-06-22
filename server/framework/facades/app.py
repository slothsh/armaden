from typing import TYPE_CHECKING
from ._registry import get_kernel

if TYPE_CHECKING:
    from ..protocols.kernel import KernelInterface


def app() -> 'KernelInterface':
    return get_kernel()
