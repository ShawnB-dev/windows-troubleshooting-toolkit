import socket
import subprocess
import psutil
from .util import header, section, run_command


def resolve_host(host: str) -> str:
    try:
        address = socket.gethostbyname(host)
        return f"{host} resolves to {address}"
    except Exception as exc:
        return f"DNS resolution failed for {host}: {exc}"


def ping_target(target: str) -> str:
    return run_command(["ping", "-n", "2", target])


def traceroute_target(target: str) -> str:
    return run_command(["tracert", "-d", "-h", "10", target])


def run(args):
    pieces = [header("Network Connectivity Diagnostics")]

    pieces.append(section("DNS Resolution"))
    pieces.append(resolve_host("www.microsoft.com"))
    pieces.append(resolve_host("1.1.1.1"))

    pieces.append(section("Ping Tests"))
    pieces.append(ping_target("8.8.8.8"))
    pieces.append(ping_target("www.microsoft.com"))

    pieces.append(section("Traceroute"))
    pieces.append(traceroute_target("www.microsoft.com"))

    pieces.append(section("Listening Connections"))
    try:
        net_connections = psutil.net_connections(kind="inet")
        listeners = [conn for conn in net_connections if conn.status == "LISTEN" or conn.status == "LISTENING"]
        for conn in listeners[:20]:
            pieces.append(
                f"{conn.laddr.ip}:{conn.laddr.port} -> {conn.raddr.ip if conn.raddr else '-'}:{conn.raddr.port if conn.raddr else '-'} {conn.status} PID {conn.pid}"
            )
        if not listeners:
            pieces.append("No listening connections detected.")
    except Exception as exc:
        pieces.append(f"Failed to enumerate network listeners: {exc}")

    return "\n".join(pieces)
