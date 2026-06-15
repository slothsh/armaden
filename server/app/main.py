"""Main entry point for the Arma Reforger dedicated server Docker image."""

import logging
from app.application import Application

logger = logging.getLogger("app.main")


def main():
    return Application.main()


if __name__ == "__main__":
    Application.main()
