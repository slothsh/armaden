from framework.runtime.kernel import Kernel


def app() -> Kernel:
    return Kernel.instance()
