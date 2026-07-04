import asyncio
from asyncio import AbstractEventLoop, DatagramProtocol
from asyncio.transports import DatagramTransport

from .exceptions import TransportNotConnectedException
from .wrapper_transport_interface import WrapperTransportInterface
from typing import Any


class AsyncDatagramTransport(DatagramProtocol):
    __slots__ = ('_wrapper', '_event_loop', '_transport')

    def __init__(self, wrapper: WrapperTransportInterface, event_loop: AbstractEventLoop | None = None):
        self._wrapper = wrapper
        self._event_loop = event_loop if event_loop else asyncio.get_running_loop()
        self._transport: DatagramTransport | None = None


    async def connect_client(self, address: str, port: int) -> None:
        _ = await self._event_loop.create_datagram_endpoint(
            lambda: self,
            remote_addr=(address, port),
        )


    async def connect_server(self, address: str, port: int) -> None:
        _ = await self._event_loop.create_datagram_endpoint(
            lambda: self,
            local_addr=(address, port),
        )


    async def close(self) -> None:
        if self._transport:
            self._transport.close()
        self._transport = None


    async def send_data(
        self,
        data: bytes,
        *,
        address: tuple[str, int] | None = None,
    ) -> None:
        if not self._transport:
            raise TransportNotConnectedException(f"The {self.__class__} is not connected")

        self._transport.sendto(data, address)


    def datagram_received(self, data: bytes, addr: tuple[str | Any, int]) -> None:
        _ = asyncio.create_task(self._wrapper.receive_datagram(data, addr[0], addr[1]))


    def error_received(self, exc: Exception) -> None:
        _ = asyncio.create_task(self._wrapper.handle_error(exc))


    def connection_made(self, transport: DatagramTransport):
        self._transport = transport
        address, port = self._transport.get_extra_info('sockname')
        _ = asyncio.create_task(self._wrapper.handle_new_connection(address, port))


    def connection_lost(self, exc: Exception | None) -> None:
        self._transport = None
        _ = asyncio.create_task(self._wrapper.handle_lost_connection(exc))
