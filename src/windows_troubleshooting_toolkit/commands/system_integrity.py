import subprocess
from .util import header, section, run_command


def run(args):
    pieces = [header("System Integrity Diagnostics")]
    pieces.append(section("SFC Verify"))
    pieces.append(run_command(["sfc", "/verifyonly"]))

    pieces.append(section("DISM Image Health"))
    pieces.append(run_command(["dism", "/Online", "/Cleanup-Image", "/CheckHealth"]))

    pieces.append(section("Windows Update History"))
    pieces.append(run_command(["wmic", "qfe", "get", "HotFixID,InstalledOn,Description", "/format:list"]))

    pieces.append(section("System Restore Points"))
    pieces.append(run_command([
        "powershell",
        "-NoProfile",
        "-Command",
        "Try { Get-ComputerRestorePoint | Select-Object SequenceNumber, Description, CreationTime, RestorePointType | Format-Table -AutoSize } Catch { Write-Error $_.Exception.Message }"
    ]))

    return "\n".join(pieces)
