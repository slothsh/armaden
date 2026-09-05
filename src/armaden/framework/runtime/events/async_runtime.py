import asyncio
import threading
from collections.abc import Coroutine


def run_coroutine_sync(coroutine: Coroutine[object, object, object]) -> None:
    try:
        _ = asyncio.get_running_loop()
    except RuntimeError:
        _ = asyncio.run(coroutine)
        return

    error: list[BaseException] = []

    def execute() -> None:
        try:
            _ = asyncio.run(coroutine)
        except BaseException as exception:
            error.append(exception)

    thread = threading.Thread(target=execute)
    thread.start()
    thread.join()
    if error:
        raise error[0]
