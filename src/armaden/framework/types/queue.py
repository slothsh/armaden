from collections.abc import Callable, Mapping

from armaden.framework.protocols.queue_driver_protocol import QueueDriverProtocol


type QueueConfiguration = Mapping[str, object]
type QueueDriverConstructor = Callable[..., QueueDriverProtocol]
