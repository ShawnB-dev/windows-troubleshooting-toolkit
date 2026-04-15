from .util import header, section, run_command


def run(args):
    pieces = [header("Security Diagnostics")]

    pieces.append(section("Windows Defender / Security Status"))
    pieces.append(run_command([
        "powershell",
        "-NoProfile",
        "-Command",
        "Try { Get-MpComputerStatus | Select-Object AMServiceEnabled, AntivirusEnabled, RealTimeProtectionEnabled, NISEnabled | Format-List } Catch { Write-Error $_.Exception.Message }"
    ]))

    pieces.append(section("UAC & Secure Boot"))
    pieces.append(run_command([
        "powershell",
        "-NoProfile",
        "-Command",
        "Try { $uac = Get-ItemProperty HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System; [PSCustomObject]@{EnableLUA=$uac.EnableLUA; ConsentPromptBehaviorAdmin=$uac.ConsentPromptBehaviorAdmin; PromptOnSecureDesktop=$uac.PromptOnSecureDesktop} | Format-List } Catch { Write-Error $_.Exception.Message }"
    ]))
    pieces.append(run_command([
        "powershell",
        "-NoProfile",
        "-Command",
        "Try { Confirm-SecureBootUEFI } Catch { Write-Error $_.Exception.Message }"
    ]))

    return "\n".join(pieces)
