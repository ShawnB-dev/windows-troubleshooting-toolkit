import time
import psutil
from .util import header, section, normalize_size


def format_process(proc):
    try:
        info = proc.as_dict(attrs=["pid", "name", "cpu_percent", "memory_info", "num_threads", "num_handles"])
        rss = normalize_size(info["memory_info"].rss) if info.get("memory_info") else "N/A"
        return f"{info['pid']:>5} {info['name'][:25]:25} CPU {info['cpu_percent']:5.1f}% MEM {rss} THR {info.get('num_threads', 0)}"
    except psutil.NoSuchProcess:
        return "Process terminated"


def run(args):
    pieces = [header("Performance Diagnostics")]

    pieces.append(section("CPU Usage"))
    cpu = psutil.cpu_percent(interval=1, percpu=True)
    pieces.append("CPU usage per core: " + ", ".join(f"{value}%" for value in cpu))
    pieces.append(f"Total CPU usage: {psutil.cpu_percent()}%")

    pieces.append(section("Top Processes by CPU"))
    procs = sorted(psutil.process_iter(), key=lambda p: p.cpu_percent(interval=0.1), reverse=True)
    for proc in procs[:10]:
        pieces.append(format_process(proc))

    pieces.append(section("Top Processes by Memory"))
    procs_by_mem = sorted(psutil.process_iter(), key=lambda p: p.memory_info().rss if p.is_running() else 0, reverse=True)
    for proc in procs_by_mem[:10]:
        pieces.append(format_process(proc))

    pieces.append(section("Disk IO"))
    io = psutil.disk_io_counters()
    pieces.append(f"Read: {normalize_size(io.read_bytes)}, Write: {normalize_size(io.write_bytes)}")

    pieces.append(section("Network IO"))
    net_io = psutil.net_io_counters()
    pieces.append(f"Sent: {normalize_size(net_io.bytes_sent)}, Received: {normalize_size(net_io.bytes_recv)}")

    return "\n".join(pieces)
