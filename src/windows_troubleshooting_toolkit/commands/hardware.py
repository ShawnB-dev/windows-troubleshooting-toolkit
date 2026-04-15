import psutil
from .util import header, section, run_command


def run(args):
    pieces = [header("Hardware Diagnostics")]

    pieces.append(section("Device Errors"))
    pieces.append(run_command([
        "powershell",
        "-NoProfile",
        "-Command",
        "Try { Get-PnpDevice -Status Error | Select-Object Class, FriendlyName, InstanceId | Format-Table -AutoSize } Catch { Write-Error $_.Exception.Message }"
    ]))

    pieces.append(section("GPU / Display Adapter"))
    pieces.append(run_command([
        "wmic",
        "path",
        "win32_VideoController",
        "get",
        "Name,DriverVersion"
    ]))

    pieces.append(section("Battery / Power"))
    battery = psutil.sensors_battery()
    if battery is not None:
        pieces.append(f"Percent: {battery.percent}%")
        pieces.append(f"Plugged In: {battery.power_plugged}")
        pieces.append(f"Secs Left: {battery.secsleft}")
    else:
        pieces.append("Battery information is not available on this device.")

    return "\n".join(pieces)
