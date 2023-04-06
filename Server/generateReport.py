from reportlab.pdfgen import canvas
from datetime import datetime
date = "ATTENDANCE REPORT"+"\n DATE -"+str(datetime.now())


class generate:
    def report(data):
        pdf = canvas.Canvas("report.pdf")
        y = 700  # starting y-coordinate
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(100, 800, date)
        pdf.setFont("Helvetica", 12)
        line_height = 20  # height of each line
        for key, value in data.items():
            text = f"{key}: {value}"
            pdf.drawString(100, y, text)
            y -= 20

        pdf.save()
