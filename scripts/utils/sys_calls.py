"""
Utilities to interface with the outside world.
"""

import os
import subprocess
from typing import Dict, List, Tuple, Union


# -----------------------------------------------------------------
# Check prereqs installed
# -----------------------------------------------------------------


def check_prereqs_installed() -> None:
    """
    Confirm all required software installed.
    """
    pass  # nothing required


# -----------------------------------------------------------------
# Determine environment
# -----------------------------------------------------------------


def is_windows_environment() -> bool:
    """
    Return True if on Windows, else on Posix.
    """
    return os.name == "nt"


def determine_python_executable() -> str:
    """
    Get name of python executable depending on system.
    """
    return "python3" if not is_windows_environment() else "python"


Command = Union[List[str], str]


def _modify_for_windows(command: List[str], kwargs: Dict) -> Tuple[Command, Dict]:
    """
    Allows running the command on Windows, if Windows is detected.
    """
    if is_windows_environment():
        windows_command = " ".join(command)
        windows_kwargs = dict(kwargs, shell=True)
        return windows_command, windows_kwargs
    return command, kwargs


# -----------------------------------------------------------------
# Modify environment
# -----------------------------------------------------------------


def export(key: str, value: str) -> None:
    """
    Add value to environment.
    """
    os.environ[key] = value


# -----------------------------------------------------------------
# Run commands
# -----------------------------------------------------------------


def _check_return_code(process: subprocess.CompletedProcess) -> None:
    """
    Ensures process had 0 exit code, and fails
    """
    try:
        process.check_returncode()
    except subprocess.CalledProcessError:
        raise SystemExit(f"\n\nCommand failed.")


def run(
    command: List[str], check_return_code: bool = True, **kwargs
) -> subprocess.CompletedProcess:
    """
    Calls subprocess.run() and allows seamless support of both Windows and Unix.
    """
    new_command, new_kwargs = _modify_for_windows(command, kwargs)
    completed_process = subprocess.run(new_command, **new_kwargs)
    if check_return_code:
        _check_return_code(completed_process)
    return completed_process


def run_detached(command: List[str], **kwargs) -> None:
    """
    Calls non-blocking subprocess.Popen() and ignores all input and output.
    """
    new_command, new_kwargs = _modify_for_windows(command, kwargs)
    subprocess.Popen(
        new_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **new_kwargs
    )


def run_as_shell(
    command: str, check_return_code: bool = True, **kwargs
) -> subprocess.CompletedProcess:
    """
    Calls subprocess.run() with shell=True.
    """
    completed_process = subprocess.run(command, shell=True, **kwargs)
    if check_return_code:
        _check_return_code(completed_process)
    return completed_process


def run_python(
    command: List[str], check_return_code: bool = True, **kwargs
) -> subprocess.CompletedProcess:
    """
    Run the command using Python executable.
    """
    python = determine_python_executable()
    new_command, new_kwargs = _modify_for_windows([python] + command, kwargs)
    completed_process = subprocess.run(new_command, **new_kwargs)
    if check_return_code:
        _check_return_code(completed_process)
    return completed_process


# -----------------------------------------------------------------
# Get StdOut of process
# -----------------------------------------------------------------


def get_stdout(command: List[str], check_return_code: bool = True, **kwargs) -> str:
    """
    Performs the given command and returns the stdout as a string.
    """
    new_command, new_kwargs = _modify_for_windows(command, kwargs)
    completed_process = subprocess.run(
        new_command, stdout=subprocess.PIPE, encoding="utf-8", **new_kwargs
    )
    if check_return_code:
        _check_return_code(completed_process)
    stdout: str = completed_process.stdout.strip()
    return stdout


def get_stdout_as_shell(command: str, check_return_code: bool = True, **kwargs) -> str:
    """
    Performs the given command using Shell and returns the stdout as a string.
    """
    completed_process = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, encoding="utf-8", **kwargs
    )
    if check_return_code:
        _check_return_code(completed_process)
    stdout: str = completed_process.stdout.strip()
    return stdout
