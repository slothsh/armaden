import asyncio
import logging
import errno
from datetime import datetime
from dataclasses import dataclass
from asyncio import AbstractEventLoop
from typing import Generator

from armaden.network.rcon.battle_eye.packets.keep_alive_packet import KeepAlivePacket
from armaden.network.rcon.battle_eye.packets.login_request_packet import LoginRequestPacket
from armaden.network.rcon.battle_eye.packets.login_response_packet import LoginResponsePacket
from armaden.network.rcon.battle_eye.packets.unknown_packet import UnknownPacket
from armaden.network.udp.exceptions import TransportNotConnectedException

from .packets.packet import Packet
from armaden.network.udp import DatagramTransportFactory
from armaden.network.udp.async_datagram_transport import AsyncDatagramTransport

logger = logging.getLogger(__name__)


class BattleEyeRconClient:
    RECONNECT_TIMEOUT = 45
    KEEP_ALIVE_TIMEOUT = 30
    LOGIN_TIMEOUT = 5

    def __init__(
        self,
        *,
        address: str = '127.0.0.1',
        port: int = 25575,
        password: str = '',
        event_loop: AbstractEventLoop | None = None,
        transport: DatagramTransportFactory = AsyncDatagramTransport,
    ) -> None:
        self._transport = transport(self, event_loop)
        self._connected = False
        self._client_status = ClientStatus(authenticated=False, time_last_attempt=datetime.fromtimestamp(0))
        self._last_send_time: datetime = datetime.fromtimestamp(0)
        self._address = address
        self._port = port
        self._password = password
        self._request_queue: list[Message] = []
        self._response_queue: list[Message] = []

        self._sequence_generator = self._new_sequence_generator()
        def generate_sequence() -> int:
            return next(self._sequence_generator)
        self._generate_sequence = generate_sequence


    @property
    def address(self) -> str:
        return self._address


    @property
    def port(self) -> int:
        return self._port


    async def connect(self) -> None:
        while True:
            try:
                if not self._connected:
                    await self._try_connect()

                if self._client_status.authenticated:
                    await self._keep_alive()
                else:
                    await self._try_login()

                await self._handle_responses()
                await self._handle_requests()

                await asyncio.sleep(1)
            except TransportNotConnectedException as exception:
                logger.warning(exception)
                await self._try_connect()

            except Exception as exception:
                logger.error(exception)


    async def receive_datagram(self, data: bytes, address: str, port: int) -> None:
        packet = Packet.try_any_from_datagram(
            data,
            [
                LoginResponsePacket,
            ],
            UnknownPacket
        )

        self._response_queue.append(Message(
            packet_response=packet,
            time_response=datetime.now()
        ))


    async def handle_new_connection(self, address: str, port: int) -> None:
        _ = address
        _ = port
        self._connected = True


    async def handle_lost_connection(self, exception: Exception | None) -> None:
        logger.warning(exception)
        self._connected = False
        self._client_status.authenticated = False


    async def handle_error(self, exception: Exception) -> None:
        self._handle_transport_error(exception)


    async def _try_connect(self):
        await self._transport.connect_client(self.address, self.port)


    async def _keep_alive(self) -> None:
        if self._request_queue:
            return

        delta = abs(datetime.now() - self._last_send_time).total_seconds()
        if self.KEEP_ALIVE_TIMEOUT < delta and delta < self.RECONNECT_TIMEOUT:
            sequence = self._generate_sequence()
            packet = Packet.new(KeepAlivePacket, sequence=sequence)
            message = Message(packet_request=packet)
            self._request_queue.append(message)
            return


    async def _try_login(self):
        now = datetime.now()
        delta = abs(now - self._client_status.time_last_attempt).total_seconds()
        if delta > self.LOGIN_TIMEOUT:
            packet = Packet.new(LoginRequestPacket, self._password)
            message = Message(packet_request=packet)
            self._client_status.time_last_attempt = now
            self._request_queue.append(message)


    async def _handle_requests(self):
        while self._request_queue:
            message = self._request_queue.pop(0)
            if not message.packet_request:
                logger.warning("Cannot sent message with empty request packet %s", message)
                continue

            last_send_time = datetime.now()
            await self._transport.send_data(message.packet_request.to_bytes())
            self._last_send_time = last_send_time


    async def _handle_responses(self):
        while self._response_queue:
            message = self._response_queue.pop(0)
            match message.packet_response:
                case LoginResponsePacket():
                    self._authenticate(message.packet_response)
                case UnknownPacket():
                    logger.warning('Unknown response packet received %s', message)
                case None:
                    logger.warning("Cannot handle response message with None type packet %s", message)


    def _handle_transport_error(self, exception: Exception):
        if isinstance(exception, OSError):
            if exception.errno == errno.ECONNREFUSED:
                logger.warning(exception)
                self._client_status.authenticated = False
            else:
                logger.error(exception)
        else:
            logger.error(f"An unexpected error occurred: {type(exception).__name__}: {exception!r}")


    def _authenticate(self, packet: LoginResponsePacket):
        if packet.authenticated:
            logger.info(f"Successfully authenticated with remote console {self._address}:{self._port}")
            self._client_status.authenticated = True
        else:
            logger.info(f"Authentication with remote console {self._address}:{self._port} failed")
            self._client_status.authenticated = False


    def _new_sequence_generator(self) -> Generator[int]:
        i = 0
        while True:
            yield i
            i = (i + 1) % 255


# -- Internal Types -----------------------------------------------------------

@dataclass
class Message:
    sequence: int | None = None
    packet_request: Packet | None = None
    time_request: datetime | None = None
    packet_response: Packet | None = None
    time_response: datetime | None = None

@dataclass
class ClientStatus:
    authenticated: bool
    time_last_attempt: datetime
