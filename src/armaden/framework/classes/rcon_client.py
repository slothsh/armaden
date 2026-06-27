"""Base BattlEye RCON client abstract class."""

from abc import ABC, abstractmethod


class RconClient(ABC):
    """BattlEye RCON client abstract base class."""

    @abstractmethod
    async def connect(self) -> None:
        """Open the connection and authenticate."""

    @abstractmethod
    async def disconnect(self) -> None:
        """Close the connection gracefully."""

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        ...

    @property
    @abstractmethod
    def is_logged_in(self) -> bool | None:
        ...

    @abstractmethod
    async def send(self, command: str) -> str:
        """Send a raw command and return the server's response."""

    @abstractmethod
    async def send_with_fallback(
        self,
        command: str,
        *,
        fallback_delay: float = 1.5,
    ) -> str:
        """Send a command and fall back to server messages if response is empty."""


class RconClientError(Exception):
    """Base exception for RCON errors."""
    pass


class RconClientConnectionError(RconClientError):
    """Raised when the RCON connection cannot be established."""
    pass
