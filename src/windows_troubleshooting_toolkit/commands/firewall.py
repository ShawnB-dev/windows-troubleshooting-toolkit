from .util import header, section, run_command


def run(args):
    pieces = [header("Firewall Diagnostics")]

    pieces.append(section("Firewall Profiles"))
    pieces.append(run_command(["netsh", "advfirewall", "show", "allprofiles"]))

    pieces.append(section("Firewall Rules"))
    pieces.append(run_command(["netsh", "advfirewall", "firewall", "show", "rule", "name=all"]))

    pieces.append(section("Listening Ports"))
    pieces.append(run_command(["netstat", "-ano"]))

    return "\n".join(pieces)
