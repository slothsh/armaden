import asyncio
import logging
from datetime import datetime
from dataclasses import dataclass
from asyncio import AbstractEventLoop
from typing import Generator

from armaden.network.rcon.battle_eye.enums.login_status import LoginStatus
from armaden.network.rcon.battle_eye.packets.command_request_packet import CommandRequestPacket
from armaden.network.rcon.battle_eye.packets.command_response_packet import CommandResponsePacket
from armaden.network.rcon.battle_eye.packets.server_message_request_packet import ServerMessageRequestPacket
from armaden.network.rcon.battle_eye.packets.server_message_response_packet import ServerMessageResponsePacket
from armaden.network.rcon.battle_eye.packets.keep_alive_packet import KeepAlivePacket
from armaden.network.rcon.battle_eye.packets.login_request_packet import LoginRequestPacket
from armaden.network.rcon.battle_eye.packets.login_response_packet import LoginResponsePacket
from armaden.network.rcon.battle_eye.packets.unknown_packet import UnknownPacket

from .packets.packet import Packet
from armaden.network.udp import DatagramTransportFactory
from armaden.network.udp.async_datagram_transport import AsyncDatagramTransport

logger = logging.getLogger(__name__)


class BattleEyeRconServer:
    RECONNECT_TIMEOUT = 45

    def __init__(
        self,
        *,
        address: str = '0.0.0.0',
        port: int = 25575,
        password: str = '',
        event_loop: AbstractEventLoop | None = None,
        transport: DatagramTransportFactory = AsyncDatagramTransport,
    ) -> None:
        self._connected = False
        self._transport = transport(self, event_loop)
        self._address = address
        self._port = port
        self._password = password
        self._clients: dict[Client, ClientState] = {}
        self._request_queue: list[RequestMessage] = []
        self._response_queue: list[ResponseMessage] = []

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


    async def serve(self) -> None:
        while True:
            try:
                if not self._connected:
                    logger.info(f"Trying connection on {self._address}:{self._port}")
                    await self._try_connect()
                    logger.info(f"BattleEye RCON server listening on {self._address}:{self._port}")

                await self._dispatch_server_messages()
                await self._handle_requests()
                await self._handle_responses()
                await self._prune_clients()

                await asyncio.sleep(1)
            except Exception as exception:
                logger.error(exception)


    async def receive_datagram(self, data: bytes, address: str, port: int) -> None:
        logger.info(f"Received message from {address}:{port}")

        packet = Packet.try_any_from_datagram(
            data,
            [
                KeepAlivePacket,
                LoginRequestPacket,
                CommandRequestPacket,
                ServerMessageResponsePacket,
            ],
            UnknownPacket
        )

        self._request_queue.append(
            RequestMessage(
                client=Client(address=address, port=port),
                packet=packet,
                time_received=datetime.now()
            )
        )


    async def handle_new_connection(self, address: str, port: int) -> None:
        _ = address
        _ = port
        self._connected = True


    async def handle_lost_connection(self, exception: Exception | None) -> None:
        logger.warning(exception)
        self._connected = False


    async def handle_error(self, exception: Exception) -> None:
        logger.error(exception)


    async def _try_connect(self):
        await self._transport.connect_server(self.address, self.port)


    async def _handle_requests(self):
        while self._request_queue:
            message = self._request_queue.pop(0)
            match message.packet:
                case LoginRequestPacket():
                    self._authenticate_client(message.client, message.packet)
                case KeepAlivePacket():
                    self._refresh_client(message.client, message.time_received)
                case CommandRequestPacket():
                    await self._dispatch_client_command(message.client, message.packet)
                case ServerMessageResponsePacket():
                    logger.info("Received server message response from client %s, %s", message.client, message.packet)
                case UnknownPacket():
                    logger.warning('Unknown packet received from client %s', message.client)


    async def _handle_responses(self):
        while self._response_queue:
            message = self._response_queue.pop(0)
            await self._transport.send_data(
                message.packet.to_bytes(),
                address=(message.client.address, message.client.port)
            )


    def _authenticate_client(self, client: Client, packet: LoginRequestPacket) -> None:
        now = datetime.now()

        if self._password != packet.password:
            logger.info(f"Could not authenticate client %s with invalid password", client)
            message = ResponseMessage(
                client=client,
                packet=Packet.new(LoginResponsePacket, LoginStatus.DENIED)
            )
            self._response_queue.append(message)
            return

        if client not in self._clients:
            self._clients[client] = ClientState(time_authenticated=now, time_last_message=now)
        else:
            self._clients[client].time_authenticated=now
            self._clients[client].time_last_message=now

        message = ResponseMessage(
            client=client,
            packet=Packet.new(LoginResponsePacket, LoginStatus.AUTHENTICATED)
        )
        self._response_queue.append(message)

        logger.info('Successfully authenticated client %s', client)


    def _refresh_client(self, client: Client, time: datetime) -> None:
        if client not in self._clients:
            logger.warning('Unknown/unauthenticated client requesting refresh: %s', client)
            return


        logger.info('Refreshed client lease %s', client)
        self._clients[client].time_last_message=time


    async def _prune_clients(self) -> None:
        now = datetime.now()
        prune: list[Client] = []
        for client, state in self._clients.items():
            delta = abs(now - state.time_last_message).total_seconds()
            if delta > self.RECONNECT_TIMEOUT:
                prune.append(client)

        for client in prune:
            logger.info('Pruning client %s', client)
            del(self._clients[client])


    async def _dispatch_client_command(self, client: Client, packet: CommandRequestPacket) -> None:
        logger.info("Received command request %s from client %s", repr(packet), client)
        message = ResponseMessage(
            client=client,
            packet=Packet.new(CommandResponsePacket, packet.sequence, b"OK", (42, 0))
        )
        self._response_queue.append(message)


    async def _dispatch_server_messages(self) -> None:
        for client in self._clients.keys():
            message = ResponseMessage(
                client=client,
                packet=Packet.new(ServerMessageRequestPacket, 42, b"Hello, from Server!")
            )
            self._response_queue.append(message)


    def _new_sequence_generator(self) -> Generator[int]:
        i = 0
        while True:
            yield i
            i = (i + 1) % 255


# -- Internal Types -----------------------------------------------------------

@dataclass(frozen=True)
class Client:
    address: str
    port: int


@dataclass
class ClientState:
    time_authenticated: datetime
    time_last_message: datetime


@dataclass
class RequestMessage:
    client: Client
    packet: Packet
    time_received: datetime
    sequence: int | None = None


@dataclass
class ResponseMessage:
    client: Client
    packet: Packet
    sequence: int | None = None
