"""Arma Reforger dedicated server wrapper.

Provides a typed, fluent interface for driving the Arma Reforger server
executable with all documented launch parameters.

Reference:
    https://community.bistudio.com/wiki/Arma_Reforger:Server_Quick_Start_Guide
"""

from enum import StrEnum

import logging
from pathlib import Path

from returns.pipeline import is_successful
from returns.result import Failure, Success
from armaden.framework.classes.executable import Executable
from armaden.framework.protocols.task_runtime import TaskRuntimeInterface
from armaden.framework.utils.types import Result
from armaden.framework.utils.dictionary import Dictionary
from armaden.framework.errors import Error
from armaden.games.steamcmd.steamcmd_executable import SteamCmdExecutable
from .enums import ArmaReforgerExecutableFlag
from .arma_reforger_executable_config import Config, DEFAULT_CONFIG

logger = logging.getLogger('games.arma_reforger.executable')


class ArmaReforgerServerExecutable(Executable):
    STEAM_APP_ID: int = 1874900
    STEAM_APP_ID_CLIENT: int = 1874880

    def __init__(self, config: Config | None = None) -> None:
        self._config: Config = Dictionary.merge(DEFAULT_CONFIG, config or {})
        self._params: list[str] = []
        self._scratch_params: list[str] = []
        self._executable: Path | None = None


    def resolve_executable(self) -> Result[Path]:
        common_paths = [
            Path.home() / "Steam" / "steamapps" / "common" / "Arma Reforger" / "ArmaReforgerServer",
            Path.home() / ".local" / "share" / "Steam" / "steamapps" / "common" / "Arma Reforger" / "ArmaReforgerServer",
            Path("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Arma Reforger\\ArmaReforgerServer.exe"),
        ]

        if directory := self._config.get('installDirectory'):
            common_paths.insert(0, Path(directory).absolute() / 'ArmaReforgerServer')

        if executable := self._config.get('executable'):
            common_paths.insert(0, Path(executable).absolute())

        for candidate in common_paths:
            if candidate.exists():
                self._executable = candidate.resolve()
                return Success(self._executable)

        return Failure(
            Error(ArmaReforgerExecutableError.EXECUTABLE_NOT_FOUND)
        )


    async def ensure_installed(self, runtime: TaskRuntimeInterface, steamcmd: SteamCmdExecutable) -> Result[Path]:
        if self._executable is not None and self._executable.exists():
            return Success(self._executable)
        if not is_successful(result := await self.install(runtime, steamcmd)):
            return Failure(Error(ArmaReforgerExecutableError.INSTALL_FAILED, details={
                'error': result.failure()
            }))
        if not is_successful(result := self.resolve_executable()):
            return Failure(Error(ArmaReforgerExecutableError.INSTALL_FAILED, details={
                'error': result.failure()
            }))
        return result


    async def install(self, runtime: TaskRuntimeInterface, steamcmd: SteamCmdExecutable) -> Result[None]:
        install_dir = self._config['installDirectory'] or '/arma_reforger'
        argv = (
            steamcmd
            .save_params()
            .force_install_dir(install_dir)
            .login_anonymous()
            .app_update(self.STEAM_APP_ID, validate=True)
            .quit()
            .consume_argv()
        )

        steamcmd.restore_params()

        async def log_subprocess(line: str) -> Result[None]:
            logger.info(line)
            return Success(None)

        result = await runtime.dispatch_subprocess(
            argv, cwd=install_dir,
            handle_std_stream=log_subprocess
        )

        if not is_successful(result):
            logger.info('An error occurred trying to install the Arma Reforger Server Assets: %s', result.failure())
            return result.map(lambda _: None)

        return Success(None)


    def install_directory(self) -> Result[Path]:
        if not self._executable:
            return Failure(Error(ArmaReforgerExecutableError.EXECUTABLE_NOT_FOUND))

        path = Path(self._executable).parent

        if not path:
            return Failure(Error(ArmaReforgerExecutableError.EXECUTABLE_NOT_FOUND))

        return Success(path.absolute())


    # -- Arma Reforger Server Flags -------------------------------------------

    def config(self, path: str | Path) -> ArmaReforgerServerExecutable:
        """Path to a server configuration JSON file."""
        self.push(ArmaReforgerExecutableFlag.CONFIG_FILE, str(Path(path).resolve()))
        return self

    def profile(self, path: str | Path) -> ArmaReforgerServerExecutable:
        """Directory for profiles (saves, logs, settings).

        The directory is created automatically if it does not exist.
        """
        target = Path(path)
        target.mkdir(parents=True, exist_ok=True)
        self.push(ArmaReforgerExecutableFlag.PROFILE_DIR, str(target.resolve()))
        return self

    def logs_dir(self, path: str | Path) -> ArmaReforgerServerExecutable:
        """Redirect log output to the given directory."""
        target = Path(path)
        target.mkdir(parents=True, exist_ok=True)
        self.push(ArmaReforgerExecutableFlag.LOGS_DIR, str(target.resolve()))
        return self

    def bind(
        self,
        *,
        address: str | None = None,
        game_port: int | None = None,
        steam_port: int | None = None,
    ) -> ArmaReforgerServerExecutable:
        """Bind the server to specific addresses / ports.

        Keyword Args:
            address: IP address to bind (sets ``-bindIP``).
            game_port: Game UDP port (sets ``-gamePort``).
            steam_port: Steam query UDP port (sets ``-steamPort``).
        """
        if address:
            self.push(ArmaReforgerExecutableFlag.BIND_IP, address)
        if game_port is not None:
            self.push(ArmaReforgerExecutableFlag.GAME_PORT, game_port)
        if steam_port is not None:
            self.push(ArmaReforgerExecutableFlag.STEAM_PORT, steam_port)
        return self

    def a2s(
        self,
        *,
        address: str | None = None,
        query_port: int | None = None,
    ) -> ArmaReforgerServerExecutable:
        """Configure A2S query endpoint.

        Keyword Args:
            address: IP address for A2S queries (sets ``-a2s``).
            query_port: UDP port for A2S queries (sets ``-a2sPort``).
        """
        if address:
            self.push(ArmaReforgerExecutableFlag.A2S_ADDRESS, address)
        if query_port is not None:
            self.push(ArmaReforgerExecutableFlag.A2S_PORT, query_port)
        return self

    def rcon(
        self,
        *,
        address: str | None = None,
        port: int | None = None,
        password: str | None = None,
    ) -> ArmaReforgerServerExecutable:
        """Configure BattlEye / RCON remote console.

        Keyword Args:
            address: IP address for RCON (sets ``-rcon``).
            port: TCP port for RCON (sets ``-rconPort``).
            password: RCON password (sets ``-rconPassword``).
        """
        if address:
            self.push(ArmaReforgerExecutableFlag.RCON_HOST, address)
        if port is not None:
            self.push(ArmaReforgerExecutableFlag.RCON_PORT, port)
        if password is not None:
            self.push(ArmaReforgerExecutableFlag.RCON_PASSWORD, password)
        return self

    def limit_fps(self, fps: int) -> ArmaReforgerServerExecutable:
        """Cap the server frame rate."""
        self.push(ArmaReforgerExecutableFlag.MAX_FPS, fps)
        return self

    def addon(self, mod_id: str) -> ArmaReforgerServerExecutable:
        """Load a server-side addon (mod) by ID.

        May be called multiple times to load several mods.
        """
        self.push(ArmaReforgerExecutableFlag.ADDONS, mod_id)
        return self

    def addons(self, *mod_ids: str) -> ArmaReforgerServerExecutable:
        """Load multiple addons at once.

        Args:
            mod_ids: Variable-length list of Steam Workshop / mod IDs.
        """
        self.push(ArmaReforgerExecutableFlag.ADDONS, ",".join(mod_ids))
        return self

    def scenario(self, scenario_id: str) -> ArmaReforgerServerExecutable:
        """ID of the scenario to host."""
        self.push(ArmaReforgerExecutableFlag.SCENARIO, scenario_id)
        return self

    def auto_reload(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Auto-restart the server when it crashes (default: ``True``)."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.AUTO_RELOAD)
        return self

    def server_id(self, server_id: str) -> ArmaReforgerServerExecutable:
        """Unique server identifier."""
        self.push(ArmaReforgerExecutableFlag.SERVER_ID, server_id)
        return self

    def region(self, region: str) -> ArmaReforgerServerExecutable:
        """Server region tag (used by the server browser)."""
        self.push(ArmaReforgerExecutableFlag.SERVER_REGION, region)
        return self

    def load_session_save(self, path: str | Path) -> ArmaReforgerServerExecutable:
        """Path to a session save to load on startup."""
        self.push(ArmaReforgerExecutableFlag.LOAD_SESSION_SAVE, str(Path(path).resolve()))
        return self

    def force_session_load(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Force loading a session save even if version mismatched."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.FORCE_SESSION_LOAD)
        return self

    def addons_dir(self, *paths: str | Path) -> ArmaReforgerServerExecutable:
        """Additional directories to search for mods.

        Multiple directories can be passed; they are joined with commas.
        """
        self.push(
            ArmaReforgerExecutableFlag.ADDONS_DIR,
            ",".join(str(Path(p).resolve()) for p in paths),
        )
        return self

    def addon_download_dir(self, path: str | Path) -> ArmaReforgerServerExecutable:
        """Directory where addons are downloaded."""
        self.push(ArmaReforgerExecutableFlag.ADDON_DOWNLOAD_DIR, str(Path(path).resolve()))
        return self

    def addon_temp_dir(self, path: str | Path) -> ArmaReforgerServerExecutable:
        """Directory for temporary addon data."""
        self.push(ArmaReforgerExecutableFlag.ADDON_TEMP_DIR, str(Path(path).resolve()))
        return self

    def backend_disable_storage(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Disable storage loads and saves (online and local)."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.BACKEND_DISABLE_STORAGE)
        return self

    def backend_fresh_session(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Skip the initial load request and start a brand-new session."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.BACKEND_FRESH_SESSION)
        return self

    def backend_local_storage(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Force save/load to use local JSON files instead of the backend."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.BACKEND_LOCAL_STORAGE)
        return self

    def freeze_check(self, seconds: int) -> ArmaReforgerServerExecutable:
        """Override the freeze-detection timeout in seconds (0..600)."""
        self.push(ArmaReforgerExecutableFlag.FREEZE_CHECK, seconds)
        return self

    def freeze_check_mode(self, mode: str) -> ArmaReforgerServerExecutable:
        """Behaviour on freeze: ``crash``, ``minidump`` or ``kill``."""
        self.push(ArmaReforgerExecutableFlag.FREEZE_CHECK_MODE, mode)
        return self

    def cfg(self, path: str | Path) -> ArmaReforgerServerExecutable:
        """Load a specific user engine-settings config file."""
        self.push(ArmaReforgerExecutableFlag.CFG, str(Path(path).resolve()))
        return self

    def language(self, code: str) -> ArmaReforgerServerExecutable:
        """Set the game language (e.g. ``en_us``, ``de_de``)."""
        self.push(ArmaReforgerExecutableFlag.LANGUAGE, code)
        return self

    def no_backend(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Disable backend HTTP communication."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.NO_BACKEND)
        return self

    def no_sound(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Disable the sound system."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.NO_SOUND)
        return self

    def no_splash(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Skip splash screens on startup."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.NO_SPLASH)
        return self

    def no_throw(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Suppress all error-message dialogs."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.NO_THROW)
        return self

    def single_threaded_update(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Disable multi-threaded update."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.SINGLE_THREADED_UPDATE)
        return self

    def world(self, path: str | Path) -> ArmaReforgerServerExecutable:
        """World file to load on startup (relative or absolute path)."""
        self.push(ArmaReforgerExecutableFlag.WORLD, str(Path(path)))
        return self

    # -- Hosting --------------------------------------------------------------

    def a2s_ip_address(self, address: str) -> ArmaReforgerServerExecutable:
        """Set the Steam Query Protocol bind IP address."""
        self.push(ArmaReforgerExecutableFlag.A2S_IP_ADDRESS, address)
        return self

    def autoshutdown(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Ensure a clean server shutdown after the game ends."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.AUTOSHUTDOWN)
        return self

    def enable_night_grain(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Enable night grain in multiplayer."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.ENABLE_NIGHT_GRAIN)
        return self

    def list_scenarios(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Print scenario .conf file paths to the log on startup."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.LIST_SCENARIOS)
        return self

    def keep_session_save(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Keep save data for completed playthroughs on the end screen."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.KEEP_SESSION_SAVE)
        return self

    def log_stats(self, interval_ms: int | None = None) -> ArmaReforgerServerExecutable:
        """Log performance statistics every *interval_ms* (default 1000 ms)."""
        if interval_ms is not None:
            self.push(ArmaReforgerExecutableFlag.LOG_STATS, interval_ms)
        else:
            self._params.append(ArmaReforgerExecutableFlag.LOG_STATS)
        return self

    def log_voting(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Add logging to the voting system."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.LOG_VOTING)
        return self

    def player_limits(self, *limits: str) -> ArmaReforgerServerExecutable:
        """Maximum players per faction (``FactionKey:Number`` pairs)."""
        self.push(ArmaReforgerExecutableFlag.PLAYER_LIMITS, ",".join(limits))
        return self

    def server_world(self, path: str | Path) -> ArmaReforgerServerExecutable:
        """Launch a local server and load the specified world file."""
        self.push(ArmaReforgerExecutableFlag.SERVER, str(Path(path)))
        return self

    def addons_verify(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Verify integrity of all installed addons on startup."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.ADDONS_VERIFY)
        return self

    def addons_repair(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Repair corrupted addons automatically on startup."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.ADDONS_REPAIR)
        return self

    # -- Network Tuning -------------------------------------------------------

    def nds(self, diameter: int) -> ArmaReforgerServerExecutable:
        """Network Dynamic Simulation cell diameter (0 disables)."""
        self.push(ArmaReforgerExecutableFlag.NDS, diameter)
        return self

    def nwk_resolution(self, meters: int) -> ArmaReforgerServerExecutable:
        """Spatial-map cell resolution in meters (100..1000)."""
        self.push(ArmaReforgerExecutableFlag.NWK_RESOLUTION, meters)
        return self

    def rpl_timeout_ms(self, milliseconds: int) -> ArmaReforgerServerExecutable:
        """Replication client/server timeout in milliseconds."""
        self.push(ArmaReforgerExecutableFlag.RPL_TIMEOUT_MS, milliseconds)
        return self

    def staggering_budget(self, cells: int) -> ArmaReforgerServerExecutable:
        """Stationary spatial-map cells processed per tick (1..10201)."""
        self.push(ArmaReforgerExecutableFlag.STAGGERING_BUDGET, cells)
        return self

    def streaming_budget(self, budget: int) -> ArmaReforgerServerExecutable:
        """Global streaming budget distributed between all connections."""
        self.push(ArmaReforgerExecutableFlag.STREAMING_BUDGET, budget)
        return self

    def streams_delta(self, delta: int) -> ArmaReforgerServerExecutable:
        """Limit the number of streams opened for a client (1..1000)."""
        self.push(ArmaReforgerExecutableFlag.STREAMS_DELTA, delta)
        return self

    # -- Debug ----------------------------------------------------------------

    def ai_limit(self, count: int) -> ArmaReforgerServerExecutable:
        """Hard cap on the number of AIs that can exist."""
        self.push(ArmaReforgerExecutableFlag.AI_LIMIT, count)
        return self

    def ai_partial_sim(self, batches: int) -> ArmaReforgerServerExecutable:
        """Divide simulable AIs into *batches* for processing."""
        self.push(ArmaReforgerExecutableFlag.AI_PARTIAL_SIM, batches)
        return self

    def create_db(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Force regeneration of the resource database file."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.CREATE_DB)
        return self

    def debugger(self, address: str) -> ArmaReforgerServerExecutable:
        """Set the script debugger target address."""
        self.push(ArmaReforgerExecutableFlag.DEBUGGER, address)
        return self

    def debugger_port(self, port: int) -> ArmaReforgerServerExecutable:
        """Set the script debugger port."""
        self.push(ArmaReforgerExecutableFlag.DEBUGGER_PORT, port)
        return self

    def disable_ai(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Disable AIWorld initialisation and ticking."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.DISABLE_AI)
        return self

    def disable_crash_reporter(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Disable the Crash Reporter."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.DISABLE_CRASH_REPORTER)
        return self

    def disable_navmesh_streaming(self, *projects: str) -> ArmaReforgerServerExecutable:
        """Disable navmesh streaming for the given projects (or all if none)."""
        if projects:
            self.push(ArmaReforgerExecutableFlag.DISABLE_NAVMESH_STREAMING, ",".join(projects))
        else:
            self._params.append(ArmaReforgerExecutableFlag.DISABLE_NAVMESH_STREAMING)
        return self

    def disable_shaders_build(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Disable shader generation on startup."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.DISABLE_SHADERS_BUILD)
        return self

    def generate_shaders(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Force shader generation on startup."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.GENERATE_SHADERS)
        return self

    def rpl_encode_as_long_jobs(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Make replication use long encoding jobs."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.RPL_ENCODE_AS_LONG_JOBS)
        return self

    def jobsys_short_worker_count(self, count: int) -> ArmaReforgerServerExecutable:
        """Threads for short jobs (capped to CPU count or 16)."""
        self.push(ArmaReforgerExecutableFlag.JOBSYS_SHORT_WORKER_COUNT, count)
        return self

    def jobsys_long_worker_count(self, count: int) -> ArmaReforgerServerExecutable:
        """Threads for long jobs."""
        self.push(ArmaReforgerExecutableFlag.JOBSYS_LONG_WORKER_COUNT, count)
        return self

    def keep_num_of_logs(self, count: int) -> ArmaReforgerServerExecutable:
        """Maximum number of log files to retain."""
        self.push(ArmaReforgerExecutableFlag.KEEP_NUM_OF_LOGS, count)
        return self

    def log_rdb_checksum(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Log detailed RDB checksum computation."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.LOG_RDB_CHECKSUM)
        return self

    def log_scr_checksum(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Log all script files used in compilation and their checksums."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.LOG_SCR_CHECKSUM)
        return self

    def log_append(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Append to existing logs instead of truncating on startup."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.LOG_APPEND)
        return self

    def log_fs(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Log every file-system read/write operation (very verbose)."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.LOG_FS)
        return self

    def log_level(self, level: str) -> ArmaReforgerServerExecutable:
        """Set the log verbosity: ``normal``, ``warning``, ``error`` or ``fatal``."""
        self.push(ArmaReforgerExecutableFlag.LOG_LEVEL, level)
        return self

    def log_time(self, fmt: str) -> ArmaReforgerServerExecutable:
        """Log timestamp format: ``none``, ``time`` or ``datetime``."""
        self.push(ArmaReforgerExecutableFlag.LOG_TIME, fmt)
        return self

    def keep_crash_files(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Prevent the Crash Reporter from cleaning up crash files."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.KEEP_CRASH_FILES)
        return self

    def minidump(self, mode: str) -> ArmaReforgerServerExecutable:
        """Minidump detail level: ``normal``, ``dataSegs`` or ``fullMemory``."""
        self.push(ArmaReforgerExecutableFlag.MINIDUMP, mode)
        return self

    def script_authorize_all(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Suppress security popups for script operations."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.SCRIPT_AUTHORIZE_ALL)
        return self

    def silent_crash_report(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Suppress the Crash Reporter dialog and send reports silently."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.SILENT_CRASH_REPORT)
        return self

    def vm_error_mode(self, mode: str) -> ArmaReforgerServerExecutable:
        """Script VM error mode: ``silent``, ``log_only``, ``full`` or ``fatal``."""
        self.push(ArmaReforgerExecutableFlag.VM_ERROR_MODE, mode)
        return self

    # -- Profiling ------------------------------------------------------------

    def check_instance(self, enabled: bool = True) -> ArmaReforgerServerExecutable:
        """Enable script VM memory-allocation logging."""
        if enabled:
            self._params.append(ArmaReforgerExecutableFlag.CHECK_INSTANCE)
        return self

    # -- Miscellaneous --------------------------------------------------------

    def custom(self, flag: str, *values: str | int) -> ArmaReforgerServerExecutable:
        """Append an arbitrary launch flag and values.

        Useful for undocumented or future parameters.

        Args:
            flag: The flag name (e.g. ``"-myFlag"``).
            values: Flag values.
        """
        self.push(flag, *values)
        return self


# --- Internal Types ----------------------------------------------------------

class ArmaReforgerExecutableError(StrEnum):
    EXECUTABLE_NOT_FOUND = "the arma reforger server executable could not be found in the host system"
    INSTALL_FAILED = "the arma reforger executable could not be installed"
