import sys
from database import Database
from pdf_exporter import PDFExporter
from ui.main_window import MainWindow


def main():
    db = Database()
    pdf_exporter = PDFExporter()
    app = MainWindow(db, pdf_exporter)

    def on_closing():
        db.close()
        app.destroy()  # Properly destroy the Tkinter window
        sys.exit()

    app.protocol("WM_DELETE_WINDOW", on_closing)  # Handle window closing
    app.mainloop()


if __name__ == "__main__":
    main()
