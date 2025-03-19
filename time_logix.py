import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import csv
import os

class TimeLogix(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Time Logix")
        self.geometry("450x350")

        self.start_time = None
        self.tracking = False
        self.sessions = []

        self.create_widgets()

    def create_widgets(self):
        self.status_label = tk.Label(self, text="Status: Not Tracking", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

        self.start_button = tk.Button(
            self, text="Start Tracking", width=20, command=self.start_tracking
        )
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(
            self, text="Stop Tracking", width=20, command=self.stop_tracking, state=tk.DISABLED
        )
        self.stop_button.pack(pady=5)

        self.export_button = tk.Button(
            self, text="Export Sessions", width=20, command=self.export_sessions
        )
        self.export_button.pack(pady=5)

        self.log_text = tk.Text(self, height=10, state=tk.DISABLED)
        self.log_text.pack(pady=10, padx=10, fill='both', expand=True)

    def log_message(self, message):
        """Append message to the log text widget."""
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.configure(state=tk.DISABLED)
        self.log_text.see(tk.END)

    def start_tracking(self):
        if self.tracking:
            messagebox.showwarning("Warning", "Already tracking!")
            return

        self.start_time = datetime.now()
        self.tracking = True
        self.status_label.config(
            text=f"Status: Tracking started at {self.start_time.strftime('%H:%M:%S')}"
        )
        self.log_message(f"Started at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_tracking(self):
        if not self.tracking:
            messagebox.showwarning("Warning", "Not currently tracking!")
            return

        end_time = datetime.now()
        duration = end_time - self.start_time
        self.sessions.append((self.start_time, end_time, duration))
        self.tracking = False
        self.status_label.config(text="Status: Not Tracking")
        decimal_hours = self.get_decimal_hours(duration)
        self.log_message(
            f"Stopped at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}, Duration: {self.format_duration(duration)} "
            f"({decimal_hours:.2f} hours)"
        )
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def format_duration(self, duration):
        """Format duration as H:MM:SS"""
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours}:{minutes:02d}:{seconds:02d}"

    def get_decimal_hours(self, duration):
        """Convert a timedelta duration to decimal hours."""
        total_hours = duration.total_seconds() / 3600
        return total_hours

    def export_sessions(self):
        if not self.sessions:
            messagebox.showinfo("Info", "No sessions to export.")
            return

        filename = "working_sessions.csv"
        try:
            file_exists = os.path.isfile(filename)
            with open(filename, mode="a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow([
                        "Start Time", "End Time", 
                        "Duration (H:MM:SS)", "Decimal Hours"
                    ])
                for session in self.sessions:
                    start, end, duration = session
                    writer.writerow([
                        start.strftime("%Y-%m-%d %H:%M:%S"),
                        end.strftime("%Y-%m-%d %H:%M:%S"),
                        self.format_duration(duration),
                        f"{self.get_decimal_hours(duration):.2f}"
                    ])
            messagebox.showinfo("Export Successful", f"Sessions exported to {filename}")
            self.sessions.clear()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {e}")

if __name__ == "__main__":
    app = TimeLogix()
    app.mainloop()
