from enum import StrEnum
import logging
from pathlib import Path
from typing import List

from returns.result import Success

from server.lib.interfaces import Executable
from server.lib.types import Result
from server.steamcmd.enums import SteamCmdExecutableFlag

logger = logging.getLogger(__name__)


class SteamCmdExecutable(Executable):
    def __init__(self) -> None:
        self._executable: Path | None = self.resolve_executable().value_or(None)
        self._params: List[str] = []


    @classmethod
    def resolve_executable(cls) -> Result[Path]:
        return Success(Path("/bin/echo"))

        # common_paths = [
        #     Path.home() / "Steam" / "steamcmd" / "steamcmd.sh",
        #     Path("/usr/games/steamcmd"),
        #     Path("/usr/local/bin/steamcmd"),
        #     Path("C:\\steamcmd\\steamcmd.exe"),
        # ]
        #
        # for candidate in common_paths:
        #     if candidate.exists():
        #         return Success(candidate.resolve())
        #
        # return Failure(
        #     Error(SteamCmdExecutableError.EXECUTABLE_NOT_FOUND)
        # )


    # -- steamcmd Server Flags ------------------------------------------------

    def login(self, username: str, password: str | None = None) -> SteamCmdExecutable:
        if password:
            self.push(SteamCmdExecutableFlag.LOGIN, username, password)
        return self


    def login_anonymous(self) -> SteamCmdExecutable:
        self.push(SteamCmdExecutableFlag.LOGIN_ANONYMOUS)
        # self.push(SteamCmdExecutableFlag.LOGIN, "anonymous")
        return self


    def force_install_dir(self, path: str | Path) -> SteamCmdExecutable:
        target = Path(path)
        target.mkdir(parents=True, exist_ok=True)
        self.push(SteamCmdExecutableFlag.FORCE_INSTALL_DIR, str(path))
        # self.push(SteamCmdExecutableFlag.FORCE_INSTALL_DIR, str(target.resolve()))
        return self


    def app_update( self, app_id: int, validate: bool = False) -> SteamCmdExecutable:
        self.push(SteamCmdExecutableFlag.APP_UPDATE, str(app_id), str(validate))
        return self


    def app_info_print(self, app_id: int) -> SteamCmdExecutable:
        self.push(SteamCmdExecutableFlag.APP_INFO_PRINT, app_id)
        return self


    def workshop_download_item(self, app_id: int, item_id: int) -> SteamCmdExecutable:
        self.push(SteamCmdExecutableFlag.WORKSHOP_DOWNLOAD_ITEM, app_id, item_id)
        return self


    def quit(self) -> SteamCmdExecutable:
        self.push(SteamCmdExecutableFlag.QUIT)
        return self


    def raw(self, command: str, *args: str | int) -> SteamCmdExecutable:
        self.push(command, *args)
        return self


    def script( self, script_path: str | Path) -> SteamCmdExecutable:
        self._commands = []
        self.push(SteamCmdExecutableFlag.RUNSCRIPT, str(Path(script_path).resolve()))
        return self


# -- Internal Types -----------------------------------------------------------

class SteamCmdExecutableError(StrEnum):
    EXECUTABLE_NOT_FOUND = "the steam executable could not be found in the host system"
