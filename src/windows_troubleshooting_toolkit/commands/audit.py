from .util import header, section, run_command


def run(args):
    pieces = [header("Audit & Event Diagnostics")]

    pieces.append(section("Recent Security Errors and Warnings"))
    pieces.append(run_command([
        "wevtutil",
        "qe",
        "Security",
        "/c:20",
        "/f:text",
        "/q:*[System[(Level=2 or Level=3)]]"
    ]))

    pieces.append(section("User Session History"))
    pieces.append(run_command(["query", "user"]))

    return "\n".join(pieces)
