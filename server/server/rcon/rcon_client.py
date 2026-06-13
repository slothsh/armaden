"""Base BattlEye RCON wrapper around :mod:`berconpy`.

Provides connection management, automatic reconnection, and a simple
synchronous-style façade for the fully-async underlying library.

Typical usage::

    rcon = Rcon(host="127.0.0.1", port=2302, password="secret")
    await rcon.connect()
    response = await rcon.send("players")
    await rcon.disconnect()
"""

import asyncio
import contextlib
import logging
from typing import Any

import berconpy

logger = logging.getLogger("server.arma.rcon")


class RconClient:
    """BattlEye RCON client wrapper.

    Args:
        host: Server IP or hostname.
        port: RCON TCP port.
        password: RCON password.
    """

    def __init__(self, host: str, port: int, password: str) -> None:
        self.host = host
        self.port = port
        self.password = password
        self._client = berconpy.RCONClient()
        self._task: asyncio.Task[Any] | None = None
        self._lock = asyncio.Lock()
        self._setup_event_logging()

    def _setup_event_logging(self) -> None:
        """Register permanent listeners to log raw RCON traffic."""

        @self._client.dispatch.on_command
        async def _on_command(response: str) -> None:
            logger.debug("RCON on_command event: %r", response)

        @self._client.dispatch.on_message
        async def _on_message(message: str) -> None:
            logger.debug("RCON on_message event: %r", message)


    # -- connection ---------------------------------------------------

    async def connect(self) -> None:
        """Open the connection and authenticate.

        This starts the protocol task in the background so the client
        stays alive until :meth:`disconnect` is called.
        """
        async with self._lock:
            if self._client.is_running():
                logger.debug("RCON already connected")
                return

            logger.info("Connecting to RCON %s:%d", self.host, self.port)
            try:
                self._task = self._client.protocol.run(
                    self.host, self.port, self.password
                )
                await self._client.protocol.wait_for_login()
            except berconpy.LoginFailure as exc:
                await self._cancel_task()
                raise RconClientConnectionError(f"RCON login failed: {exc}") from exc
            except OSError as exc:
                await self._cancel_task()
                raise RconClientConnectionError(f"RCON connection error: {exc}") from exc
            except Exception:
                await self._cancel_task()
                raise

            logger.info("RCON connected and authenticated")

    async def _cancel_task(self) -> None:
        """Cancel and drain the background protocol task."""
        if self._task is None:
            return
        if not self._task.done():
            self._task.cancel()
        with contextlib.suppress(asyncio.CancelledError, Exception):
            await self._task
        self._task = None

    async def disconnect(self) -> None:
        """Close the connection gracefully."""
        async with self._lock:
            if not self._client.is_running():
                return
            logger.info("Disconnecting from RCON")
            self._client.close()
            if self._task is not None:
                try:
                    await asyncio.wait_for(self._task, timeout=5.0)
                except asyncio.TimeoutError:
                    self._task.cancel()
                    with contextlib.suppress(asyncio.CancelledError):
                        await self._task
                self._task = None

    # -- state --------------------------------------------------------

    @property
    def is_connected(self) -> bool:
        return self._client.is_connected()

    @property
    def is_logged_in(self) -> bool | None:
        return self._client.is_logged_in()

    # -- commands -----------------------------------------------------

    async def send(self, command: str) -> str:
        """Send a raw command and return the server's response.

        Args:
            command: The command string (without any leading prefix).

        Returns:
            The raw response text from the server.

        Raises:
            RconConnectionError: If not connected.
            RconError: If the command fails or times out.
        """
        if not self._client.is_running():
            raise RconConnectionError("RCON client is not connected")

        logger.debug("RCON send: %r", command)
        try:
            response = await self._client.send_command(command)
        except berconpy.RCONCommandError as exc:
            raise RconClientError(f"Command failed: {exc}") from exc
        except RuntimeError as exc:
            raise RconClientConnectionError(f"RCON not ready: {exc}") from exc
        logger.debug("RCON response: %r", response)
        return response

    async def send_with_fallback(
        self,
        command: str,
        *,
        fallback_delay: float = 1.5,
    ) -> str:
        """Send a command and fall back to server messages if response is empty.

        Some BattlEye servers (including Arma Reforger) send an empty
        command acknowledgment and broadcast the actual payload as a
        server message.  This method captures any messages that arrive
        shortly after the command and returns them when the command
        response is empty.

        Args:
            command: The command to send.
            fallback_delay: Seconds to wait for message fallback.

        Returns:
            The command response, or any captured messages if the
            response was empty.
        """
        messages: list[str] = []

        async def _collect(message: str) -> None:
            messages.append(message)

        self._client.add_listener("on_message", _collect)
        try:
            response = await self.send(command)
            if response.strip():
                return response
            await asyncio.sleep(fallback_delay)
            if messages:
                return "\n".join(messages)
            return response
        finally:
            self._client.remove_listener("on_message", _collect)


class RconClientError(Exception):
    """Base exception for RCON errors."""

    pass


class RconClientConnectionError(RconClientError):
    """Raised when the RCON connection cannot be established."""

    pass

