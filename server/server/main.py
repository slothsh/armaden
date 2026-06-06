"""Main entry point for the Arma Reforger dedicated server Docker image.

This module simply delegates to :class:`server.supervisor.Server`.
For available environment variables see :mod:`server.supervisor`.
"""

from __future__ import annotations

import sys

from server.supervisor import Server


def main() -> int:
    return Server.from_env().run()


if __name__ == "__main__":
    sys.exit(main())
