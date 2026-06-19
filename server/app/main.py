"""Main entry point for the Arma Reforger dedicated server Docker image."""

import logging
from framework.classes.default_application import DefaultApplication

logger = logging.getLogger("app.main")


def main():
    return DefaultApplication.main()


if __name__ == "__main__":
    DefaultApplication.main()
