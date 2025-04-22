from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
import datetime

class PDFExporter:
    def __init__(self, company_name, company_address, client_name, client_address, hourly_rate, invoice_number):
        self.company_name = company_name
        self.company_address = company_address
        self.client_name = client_name
        self.client_address = client_address
        self.hourly_rate = hourly_rate
        self.invoice_number = invoice_number

    def export_to_pdf(self, log_entries, filename):
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        
        header_table_data = [
            [
                Preformatted(f"BILL FROM:\n{self.company_name}\n{self.company_address}\n", styles['Normal']),
                Paragraph(f"INVOICE # {self.invoice_number}", styles['Heading1']),

            ],
            [
                Preformatted(f"BILL TO:\n{self.client_name}\n{self.client_address}\n", styles['Normal']),
                Paragraph(f"Invoice Date: {datetime.date.today().strftime('%m/%d/%Y')}", styles['Normal']),
            ],
        ]

        header_table_style = TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('ALIGN', (0, 1), (0, 1), 'LEFT'),
            ('ALIGN', (1, 1), (1, 1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ])

        header_table = Table(header_table_data, colWidths=[3*inch, 3*inch])
        header_table.setStyle(header_table_style)

        data = [["Date", "Project", "Hours", "Rate", "Total"]]
        total_amount = 0
        for entry in log_entries:
            hours = entry["duration"] / 3600
            line_total = hours * self.hourly_rate
            total_amount += line_total
            data.append([
                entry["start_time"].split(' ')[0],
                entry["project"],
                f"{hours:.2f}",
                f"${self.hourly_rate:.2f}",
                f"${line_total:.2f}",
            ])
            
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table = Table(data)
        table.setStyle(table_style)

        totals_style = ParagraphStyle(name='Totals', fontSize=10, alignment=TA_RIGHT)
        subtotal = Paragraph(f"Subtotal: ${total_amount:.2f}", totals_style)
        tax = Paragraph(f"Tax (0%): $0.00", totals_style)
        total = Paragraph(f"Total: ${total_amount:.2f}", totals_style)

        notes_style = ParagraphStyle(name='Notes', fontSize=10, alignment=TA_LEFT)
        notes = Paragraph("Notes:\nThank you for your business!", notes_style)

        elements = [
            header_table,
            Spacer(1, 12),
            table,
            Spacer(1, 12),
            subtotal,
            tax,
            total,
            Spacer(1, 12),
            notes,
        ]

        doc.build(elements)
