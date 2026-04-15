from .util import header, section
import psutil


def run(args):
    pieces = [header("Windows Service Diagnostics")]
    try:
        services = psutil.win_service_iter()
        pieces.append(section("Services"))
        for svc in services:
            pieces.append(f"{svc.name():30} Status: {svc.status():<10} Startup: {svc.start_type()}")
    except AttributeError:
        pieces.append("Windows service inspection is only supported on Windows.")
    except Exception as exc:
        pieces.append(f"Failed to enumerate services: {exc}")
    return "\n".join(pieces)
