import subprocess
import winreg
from .util import header, section, run_command

STARTUP_KEYS = [
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
    (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
    (winreg.HKEY_LOCAL_MACHINE, r"Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Run"),
]


def read_startup_keys():
    entries = []
    for root, key_path in STARTUP_KEYS:
        try:
            with winreg.OpenKey(root, key_path) as key:
                for i in range(0, winreg.QueryInfoKey(key)[1]):
                    name, value, _ = winreg.EnumValue(key, i)
                    entries.append(f"{name}: {value}")
        except FileNotFoundError:
            continue
        except OSError as exc:
            entries.append(f"Unable to read {key_path}: {exc}")
    return entries


def run(args):
    pieces = [header("Startup Diagnostics")]

    pieces.append(section("Startup Applications"))
    for entry in read_startup_keys():
        pieces.append(entry)
    if not read_startup_keys():
        pieces.append("No startup registry entries found.")

    pieces.append(section("Scheduled Tasks"))
    pieces.append(run_command(["schtasks", "/query", "/fo", "LIST", "/v"]))

    return "\n".join(pieces)
