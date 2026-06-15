"""Main entry point for the Arma Reforger dedicated server Docker image.

This module simply delegates to :class:`server.supervisor.Server`.
For available environment variables see :mod:`server.supervisor`.
"""

import logging
from server.lib.types import Result
from server.application import EntryPoint

logger = logging.getLogger("server.main")


def main() -> Result[None]:
    return EntryPoint.main()


if __name__ == "__main__":
    EntryPoint.main()
