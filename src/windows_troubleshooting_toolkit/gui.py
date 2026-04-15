import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
from . import cli
from .commands import (
    system, system_integrity, disk_health, network, connectivity, firewall,
    processes, services, startup, installed, security, audit, hardware,
    performance, eventlogs, report
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

class WindowsTroubleshootingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows Troubleshooting Toolkit")
        self.root.geometry("900x700")
        self.current_output = ""
        self.running = False

        self.setup_ui()

    def setup_ui(self):
        # Top frame for controls
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)

        # Command selection
        ttk.Label(control_frame, text="Select Diagnostic:").pack(side=tk.LEFT, padx=5)
        
        self.command_var = tk.StringVar(value="report")
        command_combo = ttk.Combobox(
            control_frame,
            textvariable=self.command_var,
            values=list(COMMANDS.keys()),
            state="readonly",
            width=25
        )
        command_combo.pack(side=tk.LEFT, padx=5)

        # Verbose checkbox
        self.verbose_var = tk.BooleanVar()
        verbose_check = ttk.Checkbutton(
            control_frame,
            text="Verbose Output",
            variable=self.verbose_var
        )
        verbose_check.pack(side=tk.LEFT, padx=5)

        # Run button
        run_button = ttk.Button(control_frame, text="Run Diagnostic", command=self.run_diagnostic)
        run_button.pack(side=tk.LEFT, padx=5)

        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(control_frame, textvariable=self.status_var, foreground="blue")
        status_label.pack(side=tk.LEFT, padx=10)

        # Middle frame for output
        output_frame = ttk.LabelFrame(self.root, text="Diagnostic Output", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Text display
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            height=20,
            font=("Courier", 9)
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # Bottom frame for export
        export_frame = ttk.Frame(self.root, padding="10")
        export_frame.pack(fill=tk.X)

        export_button = ttk.Button(export_frame, text="Export to File", command=self.export_results)
        export_button.pack(side=tk.LEFT, padx=5)

        copy_button = ttk.Button(export_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_button.pack(side=tk.LEFT, padx=5)

        clear_button = ttk.Button(export_frame, text="Clear Output", command=self.clear_output)
        clear_button.pack(side=tk.LEFT, padx=5)

    def run_diagnostic(self):
        if self.running:
            messagebox.showwarning("Already Running", "A diagnostic is already running. Please wait.")
            return

        command = self.command_var.get()
        self.running = True
        self.status_var.set("Running...")
        self.output_text.delete(1.0, tk.END)

        # Run diagnostic in a separate thread to keep UI responsive
        thread = threading.Thread(target=self._run_in_thread, args=(command,))
        thread.daemon = True
        thread.start()

    def _run_in_thread(self, command):
        try:
            # Create a simple args object
            class Args:
                verbose = self.verbose_var.get()
                output = None

            args = Args()
            func = COMMANDS[command]
            result = func(args)
            self.current_output = result or ""

            # Update UI from main thread
            self.root.after(0, self._update_output, self.current_output)
        except Exception as exc:
            error_msg = f"Error running {command}: {exc}"
            self.root.after(0, self._update_output, error_msg)
        finally:
            self.running = False
            self.root.after(0, lambda: self.status_var.set("Ready"))

    def _update_output(self, text):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(1.0, text)

    def export_results(self):
        if not self.current_output:
            messagebox.showwarning("No Output", "Run a diagnostic first to export results.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="diagnostic_report.txt"
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.current_output)
                messagebox.showinfo("Success", f"Report saved to {file_path}")
            except Exception as exc:
                messagebox.showerror("Error", f"Failed to save file: {exc}")

    def copy_to_clipboard(self):
        if not self.current_output:
            messagebox.showwarning("No Output", "Run a diagnostic first to copy results.")
            return

        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.current_output)
            messagebox.showinfo("Success", "Output copied to clipboard")
        except Exception as exc:
            messagebox.showerror("Error", f"Failed to copy to clipboard: {exc}")

    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
        self.current_output = ""


def run_gui():
    root = tk.Tk()
    app = WindowsTroubleshootingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
