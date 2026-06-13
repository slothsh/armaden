# Arma Server Tools

Server tools for running Arma Reforger


# Environment variables
~~~~~~~~~~~~~~~~~~~~~

General
    ``ARMA_INSTALL_DIR``      — Installation directory (default ``/arma``).
    ``ARMA_EXECUTABLE``       — Full path to the server binary
                                (default ``$ARMA_INSTALL_DIR/ArmaReforgerServer``).
    ``STEAMCMD_EXECUTABLE``   — Path to the steamcmd binary (default: auto-discover).
    ``ARMA_UPDATE_ON_START``  — Force a SteamCMD update before launching
                                (``1`` / ``true`` / ``yes``).

Paths
    ``ARMA_CONFIG``           — Path to the server JSON config file.
    ``ARMA_CONFIGS_DIR``      — Directory for stored configs
                                (default ``/arma/configs``).
    ``ARMA_PROFILE``          — Profile directory (default ``/arma/profile``).
    ``ARMA_LOGS_DIR``         — Log directory (default ``/arma/logs``).

Binding
    ``ARMA_BIND_ADDRESS``     — IP address to bind.
    ``ARMA_GAME_PORT``        — Game UDP port.
    ``ARMA_STEAM_PORT``       — Steam UDP query port.

A2S query
    ``ARMA_A2S_ADDRESS``      — A2S query bind address.
    ``ARMA_A2S_PORT``         — A2S query UDP port.

RCON
    ``ARMA_RCON_ADDRESS``     — RCON bind address.
    ``ARMA_RCON_PORT``        — RCON TCP port.
    ``ARMA_RCON_PASSWORD``    — RCON password.
    ``RCON_HOST``             — Host to connect to for RCON commands
                                (default ``127.0.0.1``).

Gameplay
    ``ARMA_SCENARIO``         — Scenario ID to host.
    ``ARMA_ADDONS``           — Comma-separated list of mod IDs.
    ``ARMA_LIMIT_FPS``        — Server FPS cap.
    ``ARMA_AUTO_RELOAD``      — Auto-restart on crash (default ``true``).
    ``ARMA_SERVER_ID``        — Unique server identifier.
    ``ARMA_REGION``           — Server browser region tag.
    ``ARMA_LOAD_SESSION_SAVE``— Path to a session save to load.
    ``ARMA_FORCE_SESSION_LOAD``— Force loading mismatched save (default ``false``).

Control API
    ``CONTROL_BIND``          — HTTP control bind address (default ``0.0.0.0``).
    ``CONTROL_PORT``          — HTTP control port (default ``8888``).
