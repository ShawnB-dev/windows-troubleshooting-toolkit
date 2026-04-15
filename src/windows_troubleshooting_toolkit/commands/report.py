from .util import header
from . import (
    system,
    system_integrity,
    disk_health,
    network,
    connectivity,
    firewall,
    processes,
    services,
    startup,
    installed,
    security,
    audit,
    hardware,
    performance,
    eventlogs,
)


def run(args):
    pieces = [header("Windows Troubleshooting Toolkit Report")]
    pieces.extend([
        system.run(args),
        system_integrity.run(args),
        disk_health.run(args),
        network.run(args),
        connectivity.run(args),
        firewall.run(args),
        processes.run(args),
        services.run(args),
        startup.run(args),
        installed.run(args),
        security.run(args),
        audit.run(args),
        hardware.run(args),
        performance.run(args),
        eventlogs.run(args),
    ])
    return "\n".join(pieces)
