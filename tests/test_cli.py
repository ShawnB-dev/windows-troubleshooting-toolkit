import subprocess
import sys
import os


def test_cli_help():
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.join(os.path.dirname(__file__), "..", "src")
    result = subprocess.run([sys.executable, "-m", "windows_troubleshooting_toolkit", "system"], capture_output=True, text=True, env=env)
    assert result.returncode == 0
    assert "System Diagnostics" in result.stdout
