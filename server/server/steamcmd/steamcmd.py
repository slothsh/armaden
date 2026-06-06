"""Python wrapper for the steamcmd CLI tool.

Provides a typed, fluent interface for driving steamcmd with proper error
handling, output capture, and subprocess management.

Example::

    from server.steamcmd import SteamCmd

    sc = SteamCmd()
    result = (
        sc.login_anonymous()
        .force_install_dir("/arma/server")
        .app_update(233780, validate=True)
        .run()
    )
    print(result.stdout)

See Valve's steamcmd documentation for command details:
https://developer.valvesoftware.com/wiki/SteamCMD
"""

from __future__ import annotations

import dataclasses
import logging
import os
import shutil
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class SteamCmdError(Exception):
    """Base exception for steamcmd errors."""

    pass


class SteamCmdNotFoundError(SteamCmdError):
    """Raised when the steamcmd executable cannot be located."""

    pass


class SteamCmdExitError(SteamCmdError):
    """Raised when steamcmd exits with a non-zero status.

    Attributes:
        returncode: Exit code from the process.
        stdout: Captured standard output.
        stderr: Captured standard error.
        command: The steamcmd command sequence that was executed.
    """

    def __init__(
        self,
        returncode: int,
        stdout: str,
        stderr: str,
        command: list[str],
    ) -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.command = command
        super().__init__(
            f"steamcmd exited with code {returncode}: "
            f"{' '.join(command[:5])}..."
        )


@dataclasses.dataclass(frozen=True)
class SteamCmdResult:
    """Result of a steamcmd execution.

    Attributes:
        returncode: Process exit code.
        stdout: Complete standard output as a string.
        stderr: Complete standard error as a string.
        command: The full list of arguments passed to the subprocess.
    """

    returncode: int
    stdout: str
    stderr: str
    command: list[str]

    @property
    def success(self) -> bool:
        """Whether the command completed successfully (returncode == 0)."""
        return self.returncode == 0

    def raise_for_status(self) -> SteamCmdResult:
        """Raise :exc:`SteamCmdExitError` if the command failed.

        Returns:
            ``self`` to support fluent chaining.

        Raises:
            SteamCmdExitError: If ``returncode != 0``.
        """
        if not self.success:
            raise SteamCmdExitError(
                self.returncode,
                self.stdout,
                self.stderr,
                self.command,
            )
        return self


class SteamCmd:
    """Fluent wrapper for the steamcmd command-line tool.

    Commands are accumulated via method calls until :meth:`run` is invoked.
    The wrapper supports running steamcmd either by building an ``+`` prefixed
    argument list (the default) or by generating a temporary script file via
    :meth:`run_script`.

    Args:
        executable: Path to the steamcmd binary. ``"steamcmd"`` is used if
            the binary is on ``$PATH``; otherwise common install locations
            are tried.
        cwd: Working directory for the subprocess.
        env: Additional environment variables for the subprocess.

    Example::

        sc = SteamCmd()
        result = (
            sc.login_anonymous()
            .force_install_dir("/games/arma")
            .app_update(233780, validate=True)
            .run()
        )
    """

    # Common install locations to probe when `steamcmd` is not on PATH.
    _COMMON_PATHS: tuple[Path, ...] = (
        Path.home() / "Steam" / "steamcmd" / "steamcmd.sh",
        Path("/usr/games/steamcmd"),
        Path("/usr/local/bin/steamcmd"),
        Path("C:\\steamcmd\\steamcmd.exe"),
    )

    def __init__(
        self,
        executable: str | Path | None = None,
        cwd: str | Path | None = None,
        env: dict[str, str] | None = None,
    ) -> None:
        self._executable = self._resolve_executable(executable)
        self._cwd = cwd
        self._env: dict[str, str] = {**os.environ, **(env or {})}
        self._commands: list[str] = []

    # ------------------------------------------------------------------
    # Core helpers
    # ------------------------------------------------------------------

    @classmethod
    def _resolve_executable(cls, executable: str | Path | None = None) -> Path:
        """Return the absolute path to the steamcmd binary.

        Raises:
            SteamCmdNotFoundError: If no binary can be found.
        """
        if executable is not None:
            path = Path(executable)
            if path.exists():
                return path.resolve()
            # shutil.which handles both relative and absolute lookups.
            found = shutil.which(str(executable))
            if found:
                return Path(found).resolve()
            raise SteamCmdNotFoundError(
                f"Provided executable not found: {executable}"
            )

        # Try the generic command name first.
        found = shutil.which("steamcmd")
        if found:
            return Path(found).resolve()

        # Probe common install locations.
        for candidate in cls._COMMON_PATHS:
            if candidate.exists():
                return candidate.resolve()

        raise SteamCmdNotFoundError(
            "steamcmd executable not found on PATH or in common install locations. "
            "Provide the full path via the `executable` argument."
        )

    def _push(self, command: str, *args: str | int) -> SteamCmd:
        """Append a steamcmd command and its arguments, returning self.

        steamcmd expects commands prefixed with ``+`` and arguments separated
        by spaces in the argv list.
        """
        self._commands.append(f"+{command}")
        for arg in args:
            self._commands.append(str(arg))
        return self

    def _append(self, *tokens: str | int) -> SteamCmd:
        """Append raw tokens to the command list (no ``+`` prefix)."""
        for token in tokens:
            self._commands.append(str(token))
        return self

    def _build_argv(self) -> list[str]:
        """Return the full argument vector for :func:`subprocess.run`."""
        return [str(self._executable), *self._commands]

    # ------------------------------------------------------------------
    # Public fluent commands
    # ------------------------------------------------------------------

    def login(self, username: str, password: str | None = None) -> SteamCmd:
        """Authenticate with a specific Steam account.

        Args:
            username: Steam username.
            password: Optional password. Prefer using Steam Guard tokens
                or the anonymous login for headless environments.
        """
        if password:
            return self._push("login", username, password)
        return self._push("login", username)

    def login_anonymous(self) -> SteamCmd:
        """Log in with an anonymous account (no credentials required)."""
        return self._push("login", "anonymous")

    def force_install_dir(self, path: str | Path) -> SteamCmd:
        """Set the installation directory for subsequent app operations.

        Args:
            path: Target directory. Created automatically if it does not exist.
        """
        target = Path(path)
        target.mkdir(parents=True, exist_ok=True)
        return self._push("force_install_dir", str(target.resolve()))

    def app_update(
        self,
        app_id: int,
        validate: bool = False,
        beta: str | None = None,
        beta_password: str | None = None,
    ) -> SteamCmd:
        """Request an application update.

        Args:
            app_id: Steam AppID to install or update.
            validate: If ``True``, append ``validate`` to verify file integrity.
            beta: Optional beta branch name.
            beta_password: Optional password for the beta branch.
        """
        self._push("app_update", app_id)
        if beta is not None:
            self._append("-beta", beta)
        if beta_password is not None:
            self._append("-betapassword", beta_password)
        if validate:
            self._append("validate")
        return self

    def app_info_print(self, app_id: int) -> SteamCmd:
        """Print application metadata (useful for resolving depots or branches).

        Args:
            app_id: Steam AppID to inspect.
        """
        return self._push("app_info_print", app_id)

    def workshop_download_item(self, app_id: int, item_id: int) -> SteamCmd:
        """Download a Steam Workshop item.

        Args:
            app_id: Parent application AppID.
            item_id: Workshop item ID to download.
        """
        return self._push("workshop_download_item", app_id, item_id)

    def quit(self) -> SteamCmd:
        """Insert an explicit ``quit`` command.

        steamcmd implicitly quits when input is exhausted, but an explicit
        command ensures predictable behaviour.
        """
        return self._push("quit")

    def raw(self, command: str, *args: str | int) -> SteamCmd:
        """Send an arbitrary steamcmd command.

        Useful for commands not yet covered by dedicated methods.

        Args:
            command: Command name (without leading ``+``).
            args: Command arguments.
        """
        return self._push(command, *args)

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def run(
        self,
        *,
        capture_output: bool = True,
        timeout: float | None = None,
        text: bool = True,
    ) -> SteamCmdResult:
        """Execute the accumulated command sequence.

        By default, an explicit ``+quit`` is appended automatically.

        Keyword Args:
            capture_output: Capture stdout and stderr instead of inheriting
                the parent's file descriptors.
            timeout: Maximum runtime in seconds. ``None`` disables the timeout.
            text: Decode stdout/stderr as text (``True`` by default).

        Returns:
            A :class:`SteamCmdResult` containing exit code and outputs.

        Raises:
            SteamCmdExitError: If the process exits with a non-zero code
                (wrapped in the result; callers can inspect
                :attr:`SteamCmdResult.returncode`).
            SteamCmdError: For other subprocess failures (e.g., timeout,
                process not found).
        """
        if not self._commands or self._commands[-1] != "+quit":
            self.quit()

        argv = self._build_argv()
        logger.debug("Executing steamcmd: %s", " ".join(argv))

        kwargs: dict[str, Any] = {
            "args": argv,
            "cwd": self._cwd,
            "env": self._env,
            "text": text,
        }

        if capture_output:
            kwargs["stdout"] = subprocess.PIPE
            kwargs["stderr"] = subprocess.PIPE

        try:
            proc = subprocess.run(argv, timeout=timeout, **kwargs)
        except subprocess.TimeoutExpired as exc:
            raise SteamCmdError(
                f"steamcmd timed out after {timeout} seconds: {' '.join(argv)}"
            ) from exc
        except FileNotFoundError as exc:
            raise SteamCmdNotFoundError(
                f"steamcmd executable disappeared: {self._executable}"
            ) from exc
        except OSError as exc:
            raise SteamCmdError(
                f"Failed to execute steamcmd: {exc}"
            ) from exc

        stdout = proc.stdout if isinstance(proc.stdout, str) else ""
        stderr = proc.stderr if isinstance(proc.stderr, str) else ""

        result = SteamCmdResult(
            returncode=proc.returncode,
            stdout=stdout,
            stderr=stderr,
            command=argv,
        )

        if result.returncode != 0:
            logger.warning(
                "steamcmd exited with code %d\nstdout: %s\nstderr: %s",
                result.returncode,
                stdout[:2000],
                stderr[:2000],
            )

        return result

    def run_script(
        self,
        script_path: str | Path,
        *,
        capture_output: bool = True,
        timeout: float | None = None,
        text: bool = True,
    ) -> SteamCmdResult:
        """Execute a pre-existing steamcmd script file.

        steamcmd supports ``+runscript <path>`` for batching commands in a
        file. This method resets any accumulated commands and runs the script.

        Args:
            script_path: Path to the script file.

        Keyword Args:
            capture_output: Capture stdout and stderr.
            timeout: Maximum runtime in seconds.
            text: Decode outputs as text.

        Returns:
            The execution result.
        """
        self._commands = []
        self._push("runscript", str(Path(script_path).resolve()))
        return self.run(
            capture_output=capture_output,
            timeout=timeout,
            text=text,
        )

    def stream(
        self,
        *,
        timeout: float | None = None,
        text: bool = True,
    ) -> Iterator[str]:
        """Execute steamcmd and yield output lines as they are produced.

        This is useful for monitoring long-running downloads or updates.

        Keyword Args:
            timeout: Maximum runtime in seconds.
            text: Decode output as text (``True`` by default).

        Yields:
            Lines from the process stdout.

        Raises:
            SteamCmdExitError: If the process exits with a non-zero code.
        """
        if not self._commands or self._commands[-1] != "+quit":
            self.quit()

        argv = self._build_argv()
        logger.debug("Streaming steamcmd: %s", " ".join(argv))

        try:
            with subprocess.Popen(
                argv,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=self._cwd,
                env=self._env,
                text=text,
            ) as proc:
                if proc.stdout is None:
                    raise SteamCmdError(
                        "Failed to open stdout pipe for steamcmd"
                    )

                for line in proc.stdout:
                    yield line.rstrip("\n\r")

                proc.wait(timeout=timeout)
                if proc.returncode != 0:
                    raise SteamCmdExitError(
                        proc.returncode,
                        "",
                        "",
                        argv,
                    )
        except subprocess.TimeoutExpired as exc:
            raise SteamCmdError(
                f"steamcmd stream timed out after {timeout} seconds"
            ) from exc
        except FileNotFoundError as exc:
            raise SteamCmdNotFoundError(
                f"steamcmd executable disappeared: {self._executable}"
            ) from exc

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    def install_app(
        self,
        app_id: int,
        install_dir: str | Path,
        *,
        validate: bool = False,
    ) -> SteamCmdResult:
        """One-shot install or update of an application.

        Equivalent to::

            login_anonymous()
            force_install_dir(install_dir)
            app_update(app_id, validate=validate)

        Args:
            app_id: Steam AppID.
            install_dir: Target installation directory.
            validate: Verify file integrity after update.

        Returns:
            Execution result.
        """
        return (
            self.login_anonymous()
            .force_install_dir(install_dir)
            .app_update(app_id, validate=validate)
            .run()
        )

    def version(self) -> str:
        """Return the steamcmd version string.

        Returns:
            Version output from ``steamcmd +quit``.

        Raises:
            SteamCmdExitError: If the command fails.
        """
        result = self.run()
        result.raise_for_status()
        return result.stdout

    def __enter__(self) -> SteamCmd:
        """Support usage as a context manager.::

            with SteamCmd() as sc:
                sc.login_anonymous()...
        """
        return self

    def __exit__(self, *exc: object) -> None:
        """Ensure a clean exit — no resources need explicit cleanup."""
        pass

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}("
            f"executable={self._executable!r}, "
            f"commands={self._commands!r})"
        )
