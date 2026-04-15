import subprocess
import sys
import os

def launch_in_new_window(toolkit_command="system"):
    """
    Launches a specific toolkit diagnostic in a new, separate PowerShell window.
    The '-NoExit' flag is used so you can inspect the output after completion.
    """
    # Resolve the project structure
    project_root = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(project_root, "src")

    # Prepare the environment variables
    env = os.environ.copy()
    env["PYTHONPATH"] = src_path

    # Build the PowerShell command
    # We use -NoExit to keep the window open for review
    ps_args = [
        "powershell.exe",
        "-NoExit",
        "-Command",
        f"& '{sys.executable}' -m windows_troubleshooting_toolkit {toolkit_command}"
    ]

    print(f"Spawning new PowerShell instance for: {toolkit_command}")
    subprocess.Popen(ps_args, env=env, creationflags=subprocess.CREATE_NEW_CONSOLE)

if __name__ == "__main__":
    # Usage: python launch_separate.py [command_name]
    target = sys.argv[1] if len(sys.argv) > 1 else "system"
    launch_in_new_window(target)