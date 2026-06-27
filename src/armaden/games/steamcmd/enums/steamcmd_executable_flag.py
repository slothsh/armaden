from enum import StrEnum

class SteamCmdExecutableFlag(StrEnum):
    """SteamCMD CLI command flags (prefixed with ``+``)."""

    LOGIN = "+login"
    FORCE_INSTALL_DIR = "+force_install_dir"
    APP_UPDATE = "+app_update"
    APP_INFO_PRINT = "+app_info_print"
    WORKSHOP_DOWNLOAD_ITEM = "+workshop_download_item"
    QUIT = "+quit"
    RUNSCRIPT = "+runscript"
