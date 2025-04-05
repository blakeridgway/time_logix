# timelogix/pdf_exporter.py
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


class PDFExporter:
    def __init__(self):
        self.company_name = "Your Company Name"
        self.company_address = "123 Main St, Anytown, USA"
        self.client_name = "Client Name"
        self.client_address = "Client Address"
        self.hourly_rate = 60.00
        self.invoice_number = 1

    def export_to_pdf(self, log_entries):
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

            for entry in log_entries:
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

        except Exception as e:
            print(f"Error exporting to PDF: {e}")
