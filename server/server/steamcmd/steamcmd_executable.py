from enum import StrEnum
import logging
from pathlib import Path
from typing import List

from returns.result import Success

from server.lib.interfaces import Executable
from server.lib.types import Result

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


    # -- Core Functions -------------------------------------------------------

    def login(self, username: str, password: str | None = None) -> SteamCmdExecutable:
        if password:
            self.push("login", username, password)
        return self


    def login_anonymous(self) -> SteamCmdExecutable:
        self.push("login_anonymous")
        # self.push("login", "anonymous")
        return self


    def force_install_dir(self, path: str | Path) -> SteamCmdExecutable:
        target = Path(path)
        target.mkdir(parents=True, exist_ok=True)
        self.push("force_install_dir", str(path))
        # self.push("force_install_dir", str(target.resolve()))
        return self


    def app_update( self, app_id: int, validate: bool = False) -> SteamCmdExecutable:
        self.push("app_update", str(app_id),  str(validate))
        # if beta is not None:
        #     self.push("-beta", beta)
        # if beta_password is not None:
        #     self.push("-betapassword", beta_password)
        # if validate:
        #     self.push("validate")
        return self


    def app_info_print(self, app_id: int) -> SteamCmdExecutable:
        self.push("app_info_print", app_id)
        return self


    def workshop_download_item(self, app_id: int, item_id: int) -> SteamCmdExecutable:
        self.push("workshop_download_item", app_id, item_id)
        return self


    def quit(self) -> SteamCmdExecutable:
        self.push("quit")
        return self


    def raw(self, command: str, *args: str | int) -> SteamCmdExecutable:
        self.push(command, *args)
        return self


    def script( self, script_path: str | Path) -> SteamCmdExecutable:
        self._commands = []
        self.push("runscript", str(Path(script_path).resolve()))
        return self


# -- Internal Types -----------------------------------------------------------

class ArmaReforgerExecutableError(StrEnum):
    EXECUTABLE_NOT_FOUND = "the steam executable could not be found in the host system"
