import winreg
from .util import header, section

UNINSTALL_PATHS = [
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
]


def read_installed_programs():
    programs = []
    for root, path in UNINSTALL_PATHS:
        try:
            with winreg.OpenKey(root, path) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            version = winreg.QueryValueEx(subkey, "DisplayVersion")[0] if winreg.QueryInfoKey(subkey)[1] else ""
                            programs.append(f"{name} {version}".strip())
                    except FileNotFoundError:
                        continue
                    except OSError:
                        continue
        except FileNotFoundError:
            continue
    return sorted(set(programs))


def run(args):
    pieces = [header("Installed Programs")]
    programs = read_installed_programs()
    if programs:
        for program in programs[:50]:
            pieces.append(program)
        if len(programs) > 50:
            pieces.append(f"...and {len(programs) - 50} more installed programs.")
    else:
        pieces.append("No installed programs found in the registry.")
    return "\n".join(pieces)
