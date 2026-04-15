from .util import header, section, normalize_size
import psutil


def run(args):
    pieces = [header("Process Diagnostics")]
    pieces.append(section("Top Processes by CPU"))
    processes = sorted(psutil.process_iter(["pid", "name", "cpu_percent", "memory_info"]), key=lambda p: p.info["cpu_percent"] or 0, reverse=True)
    for proc in processes[:10]:
        info = proc.info
        mem = normalize_size(info["memory_info"].rss) if info.get("memory_info") else "N/A"
        pieces.append(f"{info['pid']:>5} {info['name'][:25]:25} CPU {info['cpu_percent']:5.1f}% MEM {mem}")

    pieces.append(section("Memory Usage by Process"))
    by_mem = sorted(processes, key=lambda p: (p.info.get("memory_info").rss if p.info.get("memory_info") else 0), reverse=True)
    for proc in by_mem[:10]:
        info = proc.info
        mem = normalize_size(info["memory_info"].rss) if info.get("memory_info") else "N/A"
        pieces.append(f"{info['pid']:>5} {info['name'][:25]:25} RSS {mem}")

    return "\n".join(pieces)
