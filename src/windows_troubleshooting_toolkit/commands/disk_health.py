import psutil
from .util import header, section, normalize_size, run_command


def run(args):
    pieces = [header("Disk Health Diagnostics")]

    pieces.append(section("Disk Drives"))
    pieces.append(run_command(["wmic", "diskdrive", "get", "Model,Status,InterfaceType,Size"]))

    pieces.append(section("Logical Disks"))
    for partition in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            pieces.append(
                f"{partition.device} ({partition.fstype}) mounted on {partition.mountpoint}: "
                f"{normalize_size(usage.used)} used of {normalize_size(usage.total)} ({usage.percent}%)"
            )
        except PermissionError:
            pieces.append(f"{partition.device} ({partition.fstype}) mounted on {partition.mountpoint}: permission denied")

    pieces.append(section("Disk Check Summary"))
    if psutil.WINDOWS:
        target = "C:"
        pieces.append(run_command(["chkdsk", target]))
    else:
        pieces.append("Disk check summary is available only on Windows.")

    return "\n".join(pieces)
