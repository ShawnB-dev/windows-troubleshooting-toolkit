from .util import header, section
import psutil


def run(args):
    pieces = [header("Network Diagnostics")]
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    for iface, addresses in addrs.items():
        pieces.append(section(f"Interface: {iface}"))
        stat = stats.get(iface)
        if stat:
            pieces.append(f"Status: {'up' if stat.isup else 'down'}")
            pieces.append(f"Speed: {stat.speed}Mbps")
            pieces.append(f"MTU: {stat.mtu}")

        for address in addresses:
            pieces.append(f"{address.family.name}: {address.address}")
            if address.netmask:
                pieces.append(f"Netmask: {address.netmask}")
            if address.broadcast:
                pieces.append(f"Broadcast: {address.broadcast}")
            if address.ptp:
                pieces.append(f"PTP: {address.ptp}")

    net_io = psutil.net_io_counters()
    pieces.append(section("IO Counters"))
    pieces.append(f"Bytes Sent: {net_io.bytes_sent}")
    pieces.append(f"Bytes Received: {net_io.bytes_recv}")
    pieces.append(f"Packets Sent: {net_io.packets_sent}")
    pieces.append(f"Packets Received: {net_io.packets_recv}")

    return "\n".join(pieces)
