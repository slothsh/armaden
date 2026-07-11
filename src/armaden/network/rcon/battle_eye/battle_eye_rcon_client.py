import asyncio
import logging
import errno
import time
from datetime import datetime
from dataclasses import dataclass, field
from asyncio import AbstractEventLoop
import signal
from typing import Any, Generator

from armaden.network.rcon.battle_eye.packets.command_request_packet import CommandRequestPacket
from armaden.network.rcon.battle_eye.packets.command_response_packet import CommandHeader, CommandResponsePacket
from armaden.network.rcon.battle_eye.packets.keep_alive_packet import KeepAlivePacket
from armaden.network.rcon.battle_eye.packets.login_request_packet import LoginRequestPacket
from armaden.network.rcon.battle_eye.packets.login_response_packet import LoginResponsePacket
from armaden.network.rcon.battle_eye.packets.server_message_request_packet import ServerMessageRequestPacket
from armaden.network.rcon.battle_eye.packets.server_message_response_packet import ServerMessageResponsePacket
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
    MULTI_PACKET_TIMEOUT = 10.0

    def __init__(
        self,
        *,
        address: str = '127.0.0.1',
        port: int = 25575,
        password: str = '',
        event_loop: AbstractEventLoop | None = None,
        transport: DatagramTransportFactory = AsyncDatagramTransport,
        initialize_signal_handlers: bool = False
    ) -> None:
        self._transport = transport(self, event_loop)
        self._shutdown_event = asyncio.Event()
        self._connected = False
        self._client_status = ClientStatus(authenticated=False, time_last_attempt=datetime.fromtimestamp(0))
        self._last_send_time: datetime = datetime.fromtimestamp(0)
        self._address = address
        self._port = port
        self._password = password
        self._request_queue: list[Message] = []
        self._response_queue: list[Message] = []
        self._pending_commands: dict[int, _PendingCommand] = {}

        self._sequence_generator = self._new_sequence_generator()
        def generate_sequence() -> int:
            return next(self._sequence_generator)
        self._generate_sequence = generate_sequence

        if initialize_signal_handlers:
            self._initialize_signal_handlers()


    @property
    def address(self) -> str:
        return self._address


    @property
    def port(self) -> int:
        return self._port


    def send_command(self, command: str, *args: str) -> asyncio.Future[CommandResponse]:
        argv = [command] + list(args)
        sequence = self._generate_sequence()
        packet = Packet.new(CommandRequestPacket, sequence, argv)
        loop = asyncio.get_running_loop()
        future: asyncio.Future[CommandResponse] = loop.create_future()
        self._pending_commands[sequence] = _PendingCommand(
            command=' '.join(argv),
            future=future,
        )
        self._request_queue.append(Message(
            sequence=sequence,
            packet_request=packet,
        ))
        return future


    async def on_server_message(self, message: ServerMessage) -> None:
        _ = message
        pass


    async def on_command_response(self, response: CommandResponse) -> None:
        _ = response
        pass


    async def on_connected(self) -> None:
        pass


    async def on_disconnected(self) -> None:
        pass


    async def connect(self) -> None:
        while not self._shutdown_event.is_set():
            try:
                if not self._connected:
                    await self._try_connect()

                if self._client_status.authenticated:
                    await self._keep_alive()
                else:
                    await self._try_login()

                await self._handle_responses()
                await self._handle_requests()
                await self._cleanup_pending_commands()

                await asyncio.wait_for(self._shutdown_event.wait(), timeout=1.0)
            except asyncio.TimeoutError:
                pass
            except TransportNotConnectedException as exception:
                logger.warning(exception)
                await self._try_connect()
            except Exception as exception:
                logger.error(exception)


    async def shutdown(self) -> None:
        self._shutdown_event.set()


    def _initialize_signal_handlers(self) -> None:
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGQUIT):
            signal.signal(sig, self._handle_os_signal)


    def _handle_os_signal(self, signum: int, frame: Any) -> None:
        _ = signum
        _ = frame
        self._shutdown_event.set()


    async def receive_datagram(self, data: bytes, address: str, port: int) -> None:
        _ = address
        _ = port

        packet = Packet.try_any_from_datagram(
            data,
            [
                LoginResponsePacket,
                CommandResponsePacket,
                ServerMessageRequestPacket,
            ],
            UnknownPacket
        )

        self._handle_packet(packet, datetime.now())


    async def handle_new_connection(self, address: str, port: int) -> None:
        _ = address
        _ = port
        self._connected = True


    async def handle_lost_connection(self, exception: Exception | None) -> None:
        logger.warning(exception)
        self._connected = False
        self._client_status.authenticated = False
        self._cancel_pending_commands(exception or ConnectionError("Transport disconnected"))
        await self.on_disconnected()

    def _cancel_pending_commands(self, exception: Exception) -> None:
        for seq, pending in list(self._pending_commands.items()):
            if not pending.future.done():
                pending.future.set_exception(exception)
        self._pending_commands.clear()


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


    def _handle_packet(self, packet: Packet, time_received: datetime) -> None:
        match packet:
            case ServerMessageRequestPacket():
                self._handle_server_message(packet, time_received)
            case CommandResponsePacket():
                self._handle_command_response(packet)
            case LoginResponsePacket():
                self._response_queue.append(Message(
                    packet_response=packet,
                    time_response=time_received,
                ))
            case _:
                self._response_queue.append(Message(
                    packet_response=packet,
                    time_response=time_received,
                ))


    def _handle_server_message(self, packet: ServerMessageRequestPacket, time_received: datetime) -> None:
        ack_packet = Packet.new(ServerMessageResponsePacket, packet.sequence)
        self._response_queue.append(Message(
            sequence=packet.sequence,
            packet_request=packet,
            time_request=time_received,
            server_message=ServerMessage(
                sequence=packet.sequence,
                message=packet.message_data.decode('ascii'),
            ),
        ))
        self._request_queue.append(Message(
            sequence=packet.sequence,
            packet_request=ack_packet,
        ))


    def _handle_command_response(self, packet: CommandResponsePacket) -> None:
        pending = self._pending_commands.get(packet.request_sequence)

        if (header := packet.response_header) is not None:
            self._handle_multi_packet_response(header, packet, pending)
            return

        if pending is None:
            return

        response_data = packet.response_data.decode('ascii') if packet.response_data else None
        response = CommandResponse(
            sequence=packet.request_sequence,
            command=pending.command,
            response=response_data,
        )
        if not pending.future.done():
            pending.future.set_result(response)
        del self._pending_commands[packet.request_sequence]

        self._response_queue.append(Message(
            sequence=packet.request_sequence,
            command_response=response,
        ))


    def _handle_multi_packet_response(
        self, header: CommandHeader, packet: CommandResponsePacket, pending: _PendingCommand | None
    ) -> None:
        if pending is None:
            logger.warning(
                "Received multi-packet response for unknown sequence %d (packet %d/%d), ignoring",
                packet.request_sequence, header.index + 1, header.total_packets,
            )
            return

        pending.total_packets = header.total_packets
        pending.partials[header.index] = packet.response_data or b''

        if len(pending.partials) == header.total_packets:
            full_data = b''.join(
                pending.partials[i] for i in range(header.total_packets)
            )
            response = CommandResponse(
                sequence=packet.request_sequence,
                command=pending.command,
                response=full_data.decode('ascii') if full_data else None,
            )
            if not pending.future.done():
                pending.future.set_result(response)
            del self._pending_commands[packet.request_sequence]

            self._response_queue.append(Message(
                sequence=packet.request_sequence,
                command_response=response,
            ))


    async def _cleanup_pending_commands(self) -> None:
        now = time.monotonic()
        timed_out: list[int] = []
        for seq, pending in self._pending_commands.items():
            if pending.total_packets is not None and (now - pending.created_at) > self.MULTI_PACKET_TIMEOUT:
                timed_out.append(seq)

        for seq in timed_out:
            pending = self._pending_commands.pop(seq)
            error_message = f"Multi-packet response timed out after {self.MULTI_PACKET_TIMEOUT:.0f}s"
            response = CommandResponse(
                sequence=seq,
                command=pending.command,
                response=None,
                error=error_message,
            )
            if not pending.future.done():
                pending.future.set_exception(TimeoutError(error_message))
            self._response_queue.append(Message(
                sequence=seq,
                command_response=response,
            ))


    async def _handle_requests(self):
        while self._request_queue:
            message = self._request_queue.pop(0)
            if not message.packet_request:
                logger.warning("Cannot send message with empty request packet %s", message)
                continue

            last_send_time = datetime.now()
            await self._transport.send_data(message.packet_request.to_bytes())
            self._last_send_time = last_send_time


    async def _handle_responses(self):
        while self._response_queue:
            message = self._response_queue.pop(0)

            if message.server_message is not None:
                await self.on_server_message(message.server_message)
                continue

            if message.command_response is not None:
                await self.on_command_response(message.command_response)
                continue

            if message.login_connected:
                await self.on_connected()
                continue

            match message.packet_response:
                case LoginResponsePacket():
                    self._handle_login_response(message.packet_response)
                case UnknownPacket():
                    logger.warning('Unknown response packet received %s', message)
                case None:
                    logger.warning("Cannot handle response message with None type packet %s", message)
                case _:
                    logger.warning('Unhandled response packet %s', message.packet_response)


    def _handle_login_response(self, packet: LoginResponsePacket) -> None:
        if packet.authenticated:
            logger.info(f"Successfully authenticated with remote console {self._address}:{self._port}")
            self._client_status.authenticated = True
            self._response_queue.append(Message(login_connected=True))
        else:
            logger.info(f"Authentication with remote console {self._address}:{self._port} failed")
            self._client_status.authenticated = False


    def _handle_transport_error(self, exception: Exception):
        if isinstance(exception, OSError):
            if exception.errno == errno.ECONNREFUSED:
                logger.warning(exception)
                self._client_status.authenticated = False
            else:
                logger.error(exception)
        else:
            logger.error(f"An unexpected error occurred: {type(exception).__name__}: {exception!r}")


    def _new_sequence_generator(self) -> Generator[int]:
        i = 0
        while True:
            yield i
            i = (i + 1) % 255


# -- Public Types -------------------------------------------------------------

@dataclass
class CommandResponse:
    sequence: int
    command: str
    response: str | None
    error: str | None = None


@dataclass
class ServerMessage:
    sequence: int
    message: str


# -- Internal Types -----------------------------------------------------------

@dataclass
class Message:
    sequence: int | None = None
    packet_request: Packet | None = None
    time_request: datetime | None = None
    packet_response: Packet | None = None
    time_response: datetime | None = None
    server_message: ServerMessage | None = None
    command_response: CommandResponse | None = None
    login_connected: bool = False


@dataclass
class _PendingCommand:
    command: str
    future: asyncio.Future[CommandResponse]
    total_packets: int | None = None
    partials: dict[int, bytes] = field(default_factory=dict)
    created_at: float = field(default_factory=time.monotonic)


@dataclass
class ClientStatus:
    authenticated: bool
    time_last_attempt: datetime
