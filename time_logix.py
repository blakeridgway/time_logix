import customtkinter as ctk
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
import sys
import os


class TimeLogix:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("TimeLogix")

        # Theme Configuration
        ctk.set_appearance_mode("Dark")  # Or "Light", "System"
        ctk.set_default_color_theme("blue")

        # --- Styling ---
        self.font_family = "Segoe UI"
        self.font_size = 12

        # --- App Data ---
        self.project_file = "projects.txt"
        self.invoice_file = "invoice_number.txt"  # File to store invoice number
        self.projects = self.load_projects()
        self.is_running = False
        self.start_time = None
        self.elapsed_time = 0
        self.timer_id = None
        self.log_entries = []
        self.invoice_number = self.load_invoice_number()  # Load invoice number
        self.company_name = "Your Company Name"
        self.company_address = "123 Main St, Anytown, USA"
        self.client_name = "Client Name"
        self.client_address = "Client Address"
        self.hourly_rate = 60.00
        self.csv_file = "working_sessions.csv"

        # --- Scrollable Frame ---
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.root, width=450, height=600
        )  # Consider making height adaptable
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # --- UI Elements ---
        self.task_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Task Description:",
            font=(self.font_family, self.font_size),
        )
        self.task_label.pack(pady=(10, 2))

        self.task_entry = ctk.CTkEntry(self.scrollable_frame, width=250)
        self.task_entry.pack(pady=(2, 10))

        self.project_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Project:",
            font=(self.font_family, self.font_size),
        )
        self.project_label.pack(pady=(10, 2))

        self.project_combo = ctk.CTkComboBox(
            self.scrollable_frame, values=self.projects, width=250
        )
        self.project_combo.pack(pady=(2, 10))
        if self.projects:
            self.project_combo.set(self.projects[0])

        self.time_label = ctk.CTkLabel(
            self.scrollable_frame, text="00:00:00", font=(self.font_family, 36)
        )
        self.time_label.pack(pady=(15, 20))

        self.start_stop_button = ctk.CTkButton(
            self.scrollable_frame,
            text="Start",
            command=self.toggle_timer,
            corner_radius=8,
        )
        self.start_stop_button.pack(pady=(5, 20))

        self.log_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Log Entries:",
            font=(self.font_family, self.font_size),
        )
        self.log_label.pack(pady=(10, 2))

        self.log_text = ctk.CTkTextbox(
            self.scrollable_frame,
            width=400,
            height=100,
            font=(self.font_family, self.font_size),
        )
        self.log_text.pack(pady=5, padx=10, fill="both", expand=True)

        self.new_project_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="New Project:",
            font=(self.font_family, self.font_size),
        )
        self.new_project_label.pack(pady=(10, 2))

        self.new_project_entry = ctk.CTkEntry(self.scrollable_frame, width=250)
        self.new_project_entry.pack(pady=(2, 10))

        self.add_project_button = ctk.CTkButton(
            self.scrollable_frame,
            text="Add Project",
            command=self.add_project,
            corner_radius=8,
        )
        self.add_project_button.pack(pady=(5, 15))

        # --- Button Frame ---
        button_frame = ctk.CTkFrame(self.scrollable_frame)
        button_frame.pack(pady=(10, 15))

        self.export_csv_button = ctk.CTkButton(
            button_frame,
            text="Export to CSV",
            command=self.export_to_csv,
            corner_radius=8,
        )
        self.export_csv_button.pack(
            side="left", padx=5, pady=5
        )  # Using side="left" for horizontal layout

        self.export_pdf_button = ctk.CTkButton(
            button_frame,
            text="Export to PDF",
            command=self.export_to_pdf,
            corner_radius=8,
        )
        self.export_pdf_button.pack(side="left", padx=5, pady=5)

        self.exit_button = ctk.CTkButton(
            button_frame, text="Exit", command=self.exit_app, corner_radius=8
        )
        self.exit_button.pack(side="left", padx=5, pady=5)

        self.total_time_button = ctk.CTkButton(
            self.scrollable_frame,
            text="Calculate Total Time",
            command=self.calculate_total_time,
            corner_radius=8,
        )
        self.total_time_button.pack(pady=(5, 15))

        self.total_time_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Total Time: 00:00:00",
            font=(self.font_family, self.font_size),
        )
        self.total_time_label.pack(pady=(5, 15))

        # --- Settings UI ---
        self.company_name_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Company Name:",
            font=(self.font_family, self.font_size),
        )
        self.company_name_label.pack(pady=(10, 2))

        self.company_name_entry = ctk.CTkEntry(self.scrollable_frame, width=250)
        self.company_name_entry.pack(pady=(2, 10))

        self.company_address_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Company Address:",
            font=(self.font_family, self.font_size),
        )
        self.company_address_label.pack(pady=(10, 2))

        self.company_address_entry = ctk.CTkEntry(self.scrollable_frame, width=250)
        self.company_address_entry.pack(pady=(2, 10))

        self.client_name_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Client Name:",
            font=(self.font_family, self.font_size),
        )
        self.client_name_label.pack(pady=(10, 2))

        self.client_name_entry = ctk.CTkEntry(self.scrollable_frame, width=250)
        self.client_name_entry.pack(pady=(2, 10))

        self.client_address_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Client Address:",
            font=(self.font_family, self.font_size),
        )
        self.client_address_label.pack(pady=(10, 2))

        self.client_address_entry = ctk.CTkEntry(self.scrollable_frame, width=250)
        self.client_address_entry.pack(pady=(2, 10))

        self.hourly_rate_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Hourly Rate:",
            font=(self.font_family, self.font_size),
        )
        self.hourly_rate_label.pack(pady=(10, 2))

        self.hourly_rate_entry = ctk.CTkEntry(self.scrollable_frame, width=100)
        self.hourly_rate_entry.pack(pady=(2, 10))

        self.update_settings_button = ctk.CTkButton(
            self.scrollable_frame,
            text="Update Settings",
            command=self.update_settings,
            corner_radius=8,
        )
        self.update_settings_button.pack(pady=(15, 20))

        self.load_log_entries()

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

    def load_invoice_number(self):
        try:
            with open(self.invoice_file, "r") as f:
                return int(f.read().strip())
        except FileNotFoundError:
            return 1
        except ValueError:
            print("Invalid invoice number in file, resetting to 1.")
            return 1

    def save_invoice_number(self):
        try:
            with open(self.invoice_file, "w") as f:
                f.write(str(self.invoice_number))
        except Exception as e:
            print(f"Error saving invoice number: {e}")

    def add_project(self):
        new_project = self.new_project_entry.get().strip()
        if new_project and new_project not in self.projects:
            self.projects.append(new_project)
            self.project_combo.configure(values=self.projects)
            self.project_combo.set(new_project)
            self.save_projects()
            self.new_project_entry.delete(0, tk.END)
        elif new_project in self.projects:
            print("Project already exists.")
        else:
            print("Project name cannot be empty.")

    def update_settings(self):
        self.company_name = self.company_name_entry.get()
        self.company_address = self.company_address_entry.get()
        self.client_name = self.client_name_entry.get()
        self.client_address = self.client_address_entry.get()
        try:
            self.hourly_rate = float(self.hourly_rate_entry.get())
        except ValueError:
            print("Invalid hourly rate. Using default.")
            self.hourly_rate = 50.00

    def toggle_timer(self):
        if self.is_running:
            self.stop_timer()
        else:
            self.start_timer()

    def start_timer(self):
        self.is_running = True
        self.start_stop_button.configure(text="Stop")
        self.start_time = time.time()
        self.update_timer()

    def stop_timer(self):
        self.is_running = False
        self.start_stop_button.configure(text="Start")
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
            self.time_label.configure(text=time_str)
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
        self.time_label.configure(text="00:00:00")

    def update_log_display(self):
        self.log_text.delete("1.0", tk.END)
        for entry in self.log_entries:
            self.log_text.insert(tk.END, f"Task: {entry['task']}\n")
            self.log_text.insert(tk.END, f"Project: {entry['project']}\n")
            self.log_text.insert(tk.END, f"Start: {entry['start_time']}\n")
            self.log_text.insert(tk.END, f"End: {entry['end_time']}\n")
            self.log_text.insert(
                tk.END, f"Duration: {entry['duration']} seconds\n"
            )
            self.log_text.insert(tk.END, "-" * 20 + "\n")

    def load_log_entries(self):
        if os.path.exists(self.csv_file):
            try:
                with open(self.csv_file, "r") as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        try:
                            row["duration"] = float(row["duration"])
                        except ValueError:
                            # Try converting duration from hh:mm:ss format to seconds
                            try:
                                h, m, s = map(int, row["duration"].split(":"))
                                row["duration"] = h * 3600 + m * 60 + s
                            except ValueError:
                                print(
                                    f"Invalid duration format: {row['duration']}. "
                                    "Skipping this entry."
                                )
                                continue  # Skip this entry if the format is invalid

                        self.log_entries.append(row)
                self.update_log_display()
                print("Loaded log entries from CSV successfully!")
            except Exception as e:
                print(f"Error loading log entries from CSV: {e}")

    def export_to_csv(self):
        try:
            with open(self.csv_file, "w", newline="") as csvfile:
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
            bill_to_y = 6.5 * inch  # Starting y position for "Bill To:"
            line_height = 0.2 * inch  # Height for each line of text

            c.setFont("Helvetica-Bold", 12)
            c.drawString(inch, bill_to_y, "Bill To:")  # "Bill To:" label

            c.setFont("Helvetica", 10)
            c.drawString(
                inch, bill_to_y - line_height, self.client_name
            )  # Client Name
            c.drawString(
                inch, bill_to_y - 2 * line_height, self.client_address
            )  # Client Address

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
            self.save_invoice_number()  # Save the updated invoice number

        except Exception as e:
            print(f"Error exporting to PDF: {e}")

    def calculate_total_time(self):
        total_seconds = sum(entry["duration"] for entry in self.log_entries)
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        time_str = "{:02d}:{:02d}:{:02d}".format(
            int(hours), int(minutes), int(seconds)
        )
        self.total_time_label.configure(text=f"Total Time: {time_str}")

    def exit_app(self):
        self.root.destroy()
        sys.exit()


if __name__ == "__main__":
    app = TimeLogix()
    app.root.mainloop()
