import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import time
import csv
import datetime
from .components import create_label, create_entry, create_button, create_combo, create_text_box


class MainWindow(ctk.CTk):
    def __init__(self, db, pdf_exporter):
        super().__init__()
        self.db = db
        self.pdf_exporter = pdf_exporter
        self.title("TimeLogix")

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.font_family = "Segoe UI"
        self.font_size = 12

        self.is_running = False
        self.start_time = None
        self.elapsed_time = 0
        self.timer_id = None

        settings = self.db.load_settings()
        if settings:
            self.company_name = settings["company_name"]
            self.company_address = settings["company_address"]
            self.client_name = settings["client_name"]
            self.client_address = settings["client_address"]
            self.hourly_rate = settings["hourly_rate"]
            self.invoice_number = settings["invoice_number"]
        else:
            self.company_name = "Your Company Name"
            self.company_address = "123 Main St, Anytown, USA"
            self.client_name = "Client Name"
            self.client_address = "Client Address"
            self.hourly_rate = 60.00
            self.invoice_number = 1


        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=450, height=600)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.task_label = create_label(self.scrollable_frame, "Task Description:", self.font_family, self.font_size)
        self.task_label.pack(pady=(10, 2))
        self.task_entry = create_entry(self.scrollable_frame, width=250)
        self.task_entry.pack(pady=(2, 10))

        self.project_label = create_label(self.scrollable_frame, "Project:", self.font_family, self.font_size)
        self.project_label.pack(pady=(10, 2))
        self.projects = self.db.load_projects()
        self.project_combo = create_combo(self.scrollable_frame, values=self.projects, width=250)
        self.project_combo.pack(pady=(2, 10))
        if self.projects:
            self.project_combo.set(self.projects[0])

        self.time_label = create_label(self.scrollable_frame, "00:00:00", self.font_family, 36)
        self.time_label.pack(pady=(15, 20))
        self.start_stop_button = create_button(self.scrollable_frame, "Start", self.toggle_timer)
        self.start_stop_button.pack(pady=(5, 20))

        self.log_label = create_label(self.scrollable_frame, "Log Entries:", self.font_family, self.font_size)
        self.log_label.pack(pady=(10, 2))
        self.log_text = create_text_box(self.scrollable_frame, width=400, height=100, font=(self.font_family, self.font_size))
        self.log_text.pack(pady=5, padx=10, fill="both", expand=True)

        self.new_project_label = create_label(self.scrollable_frame, "New Project:", self.font_family, self.font_size)
        self.new_project_label.pack(pady=(10, 2))
        self.new_project_entry = create_entry(self.scrollable_frame, width=250)
        self.new_project_entry.pack(pady=(2, 10))
        self.add_project_button = create_button(self.scrollable_frame, "Add Project", self.add_project)
        self.add_project_button.pack(pady=(5, 15))

        button_frame = ctk.CTkFrame(self.scrollable_frame)
        button_frame.pack(pady=(10, 15))
        self.export_csv_button = create_button(button_frame, "Export to CSV", self.export_to_csv)
        self.export_csv_button.pack(side="left", padx=5, pady=5)
        self.export_pdf_button = create_button(button_frame, "Export to PDF", self.export_to_pdf)
        self.export_pdf_button.pack(side="left", padx=5, pady=5)
        self.exit_button = create_button(button_frame, "Exit", self.exit_app)
        self.exit_button.pack(side="left", padx=5, pady=5)

        self.total_time_button = create_button(self.scrollable_frame, "Calculate Total Time", self.calculate_total_time)
        self.total_time_button.pack(pady=(5, 15))
        self.total_time_label = create_label(self.scrollable_frame, "Total Time: 00:00:00", self.font_family, self.font_size)
        self.total_time_label.pack(pady=(5, 15))

        self.company_name_label = create_label(self.scrollable_frame, "Company Name:", self.font_family, self.font_size)
        self.company_name_label.pack(pady=(10, 2))
        self.company_name_entry = create_entry(self.scrollable_frame, width=250)
        self.company_name_entry.pack(pady=(2, 10))
        self.company_name_entry.insert(0, self.company_name)

        self.company_address_label = create_label(self.scrollable_frame, "Company Address:", self.font_family, self.font_size)
        self.company_address_label.pack(pady=(10, 2))
        self.company_address_entry = create_entry(self.scrollable_frame, width=250)
        self.company_address_entry.pack(pady=(2, 10))
        self.company_address_entry.insert(0, self.company_address)\

        self.client_name_label = create_label(self.scrollable_frame, "Client Name:", self.font_family, self.font_size)
        self.client_name_label.pack(pady=(10, 2))
        self.client_name_entry = create_entry(self.scrollable_frame, width=250)
        self.client_name_entry.pack(pady=(2, 10))
        self.client_name_entry.insert(0, self.client_name)

        self.client_address_label = create_label(self.scrollable_frame, "Client Address:", self.font_family, self.font_size)
        self.client_address_label.pack(pady=(10, 2))
        self.client_address_entry = create_entry(self.scrollable_frame, width=250)
        self.client_address_entry.pack(pady=(2, 10))
        self.client_address_entry.insert(0, self.client_address)

        self.hourly_rate_label = create_label(self.scrollable_frame, "Hourly Rate:", self.font_family, self.font_size)
        self.hourly_rate_label.pack(pady=(10, 2))
        self.hourly_rate_entry = create_entry(self.scrollable_frame, width=100)
        self.hourly_rate_entry.pack(pady=(2, 10))
        self.hourly_rate_entry.insert(0, str(self.hourly_rate))

        self.update_settings_button = create_button(self.scrollable_frame, "Update Settings", self.update_settings)
        self.update_settings_button.pack(pady=(15, 20))


        self.load_log_entries()

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
        self.after_cancel(self.timer_id)
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
            self.timer_id = self.after(100, self.update_timer)

    def log_time_entry(self):
        end_time = datetime.datetime.now()
        task_description = self.task_entry.get()
        project = self.project_combo.get()
        duration = self.elapsed_time
        start_time_str = end_time - datetime.timedelta(seconds=duration)

        project_id = self.db.get_project_id(project)
        if not project_id:
            print("Project not found in the database.")
            return

        self.db.insert_log_entry(
            task_description,
            project_id,
            start_time_str.strftime("%Y-%m-%d %H:%M:%S"),
            end_time.strftime("%Y-%m-%d %H:%M:%S"),
            duration,
        )

        self.load_log_entries()
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
        self.log_entries = self.db.load_log_entries()
        self.update_log_display()

    def add_project(self):
        new_project = self.new_project_entry.get().strip()
        if new_project and new_project not in self.projects:
            if self.db.add_project(new_project):
                self.projects.append(new_project)
                self.project_combo.configure(values=self.projects)
                self.project_combo.set(new_project)
                self.new_project_entry.delete(0, tk.END)
            else:
                print("Project already exists in the database.")
        elif new_project in self.projects:
            print("Project already exists.")
        else:
            print("Project name cannot be empty.")

    def update_settings(self):
        company_name = self.company_name_entry.get()
        company_address = self.company_address_entry.get()
        client_name = self.client_name_entry.get()
        client_address = self.client_address_entry.get()
        try:
            hourly_rate = float(self.hourly_rate_entry.get())
        except ValueError:
            print("Invalid hourly rate. Using default.")
            hourly_rate = 50.00

        self.db.update_settings(
            company_name, company_address, client_name, client_address, hourly_rate
        )

        self.company_name = company_name
        self.company_address = company_address
        self.client_name = client_name
        self.client_address = client_address
        self.hourly_rate = hourly_rate

    def export_to_csv(self):
        try:
            with open("working_sessions.csv", "w", newline="", encoding='utf-8') as csvfile:
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
            settings = self.db.load_settings()
            if settings:
                self.company_name = settings["company_name"]
                self.company_address = settings["company_address"]
                self.client_name = settings["client_name"]
                self.client_address = settings["client_address"]
                self.hourly_rate = settings["hourly_rate"]
                self.invoice_number = settings["invoice_number"]

            self.pdf_exporter.company_name = self.company_name
            self.pdf_exporter.company_address = self.company_address
            self.pdf_exporter.client_name = self.client_name
            self.pdf_exporter.client_address = self.client_address
            self.pdf_exporter.hourly_rate = self.hourly_rate
            self.pdf_exporter.invoice_number = self.invoice_number

            filename = f"invoice_{self.invoice_number}.pdf"
            self.pdf_exporter.export_to_pdf(self.log_entries, filename)

            self.invoice_number += 1
            self.db.save_invoice_number(self.invoice_number)
            self.db.conn.commit()
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
        self.destroy()


