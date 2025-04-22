import sys
from database import Database
from pdf_exporter import PDFExporter
from ui.main_window import MainWindow


def main():
    db = Database()
    settings = db.load_settings()
    if settings:
        pdf_exporter = PDFExporter(
            settings["company_name"],
            settings["company_address"],
            settings["client_name"],
            settings["client_address"],
            settings["hourly_rate"],
            settings["invoice_number"],
        )
    else:
        pdf_exporter = PDFExporter(
            "Your Company Name",
            "123 Main St, Anytown, USA",
            "Client Name",
            "Client Address",
            60.00,
            1,
        )

    app = MainWindow(db, pdf_exporter)

    def on_closing():
        db.close()
        app.destroy()
        sys.exit()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()


if __name__ == "__main__":
    main()
