from asyncio import AbstractEventLoop
from typing import Callable

from .datagram_transport_interface import DatagramTransportInterface
from .wrapper_transport_interface import WrapperTransportInterface

type DatagramTransportFactory = Callable[[WrapperTransportInterface, AbstractEventLoop | None], DatagramTransportInterface
                                         ]
__all__ = [
    'DatagramTransportFactory'
]
