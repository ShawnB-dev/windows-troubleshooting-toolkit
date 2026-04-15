import argparse
import sys
from . import __version__
from .commands import (
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
    report,
)

COMMANDS = {
    "system": system.run,
    "system-integrity": system_integrity.run,
    "disk-health": disk_health.run,
    "network": network.run,
    "connectivity": connectivity.run,
    "firewall": firewall.run,
    "processes": processes.run,
    "services": services.run,
    "startup": startup.run,
    "installed": installed.run,
    "security": security.run,
    "audit": audit.run,
    "hardware": hardware.run,
    "performance": performance.run,
    "eventlogs": eventlogs.run,
    "report": report.run,
}


def create_parser():
    parser = argparse.ArgumentParser(
        description="Windows Troubleshooting Toolkit",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("command", choices=COMMANDS.keys(), help="Toolkit command to run")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--output", help="Path to save a text report")
    parser.add_argument("--verbose", action="store_true", help="Show verbose diagnostics")
    return parser


def main(argv=None):
    argv = argv or sys.argv[1:]
    parser = create_parser()
    args = parser.parse_args(argv)

    command = COMMANDS[args.command]
    output = command(args)

    if args.output and output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(output)
        print(f"Saved report to {args.output}")
    elif output:
        print(output)
