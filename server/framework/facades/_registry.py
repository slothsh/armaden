from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..protocols.kernel import KernelInterface

_kernel: 'KernelInterface | None' = None


def set_kernel(kernel: 'KernelInterface') -> None:
    global _kernel
    _kernel = kernel


def get_kernel() -> 'KernelInterface':
    if _kernel is None:
        raise RuntimeError("No kernel registered. Did you bootstrap the application?")
    return _kernel
