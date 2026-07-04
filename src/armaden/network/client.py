import asyncio
from .udp.async_datagram_transport import AsyncDatagramTransport
from .rcon.battle_eye.battle_eye_rcon_client import BattleEyeRconClient
import logging
import sys

async def entry():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s][%(name)s][%(threadName)s]: %(message)s",
        stream=sys.stdout,
    )

    client = BattleEyeRconClient(transport=AsyncDatagramTransport, port=19999, password='password', initialize_signal_handlers=True)
    await client.connect()


def main():
    asyncio.run(entry())


if __name__ == '__main__':
    asyncio.run(entry())
