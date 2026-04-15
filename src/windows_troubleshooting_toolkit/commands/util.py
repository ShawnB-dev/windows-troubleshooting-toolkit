import platform
import psutil
import subprocess
from datetime import datetime


def normalize_size(value: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    index = 0
    while value >= 1024 and index < len(units) - 1:
        value /= 1024.0
        index += 1
    return f"{value:.2f} {units[index]}"


def header(title: str) -> str:
    return f"{title}\n{'=' * len(title)}\n"


def section(title: str) -> str:
    return f"\n{title}\n{'-' * len(title)}\n"


def run_command(command, timeout=20) -> str:
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
        )
        output = completed.stdout.strip() or completed.stderr.strip()
        if completed.returncode != 0 and output:
            return output
        return output or f"Command {' '.join(command)} returned no output."
    except FileNotFoundError:
        return f"Command not found: {command[0]}"
    except subprocess.TimeoutExpired:
        return f"Command timed out: {' '.join(command)}"
    except Exception as exc:
        return f"Failed to run {' '.join(command)}: {exc}"


def get_system_info() -> str:
    uname = platform.uname()
    boot = datetime.fromtimestamp(psutil.boot_time()).isoformat(sep=" ", timespec="seconds")
    lines = [
        f"System: {uname.system}",
        f"Node Name: {uname.node}",
        f"Release: {uname.release}",
        f"Version: {uname.version}",
        f"Machine: {uname.machine}",
        f"Processor: {uname.processor}",
        f"Boot Time: {boot}",
    ]
    return "\n".join(lines)
