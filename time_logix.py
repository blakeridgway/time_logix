import tkinter as tk
from tkinter import ttk
import time
import datetime
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import sys  # Import the sys module


class TimeLogix:
    def __init__(self, root):
        self.root = root
        self.root.title("TimeLogix Application")

        # Styling
        self.bg_color = "#f0f0f0"  # Light gray background
        self.font_family = "Segoe UI"  # Modern font
        self.font_size = 10
        self.button_bg = "#4CAF50"  # Green button background
        self.button_fg = "white"  # White button text
        self.button_width = 15  # Consistent button width

        self.root.configure(bg=self.bg_color)

        style = ttk.Style()
        style.configure(
            "TLabel", background=self.bg_color, font=(self.font_family, self.font_size)
        )
        style.configure(
            "TButton",
            background=self.button_bg,
            foreground=self.button_fg,
            font=(self.font_family, self.font_size),
            padding=5,
            width=self.button_width,  # Set button width here
        )
        style.configure(
            "TCombobox", background="white", font=(self.font_family, self.font_size)
        )
        style.configure(
            "TEntry", background="white", font=(self.font_family, self.font_size)
        )
        style.configure("My.TFrame", background=self.bg_color)  # Frame style

        self.is_running = False
        self.start_time = None
        self.elapsed_time = 0
        self.timer_id = None
        self.log_entries = []
        self.project_file = "projects.txt"
        self.projects = self.load_projects()
        self.invoice_number = 1
        self.company_name = "Your Company Name"
        self.company_address = "123 Main St, Anytown, USA"
        self.client_name = "Client Name"
        self.client_address = "Client Address"
        self.hourly_rate = 60.00

        # UI elements
        self.task_label = ttk.Label(root, text="Task Description:")
        self.task_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.task_entry = ttk.Entry(root, width=40)
        self.task_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)

        self.project_label = ttk.Label(root, text="Project:")
        self.project_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.project_combo = ttk.Combobox(root, values=self.projects)
        self.project_combo.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        if self.projects:
            self.project_combo.set(self.projects[0])

        self.time_label = ttk.Label(
            root, text="00:00:00", font=(self.font_family, 36)
        )  # Larger time
        self.time_label.grid(row=2, column=0, columnspan=2, pady=15)

        self.start_stop_button = ttk.Button(
            root, text="Start", command=self.toggle_timer
        )
        self.start_stop_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.log_label = ttk.Label(root, text="Log Entries:")
        self.log_label.grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)

        self.log_text = tk.Text(
            root,
            height=10,
            width=50,
            bg="white",
            font=(self.font_family, self.font_size),
        )
        self.log_text.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        # Add Project UI
        self.new_project_label = ttk.Label(root, text="New Project:")
        self.new_project_label.grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)
        self.new_project_entry = ttk.Entry(root, width=30)
        self.new_project_entry.grid(row=6, column=1, sticky=tk.W, padx=10, pady=5)

        self.add_project_button = ttk.Button(
            root, text="Add Project", command=self.add_project
        )
        self.add_project_button.grid(row=7, column=0, columnspan=2, pady=5)

        # Button Grouping
        button_frame = ttk.Frame(root, padding=10, style="My.TFrame")
        button_frame.grid(row=8, column=0, columnspan=2, pady=10)

        self.export_csv_button = ttk.Button(
            button_frame, text="Export to CSV", command=self.export_to_csv
        )
        self.export_csv_button.grid(row=0, column=0, padx=5, pady=5)

        self.export_pdf_button = ttk.Button(
            button_frame, text="Export to PDF", command=self.export_to_pdf
        )
        self.export_pdf_button.grid(row=0, column=1, padx=5, pady=5)

        self.exit_button = ttk.Button(  # Create Exit button
            button_frame, text="Exit", command=self.exit_app
        )
        self.exit_button.grid(row=0, column=2, padx=5, pady=5)  # Place in button_frame

        self.total_time_button = ttk.Button(
            root,
            text="Calculate Total Time",
            command=self.calculate_total_time,
            width=20,  # Set specific width for this button
        )
        self.total_time_button.grid(row=9, column=0, columnspan=2, pady=5)

        self.total_time_label = ttk.Label(root, text="Total Time: 00:00:00")
        self.total_time_label.grid(row=10, column=0, columnspan=2, pady=5)

        # Settings UI
        self.company_name_label = ttk.Label(root, text="Company Name:")
        self.company_name_label.grid(row=11, column=0, sticky=tk.W, padx=10, pady=5)
        self.company_name_entry = ttk.Entry(root, width=30)
        self.company_name_entry.grid(row=11, column=1, sticky=tk.W, padx=10, pady=5)
        self.company_name_entry.insert(0, self.company_name)

        self.company_address_label = ttk.Label(root, text="Company Address:")
        self.company_address_label.grid(row=12, column=0, sticky=tk.W, padx=10, pady=5)
        self.company_address_entry = ttk.Entry(root, width=30)
        self.company_address_entry.grid(row=12, column=1, sticky=tk.W, padx=10, pady=5)
        self.company_address_entry.insert(0, self.company_address)

        self.client_name_label = ttk.Label(root, text="Client Name:")
        self.client_name_label.grid(row=13, column=0, sticky=tk.W, padx=10, pady=5)
        self.client_name_entry = ttk.Entry(root, width=30)
        self.client_name_entry.grid(row=13, column=1, sticky=tk.W, padx=10, pady=5)
        self.client_name_entry.insert(0, self.client_name)

        self.client_address_label = ttk.Label(root, text="Client Address:")
        self.client_address_label.grid(row=14, column=0, sticky=tk.W, padx=10, pady=5)
        self.client_address_entry = ttk.Entry(root, width=30)
        self.client_address_entry.grid(row=14, column=1, sticky=tk.W, padx=10, pady=5)
        self.client_address_entry.insert(0, self.client_address)

        self.hourly_rate_label = ttk.Label(root, text="Hourly Rate:")
        self.hourly_rate_label.grid(row=15, column=0, sticky=tk.W, padx=10, pady=5)
        self.hourly_rate_entry = ttk.Entry(root, width=10)
        self.hourly_rate_entry.grid(row=15, column=1, sticky=tk.W, padx=10, pady=5)
        self.hourly_rate_entry.insert(0, str(self.hourly_rate))

        self.update_settings_button = ttk.Button(
            root, text="Update Settings", command=self.update_settings
        )
        self.update_settings_button.grid(row=16, column=0, columnspan=2, pady=10)

        # Configure grid weights to make the layout expand
        for i in range(17):
            root.grid_rowconfigure(i, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

    def load_projects(self):
        try:
            with open(self.project_file, "r") as f:
                projects = [line.strip() for line in f]
            return projects
        except FileNotFoundError:
            return []

    def save_projects(self):
        try:
            with open(self.project_file, "w") as f:
                for project in self.projects:
                    f.write(project + "\n")
        except Exception as e:
            print(f"Error saving projects: {e}")

    def add_project(self):
        new_project = self.new_project_entry.get().strip()
        if new_project and new_project not in self.projects:
            self.projects.append(new_project)
            self.project_combo["values"] = self.projects  # Update Combobox
            self.project_combo.set(new_project)  # Set to the new project
            self.save_projects()
            self.new_project_entry.delete(0, tk.END)  # Clear the entry
        elif new_project in self.projects:
            print("Project already exists.")  # Replace with a GUI message box
        else:
            print("Project name cannot be empty.")  # Replace with a GUI message box

    def update_settings(self):
        self.company_name = self.company_name_entry.get()
        self.company_address = self.company_address_entry.get()
        self.client_name = self.client_name_entry.get()
        self.client_address = self.client_address_entry.get()
        try:
            self.hourly_rate = float(self.hourly_rate_entry.get())
        except ValueError:
            print("Invalid hourly rate.  Using default.")  # Replace with GUI message
            self.hourly_rate = 50.00  # Revert to default, or handle the error

        # OPTIONAL: Save settings to a file here (e.g., JSON)

    def toggle_timer(self):
        if self.is_running:
            self.stop_timer()
        else:
            self.start_timer()

    def start_timer(self):
        self.is_running = True
        self.start_stop_button.config(text="Stop")
        self.start_time = time.time()
        self.update_timer()

    def stop_timer(self):
        self.is_running = False
        self.start_stop_button.config(text="Start")
        self.root.after_cancel(self.timer_id)
        self.log_time_entry()

    def update_timer(self):
        if self.is_running:
            self.elapsed_time = time.time() - self.start_time
            minutes, seconds = divmod(self.elapsed_time, 60)
            hours, minutes = divmod(minutes, 60)
            time_str = "{:02d}:{:02d}:{:02d}".format(
                int(hours), int(minutes), int(seconds)
            )
            self.time_label.config(text=time_str)
            self.timer_id = self.root.after(100, self.update_timer)

    def log_time_entry(self):
        end_time = datetime.datetime.now()
        task_description = self.task_entry.get()
        project = self.project_combo.get()
        duration = self.elapsed_time
        start_time_str = end_time - datetime.timedelta(seconds=duration)

        entry = {
            "task": task_description,
            "project": project,
            "start_time": start_time_str.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration": round(duration, 2),
        }
        self.log_entries.append(entry)
        self.update_log_display()
        self.elapsed_time = 0
        self.time_label.config(text="00:00:00")

    def update_log_display(self):
        self.log_text.delete("1.0", tk.END)
        for entry in self.log_entries:
            self.log_text.insert(tk.END, f"Task: {entry['task']}\n")
            self.log_text.insert(tk.END, f"Project: {entry['project']}\n")
            self.log_text.insert(tk.END, f"Start: {entry['start_time']}\n")
            self.log_text.insert(tk.END, f"End: {entry['end_time']}\n")
            self.log_text.insert(tk.END, f"Duration: {entry['duration']} seconds\n")
            self.log_text.insert(tk.END, "-" * 20 + "\n")

    def export_to_csv(self):
        try:
            with open("time_entries.csv", "w", newline="") as csvfile:
                fieldnames = ["task", "project", "start_time", "end_time", "duration"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for entry in self.log_entries:
                    writer.writerow(entry)
            print("Exported to CSV successfully!")
        except Exception as e:
            print(f"Error exporting to CSV: {e}")

    def export_to_pdf(self):
        try:
            filename = f"invoice_{self.invoice_number}.pdf"
            c = canvas.Canvas(filename, pagesize=letter)
            styles = getSampleStyleSheet()

            # --- Header ---
            c.setFont("Helvetica-Bold", 16)
            c.drawString(inch, 7.5 * inch, self.company_name)
            c.setFont("Helvetica", 10)
            c.drawString(inch, 7.3 * inch, self.company_address)

            c.setFont("Helvetica-Bold", 12)
            c.drawString(4.5 * inch, 7.5 * inch, "Invoice")
            c.setFont("Helvetica", 10)
            c.drawString(
                4.5 * inch, 7.3 * inch, f"Invoice Number: {self.invoice_number}"
            )
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            c.drawString(4.5 * inch, 7.1 * inch, f"Date: {current_date}")

            # --- Client Info ---
            c.setFont("Helvetica-Bold", 12)
            c.drawString(inch, 6.5 * inch, "Bill To:")
            c.setFont("Helvetica", 10)
            c.drawString(inch, 6.3 * inch, self.client_name)
            c.drawString(inch, 6.1 * inch, self.client_address)

            # --- Table ---
            data = [["Task", "Project", "Hours", "Rate", "Total"]]
            total_amount = 0

            for entry in self.log_entries:
                hours = entry["duration"] / 3600
                line_total = hours * self.hourly_rate
                total_amount += line_total
                data.append(
                    [
                        entry["task"],
                        entry["project"],
                        f"{hours:.2f}",
                        f"${self.hourly_rate:.2f}",
                        f"${line_total:.2f}",
                    ]
                )

            table = Table(data, colWidths=[1.5 * inch, 1.5 * inch, inch, inch, inch])
            style = TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
            table.setStyle(style)
            table.wrapOn(c, letter[0] - 2 * inch, letter[1] - 2 * inch)
            table.drawOn(c, inch, 4 * inch)

            # --- Totals ---
            c.setFont("Helvetica-Bold", 12)
            c.drawString(4 * inch, 3.5 * inch, "Subtotal:")
            c.setFont("Helvetica", 12)
            c.drawRightString(5.5 * inch, 3.5 * inch, f"${total_amount:.2f}")

            c.setFont("Helvetica-Bold", 12)
            c.drawString(4 * inch, 3.3 * inch, "Tax (0%):")
            c.setFont("Helvetica", 12)
            c.drawRightString(5.5 * inch, 3.3 * inch, "$0.00")

            c.setFont("Helvetica-Bold", 12)
            c.drawString(4 * inch, 3.1 * inch, "Total:")
            c.setFont("Helvetica", 12)
            c.drawRightString(5.5 * inch, 3.1 * inch, f"${total_amount:.2f}")

            # --- Notes ---
            c.setFont("Helvetica", 10)
            c.drawString(inch, 2 * inch, "Notes:")
            c.drawString(inch, 1.8 * inch, "Thank you for your business!")

            c.save()
            print(f"Exported to PDF successfully as {filename}!")
            self.invoice_number += 1

        except Exception as e:
            print(f"Error exporting to PDF: {e}")

    def calculate_total_time(self):
        total_seconds = sum(entry["duration"] for entry in self.log_entries)
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        time_str = "{:02d}:{:02d}:{:02d}".format(
            int(hours), int(minutes), int(seconds)
        )
        self.total_time_label.config(text=f"Total Time: {time_str}")

    def exit_app(self):  # Define the exit_app method
        self.root.destroy()  # Close the Tkinter window
        sys.exit()


if __name__ == "__main__":
    root = tk.Tk()
    app = TimeLogix(root)
    root.mainloop()
