# timelogix/database.py
import sqlite3


class Database:
    def __init__(self, db_file="timelogix.db"):
        self.db_file = db_file
        self.conn = None  # Initialize conn to None
        self.cursor = None  # Initialize cursor to None
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
            self.create_tables()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            # Handle the error appropriately, e.g., exit or disable DB features

    def create_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS log_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT,
                project_id INTEGER,
                start_time TEXT,
                end_time TEXT,
                duration REAL,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )
        """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT,
                company_address TEXT,
                client_name TEXT,
                client_address TEXT,
                hourly_rate REAL,
                invoice_number INTEGER
            )
        """
        )
        # Check if settings exist, if not create
        self.cursor.execute("SELECT COUNT(*) FROM settings")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute(
                """
                INSERT INTO settings (company_name, company_address, client_name, client_address, hourly_rate, invoice_number)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    "Your Company Name",  # Default company name
                    "123 Main St, Anytown, USA",  # Default company address
                    "Client Name",  # Default client name
                    "Client Address",  # Default client address
                    60.00,  # Default hourly rate
                    1,
                ),
            )  # Start invoice number at 1
        self.conn.commit()

    def load_projects(self):
        self.cursor.execute("SELECT name FROM projects")
        projects = [row[0] for row in self.cursor.fetchall()]
        return projects

    def save_projects(self, projects):
        for project in projects:
            try:
                self.cursor.execute(
                    "INSERT INTO projects (name) VALUES (?)", (project,)
                )
            except sqlite3.IntegrityError:
                pass  # Ignore if project already exists
        self.conn.commit()

    def load_invoice_number(self):
        self.cursor.execute("SELECT invoice_number FROM settings")
        invoice_number = self.cursor.fetchone()[0]
        return invoice_number

    def save_invoice_number(self, invoice_number):
        self.cursor.execute("UPDATE settings SET invoice_number = ?", (invoice_number,))
        self.conn.commit()

    def add_project(self, project_name):
        try:
            self.cursor.execute(
                "INSERT INTO projects (name) VALUES (?)", (project_name,)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Project already exists

    def get_project_id(self, project_name):
        self.cursor.execute("SELECT id FROM projects WHERE name = ?", (project_name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def insert_log_entry(self, task, project_id, start_time, end_time, duration):
        self.cursor.execute(
            """
            INSERT INTO log_entries (task, project_id, start_time, end_time, duration)
            VALUES (?, ?, ?, ?, ?)
        """,
            (task, project_id, start_time, end_time, duration),
        )
        self.conn.commit()

    def load_log_entries(self):
        self.cursor.execute(
            """
            SELECT log_entries.task, projects.name, log_entries.start_time,
                   log_entries.end_time, log_entries.duration
            FROM log_entries
            JOIN projects ON log_entries.project_id = projects.id
        """
        )
        rows = self.cursor.fetchall()
        log_entries = []
        for row in rows:
            task, project, start_time, end_time, duration = row
            entry = {
                "task": task,
                "project": project,
                "start_time": start_time,
                "end_time": end_time,
                "duration": duration,
            }
            log_entries.append(entry)
        return log_entries

    def update_settings(
        self, company_name, company_address, client_name, client_address, hourly_rate
    ):
        self.cursor.execute(
            """
            UPDATE settings SET
            company_name = ?, company_address = ?, client_name = ?,
            client_address = ?, hourly_rate = ?
        """,
            (company_name, company_address, client_name, client_address, hourly_rate),
        )
        self.conn.commit()

    def load_settings(self):
        self.cursor.execute("SELECT * FROM settings")
        settings = self.cursor.fetchone()
        if settings:
            (
                _,
                company_name,
                company_address,
                client_name,
                client_address,
                hourly_rate,
                invoice_number,
            ) = settings
            return {
                "company_name": company_name,
                "company_address": company_address,
                "client_name": client_name,
                "client_address": client_address,
                "hourly_rate": hourly_rate,
                "invoice_number": invoice_number,
            }
        else:
            return None

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
