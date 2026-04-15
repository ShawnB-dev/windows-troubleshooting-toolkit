from .util import header, section, get_system_info, normalize_size
import psutil


def run(args):
    pieces = [header("System Diagnostics"), get_system_info()]

    cpu = psutil.cpu_percent(interval=1, percpu=True)
    pieces.append(section("CPU"))
    pieces.append(f"Physical cores: {psutil.cpu_count(logical=False)}")
    pieces.append(f"Total cores: {psutil.cpu_count(logical=True)}")
    pieces.append("CPU usage per core: " + ", ".join(f"{usage}%" for usage in cpu))
    pieces.append(f"Total CPU usage: {psutil.cpu_percent()} %")

    svmem = psutil.virtual_memory()
    pieces.append(section("Memory"))
    pieces.append(f"Total: {normalize_size(svmem.total)}")
    pieces.append(f"Available: {normalize_size(svmem.available)}")
    pieces.append(f"Used: {normalize_size(svmem.used)}")
    pieces.append(f"Percentage: {svmem.percent}%")

    disk = psutil.disk_usage("C:\\")
    pieces.append(section("Disk (C:)"))
    pieces.append(f"Total: {normalize_size(disk.total)}")
    pieces.append(f"Used: {normalize_size(disk.used)}")
    pieces.append(f"Free: {normalize_size(disk.free)}")
    pieces.append(f"Percentage: {disk.percent}%")

    return "\n".join(pieces)
