from .util import header, section

try:
    import win32evtlog
except ImportError:
    win32evtlog = None


def run(args):
    pieces = [header("Windows Event Log Summary")]
    if win32evtlog is None:
        pieces.append("pywin32 is required for event log access. Install with 'python -m pip install pywin32'.")
        return "\n".join(pieces)

    logs = ["System", "Application", "Security"]
    for log_name in logs:
        pieces.append(section(f"{log_name} Log"))
        try:
            handle = win32evtlog.OpenEventLog(None, log_name)
            total = win32evtlog.GetNumberOfEventLogRecords(handle)
            pieces.append(f"Total records: {total}")
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            events = win32evtlog.ReadEventLog(handle, flags, 0)
            count = 0
            for event in events:
                pieces.append(f"Record {event.RecordNumber}: {event.EventType} {event.TimeGenerated.Format()}")
                count += 1
                if count >= 5:
                    break
        except Exception as exc:
            pieces.append(f"Unable to read {log_name} log: {exc}")
    return "\n".join(pieces)
