import asyncio
import base64
from .udp.async_datagram_transport import AsyncDatagramTransport
from .rcon.battle_eye.battle_eye_rcon_client import BattleEyeRconClient
import logging
from pathlib import Path
import shlex
import sys


async def _forward_stdin(client: BattleEyeRconClient) -> None:
    loop = asyncio.get_running_loop()
    stdin_closed = loop.create_future()
    stdin_fd = sys.stdin.fileno()

    def forward_line() -> None:
        line = sys.stdin.readline()
        if not line:
            if not stdin_closed.done():
                stdin_closed.set_result(None)
            return

        argv = shlex.split(line)
        if not argv:
            return

        try:
            argv = [
                base64.b64encode(Path(argument[1:]).read_bytes()).decode('ascii')
                if argument.startswith('@') else argument
                for argument in argv
            ]
        except OSError as exception:
            logging.error("Unable to read command input file: %s", exception)
            return

        response = client.send_command(argv[0], *argv[1:])
        response.add_done_callback(
            lambda future: None if future.cancelled() else future.exception()
        )

    loop.add_reader(stdin_fd, forward_line)
    try:
        await stdin_closed
    finally:
        loop.remove_reader(stdin_fd)


async def entry():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s][%(name)s][%(threadName)s]: %(message)s",
        stream=sys.stdout,
    )

    client = BattleEyeRconClient(transport=AsyncDatagramTransport, port=19999, password='password', initialize_signal_handlers=True)

    connect_task = asyncio.create_task(client.connect())
    stdin_task = asyncio.create_task(_forward_stdin(client))

    try:
        done, _ = await asyncio.wait({connect_task, stdin_task}, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            task.result()
    finally:
        await client.shutdown()
        stdin_task.cancel()
        connect_task.cancel()
        await asyncio.gather(stdin_task, connect_task, return_exceptions=True)
        await client._transport.close()


def main():
    asyncio.run(entry())


if __name__ == '__main__':
    asyncio.run(entry())
