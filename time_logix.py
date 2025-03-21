import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import csv
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

class TimeLogix(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TimeLogix")
        self.geometry("500x500")

        self.start_time = None
        self.tracking = False
        self.sessions = []
        self.total_hours = 0

        self.create_widgets()
        self.load_sessions_from_csv()
        self.update_total_hours()

    def create_widgets(self):
        self.status_label = tk.Label(self, text="Status: Not Tracking", font=("Helvetica", 12))
        self.status_label.pack(pady=5)

        self.start_button = tk.Button(
            self, text="Start Tracking", width=20, command=self.start_tracking
        )
        self.start_button.pack(pady=2)

        self.stop_button = tk.Button(
            self, text="Stop Tracking", width=20, command=self.stop_tracking, state=tk.DISABLED
        )
        self.stop_button.pack(pady=2)

        self.description_label = tk.Label(self, text="Work Description:")
        self.description_label.pack(pady=1)
        self.description_entry = tk.Text(self, height=3, width=40)
        self.description_entry.pack(pady=1)

        self.export_csv_button = tk.Button(
            self, text="Export to CSV", width=20, command=self.export_sessions_csv
        )
        self.export_csv_button.pack(pady=2)

        self.export_pdf_button = tk.Button(
            self, text="Export to PDF", width=20, command=self.export_sessions_pdf
        )
        self.export_pdf_button.pack(pady=2)

        self.total_hours_label = tk.Label(self, text="Total Hours Worked: 0.00", font=("Helvetica", 12))
        self.total_hours_label.pack(pady=5)

        self.log_text = tk.Text(self, height=10, state=tk.DISABLED)
        self.log_text.pack(pady=5, padx=10, fill='both', expand=True)
        
        self.exit_button = tk.Button(
        self, text="Exit", width=10, command=self.exit_app
        )
        self.exit_button.pack(pady=5)

    def log_message(self, message):
        if hasattr(self, 'log_text'):
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
        description = self.description_entry.get("1.0", tk.END).strip()
        self.sessions.append((self.start_time, end_time, duration, description))
        self.tracking = False
        self.status_label.config(text="Status: Not Tracking")
        decimal_hours = self.get_decimal_hours(duration)
        self.log_message(
            f"Stopped at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}, Duration: {self.format_duration(duration)} "
            f"({decimal_hours:.2f} hours), Description: {description}"
        )
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.description_entry.delete("1.0", tk.END)

        self.update_total_hours()

    def format_duration(self, duration):
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours}:{minutes:02d}:{seconds:02d}"

    def get_decimal_hours(self, duration):
        total_hours = duration.total_seconds() / 3600
        return total_hours

    def export_sessions_csv(self):
        if not self.sessions:
            messagebox.showinfo("Info", "No sessions to export.")
            return

        filename = "working_sessions.csv"
        try:
            with open(filename, mode="w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    "Start Time", "End Time",
                    "Duration (H:MM:SS)", "Decimal Hours", "Description"
                ])
                for start, end, duration, description in self.sessions:
                    writer.writerow([
                        start.strftime("%Y-%m-%d %H:%M:%S"),
                        end.strftime("%Y-%m-%d %H:%M:%S"),
                        self.format_duration(duration),
                        f"{self.get_decimal_hours(duration):.2f}",
                        description
                    ])
                writer.writerow(["", "", "", "Total Hours", f"{self.total_hours:.2f}"])
            messagebox.showinfo("Export Successful", f"Sessions exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {e}")

    def export_sessions_pdf(self):
        if not self.sessions:
            messagebox.showinfo("Info", "No sessions to export.")
            return

        filename = "working_sessions.pdf"
        try:
            doc = SimpleDocTemplate(filename, pagesize=letter)
            elements = []

            data = [
                ["Start Time", "End Time", "Duration (H:MM:SS)", "Decimal Hours", "Description"]
            ]
            for start, end, duration, description in self.sessions:
                data.append([
                    start.strftime("%Y-%m-%d %H:%M:%S"),
                    end.strftime("%Y-%m-%d %H:%M:%S"),
                    self.format_duration(duration),
                    f"{self.get_decimal_hours(duration):.2f}",
                    description
                ])

            data.append(["", "", "", "Total Hours", f"{self.total_hours:.2f}"])

            table = Table(data)
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])
            table.setStyle(style)
            elements.append(table)

            doc.build(elements)
            messagebox.showinfo("Export Successful", f"Sessions exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {e}")

    def load_sessions_from_csv(self):
        filename = "working_sessions.csv"
        if os.path.exists(filename):
            try:
                with open(filename, mode="r") as csvfile:
                    reader = csv.reader(csvfile)
                    header = next(reader, None)

                    for row in reader:
                        if len(row) == 5:
                            start_time_str, end_time_str, duration_str, decimal_hours_str, description = row
                        elif len(row) == 4:
                            start_time_str, end_time_str, duration_str, decimal_hours_str = row
                            description = ""
                        else:
                            print(f"Skipping row with unexpected number of columns: {len(row)}")
                            continue

                        try:
                            start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
                            end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
                            duration = self.parse_duration(duration_str)
                            self.sessions.append((start_time, end_time, duration, description))
                            self.log_message(
                                f"Loaded: {start_time.strftime('%Y-%m-%d %H:%M:%S')} - {end_time.strftime('%Y-%m-%d %H:%M:%S')}, "
                                f"Duration: {duration_str}, Description: {description}"
                            )
                        except ValueError as ve:
                            print(f"Skipping row due to parsing error: {ve}")
            except FileNotFoundError:
                messagebox.showinfo("Info", "No CSV file found. Starting with a new session.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load sessions from CSV: {e}")

    def parse_duration(self, duration_str):
        hours, minutes, seconds = map(int, duration_str.split(':'))
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def update_total_hours(self):
        total_duration = timedelta()
        for start, end, duration, description in self.sessions:
            total_duration += duration

        self.total_hours = total_duration.total_seconds() / 3600
        self.total_hours_label.config(text=f"Total Hours Worked: {self.total_hours:.2f}")

    def exit_app(self):
        self.destroy()

if __name__ == "__main__":
    app = TimeLogix()
    app.mainloop()
